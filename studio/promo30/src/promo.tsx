import {makeScene2D, Node, Txt, Rect, Circle, Line} from '@motion-canvas/2d';
import {createSignal, tween, linear} from '@motion-canvas/core';

// All visuals are Motion Canvas nodes. No editor simulation or Python footage.
const C={bg:'#F4F3EB',ink:'#172E32',muted:'#687C7C',green:'#C4EE94',orange:'#FF885B',line:'#D8DFD5',paper:'#FFFFFF'};
const font='Noto Sans CJK SC';
const clamp=(v:number)=>Math.min(1,Math.max(0,v));
const ease=(v:number)=>1-Math.pow(1-clamp(v),3);
const T=(p:any)=><Txt fontFamily={font} fill={C.ink} fontSize={36} fontWeight={600} {...p}/>;
export default makeScene2D(function*(view){
  const time=createSignal(0);
  const enter=(a:number,d=.65)=>ease((time()-a)/d);
  const vis=(a:number,b:number)=>enter(a,.3)*(1-ease((time()-(b-.25))/.25));
  view.fill(C.bg);
  view.add(<>
    <Circle size={850} x={610} y={-400} stroke={C.line} lineWidth={1}/>
    <Circle size={630} x={610} y={-400} stroke={C.line} lineWidth={1}/>
    <T text="PYTHON / 学得明白" fontSize={19} letterSpacing={2} x={-455} y={-303}/>
    <T text="大学 Python · 动画课" fontSize={17} fill={C.muted} x={456} y={-303}/>
    <Line points={[[-570,-270],[570,-270]]} stroke={C.line} lineWidth={1}/>
    <Rect x={-640} y={355} offsetX={-1} width={()=>1280*time()/30} height={10} fill={C.ink}/>
    <T x={505} y={312} fontSize={16} fill={C.muted} text={()=>`${String(Math.min(30,Math.floor(time()))).padStart(2,'0')} / 30`}/>
  </>);
  // 00–05: four pain points, accumulating in staggered motion.
  view.add(<Node opacity={()=>vis(0,5)} y={()=>(1-enter(0))*24}>
    <T text="校内 Python，" x={-275} y={-163} fontSize={59}/>
    <T text="卡在哪一步？" x={-240} y={-82} fontSize={67}/>
    {['难学','没意思','听不懂','不想实践'].map((s,i)=><Node
      x={-435+i*286} y={()=>105+(1-enter(.65+i*.62))*75}
      rotation={()=>[ -5,3,-3,5][i]*enter(.65+i*.62)} opacity={()=>enter(.65+i*.62)}>
      <Rect size={[250,118]} radius={20} fill={i===2?C.orange:C.paper} stroke={C.line} lineWidth={1}/>
      <T text={s} fontSize={36}/>
      <T text={`0${i+1}`} fontSize={16} y={-80} fill={C.muted}/>
    </Node>)}
    <T text="从听不懂，到愿意动手。" fontSize={24} y={234} fill={C.muted} opacity={()=>enter(3.5)}/>
    <T text="?" fontSize={200} x={423} y={-133} fill={C.orange} rotation={()=>-10+4*Math.sin(time()*2)}/>
  </Node>);
  // 05–06: one-second punch, matching the attached script.
  view.add(<Node opacity={()=>vis(5,6)}>
    <Circle size={()=>2400*enter(5,.35)} fill={C.green}/>
    <T text="一站式解决！" fontSize={91} scale={()=>.82+.18*enter(5,.4)}/>
    <T text="看懂原理  /  建立思路" fontSize={25} y={100}/>
  </Node>);
  // 06–10: goal and credit requirement. No outcome guarantee.
  view.add(<Node opacity={()=>vis(6,10)}>
    <T text="先有目标，再有方法。" fontSize={55} y={-171}/>
    <Node x={-345} y={()=>40+55*(1-enter(6.3))} opacity={()=>enter(6.3)}>
      <Circle size={190} fill={C.green}/><T text="学分" fontSize={54}/>
      <T text="完成课程要求" fontSize={23} y={138} fill={C.muted}/>
    </Node>
    <Line points={[[-195,40],[185,40]]} stroke={C.ink} lineWidth={4} endArrow end={()=>enter(6.9,1)} arrowSize={16}/>
    <T text="明确学习目标" fontSize={21} y={0} opacity={()=>enter(7.2)}/>
    <Node x={345} y={()=>40+55*(1-enter(7.6))} opacity={()=>enter(7.6)}>
      <Rect size={[245,190]} radius={30} fill={C.ink}/><T text="期末通过" fontSize={42} fill={C.bg}/>
      <T text="一步一步准备" fontSize={23} y={138} fill={C.muted}/>
    </Node>
  </Node>);
  // 10–19: concept demonstration, append token travels into a list.
  view.add(<Node opacity={()=>vis(10,19)}>
    <T text="01 / 动画，把抽象变直观" fontSize={22} fill={C.muted} y={-200}/>
    <T text="不只记住，更要看懂。" fontSize={58} y={-128}/>
    <Rect y={33} size={[890,170]} radius={30} stroke={C.line} lineWidth={2}/>
    <T text="列表" fontSize={23} x={-506} y={35} fill={C.muted}/>
    {[72,85].map((n,i)=><Node x={-290+i*205} y={()=>30+60*(1-enter(10.6+i*.22))} opacity={()=>enter(10.6+i*.22)}>
      <Rect size={[170,112]} radius={18} fill={C.paper}/><T text={String(n)} fontSize={51}/>
      <T text={String(i)} fontSize={18} y={96} fill={C.muted}/>
    </Node>)}
    <Node x={()=>400-280*enter(13.0,1.5)} y={()=>-20+50*enter(13,1.5)}
      opacity={()=>enter(11.7)} scale={()=>.85+.15*enter(11.7)}>
      <Rect size={[170,112]} radius={18} fill={C.orange}/><T text="90" fontSize={51}/>
    </Node>
    <T text="2" x={120} y={126} fontSize={18} fill={C.muted} opacity={()=>enter(14.5)}/>
    <Line points={[[350,-1],[215,-1]]} endArrow arrowSize={13} stroke={C.ink} lineWidth={3} opacity={()=>vis(12,13.1)}/>
    <T text={()=>time()<14.5?'append：把新元素加到末尾':'[72, 85]  →  [72, 85, 90]'} fontSize={29} y={210}/>
    <Rect x={338} y={30} size={[135,86]} radius={43} fill={C.green} opacity={()=>enter(15.4)}/>
    <T text="+1" x={338} y={30} fontSize={39} opacity={()=>enter(15.4)}/>
    <T text="概念 → 变化 → 结果" fontSize={19} y={264} fill={C.muted} opacity={()=>enter(16.1)}/>
  </Node>);
  // 19–25: assessment formats, without claiming universal coverage.
  view.add(<Node opacity={()=>vis(19,25)}>
    <T text="02 / 面向上海高校校内考试" fontSize={22} fill={C.muted} y={-204}/>
    <T text="让学习，贴近考情。" fontSize={58} y={-130}/>
    {['选择判断','结果填空','简单编程'].map((s,i)=><Node x={-352+i*352} y={()=>45+80*(1-enter(19.7+i*.48))} opacity={()=>enter(19.7+i*.48)}>
      <Rect size={[314,217]} radius={22} fill={i===1?C.green:C.paper}/>
      {i===0?<><Circle size={26} x={-71} y={-40} stroke={C.ink} lineWidth={3}/><Line points={[[-18,-40],[86,-40]]} stroke={C.ink} lineWidth={5}/></>:null}
      {i===1?<><T text="[    ?    ]" fontSize={43} y={-40}/></>:null}
      {i===2?<T text="{  }" fontSize={54} y={-40}/>:null}
      <T text={s} fontSize={32} y={49}/>
    </Node>)}
    <T text="期中 · 期末  /  以学校课件与题型为依据" fontSize={24} y={219} fill={C.muted} opacity={()=>enter(21.8)}/>
    <T text="具体范围按学校要求调整" fontSize={17} y={269} fill={C.muted} opacity={()=>enter(22.8)}/>
  </Node>);
  // 25–30: aspiration and closing hold.
  view.add(<Node opacity={()=>enter(25,.35)}>
    <T text="为期末，更进一步。" fontSize={64} x={-150} y={-132}/>
    <Rect x={-199} y={-27} size={[702,75]} radius={9} fill={C.green} scaleX={()=>enter(25.5)}/>
    <T text="向通过与高绩点目标迈进" fontSize={38} x={-199} y={-27} opacity={()=>enter(25.7)}/>
    <T text="动画讲解 · 校内考情 · 循序渐进" x={-215} y={87} fontSize={26} fill={C.muted} opacity={()=>enter(26.4)}/>
    {[90,150,220].map((h,i)=><Rect x={270+i*104} y={()=>110-h*enter(25.5+i*.35)/2} width={76}
      height={()=>h*enter(25.5+i*.35)} radius={12} fill={i===2?C.orange:C.ink}/>)}
    <Line points={[[245,-31],[346,-90],[458,-174]]} stroke={C.orange} lineWidth={5} endArrow end={()=>enter(26.3,1.2)} arrowSize={17}/>
    <Line points={[[-545,171],[545,171]]} stroke={C.line} lineWidth={1}/>
    <T text="从这一课，开始看懂 Python。" fontSize={33} y={223} opacity={()=>enter(27.1)}/>
    <T text="看懂 · 会做 · 能复习" fontSize={16} fill={C.muted} y={280} opacity={()=>enter(27.5)}/>
  </Node>);
  yield* tween(30,v=>time(v*30),linear);
});
