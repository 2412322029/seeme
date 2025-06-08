import{z as r,aX as j,A as P,d as T,y as x,ap as E,aY as S,F as N,K as A,Q as y,aZ as C,T as I,U as R,a_ as k}from"./index-DAkhcvNy.js";import{u as D}from"./use-houdini-CqCqhEt-.js";const{cubicBezierEaseInOut:t,cubicBezierEaseOut:F,cubicBezierEaseIn:K}=j;function Y({overflow:a="hidden",duration:n=".3s",originalTransition:i="",leavingDelay:e="0s",foldPadding:o=!1,enterToProps:s,leaveToProps:p,reverse:l=!1}={}){const d=l?"leave":"enter",c=l?"enter":"leave";return[r(`&.fade-in-height-expand-transition-${c}-from,
 &.fade-in-height-expand-transition-${d}-to`,Object.assign(Object.assign({},s),{opacity:1})),r(`&.fade-in-height-expand-transition-${c}-to,
 &.fade-in-height-expand-transition-${d}-from`,Object.assign(Object.assign({},p),{opacity:0,marginTop:"0 !important",marginBottom:"0 !important",paddingTop:o?"0 !important":void 0,paddingBottom:o?"0 !important":void 0})),r(`&.fade-in-height-expand-transition-${c}-active`,`
 overflow: ${a};
 transition:
 max-height ${n} ${t} ${e},
 opacity ${n} ${F} ${e},
 margin-top ${n} ${t} ${e},
 margin-bottom ${n} ${t} ${e},
 padding-top ${n} ${t} ${e},
 padding-bottom ${n} ${t} ${e}
 ${i?`,${i}`:""}
 `),r(`&.fade-in-height-expand-transition-${d}-active`,`
 overflow: ${a};
 transition:
 max-height ${n} ${t},
 opacity ${n} ${K},
 margin-top ${n} ${t},
 margin-bottom ${n} ${t},
 padding-top ${n} ${t},
 padding-bottom ${n} ${t}
 ${i?`,${i}`:""}
 `)]}const Q=r([P("skeleton",`
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
 `)]),Z=T({name:"Skeleton",inheritAttrs:!1,props:Object.assign(Object.assign({},y.props),{text:Boolean,round:Boolean,circle:Boolean,height:[String,Number],width:[String,Number],size:String,repeat:{type:Number,default:1},animated:{type:Boolean,default:!0},sharp:{type:Boolean,default:!0}}),setup(a){D();const{mergedClsPrefixRef:n}=A(a),i=y("Skeleton","-skeleton",Q,C,a,n);return{mergedClsPrefix:n,style:I(()=>{var e,o;const s=i.value,{common:{cubicBezierEaseInOut:p}}=s,l=s.self,{color:d,colorEnd:c,borderRadius:z}=l;let m;const{circle:$,sharp:B,round:O,width:g,height:b,size:f,text:v,animated:w}=a;f!==void 0&&(m=l[R("height",f)]);const u=$?(e=g??b)!==null&&e!==void 0?e:m:g,h=(o=$&&g!=null?g:b)!==null&&o!==void 0?o:m;return{display:v?"inline-block":"",verticalAlign:v?"-0.125em":"",borderRadius:$?"50%":O?"4096px":B?"":z,width:typeof u=="number"?k(u):u,height:typeof h=="number"?k(h):h,animation:w?"":"none","--n-bezier":p,"--n-color-start":d,"--n-color-end":c}})}},render(){const{repeat:a,style:n,mergedClsPrefix:i,$attrs:e}=this,o=x("div",E({class:`${i}-skeleton`,style:n},e));return a>1?x(N,null,S(a,null).map(s=>[o,`
`])):o}});export{Z as N,Y as f};
