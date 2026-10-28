import {basePeople,mergedPeople,readState,importPeople,importId} from '@/lib/family-store';
import {readPeopleWorkbook} from '@/lib/family-workbook';
import {planPeopleImport} from '@/lib/family-import.mjs';
import {FamilyError} from '@/lib/family-domain.mjs';
export const runtime='nodejs';export const dynamic='force-dynamic';
export async function POST(request:Request){try{
 const origin=request.headers.get('origin');if(origin&&new URL(origin).host!==request.headers.get('host'))throw new FamilyError('Yêu cầu không hợp lệ.',403);
 const form=await request.formData(),file=form.get('file'),mode=form.get('mode');if(!(file instanceof File)||!file.name.toLowerCase().endsWith('.xlsx')||file.size>5*1024*1024)throw new FamilyError('Chọn tệp XLSX tối đa 5 MB.');
 const bytes=new Uint8Array(await file.arrayBuffer());if(bytes[0]!==80||bytes[1]!==75)throw new FamilyError('Tệp không phải XLSX hợp lệ.');
 const rows=await readPeopleWorkbook(bytes);const current=await readState();if(rows.some(row=>current.archivedPeople.includes(String(row['Mã']))||current.archivedPeople.includes(importId(String(row['Mã'])))))throw new FamilyError('Tệp có hồ sơ đang lưu trữ. Khôi phục hồ sơ trước khi nhập.');if(mode==='apply'){const result=await importPeople(rows,Number(form.get('revision')));return Response.json(result)}
 if(mode!=='preview')throw new FamilyError('Thao tác nhập không hợp lệ.');const [base,state]=await Promise.all([basePeople(),readState()]);const plan=planPeopleImport(rows,mergedPeople(base,state),importId);
 return Response.json({revision:state.revision,total:plan.total,created:plan.created,updated:plan.updated,unchanged:plan.unchanged,errors:plan.errors,changes:plan.changes.map(c=>({key:c.key,name:c.input.name,kind:c.kind,row:c.row,fields:c.fields}))},{headers:{'Cache-Control':'no-store'}});
 }catch(e){const error=e as Error&{status?:number};return Response.json({error:error.status?error.message:'Chưa đọc được tệp Excel.'},{status:error.status||500})}}
