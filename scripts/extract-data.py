import json,re,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
pages=(root/'tmp/pdfs/source.txt').read_text().split('\f')
if not pages[-1].strip(): pages.pop()
records=[]
for page,text in enumerate(pages,1):
 if page==15: branch='Phần chung'
 elif 21<=page<=23: branch='Cành 1 · Ngành trưởng'
 elif 27<=page<=46: branch='Cành 2 · Ngành trưởng'
 elif 65<=page<=73: branch='Cành 3 · Ngành trưởng'
 elif 83<=page<=88: branch='Cành 4 · Ngành trưởng'
 elif page==96: branch='Cành 5 · Ngành trưởng'
 elif 99<=page<=103: branch='Cành 1 · Ngành thứ'
 elif 110<=page<=121: branch='Cành 2 · Ngành thứ'
 else: continue
 for line in text.splitlines():
  m=re.search(r'(Lại\s+(?:[A-ZÀ-ỸĐa-zà-ỹđ]+\s+){1,4}?)\s+(1[0-9]|2[0-5])(?:\s|$)',line)
  if not m: continue
  name=' '.join(m[1].split()); gen=int(m[2]); rest=line[m.end():].strip()
  if any(x['name']==name and x['generation']==gen and x['page']==page for x in records):continue
  records.append(dict(id=f'record-{len(records)+1}',name=name,generation=gen,branch=branch,page=page,details=rest,raw=line.strip(),status='Cần đối chiếu'))
(root/'data_json/records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(root/'data_json/pages.json').write_text(json.dumps([dict(page=i+1,text=t.strip()) for i,t in enumerate(pages)],ensure_ascii=False))
people=[]
def add(id,name,generation,parent=None,spouse='',branch='Phần chung',note='',death='',page=20):
 people.append(dict(id=id,name=name,generation=generation,parentId=parent,spouse=spouse,branch=branch,note=note,death=death,page=page,gender='female' if ' Thị ' in name else 'male',status='Đã đối chiếu phần chung'))
add('ngap','Lại Thế Ngập',10,spouse='Hoàng Thị Hàng',note='Thủy tổ họ Lại chi Diêm Điền. Tên tự: Đán. Phả ghi là con thứ hai của Đức cao tổ Lại Thế Thành. Chưa nối quan hệ trực tiếp tới đời 12 vì tài liệu có khoảng trống đời 11.',death='16/3',page=15)
for id,name in [('phuctu','Phúc Tư'),('vietanh','Viết Ảnh'),('chinhtruc','Chính Trực'),('congchinh','Công Chính'),('canman','Cần Mẫn'),('minhchinh','Minh Chính'),('anhoa','An Hòa'),('vietthan','Viết Thận')]:
 add(id,'Lại '+name,11,'ngap',note='Đối chiếu trực quan phả đồ trang PDF 19. Bảng trang 15 ghi tên Lại Minh Chín thay cho Lại Minh Chính.' if id=='minhchinh' else 'Đối chiếu trực quan phả đồ trang PDF 19.',page=19)
add('nan','Lại Thế Năn',12,spouse='Nguyễn Thị Hành',note='Thế tổ. Phần chung ghi các hậu duệ đời 13; đối chiếu phả đồ ở trang PDF 19.',death='19/4',page=19)
add('dam','Lại Thế Đằm',13,'nan','Lê Thị Hoan','Ngành trưởng','Tổ ngành trưởng chi Diêm Điền.', '4/9',19)
add('huong','Lại Thế Hương',13,'nan','Đặng Thị Quý','Ngành thứ','Tổ ngành thứ. Tên phối ngẫu được ghi là Quỳ ở bảng trang 15 và Quý ở phả đồ trang 19–20.',page=19)
add('thuan','Lại Thị Thuận',13,'nan','Nguyễn Phúc Hoàn',page=19)
add('lanh','Lại Thị Lành',13,'nan','Hoàng Công Huấn',page=19)
for id,name,spouse,c in [('tuyet','Tuyết','Vũ Thị Kim',1),('xuan','Xuân','Nguyễn Thị Tại; Nguyễn Thị Linh',2),('sanh','Sành','Nguyễn Thị Thậm; Phạm Thị Tắc',3),('hoa','Hỏa','Nguyễn Thị Lành; Vũ Thị Nhu',4),('trap','Tráp','Nguyễn Thị Sự; Nguyễn Thị Hòn',5)]:
 add(id,'Lại Thế '+name,14,'dam',spouse,f'Cành {c} · Ngành trưởng',f'Cụ tổ cành {c}, ngành trưởng. Các dị bản tên trong bảng và phả đồ cần được ban tu phả xác nhận.')
for id,name in [('mong','Mộng'),('suong','Sương'),('hop','Hợp'),('chop','Chớp'),('hoathi','Hòa')]:add(id,'Lại Thị '+name,14,'dam',branch='Ngành trưởng',note='Theo phả đồ phần chung.',page=19)
for id,name,spouse,branch in [('da','Đa','Nguyễn Thị Kiệm','Cành 1 · Ngành thứ'),('truong','Trường','Bùi Thị Trữ','Ngành thứ'),('dai','Đài','','Cành 2 · Ngành thứ')]:add(id,'Lại Thế '+name,14,'huong',spouse,branch,note='Theo phả đồ trang 20. Cách đánh số cành ngành thứ có khác biệt giữa phần chung và các đề mục.')
add('truyen','Lại Thị Truyền',14,'huong','Vũ Công Lập','Ngành thứ')
add('xa','Lại Thị Xạ',14,'huong','Lương Văn Khoái','Ngành thứ')
for id,name in [('te','Tề'),('pho','Phó'),('chuc','Chúc'),('phoi','Phối'),('ngau','Ngẫu')]:add(id,'Lại Thế '+name,15,'tuyet',branch='Cành 1 · Ngành trưởng',page=21)
(root/'data_json/people-curated.json').write_text(json.dumps(people,ensure_ascii=False,indent=2))
(root/'data_json/people.json').write_text(json.dumps(people,ensure_ascii=False,indent=2))
(root/'data_json/contributions.json').write_text('[]\n') if not (root/'data_json/contributions.json').exists() else None
print(len(pages),'pages;',len(records),'source records;',len(people),'curated profiles')
