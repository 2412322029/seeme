import{b as Ye,t as Q,g as We,a as Je,c as Xe,_ as Ze}from"./myfooter-LLhKI8wQ.js";import{c as le,h as g,a as C,b as u,d as P,e as x,i as en,f as nn,g as tn,j as G,k as ve,r as V,u as Y,t as we,l as ze,m as on,n as rn,o as j,p as Se,q as D,s as ne,v as ln,w as ie,N as an,x as Ce,y as sn,z as H,A as ee,B as cn,C as dn,D as un,E as bn,F as fe,G as ge,H as pn,I as mn,J as he,K as hn,L as vn,M as gn,O as F,P as Ae,Q as _e,R as fn,S as xn,T as yn,U as kn,V as X,W as wn,X as k,Y as O,_ as Be,Z as Re,$ as a,a0 as E,a1 as c,a2 as L,a3 as K,a4 as z,a5 as m,a6 as R,a7 as Z,a8 as xe,a9 as ye,aa as N,ab as te,ac as zn,ad as ke}from"./index-C-2t4lpF.js";import{f as Sn,N as J,a as ce}from"./Table-qgj4KypJ.js";import{u as Cn}from"./use-houdini-Bd_Chwmg.js";const An=le("n-checkbox-group"),_n=C([u("checkbox",`
 font-size: var(--n-font-size);
 outline: none;
 cursor: pointer;
 display: inline-flex;
 flex-wrap: nowrap;
 align-items: flex-start;
 word-break: break-word;
 line-height: var(--n-size);
 --n-merged-color-table: var(--n-color-table);
 `,[P("show-label","line-height: var(--n-label-line-height);"),C("&:hover",[u("checkbox-box",[x("border","border: var(--n-border-checked);")])]),C("&:focus:not(:active)",[u("checkbox-box",[x("border",`
 border: var(--n-border-focus);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),P("inside-table",[u("checkbox-box",`
 background-color: var(--n-merged-color-table);
 `)]),P("checked",[u("checkbox-box",`
 background-color: var(--n-color-checked);
 `,[u("checkbox-icon",[C(".check-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),P("indeterminate",[u("checkbox-box",[u("checkbox-icon",[C(".check-icon",`
 opacity: 0;
 transform: scale(.5);
 `),C(".line-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),P("checked, indeterminate",[C("&:focus:not(:active)",[u("checkbox-box",[x("border",`
 border: var(--n-border-checked);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),u("checkbox-box",`
 background-color: var(--n-color-checked);
 border-left: 0;
 border-top: 0;
 `,[x("border",{border:"var(--n-border-checked)"})])]),P("disabled",{cursor:"not-allowed"},[P("checked",[u("checkbox-box",`
 background-color: var(--n-color-disabled-checked);
 `,[x("border",{border:"var(--n-border-disabled-checked)"}),u("checkbox-icon",[C(".check-icon, .line-icon",{fill:"var(--n-check-mark-color-disabled-checked)"})])])]),u("checkbox-box",`
 background-color: var(--n-color-disabled);
 `,[x("border",`
 border: var(--n-border-disabled);
 `),u("checkbox-icon",[C(".check-icon, .line-icon",`
 fill: var(--n-check-mark-color-disabled);
 `)])]),x("label",`
 color: var(--n-text-color-disabled);
 `)]),u("checkbox-box-wrapper",`
 position: relative;
 width: var(--n-size);
 flex-shrink: 0;
 flex-grow: 0;
 user-select: none;
 -webkit-user-select: none;
 `),u("checkbox-box",`
 position: absolute;
 left: 0;
 top: 50%;
 transform: translateY(-50%);
 height: var(--n-size);
 width: var(--n-size);
 display: inline-block;
 box-sizing: border-box;
 border-radius: var(--n-border-radius);
 background-color: var(--n-color);
 transition: background-color 0.3s var(--n-bezier);
 `,[x("border",`
 transition:
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 border-radius: inherit;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 border: var(--n-border);
 `),u("checkbox-icon",`
 display: flex;
 align-items: center;
 justify-content: center;
 position: absolute;
 left: 1px;
 right: 1px;
 top: 1px;
 bottom: 1px;
 `,[C(".check-icon, .line-icon",`
 width: 100%;
 fill: var(--n-check-mark-color);
 opacity: 0;
 transform: scale(0.5);
 transform-origin: center;
 transition:
 fill 0.3s var(--n-bezier),
 transform 0.3s var(--n-bezier),
 opacity 0.3s var(--n-bezier),
 border-color 0.3s var(--n-bezier);
 `),en({left:"1px",top:"1px"})])]),x("label",`
 color: var(--n-text-color);
 transition: color .3s var(--n-bezier);
 user-select: none;
 -webkit-user-select: none;
 padding: var(--n-label-padding);
 font-weight: var(--n-label-font-weight);
 `,[C("&:empty",{display:"none"})])]),nn(u("checkbox",`
 --n-merged-color-table: var(--n-color-table-modal);
 `)),tn(u("checkbox",`
 --n-merged-color-table: var(--n-color-table-popover);
 `))]),Bn=Object.assign(Object.assign({},j.props),{size:String,checked:{type:[Boolean,String,Number],default:void 0},defaultChecked:{type:[Boolean,String,Number],default:!1},value:[String,Number],disabled:{type:Boolean,default:void 0},indeterminate:Boolean,label:String,focusable:{type:Boolean,default:!0},checkedValue:{type:[Boolean,String,Number],default:!0},uncheckedValue:{type:[Boolean,String,Number],default:!1},"onUpdate:checked":[Function,Array],onUpdateChecked:[Function,Array],privateInsideTable:Boolean,onChange:[Function,Array]}),oe=G({name:"Checkbox",props:Bn,setup(e){const n=ve(An,null),t=V(null),{mergedClsPrefixRef:b,inlineThemeDisabled:i,mergedRtlRef:s}=Y(e),w=V(e.defaultChecked),h=we(e,"checked"),f=ze(h,w),v=on(()=>{if(n){const d=n.valueSetRef.value;return!(!d||e.value===void 0)&&d.has(e.value)}return f.value===e.checkedValue}),S=rn(e,{mergedSize(d){const{size:_}=e;if(_!==void 0)return _;if(n){const{value:A}=n.mergedSizeRef;if(A!==void 0)return A}if(d){const{mergedSize:A}=d;if(A!==void 0)return A.value}return"medium"},mergedDisabled(d){const{disabled:_}=e;if(_!==void 0)return _;if(n){if(n.disabledRef.value)return!0;const{maxRef:{value:A},checkedCountRef:B}=n;if(A!==void 0&&B.value>=A&&!v.value)return!0;const{minRef:{value:U}}=n;if(U!==void 0&&B.value<=U&&v.value)return!0}return!!d&&d.disabled.value}}),{mergedDisabledRef:l,mergedSizeRef:o}=S,r=j("Checkbox","-checkbox",_n,sn,e,b);function p(d){if(n&&e.value!==void 0)n.toggleCheckbox(!v.value,e.value);else{const{onChange:_,"onUpdate:checked":A,onUpdateChecked:B}=e,{nTriggerFormInput:U,nTriggerFormChange:M}=S,q=v.value?e.uncheckedValue:e.checkedValue;A&&ee(A,q,d),B&&ee(B,q,d),_&&ee(_,q,d),U(),M(),w.value=q}}const y={focus:()=>{var d;(d=t.value)===null||d===void 0||d.focus()},blur:()=>{var d;(d=t.value)===null||d===void 0||d.blur()}},T=Se("Checkbox",s,b),I=D(()=>{const{value:d}=o,{common:{cubicBezierEaseInOut:_},self:{borderRadius:A,color:B,colorChecked:U,colorDisabled:M,colorTableHeader:q,colorTableHeaderModal:ae,colorTableHeaderPopover:se,checkMarkColor:W,checkMarkColorDisabled:$e,border:Ee,borderFocus:De,borderDisabled:je,borderChecked:Ie,boxShadowFocus:Ne,textColor:Ve,textColorDisabled:Ue,checkMarkColorDisabledChecked:Me,colorDisabledChecked:qe,borderDisabledChecked:Le,labelPadding:He,labelLineHeight:Qe,labelFontWeight:Fe,[H("fontSize",d)]:Ke,[H("size",d)]:Ge}}=r.value;return{"--n-label-line-height":Qe,"--n-label-font-weight":Fe,"--n-size":Ge,"--n-bezier":_,"--n-border-radius":A,"--n-border":Ee,"--n-border-checked":Ie,"--n-border-focus":De,"--n-border-disabled":je,"--n-border-disabled-checked":Le,"--n-box-shadow-focus":Ne,"--n-color":B,"--n-color-checked":U,"--n-color-table":q,"--n-color-table-modal":ae,"--n-color-table-popover":se,"--n-color-disabled":M,"--n-color-disabled-checked":qe,"--n-text-color":Ve,"--n-text-color-disabled":Ue,"--n-check-mark-color":W,"--n-check-mark-color-disabled":$e,"--n-check-mark-color-disabled-checked":Me,"--n-font-size":Ke,"--n-label-padding":He}}),$=i?ne("checkbox",D(()=>o.value[0]),I,e):void 0;return Object.assign(S,y,{rtlEnabled:T,selfRef:t,mergedClsPrefix:b,mergedDisabled:l,renderedChecked:v,mergedTheme:r,labelId:ln(),handleClick:function(d){l.value||p(d)},handleKeyUp:function(d){if(!l.value)switch(d.key){case" ":case"Enter":p(d)}},handleKeyDown:function(d){d.key===" "&&d.preventDefault()},cssVars:i?void 0:I,themeClass:$==null?void 0:$.themeClass,onRender:$==null?void 0:$.onRender})},render(){var e;const{$slots:n,renderedChecked:t,mergedDisabled:b,indeterminate:i,privateInsideTable:s,cssVars:w,labelId:h,label:f,mergedClsPrefix:v,focusable:S,handleKeyUp:l,handleKeyDown:o,handleClick:r}=this;(e=this.onRender)===null||e===void 0||e.call(this);const p=ie(n.default,y=>f||y?g("span",{class:`${v}-checkbox__label`,id:h},f||y):null);return g("div",{ref:"selfRef",class:[`${v}-checkbox`,this.themeClass,this.rtlEnabled&&`${v}-checkbox--rtl`,t&&`${v}-checkbox--checked`,b&&`${v}-checkbox--disabled`,i&&`${v}-checkbox--indeterminate`,s&&`${v}-checkbox--inside-table`,p&&`${v}-checkbox--show-label`],tabindex:b||!S?void 0:0,role:"checkbox","aria-checked":i?"mixed":t,"aria-labelledby":h,style:w,onKeyup:l,onKeydown:o,onClick:r,onMousedown:()=>{Ce("selectstart",window,y=>{y.preventDefault()},{once:!0})}},g("div",{class:`${v}-checkbox-box-wrapper`}," ",g("div",{class:`${v}-checkbox-box`},g(an,null,{default:()=>this.indeterminate?g("div",{key:"indeterminate",class:`${v}-checkbox-icon`},g("svg",{viewBox:"0 0 100 100",class:"line-icon"},g("path",{d:"M80.2,55.5H21.4c-2.8,0-5.1-2.5-5.1-5.5l0,0c0-3,2.3-5.5,5.1-5.5h58.7c2.8,0,5.1,2.5,5.1,5.5l0,0C85.2,53.1,82.9,55.5,80.2,55.5z"}))):g("div",{key:"check",class:`${v}-checkbox-icon`},g("svg",{viewBox:"0 0 64 64",class:"check-icon"},g("path",{d:"M50.42,16.76L22.34,39.45l-8.1-11.46c-1.12-1.58-3.3-1.96-4.88-0.84c-1.58,1.12-1.95,3.3-0.84,4.88l10.26,14.51  c0.56,0.79,1.42,1.31,2.38,1.45c0.16,0.02,0.32,0.03,0.48,0.03c0.8,0,1.57-0.27,2.2-0.78l30.99-25.03c1.5-1.21,1.74-3.42,0.52-4.92  C54.13,15.78,51.93,15.55,50.42,16.76z"})))}),g("div",{class:`${v}-checkbox-box__border`}))),p)}});let de;function Rn(){if(!cn)return!0;if(de===void 0){const e=document.createElement("div");e.style.display="flex",e.style.flexDirection="column",e.style.rowGap="1px",e.appendChild(document.createElement("div")),e.appendChild(document.createElement("div")),document.body.appendChild(e);const n=e.scrollHeight===1;return document.body.removeChild(e),de=n}return de}const Pn=Object.assign(Object.assign({},j.props),{align:String,justify:{type:String,default:"start"},inline:Boolean,vertical:Boolean,reverse:Boolean,size:{type:[String,Number,Array],default:"medium"},wrapItem:{type:Boolean,default:!0},itemClass:String,itemStyle:[String,Object],wrap:{type:Boolean,default:!0},internalUseGap:{type:Boolean,default:void 0}}),ue=G({name:"Space",props:Pn,setup(e){const{mergedClsPrefixRef:n,mergedRtlRef:t}=Y(e),b=j("Space","-space",void 0,un,e,n),i=Se("Space",t,n);return{useGap:Rn(),rtlEnabled:i,mergedClsPrefix:n,margin:D(()=>{const{size:s}=e;if(Array.isArray(s))return{horizontal:s[0],vertical:s[1]};if(typeof s=="number")return{horizontal:s,vertical:s};const{self:{[H("gap",s)]:w}}=b.value,{row:h,col:f}=bn(w);return{horizontal:fe(f),vertical:fe(h)}})}},render(){const{vertical:e,reverse:n,align:t,inline:b,justify:i,itemClass:s,itemStyle:w,margin:h,wrap:f,mergedClsPrefix:v,rtlEnabled:S,useGap:l,wrapItem:o,internalUseGap:r}=this,p=Sn(function(A,B="default",U=[]){const M=A.$slots[B];return M===void 0?U:M()}(this),!1);if(!p.length)return null;const y=`${h.horizontal}px`,T=h.horizontal/2+"px",I=`${h.vertical}px`,$=h.vertical/2+"px",d=p.length-1,_=i.startsWith("space-");return g("div",{role:"none",class:[`${v}-space`,S&&`${v}-space--rtl`],style:{display:b?"inline-flex":"flex",flexDirection:e&&!n?"column":e&&n?"column-reverse":!e&&n?"row-reverse":"row",justifyContent:["start","end"].includes(i)?`flex-${i}`:i,flexWrap:!f||e?"nowrap":"wrap",marginTop:l||e?"":`-${$}`,marginBottom:l||e?"":`-${$}`,alignItems:t,gap:l?`${h.vertical}px ${h.horizontal}px`:""}},o||!l&&!r?p.map((A,B)=>A.type===dn?A:g("div",{role:"none",class:s,style:[w,{maxWidth:"100%"},l?"":e?{marginBottom:B!==d?I:""}:S?{marginLeft:_?i==="space-between"&&B===d?"":T:B!==d?y:"",marginRight:_?i==="space-between"&&B===0?"":T:"",paddingTop:$,paddingBottom:$}:{marginRight:_?i==="space-between"&&B===d?"":T:B!==d?y:"",marginLeft:_?i==="space-between"&&B===0?"":T:"",paddingTop:$,paddingBottom:$}]},A)):p)}});Object.assign(Object.assign({},j.props),{left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"}});const On=le("n-float-button-group"),Tn=u("float-button",`
 user-select: none;
 cursor: pointer;
 color: var(--n-text-color);
 background-color: var(--n-color);
 font-size: 18px;
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 box-shadow: var(--n-box-shadow);
 display: flex;
 align-items: stretch;
 box-sizing: border-box;
`,[P("circle-shape",`
 border-radius: 4096px;
 `),P("square-shape",`
 border-radius: var(--n-border-radius-square);
 `),x("fill",`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0
 left: 0;
 transition: background-color .3s var(--n-bezier);
 border-radius: inherit;
 `),x("body",`
 position: relative;
 flex-grow: 1;
 display: flex;
 align-items: center;
 justify-content: center;
 transition: transform .3s var(--n-bezier), opacity .3s var(--n-bezier);
 border-radius: inherit;
 flex-direction: column;
 box-sizing: border-box;
 padding: 2px 4px;
 gap: 2px;
 transform: scale(1);
 `,[x("description",`
 font-size: 12px;
 text-align: center;
 line-height: 14px;
 `)]),C("&:hover","box-shadow: var(--n-box-shadow-hover);",[C(">",[x("fill",`
 background-color: var(--n-color-hover);
 `)])]),C("&:active","box-shadow: var(--n-box-shadow-pressed);",[C(">",[x("fill",`
 background-color: var(--n-color-pressed);
 `)])]),P("show-menu",[C(">",[x("menu",`
 pointer-events: all;
 bottom: 100%;
 opacity: 1;
 `),x("close",`
 transform: scale(1);
 opacity: 1;
 `),x("body",`
 transform: scale(0.75);
 opacity: 0;
 `)])]),x("close",`
 opacity: 0;
 transform: scale(0.75);
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0;
 left: 0;
 display: flex;
 align-items: center;
 justify-content: center;
 transition: transform .3s var(--n-bezier), opacity .3s var(--n-bezier);
 `),x("menu",`
 position: absolute;
 bottom: calc(100% - 8px);
 display: flex;
 flex-direction: column;
 opacity: 0;
 pointer-events: none;
 transition:
 opacity .3s var(--n-bezier),
 bottom .3s var(--n-bezier); 
 `,[C("> *",`
 margin-bottom: 16px;
 `),u("float-button",`
 position: relative !important;
 `)])]),$n=Object.assign(Object.assign({},j.props),{width:{type:[Number,String],default:40},height:{type:[Number,String],default:40},left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"},type:{type:String,default:"default"},menuTrigger:String,showMenu:{type:Boolean,default:void 0},onUpdateShowMenu:{type:[Function,Array],default:void 0},"onUpdate:showMenu":{type:[Function,Array],default:void 0}}),be=G({name:"FloatButton",props:$n,slots:Object,setup(e){const{mergedClsPrefixRef:n,inlineThemeDisabled:t}=Y(e),b=V(null),i=j("FloatButton","-float-button",Tn,gn,e,n),s=ve(On,null),w=V(!1),h=we(e,"showMenu"),f=ze(h,w);function v(y){const{onUpdateShowMenu:T,"onUpdate:showMenu":I}=e;w.value=y,T&&ee(T,y),I&&ee(I,y)}const S=D(()=>{const{self:{color:y,textColor:T,boxShadow:I,boxShadowHover:$,boxShadowPressed:d,colorHover:_,colorPrimary:A,colorPrimaryHover:B,textColorPrimary:U,borderRadiusSquare:M,colorPressed:q,colorPrimaryPressed:ae},common:{cubicBezierEaseInOut:se}}=i.value,{type:W}=e;return{"--n-bezier":se,"--n-box-shadow":I,"--n-box-shadow-hover":$,"--n-box-shadow-pressed":d,"--n-color":W==="primary"?A:y,"--n-text-color":W==="primary"?U:T,"--n-color-hover":W==="primary"?B:_,"--n-color-pressed":W==="primary"?ae:q,"--n-border-radius-square":M}}),l=D(()=>{const{width:y,height:T}=e;return Object.assign({position:s?void 0:e.position,width:F(y),minHeight:F(T)},s?null:{left:F(e.left),right:F(e.right),top:F(e.top),bottom:F(e.bottom)})}),o=D(()=>s?s.shapeRef.value:e.shape),r=()=>{e.menuTrigger==="hover"&&f.value&&v(!1)},p=t?ne("float-button",D(()=>e.type[0]),S,e):void 0;return ge(()=>{const y=b.value;y&&Ce("mousemoveoutside",y,r)}),pn(()=>{const y=b.value;y&&mn("mousemoveoutside",y,r)}),{inlineStyle:l,selfElRef:b,cssVars:t?void 0:S,mergedClsPrefix:n,mergedShape:o,mergedShowMenu:f,themeClass:p==null?void 0:p.themeClass,onRender:p==null?void 0:p.onRender,Mouseenter:()=>{e.menuTrigger==="hover"&&v(!0)},handleMouseleave:r,handleClick:()=>{e.menuTrigger==="click"&&v(!f.value)}}},render(){var e;const{mergedClsPrefix:n,cssVars:t,mergedShape:b,type:i,menuTrigger:s,mergedShowMenu:w,themeClass:h,$slots:f,inlineStyle:v,onRender:S}=this;return S==null||S(),g("div",{ref:"selfElRef",class:[`${n}-float-button`,`${n}-float-button--${b}-shape`,`${n}-float-button--${i}-type`,w&&`${n}-float-button--show-menu`,h],style:[t,v],onMouseenter:this.Mouseenter,onMouseleave:this.handleMouseleave,onClick:this.handleClick,role:"button"},g("div",{class:`${n}-float-button__fill`,"aria-hidden":!0}),g("div",{class:`${n}-float-button__body`},(e=f.default)===null||e===void 0?void 0:e.call(f),ie(f.description,l=>l?g("div",{class:`${n}-float-button__description`},l):null)),s?g("div",{class:`${n}-float-button__close`},g(hn,{clsPrefix:n},{default:()=>g(vn,null)})):null,s?g("div",{onClick:l=>{l.stopPropagation()},"data-float-button-menu":!0,class:`${n}-float-button__menu`},he(f.menu,()=>[])):null)}}),Pe={type:String,default:"static"},En=u("layout",`
 color: var(--n-text-color);
 background-color: var(--n-color);
 box-sizing: border-box;
 position: relative;
 z-index: auto;
 flex: auto;
 overflow: hidden;
 transition:
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
`,[u("layout-scroll-container",`
 overflow-x: hidden;
 box-sizing: border-box;
 height: 100%;
 `),P("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),Dn={embedded:Boolean,position:Pe,nativeScrollbar:{type:Boolean,default:!0},scrollbarProps:Object,onScroll:Function,contentClass:String,contentStyle:{type:[String,Object],default:""},hasSider:Boolean,siderPlacement:{type:String,default:"left"}},jn=le("n-layout");function Oe(e){return G({name:e?"LayoutContent":"Layout",props:Object.assign(Object.assign({},j.props),Dn),setup(n){const t=V(null),b=V(null),{mergedClsPrefixRef:i,inlineThemeDisabled:s}=Y(n),w=j("Layout","-layout",En,Ae,n,i);_e(jn,n);let h=0,f=0;fn(()=>{if(n.nativeScrollbar){const o=t.value;o&&(o.scrollTop=f,o.scrollLeft=h)}});const v={scrollTo:function(o,r){if(n.nativeScrollbar){const{value:p}=t;p&&(r===void 0?p.scrollTo(o):p.scrollTo(o,r))}else{const{value:p}=b;p&&p.scrollTo(o,r)}}},S=D(()=>{const{common:{cubicBezierEaseInOut:o},self:r}=w.value;return{"--n-bezier":o,"--n-color":n.embedded?r.colorEmbedded:r.color,"--n-text-color":r.textColor}}),l=s?ne("layout",D(()=>n.embedded?"e":""),S,n):void 0;return Object.assign({mergedClsPrefix:i,scrollableElRef:t,scrollbarInstRef:b,hasSiderStyle:{display:"flex",flexWrap:"nowrap",width:"100%",flexDirection:"row"},mergedTheme:w,handleNativeElScroll:o=>{var r;const p=o.target;h=p.scrollLeft,f=p.scrollTop,(r=n.onScroll)===null||r===void 0||r.call(n,o)},cssVars:s?void 0:S,themeClass:l==null?void 0:l.themeClass,onRender:l==null?void 0:l.onRender},v)},render(){var n;const{mergedClsPrefix:t,hasSider:b}=this;(n=this.onRender)===null||n===void 0||n.call(this);const i=b?this.hasSiderStyle:void 0,s=[this.themeClass,e&&`${t}-layout-content`,`${t}-layout`,`${t}-layout--${this.position}-positioned`];return g("div",{class:s,style:this.cssVars},this.nativeScrollbar?g("div",{ref:"scrollableElRef",class:[`${t}-layout-scroll-container`,this.contentClass],style:[this.contentStyle,i],onScroll:this.handleNativeElScroll},this.$slots):g(xn,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:this.contentClass,contentStyle:[this.contentStyle,i]}),this.$slots))}})}const In=Oe(!1),Nn=Oe(!0),Vn=u("layout-header",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 box-sizing: border-box;
 width: 100%;
 background-color: var(--n-color);
 color: var(--n-text-color);
`,[P("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 `),P("bordered",`
 border-bottom: solid 1px var(--n-border-color);
 `)]),Un={position:Pe,inverted:Boolean,bordered:{type:Boolean,default:!1}},Mn=G({name:"LayoutHeader",props:Object.assign(Object.assign({},j.props),Un),setup(e){const{mergedClsPrefixRef:n,inlineThemeDisabled:t}=Y(e),b=j("Layout","-layout-header",Vn,Ae,e,n),i=D(()=>{const{common:{cubicBezierEaseInOut:w},self:h}=b.value,f={"--n-bezier":w};return e.inverted?(f["--n-color"]=h.headerColorInverted,f["--n-text-color"]=h.textColorInverted,f["--n-border-color"]=h.headerBorderColorInverted):(f["--n-color"]=h.headerColor,f["--n-text-color"]=h.textColor,f["--n-border-color"]=h.headerBorderColor),f}),s=t?ne("layout-header",D(()=>e.inverted?"a":"b"),i,e):void 0;return{mergedClsPrefix:n,cssVars:t?void 0:i,themeClass:s==null?void 0:s.themeClass,onRender:s==null?void 0:s.onRender}},render(){var e;const{mergedClsPrefix:n}=this;return(e=this.onRender)===null||e===void 0||e.call(this),g("div",{class:[`${n}-layout-header`,this.themeClass,this.position&&`${n}-layout-header--${this.position}-positioned`,this.bordered&&`${n}-layout-header--bordered`],style:this.cssVars},this.$slots)}}),qn=u("timeline",`
 position: relative;
 width: 100%;
 display: flex;
 flex-direction: column;
 line-height: 1.25;
`,[P("horizontal",`
 flex-direction: row;
 `,[C(">",[u("timeline-item",`
 flex-shrink: 0;
 padding-right: 40px;
 `,[P("dashed-line-type",[C(">",[u("timeline-item-timeline",[x("line",`
 background-image: linear-gradient(90deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 10px 1px;
 `)])])]),C(">",[u("timeline-item-content",`
 margin-top: calc(var(--n-icon-size) + 12px);
 `,[C(">",[x("meta",`
 margin-top: 6px;
 margin-bottom: unset;
 `)])]),u("timeline-item-timeline",`
 width: 100%;
 height: calc(var(--n-icon-size) + 12px);
 `,[x("line",`
 left: var(--n-icon-size);
 top: calc(var(--n-icon-size) / 2 - 1px);
 right: 0px;
 width: unset;
 height: 2px;
 `)])])])])]),P("right-placement",[u("timeline-item",[u("timeline-item-content",`
 text-align: right;
 margin-right: calc(var(--n-icon-size) + 12px);
 `),u("timeline-item-timeline",`
 width: var(--n-icon-size);
 right: 0;
 `)])]),P("left-placement",[u("timeline-item",[u("timeline-item-content",`
 margin-left: calc(var(--n-icon-size) + 12px);
 `),u("timeline-item-timeline",`
 left: 0;
 `)])]),u("timeline-item",`
 position: relative;
 `,[C("&:last-child",[u("timeline-item-timeline",[x("line",`
 display: none;
 `)]),u("timeline-item-content",[x("meta",`
 margin-bottom: 0;
 `)])]),u("timeline-item-content",[x("title",`
 margin: var(--n-title-margin);
 font-size: var(--n-title-font-size);
 transition: color .3s var(--n-bezier);
 font-weight: var(--n-title-font-weight);
 color: var(--n-title-text-color);
 `),x("content",`
 transition: color .3s var(--n-bezier);
 font-size: var(--n-content-font-size);
 color: var(--n-content-text-color);
 `),x("meta",`
 transition: color .3s var(--n-bezier);
 font-size: 12px;
 margin-top: 6px;
 margin-bottom: 20px;
 color: var(--n-meta-text-color);
 `)]),P("dashed-line-type",[u("timeline-item-timeline",[x("line",`
 --n-color-start: var(--n-line-color);
 transition: --n-color-start .3s var(--n-bezier);
 background-color: transparent;
 background-image: linear-gradient(180deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 1px 10px;
 `)])]),u("timeline-item-timeline",`
 width: calc(var(--n-icon-size) + 12px);
 position: absolute;
 top: calc(var(--n-title-font-size) * 1.25 / 2 - var(--n-icon-size) / 2);
 height: 100%;
 `,[x("circle",`
 border: var(--n-circle-border);
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 border-radius: var(--n-icon-size);
 box-sizing: border-box;
 `),x("icon",`
 color: var(--n-icon-color);
 font-size: var(--n-icon-size);
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 display: flex;
 align-items: center;
 justify-content: center;
 `),x("line",`
 transition: background-color .3s var(--n-bezier);
 position: absolute;
 top: var(--n-icon-size);
 left: calc(var(--n-icon-size) / 2 - 1px);
 bottom: 0px;
 width: 2px;
 background-color: var(--n-line-color);
 `)])])]),Ln=Object.assign(Object.assign({},j.props),{horizontal:Boolean,itemPlacement:{type:String,default:"left"},size:{type:String,default:"medium"},iconSize:Number}),Te=le("n-timeline"),pe=G({name:"Timeline",props:Ln,setup(e,{slots:n}){const{mergedClsPrefixRef:t}=Y(e),b=j("Timeline","-timeline",qn,yn,e,t);return _e(Te,{props:e,mergedThemeRef:b,mergedClsPrefixRef:t}),()=>{const{value:i}=t;return g("div",{class:[`${i}-timeline`,e.horizontal&&`${i}-timeline--horizontal`,`${i}-timeline--${e.size}-size`,!e.horizontal&&`${i}-timeline--${e.itemPlacement}-placement`]},n)}}}),me=G({name:"TimelineItem",props:{time:[String,Number],title:String,content:String,color:String,lineType:{type:String,default:"default"},type:{type:String,default:"default"}},slots:Object,setup(e){const n=ve(Te);n||kn("timeline-item","`n-timeline-item` must be placed inside `n-timeline`."),Cn();const{inlineThemeDisabled:t}=Y(),b=D(()=>{const{props:{size:s,iconSize:w},mergedThemeRef:h}=n,{type:f}=e,{self:{titleTextColor:v,contentTextColor:S,metaTextColor:l,lineColor:o,titleFontWeight:r,contentFontSize:p,[H("iconSize",s)]:y,[H("titleMargin",s)]:T,[H("titleFontSize",s)]:I,[H("circleBorder",f)]:$,[H("iconColor",f)]:d},common:{cubicBezierEaseInOut:_}}=h.value;return{"--n-bezier":_,"--n-circle-border":$,"--n-icon-color":d,"--n-content-font-size":p,"--n-content-text-color":S,"--n-line-color":o,"--n-meta-text-color":l,"--n-title-font-size":I,"--n-title-font-weight":r,"--n-title-margin":T,"--n-title-text-color":v,"--n-icon-size":F(w)||y}}),i=t?ne("timeline-item",D(()=>{const{props:{size:s,iconSize:w}}=n,{type:h}=e;return`${s[0]}${w||"a"}${h[0]}`}),b,n.props):void 0;return{mergedClsPrefix:n.mergedClsPrefixRef,cssVars:t?void 0:b,themeClass:i==null?void 0:i.themeClass,onRender:i==null?void 0:i.onRender}},render(){const{mergedClsPrefix:e,color:n,onRender:t,$slots:b}=this;return t==null||t(),g("div",{class:[`${e}-timeline-item`,this.themeClass,`${e}-timeline-item--${this.type}-type`,`${e}-timeline-item--${this.lineType}-line-type`],style:this.cssVars},g("div",{class:`${e}-timeline-item-timeline`},g("div",{class:`${e}-timeline-item-timeline__line`}),ie(b.icon,i=>i?g("div",{class:`${e}-timeline-item-timeline__icon`,style:{color:n}},i):g("div",{class:`${e}-timeline-item-timeline__circle`,style:{borderColor:n}}))),g("div",{class:`${e}-timeline-item-content`},ie(b.header,i=>i||this.title?g("div",{class:`${e}-timeline-item-content__title`},i||this.title):null),g("div",{class:`${e}-timeline-item-content__content`},he(b.default,()=>[this.content])),g("div",{class:`${e}-timeline-item-content__meta`},he(b.footer,()=>[this.time]))))}}),Hn=["innerHTML"],Qn={__name:"ai",setup(e){const n=V("");return ge(()=>{try{const t=new EventSource(Ye+"/ai_summary");n.value+='<p style="margin: 5px;color: aquamarine;"> AI 摘要</p>',t.onmessage=b=>{n.value+=b.data},t.addEventListener("end",()=>{t.close()}),t.onerror=b=>{t.close()},window.eventSource=t}catch(t){X(t.message,{theme:"auto",type:"error"}),n.value+=`<p style="color: red;">${t.message}</p>`}}),wn(()=>{var t;(t=window.eventSource)==null||t.close(),window.eventSource=void 0}),(t,b)=>(k(),O("div",{id:"ai-container",style:{"max-width":"800px",border:"1px solid #5c5c5c","border-radius":"20px",padding:"10px",margin:"5px"},innerHTML:n.value},null,8,Hn))}},re=e=>e.includes("QQ")?"/assets/qq.png":e.includes("Chrome")?"data:image/png;base64,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":e.includes("哔哩哔哩")?"/assets/bilibili.jpg":"",Fn={key:0,title:"",style:{"min-width":"700px",overflow:"auto"}},Kn={style:{margin:"0"}},Gn={id:"icarea",style:{display:"flex","justify-content":"flex-start","align-items":"center"}},Yn=["src"],Wn=["src"],Jn=Be({__name:"show_activity_window",setup(e){const n=V();return Re(()=>{We().then(t=>{typeof t!="string"?n.value=t:X(t,{theme:"auto",type:"error"})}).catch(t=>{X(t,{theme:"auto",type:"error"})})}),(t,b)=>{var i;return(i=n.value)!=null&&i.activity_window?(k(),O("div",Fn,[a("p",Kn,"活动程序 "+E(c(Q)(n.value.report_time)),1),a("div",Gn,[a("img",{src:c("/assets/win.png"),class:"ic",style:{padding:"0px 5px","margin-top":"-8px"}},null,8,Yn),(k(!0),O(L,null,K(n.value.activity_window,(s,w)=>(k(),O("div",{key:w,class:"icitem"},[z(c(J),{trigger:"hover",placement:"top"},{trigger:m(()=>[a("img",{src:"/exe_icon/"+s.exe_name+".png",class:"ic"},null,8,Wn)]),default:m(()=>[R(" "+E(s.title),1)]),_:2},1024)]))),128))])])):Z("",!0)}}},[["__scopeId","data-v-137d535c"]]),Xn={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/releases"},Zn={style:{display:"flex","align-items":"center"}},et=["src"],nt={key:1},tt=["src"],ot={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/自动汇报.js"},rt=["href"],it={key:1},lt=["src"],at={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/%E8%87%AA%E5%8A%A8%E6%B1%87%E6%8A%A5.macro"},st={style:{display:"flex","align-items":"center"}},ct=["src"],dt={key:1},ut=["src"],bt=Be({__name:"pcstatus",setup(e){const n=V(!1),t=xe([!0,!0,!0]);ge(()=>{const l=localStorage.getItem("showtimeline");n.value=l?JSON.parse(l):window.innerWidth<=900;const o=localStorage.getItem("showwhat");if(o){const r=JSON.parse(o);t[0]=r[0],t[1]=r[1],t[2]=r[2]}else t.fill(!0)}),ye(n,l=>{localStorage.setItem("showtimeline",JSON.stringify(l))}),ye(t,l=>{localStorage.setItem("showwhat",JSON.stringify(l))});const b=xe({info:""}),i=V(),s=V({browser:0,pc:0,phone:0});function w(){i.value=void 0,Je().then(l=>{typeof l!="string"?s.value=l:X(l,{theme:"auto",type:"error"})}).catch(l=>{X(l,{theme:"auto",type:"error"})}),Xe().then(l=>{typeof l!="string"?i.value=l:b.info=l}).catch(l=>{X(l,{theme:"auto",type:"error"})})}function h(l,o){return l.length>o?l.substring(0,o)+"...":l}function f(l){const o=new Date(1e3*l);return`${o.getFullYear()}-${String(o.getMonth()+1).padStart(2,"0")}-${String(o.getDate()).padStart(2,"0")} ${String(o.getHours()).padStart(2,"0")}:${String(o.getMinutes()).padStart(2,"0")}:${String(o.getSeconds()).padStart(2,"0")}`}function v(l){return l.slice().reverse()}function S(l){l.target.src="/assets/desktop.png"}return Re(()=>{w()}),(l,o)=>(k(),N(c(In),null,{default:m(()=>[z(c(Mn),null,{default:m(()=>[z(c(te),{title:"你在干什么?",style:{"margin-bottom":"10px"}},{default:m(()=>[z(Qn),z(c(ue),null,{default:m(()=>[a("span",null,[o[4]||(o[4]=R("时间线表示 ")),z(c(oe),{checked:n.value,"onUpdate:checked":o[0]||(o[0]=r=>n.value=r)},null,8,["checked"])]),a("span",null,[o[5]||(o[5]=R("显示电脑 ")),z(c(oe),{checked:t[0],"onUpdate:checked":o[1]||(o[1]=r=>t[0]=r)},null,8,["checked"])]),a("span",null,[o[6]||(o[6]=R("显示浏览器 ")),z(c(oe),{checked:t[1],"onUpdate:checked":o[2]||(o[2]=r=>t[1]=r)},null,8,["checked"])]),a("span",null,[o[7]||(o[7]=R("显示手机 ")),z(c(oe),{checked:t[2],"onUpdate:checked":o[3]||(o[3]=r=>t[2]=r)},null,8,["checked"])])]),_:1}),z(c(zn),{onClick:w,text:"",style:{margin:"10px 0",float:"right","font-size":"20px"},title:"刷新"},{default:m(()=>o[8]||(o[8]=[R("↻")])),_:1})]),_:1})]),_:1}),z(c(Nn),null,{default:m(()=>[z(c(ue),{vertical:""},{default:m(()=>[i.value?(k(),N(c(ue),{key:0,vertical:""},{default:m(()=>[t[0]?(k(),N(c(te),{key:0,title:"电脑(最新"+s.value.pc+"项)"},{"header-extra":m(()=>[z(c(J),{trigger:"hover",placement:"right"},{trigger:m(()=>[a("a",Xn,[z(c(be),{position:"relative"},{default:m(()=>o[9]||(o[9]=[R("?")])),_:1})])]),default:m(()=>[o[10]||(o[10]=R(" 电脑端自动报告程序,点击前往 "))]),_:1})]),default:m(()=>[z(Jn),n.value?(k(),O("div",nt,[z(c(pe),null,{default:m(()=>[(k(!0),O(L,null,K(i.value.pc,(r,p)=>(k(),N(c(me),{key:p,type:"success",title:r.exe_name,content:r.running_exe,time:c(Q)(r.report_time)},ke({_:2},[r.exe_name?{name:"icon",fn:m(()=>[a("img",{src:"/exe_icon/"+r.exe_name+".png",alt:"",onError:S,style:{width:"20px","z-index":"2"}},null,40,tt)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(k(),N(c(ce),{key:0,bordered:!1},{default:m(()=>[o[11]||(o[11]=a("thead",null,[a("tr",null,[a("th",null,"可执行程序"),a("th",null,"前台窗口标题"),a("th",null,"时间")])],-1)),a("tbody",null,[(k(!0),O(L,null,K(v(i.value.pc),(r,p)=>(k(),O("tr",{key:p},[a("td",null,[a("div",Zn,[a("img",{size:"small",src:"/exe_icon/"+r.exe_name+".png",onError:S,style:{margin:"0 5px",width:"20px"}},null,40,et),R(" "+E(r.exe_name),1)])]),a("td",null,[z(c(J),{"show-arrow":!1,trigger:"hover"},{trigger:m(()=>{return[R(E(h((y=r.running_exe,y.includes("Google Chrome")?"Google Chrome":y),30)),1)];var y}),default:m(()=>[R(" "+E(r.running_exe),1)]),_:2},1024)]),a("td",null,E(c(Q)(r.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0),t[1]?(k(),N(c(te),{key:1,title:"电脑浏览器(最新"+s.value.browser+"项)"},{"header-extra":m(()=>[z(c(J),{trigger:"hover",placement:"right"},{trigger:m(()=>[a("a",ot,[z(c(be),{position:"relative"},{default:m(()=>o[12]||(o[12]=[R("?")])),_:1})])]),default:m(()=>[o[13]||(o[13]=R(" 浏览器油猴脚本,点击前往 "))]),_:1})]),default:m(()=>[n.value?(k(),O("div",it,[z(c(pe),null,{default:m(()=>[(k(!0),O(L,null,K(i.value.browser,(r,p)=>(k(),N(c(me),{key:p,type:"success",title:h(r.title,70),content:h(r.url,70),time:c(Q)(r.report_time)},{icon:m(()=>[a("img",{src:c(re)("Chrome"),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,lt)]),_:2},1032,["title","content","time"]))),128))]),_:1})])):(k(),N(c(ce),{key:0,bordered:!1},{default:m(()=>[o[14]||(o[14]=a("thead",null,[a("tr",null,[a("th",null,"网页标题"),a("th",null,"网页链接"),a("th",null,"时间")])],-1)),a("tbody",null,[(k(!0),O(L,null,K(v(i.value.browser),(r,p)=>(k(),O("tr",{key:p},[a("td",null,[z(c(J),{trigger:"hover"},{trigger:m(()=>[R(E(h(r.title,30)),1)]),default:m(()=>[R(" "+E(r.title),1)]),_:2},1024)]),a("td",null,[a("a",{target:"_blank",href:r.url,class:"nowrap-ellipsis"},E(h(r.url,30)),9,rt)]),a("td",null,E(c(Q)(r.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0),t[2]?(k(),N(c(te),{key:2,title:"手机(最新"+s.value.phone+"项)"},{"header-extra":m(()=>[z(c(J),{trigger:"hover",placement:"right"},{trigger:m(()=>[a("a",at,[z(c(be),{position:"relative"},{default:m(()=>o[15]||(o[15]=[R("?")])),_:1})])]),default:m(()=>[o[16]||(o[16]=R(" 点击前往, 下载文件导入安卓MacroDroid软件 "))]),_:1})]),default:m(()=>[n.value?(k(),O("div",dt,[z(c(pe),null,{default:m(()=>[(k(!0),O(L,null,K(i.value.phone,(r,p)=>(k(),N(c(me),{key:p,type:"success",title:r.app,content:r.battery_level+"  / wifi信号:  "+r.wifi_ssid,time:c(Q)(f(r.report_time))},ke({_:2},[c(re)(r.app)?{name:"icon",fn:m(()=>[a("img",{src:c(re)(r.app),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,ut)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(k(),N(c(ce),{key:0,bordered:!1},{default:m(()=>[o[17]||(o[17]=a("thead",null,[a("tr",null,[a("th",null,"前台应用"),a("th",null,"电池"),a("th",null,"wifi"),a("th",null,"时间")])],-1)),a("tbody",null,[(k(!0),O(L,null,K(v(i.value.phone),(r,p)=>(k(),O("tr",{key:p},[a("td",null,[a("div",st,[a("img",{size:"small",src:c(re)(r.app),style:{margin:"0 5px",width:"20px"}},null,8,ct),R(" "+E(r.app),1)])]),a("td",null,E(r.battery_level),1),a("td",null,E(r.wifi_ssid),1),a("td",null,E(c(Q)(f(r.report_time))),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0)]),_:1})):Z("",!0)]),_:1})]),_:1})]),_:1}))}},[["__scopeId","data-v-b9452990"]]),gt={__name:"home",setup:e=>(n,t)=>(k(),O(L,null,[z(bt),z(Ze)],64))};export{gt as default};
