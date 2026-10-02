import {makeScene2D, Txt, Rect, Circle, Line, Node} from '@motion-canvas/2d';
import {createSignal, tween, linear} from '@motion-canvas/core';

const C={bg:'#FFF8EF',ink:'#243238',muted:'#728084',mint:'#BCE8D1',coral:'#FF8066',yellow:'#FFD166',white:'#FFFFFF',line:'#E6DDD2'};
const font='Noto Sans CJK SC';
const clamp=(v:number)=>Math.min(1,Math.max(0,v));
const ease=(v:number)=>1-Math.pow(1-clamp(v),3);
const T=(p:any)=><Txt fontFamily={font} fill={C.ink} {...p}/>;

export default makeScene2D(function*(view){
  const time=createSignal(0);
  view.fill(C.bg);
  view.add(<>
    <Circle size={760} x={520} y={-350} fill={C.mint} opacity={0.28}/>
    <Circle size={430} x={-570} y={310} fill={C.yellow} opacity={0.24}/>
    <T text="LISTLY" x={-548} y={-300} fontSize={20} fontWeight={800} letterSpacing={3}/>
    <T text="把想买的，都记下来" x={350} y={-300} fontSize={18} fill={C.muted}/>
    <Line points={[[-570,-264],[570,-264]]} stroke={C.line} lineWidth={2}/>
  </>);
  const intro=()=>ease(time()/0.8);
  view.add(<Node opacity={()=>intro()} y={()=>22*(1-intro())}>
    <T text="欢迎来到" x={-550} offsetX={-1} y={-165} fontSize={34} fill={C.muted} fontWeight={500}/>
    <T text="我的购物清单" x={-550} offsetX={-1} y={-85} fontSize={68} fontWeight={800}/>
    <T text="从一件小事开始，让每次购买都更从容。" x={-550} offsetX={-1} y={5} fontSize={22} fill={C.muted}/>
    <Rect x={-390} y={105} width={230} height={58} radius={29} fill={C.ink} opacity={()=>ease((time()-0.55)/0.5)}/>
    <T text="开始添加" x={-390} y={105} fontSize={24} fill={C.bg} fontWeight={700} opacity={()=>ease((time()-0.65)/0.45)}/>
  </Node>);
  const listY=(i:number)=>-95+i*78;
  view.add(<Node x={280} y={55}>
    <Rect width={420} height={430} radius={32} fill={C.white} stroke={C.line} lineWidth={2} shadowColor={'#D6C9BB'} shadowBlur={20} shadowOffset={[0,10]}/>
    <T text="本周要买" x={-128} y={-158} fontSize={25} fontWeight={700}/>
    <T text="3 件待办" x={125} y={-158} fontSize={18} fill={C.muted}/>
    {['牛奶','鸡蛋','咖啡豆'].map((s,i)=><Node y={()=>listY(i)+28*(1-ease((time()-(0.75+i*0.38))/0.55))} opacity={()=>ease((time()-(0.65+i*0.38))/0.55)}>
      <Circle x={-150} size={28} stroke={i===1?C.coral:C.ink} lineWidth={3} fill={i===1?C.coral:C.bg}/>
      {i===1?<Line points={[[-157,0],[-151,6],[-141,-7]]} stroke={C.white} lineWidth={3}/>:null}
      <T text={s} x={-120} offsetX={-1} fontSize={29} fontWeight={600}/>
      <T text={i===0?'早餐':i===1?'日常':'提神'} x={108} fontSize={16} fill={C.muted}/>
      <Line points={[[-165,27],[165,27]]} stroke={C.line} lineWidth={1}/>
    </Node>)}
    <Circle x={147} y={163} size={62} fill={C.coral} opacity={()=>ease((time()-2.1)/0.5)} scale={()=>.7+.3*ease((time()-2.1)/0.5)}/>
    <T text="+" x={147} y={163} fontSize={42} fill={C.white} fontWeight={500} opacity={()=>ease((time()-2.1)/0.5)}/>
  </Node>);
  view.add(<Node opacity={()=>ease((time()-3.0)/0.65)} y={()=>20*(1-ease((time()-3)/.65))}>
    <T text="准备好了吗？" x={-70} y={245} fontSize={28} fontWeight={700}/>
    <T text="今天，买得更聪明。" x={-45} y={285} fontSize={19} fill={C.muted}/>
  </Node>);
  view.add(<T text={()=>String(Math.min(5,Math.floor(time()))).padStart(2,'0')+' / 05'} x={505} y={330} fontSize={16} fill={C.muted}/>);
  yield* tween(5,v=>time(v*5),linear);
});
