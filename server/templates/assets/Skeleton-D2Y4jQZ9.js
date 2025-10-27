import{M as r,b1 as j,O as P,d as E,L as x,aw as S,b2 as T,F as N,X as C,a2 as k,b3 as I,p as R,a5 as A,b4 as y}from"./index-Ow1yCR_l.js";import{u as D}from"./use-houdini-D-sxWS9s.js";const{cubicBezierEaseInOut:t,cubicBezierEaseOut:F,cubicBezierEaseIn:L}=j;function G({overflow:o="hidden",duration:n=".3s",originalTransition:i="",leavingDelay:e="0s",foldPadding:a=!1,enterToProps:s,leaveToProps:p,reverse:l=!1}={}){const d=l?"leave":"enter",c=l?"enter":"leave";return[r(`&.fade-in-height-expand-transition-${c}-from,
 &.fade-in-height-expand-transition-${d}-to`,Object.assign(Object.assign({},s),{opacity:1})),r(`&.fade-in-height-expand-transition-${c}-to,
 &.fade-in-height-expand-transition-${d}-from`,Object.assign(Object.assign({},p),{opacity:0,marginTop:"0 !important",marginBottom:"0 !important",paddingTop:a?"0 !important":void 0,paddingBottom:a?"0 !important":void 0})),r(`&.fade-in-height-expand-transition-${c}-active`,`
 overflow: ${o};
 transition:
 max-height ${n} ${t} ${e},
 opacity ${n} ${F} ${e},
 margin-top ${n} ${t} ${e},
 margin-bottom ${n} ${t} ${e},
 padding-top ${n} ${t} ${e},
 padding-bottom ${n} ${t} ${e}
 ${i?`,${i}`:""}
 `),r(`&.fade-in-height-expand-transition-${d}-active`,`
 overflow: ${o};
 transition:
 max-height ${n} ${t},
 opacity ${n} ${L},
 margin-top ${n} ${t},
 margin-bottom ${n} ${t},
 padding-top ${n} ${t},
 padding-bottom ${n} ${t}
 ${i?`,${i}`:""}
 `)]}const M=r([P("skeleton",`
 height: 1em;
 width: 100%;
 transition:
 --n-color-start .3s var(--n-bezier),
 --n-color-end .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 animation: 2s skeleton-loading infinite cubic-bezier(0.36, 0, 0.64, 1);
 background-color: var(--n-color-start);
 `),r("@keyframes skeleton-loading",`
 0% {
 background: var(--n-color-start);
 }
 40% {
 background: var(--n-color-end);
 }
 80% {
 background: var(--n-color-start);
 }
 100% {
 background: var(--n-color-start);
 }
 `)]),H=E({name:"Skeleton",inheritAttrs:!1,props:Object.assign(Object.assign({},k.props),{text:Boolean,round:Boolean,circle:Boolean,height:[String,Number],width:[String,Number],size:String,repeat:{type:Number,default:1},animated:{type:Boolean,default:!0},sharp:{type:Boolean,default:!0}}),setup(o){D();const{mergedClsPrefixRef:n}=C(o),i=k("Skeleton","-skeleton",M,I,o,n);return{mergedClsPrefix:n,style:R(()=>{var e,a;const s=i.value,{common:{cubicBezierEaseInOut:p}}=s,l=s.self,{color:d,colorEnd:c,borderRadius:z}=l;let m;const{circle:$,sharp:B,round:O,width:g,height:h,size:f,text:v,animated:w}=o;f!==void 0&&(m=l[A("height",f)]);const u=$?(e=g??h)!==null&&e!==void 0?e:m:g,b=(a=$&&g!=null?g:h)!==null&&a!==void 0?a:m;return{display:v?"inline-block":"",verticalAlign:v?"-0.125em":"",borderRadius:$?"50%":O?"4096px":B?"":z,width:typeof u=="number"?y(u):u,height:typeof b=="number"?y(b):b,animation:w?"":"none","--n-bezier":p,"--n-color-start":d,"--n-color-end":c}})}},render(){const{repeat:o,style:n,mergedClsPrefix:i,$attrs:e}=this,a=x("div",S({class:`${i}-skeleton`,style:n},e));return o>1?x(N,null,T(o,null).map(s=>[a,`
`])):a}});export{H as N,G as f};
