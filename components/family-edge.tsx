'use client';
import {BaseEdge,getBezierPath,type EdgeProps,type Edge} from '@xyflow/react';
export type LineageEdge=Edge<{lineStyle?:'orthogonal'|'curve'|'straight';busOffset?:number},'lineage'>;
export default function FamilyEdge(props:EdgeProps<LineageEdge>){const {sourceX:sx,sourceY:sy,targetX:tx,targetY:ty,data}=props;const bus=sy+Math.max(18,Math.min(data?.busOffset||50,Math.abs(ty-sy)*.7));const path=data?.lineStyle==='curve'?getBezierPath(props)[0]:data?.lineStyle==='straight'?`M ${sx} ${sy} L ${tx} ${ty}`:`M ${sx} ${sy} V ${bus} H ${tx} V ${ty}`;return <BaseEdge id={props.id} path={path} style={props.style} label={props.label} labelStyle={props.labelStyle} labelBgStyle={props.labelBgStyle} labelX={tx} labelY={ty-16} interactionWidth={12}/>}
