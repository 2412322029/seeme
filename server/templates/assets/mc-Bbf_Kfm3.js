import{d as Q,c as H,o as $,a as l,M as P,P as f,O as q,Q as N,R as u,an as te,ao as ae,S as K,T as oe,ap as le,aq as se,ar as ie,as as ce,V as X,at as de,W as Y,K as V,au as ue,av as ve,p as L,aw as he,ac as C,a1 as ee,r as O,L as pe,ax as me,ay as ge,az as fe,a0 as Z,aA as be,aB as ye,aC as ze,b as re,aD as xe,a3 as we,q as ne,H as Ce,J as Oe,ai as Se,I as ke,af as _e,j as J,w as _,f as k,y as Re,u as g,B as $e,k as T,t as R,N as G,aE as Pe,F as je,e as Le,aj as Fe,v as I,aF as Te,aG as Ae}from"./index-uHSdsz2C.js";import{N as Be}from"./DynamicTags-DcQN5Nil.js";import{f as Ee,N as Ie}from"./Skeleton-DiSpmO9y.js";import{i as Me,o as He}from"./utils-BrJM4kNr.js";import{N as Ne}from"./Input-DUote18s.js";import{a as Je,N as Ve}from"./Table-CIAf65vO.js";import"./Space-hGcNR6LJ.js";import"./use-locale-D1koWyT3.js";import"./use-houdini-CDgaNB4F.js";const We={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 448 512"},De=Q({name:"ShareAlt",render:function(n,a){return $(),H("svg",We,a[0]||(a[0]=[l("path",{d:"M352 320c-22.608 0-43.387 7.819-59.79 20.895l-102.486-64.054a96.551 96.551 0 0 0 0-41.683l102.486-64.054C308.613 184.181 329.392 192 352 192c53.019 0 96-42.981 96-96S405.019 0 352 0s-96 42.981-96 96c0 7.158.79 14.13 2.276 20.841L155.79 180.895C139.387 167.819 118.608 160 96 160c-53.019 0-96 42.981-96 96s42.981 96 96 96c22.608 0 43.387-7.819 59.79-20.895l102.486 64.054A96.301 96.301 0 0 0 256 416c0 53.019 42.981 96 96 96s96-42.981 96-96s-42.981-96-96-96z",fill:"currentColor"},null,-1)]))}}),qe=P("alert",`
 line-height: var(--n-line-height);
 border-radius: var(--n-border-radius);
 position: relative;
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-color);
 text-align: start;
 word-break: break-word;
`,[f("border",`
 border-radius: inherit;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 transition: border-color .3s var(--n-bezier);
 border: var(--n-border);
 pointer-events: none;
 `),q("closable",[P("alert-body",[f("title",`
 padding-right: 24px;
 `)])]),f("icon",{color:"var(--n-icon-color)"}),P("alert-body",{padding:"var(--n-padding)"},[f("title",{color:"var(--n-title-text-color)"}),f("content",{color:"var(--n-content-text-color)"})]),Ee({originalTransition:"transform .3s var(--n-bezier)",enterToProps:{transform:"scale(1)"},leaveToProps:{transform:"scale(0.9)"}}),f("icon",`
 position: absolute;
 left: 0;
 top: 0;
 align-items: center;
 justify-content: center;
 display: flex;
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 font-size: var(--n-icon-size);
 margin: var(--n-icon-margin);
 `),f("close",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 right: 0;
 top: 0;
 margin: var(--n-close-margin);
 `),q("show-icon",[P("alert-body",{paddingLeft:"calc(var(--n-icon-margin-left) + var(--n-icon-size) + var(--n-icon-margin-right))"})]),q("right-adjust",[P("alert-body",{paddingRight:"calc(var(--n-close-size) + var(--n-padding) + 2px)"})]),P("alert-body",`
 border-radius: var(--n-border-radius);
 transition: border-color .3s var(--n-bezier);
 `,[f("title",`
 transition: color .3s var(--n-bezier);
 font-size: 16px;
 line-height: 19px;
 font-weight: var(--n-title-font-weight);
 `,[N("& +",[f("content",{marginTop:"9px"})])]),f("content",{transition:"color .3s var(--n-bezier)",fontSize:"var(--n-font-size)"})]),f("icon",{transition:"color .3s var(--n-bezier)"})]),Qe=Q({name:"Alert",inheritAttrs:!1,props:Object.assign(Object.assign({},V.props),{title:String,showIcon:{type:Boolean,default:!0},type:{type:String,default:"default"},bordered:{type:Boolean,default:!0},closable:Boolean,onClose:Function,onAfterLeave:Function,onAfterHide:Function}),slots:Object,setup(n){const{mergedClsPrefixRef:a,mergedBorderedRef:h,inlineThemeDisabled:s,mergedRtlRef:v}=Y(n),i=V("Alert","-alert",qe,ue,n,a),b=ve("Alert",v,a),d=L(()=>{const{common:{cubicBezierEaseInOut:t},self:e}=i.value,{fontSize:o,borderRadius:p,titleFontWeight:j,lineHeight:A,iconSize:M,iconMargin:r,iconMarginRtl:c,closeIconSize:m,closeBorderRadius:S,closeSize:w,closeMargin:B,closeMarginRtl:F,padding:E}=e,{type:x}=n,{left:W,right:D}=he(r);return{"--n-bezier":t,"--n-color":e[C("color",x)],"--n-close-icon-size":m,"--n-close-border-radius":S,"--n-close-color-hover":e[C("closeColorHover",x)],"--n-close-color-pressed":e[C("closeColorPressed",x)],"--n-close-icon-color":e[C("closeIconColor",x)],"--n-close-icon-color-hover":e[C("closeIconColorHover",x)],"--n-close-icon-color-pressed":e[C("closeIconColorPressed",x)],"--n-icon-color":e[C("iconColor",x)],"--n-border":e[C("border",x)],"--n-title-text-color":e[C("titleTextColor",x)],"--n-content-text-color":e[C("contentTextColor",x)],"--n-line-height":A,"--n-border-radius":p,"--n-font-size":o,"--n-title-font-weight":j,"--n-icon-size":M,"--n-icon-margin":r,"--n-icon-margin-rtl":c,"--n-close-size":w,"--n-close-margin":B,"--n-close-margin-rtl":F,"--n-padding":E,"--n-icon-margin-left":W,"--n-icon-margin-right":D}}),y=s?ee("alert",L(()=>n.type[0]),d,n):void 0,z=O(!0);return{rtlEnabled:b,mergedClsPrefix:a,mergedBordered:h,visible:z,handleCloseClick:()=>{var t;Promise.resolve((t=n.onClose)===null||t===void 0?void 0:t.call(n)).then(e=>{e!==!1&&(z.value=!1)})},handleAfterLeave:()=>{(()=>{const{onAfterLeave:t,onAfterHide:e}=n;t&&t(),e&&e()})()},mergedTheme:i,cssVars:s?void 0:d,themeClass:y==null?void 0:y.themeClass,onRender:y==null?void 0:y.onRender}},render(){var n;return(n=this.onRender)===null||n===void 0||n.call(this),u(de,{onAfterLeave:this.handleAfterLeave},{default:()=>{const{mergedClsPrefix:a,$slots:h}=this,s={class:[`${a}-alert`,this.themeClass,this.closable&&`${a}-alert--closable`,this.showIcon&&`${a}-alert--show-icon`,!this.title&&this.closable&&`${a}-alert--right-adjust`,this.rtlEnabled&&`${a}-alert--rtl`],style:this.cssVars,role:"alert"};return this.visible?u("div",Object.assign({},te(this.$attrs,s)),this.closable&&u(ae,{clsPrefix:a,class:`${a}-alert__close`,onClick:this.handleCloseClick}),this.bordered&&u("div",{class:`${a}-alert__border`}),this.showIcon&&u("div",{class:`${a}-alert__icon`,"aria-hidden":"true"},K(h.icon,()=>[u(oe,{clsPrefix:a},{default:()=>{switch(this.type){case"success":return u(ce,null);case"info":return u(ie,null);case"warning":return u(se,null);case"error":return u(le,null);default:return null}}})])),u("div",{class:[`${a}-alert-body`,this.mergedBordered&&`${a}-alert-body--bordered`]},X(h.header,v=>{const i=v||this.title;return i?u("div",{class:`${a}-alert-body__title`},i):null}),h.default&&u("div",{class:`${a}-alert-body__content`},h))):null}})}}),Ue=pe("n-avatar-group"),Ze=P("avatar",`
 width: var(--n-merged-size);
 height: var(--n-merged-size);
 color: #FFF;
 font-size: var(--n-font-size);
 display: inline-flex;
 position: relative;
 overflow: hidden;
 text-align: center;
 border: var(--n-border);
 border-radius: var(--n-border-radius);
 --n-merged-color: var(--n-color);
 background-color: var(--n-merged-color);
 transition:
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
`,[me(N("&","--n-merged-color: var(--n-color-modal);")),ge(N("&","--n-merged-color: var(--n-color-popover);")),N("img",`
 width: 100%;
 height: 100%;
 `),f("text",`
 white-space: nowrap;
 display: inline-block;
 position: absolute;
 left: 50%;
 top: 50%;
 `),P("icon",`
 vertical-align: bottom;
 font-size: calc(var(--n-merged-size) - 6px);
 `),f("text","line-height: 1.25")]),Ge=Q({name:"Avatar",props:Object.assign(Object.assign({},V.props),{size:[String,Number],src:String,circle:{type:Boolean,default:void 0},objectFit:String,round:{type:Boolean,default:void 0},bordered:{type:Boolean,default:void 0},onError:Function,fallbackSrc:String,intersectionObserverOptions:Object,lazy:Boolean,onLoad:Function,renderPlaceholder:Function,renderFallback:Function,imgProps:Object,color:String}),slots:Object,setup(n){const{mergedClsPrefixRef:a,inlineThemeDisabled:h}=Y(n),s=O(!1);let v=null;const i=O(null),b=O(null),d=Z(Ue,null),y=L(()=>{const{size:r}=n;if(r)return r;const{size:c}=d||{};return c||"medium"}),z=V("Avatar","-avatar",Ze,be,n,a),t=Z(ye,null),e=L(()=>{if(d)return!0;const{round:r,circle:c}=n;return r!==void 0||c!==void 0?r||c:!!t&&t.roundRef.value}),o=L(()=>!!d||n.bordered||!1),p=L(()=>{const r=y.value,c=e.value,m=o.value,{color:S}=n,{self:{borderRadius:w,fontSize:B,color:F,border:E,colorModal:x,colorPopover:W},common:{cubicBezierEaseInOut:D}}=z.value;let U;return U=typeof r=="number"?`${r}px`:z.value.self[C("height",r)],{"--n-font-size":B,"--n-border":m?E:"none","--n-border-radius":c?"50%":w,"--n-color":S||F,"--n-color-modal":S||x,"--n-color-popover":S||W,"--n-bezier":D,"--n-merged-size":`var(--n-avatar-size-override, ${U})`}}),j=h?ee("avatar",L(()=>{const r=y.value,c=e.value,m=o.value,{color:S}=n;let w="";return r&&(w+=typeof r=="number"?`a${r}`:r[0]),c&&(w+="b"),m&&(w+="c"),S&&(w+=ze(S)),w}),p,n):void 0,A=O(!n.lazy);re(()=>{if(n.lazy&&n.intersectionObserverOptions){let r;const c=xe(()=>{r==null||r(),r=void 0,n.lazy&&(r=He(b.value,n.intersectionObserverOptions,A))});we(()=>{c(),r==null||r()})}}),ne(()=>{var r;return n.src||((r=n.imgProps)===null||r===void 0?void 0:r.src)},()=>{s.value=!1});const M=O(!n.lazy);return{textRef:i,selfRef:b,mergedRoundRef:e,mergedClsPrefix:a,fitTextTransform:()=>{const{value:r}=i;if(r&&(v===null||v!==r.innerHTML)){v=r.innerHTML;const{value:c}=b;if(c){const{offsetWidth:m,offsetHeight:S}=c,{offsetWidth:w,offsetHeight:B}=r,F=.9,E=Math.min(m/w*F,S/B*F,1);r.style.transform=`translateX(-50%) translateY(-50%) scale(${E})`}}},cssVars:h?void 0:p,themeClass:j==null?void 0:j.themeClass,onRender:j==null?void 0:j.onRender,hasLoadError:s,shouldStartLoading:A,loaded:M,mergedOnError:r=>{if(!A.value)return;s.value=!0;const{onError:c,imgProps:{onError:m}={}}=n;c==null||c(r),m==null||m(r)},mergedOnLoad:r=>{const{onLoad:c,imgProps:{onLoad:m}={}}=n;c==null||c(r),m==null||m(r),M.value=!0}}},render(){var n,a;const{$slots:h,src:s,mergedClsPrefix:v,lazy:i,onRender:b,loaded:d,hasLoadError:y,imgProps:z={}}=this;let t;b==null||b();const e=!d&&!y&&(this.renderPlaceholder?this.renderPlaceholder():(a=(n=this.$slots).placeholder)===null||a===void 0?void 0:a.call(n));return t=this.hasLoadError?this.renderFallback?this.renderFallback():K(h.fallback,()=>[u("img",{src:this.fallbackSrc,style:{objectFit:this.objectFit}})]):X(h.default,o=>{if(o)return u(fe,{onResize:this.fitTextTransform},{default:()=>u("span",{ref:"textRef",class:`${v}-avatar__text`},o)});if(s||z.src){const p=this.src||z.src;return u("img",Object.assign(Object.assign({},z),{loading:Me&&!this.intersectionObserverOptions&&i?"lazy":"eager",src:i&&this.intersectionObserverOptions?this.shouldStartLoading?p:void 0:p,"data-image-src":p,onLoad:this.mergedOnLoad,onError:this.mergedOnError,style:[z.style||"",{objectFit:this.objectFit},e?{height:"0",width:"0",visibility:"hidden",position:"absolute"}:""]}))}}),u("span",{ref:"selfRef",class:[`${v}-avatar`,this.themeClass],style:this.cssVars},t,i&&e)}}),Ke={style:{margin:"5px"}},Xe={key:1,style:{overflow:"auto"}},Ye=["src"],er={style:{display:"flex"}},rr={style:{margin:"5px",height:"20px"}},nr=["innerHTML"],tr={__name:"mcstatus",setup(n){const a=Ce(),h=Oe(),s=O(a.params.address||""),v=Se({mcserveraddr:""}),i=O(),b=O(),d=O(JSON.parse(localStorage.getItem("mcserveraddr_history")||"[]"));function y(){v.mcserveraddr="",i.value="",/:[0-9]{1,5}$/.test(s.value)||(s.value+=":25565",I("使用默认端口 25565",{theme:"auto",type:"info"})),/^(?!((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([0-9]{1,5})$)).*$/gm.test(s.value)?v.mcserveraddr=s.value+"  错误的地址 <host:port>":(Te(s.value).then(t=>{typeof t!="string"&&t.error===void 0?(i.value=t,h.push({name:"mcstatus",params:{address:s.value}}),function(e){const o=d.value.indexOf(e);o!==-1&&d.value.splice(o,1),d.value.unshift(e),d.value.length>10&&d.value.pop(),localStorage.setItem("mcserveraddr_history",JSON.stringify(d.value))}(s.value)):v.mcserveraddr=t}).catch(t=>{I(t+"<br>"+JSON.stringify(t.response.data),{theme:"auto",type:"error"})}),Ae(s.value).then(t=>{b.value=t}).catch(t=>{I(t,{theme:"auto",type:"error"})}))}const z=O(window.location.href);return ne(d,t=>{localStorage.setItem("mcserveraddr_history",JSON.stringify(t))}),ke((t,e,o)=>{s.value=t.params.address||"",o()}),_e(()=>{s.value&&y()}),re(()=>{const t=document.createElement("script");var e;t.type="text/javascript",t.charset="utf-8",t.src="https://widget.tsarvar.com/load.js?v=2",document.head.appendChild(t),e="TsarvarWidgetQueue",(window[e]||(window[e]=[])).push({element:'*[data-tsarvarServerId="483478"]',serverId:483478,serverIp:"49.234.20.77",serverPort:25565,color:"#18181c",blackMode:!0})}),(t,e)=>($(),J(g(Fe),{ref:"mc",title:"Mincraft Server Status",style:{"min-width":"300px",width:"100%","max-width":"800px",overflow:"auto"}},{default:_(()=>[k(g(Ne),{placeholder:"host:port",value:s.value,"onUpdate:value":e[0]||(e[0]=o=>s.value=o),clearable:"",autosize:"",style:{width:"80%",margin:"5px"}},null,8,["value"]),k(g($e),{type:"primary",style:{margin:"5px"},onClick:y},{default:_(()=>e[4]||(e[4]=[T("查询")])),_:1}),l("div",Ke,[k(g(Be),{value:d.value,"onUpdate:value":e[1]||(e[1]=o=>d.value=o),onClick:e[2]||(e[2]=o=>s.value=o.srcElement.innerText)},null,8,["value"])]),e[12]||(e[12]=l("br",null,null,-1)),v.mcserveraddr?($(),J(g(Qe),{key:0,"show-icon":!1,type:"error",closable:""},{default:_(()=>[T(R(v.mcserveraddr),1)]),_:1})):Re("",!0),!v.mcserveraddr&&i.value?($(),H("span",Xe,[k(g(G),{style:{margin:"5px"}},{default:_(()=>{var o,p;return[T("Ping to the server :"+R(((o=b.value)==null?void 0:o.time)||((p=b.value)==null?void 0:p.error)),1)]}),_:1}),k(g(Je),{bordered:!1},{default:_(()=>[l("tbody",null,[l("tr",null,[e[5]||(e[5]=l("td",null,"host",-1)),l("td",null,[k(g(G),{type:"success"},{default:_(()=>[T(R(s.value),1)]),_:1}),k(g(Pe),{onClick:e[3]||(e[3]=o=>(async p=>{try{await navigator.clipboard.writeText(p),I(`已复制到剪贴板！路径: ${p}`,{theme:"auto",type:"success"})}catch{I("复制失败，请手动复制。",{theme:"auto",type:"error"})}})(z.value)),title:"点击复制",style:{"margin-left":"5px",cursor:"pointer"}},{default:_(()=>[k(g(De))]),_:1})])]),l("tr",null,[e[6]||(e[6]=l("td",null,"version",-1)),l("td",null,R(i.value.version.name),1)]),l("tr",null,[e[7]||(e[7]=l("td",null,"protocol",-1)),l("td",null,R(i.value.version.protocol),1)]),l("tr",null,[e[8]||(e[8]=l("td",null,"icon",-1)),l("td",null,[l("img",{src:i.value.icon,alt:""},null,8,Ye)])]),l("tr",null,[e[10]||(e[10]=l("td",null,"players",-1)),l("td",null,[T(R(i.value.players.online)+"/"+R(i.value.players.max)+" ",1),e[9]||(e[9]=l("br",null,null,-1)),($(!0),H(je,null,Le(i.value.players.sample,o=>($(),H("p",null,[k(g(Ve),{placement:"top-start",trigger:"hover"},{trigger:_(()=>[l("p",er,[k(g(Ge),{size:"small",src:"https://crafatar.com/avatars/"+o.uuid},null,8,["src"]),l("span",rr,R(o.name),1)])]),default:_(()=>[T(" "+R(o.uuid),1)]),_:2},1024)]))),256))])]),l("tr",null,[e[11]||(e[11]=l("td",null,"motd",-1)),l("td",{innerHTML:i.value.motd.html},null,8,nr)])])]),_:1})])):($(),J(g(Ie),{key:2,text:"",repeat:2}))]),_:1},512))}},hr={__name:"mc",setup:n=>(a,h)=>($(),J(tr))};export{hr as default};
