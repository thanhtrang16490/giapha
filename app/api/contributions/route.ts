import {readFile,writeFile,rename} from 'node:fs/promises';
import path from 'node:path';
import {randomUUID} from 'node:crypto';
export const runtime='nodejs';
let queue=Promise.resolve();
export async function POST(request:Request){
 const origin=request.headers.get('origin');if(origin&&new URL(origin).host!==request.headers.get('host'))return Response.json({error:'Yêu cầu không hợp lệ.'},{status:403});
 try{const body=await request.text();if(body.length>16000)return Response.json({error:'Nội dung quá dài.'},{status:413});const input=JSON.parse(body);
 if(typeof input.name!=='string'||!input.name.trim()||input.name.length>120||typeof input.content!=='string'||input.content.trim().length<10||input.content.length>5000)return Response.json({error:'Vui lòng nhập tên và nội dung từ 10 đến 5.000 ký tự.'},{status:400});
 const item={id:randomUUID(),name:input.name.trim(),content:input.content.trim(),createdAt:new Date().toISOString(),status:'pending'};
 const job=queue.catch(()=>{}).then(async()=>{const file=path.join(process.cwd(),'data_json/contributions.json');const items=JSON.parse(await readFile(file,'utf8'));items.push(item);const temp=file+'.tmp';await writeFile(temp,JSON.stringify(items,null,2));await rename(temp,file)});queue=job;await job;
 return Response.json({id:item.id},{status:201});
 }catch{return Response.json({error:'Chưa lưu được đóng góp. Vui lòng thử lại.'},{status:500})}}
