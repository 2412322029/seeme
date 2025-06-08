import{z as r,A as h,B as G,C as J,c2 as L,D as a,E as t,d as Y,y as s,H as b,K as Z,Q as y,S as oo,T as S,U as C,at as eo,V as no,X as ro,c3 as to,c4 as g,aq as ao}from"./index-DAkhcvNy.js";const io=r([h("card",`
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
 `,[L({background:"var(--n-color-modal)"}),a("hoverable",[r("&:hover","box-shadow: var(--n-box-shadow);")]),a("content-segmented",[r(">",[t("content",{paddingTop:"var(--n-padding-bottom)"})])]),a("content-soft-segmented",[r(">",[t("content",`
 margin: 0 var(--n-padding-left);
 padding: var(--n-padding-bottom) 0;
 `)])]),a("footer-segmented",[r(">",[t("footer",{paddingTop:"var(--n-padding-bottom)"})])]),a("footer-soft-segmented",[r(">",[t("footer",`
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
 `)]),a("bordered",`
 border: 1px solid var(--n-border-color);
 `,[r("&:target","border-color: var(--n-color-target);")]),a("action-segmented",[r(">",[t("action",[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),a("content-segmented, content-soft-segmented",[r(">",[t("content",{transition:"border-color 0.3s var(--n-bezier)"},[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),a("footer-segmented, footer-soft-segmented",[r(">",[t("footer",{transition:"border-color 0.3s var(--n-bezier)"},[r("&:not(:first-child)",{borderTop:"1px solid var(--n-border-color)"})])])]),a("embedded",`
 background-color: var(--n-color-embedded);
 `)]),G(h("card",`
 background: var(--n-color-modal);
 `,[a("embedded",`
 background-color: var(--n-color-embedded-modal);
 `)])),J(h("card",`
 background: var(--n-color-popover);
 `,[a("embedded",`
 background-color: var(--n-color-embedded-popover);
 `)]))]),so={title:[String,Function],contentClass:String,contentStyle:[Object,String],headerClass:String,headerStyle:[Object,String],headerExtraClass:String,headerExtraStyle:[Object,String],footerClass:String,footerStyle:[Object,String],embedded:Boolean,segmented:{type:[Boolean,Object],default:!1},size:{type:String,default:"medium"},bordered:{type:Boolean,default:!0},closable:Boolean,hoverable:Boolean,role:String,onClose:[Function,Array],tag:{type:String,default:"div"},cover:Function,content:[String,Function],footer:Function,action:Function,headerExtra:Function},co=Y({name:"Card",props:Object.assign(Object.assign({},y.props),so),slots:Object,setup(o){const{inlineThemeDisabled:f,mergedClsPrefixRef:v,mergedRtlRef:n}=Z(o),p=y("Card","-card",io,to,o,v),m=oo("Card",n,v),u=S(()=>{const{size:d}=o,{self:{color:i,colorModal:e,colorTarget:l,textColor:z,titleTextColor:x,titleFontWeight:k,borderColor:$,actionColor:w,borderRadius:E,lineHeight:_,closeIconColor:T,closeIconColorHover:F,closeIconColorPressed:O,closeColorHover:j,closeColorPressed:B,closeBorderRadius:P,closeIconSize:R,closeSize:I,boxShadow:H,colorPopover:V,colorEmbedded:A,colorEmbeddedModal:D,colorEmbeddedPopover:M,[C("padding",d)]:q,[C("fontSize",d)]:K,[C("titleFontSize",d)]:N},common:{cubicBezierEaseInOut:Q}}=p.value,{top:U,left:W,bottom:X}=eo(q);return{"--n-bezier":Q,"--n-border-radius":E,"--n-color":i,"--n-color-modal":e,"--n-color-popover":V,"--n-color-embedded":A,"--n-color-embedded-modal":D,"--n-color-embedded-popover":M,"--n-color-target":l,"--n-text-color":z,"--n-line-height":_,"--n-action-color":w,"--n-title-text-color":x,"--n-title-font-weight":k,"--n-close-icon-color":T,"--n-close-icon-color-hover":F,"--n-close-icon-color-pressed":O,"--n-close-color-hover":j,"--n-close-color-pressed":B,"--n-border-color":$,"--n-box-shadow":H,"--n-padding-top":U,"--n-padding-bottom":X,"--n-padding-left":W,"--n-font-size":K,"--n-title-font-size":N,"--n-close-size":I,"--n-close-icon-size":R,"--n-close-border-radius":P}}),c=f?no("card",S(()=>o.size[0]),u,o):void 0;return{rtlEnabled:m,mergedClsPrefix:v,mergedTheme:p,handleCloseClick:()=>{const{onClose:d}=o;d&&ro(d)},cssVars:f?void 0:u,themeClass:c==null?void 0:c.themeClass,onRender:c==null?void 0:c.onRender}},render(){const{segmented:o,bordered:f,hoverable:v,mergedClsPrefix:n,rtlEnabled:p,onRender:m,embedded:u,tag:c,$slots:d}=this;return m==null||m(),s(c,{class:[`${n}-card`,this.themeClass,u&&`${n}-card--embedded`,{[`${n}-card--rtl`]:p,[`${n}-card--content${typeof o!="boolean"&&o.content==="soft"?"-soft":""}-segmented`]:o===!0||o!==!1&&o.content,[`${n}-card--footer${typeof o!="boolean"&&o.footer==="soft"?"-soft":""}-segmented`]:o===!0||o!==!1&&o.footer,[`${n}-card--action-segmented`]:o===!0||o!==!1&&o.action,[`${n}-card--bordered`]:f,[`${n}-card--hoverable`]:v}],style:this.cssVars,role:this.role},b(d.cover,i=>{const e=this.cover?g([this.cover()]):i;return e&&s("div",{class:`${n}-card-cover`,role:"none"},e)}),b(d.header,i=>{const{title:e}=this,l=e?g(typeof e=="function"?[e()]:[e]):i;return l||this.closable?s("div",{class:[`${n}-card-header`,this.headerClass],style:this.headerStyle,role:"heading"},s("div",{class:`${n}-card-header__main`,role:"heading"},l),b(d["header-extra"],z=>{const x=this.headerExtra?g([this.headerExtra()]):z;return x&&s("div",{class:[`${n}-card-header__extra`,this.headerExtraClass],style:this.headerExtraStyle},x)}),this.closable&&s(ao,{clsPrefix:n,class:`${n}-card-header__close`,onClick:this.handleCloseClick,absolute:!0})):null}),b(d.default,i=>{const{content:e}=this,l=e?g(typeof e=="function"?[e()]:[e]):i;return l&&s("div",{class:[`${n}-card__content`,this.contentClass],style:this.contentStyle,role:"none"},l)}),b(d.footer,i=>{const e=this.footer?g([this.footer()]):i;return e&&s("div",{class:[`${n}-card__footer`,this.footerClass],style:this.footerStyle,role:"none"},e)}),b(d.action,i=>{const e=this.action?g([this.action()]):i;return e&&s("div",{class:`${n}-card__action`,role:"none"},e)}))}});export{co as N};
