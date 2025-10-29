import{L as oe,R as l,Q as d,M as r,ax as ne,ay as re,O as b,P as s,c9 as ae,d as ce,V as le,ca as de,a2 as ie,r as T,W as se,Y as te,Z as be,aN as he,a0 as ue,b8 as ke,K as F,cb as ve,av as fe,p as V,ac as K,a1 as xe,aM as pe,a5 as B}from"./index-uHSdsz2C.js";const ge=oe("n-checkbox-group"),me=d([r("checkbox",`
 font-size: var(--n-font-size);
 outline: none;
 cursor: pointer;
 display: inline-flex;
 flex-wrap: nowrap;
 align-items: flex-start;
 word-break: break-word;
 line-height: var(--n-size);
 --n-merged-color-table: var(--n-color-table);
 `,[b("show-label","line-height: var(--n-label-line-height);"),d("&:hover",[r("checkbox-box",[s("border","border: var(--n-border-checked);")])]),d("&:focus:not(:active)",[r("checkbox-box",[s("border",`
 border: var(--n-border-focus);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),b("inside-table",[r("checkbox-box",`
 background-color: var(--n-merged-color-table);
 `)]),b("checked",[r("checkbox-box",`
 background-color: var(--n-color-checked);
 `,[r("checkbox-icon",[d(".check-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),b("indeterminate",[r("checkbox-box",[r("checkbox-icon",[d(".check-icon",`
 opacity: 0;
 transform: scale(.5);
 `),d(".line-icon",`
 opacity: 1;
 transform: scale(1);
 `)])])]),b("checked, indeterminate",[d("&:focus:not(:active)",[r("checkbox-box",[s("border",`
 border: var(--n-border-checked);
 box-shadow: var(--n-box-shadow-focus);
 `)])]),r("checkbox-box",`
 background-color: var(--n-color-checked);
 border-left: 0;
 border-top: 0;
 `,[s("border",{border:"var(--n-border-checked)"})])]),b("disabled",{cursor:"not-allowed"},[b("checked",[r("checkbox-box",`
 background-color: var(--n-color-disabled-checked);
 `,[s("border",{border:"var(--n-border-disabled-checked)"}),r("checkbox-icon",[d(".check-icon, .line-icon",{fill:"var(--n-check-mark-color-disabled-checked)"})])])]),r("checkbox-box",`
 background-color: var(--n-color-disabled);
 `,[s("border",`
 border: var(--n-border-disabled);
 `),r("checkbox-icon",[d(".check-icon, .line-icon",`
 fill: var(--n-check-mark-color-disabled);
 `)])]),s("label",`
 color: var(--n-text-color-disabled);
 `)]),r("checkbox-box-wrapper",`
 position: relative;
 width: var(--n-size);
 flex-shrink: 0;
 flex-grow: 0;
 user-select: none;
 -webkit-user-select: none;
 `),r("checkbox-box",`
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
 `,[s("border",`
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
 `),r("checkbox-icon",`
 display: flex;
 align-items: center;
 justify-content: center;
 position: absolute;
 left: 1px;
 right: 1px;
 top: 1px;
 bottom: 1px;
 `,[d(".check-icon, .line-icon",`
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
 `),ae({left:"1px",top:"1px"})])]),s("label",`
 color: var(--n-text-color);
 transition: color .3s var(--n-bezier);
 user-select: none;
 -webkit-user-select: none;
 padding: var(--n-label-padding);
 font-weight: var(--n-label-font-weight);
 `,[d("&:empty",{display:"none"})])]),ne(r("checkbox",`
 --n-merged-color-table: var(--n-color-table-modal);
 `)),re(r("checkbox",`
 --n-merged-color-table: var(--n-color-table-popover);
 `))]),we=ce({name:"Checkbox",props:Object.assign(Object.assign({},F.props),{size:String,checked:{type:[Boolean,String,Number],default:void 0},defaultChecked:{type:[Boolean,String,Number],default:!1},value:[String,Number],disabled:{type:Boolean,default:void 0},indeterminate:Boolean,label:String,focusable:{type:Boolean,default:!0},checkedValue:{type:[Boolean,String,Number],default:!0},uncheckedValue:{type:[Boolean,String,Number],default:!1},"onUpdate:checked":[Function,Array],onUpdateChecked:[Function,Array],privateInsideTable:Boolean,onChange:[Function,Array]}),setup(o){const c=ue(ge,null),h=T(null),{mergedClsPrefixRef:u,inlineThemeDisabled:x,mergedRtlRef:S}=se(o),C=T(o.defaultChecked),w=te(o,"checked"),y=be(w,C),n=he(()=>{if(c){const e=c.valueSetRef.value;return!(!e||o.value===void 0)&&e.has(o.value)}return y.value===o.checkedValue}),p=ke(o,{mergedSize(e){const{size:i}=o;if(i!==void 0)return i;if(c){const{value:a}=c.mergedSizeRef;if(a!==void 0)return a}if(e){const{mergedSize:a}=e;if(a!==void 0)return a.value}return"medium"},mergedDisabled(e){const{disabled:i}=o;if(i!==void 0)return i;if(c){if(c.disabledRef.value)return!0;const{maxRef:{value:a},checkedCountRef:t}=c;if(a!==void 0&&t.value>=a&&!n.value)return!0;const{minRef:{value:v}}=c;if(v!==void 0&&t.value<=v&&n.value)return!0}return!!e&&e.disabled.value}}),{mergedDisabledRef:g,mergedSizeRef:z}=p,R=F("Checkbox","-checkbox",me,ve,o,u);function m(e){if(c&&o.value!==void 0)c.toggleCheckbox(!n.value,o.value);else{const{onChange:i,"onUpdate:checked":a,onUpdateChecked:t}=o,{nTriggerFormInput:v,nTriggerFormChange:$}=p,f=n.value?o.uncheckedValue:o.checkedValue;a&&B(a,f,e),t&&B(t,f,e),i&&B(i,f,e),v(),$(),C.value=f}}const k={focus:()=>{var e;(e=h.value)===null||e===void 0||e.focus()},blur:()=>{var e;(e=h.value)===null||e===void 0||e.blur()}},N=fe("Checkbox",S,u),M=V(()=>{const{value:e}=z,{common:{cubicBezierEaseInOut:i},self:{borderRadius:a,color:t,colorChecked:v,colorDisabled:$,colorTableHeader:f,colorTableHeaderModal:I,colorTableHeaderPopover:P,checkMarkColor:U,checkMarkColorDisabled:H,border:O,borderFocus:j,borderDisabled:E,borderChecked:_,boxShadowFocus:A,textColor:L,textColorDisabled:W,checkMarkColorDisabledChecked:Y,colorDisabledChecked:Q,borderDisabledChecked:Z,labelPadding:q,labelLineHeight:G,labelFontWeight:J,[K("fontSize",e)]:X,[K("size",e)]:ee}}=R.value;return{"--n-label-line-height":G,"--n-label-font-weight":J,"--n-size":ee,"--n-bezier":i,"--n-border-radius":a,"--n-border":O,"--n-border-checked":_,"--n-border-focus":j,"--n-border-disabled":E,"--n-border-disabled-checked":Z,"--n-box-shadow-focus":A,"--n-color":t,"--n-color-checked":v,"--n-color-table":f,"--n-color-table-modal":I,"--n-color-table-popover":P,"--n-color-disabled":$,"--n-color-disabled-checked":Q,"--n-text-color":L,"--n-text-color-disabled":W,"--n-check-mark-color":U,"--n-check-mark-color-disabled":H,"--n-check-mark-color-disabled-checked":Y,"--n-font-size":X,"--n-label-padding":q}}),D=x?xe("checkbox",V(()=>z.value[0]),M,o):void 0;return Object.assign(p,k,{rtlEnabled:N,selfRef:h,mergedClsPrefix:u,mergedDisabled:g,renderedChecked:n,mergedTheme:R,labelId:pe(),handleClick:function(e){g.value||m(e)},handleKeyUp:function(e){if(!g.value)switch(e.key){case" ":case"Enter":m(e)}},handleKeyDown:function(e){e.key===" "&&e.preventDefault()},cssVars:x?void 0:M,themeClass:D==null?void 0:D.themeClass,onRender:D==null?void 0:D.onRender})},render(){var o;const{$slots:c,renderedChecked:h,mergedDisabled:u,indeterminate:x,privateInsideTable:S,cssVars:C,labelId:w,label:y,mergedClsPrefix:n,focusable:p,handleKeyUp:g,handleKeyDown:z,handleClick:R}=this;(o=this.onRender)===null||o===void 0||o.call(this);const m=le(c.default,k=>y||k?l("span",{class:`${n}-checkbox__label`,id:w},y||k):null);return l("div",{ref:"selfRef",class:[`${n}-checkbox`,this.themeClass,this.rtlEnabled&&`${n}-checkbox--rtl`,h&&`${n}-checkbox--checked`,u&&`${n}-checkbox--disabled`,x&&`${n}-checkbox--indeterminate`,S&&`${n}-checkbox--inside-table`,m&&`${n}-checkbox--show-label`],tabindex:u||!p?void 0:0,role:"checkbox","aria-checked":x?"mixed":h,"aria-labelledby":w,style:C,onKeyup:g,onKeydown:z,onClick:R,onMousedown:()=>{ie("selectstart",window,k=>{k.preventDefault()},{once:!0})}},l("div",{class:`${n}-checkbox-box-wrapper`}," ",l("div",{class:`${n}-checkbox-box`},l(de,null,{default:()=>this.indeterminate?l("div",{key:"indeterminate",class:`${n}-checkbox-icon`},l("svg",{viewBox:"0 0 100 100",class:"line-icon"},l("path",{d:"M80.2,55.5H21.4c-2.8,0-5.1-2.5-5.1-5.5l0,0c0-3,2.3-5.5,5.1-5.5h58.7c2.8,0,5.1,2.5,5.1,5.5l0,0C85.2,53.1,82.9,55.5,80.2,55.5z"}))):l("div",{key:"check",class:`${n}-checkbox-icon`},l("svg",{viewBox:"0 0 64 64",class:"check-icon"},l("path",{d:"M50.42,16.76L22.34,39.45l-8.1-11.46c-1.12-1.58-3.3-1.96-4.88-0.84c-1.58,1.12-1.95,3.3-0.84,4.88l10.26,14.51  c0.56,0.79,1.42,1.31,2.38,1.45c0.16,0.02,0.32,0.03,0.48,0.03c0.8,0,1.57-0.27,2.2-0.78l30.99-25.03c1.5-1.21,1.74-3.42,0.52-4.92  C54.13,15.78,51.93,15.55,50.42,16.76z"})))}),l("div",{class:`${n}-checkbox-box__border`}))),m)}});export{we as N};
