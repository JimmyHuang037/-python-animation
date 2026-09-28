import project from './project?project';
import {Renderer,Vector2} from '@motion-canvas/core';
class CaptureExporter {
  static id='capture';
  static async create(){return new CaptureExporter();}
  async handleFrame(canvas:HTMLCanvasElement,frame:number){
    await (window as any).saveFrame(frame,canvas.toDataURL('image/png').split(',')[1]);
  }
}
(project.meta.rendering.exporter.exporters as any).push(CaptureExporter);
project.logger.onLogged.subscribe((entry:any)=>console.log('MC_LOG',JSON.stringify(entry)));
const renderer=new Renderer(project);
renderer.onFinished.subscribe(result=>(window as any).renderResult=result);
(window as any).startRender=async()=>{
 await document.fonts.load('600 36px "Noto Sans CJK SC"');
 await renderer.render({name:'promo30',range:[0,30],fps:30,size:new Vector2(1280,720),resolutionScale:1.5,colorSpace:'srgb',background:'#F4F3EB',exporter:{name:'capture',options:{}}});
 (window as any).renderDone=true;
};
(window as any).ready=true;
