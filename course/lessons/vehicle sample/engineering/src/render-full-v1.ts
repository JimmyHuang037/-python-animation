import project from './full-project-v1?project';
import {Renderer,Vector2} from '@motion-canvas/core';
class FrameCapture {
 static id='vehicle-frame-capture';
 static async create(){return new FrameCapture();}
 async handleFrame(canvas:HTMLCanvasElement,frame:number){await window.saveFrame(frame,canvas.toDataURL('image/png').split(',')[1]);}
}
(project.meta.rendering.exporter.exporters as any).push(FrameCapture);
project.logger.onLogged.subscribe(entry=>console.log('MC_LOG',JSON.stringify(entry)));
const renderer=new Renderer(project);
window.startRender=async(options?:{from:number;to:number})=>{
 await document.fonts.load('700 62px "Noto Sans CJK SC"');
 await document.fonts.load('600 30px "Noto Sans CJK SC"');
 await document.fonts.ready;
 await renderer.render({name:'vehicle-full-v1-150s',range:[options?.from ?? 0,options?.to ?? 150],fps:30,size:new Vector2(1920,1080),resolutionScale:1,colorSpace:'srgb',background:'#FAF8F2',exporter:{name:'vehicle-frame-capture',options:{}}});
 window.renderDone=true;
};
window.ready=true;
