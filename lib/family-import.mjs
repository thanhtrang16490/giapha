import {FamilyError,validatePerson} from './family-domain.mjs';
export const importColumns={name:'Họ tên',generation:'Đời',gender:'Giới tính',branch:'Cành',spouse:'Phối ngẫu ghi nguồn',birthDate:'Ngày sinh',deathDate:'Ngày mất',death:'Húy kỵ âm lịch',phone:'Điện thoại',email:'Email',address:'Địa chỉ',occupation:'Nghề nghiệp',biography:'Tiểu sử',note:'Ghi chú',parentId:'Mã cha/mẹ chính',motherId:'Mã cha/mẹ thứ hai',spouseIds:'Mã phối ngẫu',relationshipType:'Loại quan hệ con'};
/** Every relationship uses an explicit ID. Absent columns preserve existing fields. Empty cells clear fields. */
export function planPeopleImport(rows,people,idForNew){
 if(!Array.isArray(rows)||!rows.length||rows.length>3000)throw new FamilyError('Tệp cần từ 1 đến 3.000 dòng hồ sơ.');
 const byId=new Map(people.map(p=>[p.id,p])),seen=new Set(),external=new Map();
 for(const row of rows){const key=String(row['Mã']||'').trim();if(!/^[a-zA-Z0-9_-]{1,100}$/.test(key)||['__proto__','constructor','prototype'].includes(key))throw new FamilyError(`Dòng ${row._row}: Mã không hợp lệ hoặc bỏ trống.`);if(seen.has(key))throw new FamilyError(`Dòng ${row._row}: Mã ${key} bị trùng.`);seen.add(key);external.set(key,byId.has(key)?key:idForNew(key));}
 const errors=[];/** @type {any[]} */ const changes=[];
 for(const row of rows){const key=String(row['Mã']).trim(),id=external.get(key),previous=byId.get(id);try{
  const input={name:'',generation:1,gender:'unknown',parentId:null,motherId:null,spouseIds:[],spouse:'',branch:'Chưa phân cành',death:'',note:'',...previous};
  for(const [field,header] of Object.entries(importColumns))if(Object.hasOwn(row,header)){
   const value=String(row[header]??'').trim();if(field==='generation')input[field]=Number(value);
   else if(field==='gender'){const values={nam:'male',male:'male',nữ:'female',female:'female',unknown:'unknown','chưa xác định':'unknown','':'unknown'};input[field]=values[value.toLowerCase()]||value;}
   else if(field==='spouseIds')input[field]=value?value.split(/[,;\n]/).map(x=>x.trim()).filter(Boolean).map(x=>external.get(x)||x):[];
   else if(field==='parentId'||field==='motherId')input[field]=value?(external.get(value)||value):null;
   else input[field]=value;
  }
  const normalized=(field,value)=>typeof value==='string'?value.trim():value??(field==='spouseIds'?[]:['parentId','motherId'].includes(field)?null:'');
  const fields=Object.keys(importColumns).filter(field=>Object.hasOwn(row,importColumns[field])&&JSON.stringify(normalized(field,input[field]))!==JSON.stringify(normalized(field,previous?.[field])));
  if(!previous||fields.length)changes.push({data:/** @type {Record<string, any>} */ ({}),id,key,row:row._row,kind:previous?'update':'create',input,fields});
 }catch(error){errors.push(`Dòng ${row._row}: ${error.message}`)}}
 const merged=new Map(byId);for(const change of changes)merged.set(change.id,{...change.input,id:change.id});const candidates=[...merged.values()];
 for(const change of changes)try{
  const previous=byId.get(change.id);for(const field of ['parentId','motherId']){const parent=merged.get(change.input[field]);if(parent&&(!previous||previous[field]!==parent.id||previous.generation!==change.input.generation||byId.get(parent.id)?.generation!==parent.generation)&&parent.generation>=change.input.generation)throw new FamilyError('Đời của con phải lớn hơn đời cha/mẹ.');}
  change.data=validatePerson(change.input,candidates,change.id);
 }catch(error){errors.push(`Dòng ${change.row} (${change.input.name||change.key}): ${error.message}`)}
 // Generation changes can invalidate a child omitted from the workbook.
 for(const change of changes)if(byId.get(change.id)?.generation!==change.input.generation)for(const child of candidates)if([child.parentId,child.motherId].includes(change.id)&&child.generation<=change.input.generation)errors.push(`Dòng ${change.row}: đời mới không nhỏ hơn đời của ${child.name}.`);
 return {total:rows.length,created:changes.filter(c=>c.kind==='create').length,updated:changes.filter(c=>c.kind==='update').length,unchanged:rows.length-changes.length,errors:errors.slice(0,100),changes};
}
