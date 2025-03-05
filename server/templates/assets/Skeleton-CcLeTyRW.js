import{a as r,aH as w,b as P,j as E,u as S,o as x,q as T,h as k,ah as I,aI as N,a2 as C,aJ as R,z as A,aK as y}from"./index-DGLaFKvV.js";import{u as q}from"./use-houdini-DC53MCIA.js";const{cubicBezierEaseInOut:t,cubicBezierEaseOut:D,cubicBezierEaseIn:H}=w;function G({overflow:a="hidden",duration:n=".3s",originalTransition:i="",leavingDelay:e="0s",foldPadding:o=!1,enterToProps:s,leaveToProps:p,reverse:l=!1}={}){const d=l?"leave":"enter",c=l?"enter":"leave";return[r(`&.fade-in-height-expand-transition-${c}-from,
 &.fade-in-height-expand-transition-${d}-to`,Object.assign(Object.assign({},s),{opacity:1})),r(`&.fade-in-height-expand-transition-${c}-to,
 &.fade-in-height-expand-transition-${d}-from`,Object.assign(Object.assign({},p),{opacity:0,marginTop:"0 !important",marginBottom:"0 !important",paddingTop:o?"0 !important":void 0,paddingBottom:o?"0 !important":void 0})),r(`&.fade-in-height-expand-transition-${c}-active`,`
 overflow: ${a};
 transition:
 max-height ${n} ${t} ${e},
 opacity ${n} ${D} ${e},
 margin-top ${n} ${t} ${e},
 margin-bottom ${n} ${t} ${e},
 padding-top ${n} ${t} ${e},
 padding-bottom ${n} ${t} ${e}
 ${i?`,${i}`:""}
 `),r(`&.fade-in-height-expand-transition-${d}-active`,`
 overflow: ${a};
 transition:
 max-height ${n} ${t},
 opacity ${n} ${H},
 margin-top ${n} ${t},
 margin-bottom ${n} ${t},
 padding-top ${n} ${t},
 padding-bottom ${n} ${t}
 ${i?`,${i}`:""}
 `)]}const J=r([P("skeleton",`
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
 `)]),L=E({name:"Skeleton",inheritAttrs:!1,props:Object.assign(Object.assign({},x.props),{text:Boolean,round:Boolean,circle:Boolean,height:[String,Number],width:[String,Number],size:String,repeat:{type:Number,default:1},animated:{type:Boolean,default:!0},sharp:{type:Boolean,default:!0}}),setup(a){q();const{mergedClsPrefixRef:n}=S(a),i=x("Skeleton","-skeleton",J,R,a,n);return{mergedClsPrefix:n,style:T(()=>{var e,o;const s=i.value,{common:{cubicBezierEaseInOut:p}}=s,l=s.self,{color:d,colorEnd:c,borderRadius:z}=l;let $;const{circle:m,sharp:B,round:O,width:g,height:b,size:f,text:v,animated:j}=a;f!==void 0&&($=l[A("height",f)]);const u=m?(e=g??b)!==null&&e!==void 0?e:$:g,h=(o=m&&g!=null?g:b)!==null&&o!==void 0?o:$;return{display:v?"inline-block":"",verticalAlign:v?"-0.125em":"",borderRadius:m?"50%":O?"4096px":B?"":z,width:typeof u=="number"?y(u):u,height:typeof h=="number"?y(h):h,animation:j?"":"none","--n-bezier":p,"--n-color-start":d,"--n-color-end":c}})}},render(){const{repeat:a,style:n,mergedClsPrefix:i,$attrs:e}=this,o=k("div",I({class:`${i}-skeleton`,style:n},e));return a>1?k(C,null,N(a,null).map(s=>[o,`
`])):o}});export{L as N,G as f};
