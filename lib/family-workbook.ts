import ExcelJS from 'exceljs';
import {FamilyError} from './family-domain.mjs';
export async function readPeopleWorkbook(bytes:Uint8Array){
 const workbook=new ExcelJS.Workbook();try{await workbook.xlsx.load(Buffer.from(bytes) as never)}catch{throw new FamilyError('Không đọc được tệp XLSX. Hãy dùng tệp Excel xuất từ ứng dụng.');}
 const sheet=workbook.getWorksheet('Hồ sơ');if(!sheet)throw new FamilyError('Tệp cần trang tính “Hồ sơ”.');if(sheet.rowCount>3001||sheet.columnCount>60)throw new FamilyError('Tệp vượt quá 3.000 hồ sơ hoặc 60 cột.');
 const headers:string[]=[];sheet.getRow(1).eachCell((cell,column)=>{if(cell.type===ExcelJS.ValueType.Formula)throw new FamilyError('Tiêu đề cột không được là công thức.');headers[column-1]=cell.text.trim()});
 if(!['Mã','Họ tên','Đời','Giới tính'].every(h=>headers.includes(h)))throw new FamilyError('Thiếu cột Mã, Họ tên, Đời hoặc Giới tính.');if(new Set(headers.filter(Boolean)).size!==headers.filter(Boolean).length)throw new FamilyError('Tiêu đề cột bị trùng.');
 const rows:Record<string,string|number>[]=[];sheet.eachRow((row,index)=>{if(index===1)return;const data:Record<string,string|number>={_row:index};let filled=false;headers.forEach((header,i)=>{if(!header)return;const cell=row.getCell(i+1);if(cell.type===ExcelJS.ValueType.Formula||cell.type===ExcelJS.ValueType.Hyperlink||cell.type===ExcelJS.ValueType.Error)throw new FamilyError(`Dòng ${index}: không nhận công thức, siêu liên kết hoặc ô lỗi.`);const text=cell.text.trim();if(text.length>30000)throw new FamilyError(`Dòng ${index}: ô dữ liệu quá dài.`);if(text)filled=true;data[header]=text});if(filled)rows.push(data)});return rows;
}
