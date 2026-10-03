import {makeScene2D,Node,SVG,Txt,Rect,Circle,Line} from '@motion-canvas/2d';
import {waitFor,createRef} from '@motion-canvas/core';
import {theme as t} from './theme';
import {InkPanel} from './cards';
import maybach from '../../assets/maybach.svg?raw';
import rolls from '../../assets/rolls.svg?raw';
import mercedes from '../../assets/mercedes.svg?raw';
import wall from '../../assets/environment/wall.svg?raw';
import floor from '../../assets/environment/floor.svg?raw';
import shutter from '../../assets/environment/shutter.svg?raw';
import windowArt from '../../assets/environment/window.svg?raw';
import lamp from '../../assets/environment/lamp.svg?raw';
import beam from '../../assets/environment/light-beam.svg?raw';
import bench from '../../assets/environment/bench.svg?raw';
import nearArt from '../../assets/environment/near-frame.svg?raw';
import trackTop from '../../assets/track/top.svg?raw';
import trackSide from '../../assets/track/side.svg?raw';
import trackRim from '../../assets/track/front-rim.svg?raw';
import trackLight from '../../assets/track/highlight.svg?raw';
type Name='迈巴赫'|'劳斯莱斯'|'奔驰';
const carArt:Record<Name,string>={'迈巴赫':maybach,'劳斯莱斯':rolls,'奔驰':mercedes};
const noEmbeddedShadow=(svg:string)=>svg.replace(/<path d="M39 182[^>]*\/>/,'').replace(/<ellipse cx="184" cy="190"[^>]*\/>/,'');
const inputBackRaw=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 280"><path d="M24 23 L483 15 L491 218 L27 237 Z" fill="#F4DACA" stroke="#775E52" stroke-width="3"/><path d="M24 23 L51 45 L470 36 L483 15" fill="#FFF2DF" stroke="#775E52" stroke-width="2.5"/><path d="M484 16 L520 46 L527 245 L491 218 Z" fill="#AE7E67" stroke="#775E52" stroke-width="3"/></svg>`;
const inputBack=inputBackRaw.replace(/<path d="M484[^>]*\/>/,'');
const inputSide=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 280"><path d="M484 16 L520 46 L527 245 L491 218 Z" fill="#AE7E67" stroke="#775E52" stroke-width="3"/></svg>`;
const inputFront=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 280"><path d="M28 203 L490 185 L494 221 L43 259 L27 237 Z" fill="#C79475" stroke="#775E52" stroke-width="3"/><path d="M28 203 L490 185 L511 230 L52 274 Z" fill="#E6B597" stroke="#775E52" stroke-width="3"/><path d="M31 204 L487 187" stroke="#FFF2DB" stroke-width="5" fill="none"/></svg>`;
function Nameplate({name,x,y,scale=1}:{name:Name,x:number,y:number,scale?:number}){return <Node x={x} y={y} scale={scale}>
 <InkPanel width={188} height={50} fill={'#FFFDF0'} stroke={'#AA9D86'} depth={4}/><Txt text={name} fontFamily={t.font} fontWeight={600} fontSize={31} fill={t.ink}/>
 </Node>;}
function Body({name,x=0,y=0,scale=1}:{name:Name,x?:number,y?:number,scale?:number}){return <Node x={x} y={y} scale={scale}><SVG svg={noEmbeddedShadow(carArt[name])} y={-18} width={350} height={214}/></Node>;}
function Gleam({x,y,scale=1}:{x:number,y:number,scale?:number}){return <Node x={x} y={y} scale={scale}><SVG y={-18} width={350} height={214} svg={'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 220"><path d="M115 58 Q145 56 185 61" stroke="#FFF5D9" stroke-width="2.5" fill="none" opacity=".42"/></svg>'}/></Node>;}
function Contact({x,y,scale=1}:{x:number,y:number,scale?:number}){return <Node x={x+8} y={y} scale={scale}>
 <Circle width={316} height={26} fill={'#7B7160'} opacity={.12}/><Circle width={260} height={14} fill={'#6C6354'} opacity={.18}/>
 </Node>;}

export {Body,Nameplate,Gleam,Contact,inputBack,inputSide,inputFront,wall,floor,shutter,windowArt,lamp,beam,bench,nearArt,trackTop,trackSide,trackRim,trackLight};
export type {Name};
