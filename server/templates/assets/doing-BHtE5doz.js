import{x as le,y as p,z as S,A as c,B as He,C as Ke,D as A,E as g,G as Ye,d as G,H as ie,N as Je,I as ke,J as pe,r as E,K as W,L as we,M as ze,O as Ge,P as We,Q as $,R as Xe,S as Ze,T as D,U as H,V as ne,W as en,X as ee,Y as me,Z as nn,$ as tn,a0 as on,a1 as q,b as ve,a2 as rn,a3 as ln,a4 as an,a5 as sn,a6 as Se,a7 as Ce,a8 as cn,a9 as dn,_ as ge,aa as un,ab as J,ac as bn,c as P,o as y,a as i,i as _,ad as _e,v as Z,t as O,u as s,ae as L,F as Q,e as F,h as w,w as u,af as hn,ag as fe,ah as xe,k as T,ai as mn,aj as pn,ak as vn,al as ye}from"./index-DAkhcvNy.js";import{N as Y,a as ce}from"./Table-BzSrFZ5U.js";import{N as te}from"./Card-CimJnkoP.js";import{N as de}from"./Space-csxnv958.js";import{u as gn}from"./use-houdini-CqCqhEt-.js";const fn=le("n-checkbox-group"),xn=S([c("checkbox",`
 font-size: var(--n-font-size);
 outline: none;
 cursor: pointer;
 display: inline-flex;
 flex-wrap: nowrap;
 align-items: flex-start;
 word-break: break-word;
 line-height: var(--n-size);
 --n-merged-color-table: var(--n-color-table);
 `,[A("show-label","line-height: var(--n-label-line-height);"),S("&:hover",[c("checkbox-box",[g("border","border: var(--n-border-checked);")])]),S("&:focus:not(:active)",[c("checkbox-box",[g("border",`
 border: var(--n-border-focus);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),A("inside-table",[c("checkbox-box",`
 background-color: var(--n-merged-color-table);
 `)]),A("checked",[c("checkbox-box",`
 background-color: var(--n-color-checked);
 `,[c("checkbox-icon",[S(".check-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),A("indeterminate",[c("checkbox-box",[c("checkbox-icon",[S(".check-icon",`
 opacity: 0;
 transform: scale(.5);
 `),S(".line-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),A("checked, indeterminate",[S("&:focus:not(:active)",[c("checkbox-box",[g("border",`
 border: var(--n-border-checked);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),c("checkbox-box",`
 background-color: var(--n-color-checked);
 border-left: 0;
 border-top: 0;
 `,[g("border",{border:"var(--n-border-checked)"})])]),A("disabled",{cursor:"not-allowed"},[A("checked",[c("checkbox-box",`
 background-color: var(--n-color-disabled-checked);
 `,[g("border",{border:"var(--n-border-disabled-checked)"}),c("checkbox-icon",[S(".check-icon, .line-icon",{fill:"var(--n-check-mark-color-disabled-checked)"})])])]),c("checkbox-box",`
 background-color: var(--n-color-disabled);
 `,[g("border",`
 border: var(--n-border-disabled);
 `),c("checkbox-icon",[S(".check-icon, .line-icon",`
 fill: var(--n-check-mark-color-disabled);
 `)])]),g("label",`
 color: var(--n-text-color-disabled);
 `)]),c("checkbox-box-wrapper",`
 position: relative;
 width: var(--n-size);
 flex-shrink: 0;
 flex-grow: 0;
 user-select: none;
 -webkit-user-select: none;
 `),c("checkbox-box",`
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
 `,[g("border",`
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
 `),c("checkbox-icon",`
 display: flex;
 align-items: center;
 justify-content: center;
 position: absolute;
 left: 1px;
 right: 1px;
 top: 1px;
 bottom: 1px;
 `,[S(".check-icon, .line-icon",`
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
 `),Ye({left:"1px",top:"1px"})])]),g("label",`
 color: var(--n-text-color);
 transition: color .3s var(--n-bezier);
 user-select: none;
 -webkit-user-select: none;
 padding: var(--n-label-padding);
 font-weight: var(--n-label-font-weight);
 `,[S("&:empty",{display:"none"})])]),He(c("checkbox",`
 --n-merged-color-table: var(--n-color-table-modal);
 `)),Ke(c("checkbox",`
 --n-merged-color-table: var(--n-color-table-popover);
 `))]),yn=Object.assign(Object.assign({},$.props),{size:String,checked:{type:[Boolean,String,Number],default:void 0},defaultChecked:{type:[Boolean,String,Number],default:!1},value:[String,Number],disabled:{type:Boolean,default:void 0},indeterminate:Boolean,label:String,focusable:{type:Boolean,default:!0},checkedValue:{type:[Boolean,String,Number],default:!0},uncheckedValue:{type:[Boolean,String,Number],default:!1},"onUpdate:checked":[Function,Array],onUpdateChecked:[Function,Array],privateInsideTable:Boolean,onChange:[Function,Array]}),oe=G({name:"Checkbox",props:yn,setup(e){const n=pe(fn,null),o=E(null),{mergedClsPrefixRef:d,inlineThemeDisabled:a,mergedRtlRef:b}=W(e),z=E(e.defaultChecked),x=we(e,"checked"),f=ze(x,z),v=Ge(()=>{if(n){const h=n.valueSetRef.value;return!(!h||e.value===void 0)&&h.has(e.value)}return f.value===e.checkedValue}),C=We(e,{mergedSize(h){const{size:B}=e;if(B!==void 0)return B;if(n){const{value:R}=n.mergedSizeRef;if(R!==void 0)return R}if(h){const{mergedSize:R}=h;if(R!==void 0)return R.value}return"medium"},mergedDisabled(h){const{disabled:B}=e;if(B!==void 0)return B;if(n){if(n.disabledRef.value)return!0;const{maxRef:{value:R},checkedCountRef:V}=n;if(R!==void 0&&V.value>=R&&!v.value)return!0;const{minRef:{value:M}}=n;if(M!==void 0&&V.value<=M&&v.value)return!0}return!!h&&h.disabled.value}}),{mergedDisabledRef:l,mergedSizeRef:t}=C,r=$("Checkbox","-checkbox",xn,Xe,e,d);function m(h){if(n&&e.value!==void 0)n.toggleCheckbox(!v.value,e.value);else{const{onChange:B,"onUpdate:checked":R,onUpdateChecked:V}=e,{nTriggerFormInput:M,nTriggerFormChange:X}=C,U=v.value?e.uncheckedValue:e.checkedValue;R&&ee(R,U,h),V&&ee(V,U,h),B&&ee(B,U,h),M(),X(),z.value=U}}const k={focus:()=>{var h;(h=o.value)===null||h===void 0||h.focus()},blur:()=>{var h;(h=o.value)===null||h===void 0||h.blur()}},N=Ze("Checkbox",b,d),I=D(()=>{const{value:h}=t,{common:{cubicBezierEaseInOut:B},self:{borderRadius:R,color:V,colorChecked:M,colorDisabled:X,colorTableHeader:U,colorTableHeaderModal:ae,colorTableHeaderPopover:se,checkMarkColor:K,checkMarkColorDisabled:Be,border:Oe,borderFocus:Te,borderDisabled:De,borderChecked:Ee,boxShadowFocus:$e,textColor:Ne,textColorDisabled:Ie,checkMarkColorDisabledChecked:Ve,colorDisabledChecked:je,borderDisabledChecked:Me,labelPadding:Ue,labelLineHeight:qe,labelFontWeight:Le,[H("fontSize",h)]:Qe,[H("size",h)]:Fe}}=r.value;return{"--n-label-line-height":qe,"--n-label-font-weight":Le,"--n-size":Fe,"--n-bezier":B,"--n-border-radius":R,"--n-border":Oe,"--n-border-checked":Ee,"--n-border-focus":Te,"--n-border-disabled":De,"--n-border-disabled-checked":Me,"--n-box-shadow-focus":$e,"--n-color":V,"--n-color-checked":M,"--n-color-table":U,"--n-color-table-modal":ae,"--n-color-table-popover":se,"--n-color-disabled":X,"--n-color-disabled-checked":je,"--n-text-color":Ne,"--n-text-color-disabled":Ie,"--n-check-mark-color":K,"--n-check-mark-color-disabled":Be,"--n-check-mark-color-disabled-checked":Ve,"--n-font-size":Qe,"--n-label-padding":Ue}}),j=a?ne("checkbox",D(()=>t.value[0]),I,e):void 0;return Object.assign(C,k,{rtlEnabled:N,selfRef:o,mergedClsPrefix:d,mergedDisabled:l,renderedChecked:v,mergedTheme:r,labelId:en(),handleClick:function(h){l.value||m(h)},handleKeyUp:function(h){if(!l.value)switch(h.key){case" ":case"Enter":m(h)}},handleKeyDown:function(h){h.key===" "&&h.preventDefault()},cssVars:a?void 0:I,themeClass:j==null?void 0:j.themeClass,onRender:j==null?void 0:j.onRender})},render(){var e;const{$slots:n,renderedChecked:o,mergedDisabled:d,indeterminate:a,privateInsideTable:b,cssVars:z,labelId:x,label:f,mergedClsPrefix:v,focusable:C,handleKeyUp:l,handleKeyDown:t,handleClick:r}=this;(e=this.onRender)===null||e===void 0||e.call(this);const m=ie(n.default,k=>f||k?p("span",{class:`${v}-checkbox__label`,id:x},f||k):null);return p("div",{ref:"selfRef",class:[`${v}-checkbox`,this.themeClass,this.rtlEnabled&&`${v}-checkbox--rtl`,o&&`${v}-checkbox--checked`,d&&`${v}-checkbox--disabled`,a&&`${v}-checkbox--indeterminate`,b&&`${v}-checkbox--inside-table`,m&&`${v}-checkbox--show-label`],tabindex:d||!C?void 0:0,role:"checkbox","aria-checked":a?"mixed":o,"aria-labelledby":x,style:z,onKeyup:l,onKeydown:t,onClick:r,onMousedown:()=>{ke("selectstart",window,k=>{k.preventDefault()},{once:!0})}},p("div",{class:`${v}-checkbox-box-wrapper`}," ",p("div",{class:`${v}-checkbox-box`},p(Je,null,{default:()=>this.indeterminate?p("div",{key:"indeterminate",class:`${v}-checkbox-icon`},p("svg",{viewBox:"0 0 100 100",class:"line-icon"},p("path",{d:"M80.2,55.5H21.4c-2.8,0-5.1-2.5-5.1-5.5l0,0c0-3,2.3-5.5,5.1-5.5h58.7c2.8,0,5.1,2.5,5.1,5.5l0,0C85.2,53.1,82.9,55.5,80.2,55.5z"}))):p("div",{key:"check",class:`${v}-checkbox-icon`},p("svg",{viewBox:"0 0 64 64",class:"check-icon"},p("path",{d:"M50.42,16.76L22.34,39.45l-8.1-11.46c-1.12-1.58-3.3-1.96-4.88-0.84c-1.58,1.12-1.95,3.3-0.84,4.88l10.26,14.51  c0.56,0.79,1.42,1.31,2.38,1.45c0.16,0.02,0.32,0.03,0.48,0.03c0.8,0,1.57-0.27,2.2-0.78l30.99-25.03c1.5-1.21,1.74-3.42,0.52-4.92  C54.13,15.78,51.93,15.55,50.42,16.76z"})))}),p("div",{class:`${v}-checkbox-box__border`}))),m)}});Object.assign(Object.assign({},$.props),{left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"}});const kn=le("n-float-button-group"),wn=c("float-button",`
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
`,[A("circle-shape",`
 border-radius: 4096px;
 `),A("square-shape",`
 border-radius: var(--n-border-radius-square);
 `),g("fill",`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0
 left: 0;
 transition: background-color .3s var(--n-bezier);
 border-radius: inherit;
 `),g("body",`
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
 `,[g("description",`
 font-size: 12px;
 text-align: center;
 line-height: 14px;
 `)]),S("&:hover","box-shadow: var(--n-box-shadow-hover);",[S(">",[g("fill",`
 background-color: var(--n-color-hover);
 `)])]),S("&:active","box-shadow: var(--n-box-shadow-pressed);",[S(">",[g("fill",`
 background-color: var(--n-color-pressed);
 `)])]),A("show-menu",[S(">",[g("menu",`
 pointer-events: all;
 bottom: 100%;
 opacity: 1;
 `),g("close",`
 transform: scale(1);
 opacity: 1;
 `),g("body",`
 transform: scale(0.75);
 opacity: 0;
 `)])]),g("close",`
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
 `),g("menu",`
 position: absolute;
 bottom: calc(100% - 8px);
 display: flex;
 flex-direction: column;
 opacity: 0;
 pointer-events: none;
 transition:
 opacity .3s var(--n-bezier),
 bottom .3s var(--n-bezier); 
 `,[S("> *",`
 margin-bottom: 16px;
 `),c("float-button",`
 position: relative !important;
 `)])]),zn=Object.assign(Object.assign({},$.props),{width:{type:[Number,String],default:40},height:{type:[Number,String],default:40},left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"},type:{type:String,default:"default"},menuTrigger:String,showMenu:{type:Boolean,default:void 0},onUpdateShowMenu:{type:[Function,Array],default:void 0},"onUpdate:showMenu":{type:[Function,Array],default:void 0}}),ue=G({name:"FloatButton",props:zn,slots:Object,setup(e){const{mergedClsPrefixRef:n,inlineThemeDisabled:o}=W(e),d=E(null),a=$("FloatButton","-float-button",wn,on,e,n),b=pe(kn,null),z=E(!1),x=we(e,"showMenu"),f=ze(x,z);function v(k){const{onUpdateShowMenu:N,"onUpdate:showMenu":I}=e;z.value=k,N&&ee(N,k),I&&ee(I,k)}const C=D(()=>{const{self:{color:k,textColor:N,boxShadow:I,boxShadowHover:j,boxShadowPressed:h,colorHover:B,colorPrimary:R,colorPrimaryHover:V,textColorPrimary:M,borderRadiusSquare:X,colorPressed:U,colorPrimaryPressed:ae},common:{cubicBezierEaseInOut:se}}=a.value,{type:K}=e;return{"--n-bezier":se,"--n-box-shadow":I,"--n-box-shadow-hover":j,"--n-box-shadow-pressed":h,"--n-color":K==="primary"?R:k,"--n-text-color":K==="primary"?M:N,"--n-color-hover":K==="primary"?V:B,"--n-color-pressed":K==="primary"?ae:U,"--n-border-radius-square":X}}),l=D(()=>{const{width:k,height:N}=e;return Object.assign({position:b?void 0:e.position,width:q(k),minHeight:q(N)},b?null:{left:q(e.left),right:q(e.right),top:q(e.top),bottom:q(e.bottom)})}),t=D(()=>b?b.shapeRef.value:e.shape),r=()=>{e.menuTrigger==="hover"&&f.value&&v(!1)},m=o?ne("float-button",D(()=>e.type[0]),C,e):void 0;return ve(()=>{const k=d.value;k&&ke("mousemoveoutside",k,r)}),rn(()=>{const k=d.value;k&&ln("mousemoveoutside",k,r)}),{inlineStyle:l,selfElRef:d,cssVars:o?void 0:C,mergedClsPrefix:n,mergedShape:t,mergedShowMenu:f,themeClass:m==null?void 0:m.themeClass,onRender:m==null?void 0:m.onRender,Mouseenter:()=>{e.menuTrigger==="hover"&&v(!0)},handleMouseleave:r,handleClick:()=>{e.menuTrigger==="click"&&v(!f.value)}}},render(){var e;const{mergedClsPrefix:n,cssVars:o,mergedShape:d,type:a,menuTrigger:b,mergedShowMenu:z,themeClass:x,$slots:f,inlineStyle:v,onRender:C}=this;return C==null||C(),p("div",{ref:"selfElRef",class:[`${n}-float-button`,`${n}-float-button--${d}-shape`,`${n}-float-button--${a}-type`,z&&`${n}-float-button--show-menu`,x],style:[o,v],onMouseenter:this.Mouseenter,onMouseleave:this.handleMouseleave,onClick:this.handleClick,role:"button"},p("div",{class:`${n}-float-button__fill`,"aria-hidden":!0}),p("div",{class:`${n}-float-button__body`},(e=f.default)===null||e===void 0?void 0:e.call(f),ie(f.description,l=>l?p("div",{class:`${n}-float-button__description`},l):null)),b?p("div",{class:`${n}-float-button__close`},p(nn,{clsPrefix:n},{default:()=>p(tn,null)})):null,b?p("div",{onClick:l=>{l.stopPropagation()},"data-float-button-menu":!0,class:`${n}-float-button__menu`},me(f.menu,()=>[])):null)}}),Ae={type:String,default:"static"},Sn=c("layout",`
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
`,[c("layout-scroll-container",`
 overflow-x: hidden;
 box-sizing: border-box;
 height: 100%;
 `),A("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),Cn={embedded:Boolean,position:Ae,nativeScrollbar:{type:Boolean,default:!0},scrollbarProps:Object,onScroll:Function,contentClass:String,contentStyle:{type:[String,Object],default:""},hasSider:Boolean,siderPlacement:{type:String,default:"left"}},_n=le("n-layout");function Pe(e){return G({name:e?"LayoutContent":"Layout",props:Object.assign(Object.assign({},$.props),Cn),setup(n){const o=E(null),d=E(null),{mergedClsPrefixRef:a,inlineThemeDisabled:b}=W(n),z=$("Layout","-layout",Sn,Se,n,a);Ce(_n,n);let x=0,f=0;sn(()=>{if(n.nativeScrollbar){const t=o.value;t&&(t.scrollTop=f,t.scrollLeft=x)}});const v={scrollTo:function(t,r){if(n.nativeScrollbar){const{value:m}=o;m&&(r===void 0?m.scrollTo(t):m.scrollTo(t,r))}else{const{value:m}=d;m&&m.scrollTo(t,r)}}},C=D(()=>{const{common:{cubicBezierEaseInOut:t},self:r}=z.value;return{"--n-bezier":t,"--n-color":n.embedded?r.colorEmbedded:r.color,"--n-text-color":r.textColor}}),l=b?ne("layout",D(()=>n.embedded?"e":""),C,n):void 0;return Object.assign({mergedClsPrefix:a,scrollableElRef:o,scrollbarInstRef:d,hasSiderStyle:{display:"flex",flexWrap:"nowrap",width:"100%",flexDirection:"row"},mergedTheme:z,handleNativeElScroll:t=>{var r;const m=t.target;x=m.scrollLeft,f=m.scrollTop,(r=n.onScroll)===null||r===void 0||r.call(n,t)},cssVars:b?void 0:C,themeClass:l==null?void 0:l.themeClass,onRender:l==null?void 0:l.onRender},v)},render(){var n;const{mergedClsPrefix:o,hasSider:d}=this;(n=this.onRender)===null||n===void 0||n.call(this);const a=d?this.hasSiderStyle:void 0,b=[this.themeClass,e&&`${o}-layout-content`,`${o}-layout`,`${o}-layout--${this.position}-positioned`];return p("div",{class:b,style:this.cssVars},this.nativeScrollbar?p("div",{ref:"scrollableElRef",class:[`${o}-layout-scroll-container`,this.contentClass],style:[this.contentStyle,a],onScroll:this.handleNativeElScroll},this.$slots):p(an,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:this.contentClass,contentStyle:[this.contentStyle,a]}),this.$slots))}})}const An=Pe(!1),Pn=Pe(!0),Rn=c("layout-header",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 box-sizing: border-box;
 width: 100%;
 background-color: var(--n-color);
 color: var(--n-text-color);
`,[A("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 `),A("bordered",`
 border-bottom: solid 1px var(--n-border-color);
 `)]),Bn={position:Ae,inverted:Boolean,bordered:{type:Boolean,default:!1}},On=G({name:"LayoutHeader",props:Object.assign(Object.assign({},$.props),Bn),setup(e){const{mergedClsPrefixRef:n,inlineThemeDisabled:o}=W(e),d=$("Layout","-layout-header",Rn,Se,e,n),a=D(()=>{const{common:{cubicBezierEaseInOut:z},self:x}=d.value,f={"--n-bezier":z};return e.inverted?(f["--n-color"]=x.headerColorInverted,f["--n-text-color"]=x.textColorInverted,f["--n-border-color"]=x.headerBorderColorInverted):(f["--n-color"]=x.headerColor,f["--n-text-color"]=x.textColor,f["--n-border-color"]=x.headerBorderColor),f}),b=o?ne("layout-header",D(()=>e.inverted?"a":"b"),a,e):void 0;return{mergedClsPrefix:n,cssVars:o?void 0:a,themeClass:b==null?void 0:b.themeClass,onRender:b==null?void 0:b.onRender}},render(){var e;const{mergedClsPrefix:n}=this;return(e=this.onRender)===null||e===void 0||e.call(this),p("div",{class:[`${n}-layout-header`,this.themeClass,this.position&&`${n}-layout-header--${this.position}-positioned`,this.bordered&&`${n}-layout-header--bordered`],style:this.cssVars},this.$slots)}}),Tn=c("timeline",`
 position: relative;
 width: 100%;
 display: flex;
 flex-direction: column;
 line-height: 1.25;
`,[A("horizontal",`
 flex-direction: row;
 `,[S(">",[c("timeline-item",`
 flex-shrink: 0;
 padding-right: 40px;
 `,[A("dashed-line-type",[S(">",[c("timeline-item-timeline",[g("line",`
 background-image: linear-gradient(90deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 10px 1px;
 `)])])]),S(">",[c("timeline-item-content",`
 margin-top: calc(var(--n-icon-size) + 12px);
 `,[S(">",[g("meta",`
 margin-top: 6px;
 margin-bottom: unset;
 `)])]),c("timeline-item-timeline",`
 width: 100%;
 height: calc(var(--n-icon-size) + 12px);
 `,[g("line",`
 left: var(--n-icon-size);
 top: calc(var(--n-icon-size) / 2 - 1px);
 right: 0px;
 width: unset;
 height: 2px;
 `)])])])])]),A("right-placement",[c("timeline-item",[c("timeline-item-content",`
 text-align: right;
 margin-right: calc(var(--n-icon-size) + 12px);
 `),c("timeline-item-timeline",`
 width: var(--n-icon-size);
 right: 0;
 `)])]),A("left-placement",[c("timeline-item",[c("timeline-item-content",`
 margin-left: calc(var(--n-icon-size) + 12px);
 `),c("timeline-item-timeline",`
 left: 0;
 `)])]),c("timeline-item",`
 position: relative;
 `,[S("&:last-child",[c("timeline-item-timeline",[g("line",`
 display: none;
 `)]),c("timeline-item-content",[g("meta",`
 margin-bottom: 0;
 `)])]),c("timeline-item-content",[g("title",`
 margin: var(--n-title-margin);
 font-size: var(--n-title-font-size);
 transition: color .3s var(--n-bezier);
 font-weight: var(--n-title-font-weight);
 color: var(--n-title-text-color);
 `),g("content",`
 transition: color .3s var(--n-bezier);
 font-size: var(--n-content-font-size);
 color: var(--n-content-text-color);
 `),g("meta",`
 transition: color .3s var(--n-bezier);
 font-size: 12px;
 margin-top: 6px;
 margin-bottom: 20px;
 color: var(--n-meta-text-color);
 `)]),A("dashed-line-type",[c("timeline-item-timeline",[g("line",`
 --n-color-start: var(--n-line-color);
 transition: --n-color-start .3s var(--n-bezier);
 background-color: transparent;
 background-image: linear-gradient(180deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 1px 10px;
 `)])]),c("timeline-item-timeline",`
 width: calc(var(--n-icon-size) + 12px);
 position: absolute;
 top: calc(var(--n-title-font-size) * 1.25 / 2 - var(--n-icon-size) / 2);
 height: 100%;
 `,[g("circle",`
 border: var(--n-circle-border);
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 border-radius: var(--n-icon-size);
 box-sizing: border-box;
 `),g("icon",`
 color: var(--n-icon-color);
 font-size: var(--n-icon-size);
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 display: flex;
 align-items: center;
 justify-content: center;
 `),g("line",`
 transition: background-color .3s var(--n-bezier);
 position: absolute;
 top: var(--n-icon-size);
 left: calc(var(--n-icon-size) / 2 - 1px);
 bottom: 0px;
 width: 2px;
 background-color: var(--n-line-color);
 `)])])]),Dn=Object.assign(Object.assign({},$.props),{horizontal:Boolean,itemPlacement:{type:String,default:"left"},size:{type:String,default:"medium"},iconSize:Number}),Re=le("n-timeline"),be=G({name:"Timeline",props:Dn,setup(e,{slots:n}){const{mergedClsPrefixRef:o}=W(e),d=$("Timeline","-timeline",Tn,cn,e,o);return Ce(Re,{props:e,mergedThemeRef:d,mergedClsPrefixRef:o}),()=>{const{value:a}=o;return p("div",{class:[`${a}-timeline`,e.horizontal&&`${a}-timeline--horizontal`,`${a}-timeline--${e.size}-size`,!e.horizontal&&`${a}-timeline--${e.itemPlacement}-placement`]},n)}}}),he=G({name:"TimelineItem",props:{time:[String,Number],title:String,content:String,color:String,lineType:{type:String,default:"default"},type:{type:String,default:"default"}},slots:Object,setup(e){const n=pe(Re);n||dn("timeline-item","`n-timeline-item` must be placed inside `n-timeline`."),gn();const{inlineThemeDisabled:o}=W(),d=D(()=>{const{props:{size:b,iconSize:z},mergedThemeRef:x}=n,{type:f}=e,{self:{titleTextColor:v,contentTextColor:C,metaTextColor:l,lineColor:t,titleFontWeight:r,contentFontSize:m,[H("iconSize",b)]:k,[H("titleMargin",b)]:N,[H("titleFontSize",b)]:I,[H("circleBorder",f)]:j,[H("iconColor",f)]:h},common:{cubicBezierEaseInOut:B}}=x.value;return{"--n-bezier":B,"--n-circle-border":j,"--n-icon-color":h,"--n-content-font-size":m,"--n-content-text-color":C,"--n-line-color":t,"--n-meta-text-color":l,"--n-title-font-size":I,"--n-title-font-weight":r,"--n-title-margin":N,"--n-title-text-color":v,"--n-icon-size":q(z)||k}}),a=o?ne("timeline-item",D(()=>{const{props:{size:b,iconSize:z}}=n,{type:x}=e;return`${b[0]}${z||"a"}${x[0]}`}),d,n.props):void 0;return{mergedClsPrefix:n.mergedClsPrefixRef,cssVars:o?void 0:d,themeClass:a==null?void 0:a.themeClass,onRender:a==null?void 0:a.onRender}},render(){const{mergedClsPrefix:e,color:n,onRender:o,$slots:d}=this;return o==null||o(),p("div",{class:[`${e}-timeline-item`,this.themeClass,`${e}-timeline-item--${this.type}-type`,`${e}-timeline-item--${this.lineType}-line-type`],style:this.cssVars},p("div",{class:`${e}-timeline-item-timeline`},p("div",{class:`${e}-timeline-item-timeline__line`}),ie(d.icon,a=>a?p("div",{class:`${e}-timeline-item-timeline__icon`,style:{color:n}},a):p("div",{class:`${e}-timeline-item-timeline__circle`,style:{borderColor:n}}))),p("div",{class:`${e}-timeline-item-content`},ie(d.header,a=>a||this.title?p("div",{class:`${e}-timeline-item-content__title`},a||this.title):null),p("div",{class:`${e}-timeline-item-content__content`},me(d.default,()=>[this.content])),p("div",{class:`${e}-timeline-item-content__meta`},me(d.footer,()=>[this.time]))))}}),En={id:"ai-container",style:{"max-width":"800px",border:"1px solid #5c5c5c","border-radius":"20px",padding:"10px",margin:"5px"}},$n=["innerHTML"],Nn=ge({__name:"ai",setup(e){const n=E("");return ve(()=>{try{const o=new EventSource(un+"/ai_summary");o.onmessage=d=>{n.value+=d.data},o.addEventListener("end",()=>{o.close()}),o.onerror=d=>{o.close()},window.eventSource=o}catch(o){J(o.message,{theme:"auto",type:"error"}),n.value+=`<p style="color: red;">${o.message}</p>`}}),bn(()=>{var o;(o=window.eventSource)==null||o.close(),window.eventSource=void 0}),(o,d)=>(y(),P("div",En,[d[0]||(d[0]=i("p",{style:{margin:"5px",color:"#18a058",display:"flex","align-items":"center"}},[i("i",{id:"ai-icon"}),_(" AI 摘要 ")],-1)),i("div",{innerHTML:n.value},null,8,$n)]))}},[["__scopeId","data-v-695eaa09"]]),re=e=>e.includes("QQ")?"/assets/qq.png":e.includes("Chrome")?"data:image/png;base64,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":e.includes("哔哩哔哩")?"/assets/bilibili.jpg":"",In={key:0,title:"",style:{"min-width":"700px",overflow:"auto"}},Vn={style:{margin:"0"}},jn={id:"icarea",style:{display:"flex","justify-content":"flex-start","align-items":"center"}},Mn=["src"],Un=["src"],qn=ge({__name:"show_activity_window",setup(e){const n=E();return _e(()=>{hn().then(o=>{typeof o!="string"?n.value=o:J(o,{theme:"auto",type:"error"})}).catch(o=>{J(o,{theme:"auto",type:"error"})})}),(o,d)=>{var a;return(a=n.value)!=null&&a.activity_window?(y(),P("div",In,[i("p",Vn,"活动程序 "+O(s(L)(n.value.report_time)),1),i("div",jn,[i("img",{src:s("/assets/win.png"),class:"ic",style:{padding:"0px 5px","margin-top":"-8px"}},null,8,Mn),(y(!0),P(Q,null,F(n.value.activity_window,(b,z)=>(y(),P("div",{key:z,class:"icitem"},[w(s(Y),{trigger:"hover",placement:"top"},{trigger:u(()=>[i("img",{src:"/exe_icon/"+b.exe_name+".png",class:"ic"},null,8,Un)]),default:u(()=>[_(" "+O(b.title),1)]),_:2},1024)]))),128))])])):Z("",!0)}}},[["__scopeId","data-v-137d535c"]]),Ln={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/releases"},Qn={style:{display:"flex","align-items":"center"}},Fn=["src"],Hn={key:1},Kn=["src"],Yn={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/自动汇报.js"},Jn=["href"],Gn={key:1},Wn=["src"],Xn={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/%E8%87%AA%E5%8A%A8%E6%B1%87%E6%8A%A5.macro"},Zn={style:{display:"flex","align-items":"center"}},et=["src"],nt={key:1},tt=["src"],ot=ge({__name:"pcstatus",setup(e){const n=E(!1),o=fe([!0,!0,!0]);ve(()=>{const l=localStorage.getItem("showtimeline");n.value=l?JSON.parse(l):window.innerWidth<=900;const t=localStorage.getItem("showwhat");if(t){const r=JSON.parse(t);o[0]=r[0],o[1]=r[1],o[2]=r[2]}else o.fill(!0)}),xe(n,l=>{localStorage.setItem("showtimeline",JSON.stringify(l))}),xe(o,l=>{localStorage.setItem("showwhat",JSON.stringify(l))});const d=fe({info:""}),a=E(),b=E({browser:0,pc:0,phone:0});function z(){a.value=void 0,mn().then(l=>{typeof l!="string"?b.value=l:J(l,{theme:"auto",type:"error"})}).catch(l=>{J(l,{theme:"auto",type:"error"})}),pn().then(l=>{typeof l!="string"?a.value=l:d.info=l}).catch(l=>{J(l,{theme:"auto",type:"error"})})}function x(l,t){return l.length>t?l.substring(0,t)+"...":l}function f(l){const t=new Date(1e3*l);return`${t.getFullYear()}-${String(t.getMonth()+1).padStart(2,"0")}-${String(t.getDate()).padStart(2,"0")} ${String(t.getHours()).padStart(2,"0")}:${String(t.getMinutes()).padStart(2,"0")}:${String(t.getSeconds()).padStart(2,"0")}`}function v(l){return l.slice().reverse()}function C(l){l.target.src="/assets/desktop.png"}return _e(()=>{z()}),(l,t)=>(y(),T(s(An),null,{default:u(()=>[w(s(On),null,{default:u(()=>[w(s(te),{title:"你在干什么?",style:{"margin-bottom":"10px"}},{default:u(()=>[w(Nn),w(s(de),null,{default:u(()=>[i("span",null,[t[4]||(t[4]=_("时间线表示 ")),w(s(oe),{checked:n.value,"onUpdate:checked":t[0]||(t[0]=r=>n.value=r)},null,8,["checked"])]),i("span",null,[t[5]||(t[5]=_("显示电脑 ")),w(s(oe),{checked:o[0],"onUpdate:checked":t[1]||(t[1]=r=>o[0]=r)},null,8,["checked"])]),i("span",null,[t[6]||(t[6]=_("显示浏览器 ")),w(s(oe),{checked:o[1],"onUpdate:checked":t[2]||(t[2]=r=>o[1]=r)},null,8,["checked"])]),i("span",null,[t[7]||(t[7]=_("显示手机 ")),w(s(oe),{checked:o[2],"onUpdate:checked":t[3]||(t[3]=r=>o[2]=r)},null,8,["checked"])])]),_:1}),w(s(vn),{onClick:z,text:"",style:{margin:"10px 0",float:"right","font-size":"20px"},title:"刷新"},{default:u(()=>t[8]||(t[8]=[_("↻")])),_:1})]),_:1})]),_:1}),w(s(Pn),null,{default:u(()=>[w(s(de),{vertical:""},{default:u(()=>[a.value?(y(),T(s(de),{key:0,vertical:""},{default:u(()=>[o[0]?(y(),T(s(te),{key:0,title:"电脑(最新"+b.value.pc+"项)"},{"header-extra":u(()=>[w(s(Y),{trigger:"hover",placement:"right"},{trigger:u(()=>[i("a",Ln,[w(s(ue),{position:"relative"},{default:u(()=>t[9]||(t[9]=[_("?")])),_:1})])]),default:u(()=>[t[10]||(t[10]=_(" 电脑端自动报告程序,点击前往 "))]),_:1})]),default:u(()=>[w(qn),n.value?(y(),P("div",Hn,[w(s(be),null,{default:u(()=>[(y(!0),P(Q,null,F(a.value.pc,(r,m)=>(y(),T(s(he),{key:m,type:"success",title:r.exe_name,content:r.running_exe,time:s(L)(r.report_time)},ye({_:2},[r.exe_name?{name:"icon",fn:u(()=>[i("img",{src:"/exe_icon/"+r.exe_name+".png",alt:"",onError:C,style:{width:"20px","z-index":"2"}},null,40,Kn)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(y(),T(s(ce),{key:0,bordered:!1},{default:u(()=>[t[11]||(t[11]=i("thead",null,[i("tr",null,[i("th",null,"可执行程序"),i("th",null,"前台窗口标题"),i("th",null,"时间")])],-1)),i("tbody",null,[(y(!0),P(Q,null,F(v(a.value.pc),(r,m)=>(y(),P("tr",{key:m},[i("td",null,[i("div",Qn,[i("img",{size:"small",src:"/exe_icon/"+r.exe_name+".png",onError:C,style:{margin:"0 5px",width:"20px"}},null,40,Fn),_(" "+O(r.exe_name),1)])]),i("td",null,[w(s(Y),{"show-arrow":!1,trigger:"hover"},{trigger:u(()=>{return[_(O(x((k=r.running_exe,k.includes("Google Chrome")?"Google Chrome":k),30)),1)];var k}),default:u(()=>[_(" "+O(r.running_exe),1)]),_:2},1024)]),i("td",null,O(s(L)(r.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0),o[1]?(y(),T(s(te),{key:1,title:"电脑浏览器(最新"+b.value.browser+"项)"},{"header-extra":u(()=>[w(s(Y),{trigger:"hover",placement:"right"},{trigger:u(()=>[i("a",Yn,[w(s(ue),{position:"relative"},{default:u(()=>t[12]||(t[12]=[_("?")])),_:1})])]),default:u(()=>[t[13]||(t[13]=_(" 浏览器油猴脚本,点击前往 "))]),_:1})]),default:u(()=>[n.value?(y(),P("div",Gn,[w(s(be),null,{default:u(()=>[(y(!0),P(Q,null,F(a.value.browser,(r,m)=>(y(),T(s(he),{key:m,type:"success",title:x(r.title,70),content:x(r.url,70),time:s(L)(r.report_time)},{icon:u(()=>[i("img",{src:s(re)("Chrome"),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,Wn)]),_:2},1032,["title","content","time"]))),128))]),_:1})])):(y(),T(s(ce),{key:0,bordered:!1},{default:u(()=>[t[14]||(t[14]=i("thead",null,[i("tr",null,[i("th",null,"网页标题"),i("th",null,"网页链接"),i("th",null,"时间")])],-1)),i("tbody",null,[(y(!0),P(Q,null,F(v(a.value.browser),(r,m)=>(y(),P("tr",{key:m},[i("td",null,[w(s(Y),{trigger:"hover"},{trigger:u(()=>[_(O(x(r.title,30)),1)]),default:u(()=>[_(" "+O(r.title),1)]),_:2},1024)]),i("td",null,[i("a",{target:"_blank",href:r.url,class:"nowrap-ellipsis"},O(x(r.url,30)),9,Jn)]),i("td",null,O(s(L)(r.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0),o[2]?(y(),T(s(te),{key:2,title:"手机(最新"+b.value.phone+"项)"},{"header-extra":u(()=>[w(s(Y),{trigger:"hover",placement:"right"},{trigger:u(()=>[i("a",Xn,[w(s(ue),{position:"relative"},{default:u(()=>t[15]||(t[15]=[_("?")])),_:1})])]),default:u(()=>[t[16]||(t[16]=_(" 点击前往, 下载文件导入安卓MacroDroid软件 "))]),_:1})]),default:u(()=>[n.value?(y(),P("div",nt,[w(s(be),null,{default:u(()=>[(y(!0),P(Q,null,F(a.value.phone,(r,m)=>(y(),T(s(he),{key:m,type:"success",title:r.app,content:r.battery_level+"  / wifi信号:  "+r.wifi_ssid,time:s(L)(f(r.report_time))},ye({_:2},[s(re)(r.app)?{name:"icon",fn:u(()=>[i("img",{src:s(re)(r.app),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,tt)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(y(),T(s(ce),{key:0,bordered:!1},{default:u(()=>[t[17]||(t[17]=i("thead",null,[i("tr",null,[i("th",null,"前台应用"),i("th",null,"电池"),i("th",null,"wifi"),i("th",null,"时间")])],-1)),i("tbody",null,[(y(!0),P(Q,null,F(v(a.value.phone),(r,m)=>(y(),P("tr",{key:m},[i("td",null,[i("div",Zn,[i("img",{size:"small",src:s(re)(r.app),style:{margin:"0 5px",width:"20px"}},null,8,et),_(" "+O(r.app),1)])]),i("td",null,O(r.battery_level),1),i("td",null,O(r.wifi_ssid),1),i("td",null,O(s(L)(f(r.report_time))),1)]))),128))])]),_:1}))]),_:1},8,["title"])):Z("",!0)]),_:1})):Z("",!0)]),_:1})]),_:1})]),_:1}))}},[["__scopeId","data-v-b9452990"]]),ct={__name:"doing",setup:e=>(n,o)=>(y(),T(ot))};export{ct as default};
