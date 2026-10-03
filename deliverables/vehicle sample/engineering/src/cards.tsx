import {Node,Rect,SVG,Txt,Circle} from '@motion-canvas/2d';
import {theme as t} from './theme';
import maybach from '../../assets/maybach.svg?raw';
import rolls from '../../assets/rolls.svg?raw';
import mercedes from '../../assets/mercedes.svg?raw';
export type CarName='迈巴赫'|'劳斯莱斯'|'奔驰';
const cars:Record<CarName,string>={'迈巴赫':maybach,'劳斯莱斯':rolls,'奔驰':mercedes};
// Slightly irregular deterministic paths: editable ink outlines, no random jitter.
export function InkPanel({x=0,y=0,width,height,fill=t.paper,stroke=t.ink,depth=9,lineWidth=2}:{x?:number,y?:number,width:number,height:number,fill?:string,stroke?:string,depth?:number,lineWidth?:number}){
 const path=`M 27 4 Q 502 0 968 5 Q 995 8 995 37 L 992 369 Q 990 395 964 395 L 36 398 Q 8 394 6 367 L 4 34 Q 3 8 27 4 Z`;
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 400" preserveAspectRatio="none"><path d="${path}" fill="${fill}" stroke="${stroke}" stroke-width="${lineWidth*1000/width}" stroke-linejoin="round"/><path d="M13 42 Q9 181 15 302 M46 10 Q447 6 750 12" fill="none" stroke="${stroke}" stroke-width="1.3" opacity=".13"/></svg>`;
 return <Node x={x} y={y}><Rect x={depth*0.9} y={depth*1.4} width={width-4} height={height-4} radius={16} fill={'#B5A38E28'} shadowColor={'#63564C1A'} shadowBlur={16} shadowOffset={[7,12]}/><SVG svg={svg} width={width} height={height}/></Node>;
}
export function Tray({x=0,y=0,width,height,nested=false}:{x?:number,y?:number,width:number,height:number,nested?:boolean}){
 const edge=nested?t.accent:t.blue;
 return <Node x={x} y={y}><InkPanel width={width} height={height} fill={nested?'#FBE9DE':'#EFF3EC'} stroke={edge} depth={12} lineWidth={2.8}/><Rect y={height/2-12} width={width-24} height={15} radius={7} fill={nested?'#E8BAA54D':'#8FAEAB35'}/></Node>;
}
export function CarCard({name,x=0,y=0,width=190,mini=false}:{name:CarName,x?:number,y?:number,width?:number,mini?:boolean}){
 const height=mini?124:180;
 return <Node x={x} y={y} rotation={name==='劳斯莱斯'?0.7:name==='奔驰'?-0.6:-1.1}>
 <InkPanel width={width} height={height} fill={t.paper} stroke={'#B3AEA5'} depth={mini?5:8} lineWidth={1.7}/>
 <SVG svg={cars[name]} width={width-4} height={(width-4)*220/360} y={mini?-20:-27}/>
 <Txt text={name} y={mini?41:58} fontFamily={t.font} fontSize={mini?25:30} fontWeight={600} fill={t.ink}/>
 </Node>;
}
export function Index({value,x,y}:{value:number,x:number,y:number}){return <Node x={x} y={y}><Circle size={36} fill={t.paper} stroke={'#8EAAA5'} lineWidth={1.5}/><Txt text={String(value)} fontFamily={t.font} fontSize={25} fill={t.ink}/></Node>;}
