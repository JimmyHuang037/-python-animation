/// <reference types="vite/client" />
/// <reference types="@motion-canvas/core/project" />
interface Window {ready:boolean;renderDone:boolean;startRender:(options?:{from:number;to:number})=>Promise<void>;saveFrame:(frame:number,png:string)=>Promise<void>;}

declare module "*?project" { const project: import("@motion-canvas/core").Project; export default project; }
