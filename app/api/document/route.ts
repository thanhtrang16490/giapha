import { readFile } from 'node:fs/promises';
import path from 'node:path';
export async function GET(){try {const file=await readFile(path.join(process.cwd(),'tai_lieu/GIA PHA HO LAI 200325.pdf')); return new Response(file,{headers:{'Content-Type':'application/pdf','Content-Disposition':'inline; filename="gia-pha-ho-lai.pdf"','Cache-Control':'private, max-age=3600'}})}catch{return Response.json({error:'Không tìm thấy tài liệu gốc.'},{status:404})}}
