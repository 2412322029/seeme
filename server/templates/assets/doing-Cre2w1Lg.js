import{K as R,L as le,M as v,O,P as f,Q as P,d as Q,R as x,S as oe,T as Ae,U as Pe,V as re,W as $,r as E,X as Oe,Y as Be,Z as Ee,p as B,$ as q,a0 as pe,a1 as J,b as ae,a2 as Re,a3 as Te,a4 as qe,a5 as ce,a6 as Ne,a7 as he,a8 as je,a9 as ge,aa as Ie,ab as Ve,ac as U,_ as se,ad as Le,v as M,ae as Me,c as z,o as p,a as r,k as w,af as be,y as D,t as k,u as l,ag as N,F as j,e as I,f as g,w as c,ah as Ue,ai as de,q as ue,j as A,aj as F,B as De,ak as me,al as Qe,am as $e}from"./index-uHSdsz2C.js";import{N as L,a as Z}from"./Table-CIAf65vO.js";import{N as ee}from"./Space-hGcNR6LJ.js";import{N as Y}from"./Checkbox-DDhnHpiO.js";import{u as He}from"./use-houdini-CDgaNB4F.js";Object.assign(Object.assign({},R.props),{left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"}});const Fe=le("n-float-button-group"),Ye=v("float-button",`
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
`,[O("circle-shape",`
 border-radius: 4096px;
 `),O("square-shape",`
 border-radius: var(--n-border-radius-square);
 `),f("fill",`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0
 left: 0;
 transition: background-color .3s var(--n-bezier);
 border-radius: inherit;
 `),f("body",`
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
 `,[f("description",`
 font-size: 12px;
 text-align: center;
 line-height: 14px;
 `)]),P("&:hover","box-shadow: var(--n-box-shadow-hover);",[P(">",[f("fill",`
 background-color: var(--n-color-hover);
 `)])]),P("&:active","box-shadow: var(--n-box-shadow-pressed);",[P(">",[f("fill",`
 background-color: var(--n-color-pressed);
 `)])]),O("show-menu",[P(">",[f("menu",`
 pointer-events: all;
 bottom: 100%;
 opacity: 1;
 `),f("close",`
 transform: scale(1);
 opacity: 1;
 `),f("body",`
 transform: scale(0.75);
 opacity: 0;
 `)])]),f("close",`
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
 `),f("menu",`
 position: absolute;
 bottom: calc(100% - 8px);
 display: flex;
 flex-direction: column;
 opacity: 0;
 pointer-events: none;
 transition:
 opacity .3s var(--n-bezier),
 bottom .3s var(--n-bezier); 
 `,[P("> *",`
 margin-bottom: 16px;
 `),v("float-button",`
 position: relative !important;
 `)])]),Ke=Object.assign(Object.assign({},R.props),{width:{type:[Number,String],default:40},height:{type:[Number,String],default:40},left:[Number,String],right:[Number,String],top:[Number,String],bottom:[Number,String],shape:{type:String,default:"circle"},position:{type:String,default:"fixed"},type:{type:String,default:"default"},menuTrigger:String,showMenu:{type:Boolean,default:void 0},onUpdateShowMenu:{type:[Function,Array],default:void 0},"onUpdate:showMenu":{type:[Function,Array],default:void 0}}),te=Q({name:"FloatButton",props:Ke,slots:Object,setup(t){const{mergedClsPrefixRef:n,inlineThemeDisabled:o}=$(t),d=E(null),s=R("FloatButton","-float-button",Ye,Oe,t,n),u=pe(Fe,null),S=E(!1),b=Be(t,"showMenu"),h=Ee(b,S);function C(y){const{onUpdateShowMenu:T,"onUpdate:showMenu":V}=t;S.value=y,T&&ce(T,y),V&&ce(V,y)}const _=B(()=>{const{self:{color:y,textColor:T,boxShadow:V,boxShadowHover:G,boxShadowPressed:W,colorHover:X,colorPrimary:ye,colorPrimaryHover:we,textColorPrimary:Se,borderRadiusSquare:ze,colorPressed:ke,colorPrimaryPressed:Ce},common:{cubicBezierEaseInOut:_e}}=s.value,{type:H}=t;return{"--n-bezier":_e,"--n-box-shadow":V,"--n-box-shadow-hover":G,"--n-box-shadow-pressed":W,"--n-color":H==="primary"?ye:y,"--n-text-color":H==="primary"?Se:T,"--n-color-hover":H==="primary"?we:X,"--n-color-pressed":H==="primary"?Ce:ke,"--n-border-radius-square":ze}}),a=B(()=>{const{width:y,height:T}=t;return Object.assign({position:u?void 0:t.position,width:q(y),minHeight:q(T)},u?null:{left:q(t.left),right:q(t.right),top:q(t.top),bottom:q(t.bottom)})}),e=B(()=>u?u.shapeRef.value:t.shape),i=()=>{t.menuTrigger==="hover"&&h.value&&C(!1)},m=o?J("float-button",B(()=>t.type[0]),_,t):void 0;return ae(()=>{const y=d.value;y&&Re("mousemoveoutside",y,i)}),Te(()=>{const y=d.value;y&&qe("mousemoveoutside",y,i)}),{inlineStyle:a,selfElRef:d,cssVars:o?void 0:_,mergedClsPrefix:n,mergedShape:e,mergedShowMenu:h,themeClass:m==null?void 0:m.themeClass,onRender:m==null?void 0:m.onRender,Mouseenter:()=>{t.menuTrigger==="hover"&&C(!0)},handleMouseleave:i,handleClick:()=>{t.menuTrigger==="click"&&C(!h.value)}}},render(){var t;const{mergedClsPrefix:n,cssVars:o,mergedShape:d,type:s,menuTrigger:u,mergedShowMenu:S,themeClass:b,$slots:h,inlineStyle:C,onRender:_}=this;return _==null||_(),x("div",{ref:"selfElRef",class:[`${n}-float-button`,`${n}-float-button--${d}-shape`,`${n}-float-button--${s}-type`,S&&`${n}-float-button--show-menu`,b],style:[o,C],onMouseenter:this.Mouseenter,onMouseleave:this.handleMouseleave,onClick:this.handleClick,role:"button"},x("div",{class:`${n}-float-button__fill`,"aria-hidden":!0}),x("div",{class:`${n}-float-button__body`},(t=h.default)===null||t===void 0?void 0:t.call(h),re(h.description,a=>a?x("div",{class:`${n}-float-button__description`},a):null)),u?x("div",{class:`${n}-float-button__close`},x(Ae,{clsPrefix:n},{default:()=>x(Pe,null)})):null,u?x("div",{onClick:a=>{a.stopPropagation()},"data-float-button-menu":!0,class:`${n}-float-button__menu`},oe(h.menu,()=>[])):null)}}),ve={type:String,default:"static"},Je=v("layout",`
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
`,[v("layout-scroll-container",`
 overflow-x: hidden;
 box-sizing: border-box;
 height: 100%;
 `),O("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),Ge={embedded:Boolean,position:ve,nativeScrollbar:{type:Boolean,default:!0},scrollbarProps:Object,onScroll:Function,contentClass:String,contentStyle:{type:[String,Object],default:""},hasSider:Boolean,siderPlacement:{type:String,default:"left"}},We=le("n-layout");function fe(t){return Q({name:t?"LayoutContent":"Layout",props:Object.assign(Object.assign({},R.props),Ge),setup(n){const o=E(null),d=E(null),{mergedClsPrefixRef:s,inlineThemeDisabled:u}=$(n),S=R("Layout","-layout",Je,he,n,s);ge(We,n);let b=0,h=0;je(()=>{if(n.nativeScrollbar){const e=o.value;e&&(e.scrollTop=h,e.scrollLeft=b)}});const C={scrollTo:function(e,i){if(n.nativeScrollbar){const{value:m}=o;m&&(i===void 0?m.scrollTo(e):m.scrollTo(e,i))}else{const{value:m}=d;m&&m.scrollTo(e,i)}}},_=B(()=>{const{common:{cubicBezierEaseInOut:e},self:i}=S.value;return{"--n-bezier":e,"--n-color":n.embedded?i.colorEmbedded:i.color,"--n-text-color":i.textColor}}),a=u?J("layout",B(()=>n.embedded?"e":""),_,n):void 0;return Object.assign({mergedClsPrefix:s,scrollableElRef:o,scrollbarInstRef:d,hasSiderStyle:{display:"flex",flexWrap:"nowrap",width:"100%",flexDirection:"row"},mergedTheme:S,handleNativeElScroll:e=>{var i;const m=e.target;b=m.scrollLeft,h=m.scrollTop,(i=n.onScroll)===null||i===void 0||i.call(n,e)},cssVars:u?void 0:_,themeClass:a==null?void 0:a.themeClass,onRender:a==null?void 0:a.onRender},C)},render(){var n;const{mergedClsPrefix:o,hasSider:d}=this;(n=this.onRender)===null||n===void 0||n.call(this);const s=d?this.hasSiderStyle:void 0,u=[this.themeClass,t&&`${o}-layout-content`,`${o}-layout`,`${o}-layout--${this.position}-positioned`];return x("div",{class:u,style:this.cssVars},this.nativeScrollbar?x("div",{ref:"scrollableElRef",class:[`${o}-layout-scroll-container`,this.contentClass],style:[this.contentStyle,s],onScroll:this.handleNativeElScroll},this.$slots):x(Ne,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:this.contentClass,contentStyle:[this.contentStyle,s]}),this.$slots))}})}const Xe=fe(!1),Ze=fe(!0),et=v("layout-header",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 box-sizing: border-box;
 width: 100%;
 background-color: var(--n-color);
 color: var(--n-text-color);
`,[O("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 `),O("bordered",`
 border-bottom: solid 1px var(--n-border-color);
 `)]),tt={position:ve,inverted:Boolean,bordered:{type:Boolean,default:!1}},nt=Q({name:"LayoutHeader",props:Object.assign(Object.assign({},R.props),tt),setup(t){const{mergedClsPrefixRef:n,inlineThemeDisabled:o}=$(t),d=R("Layout","-layout-header",et,he,t,n),s=B(()=>{const{common:{cubicBezierEaseInOut:S},self:b}=d.value,h={"--n-bezier":S};return t.inverted?(h["--n-color"]=b.headerColorInverted,h["--n-text-color"]=b.textColorInverted,h["--n-border-color"]=b.headerBorderColorInverted):(h["--n-color"]=b.headerColor,h["--n-text-color"]=b.textColor,h["--n-border-color"]=b.headerBorderColor),h}),u=o?J("layout-header",B(()=>t.inverted?"a":"b"),s,t):void 0;return{mergedClsPrefix:n,cssVars:o?void 0:s,themeClass:u==null?void 0:u.themeClass,onRender:u==null?void 0:u.onRender}},render(){var t;const{mergedClsPrefix:n}=this;return(t=this.onRender)===null||t===void 0||t.call(this),x("div",{class:[`${n}-layout-header`,this.themeClass,this.position&&`${n}-layout-header--${this.position}-positioned`,this.bordered&&`${n}-layout-header--bordered`],style:this.cssVars},this.$slots)}}),it=v("timeline",`
 position: relative;
 width: 100%;
 display: flex;
 flex-direction: column;
 line-height: 1.25;
`,[O("horizontal",`
 flex-direction: row;
 `,[P(">",[v("timeline-item",`
 flex-shrink: 0;
 padding-right: 40px;
 `,[O("dashed-line-type",[P(">",[v("timeline-item-timeline",[f("line",`
 background-image: linear-gradient(90deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 10px 1px;
 `)])])]),P(">",[v("timeline-item-content",`
 margin-top: calc(var(--n-icon-size) + 12px);
 `,[P(">",[f("meta",`
 margin-top: 6px;
 margin-bottom: unset;
 `)])]),v("timeline-item-timeline",`
 width: 100%;
 height: calc(var(--n-icon-size) + 12px);
 `,[f("line",`
 left: var(--n-icon-size);
 top: calc(var(--n-icon-size) / 2 - 1px);
 right: 0px;
 width: unset;
 height: 2px;
 `)])])])])]),O("right-placement",[v("timeline-item",[v("timeline-item-content",`
 text-align: right;
 margin-right: calc(var(--n-icon-size) + 12px);
 `),v("timeline-item-timeline",`
 width: var(--n-icon-size);
 right: 0;
 `)])]),O("left-placement",[v("timeline-item",[v("timeline-item-content",`
 margin-left: calc(var(--n-icon-size) + 12px);
 `),v("timeline-item-timeline",`
 left: 0;
 `)])]),v("timeline-item",`
 position: relative;
 `,[P("&:last-child",[v("timeline-item-timeline",[f("line",`
 display: none;
 `)]),v("timeline-item-content",[f("meta",`
 margin-bottom: 0;
 `)])]),v("timeline-item-content",[f("title",`
 margin: var(--n-title-margin);
 font-size: var(--n-title-font-size);
 transition: color .3s var(--n-bezier);
 font-weight: var(--n-title-font-weight);
 color: var(--n-title-text-color);
 `),f("content",`
 transition: color .3s var(--n-bezier);
 font-size: var(--n-content-font-size);
 color: var(--n-content-text-color);
 `),f("meta",`
 transition: color .3s var(--n-bezier);
 font-size: 12px;
 margin-top: 6px;
 margin-bottom: 20px;
 color: var(--n-meta-text-color);
 `)]),O("dashed-line-type",[v("timeline-item-timeline",[f("line",`
 --n-color-start: var(--n-line-color);
 transition: --n-color-start .3s var(--n-bezier);
 background-color: transparent;
 background-image: linear-gradient(180deg, var(--n-color-start), var(--n-color-start) 50%, transparent 50%, transparent 100%);
 background-size: 1px 10px;
 `)])]),v("timeline-item-timeline",`
 width: calc(var(--n-icon-size) + 12px);
 position: absolute;
 top: calc(var(--n-title-font-size) * 1.25 / 2 - var(--n-icon-size) / 2);
 height: 100%;
 `,[f("circle",`
 border: var(--n-circle-border);
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 border-radius: var(--n-icon-size);
 box-sizing: border-box;
 `),f("icon",`
 color: var(--n-icon-color);
 font-size: var(--n-icon-size);
 height: var(--n-icon-size);
 width: var(--n-icon-size);
 display: flex;
 align-items: center;
 justify-content: center;
 `),f("line",`
 transition: background-color .3s var(--n-bezier);
 position: absolute;
 top: var(--n-icon-size);
 left: calc(var(--n-icon-size) / 2 - 1px);
 bottom: 0px;
 width: 2px;
 background-color: var(--n-line-color);
 `)])])]),ot=Object.assign(Object.assign({},R.props),{horizontal:Boolean,itemPlacement:{type:String,default:"left"},size:{type:String,default:"medium"},iconSize:Number}),xe=le("n-timeline"),ne=Q({name:"Timeline",props:ot,setup(t,{slots:n}){const{mergedClsPrefixRef:o}=$(t),d=R("Timeline","-timeline",it,Ie,t,o);return ge(xe,{props:t,mergedThemeRef:d,mergedClsPrefixRef:o}),()=>{const{value:s}=o;return x("div",{class:[`${s}-timeline`,t.horizontal&&`${s}-timeline--horizontal`,`${s}-timeline--${t.size}-size`,!t.horizontal&&`${s}-timeline--${t.itemPlacement}-placement`]},n)}}}),ie=Q({name:"TimelineItem",props:{time:[String,Number],title:String,content:String,color:String,lineType:{type:String,default:"default"},type:{type:String,default:"default"}},slots:Object,setup(t){const n=pe(xe);n||Ve("timeline-item","`n-timeline-item` must be placed inside `n-timeline`."),He();const{inlineThemeDisabled:o}=$(),d=B(()=>{const{props:{size:u,iconSize:S},mergedThemeRef:b}=n,{type:h}=t,{self:{titleTextColor:C,contentTextColor:_,metaTextColor:a,lineColor:e,titleFontWeight:i,contentFontSize:m,[U("iconSize",u)]:y,[U("titleMargin",u)]:T,[U("titleFontSize",u)]:V,[U("circleBorder",h)]:G,[U("iconColor",h)]:W},common:{cubicBezierEaseInOut:X}}=b.value;return{"--n-bezier":X,"--n-circle-border":G,"--n-icon-color":W,"--n-content-font-size":m,"--n-content-text-color":_,"--n-line-color":e,"--n-meta-text-color":a,"--n-title-font-size":V,"--n-title-font-weight":i,"--n-title-margin":T,"--n-title-text-color":C,"--n-icon-size":q(S)||y}}),s=o?J("timeline-item",B(()=>{const{props:{size:u,iconSize:S}}=n,{type:b}=t;return`${u[0]}${S||"a"}${b[0]}`}),d,n.props):void 0;return{mergedClsPrefix:n.mergedClsPrefixRef,cssVars:o?void 0:d,themeClass:s==null?void 0:s.themeClass,onRender:s==null?void 0:s.onRender}},render(){const{mergedClsPrefix:t,color:n,onRender:o,$slots:d}=this;return o==null||o(),x("div",{class:[`${t}-timeline-item`,this.themeClass,`${t}-timeline-item--${this.type}-type`,`${t}-timeline-item--${this.lineType}-line-type`],style:this.cssVars},x("div",{class:`${t}-timeline-item-timeline`},x("div",{class:`${t}-timeline-item-timeline__line`}),re(d.icon,s=>s?x("div",{class:`${t}-timeline-item-timeline__icon`,style:{color:n}},s):x("div",{class:`${t}-timeline-item-timeline__circle`,style:{borderColor:n}}))),x("div",{class:`${t}-timeline-item-content`},re(d.header,s=>s||this.title?x("div",{class:`${t}-timeline-item-content__title`},s||this.title):null),x("div",{class:`${t}-timeline-item-content__content`},oe(d.default,()=>[this.content])),x("div",{class:`${t}-timeline-item-content__meta`},oe(d.footer,()=>[this.time]))))}}),rt={id:"ai-container",style:{"max-width":"800px",border:"1px solid #5c5c5c","border-radius":"20px",padding:"10px",margin:"5px"}},lt=["innerHTML"],at=se({__name:"ai",setup(t){const n=E("");return ae(()=>{try{const o=new EventSource(Le+"/ai_summary");o.onmessage=d=>{n.value+=d.data},o.addEventListener("end",()=>{o.close()}),o.onerror=d=>{o.close()},window.eventSource=o}catch(o){M(o.message,{theme:"auto",type:"error"}),n.value+=`<p style="color: red;">${o.message}</p>`}}),Me(()=>{var o;(o=window.eventSource)==null||o.close(),window.eventSource=void 0}),(o,d)=>(p(),z("div",rt,[d[0]||(d[0]=r("p",{style:{margin:"5px",color:"#18a058",display:"flex","align-items":"center"}},[r("i",{id:"ai-icon"}),w(" AI 摘要 ")],-1)),r("div",{innerHTML:n.value},null,8,lt)]))}},[["__scopeId","data-v-695eaa09"]]),K=t=>t.includes("QQ")?"/assets/qq.png":t.includes("Chrome")?"data:image/png;base64,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":t.includes("哔哩哔哩")?"/assets/bilibili.jpg":"",st={key:0,title:"",style:{"min-width":"700px",overflow:"auto"}},ct={style:{margin:"0"}},dt={id:"icarea",style:{display:"flex","justify-content":"flex-start","align-items":"center"}},ut=["src"],mt=["src"],pt=se({__name:"show_activity_window",setup(t){const n=E();return be(()=>{Ue().then(o=>{typeof o!="string"?n.value=o:M(o,{theme:"auto",type:"error"})}).catch(o=>{M(o,{theme:"auto",type:"error"})})}),(o,d)=>{var s;return(s=n.value)!=null&&s.activity_window?(p(),z("div",st,[r("p",ct,"活动程序 "+k(l(N)(n.value.report_time)),1),r("div",dt,[r("img",{src:l("/assets/win.png"),class:"ic",style:{padding:"0px 5px","margin-top":"-8px"}},null,8,ut),(p(!0),z(j,null,I(n.value.activity_window,(u,S)=>(p(),z("div",{key:S,class:"icitem"},[g(l(L),{trigger:"hover",placement:"top"},{trigger:c(()=>[r("img",{src:"/exe_icon/"+u.exe_name+".png",class:"ic"},null,8,mt)]),default:c(()=>[w(" "+k(u.title),1)]),_:2},1024)]))),128))])])):D("",!0)}}},[["__scopeId","data-v-137d535c"]]),ht={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/releases"},gt={style:{display:"flex","align-items":"center"}},bt=["src"],vt={key:1},ft=["src"],xt={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/自动汇报.js"},yt=["href"],wt={key:1},St=["src"],zt={target:"_blank",style:{"background-color":"transparent"},href:"https://github.com/2412322029/seeme/blob/master/report/%E8%87%AA%E5%8A%A8%E6%B1%87%E6%8A%A5.macro"},kt={style:{display:"flex","align-items":"center"}},Ct=["src"],_t={key:1},At=["src"],Pt=se({__name:"pcstatus",setup(t){const n=E(!1),o=de([!0,!0,!0]);ae(()=>{const a=localStorage.getItem("showtimeline");n.value=a?JSON.parse(a):window.innerWidth<=900;const e=localStorage.getItem("showwhat");if(e){const i=JSON.parse(e);o[0]=i[0],o[1]=i[1],o[2]=i[2]}else o.fill(!0)}),ue(n,a=>{localStorage.setItem("showtimeline",JSON.stringify(a))}),ue(o,a=>{localStorage.setItem("showwhat",JSON.stringify(a))});const d=de({info:""}),s=E(),u=E({browser:0,pc:0,phone:0});function S(){s.value=void 0,Qe().then(a=>{typeof a!="string"?u.value=a:M(a,{theme:"auto",type:"error"})}).catch(a=>{M(a,{theme:"auto",type:"error"})}),$e().then(a=>{typeof a!="string"?s.value=a:d.info=a}).catch(a=>{M(a,{theme:"auto",type:"error"})})}function b(a,e){return a.length>e?a.substring(0,e)+"...":a}function h(a){const e=new Date(1e3*a);return`${e.getFullYear()}-${String(e.getMonth()+1).padStart(2,"0")}-${String(e.getDate()).padStart(2,"0")} ${String(e.getHours()).padStart(2,"0")}:${String(e.getMinutes()).padStart(2,"0")}:${String(e.getSeconds()).padStart(2,"0")}`}function C(a){return a.slice().reverse()}function _(a){a.target.src="/assets/desktop.png"}return be(()=>{S()}),(a,e)=>(p(),A(l(Xe),null,{default:c(()=>[g(l(nt),null,{default:c(()=>[g(l(F),{title:"你在干什么?",style:{"margin-bottom":"10px"}},{default:c(()=>[g(at),g(l(ee),null,{default:c(()=>[r("span",null,[e[4]||(e[4]=w("时间线表示 ")),g(l(Y),{checked:n.value,"onUpdate:checked":e[0]||(e[0]=i=>n.value=i)},null,8,["checked"])]),r("span",null,[e[5]||(e[5]=w("显示电脑 ")),g(l(Y),{checked:o[0],"onUpdate:checked":e[1]||(e[1]=i=>o[0]=i)},null,8,["checked"])]),r("span",null,[e[6]||(e[6]=w("显示浏览器 ")),g(l(Y),{checked:o[1],"onUpdate:checked":e[2]||(e[2]=i=>o[1]=i)},null,8,["checked"])]),r("span",null,[e[7]||(e[7]=w("显示手机 ")),g(l(Y),{checked:o[2],"onUpdate:checked":e[3]||(e[3]=i=>o[2]=i)},null,8,["checked"])])]),_:1}),g(l(De),{onClick:S,text:"",style:{margin:"10px 0",float:"right","font-size":"20px"},title:"刷新"},{default:c(()=>e[8]||(e[8]=[w("↻")])),_:1})]),_:1})]),_:1}),g(l(Ze),null,{default:c(()=>[g(l(ee),{vertical:""},{default:c(()=>[s.value?(p(),A(l(ee),{key:0,vertical:""},{default:c(()=>[o[0]?(p(),A(l(F),{key:0,title:"电脑(最新"+u.value.pc+"项)"},{"header-extra":c(()=>[g(l(L),{trigger:"hover",placement:"right"},{trigger:c(()=>[r("a",ht,[g(l(te),{position:"relative"},{default:c(()=>e[9]||(e[9]=[w("?")])),_:1})])]),default:c(()=>[e[10]||(e[10]=w(" 电脑端自动报告程序,点击前往 "))]),_:1})]),default:c(()=>[g(pt),n.value?(p(),z("div",vt,[g(l(ne),null,{default:c(()=>[(p(!0),z(j,null,I(s.value.pc,(i,m)=>(p(),A(l(ie),{key:m,type:"success",title:i.exe_name,content:i.running_exe,time:l(N)(i.report_time)},me({_:2},[i.exe_name?{name:"icon",fn:c(()=>[r("img",{src:"/exe_icon/"+i.exe_name+".png",alt:"",onError:_,style:{width:"20px","z-index":"2"}},null,40,ft)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(p(),A(l(Z),{key:0,bordered:!1},{default:c(()=>[e[11]||(e[11]=r("thead",null,[r("tr",null,[r("th",null,"可执行程序"),r("th",null,"前台窗口标题"),r("th",null,"时间")])],-1)),r("tbody",null,[(p(!0),z(j,null,I(C(s.value.pc),(i,m)=>(p(),z("tr",{key:m},[r("td",null,[r("div",gt,[r("img",{size:"small",src:"/exe_icon/"+i.exe_name+".png",onError:_,style:{margin:"0 5px",width:"20px"}},null,40,bt),w(" "+k(i.exe_name),1)])]),r("td",null,[g(l(L),{"show-arrow":!1,trigger:"hover"},{trigger:c(()=>{return[w(k(b((y=i.running_exe,y.includes("Google Chrome")?"Google Chrome":y),30)),1)];var y}),default:c(()=>[w(" "+k(i.running_exe),1)]),_:2},1024)]),r("td",null,k(l(N)(i.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):D("",!0),o[1]?(p(),A(l(F),{key:1,title:"电脑浏览器(最新"+u.value.browser+"项)"},{"header-extra":c(()=>[g(l(L),{trigger:"hover",placement:"right"},{trigger:c(()=>[r("a",xt,[g(l(te),{position:"relative"},{default:c(()=>e[12]||(e[12]=[w("?")])),_:1})])]),default:c(()=>[e[13]||(e[13]=w(" 浏览器油猴脚本,点击前往 "))]),_:1})]),default:c(()=>[n.value?(p(),z("div",wt,[g(l(ne),null,{default:c(()=>[(p(!0),z(j,null,I(s.value.browser,(i,m)=>(p(),A(l(ie),{key:m,type:"success",title:b(i.title,70),content:b(i.url,70),time:l(N)(i.report_time)},{icon:c(()=>[r("img",{src:l(K)("Chrome"),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,St)]),_:2},1032,["title","content","time"]))),128))]),_:1})])):(p(),A(l(Z),{key:0,bordered:!1},{default:c(()=>[e[14]||(e[14]=r("thead",null,[r("tr",null,[r("th",null,"网页标题"),r("th",null,"网页链接"),r("th",null,"时间")])],-1)),r("tbody",null,[(p(!0),z(j,null,I(C(s.value.browser),(i,m)=>(p(),z("tr",{key:m},[r("td",null,[g(l(L),{trigger:"hover"},{trigger:c(()=>[w(k(b(i.title,30)),1)]),default:c(()=>[w(" "+k(i.title),1)]),_:2},1024)]),r("td",null,[r("a",{target:"_blank",href:i.url,class:"nowrap-ellipsis"},k(b(i.url,30)),9,yt)]),r("td",null,k(l(N)(i.report_time)),1)]))),128))])]),_:1}))]),_:1},8,["title"])):D("",!0),o[2]?(p(),A(l(F),{key:2,title:"手机(最新"+u.value.phone+"项)"},{"header-extra":c(()=>[g(l(L),{trigger:"hover",placement:"right"},{trigger:c(()=>[r("a",zt,[g(l(te),{position:"relative"},{default:c(()=>e[15]||(e[15]=[w("?")])),_:1})])]),default:c(()=>[e[16]||(e[16]=w(" 点击前往, 下载文件导入安卓MacroDroid软件 "))]),_:1})]),default:c(()=>[n.value?(p(),z("div",_t,[g(l(ne),null,{default:c(()=>[(p(!0),z(j,null,I(s.value.phone,(i,m)=>(p(),A(l(ie),{key:m,type:"success",title:i.app,content:i.battery_level+"  / wifi信号:  "+i.wifi_ssid,time:l(N)(h(i.report_time))},me({_:2},[l(K)(i.app)?{name:"icon",fn:c(()=>[r("img",{src:l(K)(i.app),alt:"",srcset:"",style:{width:"20px","z-index":"2"}},null,8,At)]),key:"0"}:void 0]),1032,["title","content","time"]))),128))]),_:1})])):(p(),A(l(Z),{key:0,bordered:!1},{default:c(()=>[e[17]||(e[17]=r("thead",null,[r("tr",null,[r("th",null,"前台应用"),r("th",null,"电池"),r("th",null,"wifi"),r("th",null,"时间")])],-1)),r("tbody",null,[(p(!0),z(j,null,I(C(s.value.phone),(i,m)=>(p(),z("tr",{key:m},[r("td",null,[r("div",kt,[r("img",{size:"small",src:l(K)(i.app),style:{margin:"0 5px",width:"20px"}},null,8,Ct),w(" "+k(i.app),1)])]),r("td",null,k(i.battery_level),1),r("td",null,k(i.wifi_ssid),1),r("td",null,k(l(N)(h(i.report_time))),1)]))),128))])]),_:1}))]),_:1},8,["title"])):D("",!0)]),_:1})):D("",!0)]),_:1})]),_:1})]),_:1}))}},[["__scopeId","data-v-b9452990"]]),qt={__name:"doing",setup:t=>(n,o)=>(p(),A(Pt))};export{qt as default};
