import {makeScene2D,Node,Txt,Rect,Circle,Line} from '@motion-canvas/2d';
import {createRef,tween} from '@motion-canvas/core';
import {Body,Nameplate,Gleam,Contact} from './depth-parts';
import type {Name} from './depth-parts';
import {theme as t} from './theme';
const ink='#645A4E',green='#688A78',paper='#F4EDDF';
const names:Name[]=['迈巴赫','劳斯莱斯','奔驰','迈巴赫','劳斯莱斯'];
const actorXs=[-570,-190,190,570,570];
const xs=[-570,-190,190,570];
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const smooth=(x:number)=>{x=clamp(x);return x*x*x*(10+x*(-15+6*x));};
const ramp=(s:number,a:number,b:number)=>smooth((s-a)/(b-a));
const decay=(s:number,a:number,amp:number,rate=7,freq=16)=>s<a?0:amp*Math.exp(-(s-a)*rate)*Math.sin((s-a)*freq);
const lerp=(a:number,b:number,u:number)=>a+(b-a)*u;
import {fullCues as captions} from './full-cues';
function Mini({root,label,model=['奔驰','迈巴赫'],labelRef}:{root:any,label:string,model?:Name[],labelRef?:any}){return <Node ref={root}>
 <Line points={model.length===1?[[-155,78],[150,78],[175,128],[-130,128]]:[[-307,78],[302,78],[327,128],[-282,128]]} closed fill={'#E3D4B8'} stroke={ink} lineWidth={3}/>
 <Line points={model.length===1?[[-130,128],[175,128],[175,140],[-130,140]]:[[-282,128],[327,128],[327,140],[-282,140]]} closed fill={'#BC9E7E'} stroke={ink} lineWidth={3}/>
 <Rect y={12} width={model.length===1?310:610} height={210} radius={20} stroke={'#B38866'} lineWidth={3} lineDash={[12,10]}/>
 {model.map((name,i)=><Node x={model.length===1?0:i===0?-155:155}>
  <Node y={15} scale={.66}><Contact x={0} y={49}/><Body name={name}/><Gleam x={0} y={0}/></Node>
  <Rect y={90} width={196} height={48} radius={5} fill={'#FFFAEB'} stroke={'#B6A58B'} lineWidth={2}/><Txt y={90} text={name} fontFamily={t.font} fontSize={35} fill={ink}/>
 </Node>)}
 <Rect y={-134} width={510} height={60} radius={8} fill={'#FFFAEB'} stroke={'#B38866'} lineWidth={2}/><Txt ref={labelRef} y={-134} text={label} fontFamily={t.font} fontSize={34} fill={ink}/>
 </Node>;}
export default makeScene2D(function* (view){
 view.fill(paper);
 const world=createRef<Node>(),back=createRef<Node>(),rear=createRef<Rect>(),roof=createRef<Line>(),roofFace=createRef<Rect>(),endWall=createRef<Line>(),rim=createRef<Line>(),groundFace=createRef<Line>();
 const car=names.map(()=>createRef<Node>()),body=names.map(()=>createRef<Node>()),shadows=names.map(()=>createRef<Node>()),bay=xs.map(()=>createRef<Rect>()),lines=xs.map(()=>createRef<Line>()),doors=xs.map(()=>createRef<Rect>()),badges=xs.map(()=>createRef<Node>()),lights=xs.map(()=>createRef<Circle>()),reflect=xs.map(()=>createRef<Line>());
 const bayContent=xs.map(()=>createRef<Node>());
 const pillars=[0,1,2,3,4].map(()=>createRef<Node>());
 const singleLabel=createRef<Txt>();
 const baseSource=createRef<Node>(),singleSource=createRef<Node>(),repeatMarks=createRef<Node>(),insertHint=createRef<Node>(),recap=createRef<Node>();
 const source=createRef<Node>(),module=createRef<Node>(),moduleShadow=createRef<Node>(),count=createRef<Txt>(),method=createRef<Txt>(),description=createRef<Txt>(),caption=createRef<Txt>(),countPanel=createRef<Node>(),comparison=createRef<Node>();
 view.add(<>
 <Node ref={back} opacity={.6}>
  <Rect y={-230} width={1920} height={460} fill={'#E9E1D1'}/>
  {[-790,-420,-50,320,690].map((x,i)=><Node x={x} y={-245}><Rect width={240} height={210} fill={i%2?'#DED5C4':'#E3DCCB'} stroke={'#C9C1AE'} lineWidth={2}/><Rect y={-15} width={172} height={135} fill={'#DDD8BF'} stroke={'#C1B8A3'} lineWidth={3}/><Line points={[[-86,-15],[86,-15]]} stroke={'#C1B8A3'} lineWidth={2}/><Line points={[[0,-82],[0,52]]} stroke={'#C1B8A3'} lineWidth={2}/></Node>)}
  <Line points={[[-960,45],[960,45]]} stroke={'#D0C8B6'} lineWidth={3}/>
  {[-1000,-600,-200,200,600,1000].map(x=><Line points={[[x,65],[x*1.5,400]]} stroke={'#D8CEB8'} lineWidth={2}/>)}
  {[165,270,395].map(y=><Line points={[[-960,y],[960,y]]} stroke={'#D8CEB8'} lineWidth={2}/>)}
 </Node>
 <Line points={[[-960,-398],[-620,-398],[560,398],[-350,398]]} closed fill={'#FFF6D8'} opacity={.15}/>
 <Node x={855} y={215} opacity={.52}>
  <Rect y={75} width={110} height={95} radius={8} fill={'#BA9C7D'} stroke={ink} lineWidth={2}/>
  <Line points={[[0,36],[-14,-60],[-65,-112]]} stroke={'#748975'} lineWidth={5}/>
  <Line points={[[0,36],[20,-30],[59,-94]]} stroke={'#748975'} lineWidth={5}/>
  {[[-53,-87],[-22,-41],[34,-68],[12,-18]].map(([x,y],i)=><Circle x={x} y={y} width={68} height={35} rotation={i%2?30:-30} fill={'#8C9C7E'}/>)}
 </Node>
 <Node ref={world} y={85}>
  <Line ref={groundFace} points={null} closed fill={'#D3D9C0'} stroke={green} lineWidth={3}/>
  <Rect ref={rear} y={-30} height={280} radius={6} fill={'#B4A38D'} stroke={ink} lineWidth={3}/>
  {xs.map((x,i)=><Rect ref={bay[i]} x={x} width={380} height={600} clip><Node ref={bayContent[i]}>
   <Rect y={-20} width={338} height={225} fill={'#777162'} stroke={'#655F52'} lineWidth={2}/>
   <Line points={[[-165,-115],[-165,102],[166,102]]} stroke={'#D5C3A0'} lineWidth={3}/>
   <Node y={-80}><Rect ref={doors[i]} width={320} height={178} offset={[0,-1]} fill={'#A29C87'} stroke={ink} lineWidth={2}/></Node>
   <Line ref={lines[i]} points={[[-172,115],[-145,232],[166,232],[146,115]]} stroke={'#F8F1D9'} lineWidth={4} end={0}/>
   <Line ref={reflect[i]} points={[[-115,154],[93,172]]} stroke={'#FCF3D8'} lineWidth={4} opacity={.17}/>
   <Circle ref={lights[i]} x={142} y={-104} size={14} fill={'#F6D781'} opacity={.35}/>
  </Node></Rect>)}
  {actorXs.map((x,i)=><Node ref={shadows[i]} x={x} y={122} scale={.80}><Contact x={0} y={0}/></Node>)}
  <Node ref={moduleShadow} x={190} y={159}><Circle width={306} height={23} fill={'#625A4E'} opacity={.16}/></Node>
  {actorXs.map((x,i)=><Node ref={car[i]} x={x} y={72} scale={.8}>
   <Node ref={body[i]}><Body name={names[i]}/><Gleam x={0} y={0}/></Node><Nameplate name={names[i]} x={0} y={117}/>
  </Node>)}
  <Mini root={module} label={'小列表 · 作为一项'}/>
  <Line ref={roof} points={null} closed fill={'#E9D8AA'} stroke={ink} lineWidth={3}/>
  <Rect ref={roofFace} y={-130} height={35} fill={'#CEB58C'} stroke={ink} lineWidth={3}/>
  <Line ref={endWall} points={null} closed fill={'#A78B6E'} stroke={ink} lineWidth={3}/>
  {[-760,-380,0,380,760].map((x,i)=><Node x={x} opacity={i<3?1:0} ref={pillars[i]}><Rect y={-5} width={16} height={234} fill={'#D7C39D'} stroke={ink} lineWidth={2}/></Node>)}
  <Line ref={rim} points={null} stroke={'#FAF1D1'} lineWidth={6}/>
  {xs.map((x,i)=><Node ref={badges[i]} x={x} y={260}>
   <Line points={[[0,-20],[0,-8]]} stroke={ink} lineWidth={2}/><Rect width={64} height={48} radius={8} fill={'#FEF9E9'} stroke={green} lineWidth={2}/><Txt text={String(i)} fontFamily={t.font} fontSize={30} fill={ink}/>
  </Node>)}
  <Node ref={countPanel} x={-570} y={-197}><Rect width={305} height={62} radius={8} fill={'#FFF9E8'} stroke={green} lineWidth={2}/><Txt ref={count} text={'vehicle · 2 项'} fontFamily={t.font} fontSize={28} fill={green}/></Node>
 </Node>
 <Mini root={source} label={'输入小列表 · 2 项'}/>
 <Mini root={baseSource} label={'原列表 · 2 项'} model={['迈巴赫','劳斯莱斯']}/>
 <Mini root={singleSource} label={'奔驰'} labelRef={singleLabel} model={['奔驰']}/>
 <Node ref={repeatMarks} y={0} opacity={0}>
  {[-380,380].map((x,i)=><Node x={x}><Line points={[[-340,282],[-340,291],[340,291],[340,282]]} stroke={i?'#B38866':green} lineWidth={3}/><Rect y={316} width={130} height={36} radius={6} fill={'#FFF9E8'}/><Txt y={316} text={i?'第 2 组':'第 1 组'} fontFamily={t.font} fontSize={23} fill={i?'#9A7355':green}/></Node>)}
 </Node>
 <Node ref={insertHint} x={-230} y={-251} opacity={0}><Rect width={470} height={74} radius={10} fill={'#FFFAEB'} stroke={green} lineWidth={2}/><Txt text={'索引 1：插到它前面'} fontFamily={t.font} fontSize={29} fill={green}/></Node>
 <Node ref={recap} opacity={0} y={-265}>
  {['相加','相乘','append','extend','insert'].map((name,i)=><Node x={-640+i*320}>
   <Rect width={288} height={126} radius={12} fill={'#FCF6E7'} stroke={i<2?green:'#B38866'} lineWidth={2}/><Txt y={-23} text={name} fontFamily={t.font} fontSize={32} fill={i<2?green:'#A96553'}/><Txt y={26} text={['连接 → 新列表','重复 → 新列表','整体 → 原列表','逐项 → 原列表','指定位置 → 原列表'][i]} fontFamily={t.font} fontSize={22} fill={ink}/>
  </Node>)}
 </Node>
 <Node ref={comparison} x={-500} y={-247} opacity={0}>
  <Rect width={650} height={195} radius={15} fill={'#F8F2E3'} stroke={'#B4A38D'} lineWidth={2}/>
  <Txt x={-205} y={-61} text={'append：3 项'} fontFamily={t.font} fontSize={28} fill={'#A96553'}/>
  <Node x={-215} y={25} scale={.38}><Body name={'迈巴赫'}/><Nameplate name={'迈巴赫'} x={0} y={110}/></Node>
  <Node x={-70} y={25} scale={.38}><Body name={'劳斯莱斯'}/><Nameplate name={'劳斯莱斯'} x={0} y={110}/></Node>
  <Rect x={155} y={26} width={230} height={110} radius={7} fill={'#DBCCAD'} stroke={ink} lineWidth={2}/>
  <Node x={99} y={22} scale={.29}><Body name={'奔驰'}/><Nameplate name={'奔驰'} x={0} y={110}/></Node>
  <Node x={208} y={22} scale={.29}><Body name={'迈巴赫'}/><Nameplate name={'迈巴赫'} x={0} y={110}/></Node>
 </Node>
 <Rect y={-471} width={1920} height={138} fill={paper}/>
 <Txt ref={method} x={-750} y={-456} text={'列表车库'} fontFamily={t.font} fontSize={42} fontWeight={700} fill={'#A96553'}/>
 <Txt ref={description} x={370} y={-455} text={'车位有顺序，编号从 0 开始'} width={970} textAlign={'right'} fontFamily={t.font} fontSize={30} fill={green}/>
 <Line points={[[-850,-404],[850,-404]]} stroke={'#D0C5B1'} lineWidth={2}/>
 <Rect y={475} height={130} width={1920} fill={paper}/><Txt ref={caption} y={475} width={1780} textAlign={'center'} text={''} fontFamily={t.font} fontSize={34} fill={ink}/>
 </>);
 function setWidth(w:number){const left=-760,right=left+w;rear().width(w);rear().x(left+w/2);roofFace().width(w);roofFace().x(left+w/2);roof().points([[left-12,-171],[right,-171],[right+45,-148],[left+33,-148]]);endWall().points([[right,-148],[right+45,-125],[right+45,173],[right,150]]);groundFace().points([[left-14,99],[right,99],[right+54,232],[left+38,232]]);rim().points([[left+38,233],[right+54,233]]);}
 function transfer(actor:number,slot:number,s:number,start:number,end:number,origin:[number,number],scale=.8){
  const u=ramp(s,start,end),root=car[actor]();root.position([lerp(origin[0],xs[slot],u)-8*ramp(s,start-.35,start)*(1-u)+decay(s,end,10),lerp(origin[1],72,u)-35*Math.sin(Math.PI*u)]);root.scale(lerp(.66*.43,scale,u));root.opacity(ramp(s,start-.30,start-.05));
  body[actor]().y(decay(s,end,5,8,18));body[actor]().rotation(-1.3*Math.sin(Math.PI*u)+decay(s,end,1,7,15));shadows[actor]().position([root.x(),122]);shadows[actor]().opacity(root.opacity()*(.18+.82*u));shadows[actor]().scale(.8+.15*Math.sin(Math.PI*u)-decay(s,end,.025));
 }
 function parked(actor:number,slot:number){car[actor]().position([xs[slot],72]);car[actor]().scale(.8);car[actor]().opacity(1);shadows[actor]().position([xs[slot],122]);shadows[actor]().opacity(1);}
 yield* tween(150,v=>{const s=v*150;
  const isPlus=s>=12&&s<38,isTimes=s>=38&&s<60,isAppend=s>=60&&s<85,isExtend=s>=85&&s<112,isInsert=s>=112&&s<140,isEnd=s>=140;
  const cuts=[0,12,38,60,85,112,140];let chapter=cuts.filter(x=>x<=s).pop()||0;
  const cam=(isAppend?.035*ramp(s,72.5,76)-.035*ramp(s,81.5,84):isExtend?.02*ramp(s,93.5,99.5)-.02*ramp(s,101,104):isInsert?.04*ramp(s,120,125)-.04*ramp(s,131,136):0);
  world().scale(1+cam);world().x(-cam*100);back().scale(1+cam*.22);back().x(-cam*22);
  world().opacity(ramp(s,chapter+.05,chapter+.45));
  for(let i=0;i<names.length;i++){car[i]().opacity(0);car[i]().rotation(0);body[i]().position([0,0]);body[i]().rotation(0);shadows[i]().opacity(0);shadows[i]().scale(.8);}
  for(let i=0;i<4;i++){badges[i]().opacity(0);badges[i]().rotation(0);reflect[i]().opacity(.13);}
  source().position([540,-230]);source().scale(.43);source().opacity(0);source().rotation(0);baseSource().position([-430,-230]);baseSource().scale(.43);baseSource().opacity(0);singleSource().position([540,-230]);singleSource().scale(.43);singleSource().opacity(0);
  module().opacity(0);moduleShadow().opacity(0);comparison().opacity(0);repeatMarks().opacity(0);insertHint().opacity(0);recap().opacity(0);
  let reveal=[1,1,0,0],openTimes=[-1,-1,Infinity,Infinity],label='vehicle',num=2;
  const upperSource=[540,-230+15*.43-85] as [number,number];
  if(s<12){
   reveal=[ramp(s,.1,1.1),ramp(s,.35,1.35),0,0];openTimes=[1.0,1.3,Infinity,Infinity];
   parked(0,0);parked(1,1);
   for(let i=0;i<2;i++){car[i]().x(xs[i]-18*(1-ramp(s,.55+i*.2,1.8+i*.2)));body[i]().y(decay(s,1.8+i*.2,4));body[i]().rotation(decay(s,1.8+i*.2,.7));shadows[i]().x(car[i]().x());badges[i]().opacity(ramp(s,2.25+i*.2,2.7+i*.2));}
  }else if(isPlus){
   baseSource().opacity(ramp(s,12.2,12.7));singleSource().opacity(ramp(s,16,16.5));label='新列表';
   reveal=[ramp(s,18,19),ramp(s,22,23),ramp(s,26,27),0];openTimes=[19,23,27,Infinity];world().opacity(ramp(s,18,18.4));
   transfer(0,0,s,19.3,20.8,[-430-155*.43,upperSource[1]]);transfer(1,1,s,23.3,24.8,[-430+155*.43,upperSource[1]]);transfer(2,2,s,27.3,28.8,upperSource);
   for(let i=0;i<3;i++)badges[i]().opacity(ramp(s,[21.15,25.15,29.15][i],[21.5,25.5,29.5][i]));
   num=s<21?0:s<25?1:s<29?2:3;
  }else if(isTimes){
   label='新列表';baseSource().position([0,-230]);baseSource().opacity(ramp(s,38.2,38.7));
   reveal=[ramp(s,41.4,42.4),ramp(s,43,44),ramp(s,45.8,46.8),ramp(s,47.3,48.3)];openTimes=[42.4,44,46.8,48.3];world().opacity(ramp(s,41.4,41.8));
   const starts=[42.7,44.3,47.1,48.6],ends=[44.1,45.7,48.5,50];const actors=[0,1,3,4];
   for(let i=0;i<4;i++){transfer(actors[i],i,s,starts[i],ends[i],[i%2?-0+155*.43:-155*.43,upperSource[1]]);badges[i]().opacity(ramp(s,ends[i]+.3,ends[i]+.6));}
   repeatMarks().opacity(ramp(s,50.4,51));num=ends.filter(e=>s>=e+.25).length;
  }else if(isAppend){
   parked(0,0);parked(1,1);badges[0]().opacity(1);badges[1]().opacity(1);
   if(s<69){
    singleSource().opacity(ramp(s,60.1,60.6));reveal[2]=ramp(s,62,63);openTimes[2]=63;transfer(2,2,s,63.3,64.8,upperSource);badges[2]().opacity(ramp(s,65.1,65.5));num=s>=65.05?3:2;
   }else{
    const reset=ramp(s,69,69.5),mu=ramp(s,73.8,77.2);source().opacity(ramp(s,70.2,70.7));reveal[2]=ramp(s,72.7,73.7);openTimes[2]=73.7;
    module().opacity(ramp(s,73.2,73.55));module().position([lerp(540,190,mu)-8*ramp(s,73.4,73.8)*(1-mu)+decay(s,77.2,10),lerp(-315,95,mu)-30*Math.sin(Math.PI*mu)]);module().scale(lerp(.43,.48,mu));module().rotation(-.65*Math.sin(Math.PI*mu)+decay(s,77.2,.9));moduleShadow().opacity(ramp(s,75,77.2));moduleShadow().position([module().x(),159]);moduleShadow().scale(1.2-.2*mu);badges[2]().opacity(ramp(s,77.6,78));badges[2]().rotation(decay(s,77.35,1.5));num=s>=77.6?3:2;
    world().opacity(s<69.6?1-reset:ramp(s,69.6,70.1));
   }
  }else if(isExtend){
   parked(0,0);parked(1,1);badges[0]().opacity(1);badges[1]().opacity(1);source().opacity(1);source().rotation(decay(s,93.5,-.6)+decay(s,97.8,-.6));
   reveal[2]=ramp(s,92.5,93.5);reveal[3]=ramp(s,96.5,97.5);openTimes[2]=93.5;openTimes[3]=97.5;
   transfer(2,2,s,93.5,95.3,[540-155*.43,upperSource[1]]);transfer(3,3,s,97.8,99.6,[540+155*.43,upperSource[1]]);
   badges[2]().opacity(ramp(s,95.6,96));badges[3]().opacity(ramp(s,99.9,100.3));for(let i=2;i<4;i++)badges[i]().rotation(decay(s,i===2?95.45:99.75,1.5));num=s<95.6?2:s<99.9?3:4;
   comparison().opacity(ramp(s,105.5,106.2));
  }else{
   // insert result remains as the final shared garage through the recap.
   parked(0,0);parked(1,1);badges[0]().opacity(1);badges[1]().opacity(1);
   const sh=ramp(s,122.2,124.0);car[1]().position([lerp(xs[1],xs[2],sh)+decay(s,124,10),72]);body[1]().y(decay(s,124,4));body[1]().rotation(-.8*Math.sin(Math.PI*sh)+decay(s,124,.7));shadows[1]().x(car[1]().x());
   reveal[2]=ramp(s,121.2,122.2);openTimes[2]=122.2;singleSource().opacity(isEnd?0:ramp(s,116.8,117.3));insertHint().opacity(isEnd?0:ramp(s,118.5,119));
   transfer(2,1,s,125.6,127.6,upperSource);badges[2]().opacity(ramp(s,124.35,124.75));badges[2]().rotation(decay(s,124.1,1.5));num=s>=127.9?3:2;
   if(s>=118.5&&s<122.2)badges[1]().scale(1+.05*Math.sin((s-118.5)*4));else badges[1]().scale(1);
   if(isEnd)recap().opacity(ramp(s,140.15,140.8));
  }
  const width=380*reveal.reduce((a,b)=>a+b,0);setWidth(width);
  for(let i=0;i<4;i++){
   const r=reveal[i];bay[i]().opacity(r);bay[i]().width(380*r);bay[i]().x(xs[i]-190*(1-r));bayContent[i]().x(190*(1-r));lines[i]().end(r);
   const op=!Number.isFinite(openTimes[i])?0:openTimes[i]<0?1:ramp(s,openTimes[i]-.6,openTimes[i]);doors[i]().scale.y(1-.90*op+decay(s,openTimes[i],.025,9,18));lights[i]().opacity(.3+.45*op+.12*Math.sin(s*.8+i)*op);
   pillars[i]().opacity(i===0?reveal[0]:reveal[i-1]);pillars[i]().x(-760+380*reveal.slice(0,i).reduce((a,b)=>a+b,0));
  }
  pillars[4]().opacity(reveal[3]);pillars[4]().x(-760+width);
  count().text(label+' · '+num+' 项');countPanel().rotation(decay(s,29.3,.7)+decay(s,50.4,.7)+decay(s,77.6,.7)+decay(s,99.9,.7)+decay(s,127.9,.7));
  singleLabel().text(isPlus?'原列表 · 1 项':isInsert?'插入：奔驰':'追加：奔驰');
  method().text(s<12?'列表车库':isPlus?'列表相加':isTimes?'列表相乘':isAppend?'append':isExtend?'extend':isInsert?'insert':'五个操作');
  description().text(s<12?'每辆车代表一个汽车名称 · 索引从 0 开始':isPlus?'先左后右连接 · 两个原列表保持不变':isTimes?'整组按顺序重复两遍 · 原列表保持不变':isAppend?(s<69?'在末尾追加一项 · 修改原列表':'小列表作为一个整体 · 只占一个外层车位'):isExtend?'逐项加入 · 来源小列表保持完整':isInsert?'插到指定索引之前 · 后面的位置编号更新':s<145?'相加连接 · 相乘重复 → 新列表':'append / extend / insert → 修改原列表');
  caption().text(captions.find(c=>s>=c.start&&s<c.end)?.text||'');
 });
});
