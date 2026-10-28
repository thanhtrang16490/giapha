import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=name=>JSON.parse(readFileSync(new URL(`../data_json/${name}.json`,import.meta.url)));
const people=read('people'),byId=new Map(people.map(p=>[p.id,p])),houses=read('households'),issues=read('review-issues');
const branchPerson=(name,branch)=>{const matches=people.filter(p=>p.name===name&&p.branch===branch);assert.equal(matches.length,1,`Identity ambiguous: ${name}`);return matches[0]};
test('Cành 1 preserves seven consecutive generations with repeated household appearances merged',()=>{
 const b='Cành 1 · Ngành trưởng';let parent=byId.get('tuyet');
 for(const name of ['Lại Thế Tề','Lại Thế Tế','Lại Thế Luận','Lại Thế Thinh','Lại Thế Đức']){const child=branchPerson(name,b);assert.equal(child.parentId,parent.id);assert.equal(child.generation,parent.generation+1);parent=child}
 assert.equal(branchPerson('Lại Nguyễn Toàn',b).relationshipType,'adopted');
 assert.equal(branchPerson('Lại Nguyễn Toan',b).parentId,branchPerson('Lại Nguyễn Toàn',b).id);
});
test('All seven detailed branches attach to the documented common lineage',()=>{
 for(const id of ['tuyet','xuan','sanh','hoa','trap']){assert.equal(byId.get(id).parentId,'dam');assert(people.some(p=>p.parentId===id))}
 for(const id of ['da','truong']){assert.equal(byId.get(id).parentId,'huong');assert(people.some(p=>p.parentId===id))}
 assert.equal(byId.get('truong').branch,'Cành 2 · Ngành thứ');assert.notEqual(byId.get('dai').branch,byId.get('truong').branch);
});
test('Diagram-backed spelling variants merge without losing their evidence',()=>{
 const b='Cành 4 · Ngành trưởng',child=branchPerson('Lại Văn Triệu',b),parent=branchPerson('Lại Thế Mao',b);
 assert.equal(child.parentId,parent.id);assert(child.sources.some(s=>s.page===90&&s.kind==='manually_checked_diagram'));
 assert(child.sources.some(s=>s.nameInSource==='Lại Thế Triệu'));assert.equal(child.relationshipStatus,'needs_review');
 assert.equal(people.filter(p=>p.name==='Lại Thế Triệu'&&p.branch===b).length,0);
});
test('Unproven links and duplicated household numbers do not silently combine identities',()=>{
 assert.equal(byId.get('nan').parentId,null);assert.equal(byId.get('ngap').parentId,null);
 const duplicates=houses.filter(h=>h.code==='nt2'&&h.number===125);assert.equal(duplicates.length,2);
 const thuy=people.find(p=>p.id===duplicates.find(h=>h.head.name==='Lại Thế Thủy').id);assert.equal(thuy.parentId,null);
 const hai=people.find(p=>p.id==='nt2-house-108-107');assert.equal(hai.parentId,null);assert(issues.some(i=>i.personId===hai.id&&i.type==='unresolved_parent'));
});
test('Every graph link has a valid source, valid endpoint and no ancestral cycle',()=>{
 assert.equal(byId.size,people.length);assert(people.length>1200);
 for(const p of people){assert(p.page>=1&&p.page<=171);assert(p.generation>=10&&p.generation<=23);assert(p.sources.length);
  for(const s of p.sources)assert(s.page>=1&&s.page<=171);
  if(p.parentId){assert(byId.has(p.parentId));if(p.relationshipStatus!=='needs_review')assert.equal(p.generation,byId.get(p.parentId).generation+1,`${p.name}: generation mismatch must be flagged`)}
  const seen=new Set([p.id]);let next=p;while(next.parentId){assert(!seen.has(next.parentId));seen.add(next.parentId);next=byId.get(next.parentId)}
 }
 for(const p of people.filter(p=>p.relationshipStatus==='needs_review'))assert(issues.some(i=>i.personId===p.id),`Missing review evidence: ${p.id}`);
});
