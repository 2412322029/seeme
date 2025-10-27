import{M as r,O as h,P as G,Q as J,c7 as K,R as d,S as t,d as Y,L as s,U as b,c8 as g,ax as Z,X as oo,a2 as S,c9 as eo,a4 as no,p as y,a5 as C,aA as ro,a6 as to,a8 as ao}from"./index-Ow1yCR_l.js";const io=r([h("card",`
 font-size: var(--n-font-size);
 line-height: var(--n-line-height);
 display: flex;
 flex-direction: column;
 width: 100%;
 box-sizing: border-box;
 position: relative;
 border-radius: var(--n-border-radius);
 background-color: var(--n-color);
 color: var(--n-text-color);
 word-break: break-word;
 transition: 
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[K({background:"var(--n-color-modal)"}),d("hoverable",[r("&:hover","box-shadow: var(--n-box-shadow);")]),d("content-segmented",[r(">",[t("content",{paddingTop:"var(--n-padding-bottom)"})])]),d("content-soft-segmented",[r(">",[t("content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `)])]),d("footer-segmented",[r(">",[t("footer",{paddingTop:"var(--n-padding-bottom)"})])]),d("footer-soft-segmented",[r(">",[t("footer",`
 padding: var(--n-padding-bottom) 0;
 margin: 0 var(--n-padding-left);
 `)])]),r(">",[h("card-header",`
 box-sizing: border-box;
 display: flex;
 align-items: center;
 font-size: var(--n-title-font-size);
 padding:
 var(--n-padding-top)
 var(--n-padding-left)
 var(--n-padding-bottom)
 var(--n-padding-left);
 `,[t("main",`
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 flex: 1;
 min-width: 0;
 color: var(--n-title-text-color);
 `),t("extra",`
 display: flex;
 align-items: center;
 font-size: var(--n-font-size);
 font-weight: 400;
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 `),t("close",`
 margin: 0 0 0 8px;
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)]),t("action",`
 box-sizing: border-box;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 background-clip: padding-box;
 background-color: var(--n-action-color);
 `),t("content","flex: 1; min-width: 0;"),t("content, footer",`
 box-sizing: border-box;
 padding: 0 var(--n-padding-left) var(--n-padding-bottom) var(--n-padding-left);
 font-size: var(--n-font-size);
 `,[r("&:first-child",{paddingTop:"var(--n-padding-bottom)"})]),t("action",`
 background-color: var(--n-action-color);
 padding: var(--n-padding-bottom) var(--n-padding-left);
 border-bottom-left-radius: var(--n-border-radius);
 border-bottom-right-radius: var(--n-border-radius);
 `)]),h("card-cover",`
 overflow: hidden;
 width: 100%;
 border-radius: var(--n-border-radius) var(--n-border-radius) 0 0;
 `,[r("img",`
 display: block;
 width: 100%;
 `)]),d("bordered",`
 border: 1px solid var(--n-border-color);
 `,[r("&:target","border-color: var(--n-color-target);")]),d("action-segmented",[r(">",[t("action",[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),d("content-segmented, content-soft-segmented",[r(">",[t("content",{transition:"border-color 0.3s var(--n-bezier)"},[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),d("footer-segmented, footer-soft-segmented",[r(">",[t("footer",{transition:"border-color 0.3s var(--n-bezier)"},[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),d("embedded",`
 background-color: var(--n-color-embedded);
 `)]),G(h("card",`
 background: var(--n-color-modal);
 `,[d("embedded",`
 background-color: var(--n-color-embedded-modal);
 `)])),J(h("card",`
 background: var(--n-color-popover);
 `,[d("embedded",`
 background-color: var(--n-color-embedded-popover);
 `)]))]),so={title:[String,Function],contentClass:String,contentStyle:[Object,String],headerClass:String,headerStyle:[Object,String],headerExtraClass:String,headerExtraStyle:[Object,String],footerClass:String,footerStyle:[Object,String],embedded:Boolean,segmented:{type:[Boolean,Object],default:!1},size:{type:String,default:"medium"},bordered:{type:Boolean,default:!0},closable:Boolean,hoverable:Boolean,role:String,onClose:[Function,Array],tag:{type:String,default:"div"},cover:Function,content:[String,Function],footer:Function,action:Function,headerExtra:Function},co=Y({name:"Card",props:Object.assign(Object.assign({},S.props),so),slots:Object,setup(o){const{inlineThemeDisabled:f,mergedClsPrefixRef:v,mergedRtlRef:n}=oo(o),p=S("Card","-card",io,eo,o,v),m=no("Card",n,v),u=y(()=>{const{size:a}=o,{self:{color:i,colorModal:e,colorTarget:l,textColor:z,titleTextColor:x,titleFontWeight:k,borderColor:$,actionColor:w,borderRadius:E,lineHeight:_,closeIconColor:O,closeIconColorHover:T,closeIconColorPressed:F,closeColorHover:P,closeColorPressed:R,closeBorderRadius:j,closeIconSize:B,closeSize:I,boxShadow:H,colorPopover:M,colorEmbedded:A,colorEmbeddedModal:V,colorEmbeddedPopover:D,[C("padding",a)]:L,[C("fontSize",a)]:N,[C("titleFontSize",a)]:Q},common:{cubicBezierEaseInOut:U}}=p.value,{top:W,left:X,bottom:q}=ro(L);return{"--n-bezier":U,"--n-border-radius":E,"--n-color":i,"--n-color-modal":e,"--n-color-popover":M,"--n-color-embedded":A,"--n-color-embedded-modal":V,"--n-color-embedded-popover":D,"--n-color-target":l,"--n-text-color":z,"--n-line-height":_,"--n-action-color":w,"--n-title-text-color":x,"--n-title-font-weight":k,"--n-close-icon-color":O,"--n-close-icon-color-hover":T,"--n-close-icon-color-pressed":F,"--n-close-color-hover":P,"--n-close-color-pressed":R,"--n-border-color":$,"--n-box-shadow":H,"--n-padding-top":W,"--n-padding-bottom":q,"--n-padding-left":X,"--n-font-size":N,"--n-title-font-size":Q,"--n-close-size":I,"--n-close-icon-size":B,"--n-close-border-radius":j}}),c=f?to("card",y(()=>o.size[0]),u,o):void 0;return{rtlEnabled:m,mergedClsPrefix:v,mergedTheme:p,handleCloseClick:()=>{const{onClose:a}=o;a&&ao(a)},cssVars:f?void 0:u,themeClass:c==null?void 0:c.themeClass,onRender:c==null?void 0:c.onRender}},render(){const{segmented:o,bordered:f,hoverable:v,mergedClsPrefix:n,rtlEnabled:p,onRender:m,embedded:u,tag:c,$slots:a}=this;return m==null||m(),s(c,{class:[`${n}-card`,this.themeClass,u&&`${n}-card--embedded`,{[`${n}-card--rtl`]:p,[`${n}-card--content${typeof o!="boolean"&&o.content==="soft"?"-soft":""}-segmented`]:o===!0||o!==!1&&o.content,[`${n}-card--footer${typeof o!="boolean"&&o.footer==="soft"?"-soft":""}-segmented`]:o===!0||o!==!1&&o.footer,[`${n}-card--action-segmented`]:o===!0||o!==!1&&o.action,[`${n}-card--bordered`]:f,[`${n}-card--hoverable`]:v}],style:this.cssVars,role:this.role},b(a.cover,i=>{const e=this.cover?g([this.cover()]):i;return e&&s("div",{class:`${n}-card-cover`,role:"none"},e)}),b(a.header,i=>{const{title:e}=this,l=e?g(typeof e=="function"?[e()]:[e]):i;return l||this.closable?s("div",{class:[`${n}-card-header`,this.headerClass],style:this.headerStyle,role:"heading"},s("div",{class:`${n}-card-header__main`,role:"heading"},l),b(a["header-extra"],z=>{const x=this.headerExtra?g([this.headerExtra()]):z;return x&&s("div",{class:[`${n}-card-header__extra`,this.headerExtraClass],style:this.headerExtraStyle},x)}),this.closable&&s(Z,{clsPrefix:n,class:`${n}-card-header__close`,onClick:this.handleCloseClick,absolute:!0})):null}),b(a.default,i=>{const{content:e}=this,l=e?g(typeof e=="function"?[e()]:[e]):i;return l&&s("div",{class:[`${n}-card__content`,this.contentClass],style:this.contentStyle,role:"none"},l)}),b(a.footer,i=>{const e=this.footer?g([this.footer()]):i;return e&&s("div",{class:[`${n}-card__footer`,this.footerClass],style:this.footerStyle,role:"none"},e)}),b(a.action,i=>{const e=this.action?g([this.action()]):i;return e&&s("div",{class:`${n}-card__action`,role:"none"},e)}))}});export{co as N};
