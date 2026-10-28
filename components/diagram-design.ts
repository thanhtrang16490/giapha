import {sanitizeDecorations} from '@/lib/diagram-decorations.mjs';
export type Decoration={id:string;type:'text'|'image'|'plaque';name:string;text:string;src:string;x:number;y:number;width:number;height:number;fontSize:number;align:'left'|'center'|'right';font:'sans'|'serif';color:string;fill:string;border:string;opacity:number;hidden:boolean;locked:boolean};
export type GenerationDesign={avatar?:boolean;vertical?:boolean;spouse?:boolean;fontSize?:number;gap?:number;dates?:boolean;source?:boolean};
export type DiagramDesign={theme:'modern'|'heritage';color:string;lineWidth:number;gap:number;nodeGap:number;avatar:boolean;vertical:boolean;spouse:boolean;fontSize:number;frame:boolean;heading:boolean;paperWidth:number;paperHeight:number;generations:Record<string,GenerationDesign>;dates:boolean;source:boolean;lineStyle:'orthogonal'|'curve'|'straight';title:string;subtitle:string;coupletLeft:string;coupletRight:string;ornament:boolean;decorations:Decoration[];background:'theme'|'white'|'paper'|'pattern'};
export const defaultDesign:DiagramDesign={theme:'modern',color:'#6d8d5c',lineWidth:1.5,gap:100,nodeGap:32,avatar:true,vertical:false,spouse:true,fontSize:13,frame:true,heading:true,paperWidth:1189,paperHeight:841,generations:{},dates:false,source:true,lineStyle:'orthogonal',title:'GIA PHẢ LẠI TỘC',subtitle:'CHI DIÊM ĐIỀN',coupletLeft:'',coupletRight:'',ornament:false,decorations:[],background:'theme'};
export function generationDesign(design:DiagramDesign,generation:number):GenerationDesign{return {...design,...design.generations[generation]};}
export function sanitizeDesign(input:unknown):DiagramDesign{
 const result:DiagramDesign={...defaultDesign,generations:{}};
 if(!input||typeof input!=='object')return result;
 const data=input as Record<string,unknown>;result.decorations=sanitizeDecorations(data.decorations) as Decoration[];if(['theme','white','paper','pattern'].includes(String(data.background)))result.background=data.background as DiagramDesign['background'];
 const bounded=(key:keyof DiagramDesign,min:number,max:number)=>{if(typeof data[key]==='number'&&Number.isFinite(data[key]))(result as unknown as Record<string,unknown>)[key]=Math.min(max,Math.max(min,data[key] as number))};
 bounded('lineWidth',.5,5);bounded('gap',40,320);bounded('nodeGap',16,150);bounded('fontSize',10,20);bounded('paperWidth',200,5000);bounded('paperHeight',200,5000);
 for(const key of ['avatar','vertical','spouse','frame','heading','dates','source','ornament'] as const)if(typeof data[key]==='boolean')result[key]=data[key] as boolean;
 for(const key of ['title','subtitle','coupletLeft','coupletRight'] as const)if(typeof data[key]==='string')result[key]=(data[key] as string).slice(0,key.startsWith('couplet')?100:120);
 if(['orthogonal','curve','straight'].includes(String(data.lineStyle)))result.lineStyle=data.lineStyle as DiagramDesign['lineStyle'];
 if(data.theme==='heritage')result.theme='heritage';if(typeof data.color==='string'&&/^#[0-9a-f]{6}$/i.test(data.color))result.color=data.color;
 if(data.generations&&typeof data.generations==='object')for(const [generation,raw] of Object.entries(data.generations)){
  if(!/^\d{1,2}$/.test(generation)||!raw||typeof raw!=='object')continue;const g=raw as Record<string,unknown>,override:GenerationDesign={};
  for(const key of ['avatar','vertical','spouse','dates','source'] as const)if(typeof g[key]==='boolean')override[key]=g[key] as boolean;
  if(typeof g.fontSize==='number'&&Number.isFinite(g.fontSize))override.fontSize=Math.min(20,Math.max(10,g.fontSize));if(typeof g.gap==='number'&&Number.isFinite(g.gap))override.gap=Math.min(320,Math.max(40,g.gap));result.generations[generation]=override;
 }
 return result;
}

export function memberSize(style:GenerationDesign){return {width:style.vertical?170:280,height:style.vertical?(style.dates?236:210):(style.dates?154:132)}}
