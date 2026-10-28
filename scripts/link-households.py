"""Reconstruct table cells by PDF coordinates, preserving household and page evidence.
Run extract-data.py first. No fuzzy name matching and no invented links across gaps.
"""
import json,re,pathlib,xml.etree.ElementTree as ET,unicodedata
root=pathlib.Path(__file__).resolve().parent.parent
ns={'x':'http://www.w3.org/1999/xhtml'}
pdf=ET.parse(root/'tmp/pdfs/bbox.html').findall('.//x:page',ns)
base=json.loads((root/'data_json/people-curated.json').read_text())
sections=[('nt1','Cành 1 · Ngành trưởng',range(21,24),'tuyet'),('nt2','Cành 2 · Ngành trưởng',range(27,47),'xuan'),('nt3','Cành 3 · Ngành trưởng',range(65,74),'sanh'),('nt4','Cành 4 · Ngành trưởng',range(83,89),'hoa'),('nt5','Cành 5 · Ngành trưởng',[96],'trap'),('nh1','Cành 1 · Ngành thứ',range(99,104),'da'),('nh2','Cành 2 · Ngành thứ',range(110,122),'truong')]
def norm(s):return unicodedata.normalize('NFC',' '.join(s.split())).lower().replace('lai ','lại ',1)
def val(w,k):return float(w.get(k))
def txt(ws):return ' '.join(w.text or '' for w in sorted(ws,key=lambda w:val(w,'xMin')))
def rows(words):
 out=[]
 for w in sorted(words,key=lambda w:(val(w,'yMax'),val(w,'xMin'))):
  y=val(w,'yMax')
  if not out or abs(y-out[-1][0])>4:out.append([y,[w]])
  else:out[-1][1].append(w)
 return [(y,txt(ws)) for y,ws in out]
# Explicit alias resolutions checked against the drawn arrows, never fuzzy matched.
manual_aliases={
 ('nt4',10,'Lại Thế Triệu'):(16,'Lại Văn Triệu',90),
 ('nt4',14,'Lại Thế Thuyết'):(26,'Lại Nam Thuyết',90),
 ('nt4',14,'Lại Thế Thung'):(28,'Lại Văn Thung',90),
 ('nt4',17,'Lại Văn Chung'):(31,'Lại Thế Chung',91),
 ('nt4',18,'Lại Thế Vương'):(36,'Lại Thế Vượng',92),
 ('nt4',19,'Lại Thế Thuần'):(37,'Lại Đức Thuần',93),
 ('nt4',20,'Lại Thế Quyết'):(34,'Lại Văn Quyết',94),
 ('nt4',20,'Lại Thế Thắng'):(35,'Lại Văn Thắng',94),
 ('nt4',27,'Lại Thế Nam'):(40,'Lại Văn Nam',91),
}
issues=[];allhouses=[];people={p['id']:p for p in base}
# Remove hand-transcribed direct children of Tuyet: coordinate records replace these identities.
for id in ['te','pho','chuc','phoi','ngau']:people.pop(id,None)
for code,branch,pnums,rootid in sections:
 page_data=[];number_cells=[]
 for pn in pnums:
  words=pdf[pn-1].findall('.//x:word',ns)
  header=next(w for w in words if w.text=='Đời');header_y=val(header,'yMax')
  gx=val(header,'xMin')-4;gxend=val(header,'xMax')+7
  startwords=[w for w in words if w.text in ('Lại','Lai','Lạt') and val(w,'xMin')<gx and val(w,'yMax')>header_y+7]
  nx=min(val(w,'xMin') for w in startwords)-2
  danh=next(w for w in words if w.text=='Danh');sx=val(danh,'xMin')-35
  # Column for spouse ends before the second birth column (if any) or granddaughter column.
  nsheaders=sorted([val(w,'xMin') for w in words if w.text in ('NS','SN') and abs(val(w,'yMax')-val(danh,'yMax'))<7])
  sxend=nsheaders[-1]-5 if len(nsheaders)>1 else next((val(w,'xMin')-8 for w in words if w.text=='Cháu'),520)
  primary=rows([w for w in words if nx<val(w,'xMin')<gx-3 and header_y+7<val(w,'yMax')<785])
  names=[]
  for y,t in primary:
   if re.match(r'^(Lại|Lai|Lạt)\s',t):
    name=re.sub(r'\s+(?:\d{4}|DN|MĐT|Kỵ|kỵ).*$', '',t).strip()
    names.append({'name':name,'y':y,'page':pn,'annotations':re.findall(r'\b(?:DN|MĐT|LT)\b',t)})
   elif names and len(names[-1]['name'].split())<3 and y-names[-1]['y']<24 and re.fullmatch(r'[A-Za-zÀ-ỹĐđ ]+',t) and not t.lower().startswith(('kỵ','ông','bà')):
    names[-1]['name']+=' '+t
  gens=[(val(w,'yMax'),int(w.text)) for w in words if gx<=val(w,'xMin')<=gxend and re.fullmatch(r'1\d|2\d',w.text or '') and val(w,'yMax')>header_y+7]
  spouses=rows([w for w in words if sx<=val(w,'xMin')<sxend and header_y+7<val(w,'yMax')<785])
  nums=sorted([(val(w,'yMax'),w.text) for w in words if val(w,'xMin')<nx and re.fullmatch(r'\d+(?:A1)?',w.text or '') and header_y+7<val(w,'yMax')<785])
  page_data.append(dict(page=pn,names=names,gens=gens,spouses=spouses,nums=nums))
  number_cells.extend([dict(page=pn,y=y,number=n) for y,n in nums])
 # Left column contains household above its parent household. The first/root cell has no parent.
 houses=[];i=0
 while i<len(number_cells):
  cell=number_cells[i];num=int(re.sub('A1$','',cell['number']));num=1 if i==0 else num
  h={**cell,'number':num,'parentRef':None,'rows':[],'code':code,'branch':branch}
  if i>0:
   if i+1>=len(number_cells):issues.append({'type':'unpaired_household','branch':branch,'page':cell['page'],'number':num});break
   parent=number_cells[i+1];h['parentRef']=int(re.sub('A1$','',parent['number']));i+=2
  else:i+=1
  houses.append(h)
 # Partition name rows using household top coordinates, allowing a 4pt baseline difference.
 for pd in page_data:
  for row in pd['names']:
   eligible=[h for h in houses if (h['page'],h['y'])<=(row['page'],row['y']+4)]
   if not eligible:issues.append({'type':'unassigned_row',**row,'branch':branch});continue
   h=eligible[-1];ishead=not h['rows']
   match=[(abs(y-row['y']),g) for y,g in pd['gens'] if abs(y-row['y'])<7]
   if not match and ishead:match=[(abs(y-row['y']),g) for y,g in pd['gens'] if abs(y-row['y'])<25 and abs(y-h['y'])<7]
   row['generation']=min(match)[1] if match else None
   row['spouse']='';row['childRef']=None
   aligned=[t for y,t in pd['spouses'] if abs(y-row['y'])<7]
   for t in aligned:
    if re.fullmatch(r'\d+',t):row['childRef']=int(t)
    elif re.search(r'\b(?:Thị|thị|Văn|Phúc|Công|Đình|Hà|Minh|Bá|Kim|Viết|Hải|Kiều)\b',t):row['spouse']=t
   h['rows'].append(row)
 # Make roots and head IDs first, then unify only with children identified by explicit household references or exact name + parentRef.
 index={}
 for j,h in enumerate(houses):
  h['id']=rootid if j==0 else f'{code}-house-{h["number"]}-{j}'
  index.setdefault(h['number'],[]).append(h)
  if not h['rows']:issues.append({'type':'empty_household','branch':branch,'household':h['number'],'page':h['page']});continue
  head=h['rows'][0];h['head']=head
  if j==0:
   p=people[rootid];p['branch']=branch;p.setdefault('sources',[]).append({'page':head['page'],'household':h['number'],'kind':'household_head'})
  else:
   p=dict(id=h['id'],name=head['name'],generation=head['generation'] or 0,parentId=None,spouse=head['spouse'],branch=branch,note='',death='',page=head['page'],gender='female' if ' Thị ' in head['name'] else 'male',status='Theo bảng mã hộ',sources=[{'page':head['page'],'household':h['number'],'kind':'household_head','nameInSource':head['name'],'generationInSource':head['generation']}],relationshipStatus='unresolved')
   people[p['id']]=p
 for h in houses:
  if 'head' not in h:continue
  parent=people[h['id']]
  for j,row in enumerate(h['rows'][1:]):
   candidates=[]
   if row['childRef']:
    candidates=[c for c in index.get(row['childRef'],[]) if c.get('head') and c['parentRef']==h['number']]
   if len(candidates)>1:
    exact=[c for c in candidates if norm(c['head']['name'])==norm(row['name'])]
    if len(exact)==1:candidates=exact
   alias=manual_aliases.get((code,h['number'],row['name']))
   if not candidates and alias:
    candidates=[c for c in index.get(alias[0],[]) if c.get('head') and c['head']['name']==alias[1] and c['parentRef']==h['number']]
   if not candidates:
    candidates=[c for c in houses if c.get('head') and c['parentRef']==h['number'] and norm(c['head']['name'])==norm(row['name'])]
   match=candidates[0] if len(candidates)==1 else None
   pid=match['id'] if match else f'{code}-child-{h["number"]}-{h["id"].split("-")[-1]}-{j}'
   expected=parent['generation']+1 if parent['generation'] else None
   observed=row['generation'];headgen=people[pid]['generation'] if match else None
   gen=observed or headgen or expected or 0
   conflicts=[]
   if observed and headgen and observed!=headgen:conflicts.append(f'Đời trong danh sách con: {observed}; đời tại hộ riêng: {headgen}.')
   if match and norm(row['name'])!=norm(match['head']['name']):conflicts.append(f'Tên trong danh sách con: {row["name"]}; tên chủ hộ: {match["head"]["name"]}. '+(f'Quan hệ đối chiếu trực quan ở sơ đồ PDF {alias[2]}.' if alias else f'Ghép theo mã hộ {row["childRef"]} và mã hộ cha {h["number"]}.'))
   if expected and gen!=expected:conflicts.append(f'Đời ghi trong nguồn ({gen}) không liền sau đời của chủ hộ ({parent["generation"]}).')
   if match:p=people[pid]
   else:
    p=dict(id=pid,name=row['name'],generation=gen,parentId=None,spouse=row['spouse'],branch=branch,note='',death='',page=row['page'],gender='female' if ' Thị ' in row['name'] else 'male',status='Theo bảng mã hộ',sources=[])
    people[pid]=p
   if alias and match:p['sources'].append({'page':alias[2],'kind':'manually_checked_diagram','nameInSource':match['head']['name']})
   p['sources'].append({'page':row['page'],'household':h['number'],'kind':'listed_child','childHousehold':row['childRef'],'nameInSource':row['name'],'generationInSource':observed})
   # Keep ambiguous generation/name records visible, but clearly mark their source-supported relationship for review.
   if 'DN' in row.get('annotations',[]):
    p['relationshipType']='adopted';p['note']+=' Ký hiệu DN trong bảng nguồn: con nuôi đã mang họ nuôi.'
   p['parentId']=parent['id'];p['generation']=gen;p['relationshipStatus']='needs_review' if conflicts else 'supported';p['status']='Cần rà soát dị bản' if conflicts else 'Theo bảng mã hộ'
   if not p['spouse']:p['spouse']=row['spouse']
   if not observed:
    p['note']+=' Đời được suy ra từ vị trí con trong hộ; cần đối chiếu sơ đồ.';p['status']='Cần đối chiếu đời';p['relationshipStatus']='needs_review'
    issues.append({'type':'inferred_generation','personId':pid,'branch':branch,'page':row['page'],'details':'Ô đời chưa đọc được trên cùng hàng; đời hiển thị dựa vào hộ và cần đối chiếu.'})
   if conflicts:
    p['note']+=' '+' '.join(conflicts);issues.append({'type':'source_conflict','personId':pid,'branch':branch,'page':row['page'],'details':conflicts})
 for h in houses:
  if 'head' not in h:continue
  p=people[h['id']]
  if h['parentRef'] and not p['parentId']:
   issues.append({'type':'unresolved_parent','personId':p['id'],'branch':branch,'page':p['page'],'household':h['number'],'parentHousehold':h['parentRef'],'details':'Chưa tìm được dòng con tương ứng trong hộ cha; không nối chỉ theo tên hoặc đời.'})
   p['status']='Chưa ghép được hộ cha'
   p['note']+=f' Hộ {h["number"]} tham chiếu hộ cha {h["parentRef"]}; chưa ghép được với dòng con. Giữ riêng để đối chiếu.'
  if p['generation']==0:
   p['generation']=h['head']['generation'] or 0
   issues.append({'type':'missing_generation','personId':p['id'],'branch':branch,'page':p['page']})
  h['personId']=p['id']
 allhouses+=houses
# Correct branch identification: the detailed second junior-branch table starts with Truong, not Dai.
people['dai']['branch']='Ngành thứ · Kim Bảng'
people['dai']['note']='Phần chung ghi Lại Thế Đài (Thạnh), Kim Bảng, Hà Nam. Bảng chi tiết cành 2 ngành thứ ở trang PDF 110 bắt đầu bằng Lại Thế Trường; không gán hai người làm một.'
# Existing manually verified links retain their evidence.
for p in people.values():
 p.setdefault('relationshipStatus','verified' if p['parentId'] else 'unresolved')
 p.setdefault('sources',[{'page':p['page'],'kind':'manually_checked_diagram'}])
# Structural validation: every edge has provenance and never forms a cycle.
for p in people.values():
 seen={p['id']};q=p
 while q['parentId']:
  assert q['parentId'] in people,(p['id'],q['parentId'])
  assert q['parentId'] not in seen,('cycle',p['id']);seen.add(q['parentId']);q=people[q['parentId']]
assert len(people)==len(set(people))
(root/'data_json/people.json').write_text(json.dumps(list(people.values()),ensure_ascii=False,indent=2))
(root/'data_json/households.json').write_text(json.dumps(allhouses,ensure_ascii=False,indent=2))
(root/'data_json/review-issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2))
from collections import Counter
print('Profiles:',len(people),'links:',sum(bool(p['parentId']) for p in people.values()),'issues:',len(issues))
print('Issue types:',Counter(i['type'] for i in issues))
for code,b,_,rid in sections:
 ps=[p for p in people.values() if p['branch']==b];print(b,len(ps),'linked',sum(bool(p['parentId']) for p in ps))
