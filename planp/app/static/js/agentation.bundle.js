(()=>{var cp=Object.create;var Jf=Object.defineProperty;var up=Object.getOwnPropertyDescriptor;var dp=Object.getOwnPropertyNames;var _p=Object.getPrototypeOf,fp=Object.prototype.hasOwnProperty;var Sl=(e,t)=>()=>(t||e((t={exports:{}}).exports,t),t.exports);var hp=(e,t,n,l)=>{if(t&&typeof t=="object"||typeof t=="function")for(let o of dp(t))!fp.call(e,o)&&o!==n&&Jf(e,o,{get:()=>t[o],enumerable:!(l=up(t,o))||l.enumerable});return e};var wt=(e,t,n)=>(n=e!=null?cp(_p(e)):{},hp(t||!e||!e.__esModule?Jf(n,"default",{value:e,enumerable:!0}):n,e));var c0=Sl(ze=>{"use strict";var yu=Symbol.for("react.transitional.element"),mp=Symbol.for("react.portal"),gp=Symbol.for("react.fragment"),yp=Symbol.for("react.strict_mode"),pp=Symbol.for("react.profiler"),bp=Symbol.for("react.consumer"),xp=Symbol.for("react.context"),vp=Symbol.for("react.forward_ref"),wp=Symbol.for("react.suspense"),kp=Symbol.for("react.memo"),l0=Symbol.for("react.lazy"),Sp=Symbol.for("react.activity"),Pf=Symbol.iterator;function Cp(e){return e===null||typeof e!="object"?null:(e=Pf&&e[Pf]||e["@@iterator"],typeof e=="function"?e:null)}var o0={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},a0=Object.assign,i0={};function Ta(e,t,n){this.props=e,this.context=t,this.refs=i0,this.updater=n||o0}Ta.prototype.isReactComponent={};Ta.prototype.setState=function(e,t){if(typeof e!="object"&&typeof e!="function"&&e!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")};Ta.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")};function s0(){}s0.prototype=Ta.prototype;function pu(e,t,n){this.props=e,this.context=t,this.refs=i0,this.updater=n||o0}var bu=pu.prototype=new s0;bu.constructor=pu;a0(bu,Ta.prototype);bu.isPureReactComponent=!0;var e0=Array.isArray;function gu(){}var St={H:null,A:null,T:null,S:null},r0=Object.prototype.hasOwnProperty;function xu(e,t,n){var l=n.ref;return{$$typeof:yu,type:e,key:t,ref:l!==void 0?l:null,props:n}}function Mp(e,t){return xu(e.type,t,e.props)}function vu(e){return typeof e=="object"&&e!==null&&e.$$typeof===yu}function Ep(e){var t={"=":"=0",":":"=2"};return"$"+e.replace(/[=:]/g,function(n){return t[n]})}var t0=/\/+/g;function mu(e,t){return typeof e=="object"&&e!==null&&e.key!=null?Ep(""+e.key):t.toString(36)}function Tp(e){switch(e.status){case"fulfilled":return e.value;case"rejected":throw e.reason;default:switch(typeof e.status=="string"?e.then(gu,gu):(e.status="pending",e.then(function(t){e.status==="pending"&&(e.status="fulfilled",e.value=t)},function(t){e.status==="pending"&&(e.status="rejected",e.reason=t)})),e.status){case"fulfilled":return e.value;case"rejected":throw e.reason}}throw e}function Ea(e,t,n,l,o){var a=typeof e;(a==="undefined"||a==="boolean")&&(e=null);var i=!1;if(e===null)i=!0;else switch(a){case"bigint":case"string":case"number":i=!0;break;case"object":switch(e.$$typeof){case yu:case mp:i=!0;break;case l0:return i=e._init,Ea(i(e._payload),t,n,l,o)}}if(i)return o=o(e),i=l===""?"."+mu(e,0):l,e0(o)?(n="",i!=null&&(n=i.replace(t0,"$&/")+"/"),Ea(o,t,n,"",function(p){return p})):o!=null&&(vu(o)&&(o=Mp(o,n+(o.key==null||e&&e.key===o.key?"":(""+o.key).replace(t0,"$&/")+"/")+i)),t.push(o)),1;i=0;var s=l===""?".":l+":";if(e0(e))for(var r=0;r<e.length;r++)l=e[r],a=s+mu(l,r),i+=Ea(l,t,n,a,o);else if(r=Cp(e),typeof r=="function")for(e=r.call(e),r=0;!(l=e.next()).done;)l=l.value,a=s+mu(l,r++),i+=Ea(l,t,n,a,o);else if(a==="object"){if(typeof e.then=="function")return Ea(Tp(e),t,n,l,o);throw t=String(e),Error("Objects are not valid as a React child (found: "+(t==="[object Object]"?"object with keys {"+Object.keys(e).join(", ")+"}":t)+"). If you meant to render a collection of children, use an array instead.")}return i}function ir(e,t,n){if(e==null)return e;var l=[],o=0;return Ea(e,l,"","",function(a){return t.call(n,a,o++)}),l}function Dp(e){if(e._status===-1){var t=e._result;t=t(),t.then(function(n){(e._status===0||e._status===-1)&&(e._status=1,e._result=n)},function(n){(e._status===0||e._status===-1)&&(e._status=2,e._result=n)}),e._status===-1&&(e._status=0,e._result=t)}if(e._status===1)return e._result.default;throw e._result}var n0=typeof reportError=="function"?reportError:function(e){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof e=="object"&&e!==null&&typeof e.message=="string"?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",e);return}console.error(e)},Np={map:ir,forEach:function(e,t,n){ir(e,function(){t.apply(this,arguments)},n)},count:function(e){var t=0;return ir(e,function(){t++}),t},toArray:function(e){return ir(e,function(t){return t})||[]},only:function(e){if(!vu(e))throw Error("React.Children.only expected to receive a single React element child.");return e}};ze.Activity=Sp;ze.Children=Np;ze.Component=Ta;ze.Fragment=gp;ze.Profiler=pp;ze.PureComponent=pu;ze.StrictMode=yp;ze.Suspense=wp;ze.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=St;ze.__COMPILER_RUNTIME={__proto__:null,c:function(e){return St.H.useMemoCache(e)}};ze.cache=function(e){return function(){return e.apply(null,arguments)}};ze.cacheSignal=function(){return null};ze.cloneElement=function(e,t,n){if(e==null)throw Error("The argument must be a React element, but you passed "+e+".");var l=a0({},e.props),o=e.key;if(t!=null)for(a in t.key!==void 0&&(o=""+t.key),t)!r0.call(t,a)||a==="key"||a==="__self"||a==="__source"||a==="ref"&&t.ref===void 0||(l[a]=t[a]);var a=arguments.length-2;if(a===1)l.children=n;else if(1<a){for(var i=Array(a),s=0;s<a;s++)i[s]=arguments[s+2];l.children=i}return xu(e.type,o,l)};ze.createContext=function(e){return e={$$typeof:xp,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null},e.Provider=e,e.Consumer={$$typeof:bp,_context:e},e};ze.createElement=function(e,t,n){var l,o={},a=null;if(t!=null)for(l in t.key!==void 0&&(a=""+t.key),t)r0.call(t,l)&&l!=="key"&&l!=="__self"&&l!=="__source"&&(o[l]=t[l]);var i=arguments.length-2;if(i===1)o.children=n;else if(1<i){for(var s=Array(i),r=0;r<i;r++)s[r]=arguments[r+2];o.children=s}if(e&&e.defaultProps)for(l in i=e.defaultProps,i)o[l]===void 0&&(o[l]=i[l]);return xu(e,a,o)};ze.createRef=function(){return{current:null}};ze.forwardRef=function(e){return{$$typeof:vp,render:e}};ze.isValidElement=vu;ze.lazy=function(e){return{$$typeof:l0,_payload:{_status:-1,_result:e},_init:Dp}};ze.memo=function(e,t){return{$$typeof:kp,type:e,compare:t===void 0?null:t}};ze.startTransition=function(e){var t=St.T,n={};St.T=n;try{var l=e(),o=St.S;o!==null&&o(n,l),typeof l=="object"&&l!==null&&typeof l.then=="function"&&l.then(gu,n0)}catch(a){n0(a)}finally{t!==null&&n.types!==null&&(t.types=n.types),St.T=t}};ze.unstable_useCacheRefresh=function(){return St.H.useCacheRefresh()};ze.use=function(e){return St.H.use(e)};ze.useActionState=function(e,t,n){return St.H.useActionState(e,t,n)};ze.useCallback=function(e,t){return St.H.useCallback(e,t)};ze.useContext=function(e){return St.H.useContext(e)};ze.useDebugValue=function(){};ze.useDeferredValue=function(e,t){return St.H.useDeferredValue(e,t)};ze.useEffect=function(e,t){return St.H.useEffect(e,t)};ze.useEffectEvent=function(e){return St.H.useEffectEvent(e)};ze.useId=function(){return St.H.useId()};ze.useImperativeHandle=function(e,t,n){return St.H.useImperativeHandle(e,t,n)};ze.useInsertionEffect=function(e,t){return St.H.useInsertionEffect(e,t)};ze.useLayoutEffect=function(e,t){return St.H.useLayoutEffect(e,t)};ze.useMemo=function(e,t){return St.H.useMemo(e,t)};ze.useOptimistic=function(e,t){return St.H.useOptimistic(e,t)};ze.useReducer=function(e,t,n){return St.H.useReducer(e,t,n)};ze.useRef=function(e){return St.H.useRef(e)};ze.useState=function(e){return St.H.useState(e)};ze.useSyncExternalStore=function(e,t,n){return St.H.useSyncExternalStore(e,t,n)};ze.useTransition=function(){return St.H.useTransition()};ze.version="19.2.4"});var Vn=Sl((B4,u0)=>{"use strict";u0.exports=c0()});var x0=Sl(Tt=>{"use strict";function Cu(e,t){var n=e.length;e.push(t);e:for(;0<n;){var l=n-1>>>1,o=e[l];if(0<sr(o,t))e[l]=t,e[n]=o,n=l;else break e}}function Cl(e){return e.length===0?null:e[0]}function cr(e){if(e.length===0)return null;var t=e[0],n=e.pop();if(n!==t){e[0]=n;e:for(var l=0,o=e.length,a=o>>>1;l<a;){var i=2*(l+1)-1,s=e[i],r=i+1,p=e[r];if(0>sr(s,n))r<o&&0>sr(p,s)?(e[l]=p,e[r]=n,l=r):(e[l]=s,e[i]=n,l=i);else if(r<o&&0>sr(p,n))e[l]=p,e[r]=n,l=r;else break e}}return t}function sr(e,t){var n=e.sortIndex-t.sortIndex;return n!==0?n:e.id-t.id}Tt.unstable_now=void 0;typeof performance=="object"&&typeof performance.now=="function"?(d0=performance,Tt.unstable_now=function(){return d0.now()}):(wu=Date,_0=wu.now(),Tt.unstable_now=function(){return wu.now()-_0});var d0,wu,_0,Hl=[],co=[],zp=1,Zn=null,fn=3,Mu=!1,Hi=!1,Ui=!1,Eu=!1,m0=typeof setTimeout=="function"?setTimeout:null,g0=typeof clearTimeout=="function"?clearTimeout:null,f0=typeof setImmediate<"u"?setImmediate:null;function rr(e){for(var t=Cl(co);t!==null;){if(t.callback===null)cr(co);else if(t.startTime<=e)cr(co),t.sortIndex=t.expirationTime,Cu(Hl,t);else break;t=Cl(co)}}function Tu(e){if(Ui=!1,rr(e),!Hi)if(Cl(Hl)!==null)Hi=!0,Na||(Na=!0,Da());else{var t=Cl(co);t!==null&&Du(Tu,t.startTime-e)}}var Na=!1,Yi=-1,y0=5,p0=-1;function b0(){return Eu?!0:!(Tt.unstable_now()-p0<y0)}function ku(){if(Eu=!1,Na){var e=Tt.unstable_now();p0=e;var t=!0;try{e:{Hi=!1,Ui&&(Ui=!1,g0(Yi),Yi=-1),Mu=!0;var n=fn;try{t:{for(rr(e),Zn=Cl(Hl);Zn!==null&&!(Zn.expirationTime>e&&b0());){var l=Zn.callback;if(typeof l=="function"){Zn.callback=null,fn=Zn.priorityLevel;var o=l(Zn.expirationTime<=e);if(e=Tt.unstable_now(),typeof o=="function"){Zn.callback=o,rr(e),t=!0;break t}Zn===Cl(Hl)&&cr(Hl),rr(e)}else cr(Hl);Zn=Cl(Hl)}if(Zn!==null)t=!0;else{var a=Cl(co);a!==null&&Du(Tu,a.startTime-e),t=!1}}break e}finally{Zn=null,fn=n,Mu=!1}t=void 0}}finally{t?Da():Na=!1}}}var Da;typeof f0=="function"?Da=function(){f0(ku)}:typeof MessageChannel<"u"?(Su=new MessageChannel,h0=Su.port2,Su.port1.onmessage=ku,Da=function(){h0.postMessage(null)}):Da=function(){m0(ku,0)};var Su,h0;function Du(e,t){Yi=m0(function(){e(Tt.unstable_now())},t)}Tt.unstable_IdlePriority=5;Tt.unstable_ImmediatePriority=1;Tt.unstable_LowPriority=4;Tt.unstable_NormalPriority=3;Tt.unstable_Profiling=null;Tt.unstable_UserBlockingPriority=2;Tt.unstable_cancelCallback=function(e){e.callback=null};Tt.unstable_forceFrameRate=function(e){0>e||125<e?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):y0=0<e?Math.floor(1e3/e):5};Tt.unstable_getCurrentPriorityLevel=function(){return fn};Tt.unstable_next=function(e){switch(fn){case 1:case 2:case 3:var t=3;break;default:t=fn}var n=fn;fn=t;try{return e()}finally{fn=n}};Tt.unstable_requestPaint=function(){Eu=!0};Tt.unstable_runWithPriority=function(e,t){switch(e){case 1:case 2:case 3:case 4:case 5:break;default:e=3}var n=fn;fn=e;try{return t()}finally{fn=n}};Tt.unstable_scheduleCallback=function(e,t,n){var l=Tt.unstable_now();switch(typeof n=="object"&&n!==null?(n=n.delay,n=typeof n=="number"&&0<n?l+n:l):n=l,e){case 1:var o=-1;break;case 2:o=250;break;case 5:o=1073741823;break;case 4:o=1e4;break;default:o=5e3}return o=n+o,e={id:zp++,callback:t,priorityLevel:e,startTime:n,expirationTime:o,sortIndex:-1},n>l?(e.sortIndex=n,Cu(co,e),Cl(Hl)===null&&e===Cl(co)&&(Ui?(g0(Yi),Yi=-1):Ui=!0,Du(Tu,n-l))):(e.sortIndex=o,Cu(Hl,e),Hi||Mu||(Hi=!0,Na||(Na=!0,Da()))),e};Tt.unstable_shouldYield=b0;Tt.unstable_wrapCallback=function(e){var t=fn;return function(){var n=fn;fn=t;try{return e.apply(this,arguments)}finally{fn=n}}}});var w0=Sl(($4,v0)=>{"use strict";v0.exports=x0()});var S0=Sl(gn=>{"use strict";var Ap=Vn();function k0(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var n=2;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function uo(){}var mn={d:{f:uo,r:function(){throw Error(k0(522))},D:uo,C:uo,L:uo,m:uo,X:uo,S:uo,M:uo},p:0,findDOMNode:null},Lp=Symbol.for("react.portal");function Rp(e,t,n){var l=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:Lp,key:l==null?null:""+l,children:e,containerInfo:t,implementation:n}}var ji=Ap.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function ur(e,t){if(e==="font")return"";if(typeof t=="string")return t==="use-credentials"?t:""}gn.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=mn;gn.createPortal=function(e,t){var n=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)throw Error(k0(299));return Rp(e,t,null,n)};gn.flushSync=function(e){var t=ji.T,n=mn.p;try{if(ji.T=null,mn.p=2,e)return e()}finally{ji.T=t,mn.p=n,mn.d.f()}};gn.preconnect=function(e,t){typeof e=="string"&&(t?(t=t.crossOrigin,t=typeof t=="string"?t==="use-credentials"?t:"":void 0):t=null,mn.d.C(e,t))};gn.prefetchDNS=function(e){typeof e=="string"&&mn.d.D(e)};gn.preinit=function(e,t){if(typeof e=="string"&&t&&typeof t.as=="string"){var n=t.as,l=ur(n,t.crossOrigin),o=typeof t.integrity=="string"?t.integrity:void 0,a=typeof t.fetchPriority=="string"?t.fetchPriority:void 0;n==="style"?mn.d.S(e,typeof t.precedence=="string"?t.precedence:void 0,{crossOrigin:l,integrity:o,fetchPriority:a}):n==="script"&&mn.d.X(e,{crossOrigin:l,integrity:o,fetchPriority:a,nonce:typeof t.nonce=="string"?t.nonce:void 0})}};gn.preinitModule=function(e,t){if(typeof e=="string")if(typeof t=="object"&&t!==null){if(t.as==null||t.as==="script"){var n=ur(t.as,t.crossOrigin);mn.d.M(e,{crossOrigin:n,integrity:typeof t.integrity=="string"?t.integrity:void 0,nonce:typeof t.nonce=="string"?t.nonce:void 0})}}else t==null&&mn.d.M(e)};gn.preload=function(e,t){if(typeof e=="string"&&typeof t=="object"&&t!==null&&typeof t.as=="string"){var n=t.as,l=ur(n,t.crossOrigin);mn.d.L(e,n,{crossOrigin:l,integrity:typeof t.integrity=="string"?t.integrity:void 0,nonce:typeof t.nonce=="string"?t.nonce:void 0,type:typeof t.type=="string"?t.type:void 0,fetchPriority:typeof t.fetchPriority=="string"?t.fetchPriority:void 0,referrerPolicy:typeof t.referrerPolicy=="string"?t.referrerPolicy:void 0,imageSrcSet:typeof t.imageSrcSet=="string"?t.imageSrcSet:void 0,imageSizes:typeof t.imageSizes=="string"?t.imageSizes:void 0,media:typeof t.media=="string"?t.media:void 0})}};gn.preloadModule=function(e,t){if(typeof e=="string")if(t){var n=ur(t.as,t.crossOrigin);mn.d.m(e,{as:typeof t.as=="string"&&t.as!=="script"?t.as:void 0,crossOrigin:n,integrity:typeof t.integrity=="string"?t.integrity:void 0})}else mn.d.m(e)};gn.requestFormReset=function(e){mn.d.r(e)};gn.unstable_batchedUpdates=function(e,t){return e(t)};gn.useFormState=function(e,t,n){return ji.H.useFormState(e,t,n)};gn.useFormStatus=function(){return ji.H.useHostTransitionStatus()};gn.version="19.2.4"});var dr=Sl((U4,M0)=>{"use strict";function C0(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(C0)}catch(e){console.error(e)}}C0(),M0.exports=S0()});var Hg=Sl(Oc=>{"use strict";var en=w0(),Jh=Vn(),Bp=dr();function O(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var n=2;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function Ph(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11)}function Es(e){var t=e,n=e;if(e.alternate)for(;t.return;)t=t.return;else{e=t;do t=e,(t.flags&4098)!==0&&(n=t.return),e=t.return;while(e)}return t.tag===3?n:null}function e1(e){if(e.tag===13){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function t1(e){if(e.tag===31){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function E0(e){if(Es(e)!==e)throw Error(O(188))}function Op(e){var t=e.alternate;if(!t){if(t=Es(e),t===null)throw Error(O(188));return t!==e?null:e}for(var n=e,l=t;;){var o=n.return;if(o===null)break;var a=o.alternate;if(a===null){if(l=o.return,l!==null){n=l;continue}break}if(o.child===a.child){for(a=o.child;a;){if(a===n)return E0(o),e;if(a===l)return E0(o),t;a=a.sibling}throw Error(O(188))}if(n.return!==l.return)n=o,l=a;else{for(var i=!1,s=o.child;s;){if(s===n){i=!0,n=o,l=a;break}if(s===l){i=!0,l=o,n=a;break}s=s.sibling}if(!i){for(s=a.child;s;){if(s===n){i=!0,n=a,l=o;break}if(s===l){i=!0,l=a,n=o;break}s=s.sibling}if(!i)throw Error(O(189))}}if(n.alternate!==l)throw Error(O(190))}if(n.tag!==3)throw Error(O(188));return n.stateNode.current===n?e:t}function n1(e){var t=e.tag;if(t===5||t===26||t===27||t===6)return e;for(e=e.child;e!==null;){if(t=n1(e),t!==null)return t;e=e.sibling}return null}var Et=Object.assign,$p=Symbol.for("react.element"),_r=Symbol.for("react.transitional.element"),Zi=Symbol.for("react.portal"),Oa=Symbol.for("react.fragment"),l1=Symbol.for("react.strict_mode"),cd=Symbol.for("react.profiler"),o1=Symbol.for("react.consumer"),Wl=Symbol.for("react.context"),o_=Symbol.for("react.forward_ref"),ud=Symbol.for("react.suspense"),dd=Symbol.for("react.suspense_list"),a_=Symbol.for("react.memo"),_o=Symbol.for("react.lazy"),_d=Symbol.for("react.activity"),Hp=Symbol.for("react.memo_cache_sentinel"),T0=Symbol.iterator;function Xi(e){return e===null||typeof e!="object"?null:(e=T0&&e[T0]||e["@@iterator"],typeof e=="function"?e:null)}var Up=Symbol.for("react.client.reference");function fd(e){if(e==null)return null;if(typeof e=="function")return e.$$typeof===Up?null:e.displayName||e.name||null;if(typeof e=="string")return e;switch(e){case Oa:return"Fragment";case cd:return"Profiler";case l1:return"StrictMode";case ud:return"Suspense";case dd:return"SuspenseList";case _d:return"Activity"}if(typeof e=="object")switch(e.$$typeof){case Zi:return"Portal";case Wl:return e.displayName||"Context";case o1:return(e._context.displayName||"Context")+".Consumer";case o_:var t=e.render;return e=e.displayName,e||(e=t.displayName||t.name||"",e=e!==""?"ForwardRef("+e+")":"ForwardRef"),e;case a_:return t=e.displayName||null,t!==null?t:fd(e.type)||"Memo";case _o:t=e._payload,e=e._init;try{return fd(e(t))}catch{}}return null}var Ki=Array.isArray,we=Jh.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,ot=Bp.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,Jo={pending:!1,data:null,method:null,action:null},hd=[],$a=-1;function Nl(e){return{current:e}}function on(e){0>$a||(e.current=hd[$a],hd[$a]=null,$a--)}function kt(e,t){$a++,hd[$a]=e.current,e.current=t}var Dl=Nl(null),fs=Nl(null),ko=Nl(null),Qr=Nl(null);function Wr(e,t){switch(kt(ko,t),kt(fs,e),kt(Dl,null),t.nodeType){case 9:case 11:e=(e=t.documentElement)&&(e=e.namespaceURI)?Bh(e):0;break;default:if(e=t.tagName,t=t.namespaceURI)t=Bh(t),e=Sg(t,e);else switch(e){case"svg":e=1;break;case"math":e=2;break;default:e=0}}on(Dl),kt(Dl,e)}function ti(){on(Dl),on(fs),on(ko)}function md(e){e.memoizedState!==null&&kt(Qr,e);var t=Dl.current,n=Sg(t,e.type);t!==n&&(kt(fs,e),kt(Dl,n))}function Gr(e){fs.current===e&&(on(Dl),on(fs)),Qr.current===e&&(on(Qr),Ss._currentValue=Jo)}var Nu,D0;function Vo(e){if(Nu===void 0)try{throw Error()}catch(n){var t=n.stack.trim().match(/\n( *(at )?)/);Nu=t&&t[1]||"",D0=-1<n.stack.indexOf(`
    at`)?" (<anonymous>)":-1<n.stack.indexOf("@")?"@unknown:0:0":""}return`
`+Nu+e+D0}var zu=!1;function Au(e,t){if(!e||zu)return"";zu=!0;var n=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var l={DetermineComponentFrameRoot:function(){try{if(t){var b=function(){throw Error()};if(Object.defineProperty(b.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(b,[])}catch(w){var _=w}Reflect.construct(e,[],b)}else{try{b.call()}catch(w){_=w}e.call(b.prototype)}}else{try{throw Error()}catch(w){_=w}(b=e())&&typeof b.catch=="function"&&b.catch(function(){})}}catch(w){if(w&&_&&typeof w.stack=="string")return[w.stack,_.stack]}return[null,null]}};l.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var o=Object.getOwnPropertyDescriptor(l.DetermineComponentFrameRoot,"name");o&&o.configurable&&Object.defineProperty(l.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var a=l.DetermineComponentFrameRoot(),i=a[0],s=a[1];if(i&&s){var r=i.split(`
`),p=s.split(`
`);for(o=l=0;l<r.length&&!r[l].includes("DetermineComponentFrameRoot");)l++;for(;o<p.length&&!p[o].includes("DetermineComponentFrameRoot");)o++;if(l===r.length||o===p.length)for(l=r.length-1,o=p.length-1;1<=l&&0<=o&&r[l]!==p[o];)o--;for(;1<=l&&0<=o;l--,o--)if(r[l]!==p[o]){if(l!==1||o!==1)do if(l--,o--,0>o||r[l]!==p[o]){var f=`
`+r[l].replace(" at new "," at ");return e.displayName&&f.includes("<anonymous>")&&(f=f.replace("<anonymous>",e.displayName)),f}while(1<=l&&0<=o);break}}}finally{zu=!1,Error.prepareStackTrace=n}return(n=e?e.displayName||e.name:"")?Vo(n):""}function Yp(e,t){switch(e.tag){case 26:case 27:case 5:return Vo(e.type);case 16:return Vo("Lazy");case 13:return e.child!==t&&t!==null?Vo("Suspense Fallback"):Vo("Suspense");case 19:return Vo("SuspenseList");case 0:case 15:return Au(e.type,!1);case 11:return Au(e.type.render,!1);case 1:return Au(e.type,!0);case 31:return Vo("Activity");default:return""}}function N0(e){try{var t="",n=null;do t+=Yp(e,n),n=e,e=e.return;while(e);return t}catch(l){return`
Error generating stack: `+l.message+`
`+l.stack}}var gd=Object.prototype.hasOwnProperty,i_=en.unstable_scheduleCallback,Lu=en.unstable_cancelCallback,jp=en.unstable_shouldYield,Xp=en.unstable_requestPaint,On=en.unstable_now,Ip=en.unstable_getCurrentPriorityLevel,a1=en.unstable_ImmediatePriority,i1=en.unstable_UserBlockingPriority,Vr=en.unstable_NormalPriority,qp=en.unstable_LowPriority,s1=en.unstable_IdlePriority,Qp=en.log,Wp=en.unstable_setDisableYieldValue,Ts=null,$n=null;function po(e){if(typeof Qp=="function"&&Wp(e),$n&&typeof $n.setStrictMode=="function")try{$n.setStrictMode(Ts,e)}catch{}}var Hn=Math.clz32?Math.clz32:Zp,Gp=Math.log,Vp=Math.LN2;function Zp(e){return e>>>=0,e===0?32:31-(Gp(e)/Vp|0)|0}var fr=256,hr=262144,mr=4194304;function Zo(e){var t=e&42;if(t!==0)return t;switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return e&261888;case 262144:case 524288:case 1048576:case 2097152:return e&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return e&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return e}}function xc(e,t,n){var l=e.pendingLanes;if(l===0)return 0;var o=0,a=e.suspendedLanes,i=e.pingedLanes;e=e.warmLanes;var s=l&134217727;return s!==0?(l=s&~a,l!==0?o=Zo(l):(i&=s,i!==0?o=Zo(i):n||(n=s&~e,n!==0&&(o=Zo(n))))):(s=l&~a,s!==0?o=Zo(s):i!==0?o=Zo(i):n||(n=l&~e,n!==0&&(o=Zo(n)))),o===0?0:t!==0&&t!==o&&(t&a)===0&&(a=o&-o,n=t&-t,a>=n||a===32&&(n&4194048)!==0)?t:o}function Ds(e,t){return(e.pendingLanes&~(e.suspendedLanes&~e.pingedLanes)&t)===0}function Kp(e,t){switch(e){case 1:case 2:case 4:case 8:case 64:return t+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function r1(){var e=mr;return mr<<=1,(mr&62914560)===0&&(mr=4194304),e}function Ru(e){for(var t=[],n=0;31>n;n++)t.push(e);return t}function Ns(e,t){e.pendingLanes|=t,t!==268435456&&(e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0)}function Fp(e,t,n,l,o,a){var i=e.pendingLanes;e.pendingLanes=n,e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0,e.expiredLanes&=n,e.entangledLanes&=n,e.errorRecoveryDisabledLanes&=n,e.shellSuspendCounter=0;var s=e.entanglements,r=e.expirationTimes,p=e.hiddenUpdates;for(n=i&~n;0<n;){var f=31-Hn(n),b=1<<f;s[f]=0,r[f]=-1;var _=p[f];if(_!==null)for(p[f]=null,f=0;f<_.length;f++){var w=_[f];w!==null&&(w.lane&=-536870913)}n&=~b}l!==0&&c1(e,l,0),a!==0&&o===0&&e.tag!==0&&(e.suspendedLanes|=a&~(i&~t))}function c1(e,t,n){e.pendingLanes|=t,e.suspendedLanes&=~t;var l=31-Hn(t);e.entangledLanes|=t,e.entanglements[l]=e.entanglements[l]|1073741824|n&261930}function u1(e,t){var n=e.entangledLanes|=t;for(e=e.entanglements;n;){var l=31-Hn(n),o=1<<l;o&t|e[l]&t&&(e[l]|=t),n&=~o}}function d1(e,t){var n=t&-t;return n=(n&42)!==0?1:s_(n),(n&(e.suspendedLanes|t))!==0?0:n}function s_(e){switch(e){case 2:e=1;break;case 8:e=4;break;case 32:e=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:e=128;break;case 268435456:e=134217728;break;default:e=0}return e}function r_(e){return e&=-e,2<e?8<e?(e&134217727)!==0?32:268435456:8:2}function _1(){var e=ot.p;return e!==0?e:(e=window.event,e===void 0?32:Bg(e.type))}function z0(e,t){var n=ot.p;try{return ot.p=e,t()}finally{ot.p=n}}var Oo=Math.random().toString(36).slice(2),rn="__reactFiber$"+Oo,Dn="__reactProps$"+Oo,_i="__reactContainer$"+Oo,yd="__reactEvents$"+Oo,Jp="__reactListeners$"+Oo,Pp="__reactHandles$"+Oo,A0="__reactResources$"+Oo,zs="__reactMarker$"+Oo;function c_(e){delete e[rn],delete e[Dn],delete e[yd],delete e[Jp],delete e[Pp]}function Ha(e){var t=e[rn];if(t)return t;for(var n=e.parentNode;n;){if(t=n[_i]||n[rn]){if(n=t.alternate,t.child!==null||n!==null&&n.child!==null)for(e=Yh(e);e!==null;){if(n=e[rn])return n;e=Yh(e)}return t}e=n,n=e.parentNode}return null}function fi(e){if(e=e[rn]||e[_i]){var t=e.tag;if(t===5||t===6||t===13||t===31||t===26||t===27||t===3)return e}return null}function Fi(e){var t=e.tag;if(t===5||t===26||t===27||t===6)return e.stateNode;throw Error(O(33))}function Va(e){var t=e[A0];return t||(t=e[A0]={hoistableStyles:new Map,hoistableScripts:new Map}),t}function ln(e){e[zs]=!0}var f1=new Set,h1={};function ra(e,t){ni(e,t),ni(e+"Capture",t)}function ni(e,t){for(h1[e]=t,e=0;e<t.length;e++)f1.add(t[e])}var e5=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),L0={},R0={};function t5(e){return gd.call(R0,e)?!0:gd.call(L0,e)?!1:e5.test(e)?R0[e]=!0:(L0[e]=!0,!1)}function Nr(e,t,n){if(t5(t))if(n===null)e.removeAttribute(t);else{switch(typeof n){case"undefined":case"function":case"symbol":e.removeAttribute(t);return;case"boolean":var l=t.toLowerCase().slice(0,5);if(l!=="data-"&&l!=="aria-"){e.removeAttribute(t);return}}e.setAttribute(t,""+n)}}function gr(e,t,n){if(n===null)e.removeAttribute(t);else{switch(typeof n){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(t);return}e.setAttribute(t,""+n)}}function Ul(e,t,n,l){if(l===null)e.removeAttribute(n);else{switch(typeof l){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(n);return}e.setAttributeNS(t,n,""+l)}}function Fn(e){switch(typeof e){case"bigint":case"boolean":case"number":case"string":case"undefined":return e;case"object":return e;default:return""}}function m1(e){var t=e.type;return(e=e.nodeName)&&e.toLowerCase()==="input"&&(t==="checkbox"||t==="radio")}function n5(e,t,n){var l=Object.getOwnPropertyDescriptor(e.constructor.prototype,t);if(!e.hasOwnProperty(t)&&typeof l<"u"&&typeof l.get=="function"&&typeof l.set=="function"){var o=l.get,a=l.set;return Object.defineProperty(e,t,{configurable:!0,get:function(){return o.call(this)},set:function(i){n=""+i,a.call(this,i)}}),Object.defineProperty(e,t,{enumerable:l.enumerable}),{getValue:function(){return n},setValue:function(i){n=""+i},stopTracking:function(){e._valueTracker=null,delete e[t]}}}}function pd(e){if(!e._valueTracker){var t=m1(e)?"checked":"value";e._valueTracker=n5(e,t,""+e[t])}}function g1(e){if(!e)return!1;var t=e._valueTracker;if(!t)return!0;var n=t.getValue(),l="";return e&&(l=m1(e)?e.checked?"true":"false":e.value),e=l,e!==n?(t.setValue(e),!0):!1}function Zr(e){if(e=e||(typeof document<"u"?document:void 0),typeof e>"u")return null;try{return e.activeElement||e.body}catch{return e.body}}var l5=/[\n"\\]/g;function el(e){return e.replace(l5,function(t){return"\\"+t.charCodeAt(0).toString(16)+" "})}function bd(e,t,n,l,o,a,i,s){e.name="",i!=null&&typeof i!="function"&&typeof i!="symbol"&&typeof i!="boolean"?e.type=i:e.removeAttribute("type"),t!=null?i==="number"?(t===0&&e.value===""||e.value!=t)&&(e.value=""+Fn(t)):e.value!==""+Fn(t)&&(e.value=""+Fn(t)):i!=="submit"&&i!=="reset"||e.removeAttribute("value"),t!=null?xd(e,i,Fn(t)):n!=null?xd(e,i,Fn(n)):l!=null&&e.removeAttribute("value"),o==null&&a!=null&&(e.defaultChecked=!!a),o!=null&&(e.checked=o&&typeof o!="function"&&typeof o!="symbol"),s!=null&&typeof s!="function"&&typeof s!="symbol"&&typeof s!="boolean"?e.name=""+Fn(s):e.removeAttribute("name")}function y1(e,t,n,l,o,a,i,s){if(a!=null&&typeof a!="function"&&typeof a!="symbol"&&typeof a!="boolean"&&(e.type=a),t!=null||n!=null){if(!(a!=="submit"&&a!=="reset"||t!=null)){pd(e);return}n=n!=null?""+Fn(n):"",t=t!=null?""+Fn(t):n,s||t===e.value||(e.value=t),e.defaultValue=t}l=l??o,l=typeof l!="function"&&typeof l!="symbol"&&!!l,e.checked=s?e.checked:!!l,e.defaultChecked=!!l,i!=null&&typeof i!="function"&&typeof i!="symbol"&&typeof i!="boolean"&&(e.name=i),pd(e)}function xd(e,t,n){t==="number"&&Zr(e.ownerDocument)===e||e.defaultValue===""+n||(e.defaultValue=""+n)}function Za(e,t,n,l){if(e=e.options,t){t={};for(var o=0;o<n.length;o++)t["$"+n[o]]=!0;for(n=0;n<e.length;n++)o=t.hasOwnProperty("$"+e[n].value),e[n].selected!==o&&(e[n].selected=o),o&&l&&(e[n].defaultSelected=!0)}else{for(n=""+Fn(n),t=null,o=0;o<e.length;o++){if(e[o].value===n){e[o].selected=!0,l&&(e[o].defaultSelected=!0);return}t!==null||e[o].disabled||(t=e[o])}t!==null&&(t.selected=!0)}}function p1(e,t,n){if(t!=null&&(t=""+Fn(t),t!==e.value&&(e.value=t),n==null)){e.defaultValue!==t&&(e.defaultValue=t);return}e.defaultValue=n!=null?""+Fn(n):""}function b1(e,t,n,l){if(t==null){if(l!=null){if(n!=null)throw Error(O(92));if(Ki(l)){if(1<l.length)throw Error(O(93));l=l[0]}n=l}n==null&&(n=""),t=n}n=Fn(t),e.defaultValue=n,l=e.textContent,l===n&&l!==""&&l!==null&&(e.value=l),pd(e)}function li(e,t){if(t){var n=e.firstChild;if(n&&n===e.lastChild&&n.nodeType===3){n.nodeValue=t;return}}e.textContent=t}var o5=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function B0(e,t,n){var l=t.indexOf("--")===0;n==null||typeof n=="boolean"||n===""?l?e.setProperty(t,""):t==="float"?e.cssFloat="":e[t]="":l?e.setProperty(t,n):typeof n!="number"||n===0||o5.has(t)?t==="float"?e.cssFloat=n:e[t]=(""+n).trim():e[t]=n+"px"}function x1(e,t,n){if(t!=null&&typeof t!="object")throw Error(O(62));if(e=e.style,n!=null){for(var l in n)!n.hasOwnProperty(l)||t!=null&&t.hasOwnProperty(l)||(l.indexOf("--")===0?e.setProperty(l,""):l==="float"?e.cssFloat="":e[l]="");for(var o in t)l=t[o],t.hasOwnProperty(o)&&n[o]!==l&&B0(e,o,l)}else for(var a in t)t.hasOwnProperty(a)&&B0(e,a,t[a])}function u_(e){if(e.indexOf("-")===-1)return!1;switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var a5=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),i5=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function zr(e){return i5.test(""+e)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":e}function Gl(){}var vd=null;function d_(e){return e=e.target||e.srcElement||window,e.correspondingUseElement&&(e=e.correspondingUseElement),e.nodeType===3?e.parentNode:e}var Ua=null,Ka=null;function O0(e){var t=fi(e);if(t&&(e=t.stateNode)){var n=e[Dn]||null;e:switch(e=t.stateNode,t.type){case"input":if(bd(e,n.value,n.defaultValue,n.defaultValue,n.checked,n.defaultChecked,n.type,n.name),t=n.name,n.type==="radio"&&t!=null){for(n=e;n.parentNode;)n=n.parentNode;for(n=n.querySelectorAll('input[name="'+el(""+t)+'"][type="radio"]'),t=0;t<n.length;t++){var l=n[t];if(l!==e&&l.form===e.form){var o=l[Dn]||null;if(!o)throw Error(O(90));bd(l,o.value,o.defaultValue,o.defaultValue,o.checked,o.defaultChecked,o.type,o.name)}}for(t=0;t<n.length;t++)l=n[t],l.form===e.form&&g1(l)}break e;case"textarea":p1(e,n.value,n.defaultValue);break e;case"select":t=n.value,t!=null&&Za(e,!!n.multiple,t,!1)}}}var Bu=!1;function v1(e,t,n){if(Bu)return e(t,n);Bu=!0;try{var l=e(t);return l}finally{if(Bu=!1,(Ua!==null||Ka!==null)&&(Ac(),Ua&&(t=Ua,e=Ka,Ka=Ua=null,O0(t),e)))for(t=0;t<e.length;t++)O0(e[t])}}function hs(e,t){var n=e.stateNode;if(n===null)return null;var l=n[Dn]||null;if(l===null)return null;n=l[t];e:switch(t){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(l=!l.disabled)||(e=e.type,l=!(e==="button"||e==="input"||e==="select"||e==="textarea")),e=!l;break e;default:e=!1}if(e)return null;if(n&&typeof n!="function")throw Error(O(231,t,typeof n));return n}var Jl=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),wd=!1;if(Jl)try{za={},Object.defineProperty(za,"passive",{get:function(){wd=!0}}),window.addEventListener("test",za,za),window.removeEventListener("test",za,za)}catch{wd=!1}var za,bo=null,__=null,Ar=null;function w1(){if(Ar)return Ar;var e,t=__,n=t.length,l,o="value"in bo?bo.value:bo.textContent,a=o.length;for(e=0;e<n&&t[e]===o[e];e++);var i=n-e;for(l=1;l<=i&&t[n-l]===o[a-l];l++);return Ar=o.slice(e,1<l?1-l:void 0)}function Lr(e){var t=e.keyCode;return"charCode"in e?(e=e.charCode,e===0&&t===13&&(e=13)):e=t,e===10&&(e=13),32<=e||e===13?e:0}function yr(){return!0}function $0(){return!1}function Nn(e){function t(n,l,o,a,i){this._reactName=n,this._targetInst=o,this.type=l,this.nativeEvent=a,this.target=i,this.currentTarget=null;for(var s in e)e.hasOwnProperty(s)&&(n=e[s],this[s]=n?n(a):a[s]);return this.isDefaultPrevented=(a.defaultPrevented!=null?a.defaultPrevented:a.returnValue===!1)?yr:$0,this.isPropagationStopped=$0,this}return Et(t.prototype,{preventDefault:function(){this.defaultPrevented=!0;var n=this.nativeEvent;n&&(n.preventDefault?n.preventDefault():typeof n.returnValue!="unknown"&&(n.returnValue=!1),this.isDefaultPrevented=yr)},stopPropagation:function(){var n=this.nativeEvent;n&&(n.stopPropagation?n.stopPropagation():typeof n.cancelBubble!="unknown"&&(n.cancelBubble=!0),this.isPropagationStopped=yr)},persist:function(){},isPersistent:yr}),t}var ca={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},vc=Nn(ca),As=Et({},ca,{view:0,detail:0}),s5=Nn(As),Ou,$u,Ii,wc=Et({},As,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:f_,button:0,buttons:0,relatedTarget:function(e){return e.relatedTarget===void 0?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==Ii&&(Ii&&e.type==="mousemove"?(Ou=e.screenX-Ii.screenX,$u=e.screenY-Ii.screenY):$u=Ou=0,Ii=e),Ou)},movementY:function(e){return"movementY"in e?e.movementY:$u}}),H0=Nn(wc),r5=Et({},wc,{dataTransfer:0}),c5=Nn(r5),u5=Et({},As,{relatedTarget:0}),Hu=Nn(u5),d5=Et({},ca,{animationName:0,elapsedTime:0,pseudoElement:0}),_5=Nn(d5),f5=Et({},ca,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}}),h5=Nn(f5),m5=Et({},ca,{data:0}),U0=Nn(m5),g5={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},y5={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},p5={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function b5(e){var t=this.nativeEvent;return t.getModifierState?t.getModifierState(e):(e=p5[e])?!!t[e]:!1}function f_(){return b5}var x5=Et({},As,{key:function(e){if(e.key){var t=g5[e.key]||e.key;if(t!=="Unidentified")return t}return e.type==="keypress"?(e=Lr(e),e===13?"Enter":String.fromCharCode(e)):e.type==="keydown"||e.type==="keyup"?y5[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:f_,charCode:function(e){return e.type==="keypress"?Lr(e):0},keyCode:function(e){return e.type==="keydown"||e.type==="keyup"?e.keyCode:0},which:function(e){return e.type==="keypress"?Lr(e):e.type==="keydown"||e.type==="keyup"?e.keyCode:0}}),v5=Nn(x5),w5=Et({},wc,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Y0=Nn(w5),k5=Et({},As,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:f_}),S5=Nn(k5),C5=Et({},ca,{propertyName:0,elapsedTime:0,pseudoElement:0}),M5=Nn(C5),E5=Et({},wc,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0}),T5=Nn(E5),D5=Et({},ca,{newState:0,oldState:0}),N5=Nn(D5),z5=[9,13,27,32],h_=Jl&&"CompositionEvent"in window,es=null;Jl&&"documentMode"in document&&(es=document.documentMode);var A5=Jl&&"TextEvent"in window&&!es,k1=Jl&&(!h_||es&&8<es&&11>=es),j0=" ",X0=!1;function S1(e,t){switch(e){case"keyup":return z5.indexOf(t.keyCode)!==-1;case"keydown":return t.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function C1(e){return e=e.detail,typeof e=="object"&&"data"in e?e.data:null}var Ya=!1;function L5(e,t){switch(e){case"compositionend":return C1(t);case"keypress":return t.which!==32?null:(X0=!0,j0);case"textInput":return e=t.data,e===j0&&X0?null:e;default:return null}}function R5(e,t){if(Ya)return e==="compositionend"||!h_&&S1(e,t)?(e=w1(),Ar=__=bo=null,Ya=!1,e):null;switch(e){case"paste":return null;case"keypress":if(!(t.ctrlKey||t.altKey||t.metaKey)||t.ctrlKey&&t.altKey){if(t.char&&1<t.char.length)return t.char;if(t.which)return String.fromCharCode(t.which)}return null;case"compositionend":return k1&&t.locale!=="ko"?null:t.data;default:return null}}var B5={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function I0(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t==="input"?!!B5[e.type]:t==="textarea"}function M1(e,t,n,l){Ua?Ka?Ka.push(l):Ka=[l]:Ua=l,t=fc(t,"onChange"),0<t.length&&(n=new vc("onChange","change",null,n,l),e.push({event:n,listeners:t}))}var ts=null,ms=null;function O5(e){vg(e,0)}function kc(e){var t=Fi(e);if(g1(t))return e}function q0(e,t){if(e==="change")return t}var E1=!1;Jl&&(Jl?(br="oninput"in document,br||(Uu=document.createElement("div"),Uu.setAttribute("oninput","return;"),br=typeof Uu.oninput=="function"),pr=br):pr=!1,E1=pr&&(!document.documentMode||9<document.documentMode));var pr,br,Uu;function Q0(){ts&&(ts.detachEvent("onpropertychange",T1),ms=ts=null)}function T1(e){if(e.propertyName==="value"&&kc(ms)){var t=[];M1(t,ms,e,d_(e)),v1(O5,t)}}function $5(e,t,n){e==="focusin"?(Q0(),ts=t,ms=n,ts.attachEvent("onpropertychange",T1)):e==="focusout"&&Q0()}function H5(e){if(e==="selectionchange"||e==="keyup"||e==="keydown")return kc(ms)}function U5(e,t){if(e==="click")return kc(t)}function Y5(e,t){if(e==="input"||e==="change")return kc(t)}function j5(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var Yn=typeof Object.is=="function"?Object.is:j5;function gs(e,t){if(Yn(e,t))return!0;if(typeof e!="object"||e===null||typeof t!="object"||t===null)return!1;var n=Object.keys(e),l=Object.keys(t);if(n.length!==l.length)return!1;for(l=0;l<n.length;l++){var o=n[l];if(!gd.call(t,o)||!Yn(e[o],t[o]))return!1}return!0}function W0(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function G0(e,t){var n=W0(e);e=0;for(var l;n;){if(n.nodeType===3){if(l=e+n.textContent.length,e<=t&&l>=t)return{node:n,offset:t-e};e=l}e:{for(;n;){if(n.nextSibling){n=n.nextSibling;break e}n=n.parentNode}n=void 0}n=W0(n)}}function D1(e,t){return e&&t?e===t?!0:e&&e.nodeType===3?!1:t&&t.nodeType===3?D1(e,t.parentNode):"contains"in e?e.contains(t):e.compareDocumentPosition?!!(e.compareDocumentPosition(t)&16):!1:!1}function N1(e){e=e!=null&&e.ownerDocument!=null&&e.ownerDocument.defaultView!=null?e.ownerDocument.defaultView:window;for(var t=Zr(e.document);t instanceof e.HTMLIFrameElement;){try{var n=typeof t.contentWindow.location.href=="string"}catch{n=!1}if(n)e=t.contentWindow;else break;t=Zr(e.document)}return t}function m_(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t&&(t==="input"&&(e.type==="text"||e.type==="search"||e.type==="tel"||e.type==="url"||e.type==="password")||t==="textarea"||e.contentEditable==="true")}var X5=Jl&&"documentMode"in document&&11>=document.documentMode,ja=null,kd=null,ns=null,Sd=!1;function V0(e,t,n){var l=n.window===n?n.document:n.nodeType===9?n:n.ownerDocument;Sd||ja==null||ja!==Zr(l)||(l=ja,"selectionStart"in l&&m_(l)?l={start:l.selectionStart,end:l.selectionEnd}:(l=(l.ownerDocument&&l.ownerDocument.defaultView||window).getSelection(),l={anchorNode:l.anchorNode,anchorOffset:l.anchorOffset,focusNode:l.focusNode,focusOffset:l.focusOffset}),ns&&gs(ns,l)||(ns=l,l=fc(kd,"onSelect"),0<l.length&&(t=new vc("onSelect","select",null,t,n),e.push({event:t,listeners:l}),t.target=ja)))}function Go(e,t){var n={};return n[e.toLowerCase()]=t.toLowerCase(),n["Webkit"+e]="webkit"+t,n["Moz"+e]="moz"+t,n}var Xa={animationend:Go("Animation","AnimationEnd"),animationiteration:Go("Animation","AnimationIteration"),animationstart:Go("Animation","AnimationStart"),transitionrun:Go("Transition","TransitionRun"),transitionstart:Go("Transition","TransitionStart"),transitioncancel:Go("Transition","TransitionCancel"),transitionend:Go("Transition","TransitionEnd")},Yu={},z1={};Jl&&(z1=document.createElement("div").style,"AnimationEvent"in window||(delete Xa.animationend.animation,delete Xa.animationiteration.animation,delete Xa.animationstart.animation),"TransitionEvent"in window||delete Xa.transitionend.transition);function ua(e){if(Yu[e])return Yu[e];if(!Xa[e])return e;var t=Xa[e],n;for(n in t)if(t.hasOwnProperty(n)&&n in z1)return Yu[e]=t[n];return e}var A1=ua("animationend"),L1=ua("animationiteration"),R1=ua("animationstart"),I5=ua("transitionrun"),q5=ua("transitionstart"),Q5=ua("transitioncancel"),B1=ua("transitionend"),O1=new Map,Cd="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");Cd.push("scrollEnd");function ml(e,t){O1.set(e,t),ra(t,[e])}var Kr=typeof reportError=="function"?reportError:function(e){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof e=="object"&&e!==null&&typeof e.message=="string"?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",e);return}console.error(e)},Kn=[],Ia=0,g_=0;function Sc(){for(var e=Ia,t=g_=Ia=0;t<e;){var n=Kn[t];Kn[t++]=null;var l=Kn[t];Kn[t++]=null;var o=Kn[t];Kn[t++]=null;var a=Kn[t];if(Kn[t++]=null,l!==null&&o!==null){var i=l.pending;i===null?o.next=o:(o.next=i.next,i.next=o),l.pending=o}a!==0&&$1(n,o,a)}}function Cc(e,t,n,l){Kn[Ia++]=e,Kn[Ia++]=t,Kn[Ia++]=n,Kn[Ia++]=l,g_|=l,e.lanes|=l,e=e.alternate,e!==null&&(e.lanes|=l)}function y_(e,t,n,l){return Cc(e,t,n,l),Fr(e)}function da(e,t){return Cc(e,null,null,t),Fr(e)}function $1(e,t,n){e.lanes|=n;var l=e.alternate;l!==null&&(l.lanes|=n);for(var o=!1,a=e.return;a!==null;)a.childLanes|=n,l=a.alternate,l!==null&&(l.childLanes|=n),a.tag===22&&(e=a.stateNode,e===null||e._visibility&1||(o=!0)),e=a,a=a.return;return e.tag===3?(a=e.stateNode,o&&t!==null&&(o=31-Hn(n),e=a.hiddenUpdates,l=e[o],l===null?e[o]=[t]:l.push(t),t.lane=n|536870912),a):null}function Fr(e){if(50<ds)throw ds=0,Wd=null,Error(O(185));for(var t=e.return;t!==null;)e=t,t=e.return;return e.tag===3?e.stateNode:null}var qa={};function W5(e,t,n,l){this.tag=e,this.key=n,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=t,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=l,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Rn(e,t,n,l){return new W5(e,t,n,l)}function p_(e){return e=e.prototype,!(!e||!e.isReactComponent)}function Zl(e,t){var n=e.alternate;return n===null?(n=Rn(e.tag,t,e.key,e.mode),n.elementType=e.elementType,n.type=e.type,n.stateNode=e.stateNode,n.alternate=e,e.alternate=n):(n.pendingProps=t,n.type=e.type,n.flags=0,n.subtreeFlags=0,n.deletions=null),n.flags=e.flags&65011712,n.childLanes=e.childLanes,n.lanes=e.lanes,n.child=e.child,n.memoizedProps=e.memoizedProps,n.memoizedState=e.memoizedState,n.updateQueue=e.updateQueue,t=e.dependencies,n.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext},n.sibling=e.sibling,n.index=e.index,n.ref=e.ref,n.refCleanup=e.refCleanup,n}function H1(e,t){e.flags&=65011714;var n=e.alternate;return n===null?(e.childLanes=0,e.lanes=t,e.child=null,e.subtreeFlags=0,e.memoizedProps=null,e.memoizedState=null,e.updateQueue=null,e.dependencies=null,e.stateNode=null):(e.childLanes=n.childLanes,e.lanes=n.lanes,e.child=n.child,e.subtreeFlags=0,e.deletions=null,e.memoizedProps=n.memoizedProps,e.memoizedState=n.memoizedState,e.updateQueue=n.updateQueue,e.type=n.type,t=n.dependencies,e.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext}),e}function Rr(e,t,n,l,o,a){var i=0;if(l=e,typeof e=="function")p_(e)&&(i=1);else if(typeof e=="string")i=Z2(e,n,Dl.current)?26:e==="html"||e==="head"||e==="body"?27:5;else e:switch(e){case _d:return e=Rn(31,n,t,o),e.elementType=_d,e.lanes=a,e;case Oa:return Po(n.children,o,a,t);case l1:i=8,o|=24;break;case cd:return e=Rn(12,n,t,o|2),e.elementType=cd,e.lanes=a,e;case ud:return e=Rn(13,n,t,o),e.elementType=ud,e.lanes=a,e;case dd:return e=Rn(19,n,t,o),e.elementType=dd,e.lanes=a,e;default:if(typeof e=="object"&&e!==null)switch(e.$$typeof){case Wl:i=10;break e;case o1:i=9;break e;case o_:i=11;break e;case a_:i=14;break e;case _o:i=16,l=null;break e}i=29,n=Error(O(130,e===null?"null":typeof e,"")),l=null}return t=Rn(i,n,t,o),t.elementType=e,t.type=l,t.lanes=a,t}function Po(e,t,n,l){return e=Rn(7,e,l,t),e.lanes=n,e}function ju(e,t,n){return e=Rn(6,e,null,t),e.lanes=n,e}function U1(e){var t=Rn(18,null,null,0);return t.stateNode=e,t}function Xu(e,t,n){return t=Rn(4,e.children!==null?e.children:[],e.key,t),t.lanes=n,t.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},t}var Z0=new WeakMap;function tl(e,t){if(typeof e=="object"&&e!==null){var n=Z0.get(e);return n!==void 0?n:(t={value:e,source:t,stack:N0(t)},Z0.set(e,t),t)}return{value:e,source:t,stack:N0(t)}}var Qa=[],Wa=0,Jr=null,ys=0,Jn=[],Pn=0,Ao=null,Ml=1,El="";function ql(e,t){Qa[Wa++]=ys,Qa[Wa++]=Jr,Jr=e,ys=t}function Y1(e,t,n){Jn[Pn++]=Ml,Jn[Pn++]=El,Jn[Pn++]=Ao,Ao=e;var l=Ml;e=El;var o=32-Hn(l)-1;l&=~(1<<o),n+=1;var a=32-Hn(t)+o;if(30<a){var i=o-o%5;a=(l&(1<<i)-1).toString(32),l>>=i,o-=i,Ml=1<<32-Hn(t)+o|n<<o|l,El=a+e}else Ml=1<<a|n<<o|l,El=e}function b_(e){e.return!==null&&(ql(e,1),Y1(e,1,0))}function x_(e){for(;e===Jr;)Jr=Qa[--Wa],Qa[Wa]=null,ys=Qa[--Wa],Qa[Wa]=null;for(;e===Ao;)Ao=Jn[--Pn],Jn[Pn]=null,El=Jn[--Pn],Jn[Pn]=null,Ml=Jn[--Pn],Jn[Pn]=null}function j1(e,t){Jn[Pn++]=Ml,Jn[Pn++]=El,Jn[Pn++]=Ao,Ml=t.id,El=t.overflow,Ao=e}var cn=null,Mt=null,We=!1,So=null,nl=!1,Md=Error(O(519));function Lo(e){var t=Error(O(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw ps(tl(t,e)),Md}function K0(e){var t=e.stateNode,n=e.type,l=e.memoizedProps;switch(t[rn]=e,t[Dn]=l,n){case"dialog":je("cancel",t),je("close",t);break;case"iframe":case"object":case"embed":je("load",t);break;case"video":case"audio":for(n=0;n<ws.length;n++)je(ws[n],t);break;case"source":je("error",t);break;case"img":case"image":case"link":je("error",t),je("load",t);break;case"details":je("toggle",t);break;case"input":je("invalid",t),y1(t,l.value,l.defaultValue,l.checked,l.defaultChecked,l.type,l.name,!0);break;case"select":je("invalid",t);break;case"textarea":je("invalid",t),b1(t,l.value,l.defaultValue,l.children)}n=l.children,typeof n!="string"&&typeof n!="number"&&typeof n!="bigint"||t.textContent===""+n||l.suppressHydrationWarning===!0||kg(t.textContent,n)?(l.popover!=null&&(je("beforetoggle",t),je("toggle",t)),l.onScroll!=null&&je("scroll",t),l.onScrollEnd!=null&&je("scrollend",t),l.onClick!=null&&(t.onclick=Gl),t=!0):t=!1,t||Lo(e,!0)}function F0(e){for(cn=e.return;cn;)switch(cn.tag){case 5:case 31:case 13:nl=!1;return;case 27:case 3:nl=!0;return;default:cn=cn.return}}function Aa(e){if(e!==cn)return!1;if(!We)return F0(e),We=!0,!1;var t=e.tag,n;if((n=t!==3&&t!==27)&&((n=t===5)&&(n=e.type,n=!(n!=="form"&&n!=="button")||Fd(e.type,e.memoizedProps)),n=!n),n&&Mt&&Lo(e),F0(e),t===13){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(O(317));Mt=Uh(e)}else if(t===31){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(O(317));Mt=Uh(e)}else t===27?(t=Mt,$o(e.type)?(e=t_,t_=null,Mt=e):Mt=t):Mt=cn?ol(e.stateNode.nextSibling):null;return!0}function la(){Mt=cn=null,We=!1}function Iu(){var e=So;return e!==null&&(En===null?En=e:En.push.apply(En,e),So=null),e}function ps(e){So===null?So=[e]:So.push(e)}var Ed=Nl(null),_a=null,Vl=null;function ho(e,t,n){kt(Ed,t._currentValue),t._currentValue=n}function Kl(e){e._currentValue=Ed.current,on(Ed)}function Td(e,t,n){for(;e!==null;){var l=e.alternate;if((e.childLanes&t)!==t?(e.childLanes|=t,l!==null&&(l.childLanes|=t)):l!==null&&(l.childLanes&t)!==t&&(l.childLanes|=t),e===n)break;e=e.return}}function Dd(e,t,n,l){var o=e.child;for(o!==null&&(o.return=e);o!==null;){var a=o.dependencies;if(a!==null){var i=o.child;a=a.firstContext;e:for(;a!==null;){var s=a;a=o;for(var r=0;r<t.length;r++)if(s.context===t[r]){a.lanes|=n,s=a.alternate,s!==null&&(s.lanes|=n),Td(a.return,n,e),l||(i=null);break e}a=s.next}}else if(o.tag===18){if(i=o.return,i===null)throw Error(O(341));i.lanes|=n,a=i.alternate,a!==null&&(a.lanes|=n),Td(i,n,e),i=null}else i=o.child;if(i!==null)i.return=o;else for(i=o;i!==null;){if(i===e){i=null;break}if(o=i.sibling,o!==null){o.return=i.return,i=o;break}i=i.return}o=i}}function hi(e,t,n,l){e=null;for(var o=t,a=!1;o!==null;){if(!a){if((o.flags&524288)!==0)a=!0;else if((o.flags&262144)!==0)break}if(o.tag===10){var i=o.alternate;if(i===null)throw Error(O(387));if(i=i.memoizedProps,i!==null){var s=o.type;Yn(o.pendingProps.value,i.value)||(e!==null?e.push(s):e=[s])}}else if(o===Qr.current){if(i=o.alternate,i===null)throw Error(O(387));i.memoizedState.memoizedState!==o.memoizedState.memoizedState&&(e!==null?e.push(Ss):e=[Ss])}o=o.return}e!==null&&Dd(t,e,n,l),t.flags|=262144}function Pr(e){for(e=e.firstContext;e!==null;){if(!Yn(e.context._currentValue,e.memoizedValue))return!0;e=e.next}return!1}function oa(e){_a=e,Vl=null,e=e.dependencies,e!==null&&(e.firstContext=null)}function un(e){return X1(_a,e)}function xr(e,t){return _a===null&&oa(e),X1(e,t)}function X1(e,t){var n=t._currentValue;if(t={context:t,memoizedValue:n,next:null},Vl===null){if(e===null)throw Error(O(308));Vl=t,e.dependencies={lanes:0,firstContext:t},e.flags|=524288}else Vl=Vl.next=t;return n}var G5=typeof AbortController<"u"?AbortController:function(){var e=[],t=this.signal={aborted:!1,addEventListener:function(n,l){e.push(l)}};this.abort=function(){t.aborted=!0,e.forEach(function(n){return n()})}},V5=en.unstable_scheduleCallback,Z5=en.unstable_NormalPriority,Zt={$$typeof:Wl,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function v_(){return{controller:new G5,data:new Map,refCount:0}}function Ls(e){e.refCount--,e.refCount===0&&V5(Z5,function(){e.controller.abort()})}var ls=null,Nd=0,oi=0,Fa=null;function K5(e,t){if(ls===null){var n=ls=[];Nd=0,oi=W_(),Fa={status:"pending",value:void 0,then:function(l){n.push(l)}}}return Nd++,t.then(J0,J0),t}function J0(){if(--Nd===0&&ls!==null){Fa!==null&&(Fa.status="fulfilled");var e=ls;ls=null,oi=0,Fa=null;for(var t=0;t<e.length;t++)(0,e[t])()}}function F5(e,t){var n=[],l={status:"pending",value:null,reason:null,then:function(o){n.push(o)}};return e.then(function(){l.status="fulfilled",l.value=t;for(var o=0;o<n.length;o++)(0,n[o])(t)},function(o){for(l.status="rejected",l.reason=o,o=0;o<n.length;o++)(0,n[o])(void 0)}),l}var P0=we.S;we.S=function(e,t){ng=On(),typeof t=="object"&&t!==null&&typeof t.then=="function"&&K5(e,t),P0!==null&&P0(e,t)};var ea=Nl(null);function w_(){var e=ea.current;return e!==null?e:pt.pooledCache}function Br(e,t){t===null?kt(ea,ea.current):kt(ea,t.pool)}function I1(){var e=w_();return e===null?null:{parent:Zt._currentValue,pool:e}}var mi=Error(O(460)),k_=Error(O(474)),Mc=Error(O(542)),ec={then:function(){}};function eh(e){return e=e.status,e==="fulfilled"||e==="rejected"}function q1(e,t,n){switch(n=e[n],n===void 0?e.push(t):n!==t&&(t.then(Gl,Gl),t=n),t.status){case"fulfilled":return t.value;case"rejected":throw e=t.reason,nh(e),e;default:if(typeof t.status=="string")t.then(Gl,Gl);else{if(e=pt,e!==null&&100<e.shellSuspendCounter)throw Error(O(482));e=t,e.status="pending",e.then(function(l){if(t.status==="pending"){var o=t;o.status="fulfilled",o.value=l}},function(l){if(t.status==="pending"){var o=t;o.status="rejected",o.reason=l}})}switch(t.status){case"fulfilled":return t.value;case"rejected":throw e=t.reason,nh(e),e}throw ta=t,mi}}function Ko(e){try{var t=e._init;return t(e._payload)}catch(n){throw n!==null&&typeof n=="object"&&typeof n.then=="function"?(ta=n,mi):n}}var ta=null;function th(){if(ta===null)throw Error(O(459));var e=ta;return ta=null,e}function nh(e){if(e===mi||e===Mc)throw Error(O(483))}var Ja=null,bs=0;function vr(e){var t=bs;return bs+=1,Ja===null&&(Ja=[]),q1(Ja,e,t)}function qi(e,t){t=t.props.ref,e.ref=t!==void 0?t:null}function wr(e,t){throw t.$$typeof===$p?Error(O(525)):(e=Object.prototype.toString.call(t),Error(O(31,e==="[object Object]"?"object with keys {"+Object.keys(t).join(", ")+"}":e)))}function Q1(e){function t(h,y){if(e){var k=h.deletions;k===null?(h.deletions=[y],h.flags|=16):k.push(y)}}function n(h,y){if(!e)return null;for(;y!==null;)t(h,y),y=y.sibling;return null}function l(h){for(var y=new Map;h!==null;)h.key!==null?y.set(h.key,h):y.set(h.index,h),h=h.sibling;return y}function o(h,y){return h=Zl(h,y),h.index=0,h.sibling=null,h}function a(h,y,k){return h.index=k,e?(k=h.alternate,k!==null?(k=k.index,k<y?(h.flags|=67108866,y):k):(h.flags|=67108866,y)):(h.flags|=1048576,y)}function i(h){return e&&h.alternate===null&&(h.flags|=67108866),h}function s(h,y,k,E){return y===null||y.tag!==6?(y=ju(k,h.mode,E),y.return=h,y):(y=o(y,k),y.return=h,y)}function r(h,y,k,E){var Q=k.type;return Q===Oa?f(h,y,k.props.children,E,k.key):y!==null&&(y.elementType===Q||typeof Q=="object"&&Q!==null&&Q.$$typeof===_o&&Ko(Q)===y.type)?(y=o(y,k.props),qi(y,k),y.return=h,y):(y=Rr(k.type,k.key,k.props,null,h.mode,E),qi(y,k),y.return=h,y)}function p(h,y,k,E){return y===null||y.tag!==4||y.stateNode.containerInfo!==k.containerInfo||y.stateNode.implementation!==k.implementation?(y=Xu(k,h.mode,E),y.return=h,y):(y=o(y,k.children||[]),y.return=h,y)}function f(h,y,k,E,Q){return y===null||y.tag!==7?(y=Po(k,h.mode,E,Q),y.return=h,y):(y=o(y,k),y.return=h,y)}function b(h,y,k){if(typeof y=="string"&&y!==""||typeof y=="number"||typeof y=="bigint")return y=ju(""+y,h.mode,k),y.return=h,y;if(typeof y=="object"&&y!==null){switch(y.$$typeof){case _r:return k=Rr(y.type,y.key,y.props,null,h.mode,k),qi(k,y),k.return=h,k;case Zi:return y=Xu(y,h.mode,k),y.return=h,y;case _o:return y=Ko(y),b(h,y,k)}if(Ki(y)||Xi(y))return y=Po(y,h.mode,k,null),y.return=h,y;if(typeof y.then=="function")return b(h,vr(y),k);if(y.$$typeof===Wl)return b(h,xr(h,y),k);wr(h,y)}return null}function _(h,y,k,E){var Q=y!==null?y.key:null;if(typeof k=="string"&&k!==""||typeof k=="number"||typeof k=="bigint")return Q!==null?null:s(h,y,""+k,E);if(typeof k=="object"&&k!==null){switch(k.$$typeof){case _r:return k.key===Q?r(h,y,k,E):null;case Zi:return k.key===Q?p(h,y,k,E):null;case _o:return k=Ko(k),_(h,y,k,E)}if(Ki(k)||Xi(k))return Q!==null?null:f(h,y,k,E,null);if(typeof k.then=="function")return _(h,y,vr(k),E);if(k.$$typeof===Wl)return _(h,y,xr(h,k),E);wr(h,k)}return null}function w(h,y,k,E,Q){if(typeof E=="string"&&E!==""||typeof E=="number"||typeof E=="bigint")return h=h.get(k)||null,s(y,h,""+E,Q);if(typeof E=="object"&&E!==null){switch(E.$$typeof){case _r:return h=h.get(E.key===null?k:E.key)||null,r(y,h,E,Q);case Zi:return h=h.get(E.key===null?k:E.key)||null,p(y,h,E,Q);case _o:return E=Ko(E),w(h,y,k,E,Q)}if(Ki(E)||Xi(E))return h=h.get(k)||null,f(y,h,E,Q,null);if(typeof E.then=="function")return w(h,y,k,vr(E),Q);if(E.$$typeof===Wl)return w(h,y,k,xr(y,E),Q);wr(y,E)}return null}function C(h,y,k,E){for(var Q=null,oe=null,L=y,K=y=0,ee=null;L!==null&&K<k.length;K++){L.index>K?(ee=L,L=null):ee=L.sibling;var F=_(h,L,k[K],E);if(F===null){L===null&&(L=ee);break}e&&L&&F.alternate===null&&t(h,L),y=a(F,y,K),oe===null?Q=F:oe.sibling=F,oe=F,L=ee}if(K===k.length)return n(h,L),We&&ql(h,K),Q;if(L===null){for(;K<k.length;K++)L=b(h,k[K],E),L!==null&&(y=a(L,y,K),oe===null?Q=L:oe.sibling=L,oe=L);return We&&ql(h,K),Q}for(L=l(L);K<k.length;K++)ee=w(L,h,K,k[K],E),ee!==null&&(e&&ee.alternate!==null&&L.delete(ee.key===null?K:ee.key),y=a(ee,y,K),oe===null?Q=ee:oe.sibling=ee,oe=ee);return e&&L.forEach(function(he){return t(h,he)}),We&&ql(h,K),Q}function z(h,y,k,E){if(k==null)throw Error(O(151));for(var Q=null,oe=null,L=y,K=y=0,ee=null,F=k.next();L!==null&&!F.done;K++,F=k.next()){L.index>K?(ee=L,L=null):ee=L.sibling;var he=_(h,L,F.value,E);if(he===null){L===null&&(L=ee);break}e&&L&&he.alternate===null&&t(h,L),y=a(he,y,K),oe===null?Q=he:oe.sibling=he,oe=he,L=ee}if(F.done)return n(h,L),We&&ql(h,K),Q;if(L===null){for(;!F.done;K++,F=k.next())F=b(h,F.value,E),F!==null&&(y=a(F,y,K),oe===null?Q=F:oe.sibling=F,oe=F);return We&&ql(h,K),Q}for(L=l(L);!F.done;K++,F=k.next())F=w(L,h,K,F.value,E),F!==null&&(e&&F.alternate!==null&&L.delete(F.key===null?K:F.key),y=a(F,y,K),oe===null?Q=F:oe.sibling=F,oe=F);return e&&L.forEach(function(et){return t(h,et)}),We&&ql(h,K),Q}function D(h,y,k,E){if(typeof k=="object"&&k!==null&&k.type===Oa&&k.key===null&&(k=k.props.children),typeof k=="object"&&k!==null){switch(k.$$typeof){case _r:e:{for(var Q=k.key;y!==null;){if(y.key===Q){if(Q=k.type,Q===Oa){if(y.tag===7){n(h,y.sibling),E=o(y,k.props.children),E.return=h,h=E;break e}}else if(y.elementType===Q||typeof Q=="object"&&Q!==null&&Q.$$typeof===_o&&Ko(Q)===y.type){n(h,y.sibling),E=o(y,k.props),qi(E,k),E.return=h,h=E;break e}n(h,y);break}else t(h,y);y=y.sibling}k.type===Oa?(E=Po(k.props.children,h.mode,E,k.key),E.return=h,h=E):(E=Rr(k.type,k.key,k.props,null,h.mode,E),qi(E,k),E.return=h,h=E)}return i(h);case Zi:e:{for(Q=k.key;y!==null;){if(y.key===Q)if(y.tag===4&&y.stateNode.containerInfo===k.containerInfo&&y.stateNode.implementation===k.implementation){n(h,y.sibling),E=o(y,k.children||[]),E.return=h,h=E;break e}else{n(h,y);break}else t(h,y);y=y.sibling}E=Xu(k,h.mode,E),E.return=h,h=E}return i(h);case _o:return k=Ko(k),D(h,y,k,E)}if(Ki(k))return C(h,y,k,E);if(Xi(k)){if(Q=Xi(k),typeof Q!="function")throw Error(O(150));return k=Q.call(k),z(h,y,k,E)}if(typeof k.then=="function")return D(h,y,vr(k),E);if(k.$$typeof===Wl)return D(h,y,xr(h,k),E);wr(h,k)}return typeof k=="string"&&k!==""||typeof k=="number"||typeof k=="bigint"?(k=""+k,y!==null&&y.tag===6?(n(h,y.sibling),E=o(y,k),E.return=h,h=E):(n(h,y),E=ju(k,h.mode,E),E.return=h,h=E),i(h)):n(h,y)}return function(h,y,k,E){try{bs=0;var Q=D(h,y,k,E);return Ja=null,Q}catch(L){if(L===mi||L===Mc)throw L;var oe=Rn(29,L,null,h.mode);return oe.lanes=E,oe.return=h,oe}}}var aa=Q1(!0),W1=Q1(!1),fo=!1;function S_(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function zd(e,t){e=e.updateQueue,t.updateQueue===e&&(t.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,callbacks:null})}function Co(e){return{lane:e,tag:0,payload:null,callback:null,next:null}}function Mo(e,t,n){var l=e.updateQueue;if(l===null)return null;if(l=l.shared,(lt&2)!==0){var o=l.pending;return o===null?t.next=t:(t.next=o.next,o.next=t),l.pending=t,t=Fr(e),$1(e,null,n),t}return Cc(e,l,t,n),Fr(e)}function os(e,t,n){if(t=t.updateQueue,t!==null&&(t=t.shared,(n&4194048)!==0)){var l=t.lanes;l&=e.pendingLanes,n|=l,t.lanes=n,u1(e,n)}}function qu(e,t){var n=e.updateQueue,l=e.alternate;if(l!==null&&(l=l.updateQueue,n===l)){var o=null,a=null;if(n=n.firstBaseUpdate,n!==null){do{var i={lane:n.lane,tag:n.tag,payload:n.payload,callback:null,next:null};a===null?o=a=i:a=a.next=i,n=n.next}while(n!==null);a===null?o=a=t:a=a.next=t}else o=a=t;n={baseState:l.baseState,firstBaseUpdate:o,lastBaseUpdate:a,shared:l.shared,callbacks:l.callbacks},e.updateQueue=n;return}e=n.lastBaseUpdate,e===null?n.firstBaseUpdate=t:e.next=t,n.lastBaseUpdate=t}var Ad=!1;function as(){if(Ad){var e=Fa;if(e!==null)throw e}}function is(e,t,n,l){Ad=!1;var o=e.updateQueue;fo=!1;var a=o.firstBaseUpdate,i=o.lastBaseUpdate,s=o.shared.pending;if(s!==null){o.shared.pending=null;var r=s,p=r.next;r.next=null,i===null?a=p:i.next=p,i=r;var f=e.alternate;f!==null&&(f=f.updateQueue,s=f.lastBaseUpdate,s!==i&&(s===null?f.firstBaseUpdate=p:s.next=p,f.lastBaseUpdate=r))}if(a!==null){var b=o.baseState;i=0,f=p=r=null,s=a;do{var _=s.lane&-536870913,w=_!==s.lane;if(w?(Qe&_)===_:(l&_)===_){_!==0&&_===oi&&(Ad=!0),f!==null&&(f=f.next={lane:0,tag:s.tag,payload:s.payload,callback:null,next:null});e:{var C=e,z=s;_=t;var D=n;switch(z.tag){case 1:if(C=z.payload,typeof C=="function"){b=C.call(D,b,_);break e}b=C;break e;case 3:C.flags=C.flags&-65537|128;case 0:if(C=z.payload,_=typeof C=="function"?C.call(D,b,_):C,_==null)break e;b=Et({},b,_);break e;case 2:fo=!0}}_=s.callback,_!==null&&(e.flags|=64,w&&(e.flags|=8192),w=o.callbacks,w===null?o.callbacks=[_]:w.push(_))}else w={lane:_,tag:s.tag,payload:s.payload,callback:s.callback,next:null},f===null?(p=f=w,r=b):f=f.next=w,i|=_;if(s=s.next,s===null){if(s=o.shared.pending,s===null)break;w=s,s=w.next,w.next=null,o.lastBaseUpdate=w,o.shared.pending=null}}while(!0);f===null&&(r=b),o.baseState=r,o.firstBaseUpdate=p,o.lastBaseUpdate=f,a===null&&(o.shared.lanes=0),Bo|=i,e.lanes=i,e.memoizedState=b}}function G1(e,t){if(typeof e!="function")throw Error(O(191,e));e.call(t)}function V1(e,t){var n=e.callbacks;if(n!==null)for(e.callbacks=null,e=0;e<n.length;e++)G1(n[e],t)}var ai=Nl(null),tc=Nl(0);function lh(e,t){e=no,kt(tc,e),kt(ai,t),no=e|t.baseLanes}function Ld(){kt(tc,no),kt(ai,ai.current)}function C_(){no=tc.current,on(ai),on(tc)}var jn=Nl(null),ll=null;function mo(e){var t=e.alternate;kt(Xt,Xt.current&1),kt(jn,e),ll===null&&(t===null||ai.current!==null||t.memoizedState!==null)&&(ll=e)}function Rd(e){kt(Xt,Xt.current),kt(jn,e),ll===null&&(ll=e)}function Z1(e){e.tag===22?(kt(Xt,Xt.current),kt(jn,e),ll===null&&(ll=e)):go(e)}function go(){kt(Xt,Xt.current),kt(jn,jn.current)}function Ln(e){on(jn),ll===e&&(ll=null),on(Xt)}var Xt=Nl(0);function nc(e){for(var t=e;t!==null;){if(t.tag===13){var n=t.memoizedState;if(n!==null&&(n=n.dehydrated,n===null||Pd(n)||e_(n)))return t}else if(t.tag===19&&(t.memoizedProps.revealOrder==="forwards"||t.memoizedProps.revealOrder==="backwards"||t.memoizedProps.revealOrder==="unstable_legacy-backwards"||t.memoizedProps.revealOrder==="together")){if((t.flags&128)!==0)return t}else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return null;t=t.return}t.sibling.return=t.return,t=t.sibling}return null}var Pl=0,Le=null,gt=null,Gt=null,lc=!1,Pa=!1,ia=!1,oc=0,xs=0,ei=null,J5=0;function $t(){throw Error(O(321))}function M_(e,t){if(t===null)return!1;for(var n=0;n<t.length&&n<e.length;n++)if(!Yn(e[n],t[n]))return!1;return!0}function E_(e,t,n,l,o,a){return Pl=a,Le=t,t.memoizedState=null,t.updateQueue=null,t.lanes=0,we.H=e===null||e.memoizedState===null?Mm:H_,ia=!1,a=n(l,o),ia=!1,Pa&&(a=F1(t,n,l,o)),K1(e),a}function K1(e){we.H=vs;var t=gt!==null&&gt.next!==null;if(Pl=0,Gt=gt=Le=null,lc=!1,xs=0,ei=null,t)throw Error(O(300));e===null||Kt||(e=e.dependencies,e!==null&&Pr(e)&&(Kt=!0))}function F1(e,t,n,l){Le=e;var o=0;do{if(Pa&&(ei=null),xs=0,Pa=!1,25<=o)throw Error(O(301));if(o+=1,Gt=gt=null,e.updateQueue!=null){var a=e.updateQueue;a.lastEffect=null,a.events=null,a.stores=null,a.memoCache!=null&&(a.memoCache.index=0)}we.H=Em,a=t(n,l)}while(Pa);return a}function P5(){var e=we.H,t=e.useState()[0];return t=typeof t.then=="function"?Rs(t):t,e=e.useState()[0],(gt!==null?gt.memoizedState:null)!==e&&(Le.flags|=1024),t}function T_(){var e=oc!==0;return oc=0,e}function D_(e,t,n){t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~n}function N_(e){if(lc){for(e=e.memoizedState;e!==null;){var t=e.queue;t!==null&&(t.pending=null),e=e.next}lc=!1}Pl=0,Gt=gt=Le=null,Pa=!1,xs=oc=0,ei=null}function yn(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return Gt===null?Le.memoizedState=Gt=e:Gt=Gt.next=e,Gt}function It(){if(gt===null){var e=Le.alternate;e=e!==null?e.memoizedState:null}else e=gt.next;var t=Gt===null?Le.memoizedState:Gt.next;if(t!==null)Gt=t,gt=e;else{if(e===null)throw Le.alternate===null?Error(O(467)):Error(O(310));gt=e,e={memoizedState:gt.memoizedState,baseState:gt.baseState,baseQueue:gt.baseQueue,queue:gt.queue,next:null},Gt===null?Le.memoizedState=Gt=e:Gt=Gt.next=e}return Gt}function Ec(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function Rs(e){var t=xs;return xs+=1,ei===null&&(ei=[]),e=q1(ei,e,t),t=Le,(Gt===null?t.memoizedState:Gt.next)===null&&(t=t.alternate,we.H=t===null||t.memoizedState===null?Mm:H_),e}function Tc(e){if(e!==null&&typeof e=="object"){if(typeof e.then=="function")return Rs(e);if(e.$$typeof===Wl)return un(e)}throw Error(O(438,String(e)))}function z_(e){var t=null,n=Le.updateQueue;if(n!==null&&(t=n.memoCache),t==null){var l=Le.alternate;l!==null&&(l=l.updateQueue,l!==null&&(l=l.memoCache,l!=null&&(t={data:l.data.map(function(o){return o.slice()}),index:0})))}if(t==null&&(t={data:[],index:0}),n===null&&(n=Ec(),Le.updateQueue=n),n.memoCache=t,n=t.data[t.index],n===void 0)for(n=t.data[t.index]=Array(e),l=0;l<e;l++)n[l]=Hp;return t.index++,n}function eo(e,t){return typeof t=="function"?t(e):t}function Or(e){var t=It();return A_(t,gt,e)}function A_(e,t,n){var l=e.queue;if(l===null)throw Error(O(311));l.lastRenderedReducer=n;var o=e.baseQueue,a=l.pending;if(a!==null){if(o!==null){var i=o.next;o.next=a.next,a.next=i}t.baseQueue=o=a,l.pending=null}if(a=e.baseState,o===null)e.memoizedState=a;else{t=o.next;var s=i=null,r=null,p=t,f=!1;do{var b=p.lane&-536870913;if(b!==p.lane?(Qe&b)===b:(Pl&b)===b){var _=p.revertLane;if(_===0)r!==null&&(r=r.next={lane:0,revertLane:0,gesture:null,action:p.action,hasEagerState:p.hasEagerState,eagerState:p.eagerState,next:null}),b===oi&&(f=!0);else if((Pl&_)===_){p=p.next,_===oi&&(f=!0);continue}else b={lane:0,revertLane:p.revertLane,gesture:null,action:p.action,hasEagerState:p.hasEagerState,eagerState:p.eagerState,next:null},r===null?(s=r=b,i=a):r=r.next=b,Le.lanes|=_,Bo|=_;b=p.action,ia&&n(a,b),a=p.hasEagerState?p.eagerState:n(a,b)}else _={lane:b,revertLane:p.revertLane,gesture:p.gesture,action:p.action,hasEagerState:p.hasEagerState,eagerState:p.eagerState,next:null},r===null?(s=r=_,i=a):r=r.next=_,Le.lanes|=b,Bo|=b;p=p.next}while(p!==null&&p!==t);if(r===null?i=a:r.next=s,!Yn(a,e.memoizedState)&&(Kt=!0,f&&(n=Fa,n!==null)))throw n;e.memoizedState=a,e.baseState=i,e.baseQueue=r,l.lastRenderedState=a}return o===null&&(l.lanes=0),[e.memoizedState,l.dispatch]}function Qu(e){var t=It(),n=t.queue;if(n===null)throw Error(O(311));n.lastRenderedReducer=e;var l=n.dispatch,o=n.pending,a=t.memoizedState;if(o!==null){n.pending=null;var i=o=o.next;do a=e(a,i.action),i=i.next;while(i!==o);Yn(a,t.memoizedState)||(Kt=!0),t.memoizedState=a,t.baseQueue===null&&(t.baseState=a),n.lastRenderedState=a}return[a,l]}function J1(e,t,n){var l=Le,o=It(),a=We;if(a){if(n===void 0)throw Error(O(407));n=n()}else n=t();var i=!Yn((gt||o).memoizedState,n);if(i&&(o.memoizedState=n,Kt=!0),o=o.queue,L_(tm.bind(null,l,o,e),[e]),o.getSnapshot!==t||i||Gt!==null&&Gt.memoizedState.tag&1){if(l.flags|=2048,ii(9,{destroy:void 0},em.bind(null,l,o,n,t),null),pt===null)throw Error(O(349));a||(Pl&127)!==0||P1(l,t,n)}return n}function P1(e,t,n){e.flags|=16384,e={getSnapshot:t,value:n},t=Le.updateQueue,t===null?(t=Ec(),Le.updateQueue=t,t.stores=[e]):(n=t.stores,n===null?t.stores=[e]:n.push(e))}function em(e,t,n,l){t.value=n,t.getSnapshot=l,nm(t)&&lm(e)}function tm(e,t,n){return n(function(){nm(t)&&lm(e)})}function nm(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!Yn(e,n)}catch{return!0}}function lm(e){var t=da(e,2);t!==null&&Tn(t,e,2)}function Bd(e){var t=yn();if(typeof e=="function"){var n=e;if(e=n(),ia){po(!0);try{n()}finally{po(!1)}}}return t.memoizedState=t.baseState=e,t.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:eo,lastRenderedState:e},t}function om(e,t,n,l){return e.baseState=n,A_(e,gt,typeof l=="function"?l:eo)}function e2(e,t,n,l,o){if(Nc(e))throw Error(O(485));if(e=t.action,e!==null){var a={payload:o,action:e,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(i){a.listeners.push(i)}};we.T!==null?n(!0):a.isTransition=!1,l(a),n=t.pending,n===null?(a.next=t.pending=a,am(t,a)):(a.next=n.next,t.pending=n.next=a)}}function am(e,t){var n=t.action,l=t.payload,o=e.state;if(t.isTransition){var a=we.T,i={};we.T=i;try{var s=n(o,l),r=we.S;r!==null&&r(i,s),oh(e,t,s)}catch(p){Od(e,t,p)}finally{a!==null&&i.types!==null&&(a.types=i.types),we.T=a}}else try{a=n(o,l),oh(e,t,a)}catch(p){Od(e,t,p)}}function oh(e,t,n){n!==null&&typeof n=="object"&&typeof n.then=="function"?n.then(function(l){ah(e,t,l)},function(l){return Od(e,t,l)}):ah(e,t,n)}function ah(e,t,n){t.status="fulfilled",t.value=n,im(t),e.state=n,t=e.pending,t!==null&&(n=t.next,n===t?e.pending=null:(n=n.next,t.next=n,am(e,n)))}function Od(e,t,n){var l=e.pending;if(e.pending=null,l!==null){l=l.next;do t.status="rejected",t.reason=n,im(t),t=t.next;while(t!==l)}e.action=null}function im(e){e=e.listeners;for(var t=0;t<e.length;t++)(0,e[t])()}function sm(e,t){return t}function ih(e,t){if(We){var n=pt.formState;if(n!==null){e:{var l=Le;if(We){if(Mt){t:{for(var o=Mt,a=nl;o.nodeType!==8;){if(!a){o=null;break t}if(o=ol(o.nextSibling),o===null){o=null;break t}}a=o.data,o=a==="F!"||a==="F"?o:null}if(o){Mt=ol(o.nextSibling),l=o.data==="F!";break e}}Lo(l)}l=!1}l&&(t=n[0])}}return n=yn(),n.memoizedState=n.baseState=t,l={pending:null,lanes:0,dispatch:null,lastRenderedReducer:sm,lastRenderedState:t},n.queue=l,n=km.bind(null,Le,l),l.dispatch=n,l=Bd(!1),a=$_.bind(null,Le,!1,l.queue),l=yn(),o={state:t,dispatch:null,action:e,pending:null},l.queue=o,n=e2.bind(null,Le,o,a,n),o.dispatch=n,l.memoizedState=e,[t,n,!1]}function sh(e){var t=It();return rm(t,gt,e)}function rm(e,t,n){if(t=A_(e,t,sm)[0],e=Or(eo)[0],typeof t=="object"&&t!==null&&typeof t.then=="function")try{var l=Rs(t)}catch(i){throw i===mi?Mc:i}else l=t;t=It();var o=t.queue,a=o.dispatch;return n!==t.memoizedState&&(Le.flags|=2048,ii(9,{destroy:void 0},t2.bind(null,o,n),null)),[l,a,e]}function t2(e,t){e.action=t}function rh(e){var t=It(),n=gt;if(n!==null)return rm(t,n,e);It(),t=t.memoizedState,n=It();var l=n.queue.dispatch;return n.memoizedState=e,[t,l,!1]}function ii(e,t,n,l){return e={tag:e,create:n,deps:l,inst:t,next:null},t=Le.updateQueue,t===null&&(t=Ec(),Le.updateQueue=t),n=t.lastEffect,n===null?t.lastEffect=e.next=e:(l=n.next,n.next=e,e.next=l,t.lastEffect=e),e}function cm(){return It().memoizedState}function $r(e,t,n,l){var o=yn();Le.flags|=e,o.memoizedState=ii(1|t,{destroy:void 0},n,l===void 0?null:l)}function Dc(e,t,n,l){var o=It();l=l===void 0?null:l;var a=o.memoizedState.inst;gt!==null&&l!==null&&M_(l,gt.memoizedState.deps)?o.memoizedState=ii(t,a,n,l):(Le.flags|=e,o.memoizedState=ii(1|t,a,n,l))}function ch(e,t){$r(8390656,8,e,t)}function L_(e,t){Dc(2048,8,e,t)}function n2(e){Le.flags|=4;var t=Le.updateQueue;if(t===null)t=Ec(),Le.updateQueue=t,t.events=[e];else{var n=t.events;n===null?t.events=[e]:n.push(e)}}function um(e){var t=It().memoizedState;return n2({ref:t,nextImpl:e}),function(){if((lt&2)!==0)throw Error(O(440));return t.impl.apply(void 0,arguments)}}function dm(e,t){return Dc(4,2,e,t)}function _m(e,t){return Dc(4,4,e,t)}function fm(e,t){if(typeof t=="function"){e=e();var n=t(e);return function(){typeof n=="function"?n():t(null)}}if(t!=null)return e=e(),t.current=e,function(){t.current=null}}function hm(e,t,n){n=n!=null?n.concat([e]):null,Dc(4,4,fm.bind(null,t,e),n)}function R_(){}function mm(e,t){var n=It();t=t===void 0?null:t;var l=n.memoizedState;return t!==null&&M_(t,l[1])?l[0]:(n.memoizedState=[e,t],e)}function gm(e,t){var n=It();t=t===void 0?null:t;var l=n.memoizedState;if(t!==null&&M_(t,l[1]))return l[0];if(l=e(),ia){po(!0);try{e()}finally{po(!1)}}return n.memoizedState=[l,t],l}function B_(e,t,n){return n===void 0||(Pl&1073741824)!==0&&(Qe&261930)===0?e.memoizedState=t:(e.memoizedState=n,e=og(),Le.lanes|=e,Bo|=e,n)}function ym(e,t,n,l){return Yn(n,t)?n:ai.current!==null?(e=B_(e,n,l),Yn(e,t)||(Kt=!0),e):(Pl&42)===0||(Pl&1073741824)!==0&&(Qe&261930)===0?(Kt=!0,e.memoizedState=n):(e=og(),Le.lanes|=e,Bo|=e,t)}function pm(e,t,n,l,o){var a=ot.p;ot.p=a!==0&&8>a?a:8;var i=we.T,s={};we.T=s,$_(e,!1,t,n);try{var r=o(),p=we.S;if(p!==null&&p(s,r),r!==null&&typeof r=="object"&&typeof r.then=="function"){var f=F5(r,l);ss(e,t,f,Un(e))}else ss(e,t,l,Un(e))}catch(b){ss(e,t,{then:function(){},status:"rejected",reason:b},Un())}finally{ot.p=a,i!==null&&s.types!==null&&(i.types=s.types),we.T=i}}function l2(){}function $d(e,t,n,l){if(e.tag!==5)throw Error(O(476));var o=bm(e).queue;pm(e,o,t,Jo,n===null?l2:function(){return xm(e),n(l)})}function bm(e){var t=e.memoizedState;if(t!==null)return t;t={memoizedState:Jo,baseState:Jo,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:eo,lastRenderedState:Jo},next:null};var n={};return t.next={memoizedState:n,baseState:n,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:eo,lastRenderedState:n},next:null},e.memoizedState=t,e=e.alternate,e!==null&&(e.memoizedState=t),t}function xm(e){var t=bm(e);t.next===null&&(t=e.alternate.memoizedState),ss(e,t.next.queue,{},Un())}function O_(){return un(Ss)}function vm(){return It().memoizedState}function wm(){return It().memoizedState}function o2(e){for(var t=e.return;t!==null;){switch(t.tag){case 24:case 3:var n=Un();e=Co(n);var l=Mo(t,e,n);l!==null&&(Tn(l,t,n),os(l,t,n)),t={cache:v_()},e.payload=t;return}t=t.return}}function a2(e,t,n){var l=Un();n={lane:l,revertLane:0,gesture:null,action:n,hasEagerState:!1,eagerState:null,next:null},Nc(e)?Sm(t,n):(n=y_(e,t,n,l),n!==null&&(Tn(n,e,l),Cm(n,t,l)))}function km(e,t,n){var l=Un();ss(e,t,n,l)}function ss(e,t,n,l){var o={lane:l,revertLane:0,gesture:null,action:n,hasEagerState:!1,eagerState:null,next:null};if(Nc(e))Sm(t,o);else{var a=e.alternate;if(e.lanes===0&&(a===null||a.lanes===0)&&(a=t.lastRenderedReducer,a!==null))try{var i=t.lastRenderedState,s=a(i,n);if(o.hasEagerState=!0,o.eagerState=s,Yn(s,i))return Cc(e,t,o,0),pt===null&&Sc(),!1}catch{}if(n=y_(e,t,o,l),n!==null)return Tn(n,e,l),Cm(n,t,l),!0}return!1}function $_(e,t,n,l){if(l={lane:2,revertLane:W_(),gesture:null,action:l,hasEagerState:!1,eagerState:null,next:null},Nc(e)){if(t)throw Error(O(479))}else t=y_(e,n,l,2),t!==null&&Tn(t,e,2)}function Nc(e){var t=e.alternate;return e===Le||t!==null&&t===Le}function Sm(e,t){Pa=lc=!0;var n=e.pending;n===null?t.next=t:(t.next=n.next,n.next=t),e.pending=t}function Cm(e,t,n){if((n&4194048)!==0){var l=t.lanes;l&=e.pendingLanes,n|=l,t.lanes=n,u1(e,n)}}var vs={readContext:un,use:Tc,useCallback:$t,useContext:$t,useEffect:$t,useImperativeHandle:$t,useLayoutEffect:$t,useInsertionEffect:$t,useMemo:$t,useReducer:$t,useRef:$t,useState:$t,useDebugValue:$t,useDeferredValue:$t,useTransition:$t,useSyncExternalStore:$t,useId:$t,useHostTransitionStatus:$t,useFormState:$t,useActionState:$t,useOptimistic:$t,useMemoCache:$t,useCacheRefresh:$t};vs.useEffectEvent=$t;var Mm={readContext:un,use:Tc,useCallback:function(e,t){return yn().memoizedState=[e,t===void 0?null:t],e},useContext:un,useEffect:ch,useImperativeHandle:function(e,t,n){n=n!=null?n.concat([e]):null,$r(4194308,4,fm.bind(null,t,e),n)},useLayoutEffect:function(e,t){return $r(4194308,4,e,t)},useInsertionEffect:function(e,t){$r(4,2,e,t)},useMemo:function(e,t){var n=yn();t=t===void 0?null:t;var l=e();if(ia){po(!0);try{e()}finally{po(!1)}}return n.memoizedState=[l,t],l},useReducer:function(e,t,n){var l=yn();if(n!==void 0){var o=n(t);if(ia){po(!0);try{n(t)}finally{po(!1)}}}else o=t;return l.memoizedState=l.baseState=o,e={pending:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:o},l.queue=e,e=e.dispatch=a2.bind(null,Le,e),[l.memoizedState,e]},useRef:function(e){var t=yn();return e={current:e},t.memoizedState=e},useState:function(e){e=Bd(e);var t=e.queue,n=km.bind(null,Le,t);return t.dispatch=n,[e.memoizedState,n]},useDebugValue:R_,useDeferredValue:function(e,t){var n=yn();return B_(n,e,t)},useTransition:function(){var e=Bd(!1);return e=pm.bind(null,Le,e.queue,!0,!1),yn().memoizedState=e,[!1,e]},useSyncExternalStore:function(e,t,n){var l=Le,o=yn();if(We){if(n===void 0)throw Error(O(407));n=n()}else{if(n=t(),pt===null)throw Error(O(349));(Qe&127)!==0||P1(l,t,n)}o.memoizedState=n;var a={value:n,getSnapshot:t};return o.queue=a,ch(tm.bind(null,l,a,e),[e]),l.flags|=2048,ii(9,{destroy:void 0},em.bind(null,l,a,n,t),null),n},useId:function(){var e=yn(),t=pt.identifierPrefix;if(We){var n=El,l=Ml;n=(l&~(1<<32-Hn(l)-1)).toString(32)+n,t="_"+t+"R_"+n,n=oc++,0<n&&(t+="H"+n.toString(32)),t+="_"}else n=J5++,t="_"+t+"r_"+n.toString(32)+"_";return e.memoizedState=t},useHostTransitionStatus:O_,useFormState:ih,useActionState:ih,useOptimistic:function(e){var t=yn();t.memoizedState=t.baseState=e;var n={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return t.queue=n,t=$_.bind(null,Le,!0,n),n.dispatch=t,[e,t]},useMemoCache:z_,useCacheRefresh:function(){return yn().memoizedState=o2.bind(null,Le)},useEffectEvent:function(e){var t=yn(),n={impl:e};return t.memoizedState=n,function(){if((lt&2)!==0)throw Error(O(440));return n.impl.apply(void 0,arguments)}}},H_={readContext:un,use:Tc,useCallback:mm,useContext:un,useEffect:L_,useImperativeHandle:hm,useInsertionEffect:dm,useLayoutEffect:_m,useMemo:gm,useReducer:Or,useRef:cm,useState:function(){return Or(eo)},useDebugValue:R_,useDeferredValue:function(e,t){var n=It();return ym(n,gt.memoizedState,e,t)},useTransition:function(){var e=Or(eo)[0],t=It().memoizedState;return[typeof e=="boolean"?e:Rs(e),t]},useSyncExternalStore:J1,useId:vm,useHostTransitionStatus:O_,useFormState:sh,useActionState:sh,useOptimistic:function(e,t){var n=It();return om(n,gt,e,t)},useMemoCache:z_,useCacheRefresh:wm};H_.useEffectEvent=um;var Em={readContext:un,use:Tc,useCallback:mm,useContext:un,useEffect:L_,useImperativeHandle:hm,useInsertionEffect:dm,useLayoutEffect:_m,useMemo:gm,useReducer:Qu,useRef:cm,useState:function(){return Qu(eo)},useDebugValue:R_,useDeferredValue:function(e,t){var n=It();return gt===null?B_(n,e,t):ym(n,gt.memoizedState,e,t)},useTransition:function(){var e=Qu(eo)[0],t=It().memoizedState;return[typeof e=="boolean"?e:Rs(e),t]},useSyncExternalStore:J1,useId:vm,useHostTransitionStatus:O_,useFormState:rh,useActionState:rh,useOptimistic:function(e,t){var n=It();return gt!==null?om(n,gt,e,t):(n.baseState=e,[e,n.queue.dispatch])},useMemoCache:z_,useCacheRefresh:wm};Em.useEffectEvent=um;function Wu(e,t,n,l){t=e.memoizedState,n=n(l,t),n=n==null?t:Et({},t,n),e.memoizedState=n,e.lanes===0&&(e.updateQueue.baseState=n)}var Hd={enqueueSetState:function(e,t,n){e=e._reactInternals;var l=Un(),o=Co(l);o.payload=t,n!=null&&(o.callback=n),t=Mo(e,o,l),t!==null&&(Tn(t,e,l),os(t,e,l))},enqueueReplaceState:function(e,t,n){e=e._reactInternals;var l=Un(),o=Co(l);o.tag=1,o.payload=t,n!=null&&(o.callback=n),t=Mo(e,o,l),t!==null&&(Tn(t,e,l),os(t,e,l))},enqueueForceUpdate:function(e,t){e=e._reactInternals;var n=Un(),l=Co(n);l.tag=2,t!=null&&(l.callback=t),t=Mo(e,l,n),t!==null&&(Tn(t,e,n),os(t,e,n))}};function uh(e,t,n,l,o,a,i){return e=e.stateNode,typeof e.shouldComponentUpdate=="function"?e.shouldComponentUpdate(l,a,i):t.prototype&&t.prototype.isPureReactComponent?!gs(n,l)||!gs(o,a):!0}function dh(e,t,n,l){e=t.state,typeof t.componentWillReceiveProps=="function"&&t.componentWillReceiveProps(n,l),typeof t.UNSAFE_componentWillReceiveProps=="function"&&t.UNSAFE_componentWillReceiveProps(n,l),t.state!==e&&Hd.enqueueReplaceState(t,t.state,null)}function sa(e,t){var n=t;if("ref"in t){n={};for(var l in t)l!=="ref"&&(n[l]=t[l])}if(e=e.defaultProps){n===t&&(n=Et({},n));for(var o in e)n[o]===void 0&&(n[o]=e[o])}return n}function Tm(e){Kr(e)}function Dm(e){console.error(e)}function Nm(e){Kr(e)}function ac(e,t){try{var n=e.onUncaughtError;n(t.value,{componentStack:t.stack})}catch(l){setTimeout(function(){throw l})}}function _h(e,t,n){try{var l=e.onCaughtError;l(n.value,{componentStack:n.stack,errorBoundary:t.tag===1?t.stateNode:null})}catch(o){setTimeout(function(){throw o})}}function Ud(e,t,n){return n=Co(n),n.tag=3,n.payload={element:null},n.callback=function(){ac(e,t)},n}function zm(e){return e=Co(e),e.tag=3,e}function Am(e,t,n,l){var o=n.type.getDerivedStateFromError;if(typeof o=="function"){var a=l.value;e.payload=function(){return o(a)},e.callback=function(){_h(t,n,l)}}var i=n.stateNode;i!==null&&typeof i.componentDidCatch=="function"&&(e.callback=function(){_h(t,n,l),typeof o!="function"&&(Eo===null?Eo=new Set([this]):Eo.add(this));var s=l.stack;this.componentDidCatch(l.value,{componentStack:s!==null?s:""})})}function i2(e,t,n,l,o){if(n.flags|=32768,l!==null&&typeof l=="object"&&typeof l.then=="function"){if(t=n.alternate,t!==null&&hi(t,n,o,!0),n=jn.current,n!==null){switch(n.tag){case 31:case 13:return ll===null?uc():n.alternate===null&&Ht===0&&(Ht=3),n.flags&=-257,n.flags|=65536,n.lanes=o,l===ec?n.flags|=16384:(t=n.updateQueue,t===null?n.updateQueue=new Set([l]):t.add(l),ld(e,l,o)),!1;case 22:return n.flags|=65536,l===ec?n.flags|=16384:(t=n.updateQueue,t===null?(t={transitions:null,markerInstances:null,retryQueue:new Set([l])},n.updateQueue=t):(n=t.retryQueue,n===null?t.retryQueue=new Set([l]):n.add(l)),ld(e,l,o)),!1}throw Error(O(435,n.tag))}return ld(e,l,o),uc(),!1}if(We)return t=jn.current,t!==null?((t.flags&65536)===0&&(t.flags|=256),t.flags|=65536,t.lanes=o,l!==Md&&(e=Error(O(422),{cause:l}),ps(tl(e,n)))):(l!==Md&&(t=Error(O(423),{cause:l}),ps(tl(t,n))),e=e.current.alternate,e.flags|=65536,o&=-o,e.lanes|=o,l=tl(l,n),o=Ud(e.stateNode,l,o),qu(e,o),Ht!==4&&(Ht=2)),!1;var a=Error(O(520),{cause:l});if(a=tl(a,n),us===null?us=[a]:us.push(a),Ht!==4&&(Ht=2),t===null)return!0;l=tl(l,n),n=t;do{switch(n.tag){case 3:return n.flags|=65536,e=o&-o,n.lanes|=e,e=Ud(n.stateNode,l,e),qu(n,e),!1;case 1:if(t=n.type,a=n.stateNode,(n.flags&128)===0&&(typeof t.getDerivedStateFromError=="function"||a!==null&&typeof a.componentDidCatch=="function"&&(Eo===null||!Eo.has(a))))return n.flags|=65536,o&=-o,n.lanes|=o,o=zm(o),Am(o,e,n,l),qu(n,o),!1}n=n.return}while(n!==null);return!1}var U_=Error(O(461)),Kt=!1;function sn(e,t,n,l){t.child=e===null?W1(t,null,n,l):aa(t,e.child,n,l)}function fh(e,t,n,l,o){n=n.render;var a=t.ref;if("ref"in l){var i={};for(var s in l)s!=="ref"&&(i[s]=l[s])}else i=l;return oa(t),l=E_(e,t,n,i,a,o),s=T_(),e!==null&&!Kt?(D_(e,t,o),to(e,t,o)):(We&&s&&b_(t),t.flags|=1,sn(e,t,l,o),t.child)}function hh(e,t,n,l,o){if(e===null){var a=n.type;return typeof a=="function"&&!p_(a)&&a.defaultProps===void 0&&n.compare===null?(t.tag=15,t.type=a,Lm(e,t,a,l,o)):(e=Rr(n.type,null,l,t,t.mode,o),e.ref=t.ref,e.return=t,t.child=e)}if(a=e.child,!Y_(e,o)){var i=a.memoizedProps;if(n=n.compare,n=n!==null?n:gs,n(i,l)&&e.ref===t.ref)return to(e,t,o)}return t.flags|=1,e=Zl(a,l),e.ref=t.ref,e.return=t,t.child=e}function Lm(e,t,n,l,o){if(e!==null){var a=e.memoizedProps;if(gs(a,l)&&e.ref===t.ref)if(Kt=!1,t.pendingProps=l=a,Y_(e,o))(e.flags&131072)!==0&&(Kt=!0);else return t.lanes=e.lanes,to(e,t,o)}return Yd(e,t,n,l,o)}function Rm(e,t,n,l){var o=l.children,a=e!==null?e.memoizedState:null;if(e===null&&t.stateNode===null&&(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),l.mode==="hidden"){if((t.flags&128)!==0){if(a=a!==null?a.baseLanes|n:n,e!==null){for(l=t.child=e.child,o=0;l!==null;)o=o|l.lanes|l.childLanes,l=l.sibling;l=o&~a}else l=0,t.child=null;return mh(e,t,a,n,l)}if((n&536870912)!==0)t.memoizedState={baseLanes:0,cachePool:null},e!==null&&Br(t,a!==null?a.cachePool:null),a!==null?lh(t,a):Ld(),Z1(t);else return l=t.lanes=536870912,mh(e,t,a!==null?a.baseLanes|n:n,n,l)}else a!==null?(Br(t,a.cachePool),lh(t,a),go(t),t.memoizedState=null):(e!==null&&Br(t,null),Ld(),go(t));return sn(e,t,o,n),t.child}function Ji(e,t){return e!==null&&e.tag===22||t.stateNode!==null||(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),t.sibling}function mh(e,t,n,l,o){var a=w_();return a=a===null?null:{parent:Zt._currentValue,pool:a},t.memoizedState={baseLanes:n,cachePool:a},e!==null&&Br(t,null),Ld(),Z1(t),e!==null&&hi(e,t,l,!0),t.childLanes=o,null}function Hr(e,t){return t=ic({mode:t.mode,children:t.children},e.mode),t.ref=e.ref,e.child=t,t.return=e,t}function gh(e,t,n){return aa(t,e.child,null,n),e=Hr(t,t.pendingProps),e.flags|=2,Ln(t),t.memoizedState=null,e}function s2(e,t,n){var l=t.pendingProps,o=(t.flags&128)!==0;if(t.flags&=-129,e===null){if(We){if(l.mode==="hidden")return e=Hr(t,l),t.lanes=536870912,Ji(null,e);if(Rd(t),(e=Mt)?(e=Mg(e,nl),e=e!==null&&e.data==="&"?e:null,e!==null&&(t.memoizedState={dehydrated:e,treeContext:Ao!==null?{id:Ml,overflow:El}:null,retryLane:536870912,hydrationErrors:null},n=U1(e),n.return=t,t.child=n,cn=t,Mt=null)):e=null,e===null)throw Lo(t);return t.lanes=536870912,null}return Hr(t,l)}var a=e.memoizedState;if(a!==null){var i=a.dehydrated;if(Rd(t),o)if(t.flags&256)t.flags&=-257,t=gh(e,t,n);else if(t.memoizedState!==null)t.child=e.child,t.flags|=128,t=null;else throw Error(O(558));else if(Kt||hi(e,t,n,!1),o=(n&e.childLanes)!==0,Kt||o){if(l=pt,l!==null&&(i=d1(l,n),i!==0&&i!==a.retryLane))throw a.retryLane=i,da(e,i),Tn(l,e,i),U_;uc(),t=gh(e,t,n)}else e=a.treeContext,Mt=ol(i.nextSibling),cn=t,We=!0,So=null,nl=!1,e!==null&&j1(t,e),t=Hr(t,l),t.flags|=4096;return t}return e=Zl(e.child,{mode:l.mode,children:l.children}),e.ref=t.ref,t.child=e,e.return=t,e}function Ur(e,t){var n=t.ref;if(n===null)e!==null&&e.ref!==null&&(t.flags|=4194816);else{if(typeof n!="function"&&typeof n!="object")throw Error(O(284));(e===null||e.ref!==n)&&(t.flags|=4194816)}}function Yd(e,t,n,l,o){return oa(t),n=E_(e,t,n,l,void 0,o),l=T_(),e!==null&&!Kt?(D_(e,t,o),to(e,t,o)):(We&&l&&b_(t),t.flags|=1,sn(e,t,n,o),t.child)}function yh(e,t,n,l,o,a){return oa(t),t.updateQueue=null,n=F1(t,l,n,o),K1(e),l=T_(),e!==null&&!Kt?(D_(e,t,a),to(e,t,a)):(We&&l&&b_(t),t.flags|=1,sn(e,t,n,a),t.child)}function ph(e,t,n,l,o){if(oa(t),t.stateNode===null){var a=qa,i=n.contextType;typeof i=="object"&&i!==null&&(a=un(i)),a=new n(l,a),t.memoizedState=a.state!==null&&a.state!==void 0?a.state:null,a.updater=Hd,t.stateNode=a,a._reactInternals=t,a=t.stateNode,a.props=l,a.state=t.memoizedState,a.refs={},S_(t),i=n.contextType,a.context=typeof i=="object"&&i!==null?un(i):qa,a.state=t.memoizedState,i=n.getDerivedStateFromProps,typeof i=="function"&&(Wu(t,n,i,l),a.state=t.memoizedState),typeof n.getDerivedStateFromProps=="function"||typeof a.getSnapshotBeforeUpdate=="function"||typeof a.UNSAFE_componentWillMount!="function"&&typeof a.componentWillMount!="function"||(i=a.state,typeof a.componentWillMount=="function"&&a.componentWillMount(),typeof a.UNSAFE_componentWillMount=="function"&&a.UNSAFE_componentWillMount(),i!==a.state&&Hd.enqueueReplaceState(a,a.state,null),is(t,l,a,o),as(),a.state=t.memoizedState),typeof a.componentDidMount=="function"&&(t.flags|=4194308),l=!0}else if(e===null){a=t.stateNode;var s=t.memoizedProps,r=sa(n,s);a.props=r;var p=a.context,f=n.contextType;i=qa,typeof f=="object"&&f!==null&&(i=un(f));var b=n.getDerivedStateFromProps;f=typeof b=="function"||typeof a.getSnapshotBeforeUpdate=="function",s=t.pendingProps!==s,f||typeof a.UNSAFE_componentWillReceiveProps!="function"&&typeof a.componentWillReceiveProps!="function"||(s||p!==i)&&dh(t,a,l,i),fo=!1;var _=t.memoizedState;a.state=_,is(t,l,a,o),as(),p=t.memoizedState,s||_!==p||fo?(typeof b=="function"&&(Wu(t,n,b,l),p=t.memoizedState),(r=fo||uh(t,n,r,l,_,p,i))?(f||typeof a.UNSAFE_componentWillMount!="function"&&typeof a.componentWillMount!="function"||(typeof a.componentWillMount=="function"&&a.componentWillMount(),typeof a.UNSAFE_componentWillMount=="function"&&a.UNSAFE_componentWillMount()),typeof a.componentDidMount=="function"&&(t.flags|=4194308)):(typeof a.componentDidMount=="function"&&(t.flags|=4194308),t.memoizedProps=l,t.memoizedState=p),a.props=l,a.state=p,a.context=i,l=r):(typeof a.componentDidMount=="function"&&(t.flags|=4194308),l=!1)}else{a=t.stateNode,zd(e,t),i=t.memoizedProps,f=sa(n,i),a.props=f,b=t.pendingProps,_=a.context,p=n.contextType,r=qa,typeof p=="object"&&p!==null&&(r=un(p)),s=n.getDerivedStateFromProps,(p=typeof s=="function"||typeof a.getSnapshotBeforeUpdate=="function")||typeof a.UNSAFE_componentWillReceiveProps!="function"&&typeof a.componentWillReceiveProps!="function"||(i!==b||_!==r)&&dh(t,a,l,r),fo=!1,_=t.memoizedState,a.state=_,is(t,l,a,o),as();var w=t.memoizedState;i!==b||_!==w||fo||e!==null&&e.dependencies!==null&&Pr(e.dependencies)?(typeof s=="function"&&(Wu(t,n,s,l),w=t.memoizedState),(f=fo||uh(t,n,f,l,_,w,r)||e!==null&&e.dependencies!==null&&Pr(e.dependencies))?(p||typeof a.UNSAFE_componentWillUpdate!="function"&&typeof a.componentWillUpdate!="function"||(typeof a.componentWillUpdate=="function"&&a.componentWillUpdate(l,w,r),typeof a.UNSAFE_componentWillUpdate=="function"&&a.UNSAFE_componentWillUpdate(l,w,r)),typeof a.componentDidUpdate=="function"&&(t.flags|=4),typeof a.getSnapshotBeforeUpdate=="function"&&(t.flags|=1024)):(typeof a.componentDidUpdate!="function"||i===e.memoizedProps&&_===e.memoizedState||(t.flags|=4),typeof a.getSnapshotBeforeUpdate!="function"||i===e.memoizedProps&&_===e.memoizedState||(t.flags|=1024),t.memoizedProps=l,t.memoizedState=w),a.props=l,a.state=w,a.context=r,l=f):(typeof a.componentDidUpdate!="function"||i===e.memoizedProps&&_===e.memoizedState||(t.flags|=4),typeof a.getSnapshotBeforeUpdate!="function"||i===e.memoizedProps&&_===e.memoizedState||(t.flags|=1024),l=!1)}return a=l,Ur(e,t),l=(t.flags&128)!==0,a||l?(a=t.stateNode,n=l&&typeof n.getDerivedStateFromError!="function"?null:a.render(),t.flags|=1,e!==null&&l?(t.child=aa(t,e.child,null,o),t.child=aa(t,null,n,o)):sn(e,t,n,o),t.memoizedState=a.state,e=t.child):e=to(e,t,o),e}function bh(e,t,n,l){return la(),t.flags|=256,sn(e,t,n,l),t.child}var Gu={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function Vu(e){return{baseLanes:e,cachePool:I1()}}function Zu(e,t,n){return e=e!==null?e.childLanes&~n:0,t&&(e|=Bn),e}function Bm(e,t,n){var l=t.pendingProps,o=!1,a=(t.flags&128)!==0,i;if((i=a)||(i=e!==null&&e.memoizedState===null?!1:(Xt.current&2)!==0),i&&(o=!0,t.flags&=-129),i=(t.flags&32)!==0,t.flags&=-33,e===null){if(We){if(o?mo(t):go(t),(e=Mt)?(e=Mg(e,nl),e=e!==null&&e.data!=="&"?e:null,e!==null&&(t.memoizedState={dehydrated:e,treeContext:Ao!==null?{id:Ml,overflow:El}:null,retryLane:536870912,hydrationErrors:null},n=U1(e),n.return=t,t.child=n,cn=t,Mt=null)):e=null,e===null)throw Lo(t);return e_(e)?t.lanes=32:t.lanes=536870912,null}var s=l.children;return l=l.fallback,o?(go(t),o=t.mode,s=ic({mode:"hidden",children:s},o),l=Po(l,o,n,null),s.return=t,l.return=t,s.sibling=l,t.child=s,l=t.child,l.memoizedState=Vu(n),l.childLanes=Zu(e,i,n),t.memoizedState=Gu,Ji(null,l)):(mo(t),jd(t,s))}var r=e.memoizedState;if(r!==null&&(s=r.dehydrated,s!==null)){if(a)t.flags&256?(mo(t),t.flags&=-257,t=Ku(e,t,n)):t.memoizedState!==null?(go(t),t.child=e.child,t.flags|=128,t=null):(go(t),s=l.fallback,o=t.mode,l=ic({mode:"visible",children:l.children},o),s=Po(s,o,n,null),s.flags|=2,l.return=t,s.return=t,l.sibling=s,t.child=l,aa(t,e.child,null,n),l=t.child,l.memoizedState=Vu(n),l.childLanes=Zu(e,i,n),t.memoizedState=Gu,t=Ji(null,l));else if(mo(t),e_(s)){if(i=s.nextSibling&&s.nextSibling.dataset,i)var p=i.dgst;i=p,l=Error(O(419)),l.stack="",l.digest=i,ps({value:l,source:null,stack:null}),t=Ku(e,t,n)}else if(Kt||hi(e,t,n,!1),i=(n&e.childLanes)!==0,Kt||i){if(i=pt,i!==null&&(l=d1(i,n),l!==0&&l!==r.retryLane))throw r.retryLane=l,da(e,l),Tn(i,e,l),U_;Pd(s)||uc(),t=Ku(e,t,n)}else Pd(s)?(t.flags|=192,t.child=e.child,t=null):(e=r.treeContext,Mt=ol(s.nextSibling),cn=t,We=!0,So=null,nl=!1,e!==null&&j1(t,e),t=jd(t,l.children),t.flags|=4096);return t}return o?(go(t),s=l.fallback,o=t.mode,r=e.child,p=r.sibling,l=Zl(r,{mode:"hidden",children:l.children}),l.subtreeFlags=r.subtreeFlags&65011712,p!==null?s=Zl(p,s):(s=Po(s,o,n,null),s.flags|=2),s.return=t,l.return=t,l.sibling=s,t.child=l,Ji(null,l),l=t.child,s=e.child.memoizedState,s===null?s=Vu(n):(o=s.cachePool,o!==null?(r=Zt._currentValue,o=o.parent!==r?{parent:r,pool:r}:o):o=I1(),s={baseLanes:s.baseLanes|n,cachePool:o}),l.memoizedState=s,l.childLanes=Zu(e,i,n),t.memoizedState=Gu,Ji(e.child,l)):(mo(t),n=e.child,e=n.sibling,n=Zl(n,{mode:"visible",children:l.children}),n.return=t,n.sibling=null,e!==null&&(i=t.deletions,i===null?(t.deletions=[e],t.flags|=16):i.push(e)),t.child=n,t.memoizedState=null,n)}function jd(e,t){return t=ic({mode:"visible",children:t},e.mode),t.return=e,e.child=t}function ic(e,t){return e=Rn(22,e,null,t),e.lanes=0,e}function Ku(e,t,n){return aa(t,e.child,null,n),e=jd(t,t.pendingProps.children),e.flags|=2,t.memoizedState=null,e}function xh(e,t,n){e.lanes|=t;var l=e.alternate;l!==null&&(l.lanes|=t),Td(e.return,t,n)}function Fu(e,t,n,l,o,a){var i=e.memoizedState;i===null?e.memoizedState={isBackwards:t,rendering:null,renderingStartTime:0,last:l,tail:n,tailMode:o,treeForkCount:a}:(i.isBackwards=t,i.rendering=null,i.renderingStartTime=0,i.last=l,i.tail=n,i.tailMode=o,i.treeForkCount=a)}function Om(e,t,n){var l=t.pendingProps,o=l.revealOrder,a=l.tail;l=l.children;var i=Xt.current,s=(i&2)!==0;if(s?(i=i&1|2,t.flags|=128):i&=1,kt(Xt,i),sn(e,t,l,n),l=We?ys:0,!s&&e!==null&&(e.flags&128)!==0)e:for(e=t.child;e!==null;){if(e.tag===13)e.memoizedState!==null&&xh(e,n,t);else if(e.tag===19)xh(e,n,t);else if(e.child!==null){e.child.return=e,e=e.child;continue}if(e===t)break e;for(;e.sibling===null;){if(e.return===null||e.return===t)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}switch(o){case"forwards":for(n=t.child,o=null;n!==null;)e=n.alternate,e!==null&&nc(e)===null&&(o=n),n=n.sibling;n=o,n===null?(o=t.child,t.child=null):(o=n.sibling,n.sibling=null),Fu(t,!1,o,n,a,l);break;case"backwards":case"unstable_legacy-backwards":for(n=null,o=t.child,t.child=null;o!==null;){if(e=o.alternate,e!==null&&nc(e)===null){t.child=o;break}e=o.sibling,o.sibling=n,n=o,o=e}Fu(t,!0,n,null,a,l);break;case"together":Fu(t,!1,null,null,void 0,l);break;default:t.memoizedState=null}return t.child}function to(e,t,n){if(e!==null&&(t.dependencies=e.dependencies),Bo|=t.lanes,(n&t.childLanes)===0)if(e!==null){if(hi(e,t,n,!1),(n&t.childLanes)===0)return null}else return null;if(e!==null&&t.child!==e.child)throw Error(O(153));if(t.child!==null){for(e=t.child,n=Zl(e,e.pendingProps),t.child=n,n.return=t;e.sibling!==null;)e=e.sibling,n=n.sibling=Zl(e,e.pendingProps),n.return=t;n.sibling=null}return t.child}function Y_(e,t){return(e.lanes&t)!==0?!0:(e=e.dependencies,!!(e!==null&&Pr(e)))}function r2(e,t,n){switch(t.tag){case 3:Wr(t,t.stateNode.containerInfo),ho(t,Zt,e.memoizedState.cache),la();break;case 27:case 5:md(t);break;case 4:Wr(t,t.stateNode.containerInfo);break;case 10:ho(t,t.type,t.memoizedProps.value);break;case 31:if(t.memoizedState!==null)return t.flags|=128,Rd(t),null;break;case 13:var l=t.memoizedState;if(l!==null)return l.dehydrated!==null?(mo(t),t.flags|=128,null):(n&t.child.childLanes)!==0?Bm(e,t,n):(mo(t),e=to(e,t,n),e!==null?e.sibling:null);mo(t);break;case 19:var o=(e.flags&128)!==0;if(l=(n&t.childLanes)!==0,l||(hi(e,t,n,!1),l=(n&t.childLanes)!==0),o){if(l)return Om(e,t,n);t.flags|=128}if(o=t.memoizedState,o!==null&&(o.rendering=null,o.tail=null,o.lastEffect=null),kt(Xt,Xt.current),l)break;return null;case 22:return t.lanes=0,Rm(e,t,n,t.pendingProps);case 24:ho(t,Zt,e.memoizedState.cache)}return to(e,t,n)}function $m(e,t,n){if(e!==null)if(e.memoizedProps!==t.pendingProps)Kt=!0;else{if(!Y_(e,n)&&(t.flags&128)===0)return Kt=!1,r2(e,t,n);Kt=(e.flags&131072)!==0}else Kt=!1,We&&(t.flags&1048576)!==0&&Y1(t,ys,t.index);switch(t.lanes=0,t.tag){case 16:e:{var l=t.pendingProps;if(e=Ko(t.elementType),t.type=e,typeof e=="function")p_(e)?(l=sa(e,l),t.tag=1,t=ph(null,t,e,l,n)):(t.tag=0,t=Yd(null,t,e,l,n));else{if(e!=null){var o=e.$$typeof;if(o===o_){t.tag=11,t=fh(null,t,e,l,n);break e}else if(o===a_){t.tag=14,t=hh(null,t,e,l,n);break e}}throw t=fd(e)||e,Error(O(306,t,""))}}return t;case 0:return Yd(e,t,t.type,t.pendingProps,n);case 1:return l=t.type,o=sa(l,t.pendingProps),ph(e,t,l,o,n);case 3:e:{if(Wr(t,t.stateNode.containerInfo),e===null)throw Error(O(387));l=t.pendingProps;var a=t.memoizedState;o=a.element,zd(e,t),is(t,l,null,n);var i=t.memoizedState;if(l=i.cache,ho(t,Zt,l),l!==a.cache&&Dd(t,[Zt],n,!0),as(),l=i.element,a.isDehydrated)if(a={element:l,isDehydrated:!1,cache:i.cache},t.updateQueue.baseState=a,t.memoizedState=a,t.flags&256){t=bh(e,t,l,n);break e}else if(l!==o){o=tl(Error(O(424)),t),ps(o),t=bh(e,t,l,n);break e}else for(e=t.stateNode.containerInfo,e.nodeType===9?e=e.body:e=e.nodeName==="HTML"?e.ownerDocument.body:e,Mt=ol(e.firstChild),cn=t,We=!0,So=null,nl=!0,n=W1(t,null,l,n),t.child=n;n;)n.flags=n.flags&-3|4096,n=n.sibling;else{if(la(),l===o){t=to(e,t,n);break e}sn(e,t,l,n)}t=t.child}return t;case 26:return Ur(e,t),e===null?(n=Xh(t.type,null,t.pendingProps,null))?t.memoizedState=n:We||(n=t.type,e=t.pendingProps,l=hc(ko.current).createElement(n),l[rn]=t,l[Dn]=e,dn(l,n,e),ln(l),t.stateNode=l):t.memoizedState=Xh(t.type,e.memoizedProps,t.pendingProps,e.memoizedState),null;case 27:return md(t),e===null&&We&&(l=t.stateNode=Eg(t.type,t.pendingProps,ko.current),cn=t,nl=!0,o=Mt,$o(t.type)?(t_=o,Mt=ol(l.firstChild)):Mt=o),sn(e,t,t.pendingProps.children,n),Ur(e,t),e===null&&(t.flags|=4194304),t.child;case 5:return e===null&&We&&((o=l=Mt)&&(l=O2(l,t.type,t.pendingProps,nl),l!==null?(t.stateNode=l,cn=t,Mt=ol(l.firstChild),nl=!1,o=!0):o=!1),o||Lo(t)),md(t),o=t.type,a=t.pendingProps,i=e!==null?e.memoizedProps:null,l=a.children,Fd(o,a)?l=null:i!==null&&Fd(o,i)&&(t.flags|=32),t.memoizedState!==null&&(o=E_(e,t,P5,null,null,n),Ss._currentValue=o),Ur(e,t),sn(e,t,l,n),t.child;case 6:return e===null&&We&&((e=n=Mt)&&(n=$2(n,t.pendingProps,nl),n!==null?(t.stateNode=n,cn=t,Mt=null,e=!0):e=!1),e||Lo(t)),null;case 13:return Bm(e,t,n);case 4:return Wr(t,t.stateNode.containerInfo),l=t.pendingProps,e===null?t.child=aa(t,null,l,n):sn(e,t,l,n),t.child;case 11:return fh(e,t,t.type,t.pendingProps,n);case 7:return sn(e,t,t.pendingProps,n),t.child;case 8:return sn(e,t,t.pendingProps.children,n),t.child;case 12:return sn(e,t,t.pendingProps.children,n),t.child;case 10:return l=t.pendingProps,ho(t,t.type,l.value),sn(e,t,l.children,n),t.child;case 9:return o=t.type._context,l=t.pendingProps.children,oa(t),o=un(o),l=l(o),t.flags|=1,sn(e,t,l,n),t.child;case 14:return hh(e,t,t.type,t.pendingProps,n);case 15:return Lm(e,t,t.type,t.pendingProps,n);case 19:return Om(e,t,n);case 31:return s2(e,t,n);case 22:return Rm(e,t,n,t.pendingProps);case 24:return oa(t),l=un(Zt),e===null?(o=w_(),o===null&&(o=pt,a=v_(),o.pooledCache=a,a.refCount++,a!==null&&(o.pooledCacheLanes|=n),o=a),t.memoizedState={parent:l,cache:o},S_(t),ho(t,Zt,o)):((e.lanes&n)!==0&&(zd(e,t),is(t,null,null,n),as()),o=e.memoizedState,a=t.memoizedState,o.parent!==l?(o={parent:l,cache:l},t.memoizedState=o,t.lanes===0&&(t.memoizedState=t.updateQueue.baseState=o),ho(t,Zt,l)):(l=a.cache,ho(t,Zt,l),l!==o.cache&&Dd(t,[Zt],n,!0))),sn(e,t,t.pendingProps.children,n),t.child;case 29:throw t.pendingProps}throw Error(O(156,t.tag))}function Yl(e){e.flags|=4}function Ju(e,t,n,l,o){if((t=(e.mode&32)!==0)&&(t=!1),t){if(e.flags|=16777216,(o&335544128)===o)if(e.stateNode.complete)e.flags|=8192;else if(sg())e.flags|=8192;else throw ta=ec,k_}else e.flags&=-16777217}function vh(e,t){if(t.type!=="stylesheet"||(t.state.loading&4)!==0)e.flags&=-16777217;else if(e.flags|=16777216,!Ng(t))if(sg())e.flags|=8192;else throw ta=ec,k_}function kr(e,t){t!==null&&(e.flags|=4),e.flags&16384&&(t=e.tag!==22?r1():536870912,e.lanes|=t,si|=t)}function Qi(e,t){if(!We)switch(e.tailMode){case"hidden":t=e.tail;for(var n=null;t!==null;)t.alternate!==null&&(n=t),t=t.sibling;n===null?e.tail=null:n.sibling=null;break;case"collapsed":n=e.tail;for(var l=null;n!==null;)n.alternate!==null&&(l=n),n=n.sibling;l===null?t||e.tail===null?e.tail=null:e.tail.sibling=null:l.sibling=null}}function Ct(e){var t=e.alternate!==null&&e.alternate.child===e.child,n=0,l=0;if(t)for(var o=e.child;o!==null;)n|=o.lanes|o.childLanes,l|=o.subtreeFlags&65011712,l|=o.flags&65011712,o.return=e,o=o.sibling;else for(o=e.child;o!==null;)n|=o.lanes|o.childLanes,l|=o.subtreeFlags,l|=o.flags,o.return=e,o=o.sibling;return e.subtreeFlags|=l,e.childLanes=n,t}function c2(e,t,n){var l=t.pendingProps;switch(x_(t),t.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return Ct(t),null;case 1:return Ct(t),null;case 3:return n=t.stateNode,l=null,e!==null&&(l=e.memoizedState.cache),t.memoizedState.cache!==l&&(t.flags|=2048),Kl(Zt),ti(),n.pendingContext&&(n.context=n.pendingContext,n.pendingContext=null),(e===null||e.child===null)&&(Aa(t)?Yl(t):e===null||e.memoizedState.isDehydrated&&(t.flags&256)===0||(t.flags|=1024,Iu())),Ct(t),null;case 26:var o=t.type,a=t.memoizedState;return e===null?(Yl(t),a!==null?(Ct(t),vh(t,a)):(Ct(t),Ju(t,o,null,l,n))):a?a!==e.memoizedState?(Yl(t),Ct(t),vh(t,a)):(Ct(t),t.flags&=-16777217):(e=e.memoizedProps,e!==l&&Yl(t),Ct(t),Ju(t,o,e,l,n)),null;case 27:if(Gr(t),n=ko.current,o=t.type,e!==null&&t.stateNode!=null)e.memoizedProps!==l&&Yl(t);else{if(!l){if(t.stateNode===null)throw Error(O(166));return Ct(t),null}e=Dl.current,Aa(t)?K0(t,e):(e=Eg(o,l,n),t.stateNode=e,Yl(t))}return Ct(t),null;case 5:if(Gr(t),o=t.type,e!==null&&t.stateNode!=null)e.memoizedProps!==l&&Yl(t);else{if(!l){if(t.stateNode===null)throw Error(O(166));return Ct(t),null}if(a=Dl.current,Aa(t))K0(t,a);else{var i=hc(ko.current);switch(a){case 1:a=i.createElementNS("http://www.w3.org/2000/svg",o);break;case 2:a=i.createElementNS("http://www.w3.org/1998/Math/MathML",o);break;default:switch(o){case"svg":a=i.createElementNS("http://www.w3.org/2000/svg",o);break;case"math":a=i.createElementNS("http://www.w3.org/1998/Math/MathML",o);break;case"script":a=i.createElement("div"),a.innerHTML="<script><\/script>",a=a.removeChild(a.firstChild);break;case"select":a=typeof l.is=="string"?i.createElement("select",{is:l.is}):i.createElement("select"),l.multiple?a.multiple=!0:l.size&&(a.size=l.size);break;default:a=typeof l.is=="string"?i.createElement(o,{is:l.is}):i.createElement(o)}}a[rn]=t,a[Dn]=l;e:for(i=t.child;i!==null;){if(i.tag===5||i.tag===6)a.appendChild(i.stateNode);else if(i.tag!==4&&i.tag!==27&&i.child!==null){i.child.return=i,i=i.child;continue}if(i===t)break e;for(;i.sibling===null;){if(i.return===null||i.return===t)break e;i=i.return}i.sibling.return=i.return,i=i.sibling}t.stateNode=a;e:switch(dn(a,o,l),o){case"button":case"input":case"select":case"textarea":l=!!l.autoFocus;break e;case"img":l=!0;break e;default:l=!1}l&&Yl(t)}}return Ct(t),Ju(t,t.type,e===null?null:e.memoizedProps,t.pendingProps,n),null;case 6:if(e&&t.stateNode!=null)e.memoizedProps!==l&&Yl(t);else{if(typeof l!="string"&&t.stateNode===null)throw Error(O(166));if(e=ko.current,Aa(t)){if(e=t.stateNode,n=t.memoizedProps,l=null,o=cn,o!==null)switch(o.tag){case 27:case 5:l=o.memoizedProps}e[rn]=t,e=!!(e.nodeValue===n||l!==null&&l.suppressHydrationWarning===!0||kg(e.nodeValue,n)),e||Lo(t,!0)}else e=hc(e).createTextNode(l),e[rn]=t,t.stateNode=e}return Ct(t),null;case 31:if(n=t.memoizedState,e===null||e.memoizedState!==null){if(l=Aa(t),n!==null){if(e===null){if(!l)throw Error(O(318));if(e=t.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(O(557));e[rn]=t}else la(),(t.flags&128)===0&&(t.memoizedState=null),t.flags|=4;Ct(t),e=!1}else n=Iu(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=n),e=!0;if(!e)return t.flags&256?(Ln(t),t):(Ln(t),null);if((t.flags&128)!==0)throw Error(O(558))}return Ct(t),null;case 13:if(l=t.memoizedState,e===null||e.memoizedState!==null&&e.memoizedState.dehydrated!==null){if(o=Aa(t),l!==null&&l.dehydrated!==null){if(e===null){if(!o)throw Error(O(318));if(o=t.memoizedState,o=o!==null?o.dehydrated:null,!o)throw Error(O(317));o[rn]=t}else la(),(t.flags&128)===0&&(t.memoizedState=null),t.flags|=4;Ct(t),o=!1}else o=Iu(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=o),o=!0;if(!o)return t.flags&256?(Ln(t),t):(Ln(t),null)}return Ln(t),(t.flags&128)!==0?(t.lanes=n,t):(n=l!==null,e=e!==null&&e.memoizedState!==null,n&&(l=t.child,o=null,l.alternate!==null&&l.alternate.memoizedState!==null&&l.alternate.memoizedState.cachePool!==null&&(o=l.alternate.memoizedState.cachePool.pool),a=null,l.memoizedState!==null&&l.memoizedState.cachePool!==null&&(a=l.memoizedState.cachePool.pool),a!==o&&(l.flags|=2048)),n!==e&&n&&(t.child.flags|=8192),kr(t,t.updateQueue),Ct(t),null);case 4:return ti(),e===null&&G_(t.stateNode.containerInfo),Ct(t),null;case 10:return Kl(t.type),Ct(t),null;case 19:if(on(Xt),l=t.memoizedState,l===null)return Ct(t),null;if(o=(t.flags&128)!==0,a=l.rendering,a===null)if(o)Qi(l,!1);else{if(Ht!==0||e!==null&&(e.flags&128)!==0)for(e=t.child;e!==null;){if(a=nc(e),a!==null){for(t.flags|=128,Qi(l,!1),e=a.updateQueue,t.updateQueue=e,kr(t,e),t.subtreeFlags=0,e=n,n=t.child;n!==null;)H1(n,e),n=n.sibling;return kt(Xt,Xt.current&1|2),We&&ql(t,l.treeForkCount),t.child}e=e.sibling}l.tail!==null&&On()>rc&&(t.flags|=128,o=!0,Qi(l,!1),t.lanes=4194304)}else{if(!o)if(e=nc(a),e!==null){if(t.flags|=128,o=!0,e=e.updateQueue,t.updateQueue=e,kr(t,e),Qi(l,!0),l.tail===null&&l.tailMode==="hidden"&&!a.alternate&&!We)return Ct(t),null}else 2*On()-l.renderingStartTime>rc&&n!==536870912&&(t.flags|=128,o=!0,Qi(l,!1),t.lanes=4194304);l.isBackwards?(a.sibling=t.child,t.child=a):(e=l.last,e!==null?e.sibling=a:t.child=a,l.last=a)}return l.tail!==null?(e=l.tail,l.rendering=e,l.tail=e.sibling,l.renderingStartTime=On(),e.sibling=null,n=Xt.current,kt(Xt,o?n&1|2:n&1),We&&ql(t,l.treeForkCount),e):(Ct(t),null);case 22:case 23:return Ln(t),C_(),l=t.memoizedState!==null,e!==null?e.memoizedState!==null!==l&&(t.flags|=8192):l&&(t.flags|=8192),l?(n&536870912)!==0&&(t.flags&128)===0&&(Ct(t),t.subtreeFlags&6&&(t.flags|=8192)):Ct(t),n=t.updateQueue,n!==null&&kr(t,n.retryQueue),n=null,e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(n=e.memoizedState.cachePool.pool),l=null,t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(l=t.memoizedState.cachePool.pool),l!==n&&(t.flags|=2048),e!==null&&on(ea),null;case 24:return n=null,e!==null&&(n=e.memoizedState.cache),t.memoizedState.cache!==n&&(t.flags|=2048),Kl(Zt),Ct(t),null;case 25:return null;case 30:return null}throw Error(O(156,t.tag))}function u2(e,t){switch(x_(t),t.tag){case 1:return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 3:return Kl(Zt),ti(),e=t.flags,(e&65536)!==0&&(e&128)===0?(t.flags=e&-65537|128,t):null;case 26:case 27:case 5:return Gr(t),null;case 31:if(t.memoizedState!==null){if(Ln(t),t.alternate===null)throw Error(O(340));la()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 13:if(Ln(t),e=t.memoizedState,e!==null&&e.dehydrated!==null){if(t.alternate===null)throw Error(O(340));la()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 19:return on(Xt),null;case 4:return ti(),null;case 10:return Kl(t.type),null;case 22:case 23:return Ln(t),C_(),e!==null&&on(ea),e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 24:return Kl(Zt),null;case 25:return null;default:return null}}function Hm(e,t){switch(x_(t),t.tag){case 3:Kl(Zt),ti();break;case 26:case 27:case 5:Gr(t);break;case 4:ti();break;case 31:t.memoizedState!==null&&Ln(t);break;case 13:Ln(t);break;case 19:on(Xt);break;case 10:Kl(t.type);break;case 22:case 23:Ln(t),C_(),e!==null&&on(ea);break;case 24:Kl(Zt)}}function Bs(e,t){try{var n=t.updateQueue,l=n!==null?n.lastEffect:null;if(l!==null){var o=l.next;n=o;do{if((n.tag&e)===e){l=void 0;var a=n.create,i=n.inst;l=a(),i.destroy=l}n=n.next}while(n!==o)}}catch(s){dt(t,t.return,s)}}function Ro(e,t,n){try{var l=t.updateQueue,o=l!==null?l.lastEffect:null;if(o!==null){var a=o.next;l=a;do{if((l.tag&e)===e){var i=l.inst,s=i.destroy;if(s!==void 0){i.destroy=void 0,o=t;var r=n,p=s;try{p()}catch(f){dt(o,r,f)}}}l=l.next}while(l!==a)}}catch(f){dt(t,t.return,f)}}function Um(e){var t=e.updateQueue;if(t!==null){var n=e.stateNode;try{V1(t,n)}catch(l){dt(e,e.return,l)}}}function Ym(e,t,n){n.props=sa(e.type,e.memoizedProps),n.state=e.memoizedState;try{n.componentWillUnmount()}catch(l){dt(e,t,l)}}function rs(e,t){try{var n=e.ref;if(n!==null){switch(e.tag){case 26:case 27:case 5:var l=e.stateNode;break;case 30:l=e.stateNode;break;default:l=e.stateNode}typeof n=="function"?e.refCleanup=n(l):n.current=l}}catch(o){dt(e,t,o)}}function Tl(e,t){var n=e.ref,l=e.refCleanup;if(n!==null)if(typeof l=="function")try{l()}catch(o){dt(e,t,o)}finally{e.refCleanup=null,e=e.alternate,e!=null&&(e.refCleanup=null)}else if(typeof n=="function")try{n(null)}catch(o){dt(e,t,o)}else n.current=null}function jm(e){var t=e.type,n=e.memoizedProps,l=e.stateNode;try{e:switch(t){case"button":case"input":case"select":case"textarea":n.autoFocus&&l.focus();break e;case"img":n.src?l.src=n.src:n.srcSet&&(l.srcset=n.srcSet)}}catch(o){dt(e,e.return,o)}}function Pu(e,t,n){try{var l=e.stateNode;N2(l,e.type,n,t),l[Dn]=t}catch(o){dt(e,e.return,o)}}function Xm(e){return e.tag===5||e.tag===3||e.tag===26||e.tag===27&&$o(e.type)||e.tag===4}function ed(e){e:for(;;){for(;e.sibling===null;){if(e.return===null||Xm(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;e.tag!==5&&e.tag!==6&&e.tag!==18;){if(e.tag===27&&$o(e.type)||e.flags&2||e.child===null||e.tag===4)continue e;e.child.return=e,e=e.child}if(!(e.flags&2))return e.stateNode}}function Xd(e,t,n){var l=e.tag;if(l===5||l===6)e=e.stateNode,t?(n.nodeType===9?n.body:n.nodeName==="HTML"?n.ownerDocument.body:n).insertBefore(e,t):(t=n.nodeType===9?n.body:n.nodeName==="HTML"?n.ownerDocument.body:n,t.appendChild(e),n=n._reactRootContainer,n!=null||t.onclick!==null||(t.onclick=Gl));else if(l!==4&&(l===27&&$o(e.type)&&(n=e.stateNode,t=null),e=e.child,e!==null))for(Xd(e,t,n),e=e.sibling;e!==null;)Xd(e,t,n),e=e.sibling}function sc(e,t,n){var l=e.tag;if(l===5||l===6)e=e.stateNode,t?n.insertBefore(e,t):n.appendChild(e);else if(l!==4&&(l===27&&$o(e.type)&&(n=e.stateNode),e=e.child,e!==null))for(sc(e,t,n),e=e.sibling;e!==null;)sc(e,t,n),e=e.sibling}function Im(e){var t=e.stateNode,n=e.memoizedProps;try{for(var l=e.type,o=t.attributes;o.length;)t.removeAttributeNode(o[0]);dn(t,l,n),t[rn]=e,t[Dn]=n}catch(a){dt(e,e.return,a)}}var Ql=!1,Vt=!1,td=!1,wh=typeof WeakSet=="function"?WeakSet:Set,nn=null;function d2(e,t){if(e=e.containerInfo,Zd=pc,e=N1(e),m_(e)){if("selectionStart"in e)var n={start:e.selectionStart,end:e.selectionEnd};else e:{n=(n=e.ownerDocument)&&n.defaultView||window;var l=n.getSelection&&n.getSelection();if(l&&l.rangeCount!==0){n=l.anchorNode;var o=l.anchorOffset,a=l.focusNode;l=l.focusOffset;try{n.nodeType,a.nodeType}catch{n=null;break e}var i=0,s=-1,r=-1,p=0,f=0,b=e,_=null;t:for(;;){for(var w;b!==n||o!==0&&b.nodeType!==3||(s=i+o),b!==a||l!==0&&b.nodeType!==3||(r=i+l),b.nodeType===3&&(i+=b.nodeValue.length),(w=b.firstChild)!==null;)_=b,b=w;for(;;){if(b===e)break t;if(_===n&&++p===o&&(s=i),_===a&&++f===l&&(r=i),(w=b.nextSibling)!==null)break;b=_,_=b.parentNode}b=w}n=s===-1||r===-1?null:{start:s,end:r}}else n=null}n=n||{start:0,end:0}}else n=null;for(Kd={focusedElem:e,selectionRange:n},pc=!1,nn=t;nn!==null;)if(t=nn,e=t.child,(t.subtreeFlags&1028)!==0&&e!==null)e.return=t,nn=e;else for(;nn!==null;){switch(t=nn,a=t.alternate,e=t.flags,t.tag){case 0:if((e&4)!==0&&(e=t.updateQueue,e=e!==null?e.events:null,e!==null))for(n=0;n<e.length;n++)o=e[n],o.ref.impl=o.nextImpl;break;case 11:case 15:break;case 1:if((e&1024)!==0&&a!==null){e=void 0,n=t,o=a.memoizedProps,a=a.memoizedState,l=n.stateNode;try{var C=sa(n.type,o);e=l.getSnapshotBeforeUpdate(C,a),l.__reactInternalSnapshotBeforeUpdate=e}catch(z){dt(n,n.return,z)}}break;case 3:if((e&1024)!==0){if(e=t.stateNode.containerInfo,n=e.nodeType,n===9)Jd(e);else if(n===1)switch(e.nodeName){case"HEAD":case"HTML":case"BODY":Jd(e);break;default:e.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((e&1024)!==0)throw Error(O(163))}if(e=t.sibling,e!==null){e.return=t.return,nn=e;break}nn=t.return}}function qm(e,t,n){var l=n.flags;switch(n.tag){case 0:case 11:case 15:Xl(e,n),l&4&&Bs(5,n);break;case 1:if(Xl(e,n),l&4)if(e=n.stateNode,t===null)try{e.componentDidMount()}catch(i){dt(n,n.return,i)}else{var o=sa(n.type,t.memoizedProps);t=t.memoizedState;try{e.componentDidUpdate(o,t,e.__reactInternalSnapshotBeforeUpdate)}catch(i){dt(n,n.return,i)}}l&64&&Um(n),l&512&&rs(n,n.return);break;case 3:if(Xl(e,n),l&64&&(e=n.updateQueue,e!==null)){if(t=null,n.child!==null)switch(n.child.tag){case 27:case 5:t=n.child.stateNode;break;case 1:t=n.child.stateNode}try{V1(e,t)}catch(i){dt(n,n.return,i)}}break;case 27:t===null&&l&4&&Im(n);case 26:case 5:Xl(e,n),t===null&&l&4&&jm(n),l&512&&rs(n,n.return);break;case 12:Xl(e,n);break;case 31:Xl(e,n),l&4&&Gm(e,n);break;case 13:Xl(e,n),l&4&&Vm(e,n),l&64&&(e=n.memoizedState,e!==null&&(e=e.dehydrated,e!==null&&(n=x2.bind(null,n),H2(e,n))));break;case 22:if(l=n.memoizedState!==null||Ql,!l){t=t!==null&&t.memoizedState!==null||Vt,o=Ql;var a=Vt;Ql=l,(Vt=t)&&!a?Il(e,n,(n.subtreeFlags&8772)!==0):Xl(e,n),Ql=o,Vt=a}break;case 30:break;default:Xl(e,n)}}function Qm(e){var t=e.alternate;t!==null&&(e.alternate=null,Qm(t)),e.child=null,e.deletions=null,e.sibling=null,e.tag===5&&(t=e.stateNode,t!==null&&c_(t)),e.stateNode=null,e.return=null,e.dependencies=null,e.memoizedProps=null,e.memoizedState=null,e.pendingProps=null,e.stateNode=null,e.updateQueue=null}var Dt=null,Mn=!1;function jl(e,t,n){for(n=n.child;n!==null;)Wm(e,t,n),n=n.sibling}function Wm(e,t,n){if($n&&typeof $n.onCommitFiberUnmount=="function")try{$n.onCommitFiberUnmount(Ts,n)}catch{}switch(n.tag){case 26:Vt||Tl(n,t),jl(e,t,n),n.memoizedState?n.memoizedState.count--:n.stateNode&&(n=n.stateNode,n.parentNode.removeChild(n));break;case 27:Vt||Tl(n,t);var l=Dt,o=Mn;$o(n.type)&&(Dt=n.stateNode,Mn=!1),jl(e,t,n),_s(n.stateNode),Dt=l,Mn=o;break;case 5:Vt||Tl(n,t);case 6:if(l=Dt,o=Mn,Dt=null,jl(e,t,n),Dt=l,Mn=o,Dt!==null)if(Mn)try{(Dt.nodeType===9?Dt.body:Dt.nodeName==="HTML"?Dt.ownerDocument.body:Dt).removeChild(n.stateNode)}catch(a){dt(n,t,a)}else try{Dt.removeChild(n.stateNode)}catch(a){dt(n,t,a)}break;case 18:Dt!==null&&(Mn?(e=Dt,$h(e.nodeType===9?e.body:e.nodeName==="HTML"?e.ownerDocument.body:e,n.stateNode),di(e)):$h(Dt,n.stateNode));break;case 4:l=Dt,o=Mn,Dt=n.stateNode.containerInfo,Mn=!0,jl(e,t,n),Dt=l,Mn=o;break;case 0:case 11:case 14:case 15:Ro(2,n,t),Vt||Ro(4,n,t),jl(e,t,n);break;case 1:Vt||(Tl(n,t),l=n.stateNode,typeof l.componentWillUnmount=="function"&&Ym(n,t,l)),jl(e,t,n);break;case 21:jl(e,t,n);break;case 22:Vt=(l=Vt)||n.memoizedState!==null,jl(e,t,n),Vt=l;break;default:jl(e,t,n)}}function Gm(e,t){if(t.memoizedState===null&&(e=t.alternate,e!==null&&(e=e.memoizedState,e!==null))){e=e.dehydrated;try{di(e)}catch(n){dt(t,t.return,n)}}}function Vm(e,t){if(t.memoizedState===null&&(e=t.alternate,e!==null&&(e=e.memoizedState,e!==null&&(e=e.dehydrated,e!==null))))try{di(e)}catch(n){dt(t,t.return,n)}}function _2(e){switch(e.tag){case 31:case 13:case 19:var t=e.stateNode;return t===null&&(t=e.stateNode=new wh),t;case 22:return e=e.stateNode,t=e._retryCache,t===null&&(t=e._retryCache=new wh),t;default:throw Error(O(435,e.tag))}}function Sr(e,t){var n=_2(e);t.forEach(function(l){if(!n.has(l)){n.add(l);var o=v2.bind(null,e,l);l.then(o,o)}})}function Sn(e,t){var n=t.deletions;if(n!==null)for(var l=0;l<n.length;l++){var o=n[l],a=e,i=t,s=i;e:for(;s!==null;){switch(s.tag){case 27:if($o(s.type)){Dt=s.stateNode,Mn=!1;break e}break;case 5:Dt=s.stateNode,Mn=!1;break e;case 3:case 4:Dt=s.stateNode.containerInfo,Mn=!0;break e}s=s.return}if(Dt===null)throw Error(O(160));Wm(a,i,o),Dt=null,Mn=!1,a=o.alternate,a!==null&&(a.return=null),o.return=null}if(t.subtreeFlags&13886)for(t=t.child;t!==null;)Zm(t,e),t=t.sibling}var hl=null;function Zm(e,t){var n=e.alternate,l=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:Sn(t,e),Cn(e),l&4&&(Ro(3,e,e.return),Bs(3,e),Ro(5,e,e.return));break;case 1:Sn(t,e),Cn(e),l&512&&(Vt||n===null||Tl(n,n.return)),l&64&&Ql&&(e=e.updateQueue,e!==null&&(l=e.callbacks,l!==null&&(n=e.shared.hiddenCallbacks,e.shared.hiddenCallbacks=n===null?l:n.concat(l))));break;case 26:var o=hl;if(Sn(t,e),Cn(e),l&512&&(Vt||n===null||Tl(n,n.return)),l&4){var a=n!==null?n.memoizedState:null;if(l=e.memoizedState,n===null)if(l===null)if(e.stateNode===null){e:{l=e.type,n=e.memoizedProps,o=o.ownerDocument||o;t:switch(l){case"title":a=o.getElementsByTagName("title")[0],(!a||a[zs]||a[rn]||a.namespaceURI==="http://www.w3.org/2000/svg"||a.hasAttribute("itemprop"))&&(a=o.createElement(l),o.head.insertBefore(a,o.querySelector("head > title"))),dn(a,l,n),a[rn]=e,ln(a),l=a;break e;case"link":var i=qh("link","href",o).get(l+(n.href||""));if(i){for(var s=0;s<i.length;s++)if(a=i[s],a.getAttribute("href")===(n.href==null||n.href===""?null:n.href)&&a.getAttribute("rel")===(n.rel==null?null:n.rel)&&a.getAttribute("title")===(n.title==null?null:n.title)&&a.getAttribute("crossorigin")===(n.crossOrigin==null?null:n.crossOrigin)){i.splice(s,1);break t}}a=o.createElement(l),dn(a,l,n),o.head.appendChild(a);break;case"meta":if(i=qh("meta","content",o).get(l+(n.content||""))){for(s=0;s<i.length;s++)if(a=i[s],a.getAttribute("content")===(n.content==null?null:""+n.content)&&a.getAttribute("name")===(n.name==null?null:n.name)&&a.getAttribute("property")===(n.property==null?null:n.property)&&a.getAttribute("http-equiv")===(n.httpEquiv==null?null:n.httpEquiv)&&a.getAttribute("charset")===(n.charSet==null?null:n.charSet)){i.splice(s,1);break t}}a=o.createElement(l),dn(a,l,n),o.head.appendChild(a);break;default:throw Error(O(468,l))}a[rn]=e,ln(a),l=a}e.stateNode=l}else Qh(o,e.type,e.stateNode);else e.stateNode=Ih(o,l,e.memoizedProps);else a!==l?(a===null?n.stateNode!==null&&(n=n.stateNode,n.parentNode.removeChild(n)):a.count--,l===null?Qh(o,e.type,e.stateNode):Ih(o,l,e.memoizedProps)):l===null&&e.stateNode!==null&&Pu(e,e.memoizedProps,n.memoizedProps)}break;case 27:Sn(t,e),Cn(e),l&512&&(Vt||n===null||Tl(n,n.return)),n!==null&&l&4&&Pu(e,e.memoizedProps,n.memoizedProps);break;case 5:if(Sn(t,e),Cn(e),l&512&&(Vt||n===null||Tl(n,n.return)),e.flags&32){o=e.stateNode;try{li(o,"")}catch(C){dt(e,e.return,C)}}l&4&&e.stateNode!=null&&(o=e.memoizedProps,Pu(e,o,n!==null?n.memoizedProps:o)),l&1024&&(td=!0);break;case 6:if(Sn(t,e),Cn(e),l&4){if(e.stateNode===null)throw Error(O(162));l=e.memoizedProps,n=e.stateNode;try{n.nodeValue=l}catch(C){dt(e,e.return,C)}}break;case 3:if(Xr=null,o=hl,hl=mc(t.containerInfo),Sn(t,e),hl=o,Cn(e),l&4&&n!==null&&n.memoizedState.isDehydrated)try{di(t.containerInfo)}catch(C){dt(e,e.return,C)}td&&(td=!1,Km(e));break;case 4:l=hl,hl=mc(e.stateNode.containerInfo),Sn(t,e),Cn(e),hl=l;break;case 12:Sn(t,e),Cn(e);break;case 31:Sn(t,e),Cn(e),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Sr(e,l)));break;case 13:Sn(t,e),Cn(e),e.child.flags&8192&&e.memoizedState!==null!=(n!==null&&n.memoizedState!==null)&&(zc=On()),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Sr(e,l)));break;case 22:o=e.memoizedState!==null;var r=n!==null&&n.memoizedState!==null,p=Ql,f=Vt;if(Ql=p||o,Vt=f||r,Sn(t,e),Vt=f,Ql=p,Cn(e),l&8192)e:for(t=e.stateNode,t._visibility=o?t._visibility&-2:t._visibility|1,o&&(n===null||r||Ql||Vt||Fo(e)),n=null,t=e;;){if(t.tag===5||t.tag===26){if(n===null){r=n=t;try{if(a=r.stateNode,o)i=a.style,typeof i.setProperty=="function"?i.setProperty("display","none","important"):i.display="none";else{s=r.stateNode;var b=r.memoizedProps.style,_=b!=null&&b.hasOwnProperty("display")?b.display:null;s.style.display=_==null||typeof _=="boolean"?"":(""+_).trim()}}catch(C){dt(r,r.return,C)}}}else if(t.tag===6){if(n===null){r=t;try{r.stateNode.nodeValue=o?"":r.memoizedProps}catch(C){dt(r,r.return,C)}}}else if(t.tag===18){if(n===null){r=t;try{var w=r.stateNode;o?Hh(w,!0):Hh(r.stateNode,!1)}catch(C){dt(r,r.return,C)}}}else if((t.tag!==22&&t.tag!==23||t.memoizedState===null||t===e)&&t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break e;for(;t.sibling===null;){if(t.return===null||t.return===e)break e;n===t&&(n=null),t=t.return}n===t&&(n=null),t.sibling.return=t.return,t=t.sibling}l&4&&(l=e.updateQueue,l!==null&&(n=l.retryQueue,n!==null&&(l.retryQueue=null,Sr(e,n))));break;case 19:Sn(t,e),Cn(e),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Sr(e,l)));break;case 30:break;case 21:break;default:Sn(t,e),Cn(e)}}function Cn(e){var t=e.flags;if(t&2){try{for(var n,l=e.return;l!==null;){if(Xm(l)){n=l;break}l=l.return}if(n==null)throw Error(O(160));switch(n.tag){case 27:var o=n.stateNode,a=ed(e);sc(e,a,o);break;case 5:var i=n.stateNode;n.flags&32&&(li(i,""),n.flags&=-33);var s=ed(e);sc(e,s,i);break;case 3:case 4:var r=n.stateNode.containerInfo,p=ed(e);Xd(e,p,r);break;default:throw Error(O(161))}}catch(f){dt(e,e.return,f)}e.flags&=-3}t&4096&&(e.flags&=-4097)}function Km(e){if(e.subtreeFlags&1024)for(e=e.child;e!==null;){var t=e;Km(t),t.tag===5&&t.flags&1024&&t.stateNode.reset(),e=e.sibling}}function Xl(e,t){if(t.subtreeFlags&8772)for(t=t.child;t!==null;)qm(e,t.alternate,t),t=t.sibling}function Fo(e){for(e=e.child;e!==null;){var t=e;switch(t.tag){case 0:case 11:case 14:case 15:Ro(4,t,t.return),Fo(t);break;case 1:Tl(t,t.return);var n=t.stateNode;typeof n.componentWillUnmount=="function"&&Ym(t,t.return,n),Fo(t);break;case 27:_s(t.stateNode);case 26:case 5:Tl(t,t.return),Fo(t);break;case 22:t.memoizedState===null&&Fo(t);break;case 30:Fo(t);break;default:Fo(t)}e=e.sibling}}function Il(e,t,n){for(n=n&&(t.subtreeFlags&8772)!==0,t=t.child;t!==null;){var l=t.alternate,o=e,a=t,i=a.flags;switch(a.tag){case 0:case 11:case 15:Il(o,a,n),Bs(4,a);break;case 1:if(Il(o,a,n),l=a,o=l.stateNode,typeof o.componentDidMount=="function")try{o.componentDidMount()}catch(p){dt(l,l.return,p)}if(l=a,o=l.updateQueue,o!==null){var s=l.stateNode;try{var r=o.shared.hiddenCallbacks;if(r!==null)for(o.shared.hiddenCallbacks=null,o=0;o<r.length;o++)G1(r[o],s)}catch(p){dt(l,l.return,p)}}n&&i&64&&Um(a),rs(a,a.return);break;case 27:Im(a);case 26:case 5:Il(o,a,n),n&&l===null&&i&4&&jm(a),rs(a,a.return);break;case 12:Il(o,a,n);break;case 31:Il(o,a,n),n&&i&4&&Gm(o,a);break;case 13:Il(o,a,n),n&&i&4&&Vm(o,a);break;case 22:a.memoizedState===null&&Il(o,a,n),rs(a,a.return);break;case 30:break;default:Il(o,a,n)}t=t.sibling}}function j_(e,t){var n=null;e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(n=e.memoizedState.cachePool.pool),e=null,t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(e=t.memoizedState.cachePool.pool),e!==n&&(e!=null&&e.refCount++,n!=null&&Ls(n))}function X_(e,t){e=null,t.alternate!==null&&(e=t.alternate.memoizedState.cache),t=t.memoizedState.cache,t!==e&&(t.refCount++,e!=null&&Ls(e))}function fl(e,t,n,l){if(t.subtreeFlags&10256)for(t=t.child;t!==null;)Fm(e,t,n,l),t=t.sibling}function Fm(e,t,n,l){var o=t.flags;switch(t.tag){case 0:case 11:case 15:fl(e,t,n,l),o&2048&&Bs(9,t);break;case 1:fl(e,t,n,l);break;case 3:fl(e,t,n,l),o&2048&&(e=null,t.alternate!==null&&(e=t.alternate.memoizedState.cache),t=t.memoizedState.cache,t!==e&&(t.refCount++,e!=null&&Ls(e)));break;case 12:if(o&2048){fl(e,t,n,l),e=t.stateNode;try{var a=t.memoizedProps,i=a.id,s=a.onPostCommit;typeof s=="function"&&s(i,t.alternate===null?"mount":"update",e.passiveEffectDuration,-0)}catch(r){dt(t,t.return,r)}}else fl(e,t,n,l);break;case 31:fl(e,t,n,l);break;case 13:fl(e,t,n,l);break;case 23:break;case 22:a=t.stateNode,i=t.alternate,t.memoizedState!==null?a._visibility&2?fl(e,t,n,l):cs(e,t):a._visibility&2?fl(e,t,n,l):(a._visibility|=2,Ra(e,t,n,l,(t.subtreeFlags&10256)!==0||!1)),o&2048&&j_(i,t);break;case 24:fl(e,t,n,l),o&2048&&X_(t.alternate,t);break;default:fl(e,t,n,l)}}function Ra(e,t,n,l,o){for(o=o&&((t.subtreeFlags&10256)!==0||!1),t=t.child;t!==null;){var a=e,i=t,s=n,r=l,p=i.flags;switch(i.tag){case 0:case 11:case 15:Ra(a,i,s,r,o),Bs(8,i);break;case 23:break;case 22:var f=i.stateNode;i.memoizedState!==null?f._visibility&2?Ra(a,i,s,r,o):cs(a,i):(f._visibility|=2,Ra(a,i,s,r,o)),o&&p&2048&&j_(i.alternate,i);break;case 24:Ra(a,i,s,r,o),o&&p&2048&&X_(i.alternate,i);break;default:Ra(a,i,s,r,o)}t=t.sibling}}function cs(e,t){if(t.subtreeFlags&10256)for(t=t.child;t!==null;){var n=e,l=t,o=l.flags;switch(l.tag){case 22:cs(n,l),o&2048&&j_(l.alternate,l);break;case 24:cs(n,l),o&2048&&X_(l.alternate,l);break;default:cs(n,l)}t=t.sibling}}var Pi=8192;function La(e,t,n){if(e.subtreeFlags&Pi)for(e=e.child;e!==null;)Jm(e,t,n),e=e.sibling}function Jm(e,t,n){switch(e.tag){case 26:La(e,t,n),e.flags&Pi&&e.memoizedState!==null&&K2(n,hl,e.memoizedState,e.memoizedProps);break;case 5:La(e,t,n);break;case 3:case 4:var l=hl;hl=mc(e.stateNode.containerInfo),La(e,t,n),hl=l;break;case 22:e.memoizedState===null&&(l=e.alternate,l!==null&&l.memoizedState!==null?(l=Pi,Pi=16777216,La(e,t,n),Pi=l):La(e,t,n));break;default:La(e,t,n)}}function Pm(e){var t=e.alternate;if(t!==null&&(e=t.child,e!==null)){t.child=null;do t=e.sibling,e.sibling=null,e=t;while(e!==null)}}function Wi(e){var t=e.deletions;if((e.flags&16)!==0){if(t!==null)for(var n=0;n<t.length;n++){var l=t[n];nn=l,tg(l,e)}Pm(e)}if(e.subtreeFlags&10256)for(e=e.child;e!==null;)eg(e),e=e.sibling}function eg(e){switch(e.tag){case 0:case 11:case 15:Wi(e),e.flags&2048&&Ro(9,e,e.return);break;case 3:Wi(e);break;case 12:Wi(e);break;case 22:var t=e.stateNode;e.memoizedState!==null&&t._visibility&2&&(e.return===null||e.return.tag!==13)?(t._visibility&=-3,Yr(e)):Wi(e);break;default:Wi(e)}}function Yr(e){var t=e.deletions;if((e.flags&16)!==0){if(t!==null)for(var n=0;n<t.length;n++){var l=t[n];nn=l,tg(l,e)}Pm(e)}for(e=e.child;e!==null;){switch(t=e,t.tag){case 0:case 11:case 15:Ro(8,t,t.return),Yr(t);break;case 22:n=t.stateNode,n._visibility&2&&(n._visibility&=-3,Yr(t));break;default:Yr(t)}e=e.sibling}}function tg(e,t){for(;nn!==null;){var n=nn;switch(n.tag){case 0:case 11:case 15:Ro(8,n,t);break;case 23:case 22:if(n.memoizedState!==null&&n.memoizedState.cachePool!==null){var l=n.memoizedState.cachePool.pool;l!=null&&l.refCount++}break;case 24:Ls(n.memoizedState.cache)}if(l=n.child,l!==null)l.return=n,nn=l;else e:for(n=e;nn!==null;){l=nn;var o=l.sibling,a=l.return;if(Qm(l),l===n){nn=null;break e}if(o!==null){o.return=a,nn=o;break e}nn=a}}}var f2={getCacheForType:function(e){var t=un(Zt),n=t.data.get(e);return n===void 0&&(n=e(),t.data.set(e,n)),n},cacheSignal:function(){return un(Zt).controller.signal}},h2=typeof WeakMap=="function"?WeakMap:Map,lt=0,pt=null,Xe=null,Qe=0,ut=0,An=null,xo=!1,gi=!1,I_=!1,no=0,Ht=0,Bo=0,na=0,q_=0,Bn=0,si=0,us=null,En=null,Id=!1,zc=0,ng=0,rc=1/0,cc=null,Eo=null,Pt=0,To=null,ri=null,Fl=0,qd=0,Qd=null,lg=null,ds=0,Wd=null;function Un(){return(lt&2)!==0&&Qe!==0?Qe&-Qe:we.T!==null?W_():_1()}function og(){if(Bn===0)if((Qe&536870912)===0||We){var e=hr;hr<<=1,(hr&3932160)===0&&(hr=262144),Bn=e}else Bn=536870912;return e=jn.current,e!==null&&(e.flags|=32),Bn}function Tn(e,t,n){(e===pt&&(ut===2||ut===9)||e.cancelPendingCommit!==null)&&(ci(e,0),vo(e,Qe,Bn,!1)),Ns(e,n),((lt&2)===0||e!==pt)&&(e===pt&&((lt&2)===0&&(na|=n),Ht===4&&vo(e,Qe,Bn,!1)),zl(e))}function ag(e,t,n){if((lt&6)!==0)throw Error(O(327));var l=!n&&(t&127)===0&&(t&e.expiredLanes)===0||Ds(e,t),o=l?y2(e,t):nd(e,t,!0),a=l;do{if(o===0){gi&&!l&&vo(e,t,0,!1);break}else{if(n=e.current.alternate,a&&!m2(n)){o=nd(e,t,!1),a=!1;continue}if(o===2){if(a=t,e.errorRecoveryDisabledLanes&a)var i=0;else i=e.pendingLanes&-536870913,i=i!==0?i:i&536870912?536870912:0;if(i!==0){t=i;e:{var s=e;o=us;var r=s.current.memoizedState.isDehydrated;if(r&&(ci(s,i).flags|=256),i=nd(s,i,!1),i!==2){if(I_&&!r){s.errorRecoveryDisabledLanes|=a,na|=a,o=4;break e}a=En,En=o,a!==null&&(En===null?En=a:En.push.apply(En,a))}o=i}if(a=!1,o!==2)continue}}if(o===1){ci(e,0),vo(e,t,0,!0);break}e:{switch(l=e,a=o,a){case 0:case 1:throw Error(O(345));case 4:if((t&4194048)!==t)break;case 6:vo(l,t,Bn,!xo);break e;case 2:En=null;break;case 3:case 5:break;default:throw Error(O(329))}if((t&62914560)===t&&(o=zc+300-On(),10<o)){if(vo(l,t,Bn,!xo),xc(l,0,!0)!==0)break e;Fl=t,l.timeoutHandle=Cg(kh.bind(null,l,n,En,cc,Id,t,Bn,na,si,xo,a,"Throttled",-0,0),o);break e}kh(l,n,En,cc,Id,t,Bn,na,si,xo,a,null,-0,0)}}break}while(!0);zl(e)}function kh(e,t,n,l,o,a,i,s,r,p,f,b,_,w){if(e.timeoutHandle=-1,b=t.subtreeFlags,b&8192||(b&16785408)===16785408){b={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Gl},Jm(t,a,b);var C=(a&62914560)===a?zc-On():(a&4194048)===a?ng-On():0;if(C=F2(b,C),C!==null){Fl=a,e.cancelPendingCommit=C(Ch.bind(null,e,t,a,n,l,o,i,s,r,f,b,null,_,w)),vo(e,a,i,!p);return}}Ch(e,t,a,n,l,o,i,s,r)}function m2(e){for(var t=e;;){var n=t.tag;if((n===0||n===11||n===15)&&t.flags&16384&&(n=t.updateQueue,n!==null&&(n=n.stores,n!==null)))for(var l=0;l<n.length;l++){var o=n[l],a=o.getSnapshot;o=o.value;try{if(!Yn(a(),o))return!1}catch{return!1}}if(n=t.child,t.subtreeFlags&16384&&n!==null)n.return=t,t=n;else{if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return!0;t=t.return}t.sibling.return=t.return,t=t.sibling}}return!0}function vo(e,t,n,l){t&=~q_,t&=~na,e.suspendedLanes|=t,e.pingedLanes&=~t,l&&(e.warmLanes|=t),l=e.expirationTimes;for(var o=t;0<o;){var a=31-Hn(o),i=1<<a;l[a]=-1,o&=~i}n!==0&&c1(e,n,t)}function Ac(){return(lt&6)===0?(Os(0,!1),!1):!0}function Q_(){if(Xe!==null){if(ut===0)var e=Xe.return;else e=Xe,Vl=_a=null,N_(e),Ja=null,bs=0,e=Xe;for(;e!==null;)Hm(e.alternate,e),e=e.return;Xe=null}}function ci(e,t){var n=e.timeoutHandle;n!==-1&&(e.timeoutHandle=-1,L2(n)),n=e.cancelPendingCommit,n!==null&&(e.cancelPendingCommit=null,n()),Fl=0,Q_(),pt=e,Xe=n=Zl(e.current,null),Qe=t,ut=0,An=null,xo=!1,gi=Ds(e,t),I_=!1,si=Bn=q_=na=Bo=Ht=0,En=us=null,Id=!1,(t&8)!==0&&(t|=t&32);var l=e.entangledLanes;if(l!==0)for(e=e.entanglements,l&=t;0<l;){var o=31-Hn(l),a=1<<o;t|=e[o],l&=~a}return no=t,Sc(),n}function ig(e,t){Le=null,we.H=vs,t===mi||t===Mc?(t=th(),ut=3):t===k_?(t=th(),ut=4):ut=t===U_?8:t!==null&&typeof t=="object"&&typeof t.then=="function"?6:1,An=t,Xe===null&&(Ht=1,ac(e,tl(t,e.current)))}function sg(){var e=jn.current;return e===null?!0:(Qe&4194048)===Qe?ll===null:(Qe&62914560)===Qe||(Qe&536870912)!==0?e===ll:!1}function rg(){var e=we.H;return we.H=vs,e===null?vs:e}function cg(){var e=we.A;return we.A=f2,e}function uc(){Ht=4,xo||(Qe&4194048)!==Qe&&jn.current!==null||(gi=!0),(Bo&134217727)===0&&(na&134217727)===0||pt===null||vo(pt,Qe,Bn,!1)}function nd(e,t,n){var l=lt;lt|=2;var o=rg(),a=cg();(pt!==e||Qe!==t)&&(cc=null,ci(e,t)),t=!1;var i=Ht;e:do try{if(ut!==0&&Xe!==null){var s=Xe,r=An;switch(ut){case 8:Q_(),i=6;break e;case 3:case 2:case 9:case 6:jn.current===null&&(t=!0);var p=ut;if(ut=0,An=null,Ga(e,s,r,p),n&&gi){i=0;break e}break;default:p=ut,ut=0,An=null,Ga(e,s,r,p)}}g2(),i=Ht;break}catch(f){ig(e,f)}while(!0);return t&&e.shellSuspendCounter++,Vl=_a=null,lt=l,we.H=o,we.A=a,Xe===null&&(pt=null,Qe=0,Sc()),i}function g2(){for(;Xe!==null;)ug(Xe)}function y2(e,t){var n=lt;lt|=2;var l=rg(),o=cg();pt!==e||Qe!==t?(cc=null,rc=On()+500,ci(e,t)):gi=Ds(e,t);e:do try{if(ut!==0&&Xe!==null){t=Xe;var a=An;t:switch(ut){case 1:ut=0,An=null,Ga(e,t,a,1);break;case 2:case 9:if(eh(a)){ut=0,An=null,Sh(t);break}t=function(){ut!==2&&ut!==9||pt!==e||(ut=7),zl(e)},a.then(t,t);break e;case 3:ut=7;break e;case 4:ut=5;break e;case 7:eh(a)?(ut=0,An=null,Sh(t)):(ut=0,An=null,Ga(e,t,a,7));break;case 5:var i=null;switch(Xe.tag){case 26:i=Xe.memoizedState;case 5:case 27:var s=Xe;if(i?Ng(i):s.stateNode.complete){ut=0,An=null;var r=s.sibling;if(r!==null)Xe=r;else{var p=s.return;p!==null?(Xe=p,Lc(p)):Xe=null}break t}}ut=0,An=null,Ga(e,t,a,5);break;case 6:ut=0,An=null,Ga(e,t,a,6);break;case 8:Q_(),Ht=6;break e;default:throw Error(O(462))}}p2();break}catch(f){ig(e,f)}while(!0);return Vl=_a=null,we.H=l,we.A=o,lt=n,Xe!==null?0:(pt=null,Qe=0,Sc(),Ht)}function p2(){for(;Xe!==null&&!jp();)ug(Xe)}function ug(e){var t=$m(e.alternate,e,no);e.memoizedProps=e.pendingProps,t===null?Lc(e):Xe=t}function Sh(e){var t=e,n=t.alternate;switch(t.tag){case 15:case 0:t=yh(n,t,t.pendingProps,t.type,void 0,Qe);break;case 11:t=yh(n,t,t.pendingProps,t.type.render,t.ref,Qe);break;case 5:N_(t);default:Hm(n,t),t=Xe=H1(t,no),t=$m(n,t,no)}e.memoizedProps=e.pendingProps,t===null?Lc(e):Xe=t}function Ga(e,t,n,l){Vl=_a=null,N_(t),Ja=null,bs=0;var o=t.return;try{if(i2(e,o,t,n,Qe)){Ht=1,ac(e,tl(n,e.current)),Xe=null;return}}catch(a){if(o!==null)throw Xe=o,a;Ht=1,ac(e,tl(n,e.current)),Xe=null;return}t.flags&32768?(We||l===1?e=!0:gi||(Qe&536870912)!==0?e=!1:(xo=e=!0,(l===2||l===9||l===3||l===6)&&(l=jn.current,l!==null&&l.tag===13&&(l.flags|=16384))),dg(t,e)):Lc(t)}function Lc(e){var t=e;do{if((t.flags&32768)!==0){dg(t,xo);return}e=t.return;var n=c2(t.alternate,t,no);if(n!==null){Xe=n;return}if(t=t.sibling,t!==null){Xe=t;return}Xe=t=e}while(t!==null);Ht===0&&(Ht=5)}function dg(e,t){do{var n=u2(e.alternate,e);if(n!==null){n.flags&=32767,Xe=n;return}if(n=e.return,n!==null&&(n.flags|=32768,n.subtreeFlags=0,n.deletions=null),!t&&(e=e.sibling,e!==null)){Xe=e;return}Xe=e=n}while(e!==null);Ht=6,Xe=null}function Ch(e,t,n,l,o,a,i,s,r){e.cancelPendingCommit=null;do Rc();while(Pt!==0);if((lt&6)!==0)throw Error(O(327));if(t!==null){if(t===e.current)throw Error(O(177));if(a=t.lanes|t.childLanes,a|=g_,Fp(e,n,a,i,s,r),e===pt&&(Xe=pt=null,Qe=0),ri=t,To=e,Fl=n,qd=a,Qd=o,lg=l,(t.subtreeFlags&10256)!==0||(t.flags&10256)!==0?(e.callbackNode=null,e.callbackPriority=0,w2(Vr,function(){return gg(),null})):(e.callbackNode=null,e.callbackPriority=0),l=(t.flags&13878)!==0,(t.subtreeFlags&13878)!==0||l){l=we.T,we.T=null,o=ot.p,ot.p=2,i=lt,lt|=4;try{d2(e,t,n)}finally{lt=i,ot.p=o,we.T=l}}Pt=1,_g(),fg(),hg()}}function _g(){if(Pt===1){Pt=0;var e=To,t=ri,n=(t.flags&13878)!==0;if((t.subtreeFlags&13878)!==0||n){n=we.T,we.T=null;var l=ot.p;ot.p=2;var o=lt;lt|=4;try{Zm(t,e);var a=Kd,i=N1(e.containerInfo),s=a.focusedElem,r=a.selectionRange;if(i!==s&&s&&s.ownerDocument&&D1(s.ownerDocument.documentElement,s)){if(r!==null&&m_(s)){var p=r.start,f=r.end;if(f===void 0&&(f=p),"selectionStart"in s)s.selectionStart=p,s.selectionEnd=Math.min(f,s.value.length);else{var b=s.ownerDocument||document,_=b&&b.defaultView||window;if(_.getSelection){var w=_.getSelection(),C=s.textContent.length,z=Math.min(r.start,C),D=r.end===void 0?z:Math.min(r.end,C);!w.extend&&z>D&&(i=D,D=z,z=i);var h=G0(s,z),y=G0(s,D);if(h&&y&&(w.rangeCount!==1||w.anchorNode!==h.node||w.anchorOffset!==h.offset||w.focusNode!==y.node||w.focusOffset!==y.offset)){var k=b.createRange();k.setStart(h.node,h.offset),w.removeAllRanges(),z>D?(w.addRange(k),w.extend(y.node,y.offset)):(k.setEnd(y.node,y.offset),w.addRange(k))}}}}for(b=[],w=s;w=w.parentNode;)w.nodeType===1&&b.push({element:w,left:w.scrollLeft,top:w.scrollTop});for(typeof s.focus=="function"&&s.focus(),s=0;s<b.length;s++){var E=b[s];E.element.scrollLeft=E.left,E.element.scrollTop=E.top}}pc=!!Zd,Kd=Zd=null}finally{lt=o,ot.p=l,we.T=n}}e.current=t,Pt=2}}function fg(){if(Pt===2){Pt=0;var e=To,t=ri,n=(t.flags&8772)!==0;if((t.subtreeFlags&8772)!==0||n){n=we.T,we.T=null;var l=ot.p;ot.p=2;var o=lt;lt|=4;try{qm(e,t.alternate,t)}finally{lt=o,ot.p=l,we.T=n}}Pt=3}}function hg(){if(Pt===4||Pt===3){Pt=0,Xp();var e=To,t=ri,n=Fl,l=lg;(t.subtreeFlags&10256)!==0||(t.flags&10256)!==0?Pt=5:(Pt=0,ri=To=null,mg(e,e.pendingLanes));var o=e.pendingLanes;if(o===0&&(Eo=null),r_(n),t=t.stateNode,$n&&typeof $n.onCommitFiberRoot=="function")try{$n.onCommitFiberRoot(Ts,t,void 0,(t.current.flags&128)===128)}catch{}if(l!==null){t=we.T,o=ot.p,ot.p=2,we.T=null;try{for(var a=e.onRecoverableError,i=0;i<l.length;i++){var s=l[i];a(s.value,{componentStack:s.stack})}}finally{we.T=t,ot.p=o}}(Fl&3)!==0&&Rc(),zl(e),o=e.pendingLanes,(n&261930)!==0&&(o&42)!==0?e===Wd?ds++:(ds=0,Wd=e):ds=0,Os(0,!1)}}function mg(e,t){(e.pooledCacheLanes&=t)===0&&(t=e.pooledCache,t!=null&&(e.pooledCache=null,Ls(t)))}function Rc(){return _g(),fg(),hg(),gg()}function gg(){if(Pt!==5)return!1;var e=To,t=qd;qd=0;var n=r_(Fl),l=we.T,o=ot.p;try{ot.p=32>n?32:n,we.T=null,n=Qd,Qd=null;var a=To,i=Fl;if(Pt=0,ri=To=null,Fl=0,(lt&6)!==0)throw Error(O(331));var s=lt;if(lt|=4,eg(a.current),Fm(a,a.current,i,n),lt=s,Os(0,!1),$n&&typeof $n.onPostCommitFiberRoot=="function")try{$n.onPostCommitFiberRoot(Ts,a)}catch{}return!0}finally{ot.p=o,we.T=l,mg(e,t)}}function Mh(e,t,n){t=tl(n,t),t=Ud(e.stateNode,t,2),e=Mo(e,t,2),e!==null&&(Ns(e,2),zl(e))}function dt(e,t,n){if(e.tag===3)Mh(e,e,n);else for(;t!==null;){if(t.tag===3){Mh(t,e,n);break}else if(t.tag===1){var l=t.stateNode;if(typeof t.type.getDerivedStateFromError=="function"||typeof l.componentDidCatch=="function"&&(Eo===null||!Eo.has(l))){e=tl(n,e),n=zm(2),l=Mo(t,n,2),l!==null&&(Am(n,l,t,e),Ns(l,2),zl(l));break}}t=t.return}}function ld(e,t,n){var l=e.pingCache;if(l===null){l=e.pingCache=new h2;var o=new Set;l.set(t,o)}else o=l.get(t),o===void 0&&(o=new Set,l.set(t,o));o.has(n)||(I_=!0,o.add(n),e=b2.bind(null,e,t,n),t.then(e,e))}function b2(e,t,n){var l=e.pingCache;l!==null&&l.delete(t),e.pingedLanes|=e.suspendedLanes&n,e.warmLanes&=~n,pt===e&&(Qe&n)===n&&(Ht===4||Ht===3&&(Qe&62914560)===Qe&&300>On()-zc?(lt&2)===0&&ci(e,0):q_|=n,si===Qe&&(si=0)),zl(e)}function yg(e,t){t===0&&(t=r1()),e=da(e,t),e!==null&&(Ns(e,t),zl(e))}function x2(e){var t=e.memoizedState,n=0;t!==null&&(n=t.retryLane),yg(e,n)}function v2(e,t){var n=0;switch(e.tag){case 31:case 13:var l=e.stateNode,o=e.memoizedState;o!==null&&(n=o.retryLane);break;case 19:l=e.stateNode;break;case 22:l=e.stateNode._retryCache;break;default:throw Error(O(314))}l!==null&&l.delete(t),yg(e,n)}function w2(e,t){return i_(e,t)}var dc=null,Ba=null,Gd=!1,_c=!1,od=!1,wo=0;function zl(e){e!==Ba&&e.next===null&&(Ba===null?dc=Ba=e:Ba=Ba.next=e),_c=!0,Gd||(Gd=!0,S2())}function Os(e,t){if(!od&&_c){od=!0;do for(var n=!1,l=dc;l!==null;){if(!t)if(e!==0){var o=l.pendingLanes;if(o===0)var a=0;else{var i=l.suspendedLanes,s=l.pingedLanes;a=(1<<31-Hn(42|e)+1)-1,a&=o&~(i&~s),a=a&201326741?a&201326741|1:a?a|2:0}a!==0&&(n=!0,Eh(l,a))}else a=Qe,a=xc(l,l===pt?a:0,l.cancelPendingCommit!==null||l.timeoutHandle!==-1),(a&3)===0||Ds(l,a)||(n=!0,Eh(l,a));l=l.next}while(n);od=!1}}function k2(){pg()}function pg(){_c=Gd=!1;var e=0;wo!==0&&A2()&&(e=wo);for(var t=On(),n=null,l=dc;l!==null;){var o=l.next,a=bg(l,t);a===0?(l.next=null,n===null?dc=o:n.next=o,o===null&&(Ba=n)):(n=l,(e!==0||(a&3)!==0)&&(_c=!0)),l=o}Pt!==0&&Pt!==5||Os(e,!1),wo!==0&&(wo=0)}function bg(e,t){for(var n=e.suspendedLanes,l=e.pingedLanes,o=e.expirationTimes,a=e.pendingLanes&-62914561;0<a;){var i=31-Hn(a),s=1<<i,r=o[i];r===-1?((s&n)===0||(s&l)!==0)&&(o[i]=Kp(s,t)):r<=t&&(e.expiredLanes|=s),a&=~s}if(t=pt,n=Qe,n=xc(e,e===t?n:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),l=e.callbackNode,n===0||e===t&&(ut===2||ut===9)||e.cancelPendingCommit!==null)return l!==null&&l!==null&&Lu(l),e.callbackNode=null,e.callbackPriority=0;if((n&3)===0||Ds(e,n)){if(t=n&-n,t===e.callbackPriority)return t;switch(l!==null&&Lu(l),r_(n)){case 2:case 8:n=i1;break;case 32:n=Vr;break;case 268435456:n=s1;break;default:n=Vr}return l=xg.bind(null,e),n=i_(n,l),e.callbackPriority=t,e.callbackNode=n,t}return l!==null&&l!==null&&Lu(l),e.callbackPriority=2,e.callbackNode=null,2}function xg(e,t){if(Pt!==0&&Pt!==5)return e.callbackNode=null,e.callbackPriority=0,null;var n=e.callbackNode;if(Rc()&&e.callbackNode!==n)return null;var l=Qe;return l=xc(e,e===pt?l:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),l===0?null:(ag(e,l,t),bg(e,On()),e.callbackNode!=null&&e.callbackNode===n?xg.bind(null,e):null)}function Eh(e,t){if(Rc())return null;ag(e,t,!0)}function S2(){R2(function(){(lt&6)!==0?i_(a1,k2):pg()})}function W_(){if(wo===0){var e=oi;e===0&&(e=fr,fr<<=1,(fr&261888)===0&&(fr=256)),wo=e}return wo}function Th(e){return e==null||typeof e=="symbol"||typeof e=="boolean"?null:typeof e=="function"?e:zr(""+e)}function Dh(e,t){var n=t.ownerDocument.createElement("input");return n.name=t.name,n.value=t.value,e.id&&n.setAttribute("form",e.id),t.parentNode.insertBefore(n,t),e=new FormData(e),n.parentNode.removeChild(n),e}function C2(e,t,n,l,o){if(t==="submit"&&n&&n.stateNode===o){var a=Th((o[Dn]||null).action),i=l.submitter;i&&(t=(t=i[Dn]||null)?Th(t.formAction):i.getAttribute("formAction"),t!==null&&(a=t,i=null));var s=new vc("action","action",null,l,o);e.push({event:s,listeners:[{instance:null,listener:function(){if(l.defaultPrevented){if(wo!==0){var r=i?Dh(o,i):new FormData(o);$d(n,{pending:!0,data:r,method:o.method,action:a},null,r)}}else typeof a=="function"&&(s.preventDefault(),r=i?Dh(o,i):new FormData(o),$d(n,{pending:!0,data:r,method:o.method,action:a},a,r))},currentTarget:o}]})}}for(Cr=0;Cr<Cd.length;Cr++)Mr=Cd[Cr],Nh=Mr.toLowerCase(),zh=Mr[0].toUpperCase()+Mr.slice(1),ml(Nh,"on"+zh);var Mr,Nh,zh,Cr;ml(A1,"onAnimationEnd");ml(L1,"onAnimationIteration");ml(R1,"onAnimationStart");ml("dblclick","onDoubleClick");ml("focusin","onFocus");ml("focusout","onBlur");ml(I5,"onTransitionRun");ml(q5,"onTransitionStart");ml(Q5,"onTransitionCancel");ml(B1,"onTransitionEnd");ni("onMouseEnter",["mouseout","mouseover"]);ni("onMouseLeave",["mouseout","mouseover"]);ni("onPointerEnter",["pointerout","pointerover"]);ni("onPointerLeave",["pointerout","pointerover"]);ra("onChange","change click focusin focusout input keydown keyup selectionchange".split(" "));ra("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));ra("onBeforeInput",["compositionend","keypress","textInput","paste"]);ra("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" "));ra("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" "));ra("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var ws="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),M2=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(ws));function vg(e,t){t=(t&4)!==0;for(var n=0;n<e.length;n++){var l=e[n],o=l.event;l=l.listeners;e:{var a=void 0;if(t)for(var i=l.length-1;0<=i;i--){var s=l[i],r=s.instance,p=s.currentTarget;if(s=s.listener,r!==a&&o.isPropagationStopped())break e;a=s,o.currentTarget=p;try{a(o)}catch(f){Kr(f)}o.currentTarget=null,a=r}else for(i=0;i<l.length;i++){if(s=l[i],r=s.instance,p=s.currentTarget,s=s.listener,r!==a&&o.isPropagationStopped())break e;a=s,o.currentTarget=p;try{a(o)}catch(f){Kr(f)}o.currentTarget=null,a=r}}}}function je(e,t){var n=t[yd];n===void 0&&(n=t[yd]=new Set);var l=e+"__bubble";n.has(l)||(wg(t,e,2,!1),n.add(l))}function ad(e,t,n){var l=0;t&&(l|=4),wg(n,e,l,t)}var Er="_reactListening"+Math.random().toString(36).slice(2);function G_(e){if(!e[Er]){e[Er]=!0,f1.forEach(function(n){n!=="selectionchange"&&(M2.has(n)||ad(n,!1,e),ad(n,!0,e))});var t=e.nodeType===9?e:e.ownerDocument;t===null||t[Er]||(t[Er]=!0,ad("selectionchange",!1,t))}}function wg(e,t,n,l){switch(Bg(t)){case 2:var o=eb;break;case 8:o=tb;break;default:o=F_}n=o.bind(null,t,n,e),o=void 0,!wd||t!=="touchstart"&&t!=="touchmove"&&t!=="wheel"||(o=!0),l?o!==void 0?e.addEventListener(t,n,{capture:!0,passive:o}):e.addEventListener(t,n,!0):o!==void 0?e.addEventListener(t,n,{passive:o}):e.addEventListener(t,n,!1)}function id(e,t,n,l,o){var a=l;if((t&1)===0&&(t&2)===0&&l!==null)e:for(;;){if(l===null)return;var i=l.tag;if(i===3||i===4){var s=l.stateNode.containerInfo;if(s===o)break;if(i===4)for(i=l.return;i!==null;){var r=i.tag;if((r===3||r===4)&&i.stateNode.containerInfo===o)return;i=i.return}for(;s!==null;){if(i=Ha(s),i===null)return;if(r=i.tag,r===5||r===6||r===26||r===27){l=a=i;continue e}s=s.parentNode}}l=l.return}v1(function(){var p=a,f=d_(n),b=[];e:{var _=O1.get(e);if(_!==void 0){var w=vc,C=e;switch(e){case"keypress":if(Lr(n)===0)break e;case"keydown":case"keyup":w=v5;break;case"focusin":C="focus",w=Hu;break;case"focusout":C="blur",w=Hu;break;case"beforeblur":case"afterblur":w=Hu;break;case"click":if(n.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":w=H0;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":w=c5;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":w=S5;break;case A1:case L1:case R1:w=_5;break;case B1:w=M5;break;case"scroll":case"scrollend":w=s5;break;case"wheel":w=T5;break;case"copy":case"cut":case"paste":w=h5;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":w=Y0;break;case"toggle":case"beforetoggle":w=N5}var z=(t&4)!==0,D=!z&&(e==="scroll"||e==="scrollend"),h=z?_!==null?_+"Capture":null:_;z=[];for(var y=p,k;y!==null;){var E=y;if(k=E.stateNode,E=E.tag,E!==5&&E!==26&&E!==27||k===null||h===null||(E=hs(y,h),E!=null&&z.push(ks(y,E,k))),D)break;y=y.return}0<z.length&&(_=new w(_,C,null,n,f),b.push({event:_,listeners:z}))}}if((t&7)===0){e:{if(_=e==="mouseover"||e==="pointerover",w=e==="mouseout"||e==="pointerout",_&&n!==vd&&(C=n.relatedTarget||n.fromElement)&&(Ha(C)||C[_i]))break e;if((w||_)&&(_=f.window===f?f:(_=f.ownerDocument)?_.defaultView||_.parentWindow:window,w?(C=n.relatedTarget||n.toElement,w=p,C=C?Ha(C):null,C!==null&&(D=Es(C),z=C.tag,C!==D||z!==5&&z!==27&&z!==6)&&(C=null)):(w=null,C=p),w!==C)){if(z=H0,E="onMouseLeave",h="onMouseEnter",y="mouse",(e==="pointerout"||e==="pointerover")&&(z=Y0,E="onPointerLeave",h="onPointerEnter",y="pointer"),D=w==null?_:Fi(w),k=C==null?_:Fi(C),_=new z(E,y+"leave",w,n,f),_.target=D,_.relatedTarget=k,E=null,Ha(f)===p&&(z=new z(h,y+"enter",C,n,f),z.target=k,z.relatedTarget=D,E=z),D=E,w&&C)t:{for(z=E2,h=w,y=C,k=0,E=h;E;E=z(E))k++;E=0;for(var Q=y;Q;Q=z(Q))E++;for(;0<k-E;)h=z(h),k--;for(;0<E-k;)y=z(y),E--;for(;k--;){if(h===y||y!==null&&h===y.alternate){z=h;break t}h=z(h),y=z(y)}z=null}else z=null;w!==null&&Ah(b,_,w,z,!1),C!==null&&D!==null&&Ah(b,D,C,z,!0)}}e:{if(_=p?Fi(p):window,w=_.nodeName&&_.nodeName.toLowerCase(),w==="select"||w==="input"&&_.type==="file")var oe=q0;else if(I0(_))if(E1)oe=Y5;else{oe=H5;var L=$5}else w=_.nodeName,!w||w.toLowerCase()!=="input"||_.type!=="checkbox"&&_.type!=="radio"?p&&u_(p.elementType)&&(oe=q0):oe=U5;if(oe&&(oe=oe(e,p))){M1(b,oe,n,f);break e}L&&L(e,_,p),e==="focusout"&&p&&_.type==="number"&&p.memoizedProps.value!=null&&xd(_,"number",_.value)}switch(L=p?Fi(p):window,e){case"focusin":(I0(L)||L.contentEditable==="true")&&(ja=L,kd=p,ns=null);break;case"focusout":ns=kd=ja=null;break;case"mousedown":Sd=!0;break;case"contextmenu":case"mouseup":case"dragend":Sd=!1,V0(b,n,f);break;case"selectionchange":if(X5)break;case"keydown":case"keyup":V0(b,n,f)}var K;if(h_)e:{switch(e){case"compositionstart":var ee="onCompositionStart";break e;case"compositionend":ee="onCompositionEnd";break e;case"compositionupdate":ee="onCompositionUpdate";break e}ee=void 0}else Ya?S1(e,n)&&(ee="onCompositionEnd"):e==="keydown"&&n.keyCode===229&&(ee="onCompositionStart");ee&&(k1&&n.locale!=="ko"&&(Ya||ee!=="onCompositionStart"?ee==="onCompositionEnd"&&Ya&&(K=w1()):(bo=f,__="value"in bo?bo.value:bo.textContent,Ya=!0)),L=fc(p,ee),0<L.length&&(ee=new U0(ee,e,null,n,f),b.push({event:ee,listeners:L}),K?ee.data=K:(K=C1(n),K!==null&&(ee.data=K)))),(K=A5?L5(e,n):R5(e,n))&&(ee=fc(p,"onBeforeInput"),0<ee.length&&(L=new U0("onBeforeInput","beforeinput",null,n,f),b.push({event:L,listeners:ee}),L.data=K)),C2(b,e,p,n,f)}vg(b,t)})}function ks(e,t,n){return{instance:e,listener:t,currentTarget:n}}function fc(e,t){for(var n=t+"Capture",l=[];e!==null;){var o=e,a=o.stateNode;if(o=o.tag,o!==5&&o!==26&&o!==27||a===null||(o=hs(e,n),o!=null&&l.unshift(ks(e,o,a)),o=hs(e,t),o!=null&&l.push(ks(e,o,a))),e.tag===3)return l;e=e.return}return[]}function E2(e){if(e===null)return null;do e=e.return;while(e&&e.tag!==5&&e.tag!==27);return e||null}function Ah(e,t,n,l,o){for(var a=t._reactName,i=[];n!==null&&n!==l;){var s=n,r=s.alternate,p=s.stateNode;if(s=s.tag,r!==null&&r===l)break;s!==5&&s!==26&&s!==27||p===null||(r=p,o?(p=hs(n,a),p!=null&&i.unshift(ks(n,p,r))):o||(p=hs(n,a),p!=null&&i.push(ks(n,p,r)))),n=n.return}i.length!==0&&e.push({event:t,listeners:i})}var T2=/\r\n?/g,D2=/\u0000|\uFFFD/g;function Lh(e){return(typeof e=="string"?e:""+e).replace(T2,`
`).replace(D2,"")}function kg(e,t){return t=Lh(t),Lh(e)===t}function mt(e,t,n,l,o,a){switch(n){case"children":typeof l=="string"?t==="body"||t==="textarea"&&l===""||li(e,l):(typeof l=="number"||typeof l=="bigint")&&t!=="body"&&li(e,""+l);break;case"className":gr(e,"class",l);break;case"tabIndex":gr(e,"tabindex",l);break;case"dir":case"role":case"viewBox":case"width":case"height":gr(e,n,l);break;case"style":x1(e,l,a);break;case"data":if(t!=="object"){gr(e,"data",l);break}case"src":case"href":if(l===""&&(t!=="a"||n!=="href")){e.removeAttribute(n);break}if(l==null||typeof l=="function"||typeof l=="symbol"||typeof l=="boolean"){e.removeAttribute(n);break}l=zr(""+l),e.setAttribute(n,l);break;case"action":case"formAction":if(typeof l=="function"){e.setAttribute(n,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof a=="function"&&(n==="formAction"?(t!=="input"&&mt(e,t,"name",o.name,o,null),mt(e,t,"formEncType",o.formEncType,o,null),mt(e,t,"formMethod",o.formMethod,o,null),mt(e,t,"formTarget",o.formTarget,o,null)):(mt(e,t,"encType",o.encType,o,null),mt(e,t,"method",o.method,o,null),mt(e,t,"target",o.target,o,null)));if(l==null||typeof l=="symbol"||typeof l=="boolean"){e.removeAttribute(n);break}l=zr(""+l),e.setAttribute(n,l);break;case"onClick":l!=null&&(e.onclick=Gl);break;case"onScroll":l!=null&&je("scroll",e);break;case"onScrollEnd":l!=null&&je("scrollend",e);break;case"dangerouslySetInnerHTML":if(l!=null){if(typeof l!="object"||!("__html"in l))throw Error(O(61));if(n=l.__html,n!=null){if(o.children!=null)throw Error(O(60));e.innerHTML=n}}break;case"multiple":e.multiple=l&&typeof l!="function"&&typeof l!="symbol";break;case"muted":e.muted=l&&typeof l!="function"&&typeof l!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(l==null||typeof l=="function"||typeof l=="boolean"||typeof l=="symbol"){e.removeAttribute("xlink:href");break}n=zr(""+l),e.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",n);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":l!=null&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,""+l):e.removeAttribute(n);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":l&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,""):e.removeAttribute(n);break;case"capture":case"download":l===!0?e.setAttribute(n,""):l!==!1&&l!=null&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,l):e.removeAttribute(n);break;case"cols":case"rows":case"size":case"span":l!=null&&typeof l!="function"&&typeof l!="symbol"&&!isNaN(l)&&1<=l?e.setAttribute(n,l):e.removeAttribute(n);break;case"rowSpan":case"start":l==null||typeof l=="function"||typeof l=="symbol"||isNaN(l)?e.removeAttribute(n):e.setAttribute(n,l);break;case"popover":je("beforetoggle",e),je("toggle",e),Nr(e,"popover",l);break;case"xlinkActuate":Ul(e,"http://www.w3.org/1999/xlink","xlink:actuate",l);break;case"xlinkArcrole":Ul(e,"http://www.w3.org/1999/xlink","xlink:arcrole",l);break;case"xlinkRole":Ul(e,"http://www.w3.org/1999/xlink","xlink:role",l);break;case"xlinkShow":Ul(e,"http://www.w3.org/1999/xlink","xlink:show",l);break;case"xlinkTitle":Ul(e,"http://www.w3.org/1999/xlink","xlink:title",l);break;case"xlinkType":Ul(e,"http://www.w3.org/1999/xlink","xlink:type",l);break;case"xmlBase":Ul(e,"http://www.w3.org/XML/1998/namespace","xml:base",l);break;case"xmlLang":Ul(e,"http://www.w3.org/XML/1998/namespace","xml:lang",l);break;case"xmlSpace":Ul(e,"http://www.w3.org/XML/1998/namespace","xml:space",l);break;case"is":Nr(e,"is",l);break;case"innerText":case"textContent":break;default:(!(2<n.length)||n[0]!=="o"&&n[0]!=="O"||n[1]!=="n"&&n[1]!=="N")&&(n=a5.get(n)||n,Nr(e,n,l))}}function Vd(e,t,n,l,o,a){switch(n){case"style":x1(e,l,a);break;case"dangerouslySetInnerHTML":if(l!=null){if(typeof l!="object"||!("__html"in l))throw Error(O(61));if(n=l.__html,n!=null){if(o.children!=null)throw Error(O(60));e.innerHTML=n}}break;case"children":typeof l=="string"?li(e,l):(typeof l=="number"||typeof l=="bigint")&&li(e,""+l);break;case"onScroll":l!=null&&je("scroll",e);break;case"onScrollEnd":l!=null&&je("scrollend",e);break;case"onClick":l!=null&&(e.onclick=Gl);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!h1.hasOwnProperty(n))e:{if(n[0]==="o"&&n[1]==="n"&&(o=n.endsWith("Capture"),t=n.slice(2,o?n.length-7:void 0),a=e[Dn]||null,a=a!=null?a[n]:null,typeof a=="function"&&e.removeEventListener(t,a,o),typeof l=="function")){typeof a!="function"&&a!==null&&(n in e?e[n]=null:e.hasAttribute(n)&&e.removeAttribute(n)),e.addEventListener(t,l,o);break e}n in e?e[n]=l:l===!0?e.setAttribute(n,""):Nr(e,n,l)}}}function dn(e,t,n){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":je("error",e),je("load",e);var l=!1,o=!1,a;for(a in n)if(n.hasOwnProperty(a)){var i=n[a];if(i!=null)switch(a){case"src":l=!0;break;case"srcSet":o=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(O(137,t));default:mt(e,t,a,i,n,null)}}o&&mt(e,t,"srcSet",n.srcSet,n,null),l&&mt(e,t,"src",n.src,n,null);return;case"input":je("invalid",e);var s=a=i=o=null,r=null,p=null;for(l in n)if(n.hasOwnProperty(l)){var f=n[l];if(f!=null)switch(l){case"name":o=f;break;case"type":i=f;break;case"checked":r=f;break;case"defaultChecked":p=f;break;case"value":a=f;break;case"defaultValue":s=f;break;case"children":case"dangerouslySetInnerHTML":if(f!=null)throw Error(O(137,t));break;default:mt(e,t,l,f,n,null)}}y1(e,a,s,r,p,i,o,!1);return;case"select":je("invalid",e),l=i=a=null;for(o in n)if(n.hasOwnProperty(o)&&(s=n[o],s!=null))switch(o){case"value":a=s;break;case"defaultValue":i=s;break;case"multiple":l=s;default:mt(e,t,o,s,n,null)}t=a,n=i,e.multiple=!!l,t!=null?Za(e,!!l,t,!1):n!=null&&Za(e,!!l,n,!0);return;case"textarea":je("invalid",e),a=o=l=null;for(i in n)if(n.hasOwnProperty(i)&&(s=n[i],s!=null))switch(i){case"value":l=s;break;case"defaultValue":o=s;break;case"children":a=s;break;case"dangerouslySetInnerHTML":if(s!=null)throw Error(O(91));break;default:mt(e,t,i,s,n,null)}b1(e,l,o,a);return;case"option":for(r in n)n.hasOwnProperty(r)&&(l=n[r],l!=null)&&(r==="selected"?e.selected=l&&typeof l!="function"&&typeof l!="symbol":mt(e,t,r,l,n,null));return;case"dialog":je("beforetoggle",e),je("toggle",e),je("cancel",e),je("close",e);break;case"iframe":case"object":je("load",e);break;case"video":case"audio":for(l=0;l<ws.length;l++)je(ws[l],e);break;case"image":je("error",e),je("load",e);break;case"details":je("toggle",e);break;case"embed":case"source":case"link":je("error",e),je("load",e);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(p in n)if(n.hasOwnProperty(p)&&(l=n[p],l!=null))switch(p){case"children":case"dangerouslySetInnerHTML":throw Error(O(137,t));default:mt(e,t,p,l,n,null)}return;default:if(u_(t)){for(f in n)n.hasOwnProperty(f)&&(l=n[f],l!==void 0&&Vd(e,t,f,l,n,void 0));return}}for(s in n)n.hasOwnProperty(s)&&(l=n[s],l!=null&&mt(e,t,s,l,n,null))}function N2(e,t,n,l){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var o=null,a=null,i=null,s=null,r=null,p=null,f=null;for(w in n){var b=n[w];if(n.hasOwnProperty(w)&&b!=null)switch(w){case"checked":break;case"value":break;case"defaultValue":r=b;default:l.hasOwnProperty(w)||mt(e,t,w,null,l,b)}}for(var _ in l){var w=l[_];if(b=n[_],l.hasOwnProperty(_)&&(w!=null||b!=null))switch(_){case"type":a=w;break;case"name":o=w;break;case"checked":p=w;break;case"defaultChecked":f=w;break;case"value":i=w;break;case"defaultValue":s=w;break;case"children":case"dangerouslySetInnerHTML":if(w!=null)throw Error(O(137,t));break;default:w!==b&&mt(e,t,_,w,l,b)}}bd(e,i,s,r,p,f,a,o);return;case"select":w=i=s=_=null;for(a in n)if(r=n[a],n.hasOwnProperty(a)&&r!=null)switch(a){case"value":break;case"multiple":w=r;default:l.hasOwnProperty(a)||mt(e,t,a,null,l,r)}for(o in l)if(a=l[o],r=n[o],l.hasOwnProperty(o)&&(a!=null||r!=null))switch(o){case"value":_=a;break;case"defaultValue":s=a;break;case"multiple":i=a;default:a!==r&&mt(e,t,o,a,l,r)}t=s,n=i,l=w,_!=null?Za(e,!!n,_,!1):!!l!=!!n&&(t!=null?Za(e,!!n,t,!0):Za(e,!!n,n?[]:"",!1));return;case"textarea":w=_=null;for(s in n)if(o=n[s],n.hasOwnProperty(s)&&o!=null&&!l.hasOwnProperty(s))switch(s){case"value":break;case"children":break;default:mt(e,t,s,null,l,o)}for(i in l)if(o=l[i],a=n[i],l.hasOwnProperty(i)&&(o!=null||a!=null))switch(i){case"value":_=o;break;case"defaultValue":w=o;break;case"children":break;case"dangerouslySetInnerHTML":if(o!=null)throw Error(O(91));break;default:o!==a&&mt(e,t,i,o,l,a)}p1(e,_,w);return;case"option":for(var C in n)_=n[C],n.hasOwnProperty(C)&&_!=null&&!l.hasOwnProperty(C)&&(C==="selected"?e.selected=!1:mt(e,t,C,null,l,_));for(r in l)_=l[r],w=n[r],l.hasOwnProperty(r)&&_!==w&&(_!=null||w!=null)&&(r==="selected"?e.selected=_&&typeof _!="function"&&typeof _!="symbol":mt(e,t,r,_,l,w));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var z in n)_=n[z],n.hasOwnProperty(z)&&_!=null&&!l.hasOwnProperty(z)&&mt(e,t,z,null,l,_);for(p in l)if(_=l[p],w=n[p],l.hasOwnProperty(p)&&_!==w&&(_!=null||w!=null))switch(p){case"children":case"dangerouslySetInnerHTML":if(_!=null)throw Error(O(137,t));break;default:mt(e,t,p,_,l,w)}return;default:if(u_(t)){for(var D in n)_=n[D],n.hasOwnProperty(D)&&_!==void 0&&!l.hasOwnProperty(D)&&Vd(e,t,D,void 0,l,_);for(f in l)_=l[f],w=n[f],!l.hasOwnProperty(f)||_===w||_===void 0&&w===void 0||Vd(e,t,f,_,l,w);return}}for(var h in n)_=n[h],n.hasOwnProperty(h)&&_!=null&&!l.hasOwnProperty(h)&&mt(e,t,h,null,l,_);for(b in l)_=l[b],w=n[b],!l.hasOwnProperty(b)||_===w||_==null&&w==null||mt(e,t,b,_,l,w)}function Rh(e){switch(e){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function z2(){if(typeof performance.getEntriesByType=="function"){for(var e=0,t=0,n=performance.getEntriesByType("resource"),l=0;l<n.length;l++){var o=n[l],a=o.transferSize,i=o.initiatorType,s=o.duration;if(a&&s&&Rh(i)){for(i=0,s=o.responseEnd,l+=1;l<n.length;l++){var r=n[l],p=r.startTime;if(p>s)break;var f=r.transferSize,b=r.initiatorType;f&&Rh(b)&&(r=r.responseEnd,i+=f*(r<s?1:(s-p)/(r-p)))}if(--l,t+=8*(a+i)/(o.duration/1e3),e++,10<e)break}}if(0<e)return t/e/1e6}return navigator.connection&&(e=navigator.connection.downlink,typeof e=="number")?e:5}var Zd=null,Kd=null;function hc(e){return e.nodeType===9?e:e.ownerDocument}function Bh(e){switch(e){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function Sg(e,t){if(e===0)switch(t){case"svg":return 1;case"math":return 2;default:return 0}return e===1&&t==="foreignObject"?0:e}function Fd(e,t){return e==="textarea"||e==="noscript"||typeof t.children=="string"||typeof t.children=="number"||typeof t.children=="bigint"||typeof t.dangerouslySetInnerHTML=="object"&&t.dangerouslySetInnerHTML!==null&&t.dangerouslySetInnerHTML.__html!=null}var sd=null;function A2(){var e=window.event;return e&&e.type==="popstate"?e===sd?!1:(sd=e,!0):(sd=null,!1)}var Cg=typeof setTimeout=="function"?setTimeout:void 0,L2=typeof clearTimeout=="function"?clearTimeout:void 0,Oh=typeof Promise=="function"?Promise:void 0,R2=typeof queueMicrotask=="function"?queueMicrotask:typeof Oh<"u"?function(e){return Oh.resolve(null).then(e).catch(B2)}:Cg;function B2(e){setTimeout(function(){throw e})}function $o(e){return e==="head"}function $h(e,t){var n=t,l=0;do{var o=n.nextSibling;if(e.removeChild(n),o&&o.nodeType===8)if(n=o.data,n==="/$"||n==="/&"){if(l===0){e.removeChild(o),di(t);return}l--}else if(n==="$"||n==="$?"||n==="$~"||n==="$!"||n==="&")l++;else if(n==="html")_s(e.ownerDocument.documentElement);else if(n==="head"){n=e.ownerDocument.head,_s(n);for(var a=n.firstChild;a;){var i=a.nextSibling,s=a.nodeName;a[zs]||s==="SCRIPT"||s==="STYLE"||s==="LINK"&&a.rel.toLowerCase()==="stylesheet"||n.removeChild(a),a=i}}else n==="body"&&_s(e.ownerDocument.body);n=o}while(n);di(t)}function Hh(e,t){var n=e;e=0;do{var l=n.nextSibling;if(n.nodeType===1?t?(n._stashedDisplay=n.style.display,n.style.display="none"):(n.style.display=n._stashedDisplay||"",n.getAttribute("style")===""&&n.removeAttribute("style")):n.nodeType===3&&(t?(n._stashedText=n.nodeValue,n.nodeValue=""):n.nodeValue=n._stashedText||""),l&&l.nodeType===8)if(n=l.data,n==="/$"){if(e===0)break;e--}else n!=="$"&&n!=="$?"&&n!=="$~"&&n!=="$!"||e++;n=l}while(n)}function Jd(e){var t=e.firstChild;for(t&&t.nodeType===10&&(t=t.nextSibling);t;){var n=t;switch(t=t.nextSibling,n.nodeName){case"HTML":case"HEAD":case"BODY":Jd(n),c_(n);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(n.rel.toLowerCase()==="stylesheet")continue}e.removeChild(n)}}function O2(e,t,n,l){for(;e.nodeType===1;){var o=n;if(e.nodeName.toLowerCase()!==t.toLowerCase()){if(!l&&(e.nodeName!=="INPUT"||e.type!=="hidden"))break}else if(l){if(!e[zs])switch(t){case"meta":if(!e.hasAttribute("itemprop"))break;return e;case"link":if(a=e.getAttribute("rel"),a==="stylesheet"&&e.hasAttribute("data-precedence"))break;if(a!==o.rel||e.getAttribute("href")!==(o.href==null||o.href===""?null:o.href)||e.getAttribute("crossorigin")!==(o.crossOrigin==null?null:o.crossOrigin)||e.getAttribute("title")!==(o.title==null?null:o.title))break;return e;case"style":if(e.hasAttribute("data-precedence"))break;return e;case"script":if(a=e.getAttribute("src"),(a!==(o.src==null?null:o.src)||e.getAttribute("type")!==(o.type==null?null:o.type)||e.getAttribute("crossorigin")!==(o.crossOrigin==null?null:o.crossOrigin))&&a&&e.hasAttribute("async")&&!e.hasAttribute("itemprop"))break;return e;default:return e}}else if(t==="input"&&e.type==="hidden"){var a=o.name==null?null:""+o.name;if(o.type==="hidden"&&e.getAttribute("name")===a)return e}else return e;if(e=ol(e.nextSibling),e===null)break}return null}function $2(e,t,n){if(t==="")return null;for(;e.nodeType!==3;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!n||(e=ol(e.nextSibling),e===null))return null;return e}function Mg(e,t){for(;e.nodeType!==8;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!t||(e=ol(e.nextSibling),e===null))return null;return e}function Pd(e){return e.data==="$?"||e.data==="$~"}function e_(e){return e.data==="$!"||e.data==="$?"&&e.ownerDocument.readyState!=="loading"}function H2(e,t){var n=e.ownerDocument;if(e.data==="$~")e._reactRetry=t;else if(e.data!=="$?"||n.readyState!=="loading")t();else{var l=function(){t(),n.removeEventListener("DOMContentLoaded",l)};n.addEventListener("DOMContentLoaded",l),e._reactRetry=l}}function ol(e){for(;e!=null;e=e.nextSibling){var t=e.nodeType;if(t===1||t===3)break;if(t===8){if(t=e.data,t==="$"||t==="$!"||t==="$?"||t==="$~"||t==="&"||t==="F!"||t==="F")break;if(t==="/$"||t==="/&")return null}}return e}var t_=null;function Uh(e){e=e.nextSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="/$"||n==="/&"){if(t===0)return ol(e.nextSibling);t--}else n!=="$"&&n!=="$!"&&n!=="$?"&&n!=="$~"&&n!=="&"||t++}e=e.nextSibling}return null}function Yh(e){e=e.previousSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="$"||n==="$!"||n==="$?"||n==="$~"||n==="&"){if(t===0)return e;t--}else n!=="/$"&&n!=="/&"||t++}e=e.previousSibling}return null}function Eg(e,t,n){switch(t=hc(n),e){case"html":if(e=t.documentElement,!e)throw Error(O(452));return e;case"head":if(e=t.head,!e)throw Error(O(453));return e;case"body":if(e=t.body,!e)throw Error(O(454));return e;default:throw Error(O(451))}}function _s(e){for(var t=e.attributes;t.length;)e.removeAttributeNode(t[0]);c_(e)}var al=new Map,jh=new Set;function mc(e){return typeof e.getRootNode=="function"?e.getRootNode():e.nodeType===9?e:e.ownerDocument}var lo=ot.d;ot.d={f:U2,r:Y2,D:j2,C:X2,L:I2,m:q2,X:W2,S:Q2,M:G2};function U2(){var e=lo.f(),t=Ac();return e||t}function Y2(e){var t=fi(e);t!==null&&t.tag===5&&t.type==="form"?xm(t):lo.r(e)}var yi=typeof document>"u"?null:document;function Tg(e,t,n){var l=yi;if(l&&typeof t=="string"&&t){var o=el(t);o='link[rel="'+e+'"][href="'+o+'"]',typeof n=="string"&&(o+='[crossorigin="'+n+'"]'),jh.has(o)||(jh.add(o),e={rel:e,crossOrigin:n,href:t},l.querySelector(o)===null&&(t=l.createElement("link"),dn(t,"link",e),ln(t),l.head.appendChild(t)))}}function j2(e){lo.D(e),Tg("dns-prefetch",e,null)}function X2(e,t){lo.C(e,t),Tg("preconnect",e,t)}function I2(e,t,n){lo.L(e,t,n);var l=yi;if(l&&e&&t){var o='link[rel="preload"][as="'+el(t)+'"]';t==="image"&&n&&n.imageSrcSet?(o+='[imagesrcset="'+el(n.imageSrcSet)+'"]',typeof n.imageSizes=="string"&&(o+='[imagesizes="'+el(n.imageSizes)+'"]')):o+='[href="'+el(e)+'"]';var a=o;switch(t){case"style":a=ui(e);break;case"script":a=pi(e)}al.has(a)||(e=Et({rel:"preload",href:t==="image"&&n&&n.imageSrcSet?void 0:e,as:t},n),al.set(a,e),l.querySelector(o)!==null||t==="style"&&l.querySelector($s(a))||t==="script"&&l.querySelector(Hs(a))||(t=l.createElement("link"),dn(t,"link",e),ln(t),l.head.appendChild(t)))}}function q2(e,t){lo.m(e,t);var n=yi;if(n&&e){var l=t&&typeof t.as=="string"?t.as:"script",o='link[rel="modulepreload"][as="'+el(l)+'"][href="'+el(e)+'"]',a=o;switch(l){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":a=pi(e)}if(!al.has(a)&&(e=Et({rel:"modulepreload",href:e},t),al.set(a,e),n.querySelector(o)===null)){switch(l){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(n.querySelector(Hs(a)))return}l=n.createElement("link"),dn(l,"link",e),ln(l),n.head.appendChild(l)}}}function Q2(e,t,n){lo.S(e,t,n);var l=yi;if(l&&e){var o=Va(l).hoistableStyles,a=ui(e);t=t||"default";var i=o.get(a);if(!i){var s={loading:0,preload:null};if(i=l.querySelector($s(a)))s.loading=5;else{e=Et({rel:"stylesheet",href:e,"data-precedence":t},n),(n=al.get(a))&&V_(e,n);var r=i=l.createElement("link");ln(r),dn(r,"link",e),r._p=new Promise(function(p,f){r.onload=p,r.onerror=f}),r.addEventListener("load",function(){s.loading|=1}),r.addEventListener("error",function(){s.loading|=2}),s.loading|=4,jr(i,t,l)}i={type:"stylesheet",instance:i,count:1,state:s},o.set(a,i)}}}function W2(e,t){lo.X(e,t);var n=yi;if(n&&e){var l=Va(n).hoistableScripts,o=pi(e),a=l.get(o);a||(a=n.querySelector(Hs(o)),a||(e=Et({src:e,async:!0},t),(t=al.get(o))&&Z_(e,t),a=n.createElement("script"),ln(a),dn(a,"link",e),n.head.appendChild(a)),a={type:"script",instance:a,count:1,state:null},l.set(o,a))}}function G2(e,t){lo.M(e,t);var n=yi;if(n&&e){var l=Va(n).hoistableScripts,o=pi(e),a=l.get(o);a||(a=n.querySelector(Hs(o)),a||(e=Et({src:e,async:!0,type:"module"},t),(t=al.get(o))&&Z_(e,t),a=n.createElement("script"),ln(a),dn(a,"link",e),n.head.appendChild(a)),a={type:"script",instance:a,count:1,state:null},l.set(o,a))}}function Xh(e,t,n,l){var o=(o=ko.current)?mc(o):null;if(!o)throw Error(O(446));switch(e){case"meta":case"title":return null;case"style":return typeof n.precedence=="string"&&typeof n.href=="string"?(t=ui(n.href),n=Va(o).hoistableStyles,l=n.get(t),l||(l={type:"style",instance:null,count:0,state:null},n.set(t,l)),l):{type:"void",instance:null,count:0,state:null};case"link":if(n.rel==="stylesheet"&&typeof n.href=="string"&&typeof n.precedence=="string"){e=ui(n.href);var a=Va(o).hoistableStyles,i=a.get(e);if(i||(o=o.ownerDocument||o,i={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},a.set(e,i),(a=o.querySelector($s(e)))&&!a._p&&(i.instance=a,i.state.loading=5),al.has(e)||(n={rel:"preload",as:"style",href:n.href,crossOrigin:n.crossOrigin,integrity:n.integrity,media:n.media,hrefLang:n.hrefLang,referrerPolicy:n.referrerPolicy},al.set(e,n),a||V2(o,e,n,i.state))),t&&l===null)throw Error(O(528,""));return i}if(t&&l!==null)throw Error(O(529,""));return null;case"script":return t=n.async,n=n.src,typeof n=="string"&&t&&typeof t!="function"&&typeof t!="symbol"?(t=pi(n),n=Va(o).hoistableScripts,l=n.get(t),l||(l={type:"script",instance:null,count:0,state:null},n.set(t,l)),l):{type:"void",instance:null,count:0,state:null};default:throw Error(O(444,e))}}function ui(e){return'href="'+el(e)+'"'}function $s(e){return'link[rel="stylesheet"]['+e+"]"}function Dg(e){return Et({},e,{"data-precedence":e.precedence,precedence:null})}function V2(e,t,n,l){e.querySelector('link[rel="preload"][as="style"]['+t+"]")?l.loading=1:(t=e.createElement("link"),l.preload=t,t.addEventListener("load",function(){return l.loading|=1}),t.addEventListener("error",function(){return l.loading|=2}),dn(t,"link",n),ln(t),e.head.appendChild(t))}function pi(e){return'[src="'+el(e)+'"]'}function Hs(e){return"script[async]"+e}function Ih(e,t,n){if(t.count++,t.instance===null)switch(t.type){case"style":var l=e.querySelector('style[data-href~="'+el(n.href)+'"]');if(l)return t.instance=l,ln(l),l;var o=Et({},n,{"data-href":n.href,"data-precedence":n.precedence,href:null,precedence:null});return l=(e.ownerDocument||e).createElement("style"),ln(l),dn(l,"style",o),jr(l,n.precedence,e),t.instance=l;case"stylesheet":o=ui(n.href);var a=e.querySelector($s(o));if(a)return t.state.loading|=4,t.instance=a,ln(a),a;l=Dg(n),(o=al.get(o))&&V_(l,o),a=(e.ownerDocument||e).createElement("link"),ln(a);var i=a;return i._p=new Promise(function(s,r){i.onload=s,i.onerror=r}),dn(a,"link",l),t.state.loading|=4,jr(a,n.precedence,e),t.instance=a;case"script":return a=pi(n.src),(o=e.querySelector(Hs(a)))?(t.instance=o,ln(o),o):(l=n,(o=al.get(a))&&(l=Et({},n),Z_(l,o)),e=e.ownerDocument||e,o=e.createElement("script"),ln(o),dn(o,"link",l),e.head.appendChild(o),t.instance=o);case"void":return null;default:throw Error(O(443,t.type))}else t.type==="stylesheet"&&(t.state.loading&4)===0&&(l=t.instance,t.state.loading|=4,jr(l,n.precedence,e));return t.instance}function jr(e,t,n){for(var l=n.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),o=l.length?l[l.length-1]:null,a=o,i=0;i<l.length;i++){var s=l[i];if(s.dataset.precedence===t)a=s;else if(a!==o)break}a?a.parentNode.insertBefore(e,a.nextSibling):(t=n.nodeType===9?n.head:n,t.insertBefore(e,t.firstChild))}function V_(e,t){e.crossOrigin==null&&(e.crossOrigin=t.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=t.referrerPolicy),e.title==null&&(e.title=t.title)}function Z_(e,t){e.crossOrigin==null&&(e.crossOrigin=t.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=t.referrerPolicy),e.integrity==null&&(e.integrity=t.integrity)}var Xr=null;function qh(e,t,n){if(Xr===null){var l=new Map,o=Xr=new Map;o.set(n,l)}else o=Xr,l=o.get(n),l||(l=new Map,o.set(n,l));if(l.has(e))return l;for(l.set(e,null),n=n.getElementsByTagName(e),o=0;o<n.length;o++){var a=n[o];if(!(a[zs]||a[rn]||e==="link"&&a.getAttribute("rel")==="stylesheet")&&a.namespaceURI!=="http://www.w3.org/2000/svg"){var i=a.getAttribute(t)||"";i=e+i;var s=l.get(i);s?s.push(a):l.set(i,[a])}}return l}function Qh(e,t,n){e=e.ownerDocument||e,e.head.insertBefore(n,t==="title"?e.querySelector("head > title"):null)}function Z2(e,t,n){if(n===1||t.itemProp!=null)return!1;switch(e){case"meta":case"title":return!0;case"style":if(typeof t.precedence!="string"||typeof t.href!="string"||t.href==="")break;return!0;case"link":if(typeof t.rel!="string"||typeof t.href!="string"||t.href===""||t.onLoad||t.onError)break;return t.rel==="stylesheet"?(e=t.disabled,typeof t.precedence=="string"&&e==null):!0;case"script":if(t.async&&typeof t.async!="function"&&typeof t.async!="symbol"&&!t.onLoad&&!t.onError&&t.src&&typeof t.src=="string")return!0}return!1}function Ng(e){return!(e.type==="stylesheet"&&(e.state.loading&3)===0)}function K2(e,t,n,l){if(n.type==="stylesheet"&&(typeof l.media!="string"||matchMedia(l.media).matches!==!1)&&(n.state.loading&4)===0){if(n.instance===null){var o=ui(l.href),a=t.querySelector($s(o));if(a){t=a._p,t!==null&&typeof t=="object"&&typeof t.then=="function"&&(e.count++,e=gc.bind(e),t.then(e,e)),n.state.loading|=4,n.instance=a,ln(a);return}a=t.ownerDocument||t,l=Dg(l),(o=al.get(o))&&V_(l,o),a=a.createElement("link"),ln(a);var i=a;i._p=new Promise(function(s,r){i.onload=s,i.onerror=r}),dn(a,"link",l),n.instance=a}e.stylesheets===null&&(e.stylesheets=new Map),e.stylesheets.set(n,t),(t=n.state.preload)&&(n.state.loading&3)===0&&(e.count++,n=gc.bind(e),t.addEventListener("load",n),t.addEventListener("error",n))}}var rd=0;function F2(e,t){return e.stylesheets&&e.count===0&&Ir(e,e.stylesheets),0<e.count||0<e.imgCount?function(n){var l=setTimeout(function(){if(e.stylesheets&&Ir(e,e.stylesheets),e.unsuspend){var a=e.unsuspend;e.unsuspend=null,a()}},6e4+t);0<e.imgBytes&&rd===0&&(rd=62500*z2());var o=setTimeout(function(){if(e.waitingForImages=!1,e.count===0&&(e.stylesheets&&Ir(e,e.stylesheets),e.unsuspend)){var a=e.unsuspend;e.unsuspend=null,a()}},(e.imgBytes>rd?50:800)+t);return e.unsuspend=n,function(){e.unsuspend=null,clearTimeout(l),clearTimeout(o)}}:null}function gc(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)Ir(this,this.stylesheets);else if(this.unsuspend){var e=this.unsuspend;this.unsuspend=null,e()}}}var yc=null;function Ir(e,t){e.stylesheets=null,e.unsuspend!==null&&(e.count++,yc=new Map,t.forEach(J2,e),yc=null,gc.call(e))}function J2(e,t){if(!(t.state.loading&4)){var n=yc.get(e);if(n)var l=n.get(null);else{n=new Map,yc.set(e,n);for(var o=e.querySelectorAll("link[data-precedence],style[data-precedence]"),a=0;a<o.length;a++){var i=o[a];(i.nodeName==="LINK"||i.getAttribute("media")!=="not all")&&(n.set(i.dataset.precedence,i),l=i)}l&&n.set(null,l)}o=t.instance,i=o.getAttribute("data-precedence"),a=n.get(i)||l,a===l&&n.set(null,o),n.set(i,o),this.count++,l=gc.bind(this),o.addEventListener("load",l),o.addEventListener("error",l),a?a.parentNode.insertBefore(o,a.nextSibling):(e=e.nodeType===9?e.head:e,e.insertBefore(o,e.firstChild)),t.state.loading|=4}}var Ss={$$typeof:Wl,Provider:null,Consumer:null,_currentValue:Jo,_currentValue2:Jo,_threadCount:0};function P2(e,t,n,l,o,a,i,s,r){this.tag=1,this.containerInfo=e,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Ru(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Ru(0),this.hiddenUpdates=Ru(null),this.identifierPrefix=l,this.onUncaughtError=o,this.onCaughtError=a,this.onRecoverableError=i,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=r,this.incompleteTransitions=new Map}function zg(e,t,n,l,o,a,i,s,r,p,f,b){return e=new P2(e,t,n,i,r,p,f,b,s),t=1,a===!0&&(t|=24),a=Rn(3,null,null,t),e.current=a,a.stateNode=e,t=v_(),t.refCount++,e.pooledCache=t,t.refCount++,a.memoizedState={element:l,isDehydrated:n,cache:t},S_(a),e}function Ag(e){return e?(e=qa,e):qa}function Lg(e,t,n,l,o,a){o=Ag(o),l.context===null?l.context=o:l.pendingContext=o,l=Co(t),l.payload={element:n},a=a===void 0?null:a,a!==null&&(l.callback=a),n=Mo(e,l,t),n!==null&&(Tn(n,e,t),os(n,e,t))}function Wh(e,t){if(e=e.memoizedState,e!==null&&e.dehydrated!==null){var n=e.retryLane;e.retryLane=n!==0&&n<t?n:t}}function K_(e,t){Wh(e,t),(e=e.alternate)&&Wh(e,t)}function Rg(e){if(e.tag===13||e.tag===31){var t=da(e,67108864);t!==null&&Tn(t,e,67108864),K_(e,67108864)}}function Gh(e){if(e.tag===13||e.tag===31){var t=Un();t=s_(t);var n=da(e,t);n!==null&&Tn(n,e,t),K_(e,t)}}var pc=!0;function eb(e,t,n,l){var o=we.T;we.T=null;var a=ot.p;try{ot.p=2,F_(e,t,n,l)}finally{ot.p=a,we.T=o}}function tb(e,t,n,l){var o=we.T;we.T=null;var a=ot.p;try{ot.p=8,F_(e,t,n,l)}finally{ot.p=a,we.T=o}}function F_(e,t,n,l){if(pc){var o=n_(l);if(o===null)id(e,t,l,bc,n),Vh(e,l);else if(lb(o,e,t,n,l))l.stopPropagation();else if(Vh(e,l),t&4&&-1<nb.indexOf(e)){for(;o!==null;){var a=fi(o);if(a!==null)switch(a.tag){case 3:if(a=a.stateNode,a.current.memoizedState.isDehydrated){var i=Zo(a.pendingLanes);if(i!==0){var s=a;for(s.pendingLanes|=2,s.entangledLanes|=2;i;){var r=1<<31-Hn(i);s.entanglements[1]|=r,i&=~r}zl(a),(lt&6)===0&&(rc=On()+500,Os(0,!1))}}break;case 31:case 13:s=da(a,2),s!==null&&Tn(s,a,2),Ac(),K_(a,2)}if(a=n_(l),a===null&&id(e,t,l,bc,n),a===o)break;o=a}o!==null&&l.stopPropagation()}else id(e,t,l,null,n)}}function n_(e){return e=d_(e),J_(e)}var bc=null;function J_(e){if(bc=null,e=Ha(e),e!==null){var t=Es(e);if(t===null)e=null;else{var n=t.tag;if(n===13){if(e=e1(t),e!==null)return e;e=null}else if(n===31){if(e=t1(t),e!==null)return e;e=null}else if(n===3){if(t.stateNode.current.memoizedState.isDehydrated)return t.tag===3?t.stateNode.containerInfo:null;e=null}else t!==e&&(e=null)}}return bc=e,null}function Bg(e){switch(e){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(Ip()){case a1:return 2;case i1:return 8;case Vr:case qp:return 32;case s1:return 268435456;default:return 32}default:return 32}}var l_=!1,Do=null,No=null,zo=null,Cs=new Map,Ms=new Map,yo=[],nb="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function Vh(e,t){switch(e){case"focusin":case"focusout":Do=null;break;case"dragenter":case"dragleave":No=null;break;case"mouseover":case"mouseout":zo=null;break;case"pointerover":case"pointerout":Cs.delete(t.pointerId);break;case"gotpointercapture":case"lostpointercapture":Ms.delete(t.pointerId)}}function Gi(e,t,n,l,o,a){return e===null||e.nativeEvent!==a?(e={blockedOn:t,domEventName:n,eventSystemFlags:l,nativeEvent:a,targetContainers:[o]},t!==null&&(t=fi(t),t!==null&&Rg(t)),e):(e.eventSystemFlags|=l,t=e.targetContainers,o!==null&&t.indexOf(o)===-1&&t.push(o),e)}function lb(e,t,n,l,o){switch(t){case"focusin":return Do=Gi(Do,e,t,n,l,o),!0;case"dragenter":return No=Gi(No,e,t,n,l,o),!0;case"mouseover":return zo=Gi(zo,e,t,n,l,o),!0;case"pointerover":var a=o.pointerId;return Cs.set(a,Gi(Cs.get(a)||null,e,t,n,l,o)),!0;case"gotpointercapture":return a=o.pointerId,Ms.set(a,Gi(Ms.get(a)||null,e,t,n,l,o)),!0}return!1}function Og(e){var t=Ha(e.target);if(t!==null){var n=Es(t);if(n!==null){if(t=n.tag,t===13){if(t=e1(n),t!==null){e.blockedOn=t,z0(e.priority,function(){Gh(n)});return}}else if(t===31){if(t=t1(n),t!==null){e.blockedOn=t,z0(e.priority,function(){Gh(n)});return}}else if(t===3&&n.stateNode.current.memoizedState.isDehydrated){e.blockedOn=n.tag===3?n.stateNode.containerInfo:null;return}}}e.blockedOn=null}function qr(e){if(e.blockedOn!==null)return!1;for(var t=e.targetContainers;0<t.length;){var n=n_(e.nativeEvent);if(n===null){n=e.nativeEvent;var l=new n.constructor(n.type,n);vd=l,n.target.dispatchEvent(l),vd=null}else return t=fi(n),t!==null&&Rg(t),e.blockedOn=n,!1;t.shift()}return!0}function Zh(e,t,n){qr(e)&&n.delete(t)}function ob(){l_=!1,Do!==null&&qr(Do)&&(Do=null),No!==null&&qr(No)&&(No=null),zo!==null&&qr(zo)&&(zo=null),Cs.forEach(Zh),Ms.forEach(Zh)}function Tr(e,t){e.blockedOn===t&&(e.blockedOn=null,l_||(l_=!0,en.unstable_scheduleCallback(en.unstable_NormalPriority,ob)))}var Dr=null;function Kh(e){Dr!==e&&(Dr=e,en.unstable_scheduleCallback(en.unstable_NormalPriority,function(){Dr===e&&(Dr=null);for(var t=0;t<e.length;t+=3){var n=e[t],l=e[t+1],o=e[t+2];if(typeof l!="function"){if(J_(l||n)===null)continue;break}var a=fi(n);a!==null&&(e.splice(t,3),t-=3,$d(a,{pending:!0,data:o,method:n.method,action:l},l,o))}}))}function di(e){function t(r){return Tr(r,e)}Do!==null&&Tr(Do,e),No!==null&&Tr(No,e),zo!==null&&Tr(zo,e),Cs.forEach(t),Ms.forEach(t);for(var n=0;n<yo.length;n++){var l=yo[n];l.blockedOn===e&&(l.blockedOn=null)}for(;0<yo.length&&(n=yo[0],n.blockedOn===null);)Og(n),n.blockedOn===null&&yo.shift();if(n=(e.ownerDocument||e).$$reactFormReplay,n!=null)for(l=0;l<n.length;l+=3){var o=n[l],a=n[l+1],i=o[Dn]||null;if(typeof a=="function")i||Kh(n);else if(i){var s=null;if(a&&a.hasAttribute("formAction")){if(o=a,i=a[Dn]||null)s=i.formAction;else if(J_(o)!==null)continue}else s=i.action;typeof s=="function"?n[l+1]=s:(n.splice(l,3),l-=3),Kh(n)}}}function $g(){function e(a){a.canIntercept&&a.info==="react-transition"&&a.intercept({handler:function(){return new Promise(function(i){return o=i})},focusReset:"manual",scroll:"manual"})}function t(){o!==null&&(o(),o=null),l||setTimeout(n,20)}function n(){if(!l&&!navigation.transition){var a=navigation.currentEntry;a&&a.url!=null&&navigation.navigate(a.url,{state:a.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var l=!1,o=null;return navigation.addEventListener("navigate",e),navigation.addEventListener("navigatesuccess",t),navigation.addEventListener("navigateerror",t),setTimeout(n,100),function(){l=!0,navigation.removeEventListener("navigate",e),navigation.removeEventListener("navigatesuccess",t),navigation.removeEventListener("navigateerror",t),o!==null&&(o(),o=null)}}}function P_(e){this._internalRoot=e}Bc.prototype.render=P_.prototype.render=function(e){var t=this._internalRoot;if(t===null)throw Error(O(409));var n=t.current,l=Un();Lg(n,l,e,t,null,null)};Bc.prototype.unmount=P_.prototype.unmount=function(){var e=this._internalRoot;if(e!==null){this._internalRoot=null;var t=e.containerInfo;Lg(e.current,2,null,e,null,null),Ac(),t[_i]=null}};function Bc(e){this._internalRoot=e}Bc.prototype.unstable_scheduleHydration=function(e){if(e){var t=_1();e={blockedOn:null,target:e,priority:t};for(var n=0;n<yo.length&&t!==0&&t<yo[n].priority;n++);yo.splice(n,0,e),n===0&&Og(e)}};var Fh=Jh.version;if(Fh!=="19.2.4")throw Error(O(527,Fh,"19.2.4"));ot.findDOMNode=function(e){var t=e._reactInternals;if(t===void 0)throw typeof e.render=="function"?Error(O(188)):(e=Object.keys(e).join(","),Error(O(268,e)));return e=Op(t),e=e!==null?n1(e):null,e=e===null?null:e.stateNode,e};var ab={bundleType:0,version:"19.2.4",rendererPackageName:"react-dom",currentDispatcherRef:we,reconcilerVersion:"19.2.4"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"&&(Vi=__REACT_DEVTOOLS_GLOBAL_HOOK__,!Vi.isDisabled&&Vi.supportsFiber))try{Ts=Vi.inject(ab),$n=Vi}catch{}var Vi;Oc.createRoot=function(e,t){if(!Ph(e))throw Error(O(299));var n=!1,l="",o=Tm,a=Dm,i=Nm;return t!=null&&(t.unstable_strictMode===!0&&(n=!0),t.identifierPrefix!==void 0&&(l=t.identifierPrefix),t.onUncaughtError!==void 0&&(o=t.onUncaughtError),t.onCaughtError!==void 0&&(a=t.onCaughtError),t.onRecoverableError!==void 0&&(i=t.onRecoverableError)),t=zg(e,1,!1,null,null,n,l,null,o,a,i,$g),e[_i]=t.current,G_(e),new P_(t)};Oc.hydrateRoot=function(e,t,n){if(!Ph(e))throw Error(O(299));var l=!1,o="",a=Tm,i=Dm,s=Nm,r=null;return n!=null&&(n.unstable_strictMode===!0&&(l=!0),n.identifierPrefix!==void 0&&(o=n.identifierPrefix),n.onUncaughtError!==void 0&&(a=n.onUncaughtError),n.onCaughtError!==void 0&&(i=n.onCaughtError),n.onRecoverableError!==void 0&&(s=n.onRecoverableError),n.formState!==void 0&&(r=n.formState)),t=zg(e,1,!0,t,n??null,l,o,r,a,i,s,$g),t.context=Ag(null),n=t.current,l=Un(),l=s_(l),o=Co(l),o.callback=null,Mo(n,o,l),n=l,t.current.lanes=n,Ns(t,n),zl(t),e[_i]=t.current,G_(e),new Bc(t)};Oc.version="19.2.4"});var jg=Sl((j4,Yg)=>{"use strict";function Ug(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Ug)}catch(e){console.error(e)}}Ug(),Yg.exports=Hg()});var Ig=Sl($c=>{"use strict";var ib=Symbol.for("react.transitional.element"),sb=Symbol.for("react.fragment");function Xg(e,t,n){var l=null;if(n!==void 0&&(l=""+n),t.key!==void 0&&(l=""+t.key),"key"in t){n={};for(var o in t)o!=="key"&&(n[o]=t[o])}else n=t;return t=n.ref,{$$typeof:ib,type:e,key:l,ref:t!==void 0?t:null,props:n}}$c.Fragment=sb;$c.jsx=Xg;$c.jsxs=Xg});var pn=Sl((I4,qg)=>{"use strict";qg.exports=Ig()});var Oy=wt(Vn()),$y=wt(jg());var T=wt(Vn(),1),gy=wt(dr(),1),Lt=wt(Vn(),1),G=wt(pn(),1),Nt=wt(pn(),1),Ll=wt(Vn(),1),by=wt(dr(),1),ya=wt(pn(),1),hf=wt(pn(),1),Je=wt(Vn(),1),u=wt(pn(),1),xt=wt(pn(),1),Rt=wt(Vn(),1),c=wt(pn(),1),ke=wt(Vn(),1),Ve=wt(pn(),1),Ly=wt(Vn(),1),Xn=wt(pn(),1),Gs=wt(pn(),1),Ry=wt(Vn(),1),Si=wt(pn(),1),Ci=wt(pn(),1),Z=wt(pn(),1),j=wt(pn(),1),rb=`.styles-module__popup___IhzrD svg[fill=none] {
  fill: none !important;
}
.styles-module__popup___IhzrD svg[fill=none] :not([fill]) {
  fill: none !important;
}

@keyframes styles-module__popupEnter___AuQDN {
  from {
    opacity: 0;
    transform: translateX(-50%) scale(0.95) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) scale(1) translateY(0);
  }
}
@keyframes styles-module__popupExit___JJKQX {
  from {
    opacity: 1;
    transform: translateX(-50%) scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50%) scale(0.95) translateY(4px);
  }
}
@keyframes styles-module__shake___jdbWe {
  0%, 100% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(0);
  }
  20% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(-3px);
  }
  40% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(3px);
  }
  60% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(-2px);
  }
  80% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(2px);
  }
}
.styles-module__popup___IhzrD {
  position: fixed;
  transform: translateX(-50%);
  width: 280px;
  padding: 0.75rem 1rem 14px;
  background: #1a1a1a;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
  z-index: 100001;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  will-change: transform, opacity;
  opacity: 0;
}
.styles-module__popup___IhzrD.styles-module__enter___L7U7N {
  animation: styles-module__popupEnter___AuQDN 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
.styles-module__popup___IhzrD.styles-module__entered___COX-w {
  opacity: 1;
  transform: translateX(-50%) scale(1) translateY(0);
}
.styles-module__popup___IhzrD.styles-module__exit___5eGjE {
  animation: styles-module__popupExit___JJKQX 0.15s ease-in forwards;
}
.styles-module__popup___IhzrD.styles-module__entered___COX-w.styles-module__shake___jdbWe {
  animation: styles-module__shake___jdbWe 0.25s ease-out;
}

.styles-module__header___wWsSi {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5625rem;
}

.styles-module__element___fTV2z {
  font-size: 0.75rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.styles-module__headerToggle___WpW0b {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  flex: 1;
  min-width: 0;
  text-align: left;
}
.styles-module__headerToggle___WpW0b .styles-module__element___fTV2z {
  flex: 1;
}

.styles-module__chevron___ZZJlR {
  color: rgba(255, 255, 255, 0.5);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
}
.styles-module__chevron___ZZJlR.styles-module__expanded___2Hxgv {
  transform: rotate(90deg);
}

.styles-module__stylesWrapper___pnHgy {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.styles-module__stylesWrapper___pnHgy.styles-module__expanded___2Hxgv {
  grid-template-rows: 1fr;
}

.styles-module__stylesInner___YYZe2 {
  overflow: hidden;
}

.styles-module__stylesBlock___VfQKn {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.375rem;
  padding: 0.5rem 0.625rem;
  margin-bottom: 0.5rem;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.6875rem;
  line-height: 1.5;
}

.styles-module__styleLine___1YQiD {
  color: rgba(255, 255, 255, 0.85);
  word-break: break-word;
}

.styles-module__styleProperty___84L1i {
  color: #c792ea;
}

.styles-module__styleValue___q51-h {
  color: rgba(255, 255, 255, 0.85);
}

.styles-module__timestamp___Dtpsv {
  font-size: 0.625rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  font-variant-numeric: tabular-nums;
  margin-left: 0.5rem;
  flex-shrink: 0;
}

.styles-module__quote___mcMmQ {
  font-size: 12px;
  font-style: italic;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.5rem;
  padding: 0.4rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.25rem;
  line-height: 1.45;
}

.styles-module__textarea___jrSae {
  box-sizing: border-box;
  width: 100%;
  padding: 0.5rem 0.625rem;
  font-size: 0.8125rem;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  resize: none;
  outline: none;
  transition: border-color 0.15s ease;
}
.styles-module__textarea___jrSae:focus {
  border-color: var(--agentation-color-blue);
}
.styles-module__textarea___jrSae.styles-module__green___99l3h:focus {
  border-color: var(--agentation-color-green);
}
.styles-module__textarea___jrSae::placeholder {
  color: rgba(255, 255, 255, 0.35);
}
.styles-module__textarea___jrSae::-webkit-scrollbar {
  width: 6px;
}
.styles-module__textarea___jrSae::-webkit-scrollbar-track {
  background: transparent;
}
.styles-module__textarea___jrSae::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.styles-module__actions___D6x3f {
  display: flex;
  justify-content: flex-end;
  gap: 0.375rem;
  margin-top: 0.5rem;
}

.styles-module__cancel___hRjnL,
.styles-module__submit___K-mIR {
  padding: 0.4rem 0.875rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, opacity 0.15s ease;
}

.styles-module__cancel___hRjnL {
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
}
.styles-module__cancel___hRjnL:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.styles-module__submit___K-mIR {
  color: white;
}
.styles-module__submit___K-mIR:hover:not(:disabled) {
  filter: brightness(0.9);
}
.styles-module__submit___K-mIR:disabled {
  cursor: not-allowed;
}

.styles-module__deleteWrapper___oSjdo {
  margin-right: auto;
}

.styles-module__deleteButton___4VuAE {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
}
.styles-module__deleteButton___4VuAE:hover {
  background-color: color-mix(in srgb, var(--agentation-color-red) 25%, transparent);
  color: var(--agentation-color-red);
}
.styles-module__deleteButton___4VuAE:active {
  transform: scale(0.92);
}

.styles-module__light___6AaSQ.styles-module__popup___IhzrD {
  background: #fff;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.06);
}
.styles-module__light___6AaSQ .styles-module__element___fTV2z {
  color: rgba(0, 0, 0, 0.6);
}
.styles-module__light___6AaSQ .styles-module__timestamp___Dtpsv {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__chevron___ZZJlR {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__stylesBlock___VfQKn {
  background: rgba(0, 0, 0, 0.03);
}
.styles-module__light___6AaSQ .styles-module__styleLine___1YQiD {
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__styleProperty___84L1i {
  color: #7c3aed;
}
.styles-module__light___6AaSQ .styles-module__styleValue___q51-h {
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__quote___mcMmQ {
  color: rgba(0, 0, 0, 0.55);
  background: rgba(0, 0, 0, 0.04);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae {
  background: rgba(0, 0, 0, 0.03);
  color: #1a1a1a;
  border-color: rgba(0, 0, 0, 0.12);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae::placeholder {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
}
.styles-module__light___6AaSQ .styles-module__cancel___hRjnL {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___6AaSQ .styles-module__cancel___hRjnL:hover {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__deleteButton___4VuAE {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__deleteButton___4VuAE:hover {
  background-color: color-mix(in srgb, var(--agentation-color-red) 25%, transparent);
  color: var(--agentation-color-red);
}`,cb={popup:"styles-module__popup___IhzrD",enter:"styles-module__enter___L7U7N",popupEnter:"styles-module__popupEnter___AuQDN",entered:"styles-module__entered___COX-w",exit:"styles-module__exit___5eGjE",popupExit:"styles-module__popupExit___JJKQX",shake:"styles-module__shake___jdbWe",header:"styles-module__header___wWsSi",element:"styles-module__element___fTV2z",headerToggle:"styles-module__headerToggle___WpW0b",chevron:"styles-module__chevron___ZZJlR",expanded:"styles-module__expanded___2Hxgv",stylesWrapper:"styles-module__stylesWrapper___pnHgy",stylesInner:"styles-module__stylesInner___YYZe2",stylesBlock:"styles-module__stylesBlock___VfQKn",styleLine:"styles-module__styleLine___1YQiD",styleProperty:"styles-module__styleProperty___84L1i",styleValue:"styles-module__styleValue___q51-h",timestamp:"styles-module__timestamp___Dtpsv",quote:"styles-module__quote___mcMmQ",textarea:"styles-module__textarea___jrSae",green:"styles-module__green___99l3h",actions:"styles-module__actions___D6x3f",cancel:"styles-module__cancel___hRjnL",submit:"styles-module__submit___K-mIR",deleteWrapper:"styles-module__deleteWrapper___oSjdo",deleteButton:"styles-module__deleteButton___4VuAE",light:"styles-module__light___6AaSQ"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-annotation-popup-css-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-annotation-popup-css-styles",document.head.appendChild(e)),e.textContent=rb}var bt=cb,ub=`.icon-transitions-module__iconState___uqK9J {
  transition: opacity 0.2s ease, transform 0.2s ease;
  transform-origin: center;
}

.icon-transitions-module__iconStateFast___HxlMm {
  transition: opacity 0.15s ease, transform 0.15s ease;
  transform-origin: center;
}

.icon-transitions-module__iconFade___nPwXg {
  transition: opacity 0.2s ease;
}

.icon-transitions-module__iconFadeFast___Ofb2t {
  transition: opacity 0.15s ease;
}

.icon-transitions-module__visible___PlHsU {
  opacity: 1 !important;
}

.icon-transitions-module__visibleScaled___8Qog- {
  opacity: 1 !important;
  transform: scale(1);
}

.icon-transitions-module__hidden___ETykt {
  opacity: 0 !important;
}

.icon-transitions-module__hiddenScaled___JXn-m {
  opacity: 0 !important;
  transform: scale(0.8);
}

.icon-transitions-module__sending___uaLN- {
  opacity: 0.5 !important;
  transform: scale(0.8);
}`,db={iconState:"icon-transitions-module__iconState___uqK9J",iconStateFast:"icon-transitions-module__iconStateFast___HxlMm",iconFade:"icon-transitions-module__iconFade___nPwXg",iconFadeFast:"icon-transitions-module__iconFadeFast___Ofb2t",visible:"icon-transitions-module__visible___PlHsU",visibleScaled:"icon-transitions-module__visibleScaled___8Qog-",hidden:"icon-transitions-module__hidden___ETykt",hiddenScaled:"icon-transitions-module__hiddenScaled___JXn-m",sending:"icon-transitions-module__sending___uaLN-"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-components-icon-transitions");e||(e=document.createElement("style"),e.id="feedback-tool-styles-components-icon-transitions",document.head.appendChild(e)),e.textContent=ub}var yt=db;var _b=({size:e=16})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",children:(0,G.jsx)("path",{d:"M8 3v10M3 8h10",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})});var fb=({size:e=24,style:t={}})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",style:t,children:[(0,G.jsxs)("g",{clipPath:"url(#clip0_list_sparkle)",children:[(0,G.jsx)("path",{d:"M11.5 12L5.5 12",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M18.5 6.75L5.5 6.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M9.25 17.25L5.5 17.25",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M16 12.75L16.5179 13.9677C16.8078 14.6494 17.3506 15.1922 18.0323 15.4821L19.25 16L18.0323 16.5179C17.3506 16.8078 16.8078 17.3506 16.5179 18.0323L16 19.25L15.4821 18.0323C15.1922 17.3506 14.6494 16.8078 13.9677 16.5179L12.75 16L13.9677 15.4821C14.6494 15.1922 15.1922 14.6494 15.4821 13.9677L16 12.75Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinejoin:"round"})]}),(0,G.jsx)("defs",{children:(0,G.jsx)("clipPath",{id:"clip0_list_sparkle",children:(0,G.jsx)("rect",{width:"24",height:"24",fill:"white"})})})]}),hb=({size:e=20,...t})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",...t,children:[(0,G.jsx)("circle",{cx:"10",cy:"10",r:"5.375",stroke:"currentColor",strokeWidth:"1.25"}),(0,G.jsx)("path",{d:"M8.5 8.5C8.73 7.85 9.31 7.49 10 7.5C10.86 7.51 11.5 8.13 11.5 9C11.5 10.08 10 10.5 10 10.5V10.75",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("circle",{cx:"10",cy:"12.625",r:"0.625",fill:"currentColor"})]});var mb=({size:e=24,copied:t=!1,tint:n})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",style:n?{color:n,transition:"color 0.3s ease"}:void 0,children:[(0,G.jsxs)("g",{className:`${yt.iconState} ${t?yt.hiddenScaled:yt.visibleScaled}`,children:[(0,G.jsx)("path",{d:"M4.75 11.25C4.75 10.4216 5.42157 9.75 6.25 9.75H12.75C13.5784 9.75 14.25 10.4216 14.25 11.25V17.75C14.25 18.5784 13.5784 19.25 12.75 19.25H6.25C5.42157 19.25 4.75 18.5784 4.75 17.75V11.25Z",stroke:"currentColor",strokeWidth:"1.5"}),(0,G.jsx)("path",{d:"M17.25 14.25H17.75C18.5784 14.25 19.25 13.5784 19.25 12.75V6.25C19.25 5.42157 18.5784 4.75 17.75 4.75H11.25C10.4216 4.75 9.75 5.42157 9.75 6.25V6.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]}),(0,G.jsxs)("g",{className:`${yt.iconState} ${t?yt.visibleScaled:yt.hiddenScaled}`,children:[(0,G.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"var(--agentation-color-green)",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M15 10L11 14.25L9.25 12.25",stroke:"var(--agentation-color-green)",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]})]}),gb=({size:e=24,state:t="idle"})=>{let n=t==="idle",l=t==="sent",o=t==="failed",a=t==="sending";return(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsx)("g",{className:`${yt.iconStateFast} ${n?yt.visibleScaled:a?yt.sending:yt.hiddenScaled}`,children:(0,G.jsx)("path",{d:"M9.875 14.125L12.3506 19.6951C12.7184 20.5227 13.9091 20.4741 14.2083 19.6193L18.8139 6.46032C19.0907 5.6695 18.3305 4.90933 17.5397 5.18611L4.38072 9.79174C3.52589 10.0909 3.47731 11.2816 4.30494 11.6494L9.875 14.125ZM9.875 14.125L13.375 10.625",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})}),(0,G.jsxs)("g",{className:`${yt.iconStateFast} ${l?yt.visibleScaled:yt.hiddenScaled}`,children:[(0,G.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"var(--agentation-color-green)",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M15 10L11 14.25L9.25 12.25",stroke:"var(--agentation-color-green)",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,G.jsxs)("g",{className:`${yt.iconStateFast} ${o?yt.visibleScaled:yt.hiddenScaled}`,children:[(0,G.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"var(--agentation-color-red)",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M12 8V12",stroke:"var(--agentation-color-red)",strokeWidth:"1.5",strokeLinecap:"round"}),(0,G.jsx)("circle",{cx:"12",cy:"15",r:"0.5",fill:"var(--agentation-color-red)",stroke:"var(--agentation-color-red)",strokeWidth:"1"})]})]})};var yb=({size:e=24,isOpen:t=!0})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsxs)("g",{className:`${yt.iconFade} ${t?yt.visible:yt.hidden}`,children:[(0,G.jsx)("path",{d:"M3.91752 12.7539C3.65127 12.2996 3.65037 11.7515 3.9149 11.2962C4.9042 9.59346 7.72688 5.49994 12 5.49994C16.2731 5.49994 19.0958 9.59346 20.0851 11.2962C20.3496 11.7515 20.3487 12.2996 20.0825 12.7539C19.0908 14.4459 16.2694 18.4999 12 18.4999C7.73064 18.4999 4.90918 14.4459 3.91752 12.7539Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M12 14.8261C13.5608 14.8261 14.8261 13.5608 14.8261 12C14.8261 10.4392 13.5608 9.17392 12 9.17392C10.4392 9.17392 9.17391 10.4392 9.17391 12C9.17391 13.5608 10.4392 14.8261 12 14.8261Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,G.jsxs)("g",{className:`${yt.iconFade} ${t?yt.hidden:yt.visible}`,children:[(0,G.jsx)("path",{d:"M18.6025 9.28503C18.9174 8.9701 19.4364 8.99481 19.7015 9.35271C20.1484 9.95606 20.4943 10.507 20.7342 10.9199C21.134 11.6086 21.1329 12.4454 20.7303 13.1328C20.2144 14.013 19.2151 15.5225 17.7723 16.8193C16.3293 18.1162 14.3852 19.2497 12.0008 19.25C11.4192 19.25 10.8638 19.1823 10.3355 19.0613C9.77966 18.934 9.63498 18.2525 10.0382 17.8493C10.2412 17.6463 10.5374 17.573 10.8188 17.6302C11.1993 17.7076 11.5935 17.75 12.0008 17.75C13.8848 17.7497 15.4867 16.8568 16.7693 15.7041C18.0522 14.5511 18.9606 13.1867 19.4363 12.375C19.5656 12.1543 19.5659 11.8943 19.4373 11.6729C19.2235 11.3049 18.921 10.8242 18.5364 10.3003C18.3085 9.98991 18.3302 9.5573 18.6025 9.28503ZM12.0008 4.75C12.5814 4.75006 13.1358 4.81803 13.6632 4.93953C14.2182 5.06741 14.362 5.74812 13.9593 6.15091C13.7558 6.35435 13.4589 6.42748 13.1771 6.36984C12.7983 6.29239 12.4061 6.25006 12.0008 6.25C10.1167 6.25 8.51415 7.15145 7.23028 8.31543C5.94678 9.47919 5.03918 10.8555 4.56426 11.6729C4.43551 11.8945 4.43582 12.1542 4.56524 12.375C4.77587 12.7343 5.07189 13.2012 5.44718 13.7105C5.67623 14.0213 5.65493 14.4552 5.38193 14.7282C5.0671 15.0431 4.54833 15.0189 4.28292 14.6614C3.84652 14.0736 3.50813 13.5369 3.27129 13.1328C2.86831 12.4451 2.86717 11.6088 3.26739 10.9199C3.78185 10.0345 4.77959 8.51239 6.22247 7.2041C7.66547 5.89584 9.61202 4.75 12.0008 4.75Z",fill:"currentColor"}),(0,G.jsx)("path",{d:"M5 19L19 5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]})]}),pb=({size:e=24,isPaused:t=!1})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsxs)("g",{className:`${yt.iconFadeFast} ${t?yt.hidden:yt.visible}`,children:[(0,G.jsx)("path",{d:"M8 6L8 18",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"}),(0,G.jsx)("path",{d:"M16 18L16 6",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]}),(0,G.jsx)("path",{className:`${yt.iconFadeFast} ${t?yt.visible:yt.hidden}`,d:"M17.75 10.701C18.75 11.2783 18.75 12.7217 17.75 13.299L8.75 18.4952C7.75 19.0725 6.5 18.3509 6.5 17.1962L6.5 6.80384C6.5 5.64914 7.75 4.92746 8.75 5.50481L17.75 10.701Z",stroke:"currentColor",strokeWidth:"1.5"})]});var bb=({size:e=16})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsx)("path",{d:"M10.6504 5.81117C10.9939 4.39628 13.0061 4.39628 13.3496 5.81117C13.5715 6.72517 14.6187 7.15891 15.4219 6.66952C16.6652 5.91193 18.0881 7.33479 17.3305 8.57815C16.8411 9.38134 17.2748 10.4285 18.1888 10.6504C19.6037 10.9939 19.6037 13.0061 18.1888 13.3496C17.2748 13.5715 16.8411 14.6187 17.3305 15.4219C18.0881 16.6652 16.6652 18.0881 15.4219 17.3305C14.6187 16.8411 13.5715 17.2748 13.3496 18.1888C13.0061 19.6037 10.9939 19.6037 10.6504 18.1888C10.4285 17.2748 9.38135 16.8411 8.57815 17.3305C7.33479 18.0881 5.91193 16.6652 6.66952 15.4219C7.15891 14.6187 6.72517 13.5715 5.81117 13.3496C4.39628 13.0061 4.39628 10.9939 5.81117 10.6504C6.72517 10.4285 7.15891 9.38134 6.66952 8.57815C5.91193 7.33479 7.33479 5.91192 8.57815 6.66952C9.38135 7.15891 10.4285 6.72517 10.6504 5.81117Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("circle",{cx:"12",cy:"12",r:"2.5",stroke:"currentColor",strokeWidth:"1.5"})]});var xb=({size:e=16})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:(0,G.jsx)("path",{d:"M13.5 4C14.7426 4 15.75 5.00736 15.75 6.25V7H18.5C18.9142 7 19.25 7.33579 19.25 7.75C19.25 8.16421 18.9142 8.5 18.5 8.5H17.9678L17.6328 16.2217C17.61 16.7475 17.5912 17.1861 17.5469 17.543C17.5015 17.9087 17.4225 18.2506 17.2461 18.5723C16.9747 19.0671 16.5579 19.4671 16.0518 19.7168C15.7227 19.8791 15.3772 19.9422 15.0098 19.9717C14.6514 20.0004 14.2126 20 13.6865 20H10.3135C9.78735 20 9.34856 20.0004 8.99023 19.9717C8.62278 19.9422 8.27729 19.8791 7.94824 19.7168C7.44205 19.4671 7.02532 19.0671 6.75391 18.5723C6.57751 18.2506 6.49853 17.9087 6.45312 17.543C6.40883 17.1861 6.39005 16.7475 6.36719 16.2217L6.03223 8.5H5.5C5.08579 8.5 4.75 8.16421 4.75 7.75C4.75 7.33579 5.08579 7 5.5 7H8.25V6.25C8.25 5.00736 9.25736 4 10.5 4H13.5ZM7.86621 16.1562C7.89013 16.7063 7.90624 17.0751 7.94141 17.3584C7.97545 17.6326 8.02151 17.7644 8.06934 17.8516C8.19271 18.0763 8.38239 18.2577 8.6123 18.3711C8.70153 18.4151 8.83504 18.4545 9.11035 18.4766C9.39482 18.4994 9.76335 18.5 10.3135 18.5H13.6865C14.2367 18.5 14.6052 18.4994 14.8896 18.4766C15.165 18.4545 15.2985 18.4151 15.3877 18.3711C15.6176 18.2577 15.8073 18.0763 15.9307 17.8516C15.9785 17.7644 16.0245 17.6326 16.0586 17.3584C16.0938 17.0751 16.1099 16.7063 16.1338 16.1562L16.4668 8.5H7.5332L7.86621 16.1562ZM9.97656 10.75C10.3906 10.7371 10.7371 11.0626 10.75 11.4766L10.875 15.4766C10.8879 15.8906 10.5624 16.2371 10.1484 16.25C9.73443 16.2629 9.38794 15.9374 9.375 15.5234L9.25 11.5234C9.23706 11.1094 9.56255 10.7629 9.97656 10.75ZM14.0244 10.75C14.4384 10.7635 14.7635 11.1105 14.75 11.5244L14.6201 15.5244C14.6066 15.9384 14.2596 16.2634 13.8457 16.25C13.4317 16.2365 13.1067 15.8896 13.1201 15.4756L13.251 11.4756C13.2645 11.0617 13.6105 10.7366 14.0244 10.75ZM10.5 5.5C10.0858 5.5 9.75 5.83579 9.75 6.25V7H14.25V6.25C14.25 5.83579 13.9142 5.5 13.5 5.5H10.5Z",fill:"currentColor"})});var yy=({size:e=16})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsxs)("g",{clipPath:"url(#clip0_2_53)",children:[(0,G.jsx)("path",{d:"M16.25 16.25L7.75 7.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M7.75 16.25L16.25 7.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,G.jsx)("defs",{children:(0,G.jsx)("clipPath",{id:"clip0_2_53",children:(0,G.jsx)("rect",{width:"24",height:"24",fill:"white"})})})]}),vb=({size:e=24})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:(0,G.jsx)("path",{d:"M16.7198 6.21973C17.0127 5.92683 17.4874 5.92683 17.7803 6.21973C18.0732 6.51262 18.0732 6.9874 17.7803 7.28027L13.0606 12L17.7803 16.7197C18.0732 17.0126 18.0732 17.4874 17.7803 17.7803C17.4875 18.0731 17.0127 18.0731 16.7198 17.7803L12.0001 13.0605L7.28033 17.7803C6.98746 18.0731 6.51268 18.0731 6.21979 17.7803C5.92689 17.4874 5.92689 17.0126 6.21979 16.7197L10.9395 12L6.21979 7.28027C5.92689 6.98738 5.92689 6.51262 6.21979 6.21973C6.51268 5.92683 6.98744 5.92683 7.28033 6.21973L12.0001 10.9395L16.7198 6.21973Z",fill:"currentColor"})}),wb=({size:e=16})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",children:[(0,G.jsx)("path",{d:"M9.99999 12.7082C11.4958 12.7082 12.7083 11.4956 12.7083 9.99984C12.7083 8.50407 11.4958 7.2915 9.99999 7.2915C8.50422 7.2915 7.29166 8.50407 7.29166 9.99984C7.29166 11.4956 8.50422 12.7082 9.99999 12.7082Z",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M10 3.9585V5.05698",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M10 14.9429V16.0414",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M5.7269 5.72656L6.50682 6.50649",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M13.4932 13.4932L14.2731 14.2731",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M3.95834 10H5.05683",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M14.9432 10H16.0417",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M5.7269 14.2731L6.50682 13.4932",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,G.jsx)("path",{d:"M13.4932 6.50649L14.2731 5.72656",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"})]}),kb=({size:e=16})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",children:(0,G.jsx)("path",{d:"M15.5 10.4955C15.4037 11.5379 15.0124 12.5314 14.3721 13.3596C13.7317 14.1878 12.8688 14.8165 11.8841 15.1722C10.8995 15.5278 9.83397 15.5957 8.81217 15.3679C7.79038 15.1401 6.8546 14.6259 6.11434 13.8857C5.37408 13.1454 4.85995 12.2096 4.63211 11.1878C4.40427 10.166 4.47215 9.10048 4.82781 8.11585C5.18346 7.13123 5.81218 6.26825 6.64039 5.62791C7.4686 4.98756 8.46206 4.59634 9.5045 4.5C8.89418 5.32569 8.60049 6.34302 8.67685 7.36695C8.75321 8.39087 9.19454 9.35339 9.92058 10.0794C10.6466 10.8055 11.6091 11.2468 12.6331 11.3231C13.657 11.3995 14.6743 11.1058 15.5 10.4955Z",stroke:"currentColor",strokeWidth:"1.13793",strokeLinecap:"round",strokeLinejoin:"round"})}),Sb=({size:e=16})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,G.jsx)("path",{d:"M11.3799 6.9572L9.05645 4.63375M11.3799 6.9572L6.74949 11.5699C6.61925 11.6996 6.45577 11.791 6.277 11.8339L4.29549 12.3092C3.93194 12.3964 3.60478 12.0683 3.69297 11.705L4.16585 9.75693C4.20893 9.57947 4.29978 9.4172 4.42854 9.28771L9.05645 4.63375M11.3799 6.9572L12.3455 5.98759C12.9839 5.34655 12.9839 4.31002 12.3455 3.66897C11.7033 3.02415 10.6594 3.02415 10.0172 3.66897L9.06126 4.62892L9.05645 4.63375",stroke:"currentColor",strokeWidth:"0.9",strokeLinecap:"round",strokeLinejoin:"round"})}),Cb=({size:e=24})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,G.jsx)("path",{d:"M13.5 4C14.7426 4 15.75 5.00736 15.75 6.25V7H18.5C18.9142 7 19.25 7.33579 19.25 7.75C19.25 8.16421 18.9142 8.5 18.5 8.5H17.9678L17.6328 16.2217C17.61 16.7475 17.5912 17.1861 17.5469 17.543C17.5015 17.9087 17.4225 18.2506 17.2461 18.5723C16.9747 19.0671 16.5579 19.4671 16.0518 19.7168C15.7227 19.8791 15.3772 19.9422 15.0098 19.9717C14.6514 20.0004 14.2126 20 13.6865 20H10.3135C9.78735 20 9.34856 20.0004 8.99023 19.9717C8.62278 19.9422 8.27729 19.8791 7.94824 19.7168C7.44205 19.4671 7.02532 19.0671 6.75391 18.5723C6.57751 18.2506 6.49853 17.9087 6.45312 17.543C6.40883 17.1861 6.39005 16.7475 6.36719 16.2217L6.03223 8.5H5.5C5.08579 8.5 4.75 8.16421 4.75 7.75C4.75 7.33579 5.08579 7 5.5 7H8.25V6.25C8.25 5.00736 9.25736 4 10.5 4H13.5ZM7.86621 16.1562C7.89013 16.7063 7.90624 17.0751 7.94141 17.3584C7.97545 17.6326 8.02151 17.7644 8.06934 17.8516C8.19271 18.0763 8.38239 18.2577 8.6123 18.3711C8.70153 18.4151 8.83504 18.4545 9.11035 18.4766C9.39482 18.4994 9.76335 18.5 10.3135 18.5H13.6865C14.2367 18.5 14.6052 18.4994 14.8896 18.4766C15.165 18.4545 15.2985 18.4151 15.3877 18.3711C15.6176 18.2577 15.8073 18.0763 15.9307 17.8516C15.9785 17.7644 16.0245 17.6326 16.0586 17.3584C16.0938 17.0751 16.1099 16.7063 16.1338 16.1562L16.4668 8.5H7.5332L7.86621 16.1562ZM9.97656 10.75C10.3906 10.7371 10.7371 11.0626 10.75 11.4766L10.875 15.4766C10.8879 15.8906 10.5624 16.2371 10.1484 16.25C9.73443 16.2629 9.38794 15.9374 9.375 15.5234L9.25 11.5234C9.23706 11.1094 9.56255 10.7629 9.97656 10.75ZM14.0244 10.75C14.4383 10.7635 14.7635 11.1105 14.75 11.5244L14.6201 15.5244C14.6066 15.9384 14.2596 16.2634 13.8457 16.25C13.4317 16.2365 13.1067 15.8896 13.1201 15.4756L13.251 11.4756C13.2645 11.0617 13.6105 10.7366 14.0244 10.75ZM10.5 5.5C10.0858 5.5 9.75 5.83579 9.75 6.25V7H14.25V6.25C14.25 5.83579 13.9142 5.5 13.5 5.5H10.5Z",fill:"currentColor"})}),Mb=({size:e=16})=>(0,G.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,G.jsx)("path",{d:"M8.5 3.5L4 8L8.5 12.5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})});var Eb=({size:e=24})=>(0,G.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,G.jsx)("rect",{x:"3",y:"3",width:"18",height:"18",rx:"2",stroke:"currentColor",strokeWidth:"1.5"}),(0,G.jsx)("line",{x1:"3",y1:"9",x2:"21",y2:"9",stroke:"currentColor",strokeWidth:"1.5"}),(0,G.jsx)("line",{x1:"9",y1:"9",x2:"9",y2:"21",stroke:"currentColor",strokeWidth:"1.5"})]}),py=["data-feedback-toolbar","data-annotation-popup","data-annotation-marker"],ef=py.flatMap(e=>[`:not([${e}])`,`:not([${e}] *)`]).join(""),ff="feedback-freeze-styles",tf="__agentation_freeze";function Tb(){if(typeof window>"u")return{frozen:!1,installed:!0,origSetTimeout:setTimeout,origSetInterval:setInterval,origRAF:t=>0,pausedAnimations:[],frozenTimeoutQueue:[],frozenRAFQueue:[]};let e=window;return e[tf]||(e[tf]={frozen:!1,installed:!1,origSetTimeout:null,origSetInterval:null,origRAF:null,pausedAnimations:[],frozenTimeoutQueue:[],frozenRAFQueue:[]}),e[tf]}var He=Tb();typeof window<"u"&&!He.installed&&(He.origSetTimeout=window.setTimeout.bind(window),He.origSetInterval=window.setInterval.bind(window),He.origRAF=window.requestAnimationFrame.bind(window),window.setTimeout=(e,t,...n)=>typeof e=="string"?He.origSetTimeout(e,t):He.origSetTimeout((...l)=>{He.frozen?He.frozenTimeoutQueue.push(()=>e(...l)):e(...l)},t,...n),window.setInterval=(e,t,...n)=>typeof e=="string"?He.origSetInterval(e,t):He.origSetInterval((...l)=>{He.frozen||e(...l)},t,...n),window.requestAnimationFrame=e=>He.origRAF(t=>{He.frozen?He.frozenRAFQueue.push(e):e(t)}),He.installed=!0);var fe=He.origSetTimeout,Db=He.origSetInterval,wi=He.origRAF;function Nb(e){return e?py.some(t=>!!e.closest?.(`[${t}]`)):!1}function zb(){if(typeof document>"u"||He.frozen)return;He.frozen=!0,He.frozenTimeoutQueue=[],He.frozenRAFQueue=[];let e=document.getElementById(ff);e||(e=document.createElement("style"),e.id=ff),e.textContent=`
    *${ef},
    *${ef}::before,
    *${ef}::after {
      animation-play-state: paused !important;
      transition: none !important;
    }
  `,document.head.appendChild(e),He.pausedAnimations=[];try{document.getAnimations().forEach(t=>{if(t.playState!=="running")return;let n=t.effect?.target;Nb(n)||(t.pause(),He.pausedAnimations.push(t))})}catch{}document.querySelectorAll("video").forEach(t=>{t.paused||(t.dataset.wasPaused="false",t.pause())})}function Qg(){if(typeof document>"u"||!He.frozen)return;He.frozen=!1;let e=He.frozenTimeoutQueue;He.frozenTimeoutQueue=[];for(let n of e)He.origSetTimeout(()=>{if(He.frozen){He.frozenTimeoutQueue.push(n);return}try{n()}catch(l){console.warn("[agentation] Error replaying queued timeout:",l)}},0);let t=He.frozenRAFQueue;He.frozenRAFQueue=[];for(let n of t)He.origRAF(l=>{if(He.frozen){He.frozenRAFQueue.push(n);return}n(l)});for(let n of He.pausedAnimations)try{n.play()}catch(l){console.warn("[agentation] Error resuming animation:",l)}He.pausedAnimations=[],document.getElementById(ff)?.remove(),document.querySelectorAll("video").forEach(n=>{n.dataset.wasPaused==="false"&&(n.play().catch(()=>{}),delete n.dataset.wasPaused)})}function nf(e){if(!e)return;let t=n=>n.stopImmediatePropagation();document.addEventListener("focusin",t,!0),document.addEventListener("focusout",t,!0);try{e.focus()}finally{document.removeEventListener("focusin",t,!0),document.removeEventListener("focusout",t,!0)}}var Kc=(0,Lt.forwardRef)(function({element:t,timestamp:n,selectedText:l,placeholder:o="What should change?",initialValue:a="",submitLabel:i="Add",onSubmit:s,onCancel:r,onDelete:p,style:f,accentColor:b="#3c82f7",isExiting:_=!1,lightMode:w=!1,computedStyles:C},z){let[D,h]=(0,Lt.useState)(a),[y,k]=(0,Lt.useState)(!1),[E,Q]=(0,Lt.useState)("initial"),[oe,L]=(0,Lt.useState)(!1),[K,ee]=(0,Lt.useState)(!1),F=(0,Lt.useRef)(null),he=(0,Lt.useRef)(null),et=(0,Lt.useRef)(null),ft=(0,Lt.useRef)(null);(0,Lt.useEffect)(()=>{_&&E!=="exit"&&Q("exit")},[_,E]),(0,Lt.useEffect)(()=>{fe(()=>{Q("enter")},0);let ge=fe(()=>{Q("entered")},200),Ze=fe(()=>{let Bt=F.current;Bt&&(nf(Bt),Bt.selectionStart=Bt.selectionEnd=Bt.value.length,Bt.scrollTop=Bt.scrollHeight)},50);return()=>{clearTimeout(ge),clearTimeout(Ze),et.current&&clearTimeout(et.current),ft.current&&clearTimeout(ft.current)}},[]);let Re=(0,Lt.useCallback)(()=>{ft.current&&clearTimeout(ft.current),k(!0),ft.current=fe(()=>{k(!1),nf(F.current)},250)},[]);(0,Lt.useImperativeHandle)(z,()=>({shake:Re}),[Re]);let Ie=(0,Lt.useCallback)(()=>{Q("exit"),et.current=fe(()=>{r()},150)},[r]),Ee=(0,Lt.useCallback)(()=>{D.trim()&&s(D.trim())},[D,s]),Pe=(0,Lt.useCallback)(ge=>{ge.stopPropagation(),!ge.nativeEvent.isComposing&&(ge.key==="Enter"&&!ge.shiftKey&&(ge.preventDefault(),Ee()),ge.key==="Escape"&&Ie())},[Ee,Ie]),W=[bt.popup,w?bt.light:"",E==="enter"?bt.enter:"",E==="entered"?bt.entered:"",E==="exit"?bt.exit:"",y?bt.shake:""].filter(Boolean).join(" ");return(0,Nt.jsxs)("div",{ref:he,className:W,"data-annotation-popup":!0,style:f,onClick:ge=>ge.stopPropagation(),children:[(0,Nt.jsxs)("div",{className:bt.header,children:[C&&Object.keys(C).length>0?(0,Nt.jsxs)("button",{className:bt.headerToggle,onClick:()=>{let ge=K;ee(!K),ge&&fe(()=>nf(F.current),0)},type:"button",children:[(0,Nt.jsx)("svg",{className:`${bt.chevron} ${K?bt.expanded:""}`,width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,Nt.jsx)("path",{d:"M5.5 10.25L9 7.25L5.75 4",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})}),(0,Nt.jsx)("span",{className:bt.element,children:t})]}):(0,Nt.jsx)("span",{className:bt.element,children:t}),n&&(0,Nt.jsx)("span",{className:bt.timestamp,children:n})]}),C&&Object.keys(C).length>0&&(0,Nt.jsx)("div",{className:`${bt.stylesWrapper} ${K?bt.expanded:""}`,children:(0,Nt.jsx)("div",{className:bt.stylesInner,children:(0,Nt.jsx)("div",{className:bt.stylesBlock,children:Object.entries(C).map(([ge,Ze])=>(0,Nt.jsxs)("div",{className:bt.styleLine,children:[(0,Nt.jsx)("span",{className:bt.styleProperty,children:ge.replace(/([A-Z])/g,"-$1").toLowerCase()}),": ",(0,Nt.jsx)("span",{className:bt.styleValue,children:Ze}),";"]},ge))})})}),l&&(0,Nt.jsxs)("div",{className:bt.quote,children:["\u201C",l.slice(0,80),l.length>80?"...":"","\u201D"]}),(0,Nt.jsx)("textarea",{ref:F,className:bt.textarea,style:{borderColor:oe?b:void 0},placeholder:o,value:D,onChange:ge=>h(ge.target.value),onFocus:()=>L(!0),onBlur:()=>L(!1),rows:2,onKeyDown:Pe}),(0,Nt.jsxs)("div",{className:bt.actions,children:[p&&(0,Nt.jsx)("div",{className:bt.deleteWrapper,children:(0,Nt.jsx)("button",{className:bt.deleteButton,onClick:p,type:"button",children:(0,Nt.jsx)(Cb,{size:22})})}),(0,Nt.jsx)("button",{className:bt.cancel,onClick:Ie,children:"Cancel"}),(0,Nt.jsx)("button",{className:bt.submit,style:{backgroundColor:b,opacity:D.trim()?1:.4},onClick:Ee,disabled:!D.trim(),children:i})]})]})}),Ab=({content:e,children:t,...n})=>{let[l,o]=(0,Ll.useState)(!1),[a,i]=(0,Ll.useState)(!1),[s,r]=(0,Ll.useState)({top:0,right:0}),p=(0,Ll.useRef)(null),f=(0,Ll.useRef)(null),b=(0,Ll.useRef)(null),_=()=>{if(p.current){let z=p.current.getBoundingClientRect();r({top:z.top+z.height/2,right:window.innerWidth-z.left+8})}},w=()=>{i(!0),b.current&&(clearTimeout(b.current),b.current=null),_(),f.current=fe(()=>{o(!0)},500)},C=()=>{f.current&&(clearTimeout(f.current),f.current=null),o(!1),b.current=fe(()=>{i(!1)},150)};return(0,Ll.useEffect)(()=>()=>{f.current&&clearTimeout(f.current),b.current&&clearTimeout(b.current)},[]),(0,ya.jsxs)(ya.Fragment,{children:[(0,ya.jsx)("span",{ref:p,onMouseEnter:w,onMouseLeave:C,...n,children:t}),a&&(0,by.createPortal)((0,ya.jsx)("div",{"data-feedback-toolbar":!0,style:{position:"fixed",top:s.top,right:s.right,transform:"translateY(-50%)",padding:"6px 10px",background:"#383838",color:"rgba(255, 255, 255, 0.7)",fontSize:"11px",fontWeight:400,lineHeight:"14px",borderRadius:"10px",width:"180px",textAlign:"left",zIndex:100020,pointerEvents:"none",boxShadow:"0px 1px 8px rgba(0, 0, 0, 0.28)",opacity:l?1:0,transition:"opacity 0.15s ease"},children:e}),document.body)]})},Lb=`.styles-module__tooltip___mcXL2 {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: help;
}

.styles-module__tooltipIcon___Nq2nD {
  transform: translateY(0.5px);
  color: #fff;
  opacity: 0.2;
  transition: opacity 0.15s ease;
  will-change: transform;
}
.styles-module__tooltip___mcXL2:hover .styles-module__tooltipIcon___Nq2nD {
  opacity: 0.5;
}
[data-agentation-theme=light] .styles-module__tooltipIcon___Nq2nD {
  color: #000;
}`,Rb={tooltip:"styles-module__tooltip___mcXL2",tooltipIcon:"styles-module__tooltipIcon___Nq2nD"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-help-tooltip-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-help-tooltip-styles",document.head.appendChild(e)),e.textContent=Lb}var Wg=Rb,ga=({content:e})=>(0,hf.jsx)(Ab,{className:Wg.tooltip,content:e,children:(0,hf.jsx)(hb,{className:Wg.tooltipIcon})}),P={navigation:{width:800,height:56},hero:{width:800,height:320},header:{width:800,height:80},section:{width:800,height:400},sidebar:{width:240,height:400},footer:{width:800,height:160},modal:{width:480,height:300},card:{width:280,height:240},text:{width:400,height:120},image:{width:320,height:200},video:{width:480,height:270},table:{width:560,height:220},grid:{width:600,height:300},list:{width:300,height:180},chart:{width:400,height:240},button:{width:140,height:40},input:{width:280,height:56},form:{width:360,height:320},tabs:{width:480,height:240},dropdown:{width:200,height:200},toggle:{width:44,height:24},search:{width:320,height:44},avatar:{width:48,height:48},badge:{width:80,height:28},breadcrumb:{width:300,height:24},pagination:{width:300,height:36},progress:{width:240,height:8},divider:{width:600,height:1},accordion:{width:400,height:200},carousel:{width:600,height:300},toast:{width:320,height:64},tooltip:{width:180,height:40},pricing:{width:300,height:360},testimonial:{width:360,height:200},cta:{width:600,height:160},alert:{width:400,height:56},banner:{width:800,height:48},stat:{width:200,height:120},stepper:{width:480,height:48},tag:{width:72,height:28},rating:{width:160,height:28},map:{width:480,height:300},timeline:{width:360,height:320},fileUpload:{width:360,height:180},codeBlock:{width:480,height:200},calendar:{width:300,height:300},notification:{width:360,height:72},productCard:{width:280,height:360},profile:{width:280,height:200},drawer:{width:320,height:400},popover:{width:240,height:160},logo:{width:120,height:40},faq:{width:560,height:320},gallery:{width:560,height:360},checkbox:{width:20,height:20},radio:{width:20,height:20},slider:{width:240,height:32},datePicker:{width:300,height:320},skeleton:{width:320,height:120},chip:{width:96,height:32},icon:{width:24,height:24},spinner:{width:32,height:32},feature:{width:360,height:200},team:{width:560,height:280},login:{width:360,height:360},contact:{width:400,height:320}},xy=[{section:"Layout",items:[{type:"navigation",label:"Navigation",...P.navigation},{type:"header",label:"Header",...P.header},{type:"hero",label:"Hero",...P.hero},{type:"section",label:"Section",...P.section},{type:"sidebar",label:"Sidebar",...P.sidebar},{type:"footer",label:"Footer",...P.footer},{type:"modal",label:"Modal",...P.modal},{type:"banner",label:"Banner",...P.banner},{type:"drawer",label:"Drawer",...P.drawer},{type:"popover",label:"Popover",...P.popover},{type:"divider",label:"Divider",...P.divider}]},{section:"Content",items:[{type:"card",label:"Card",...P.card},{type:"text",label:"Text",...P.text},{type:"image",label:"Image",...P.image},{type:"video",label:"Video",...P.video},{type:"table",label:"Table",...P.table},{type:"grid",label:"Grid",...P.grid},{type:"list",label:"List",...P.list},{type:"chart",label:"Chart",...P.chart},{type:"codeBlock",label:"Code Block",...P.codeBlock},{type:"map",label:"Map",...P.map},{type:"timeline",label:"Timeline",...P.timeline},{type:"calendar",label:"Calendar",...P.calendar},{type:"accordion",label:"Accordion",...P.accordion},{type:"carousel",label:"Carousel",...P.carousel},{type:"logo",label:"Logo",...P.logo},{type:"faq",label:"FAQ",...P.faq},{type:"gallery",label:"Gallery",...P.gallery}]},{section:"Controls",items:[{type:"button",label:"Button",...P.button},{type:"input",label:"Input",...P.input},{type:"search",label:"Search",...P.search},{type:"form",label:"Form",...P.form},{type:"tabs",label:"Tabs",...P.tabs},{type:"dropdown",label:"Dropdown",...P.dropdown},{type:"toggle",label:"Toggle",...P.toggle},{type:"stepper",label:"Stepper",...P.stepper},{type:"rating",label:"Rating",...P.rating},{type:"fileUpload",label:"File Upload",...P.fileUpload},{type:"checkbox",label:"Checkbox",...P.checkbox},{type:"radio",label:"Radio",...P.radio},{type:"slider",label:"Slider",...P.slider},{type:"datePicker",label:"Date Picker",...P.datePicker}]},{section:"Elements",items:[{type:"avatar",label:"Avatar",...P.avatar},{type:"badge",label:"Badge",...P.badge},{type:"tag",label:"Tag",...P.tag},{type:"breadcrumb",label:"Breadcrumb",...P.breadcrumb},{type:"pagination",label:"Pagination",...P.pagination},{type:"progress",label:"Progress",...P.progress},{type:"alert",label:"Alert",...P.alert},{type:"toast",label:"Toast",...P.toast},{type:"notification",label:"Notification",...P.notification},{type:"tooltip",label:"Tooltip",...P.tooltip},{type:"stat",label:"Stat",...P.stat},{type:"skeleton",label:"Skeleton",...P.skeleton},{type:"chip",label:"Chip",...P.chip},{type:"icon",label:"Icon",...P.icon},{type:"spinner",label:"Spinner",...P.spinner}]},{section:"Blocks",items:[{type:"pricing",label:"Pricing",...P.pricing},{type:"testimonial",label:"Testimonial",...P.testimonial},{type:"cta",label:"CTA",...P.cta},{type:"productCard",label:"Product Card",...P.productCard},{type:"profile",label:"Profile",...P.profile},{type:"feature",label:"Feature",...P.feature},{type:"team",label:"Team",...P.team},{type:"login",label:"Login",...P.login},{type:"contact",label:"Contact",...P.contact}]}],gl={};for(let e of xy)for(let t of e.items)gl[t.type]=t;function H({w:e,h:t=3,strong:n}){return(0,u.jsx)("div",{style:{width:typeof e=="number"?`${e}px`:e,height:t,borderRadius:2,background:n?"var(--agd-bar-strong)":"var(--agd-bar)",flexShrink:0}})}function _t({w:e,h:t,radius:n=3,style:l}){return(0,u.jsx)("div",{style:{width:typeof e=="number"?`${e}px`:e,height:typeof t=="number"?`${t}px`:t,borderRadius:n,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",flexShrink:0,...l}})}function xn({size:e}){return(0,u.jsx)("div",{style:{width:e,height:e,borderRadius:"50%",border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",flexShrink:0}})}function Bb({width:e,height:t}){let n=Math.max(8,t*.2);return(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",height:"100%",padding:`0 ${n}px`,gap:e*.02},children:[(0,u.jsx)(_t,{w:Math.max(20,t*.5),h:Math.max(12,t*.4),radius:2}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",gap:e*.03,marginLeft:e*.04},children:[(0,u.jsx)(H,{w:e*.06}),(0,u.jsx)(H,{w:e*.07}),(0,u.jsx)(H,{w:e*.05}),(0,u.jsx)(H,{w:e*.06})]}),(0,u.jsx)(_t,{w:e*.1,h:Math.min(28,t*.5),radius:4})]})}function Ob({width:e,height:t,text:n}){return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"100%",gap:t*.05},children:[n?(0,u.jsx)("span",{style:{fontSize:Math.min(20,t*.08),fontWeight:600,color:"var(--agd-text-3)",textAlign:"center",maxWidth:"80%"},children:n}):(0,u.jsx)(H,{w:e*.5,h:Math.max(6,t*.04),strong:!0}),(0,u.jsx)(H,{w:e*.6}),(0,u.jsx)(H,{w:e*.4}),(0,u.jsx)(_t,{w:Math.min(140,e*.2),h:Math.min(36,t*.12),radius:6,style:{marginTop:t*.06}})]})}function $b({width:e,height:t}){let n=Math.max(3,Math.floor(t/36));return(0,u.jsxs)("div",{style:{padding:e*.08,display:"flex",flexDirection:"column",gap:t*.03},children:[(0,u.jsx)(H,{w:e*.6,h:4,strong:!0}),Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:6},children:[(0,u.jsx)(_t,{w:10,h:10,radius:2}),(0,u.jsx)(H,{w:e*(.4+o*17%30/100)})]},o))]})}function Hb({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/160)));return(0,u.jsx)("div",{style:{display:"flex",padding:`${t*.12}px ${e*.03}px`,gap:e*.05},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsx)(H,{w:"60%",h:3,strong:!0}),(0,u.jsx)(H,{w:"80%",h:2}),(0,u.jsx)(H,{w:"70%",h:2}),(0,u.jsx)(H,{w:"60%",h:2})]},o))})}function Ub({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsxs)("div",{style:{padding:"10px 12px",borderBottom:"1px solid var(--agd-stroke)",display:"flex",alignItems:"center",justifyContent:"space-between"},children:[(0,u.jsx)(H,{w:e*.3,h:4,strong:!0}),(0,u.jsx)("div",{style:{width:14,height:14,border:"1px solid var(--agd-stroke)",borderRadius:3}})]}),(0,u.jsxs)("div",{style:{flex:1,padding:12,display:"flex",flexDirection:"column",gap:6},children:[(0,u.jsx)(H,{w:"90%"}),(0,u.jsx)(H,{w:"70%"}),(0,u.jsx)(H,{w:"80%"})]}),(0,u.jsxs)("div",{style:{padding:"10px 12px",borderTop:"1px solid var(--agd-stroke)",display:"flex",justifyContent:"flex-end",gap:8},children:[(0,u.jsx)(_t,{w:70,h:26,radius:4}),(0,u.jsx)(_t,{w:70,h:26,radius:4,style:{background:"var(--agd-bar)"}})]})]})}function Yb({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsx)("div",{style:{height:"40%",background:"var(--agd-fill)",borderBottom:"1px dashed var(--agd-stroke)"}}),(0,u.jsxs)("div",{style:{flex:1,padding:10,display:"flex",flexDirection:"column",gap:5},children:[(0,u.jsx)(H,{w:"70%",h:4,strong:!0}),(0,u.jsx)(H,{w:"95%",h:2}),(0,u.jsx)(H,{w:"85%",h:2}),(0,u.jsx)(H,{w:"50%",h:2})]})]})}function jb({width:e,height:t,text:n}){if(n)return(0,u.jsx)("div",{style:{padding:4,fontSize:Math.min(14,t*.3),lineHeight:1.5,color:"var(--agd-text-3)",wordBreak:"break-word",overflow:"hidden"},children:n});let l=Math.max(2,Math.floor(t/18));return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:6,padding:4},children:[(0,u.jsx)(H,{w:e*.6,h:5,strong:!0}),Array.from({length:l},(o,a)=>(0,u.jsx)(H,{w:`${70+a*13%25}%`,h:2},a))]})}function Xb({width:e,height:t}){return(0,u.jsx)("div",{style:{height:"100%",position:"relative"},children:(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,preserveAspectRatio:"none",fill:"none",children:[(0,u.jsx)("line",{x1:"0",y1:"0",x2:e,y2:t,stroke:"var(--agd-stroke)",strokeWidth:"1"}),(0,u.jsx)("line",{x1:e,y1:"0",x2:"0",y2:t,stroke:"var(--agd-stroke)",strokeWidth:"1"}),(0,u.jsx)("circle",{cx:e*.3,cy:t*.3,r:Math.min(e,t)*.08,fill:"var(--agd-fill)",stroke:"var(--agd-stroke)",strokeWidth:"0.8"})]})})}function Ib({width:e,height:t}){let n=Math.max(2,Math.min(5,Math.floor(e/100))),l=Math.max(2,Math.min(6,Math.floor(t/32)));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsx)("div",{style:{display:"flex",borderBottom:"1px solid var(--agd-stroke)",padding:"6px 0"},children:Array.from({length:n},(o,a)=>(0,u.jsx)("div",{style:{flex:1,padding:"0 8px"},children:(0,u.jsx)(H,{w:"70%",h:3,strong:!0})},a))}),Array.from({length:l},(o,a)=>(0,u.jsx)("div",{style:{display:"flex",borderBottom:"1px solid rgba(255,255,255,0.03)",padding:"6px 0"},children:Array.from({length:n},(i,s)=>(0,u.jsx)("div",{style:{flex:1,padding:"0 8px"},children:(0,u.jsx)(H,{w:`${50+(a*7+s*13)%40}%`,h:2})},s))},a))]})}function qb({width:e,height:t}){let n=Math.max(2,Math.floor(t/28));return(0,u.jsx)("div",{style:{display:"flex",flexDirection:"column",gap:4,padding:4},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:8,padding:"4px 0"},children:[(0,u.jsx)(xn,{size:8}),(0,u.jsx)(H,{w:`${55+o*17%35}%`,h:2})]},o))})}function Qb({width:e,height:t,text:n}){return(0,u.jsx)("div",{style:{height:"100%",borderRadius:Math.min(8,t/3),border:"1px solid var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center"},children:n?(0,u.jsx)("span",{style:{fontSize:Math.min(13,t*.4),fontWeight:500,color:"var(--agd-text-3)",letterSpacing:"-0.01em"},children:n}):(0,u.jsx)(H,{w:Math.max(20,e*.5),h:3,strong:!0})})}function Wb({width:e,height:t}){return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:4,height:"100%",justifyContent:"center"},children:[(0,u.jsx)(H,{w:Math.min(80,e*.3),h:2}),(0,u.jsx)("div",{style:{height:Math.min(36,t*.6),borderRadius:4,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",paddingLeft:8},children:(0,u.jsx)(H,{w:"40%",h:2})})]})}function Gb({width:e,height:t}){let n=Math.max(2,Math.min(5,Math.floor(t/56)));return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:t*.04,padding:8},children:[Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsx)(H,{w:60+o*17%30,h:2}),(0,u.jsx)(_t,{w:"100%",h:28,radius:4})]},o)),(0,u.jsx)(_t,{w:Math.min(120,e*.35),h:30,radius:6,style:{marginTop:8,alignSelf:"flex-end",background:"var(--agd-bar)"}})]})}function Vb({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/120)));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsx)("div",{style:{display:"flex",gap:2,borderBottom:"1px solid var(--agd-stroke)"},children:Array.from({length:n},(l,o)=>(0,u.jsx)("div",{style:{padding:"8px 12px",borderBottom:o===0?"2px solid var(--agd-bar-strong)":"none"},children:(0,u.jsx)(H,{w:60,h:3,strong:o===0})},o))}),(0,u.jsxs)("div",{style:{flex:1,padding:12,display:"flex",flexDirection:"column",gap:6},children:[(0,u.jsx)(H,{w:"80%",h:2}),(0,u.jsx)(H,{w:"65%",h:2}),(0,u.jsx)(H,{w:"75%",h:2})]})]})}function Zb({width:e,height:t}){let n=Math.min(e,t)/2;return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("circle",{cx:e/2,cy:t/2,r:n-1,stroke:"var(--agd-stroke)",fill:"var(--agd-fill)",strokeWidth:"1.5",strokeDasharray:"3 2"}),(0,u.jsx)("circle",{cx:e/2,cy:t*.38,r:n*.28,stroke:"var(--agd-stroke)",fill:"var(--agd-fill)",strokeWidth:"0.8"}),(0,u.jsx)("path",{d:`M${e/2-n*.55} ${t*.78} C${e/2-n*.55} ${t*.55} ${e/2+n*.55} ${t*.55} ${e/2+n*.55} ${t*.78}`,stroke:"var(--agd-stroke)",fill:"var(--agd-fill)",strokeWidth:"0.8"})]})}function Kb({width:e,height:t}){return(0,u.jsx)("div",{style:{height:"100%",borderRadius:t/2,border:"1px solid var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)(H,{w:Math.max(16,e*.5),h:2,strong:!0})})}function Fb({width:e,height:t}){return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"100%",gap:t*.08},children:[(0,u.jsx)(H,{w:e*.5,h:Math.max(5,t*.06),strong:!0}),(0,u.jsx)(H,{w:e*.35})]})}function Jb({width:e,height:t}){return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",height:"100%",gap:t*.04,padding:e*.04},children:[(0,u.jsx)(H,{w:e*.3,h:4,strong:!0}),(0,u.jsx)(H,{w:e*.7}),(0,u.jsx)(H,{w:e*.5}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",gap:e*.03,marginTop:t*.06},children:[(0,u.jsx)(_t,{w:"33%",h:"100%",radius:4}),(0,u.jsx)(_t,{w:"33%",h:"100%",radius:4}),(0,u.jsx)(_t,{w:"33%",h:"100%",radius:4})]})]})}function Pb({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/140))),l=Math.max(1,Math.min(3,Math.floor(t/120)));return(0,u.jsx)("div",{style:{display:"grid",gridTemplateColumns:`repeat(${n}, 1fr)`,gridTemplateRows:`repeat(${l}, 1fr)`,gap:6,height:"100%"},children:Array.from({length:n*l},(o,a)=>(0,u.jsx)(_t,{w:"100%",h:"100%",radius:4},a))})}function ex({width:e,height:t}){let n=Math.max(2,Math.floor((t-32)/28));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsx)("div",{style:{padding:"6px 8px",borderBottom:"1px solid var(--agd-stroke)"},children:(0,u.jsx)(H,{w:e*.5,h:3,strong:!0})}),(0,u.jsx)("div",{style:{flex:1,padding:4,display:"flex",flexDirection:"column",gap:2},children:Array.from({length:n},(l,o)=>(0,u.jsx)("div",{style:{padding:"4px 6px",borderRadius:3,background:o===0?"var(--agd-fill)":"transparent"},children:(0,u.jsx)(H,{w:`${50+o*17%35}%`,h:2,strong:o===0})},o))})]})}function tx({width:e,height:t}){let n=Math.min(e,t)/2;return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("rect",{x:"1",y:"1",width:e-2,height:t-2,rx:n,stroke:"var(--agd-stroke)",strokeWidth:"1"}),(0,u.jsx)("circle",{cx:e-n,cy:t/2,r:n*.7,fill:"var(--agd-bar)"})]})}function nx({width:e,height:t}){let n=Math.min(t/2,20);return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:n,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:`0 ${n*.6}px`,gap:6},children:[(0,u.jsx)(xn,{size:Math.min(14,t*.4)}),(0,u.jsx)(H,{w:"50%",h:2})]})}function lx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:8,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:"0 10px",gap:8},children:[(0,u.jsx)(xn,{size:Math.min(20,t*.5)}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:"60%",h:3,strong:!0}),(0,u.jsx)(H,{w:"80%",h:2})]}),(0,u.jsx)("div",{style:{width:14,height:14,border:"1px solid var(--agd-stroke)",borderRadius:3,flexShrink:0}})]})}function ox({width:e,height:t}){return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("rect",{x:"0",y:"0",width:e,height:t,rx:t/2,stroke:"var(--agd-stroke)",strokeWidth:"0.8"}),(0,u.jsx)("rect",{x:"1",y:"1",width:e*.65,height:t-2,rx:(t-2)/2,fill:"var(--agd-bar)"})]})}function ax({width:e,height:t}){let n=Math.max(3,Math.min(7,Math.floor(e/50))),l=e/(n*2);return(0,u.jsx)("div",{style:{height:"100%",display:"flex",alignItems:"flex-end",justifyContent:"space-around",padding:"0 4px",borderBottom:"1px solid var(--agd-stroke)"},children:Array.from({length:n},(o,a)=>{let i=30+(a*37+17)%55;return(0,u.jsx)(_t,{w:l,h:`${i}%`,radius:2},a)})})}function ix({width:e,height:t}){let n=Math.min(e,t)*.12;return(0,u.jsxs)("div",{style:{height:"100%",position:"relative",display:"flex",alignItems:"center",justifyContent:"center"},children:[(0,u.jsx)(_t,{w:"100%",h:"100%",radius:4}),(0,u.jsx)("div",{style:{position:"absolute",width:n*2,height:n*2,borderRadius:"50%",border:"1.5px solid var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)("div",{style:{width:0,height:0,borderLeft:`${n*.6}px solid var(--agd-bar-strong)`,borderTop:`${n*.4}px solid transparent`,borderBottom:`${n*.4}px solid transparent`,marginLeft:n*.15}})})]})}function sx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center"},children:[(0,u.jsx)("div",{style:{flex:1,width:"100%",borderRadius:6,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)(H,{w:"60%",h:2})}),(0,u.jsx)("div",{style:{width:8,height:8,background:"var(--agd-fill)",border:"1px dashed var(--agd-stroke)",borderTop:"none",borderLeft:"none",transform:"rotate(45deg)",marginTop:-5}})]})}function rx({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/80)));return(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",height:"100%",gap:4},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:4},children:[o>0&&(0,u.jsx)("span",{style:{color:"var(--agd-stroke)",fontSize:10},children:"/"}),(0,u.jsx)(H,{w:40+o*13%20,h:2,strong:o===n-1})]},o))})}function cx({width:e,height:t}){let n=Math.max(3,Math.min(5,Math.floor(e/40))),l=Math.min(28,t*.8);return(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",gap:4},children:Array.from({length:n},(o,a)=>(0,u.jsx)(_t,{w:l,h:l,radius:4,style:a===1?{background:"var(--agd-bar)"}:void 0},a))})}function ux({width:e}){return(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",height:"100%"},children:(0,u.jsx)("div",{style:{width:"100%",height:1,background:"var(--agd-stroke)"}})})}function dx({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(t/40)));return(0,u.jsx)("div",{style:{display:"flex",flexDirection:"column",height:"100%"},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{borderBottom:"1px solid var(--agd-stroke)",padding:"8px 6px",display:"flex",alignItems:"center",justifyContent:"space-between",flex:o===0?2:1},children:[(0,u.jsx)(H,{w:`${40+o*17%25}%`,h:3,strong:!0}),(0,u.jsx)("span",{style:{fontSize:8,color:"var(--agd-stroke)"},children:o===0?"\u25BC":"\u25B6"})]},o))})}function _x({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",gap:6},children:[(0,u.jsxs)("div",{style:{flex:1,display:"flex",gap:6,alignItems:"center"},children:[(0,u.jsx)("span",{style:{fontSize:12,color:"var(--agd-stroke)"},children:"\u2039"}),(0,u.jsx)(_t,{w:"100%",h:"100%",radius:4}),(0,u.jsx)("span",{style:{fontSize:12,color:"var(--agd-stroke)"},children:"\u203A"})]}),(0,u.jsxs)("div",{style:{display:"flex",justifyContent:"center",gap:4},children:[(0,u.jsx)(xn,{size:5}),(0,u.jsx)(xn,{size:5}),(0,u.jsx)(xn,{size:5})]})]})}function fx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center",padding:10,gap:t*.04},children:[(0,u.jsx)(H,{w:e*.4,h:3,strong:!0}),(0,u.jsx)(H,{w:e*.3,h:6,strong:!0}),(0,u.jsx)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:4,width:"100%",padding:"8px 0"},children:Array.from({length:4},(n,l)=>(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:4},children:[(0,u.jsx)(xn,{size:5}),(0,u.jsx)(H,{w:`${50+l*17%35}%`,h:2})]},l))}),(0,u.jsx)(_t,{w:e*.7,h:Math.min(32,t*.1),radius:6,style:{background:"var(--agd-bar)"}})]})}function hx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",padding:10,gap:8},children:[(0,u.jsx)("span",{style:{fontSize:18,lineHeight:1,color:"var(--agd-stroke)",fontFamily:"serif"},children:"\u201C"}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsx)(H,{w:"90%",h:2}),(0,u.jsx)(H,{w:"75%",h:2}),(0,u.jsx)(H,{w:"60%",h:2})]}),(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:6},children:[(0,u.jsx)(xn,{size:20}),(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:2},children:[(0,u.jsx)(H,{w:60,h:3,strong:!0}),(0,u.jsx)(H,{w:40,h:2})]})]})]})}function mx({width:e,height:t}){return(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",height:"100%",gap:t*.08},children:[(0,u.jsx)(H,{w:e*.5,h:Math.max(4,t*.05),strong:!0}),(0,u.jsx)(H,{w:e*.35}),(0,u.jsx)(_t,{w:Math.min(140,e*.25),h:Math.min(32,t*.15),radius:6,style:{marginTop:t*.04,background:"var(--agd-bar)"}})]})}function gx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:6,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:"0 10px",gap:8},children:[(0,u.jsx)("div",{style:{width:16,height:16,borderRadius:"50%",border:"1.5px solid var(--agd-bar-strong)",display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0},children:(0,u.jsx)("div",{style:{width:2,height:6,background:"var(--agd-bar-strong)",borderRadius:1}})}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:"40%",h:3,strong:!0}),(0,u.jsx)(H,{w:"70%",h:2})]})]})}function yx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center",gap:8,padding:"0 12px"},children:[(0,u.jsx)(H,{w:e*.4,h:3,strong:!0}),(0,u.jsx)(_t,{w:60,h:Math.min(24,t*.6),radius:4})]})}function px({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:t*.06},children:[(0,u.jsx)(H,{w:e*.5,h:2}),(0,u.jsx)(H,{w:e*.4,h:Math.max(8,t*.18),strong:!0}),(0,u.jsx)(H,{w:e*.3,h:2})]})}function bx({width:e,height:t}){let n=Math.max(3,Math.min(5,Math.floor(e/100))),l=Math.min(12,t*.35);return(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between",height:"100%",padding:"0 8px"},children:Array.from({length:n},(o,a)=>(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:0,flex:1},children:[(0,u.jsx)("div",{style:{width:l,height:l,borderRadius:"50%",border:"1.5px solid var(--agd-stroke)",background:a===0?"var(--agd-bar)":"transparent",flexShrink:0}}),a<n-1&&(0,u.jsx)("div",{style:{flex:1,height:1,background:"var(--agd-stroke)",margin:"0 4px"}})]},a))})}function xx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:4,border:"1px solid var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",justifyContent:"center",gap:4,padding:"0 6px"},children:[(0,u.jsx)(H,{w:Math.max(16,e*.5),h:2,strong:!0}),(0,u.jsx)("div",{style:{width:8,height:8,borderRadius:"50%",border:"1px solid var(--agd-stroke)",flexShrink:0}})]})}function vx({width:e,height:t}){let l=Math.min(t*.7,e/7.5);return(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"center",height:"100%",gap:l*.2},children:Array.from({length:5},(o,a)=>(0,u.jsx)("svg",{width:l,height:l,viewBox:"0 0 16 16",fill:"none",children:(0,u.jsx)("path",{d:"M8 1.5l2 4 4.5.7-3.25 3.1.75 4.5L8 11.4l-4 2.4.75-4.5L1.5 6.2 6 5.5z",stroke:"var(--agd-stroke)",strokeWidth:"0.8",fill:a<3?"var(--agd-bar)":"none"})},a))})}function wx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",position:"relative",borderRadius:4,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",overflow:"hidden"},children:[(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",style:{position:"absolute",inset:0},children:[(0,u.jsx)("line",{x1:0,y1:t*.3,x2:e,y2:t*.7,stroke:"var(--agd-stroke)",strokeWidth:"0.5",opacity:".2"}),(0,u.jsx)("line",{x1:0,y1:t*.6,x2:e,y2:t*.2,stroke:"var(--agd-stroke)",strokeWidth:"0.5",opacity:".15"}),(0,u.jsx)("line",{x1:e*.4,y1:0,x2:e*.6,y2:t,stroke:"var(--agd-stroke)",strokeWidth:"0.5",opacity:".15"})]}),(0,u.jsx)("div",{style:{position:"absolute",left:"50%",top:"40%",transform:"translate(-50%, -100%)"},children:(0,u.jsxs)("svg",{width:"16",height:"22",viewBox:"0 0 16 22",fill:"none",children:[(0,u.jsx)("path",{d:"M8 0C3.6 0 0 3.6 0 8c0 6 8 14 8 14s8-8 8-14c0-4.4-3.6-8-8-8z",fill:"var(--agd-bar)",opacity:".4"}),(0,u.jsx)("circle",{cx:"8",cy:"8",r:"3",fill:"var(--agd-fill)"})]})})]})}function kx({width:e,height:t}){let n=Math.max(3,Math.min(5,Math.floor(t/60)));return(0,u.jsxs)("div",{style:{display:"flex",height:"100%",padding:"8px 0"},children:[(0,u.jsx)("div",{style:{width:16,display:"flex",flexDirection:"column",alignItems:"center"},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",flex:1},children:[(0,u.jsx)(xn,{size:8}),o<n-1&&(0,u.jsx)("div",{style:{flex:1,width:1,background:"var(--agd-stroke)"}})]},o))}),(0,u.jsx)("div",{style:{flex:1,display:"flex",flexDirection:"column",justifyContent:"space-around",paddingLeft:8},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:`${35+o*13%25}%`,h:3,strong:!0}),(0,u.jsx)(H,{w:`${50+o*17%30}%`,h:2})]},o))})]})}function Sx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:8,border:"2px dashed var(--agd-stroke)",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:t*.06},children:[(0,u.jsxs)("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",children:[(0,u.jsx)("path",{d:"M12 16V4m0 0l-4 4m4-4l4 4",stroke:"var(--agd-stroke)",strokeWidth:"1.5"}),(0,u.jsx)("path",{d:"M4 17v2a1 1 0 001 1h14a1 1 0 001-1v-2",stroke:"var(--agd-stroke)",strokeWidth:"1.5"})]}),(0,u.jsx)(H,{w:e*.4,h:2}),(0,u.jsx)(H,{w:e*.25,h:2})]})}function Cx({width:e,height:t}){let n=Math.max(3,Math.min(8,Math.floor(t/20)));return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:6,background:"var(--agd-fill)",border:"1px solid var(--agd-stroke)",padding:8,display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsxs)("div",{style:{display:"flex",gap:3,marginBottom:4},children:[(0,u.jsx)(xn,{size:6}),(0,u.jsx)(xn,{size:6}),(0,u.jsx)(xn,{size:6})]}),Array.from({length:n},(l,o)=>(0,u.jsx)("div",{style:{display:"flex",gap:6,paddingLeft:o>0&&o<n-1?12:0},children:(0,u.jsx)(H,{w:`${25+o*23%50}%`,h:2,strong:o===0})},o))]})}function Mx({width:e,height:t}){let o=Math.min((e-16)/7,(t-40)/6);return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between",padding:"6px 8px"},children:[(0,u.jsx)("span",{style:{fontSize:8,color:"var(--agd-stroke)"},children:"\u2039"}),(0,u.jsx)(H,{w:e*.3,h:3,strong:!0}),(0,u.jsx)("span",{style:{fontSize:8,color:"var(--agd-stroke)"},children:"\u203A"})]}),(0,u.jsxs)("div",{style:{display:"grid",gridTemplateColumns:"repeat(7, 1fr)",gap:2,padding:"0 4px",flex:1},children:[Array.from({length:7},(a,i)=>(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"center",height:o*.6},children:(0,u.jsx)(H,{w:o*.5,h:2})},`h${i}`)),Array.from({length:35},(a,i)=>(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"center",height:o},children:(0,u.jsx)("div",{style:{width:o*.6,height:o*.6,borderRadius:"50%",background:i===12?"var(--agd-bar)":"transparent",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)("div",{style:{width:2,height:2,borderRadius:1,background:"var(--agd-bar-strong)",opacity:i===12?1:.3}})})},i))]})]})}function Ex({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",borderRadius:8,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:"0 10px",gap:8},children:[(0,u.jsx)(xn,{size:Math.min(32,t*.55)}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:"50%",h:3,strong:!0}),(0,u.jsx)(H,{w:"75%",h:2})]}),(0,u.jsx)(H,{w:30,h:2})]})}function Tx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column"},children:[(0,u.jsx)("div",{style:{height:"50%",background:"var(--agd-fill)",borderBottom:"1px dashed var(--agd-stroke)"}}),(0,u.jsxs)("div",{style:{flex:1,padding:10,display:"flex",flexDirection:"column",gap:5},children:[(0,u.jsx)(H,{w:"65%",h:4,strong:!0}),(0,u.jsx)(H,{w:"40%",h:3}),(0,u.jsx)("div",{style:{flex:1}}),(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between"},children:[(0,u.jsx)(H,{w:"30%",h:5,strong:!0}),(0,u.jsx)(_t,{w:Math.min(70,e*.3),h:26,radius:4,style:{background:"var(--agd-bar)"}})]})]})]})}function Dx({width:e,height:t}){let n=Math.min(48,t*.3);return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:t*.06},children:[(0,u.jsx)(xn,{size:n}),(0,u.jsx)(H,{w:e*.45,h:4,strong:!0}),(0,u.jsx)(H,{w:e*.3,h:2}),(0,u.jsxs)("div",{style:{display:"flex",gap:e*.08,marginTop:t*.04},children:[(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",gap:2},children:[(0,u.jsx)(H,{w:20,h:3,strong:!0}),(0,u.jsx)(H,{w:28,h:2})]}),(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",gap:2},children:[(0,u.jsx)(H,{w:20,h:3,strong:!0}),(0,u.jsx)(H,{w:28,h:2})]}),(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",gap:2},children:[(0,u.jsx)(H,{w:20,h:3,strong:!0}),(0,u.jsx)(H,{w:28,h:2})]})]})]})}function Nx({width:e,height:t}){let n=Math.max(e*.6,80),l=Math.max(3,Math.floor(t/40));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex"},children:[(0,u.jsx)("div",{style:{width:e-n,background:"var(--agd-fill)",opacity:.3}}),(0,u.jsxs)("div",{style:{flex:1,borderLeft:"1px solid var(--agd-stroke)",display:"flex",flexDirection:"column",padding:e*.04},children:[(0,u.jsxs)("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:t*.06},children:[(0,u.jsx)(H,{w:n*.4,h:4,strong:!0}),(0,u.jsx)("div",{style:{width:12,height:12,border:"1px solid var(--agd-stroke)",borderRadius:3}})]}),Array.from({length:l},(o,a)=>(0,u.jsx)("div",{style:{padding:"6px 0"},children:(0,u.jsx)(H,{w:`${50+a*17%35}%`,h:2,strong:a===0})},a))]})]})}function zx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center"},children:[(0,u.jsxs)("div",{style:{flex:1,width:"100%",borderRadius:8,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",padding:10,display:"flex",flexDirection:"column",gap:5},children:[(0,u.jsx)(H,{w:"70%",h:3,strong:!0}),(0,u.jsx)(H,{w:"90%",h:2}),(0,u.jsx)(H,{w:"60%",h:2})]}),(0,u.jsx)("div",{style:{width:10,height:10,background:"var(--agd-fill)",border:"1px dashed var(--agd-stroke)",borderTop:"none",borderLeft:"none",transform:"rotate(45deg)",marginTop:-6}})]})}function Ax({width:e,height:t}){let n=Math.min(t*.7,e*.3);return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",alignItems:"center",gap:e*.08},children:[(0,u.jsx)(_t,{w:n,h:n,radius:n*.25}),(0,u.jsx)(H,{w:e*.45,h:Math.max(4,t*.2),strong:!0})]})}function Lx({width:e,height:t}){let n=Math.max(2,Math.min(5,Math.floor(t/56)));return(0,u.jsx)("div",{style:{display:"flex",flexDirection:"column",height:"100%"},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{borderBottom:"1px solid var(--agd-stroke)",padding:"8px 6px",display:"flex",alignItems:"center",justifyContent:"space-between",flex:o===0?2:1},children:[(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",gap:6},children:[(0,u.jsx)("span",{style:{fontSize:9,fontWeight:700,color:"var(--agd-stroke)"},children:"Q"}),(0,u.jsx)(H,{w:e*(.3+o*13%25/100),h:3,strong:!0})]}),(0,u.jsx)("span",{style:{fontSize:8,color:"var(--agd-stroke)"},children:o===0?"\u25BC":"\u25B6"})]},o))})}function Rx({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/120))),l=Math.max(1,Math.min(3,Math.floor(t/120)));return(0,u.jsx)("div",{style:{display:"grid",gridTemplateColumns:`repeat(${n}, 1fr)`,gridTemplateRows:`repeat(${l}, 1fr)`,gap:4,height:"100%"},children:Array.from({length:n*l},(o,a)=>(0,u.jsx)("div",{style:{borderRadius:4,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",position:"relative",overflow:"hidden"},children:(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:"0 0 100 100",preserveAspectRatio:"none",fill:"none",children:[(0,u.jsx)("line",{x1:"0",y1:"0",x2:"100",y2:"100",stroke:"var(--agd-stroke)",strokeWidth:"0.5"}),(0,u.jsx)("line",{x1:"100",y1:"0",x2:"0",y2:"100",stroke:"var(--agd-stroke)",strokeWidth:"0.5"})]})},a))})}function Bx({width:e,height:t}){let n=Math.min(e,t);return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("rect",{x:"1",y:(t-n+2)/2,width:n-2,height:n-2,rx:n*.15,stroke:"var(--agd-stroke)",strokeWidth:"1.5"}),(0,u.jsx)("path",{d:`M${n*.25} ${t/2}l${n*.2} ${n*.2} ${n*.3}-${n*.35}`,stroke:"var(--agd-bar)",strokeWidth:"1.5",fill:"none",strokeLinecap:"round",strokeLinejoin:"round"})]})}function Ox({width:e,height:t}){let n=Math.min(e,t)/2-1;return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("circle",{cx:e/2,cy:t/2,r:n,stroke:"var(--agd-stroke)",strokeWidth:"1.5"}),(0,u.jsx)("circle",{cx:e/2,cy:t/2,r:n*.45,fill:"var(--agd-bar)"})]})}function $x({width:e,height:t}){let n=Math.max(2,t*.12),l=Math.min(t*.35,10),o=e*.55;return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",alignItems:"center",position:"relative"},children:[(0,u.jsx)("div",{style:{width:"100%",height:n,borderRadius:n/2,background:"var(--agd-fill)",border:"1px solid var(--agd-stroke)",position:"relative"},children:(0,u.jsx)("div",{style:{width:o,height:"100%",borderRadius:n/2,background:"var(--agd-bar)"}})}),(0,u.jsx)("div",{style:{position:"absolute",left:o-l,width:l*2,height:l*2,borderRadius:"50%",border:"1.5px solid var(--agd-stroke)",background:"var(--agd-fill)"}})]})}function Hx({width:e,height:t}){let n=Math.min(36,t*.15),l=7,o=4,a=Math.min((e-16)/l,(t-n-40)/(o+1));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsxs)("div",{style:{height:n,borderRadius:4,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:"0 8px",justifyContent:"space-between"},children:[(0,u.jsx)(H,{w:"40%",h:2}),(0,u.jsxs)("svg",{width:"12",height:"12",viewBox:"0 0 16 16",fill:"none",children:[(0,u.jsx)("rect",{x:"2",y:"3",width:"12",height:"11",rx:"1",stroke:"var(--agd-stroke)",strokeWidth:"1"}),(0,u.jsx)("line",{x1:"2",y1:"6",x2:"14",y2:"6",stroke:"var(--agd-stroke)",strokeWidth:"0.5"})]})]}),(0,u.jsxs)("div",{style:{flex:1,borderRadius:6,border:"1px dashed var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",flexDirection:"column"},children:[(0,u.jsxs)("div",{style:{display:"flex",alignItems:"center",justifyContent:"space-between",padding:"4px 6px"},children:[(0,u.jsx)("span",{style:{fontSize:7,color:"var(--agd-stroke)"},children:"\u2039"}),(0,u.jsx)(H,{w:e*.25,h:2,strong:!0}),(0,u.jsx)("span",{style:{fontSize:7,color:"var(--agd-stroke)"},children:"\u203A"})]}),(0,u.jsx)("div",{style:{display:"grid",gridTemplateColumns:`repeat(${l}, 1fr)`,gap:1,padding:"0 4px",flex:1},children:Array.from({length:l*o},(i,s)=>(0,u.jsx)("div",{style:{display:"flex",alignItems:"center",justifyContent:"center",height:a},children:(0,u.jsx)("div",{style:{width:a*.5,height:a*.5,borderRadius:"50%",background:s===10?"var(--agd-bar)":"transparent"},children:(0,u.jsx)("div",{style:{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)("div",{style:{width:1.5,height:1.5,borderRadius:1,background:"var(--agd-bar-strong)",opacity:s===10?1:.25}})})})},s))})]})]})}function Ux({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",gap:t*.08,padding:4},children:[(0,u.jsx)("div",{style:{width:"100%",height:t*.2,borderRadius:4,background:"var(--agd-fill)"}}),(0,u.jsx)("div",{style:{width:"70%",height:Math.max(6,t*.1),borderRadius:3,background:"var(--agd-fill)"}}),(0,u.jsx)("div",{style:{width:"90%",height:Math.max(4,t*.06),borderRadius:3,background:"var(--agd-fill)"}}),(0,u.jsx)("div",{style:{width:"50%",height:Math.max(4,t*.06),borderRadius:3,background:"var(--agd-fill)"}})]})}function Yx({width:e,height:t}){return(0,u.jsx)("div",{style:{height:"100%",display:"flex",alignItems:"center",gap:6},children:(0,u.jsxs)("div",{style:{height:"100%",flex:1,borderRadius:t/2,border:"1px solid var(--agd-stroke)",background:"var(--agd-fill)",display:"flex",alignItems:"center",padding:`0 ${t*.3}px`,gap:4},children:[(0,u.jsx)(H,{w:"60%",h:2,strong:!0}),(0,u.jsx)("div",{style:{width:Math.max(6,t*.3),height:Math.max(6,t*.3),borderRadius:"50%",border:"1px solid var(--agd-stroke)",flexShrink:0,marginLeft:"auto"}})]})})}function jx({width:e,height:t}){let n=Math.min(e,t);return(0,u.jsx)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:(0,u.jsx)("path",{d:`M${e/2} ${(t-n)/2+n*.1}l${n*.12} ${n*.25} ${n*.28} ${n*.04}-${n*.2} ${n*.2} ${n*.05} ${n*.28}-${n*.25}-${n*.12}-${n*.25} ${n*.12} ${n*.05}-${n*.28}-${n*.2}-${n*.2} ${n*.28}-${n*.04}z`,stroke:"var(--agd-stroke)",strokeWidth:"1",fill:"var(--agd-fill)"})})}function Xx({width:e,height:t}){let n=Math.min(e,t)/2-2;return(0,u.jsxs)("svg",{width:"100%",height:"100%",viewBox:`0 0 ${e} ${t}`,fill:"none",children:[(0,u.jsx)("circle",{cx:e/2,cy:t/2,r:n,stroke:"var(--agd-stroke)",strokeWidth:"1.5",opacity:".2"}),(0,u.jsx)("path",{d:`M${e/2} ${t/2-n}a${n} ${n} 0 0 1 ${n} ${n}`,stroke:"var(--agd-bar-strong)",strokeWidth:"1.5",strokeLinecap:"round"})]})}function Ix({width:e,height:t}){let n=Math.min(36,t*.25,e*.12),l=Math.max(1,Math.min(3,Math.floor(t/80)));return(0,u.jsx)("div",{style:{display:"flex",flexDirection:"column",height:"100%",justifyContent:"space-around",padding:8},children:Array.from({length:l},(o,a)=>(0,u.jsxs)("div",{style:{display:"flex",gap:e*.04,alignItems:"flex-start"},children:[(0,u.jsx)(_t,{w:n,h:n,radius:n*.25}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:4},children:[(0,u.jsx)(H,{w:`${40+a*13%20}%`,h:3,strong:!0}),(0,u.jsx)(H,{w:`${60+a*17%25}%`,h:2})]})]},a))})}function qx({width:e,height:t}){let n=Math.max(2,Math.min(4,Math.floor(e/120))),l=Math.min(36,t*.25);return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center",gap:t*.06,padding:t*.06},children:[(0,u.jsx)(H,{w:e*.3,h:4,strong:!0}),(0,u.jsx)("div",{style:{display:"flex",gap:e*.06,justifyContent:"center",flex:1,alignItems:"center"},children:Array.from({length:n},(o,a)=>(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",alignItems:"center",gap:6},children:[(0,u.jsx)(xn,{size:l}),(0,u.jsx)(H,{w:e*.12,h:3,strong:!0}),(0,u.jsx)(H,{w:e*.08,h:2})]},a))})]})}function Qx({width:e,height:t}){let n=Math.max(2,Math.min(3,Math.floor(t/80)));return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",alignItems:"center",padding:e*.06,gap:t*.04},children:[(0,u.jsx)(H,{w:e*.5,h:Math.max(5,t*.04),strong:!0}),(0,u.jsx)(H,{w:e*.35,h:2}),(0,u.jsx)("div",{style:{width:"100%",display:"flex",flexDirection:"column",gap:t*.03,marginTop:t*.04},children:Array.from({length:n},(l,o)=>(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:Math.min(60,e*.2),h:2}),(0,u.jsx)(_t,{w:"100%",h:Math.min(32,t*.1),radius:4})]},o))}),(0,u.jsx)(_t,{w:"100%",h:Math.min(36,t*.12),radius:6,style:{marginTop:t*.03,background:"var(--agd-bar)"}}),(0,u.jsx)(H,{w:e*.4,h:2})]})}function Wx({width:e,height:t}){return(0,u.jsxs)("div",{style:{height:"100%",display:"flex",flexDirection:"column",padding:e*.04,gap:t*.03},children:[(0,u.jsx)(H,{w:e*.4,h:4,strong:!0}),(0,u.jsx)(H,{w:e*.6,h:2}),(0,u.jsxs)("div",{style:{display:"flex",gap:6,marginTop:t*.03},children:[(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:50,h:2}),(0,u.jsx)(_t,{w:"100%",h:Math.min(28,t*.1),radius:4})]}),(0,u.jsxs)("div",{style:{flex:1,display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:40,h:2}),(0,u.jsx)(_t,{w:"100%",h:Math.min(28,t*.1),radius:4})]})]}),(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:3},children:[(0,u.jsx)(H,{w:50,h:2}),(0,u.jsx)(_t,{w:"100%",h:Math.min(28,t*.1),radius:4})]}),(0,u.jsxs)("div",{style:{display:"flex",flexDirection:"column",gap:3,flex:1},children:[(0,u.jsx)(H,{w:60,h:2}),(0,u.jsx)(_t,{w:"100%",h:"100%",radius:4})]}),(0,u.jsx)(_t,{w:Math.min(120,e*.3),h:Math.min(30,t*.1),radius:6,style:{alignSelf:"flex-end",background:"var(--agd-bar)"}})]})}var Gx={navigation:Bb,hero:Ob,sidebar:$b,footer:Hb,modal:Ub,card:Yb,text:jb,image:Xb,table:Ib,list:qb,button:Qb,input:Wb,form:Gb,tabs:Vb,avatar:Zb,badge:Kb,header:Fb,section:Jb,grid:Pb,dropdown:ex,toggle:tx,search:nx,toast:lx,progress:ox,chart:ax,video:ix,tooltip:sx,breadcrumb:rx,pagination:cx,divider:ux,accordion:dx,carousel:_x,pricing:fx,testimonial:hx,cta:mx,alert:gx,banner:yx,stat:px,stepper:bx,tag:xx,rating:vx,map:wx,timeline:kx,fileUpload:Sx,codeBlock:Cx,calendar:Mx,notification:Ex,productCard:Tx,profile:Dx,drawer:Nx,popover:zx,logo:Ax,faq:Lx,gallery:Rx,checkbox:Bx,radio:Ox,slider:$x,datePicker:Hx,skeleton:Ux,chip:Yx,icon:jx,spinner:Xx,feature:Ix,team:qx,login:Qx,contact:Wx};function Vx({type:e,width:t,height:n,text:l}){let o=Gx[e];return o?(0,u.jsx)("div",{style:{width:"100%",height:"100%",padding:8,position:"relative",pointerEvents:"none"},children:(0,u.jsx)(o,{width:t,height:n,text:l})}):(0,u.jsx)("div",{style:{width:"100%",height:"100%",display:"flex",alignItems:"center",justifyContent:"center"},children:(0,u.jsx)("span",{style:{fontSize:10,fontWeight:600,color:"var(--agd-text-3)",textTransform:"uppercase",letterSpacing:"0.06em",opacity:.5},children:e})})}var Zx=`svg[fill=none] {
  fill: none !important;
}

.styles-module__overlayExiting___iEmYr {
  opacity: 0 !important;
  transition: opacity 0.25s ease !important;
  pointer-events: none !important;
}

.styles-module__overlay___aWh-q {
  position: fixed;
  inset: 0;
  z-index: 99995;
  pointer-events: auto;
  cursor: default;
  animation: styles-module__overlayFadeIn___aECVy 0.15s ease;
  --agd-stroke: rgba(59, 130, 246, 0.35);
  --agd-fill: rgba(59, 130, 246, 0.06);
  --agd-bar: rgba(59, 130, 246, 0.18);
  --agd-bar-strong: rgba(59, 130, 246, 0.28);
  --agd-text-3: rgba(255, 255, 255, 0.6);
  --agd-surface: #fff;
}
.styles-module__overlay___aWh-q.styles-module__light___ORIft {
  --agd-surface: #fff;
}
.styles-module__overlay___aWh-q:not(.styles-module__light___ORIft) {
  --agd-surface: #141414;
}
.styles-module__overlay___aWh-q.styles-module__wireframe___itvQU {
  --agd-stroke: rgba(249, 115, 22, 0.35);
  --agd-fill: rgba(249, 115, 22, 0.06);
  --agd-bar: rgba(249, 115, 22, 0.18);
  --agd-bar-strong: rgba(249, 115, 22, 0.28);
}
.styles-module__overlay___aWh-q.styles-module__placing___45yD8 {
  cursor: crosshair;
}
.styles-module__overlay___aWh-q.styles-module__passthrough___xaFeE {
  pointer-events: none;
}

.styles-module__blankCanvas___t2Eue {
  position: fixed;
  inset: 0;
  z-index: 99994;
  background: #fff;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}
.styles-module__blankCanvas___t2Eue.styles-module__visible___OKKqX {
  opacity: var(--canvas-opacity, 1);
  pointer-events: auto;
}
.styles-module__blankCanvas___t2Eue::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(0, 0, 0, 0.08) 1px, transparent 1px);
  background-size: 24px 24px;
  background-position: 12px 12px;
  pointer-events: none;
  transition: opacity 0.2s ease;
}
.styles-module__blankCanvas___t2Eue.styles-module__gridActive___OZ-cf::after {
  opacity: 1;
  background-image: radial-gradient(circle, rgba(0, 0, 0, 0.22) 1px, transparent 1px);
}

.styles-module__paletteHeader___-Q5gQ {
  padding: 0 1rem 0.375rem;
}

.styles-module__paletteHeaderTitle___oHqZC {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #fff;
  letter-spacing: -0.0094em;
}
.styles-module__light___ORIft .styles-module__paletteHeaderTitle___oHqZC {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__paletteHeaderDesc___6i74T {
  font-size: 0.6875rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.45);
  margin-top: 2px;
  line-height: 14px;
}
.styles-module__light___ORIft .styles-module__paletteHeaderDesc___6i74T {
  color: rgba(0, 0, 0, 0.45);
}
.styles-module__paletteHeaderDesc___6i74T a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: underline dotted;
  text-decoration-color: rgba(255, 255, 255, 0.2);
  text-underline-offset: 2px;
  transition: color 0.15s ease;
}
.styles-module__paletteHeaderDesc___6i74T a:hover {
  color: #fff;
}
.styles-module__light___ORIft .styles-module__paletteHeaderDesc___6i74T a {
  color: rgba(0, 0, 0, 0.6);
  text-decoration-color: rgba(0, 0, 0, 0.2);
}
.styles-module__light___ORIft .styles-module__paletteHeaderDesc___6i74T a:hover {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__wireframePurposeWrap___To-tS {
  display: grid;
  grid-template-rows: 1fr;
  transition: grid-template-rows 0.2s ease, opacity 0.15s ease;
  opacity: 1;
}
.styles-module__wireframePurposeWrap___To-tS.styles-module__collapsed___Ms9vS {
  grid-template-rows: 0fr;
  opacity: 0;
}

.styles-module__wireframePurposeInner___Lrahs {
  overflow: hidden;
}

.styles-module__wireframePurposeInput___7EtBN {
  display: block;
  width: calc(100% - 2rem);
  margin: 0.25rem 1rem 0.375rem;
  padding: 0.375rem 0.5rem;
  font-size: 0.8125rem;
  font-family: inherit;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.375rem;
  resize: none;
  outline: none;
  transition: border-color 0.15s ease;
  letter-spacing: -0.0094em;
}
.styles-module__wireframePurposeInput___7EtBN::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.styles-module__wireframePurposeInput___7EtBN:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.05);
}
.styles-module__light___ORIft .styles-module__wireframePurposeInput___7EtBN {
  color: rgba(0, 0, 0, 0.7);
  background: rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.1);
}
.styles-module__light___ORIft .styles-module__wireframePurposeInput___7EtBN::placeholder {
  color: rgba(0, 0, 0, 0.3);
}
.styles-module__light___ORIft .styles-module__wireframePurposeInput___7EtBN:focus {
  border-color: rgba(0, 0, 0, 0.25);
  background: rgba(0, 0, 0, 0.05);
}

.styles-module__canvasToggle___-QqSy {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  margin: 0.25rem 1rem 0.25rem;
  padding: 0.375rem 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  background: transparent;
  transition: background 0.15s ease, border-color 0.15s ease;
}
.styles-module__canvasToggle___-QqSy:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.15);
}
.styles-module__canvasToggle___-QqSy.styles-module__active___hosp7 {
  background: #f97316;
  border-color: transparent;
  border-style: solid;
  box-shadow: none;
}
.styles-module__light___ORIft .styles-module__canvasToggle___-QqSy {
  border-color: rgba(0, 0, 0, 0.08);
}
.styles-module__light___ORIft .styles-module__canvasToggle___-QqSy:hover {
  background: rgba(0, 0, 0, 0.02);
  border-color: rgba(0, 0, 0, 0.12);
}
.styles-module__light___ORIft .styles-module__canvasToggle___-QqSy.styles-module__active___hosp7 {
  background: #f97316;
  border-color: transparent;
  border-style: solid;
  box-shadow: none;
}

.styles-module__canvasToggleIcon___7pJ82 {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.35);
}
.styles-module__active___hosp7 .styles-module__canvasToggleIcon___7pJ82 {
  color: rgba(255, 255, 255, 0.85);
}
.styles-module__light___ORIft .styles-module__canvasToggleIcon___7pJ82 {
  color: rgba(0, 0, 0, 0.25);
}
.styles-module__light___ORIft .styles-module__active___hosp7 .styles-module__canvasToggleIcon___7pJ82 {
  color: rgba(255, 255, 255, 0.85);
}

.styles-module__canvasToggleLabel___OanpY {
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: -0.0094em;
}
.styles-module__active___hosp7 .styles-module__canvasToggleLabel___OanpY {
  color: #fff;
}
.styles-module__light___ORIft .styles-module__canvasToggleLabel___OanpY {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___ORIft .styles-module__active___hosp7 .styles-module__canvasToggleLabel___OanpY {
  color: #fff;
}

.styles-module__canvasPurposeWrap___hj6zk {
  display: grid;
  grid-template-rows: 1fr;
  transition: grid-template-rows 0.2s ease, opacity 0.15s ease;
  opacity: 1;
}
.styles-module__canvasPurposeWrap___hj6zk.styles-module__collapsed___Ms9vS {
  grid-template-rows: 0fr;
  opacity: 0;
}

.styles-module__canvasPurposeInner___VWiyu {
  overflow: hidden;
}

.styles-module__canvasPurposeToggle___byDH2 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  margin: 0.375rem 1rem 0.375rem 1.1875rem;
}
.styles-module__canvasPurposeToggle___byDH2 input[type=checkbox] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.styles-module__canvasPurposeCheck___xqd7l {
  position: relative;
  width: 14px;
  height: 14px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.25s ease, border-color 0.25s ease;
}
.styles-module__canvasPurposeCheck___xqd7l svg {
  color: #1a1a1a;
  opacity: 1;
  transition: opacity 0.15s ease;
}
.styles-module__canvasPurposeCheck___xqd7l.styles-module__checked___-1JGH {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgb(255, 255, 255);
}
.styles-module__light___ORIft .styles-module__canvasPurposeCheck___xqd7l {
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: #fff;
}
.styles-module__light___ORIft .styles-module__canvasPurposeCheck___xqd7l.styles-module__checked___-1JGH {
  border-color: #1a1a1a;
  background: #1a1a1a;
}
.styles-module__light___ORIft .styles-module__canvasPurposeCheck___xqd7l.styles-module__checked___-1JGH svg {
  color: #fff;
}

.styles-module__canvasPurposeLabel___Zu-tD {
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: -0.0094em;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.styles-module__light___ORIft .styles-module__canvasPurposeLabel___Zu-tD {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__canvasPurposeHelp___jijwR {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: help;
}
.styles-module__canvasPurposeHelp___jijwR svg {
  color: rgba(255, 255, 255, 0.2);
  transform: translateY(2px);
  transition: color 0.15s ease;
}
.styles-module__canvasPurposeHelp___jijwR:hover svg {
  color: rgba(255, 255, 255, 0.5);
}
.styles-module__light___ORIft .styles-module__canvasPurposeHelp___jijwR svg {
  color: rgba(0, 0, 0, 0.2);
}
.styles-module__light___ORIft .styles-module__canvasPurposeHelp___jijwR:hover svg {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__placement___zcxv8 {
  position: absolute;
  border: 1.5px dashed rgba(59, 130, 246, 0.4);
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.08);
  cursor: grab;
  transition: box-shadow 0.15s, border-color 0.15s, opacity 0.15s ease, transform 0.15s ease;
  user-select: none;
  pointer-events: auto;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  animation: styles-module__placementEnter___TdRhf 0.25s cubic-bezier(0.34, 1.2, 0.64, 1);
}
.styles-module__placement___zcxv8:active {
  cursor: grabbing;
}
.styles-module__placement___zcxv8:hover {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.12);
}
.styles-module__placement___zcxv8.styles-module__selected___6yrp6 {
  border-color: #3c82f7;
  border-style: solid;
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.15);
}
.styles-module__placement___zcxv8.styles-module__selected___6yrp6:hover {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.15);
}
.styles-module__wireframe___itvQU .styles-module__placement___zcxv8 {
  border-color: rgba(249, 115, 22, 0.4);
  background: rgba(249, 115, 22, 0.08);
}
.styles-module__wireframe___itvQU .styles-module__placement___zcxv8:hover {
  border-color: rgba(249, 115, 22, 0.5);
  background: rgba(249, 115, 22, 0.1);
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.12);
}
.styles-module__wireframe___itvQU .styles-module__placement___zcxv8.styles-module__selected___6yrp6 {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.1);
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.15), 0 2px 8px rgba(249, 115, 22, 0.15);
}
.styles-module__wireframe___itvQU .styles-module__placement___zcxv8.styles-module__selected___6yrp6:hover {
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.15), 0 2px 8px rgba(249, 115, 22, 0.15);
}
.styles-module__placement___zcxv8.styles-module__dragging___le6KZ {
  opacity: 0.85;
  z-index: 50;
}
.styles-module__placement___zcxv8.styles-module__exiting___YrM8F {
  opacity: 0;
  transform: scale(0.97);
  pointer-events: none;
  animation: none;
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.32, 0.72, 0, 1);
}

.styles-module__placementContent___f64A4 {
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.styles-module__placementLabel___0KvWl {
  position: absolute;
  top: -18px;
  left: 0;
  font-size: 10px;
  font-weight: 600;
  color: rgba(59, 130, 246, 0.7);
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.8), 0 0 8px rgba(255, 255, 255, 0.5);
}
.styles-module__selected___6yrp6 .styles-module__placementLabel___0KvWl {
  color: #3c82f7;
}
.styles-module__wireframe___itvQU .styles-module__placementLabel___0KvWl {
  color: rgba(249, 115, 22, 0.7);
}
.styles-module__wireframe___itvQU .styles-module__selected___6yrp6 .styles-module__placementLabel___0KvWl {
  color: #f97316;
}

.styles-module__placementAnnotation___78pTr {
  position: absolute;
  bottom: -18px;
  left: 0;
  right: 0;
  font-weight: 450;
  color: rgba(0, 0, 0, 0.5);
  font-size: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.9), 0 0 8px rgba(255, 255, 255, 0.6);
  opacity: 0;
  transform: translateY(-2px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.styles-module__placementAnnotation___78pTr.styles-module__annotationVisible___mrUyA {
  opacity: 1;
  transform: translateY(0);
}

.styles-module__sectionAnnotation___aUIs0 {
  position: absolute;
  bottom: -18px;
  left: 0;
  right: 0;
  font-weight: 450;
  color: rgba(59, 130, 246, 0.6);
  font-size: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.9), 0 0 8px rgba(255, 255, 255, 0.6);
  opacity: 0;
  transform: translateY(-2px);
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.styles-module__sectionAnnotation___aUIs0.styles-module__annotationVisible___mrUyA {
  opacity: 1;
  transform: translateY(0);
}

.styles-module__handle___Ikbxm {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #fff;
  border: 1.5px solid #3c82f7;
  border-radius: 2px;
  z-index: 12;
  box-shadow: 0 0 0 0.5px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.12);
  opacity: 0;
  transform: scale(0.3);
  pointer-events: none;
  will-change: opacity, transform;
  transition: opacity 0.2s ease-out, transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.styles-module__placement___zcxv8:hover .styles-module__handle___Ikbxm, .styles-module__sectionOutline___s0hy-:hover .styles-module__handle___Ikbxm, .styles-module__ghostOutline___po-kO:hover .styles-module__handle___Ikbxm, .styles-module__placement___zcxv8:active .styles-module__handle___Ikbxm, .styles-module__sectionOutline___s0hy-:active .styles-module__handle___Ikbxm, .styles-module__ghostOutline___po-kO:active .styles-module__handle___Ikbxm, .styles-module__selected___6yrp6 .styles-module__handle___Ikbxm {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}
.styles-module__sectionOutline___s0hy- .styles-module__handle___Ikbxm {
  border-color: inherit;
}
.styles-module__wireframe___itvQU .styles-module__handle___Ikbxm {
  border-color: #f97316;
}

.styles-module__handleNw___4TMIj {
  top: -4px;
  left: -4px;
  cursor: nw-resize;
}

.styles-module__handleNe___mnsTh {
  top: -4px;
  right: -4px;
  cursor: ne-resize;
}

.styles-module__handleSe___oSFnk {
  bottom: -4px;
  right: -4px;
  cursor: se-resize;
}

.styles-module__handleSw___pi--Z {
  bottom: -4px;
  left: -4px;
  cursor: sw-resize;
}

.styles-module__handleN___aBA-Q, .styles-module__handleE___0hM5u, .styles-module__handleS___JjDRv, .styles-module__handleW___ERWGQ {
  opacity: 0 !important;
  pointer-events: none !important;
}

.styles-module__edgeHandle___XxXdT {
  position: absolute;
  z-index: 11;
  display: flex;
  align-items: center;
  justify-content: center;
}
.styles-module__edgeHandle___XxXdT::after {
  content: "";
  position: absolute;
  border-radius: 4px;
  background: #3c82f7;
}
.styles-module__wireframe___itvQU .styles-module__edgeHandle___XxXdT::after {
  background: #f97316;
}
.styles-module__edgeHandle___XxXdT::after {
  opacity: 0;
  transition: opacity 0.1s ease, transform 0.1s ease;
  transform: scale(0.8);
}
.styles-module__edgeHandle___XxXdT:hover::after {
  opacity: 0.85;
  transform: scale(1);
}
.styles-module__edgeHandle___XxXdT svg {
  position: relative;
  z-index: 1;
  opacity: 0;
  transition: opacity 0.1s ease;
  filter: drop-shadow(0 0 2px var(--agd-surface));
}
.styles-module__edgeHandle___XxXdT:hover svg {
  opacity: 1;
}

.styles-module__edgeN___-JJDj, .styles-module__edgeS___66lMX {
  left: 12px;
  right: 12px;
  height: 12px;
  cursor: n-resize;
}
.styles-module__edgeN___-JJDj::after, .styles-module__edgeS___66lMX::after {
  width: 24px;
  height: 4px;
}

.styles-module__edgeN___-JJDj {
  top: -6px;
}

.styles-module__edgeS___66lMX {
  bottom: -6px;
  cursor: s-resize;
}

.styles-module__edgeE___1bGDa, .styles-module__edgeW___lHQNo {
  top: 12px;
  bottom: 12px;
  width: 12px;
  cursor: e-resize;
}
.styles-module__edgeE___1bGDa::after, .styles-module__edgeW___lHQNo::after {
  width: 4px;
  height: 24px;
}

.styles-module__edgeE___1bGDa {
  right: -6px;
}

.styles-module__edgeW___lHQNo {
  left: -6px;
  cursor: w-resize;
}

.styles-module__deleteButton___LkGCb {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  color: rgba(0, 0, 0, 0.35);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  line-height: 1;
  z-index: 15;
  pointer-events: none;
  opacity: 0;
  transform: scale(0.8);
  will-change: opacity, transform;
  transition: opacity 0.2s ease-out, transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.12s ease, color 0.12s ease, border-color 0.12s ease, box-shadow 0.12s ease;
}
.styles-module__placement___zcxv8:hover .styles-module__deleteButton___LkGCb, .styles-module__selected___6yrp6 .styles-module__deleteButton___LkGCb, .styles-module__sectionOutline___s0hy-:hover .styles-module__deleteButton___LkGCb, .styles-module__sectionOutline___s0hy-.styles-module__selected___6yrp6 .styles-module__deleteButton___LkGCb, .styles-module__ghostOutline___po-kO:hover .styles-module__deleteButton___LkGCb, .styles-module__ghostOutline___po-kO.styles-module__selected___6yrp6 .styles-module__deleteButton___LkGCb {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}
.styles-module__deleteButton___LkGCb:hover {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
  box-shadow: 0 1px 4px rgba(239, 68, 68, 0.3);
  transform: scale(1.1);
}
.styles-module__overlay___aWh-q:not(.styles-module__light___ORIft) .styles-module__deleteButton___LkGCb, .styles-module__rearrangeOverlay___-3R3t:not(.styles-module__light___ORIft) .styles-module__deleteButton___LkGCb {
  background: rgba(40, 40, 40, 0.9);
  border-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
}
.styles-module__overlay___aWh-q:not(.styles-module__light___ORIft) .styles-module__deleteButton___LkGCb:hover, .styles-module__rearrangeOverlay___-3R3t:not(.styles-module__light___ORIft) .styles-module__deleteButton___LkGCb:hover {
  background: #ef4444;
  color: #fff;
  border-color: #ef4444;
}

.styles-module__drawBox___BrVAa {
  position: fixed;
  pointer-events: none;
  z-index: 99996;
  border: 2px solid #3c82f7;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.15);
}

.styles-module__selectBox___Iu8kB {
  position: fixed;
  pointer-events: none;
  z-index: 99996;
  border: 1px dashed #3c82f7;
  background: rgba(59, 130, 246, 0.08);
  border-radius: 2px;
}

.styles-module__sizeIndicator___7zJ4y {
  position: fixed;
  pointer-events: none;
  z-index: 100001;
  font-size: 10px;
  color: #fff;
  background: #3c82f7;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  font-weight: 500;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.styles-module__guideLine___DUQY2 {
  pointer-events: none;
  z-index: 100001;
  background: #f0f;
  opacity: 0.5;
}

.styles-module__dragPreview___onPbU {
  position: fixed;
  z-index: 100002;
  pointer-events: none;
  border: 1.5px dashed #3c82f7;
  border-radius: 6px;
  background: rgba(59, 130, 246, 0.1);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 600;
  color: #3c82f7;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.15);
  transition: width 0.08s ease, height 0.08s ease, opacity 0.08s ease;
}

.styles-module__dragPreviewWireframe___jsg0G {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.15);
}

.styles-module__palette___C7iSH {
  position: absolute;
  right: 5px;
  bottom: calc(100% + 0.5rem);
  width: 256px;
  overflow: hidden;
  background: #1c1c1c;
  border: none;
  border-radius: 1rem;
  padding: 13px 0 16px;
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.04);
  z-index: 100001;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  cursor: default;
  opacity: 0;
  filter: blur(5px);
}
.styles-module__palette___C7iSH .styles-module__paletteItem___6TlnA,
.styles-module__palette___C7iSH .styles-module__paletteItemLabel___6ncO4,
.styles-module__palette___C7iSH .styles-module__paletteSectionTitle___PqnjX,
.styles-module__palette___C7iSH .styles-module__paletteFooter___QYnAG {
  transition: background 0.25s ease, color 0.25s ease, border-color 0.25s ease;
}
.styles-module__palette___C7iSH.styles-module__enter___6LYk5 {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0px);
  transition: opacity 0.2s ease, transform 0.2s ease, filter 0.2s ease;
}
.styles-module__palette___C7iSH.styles-module__exit___iSGRw {
  opacity: 0;
  transform: translateY(6px);
  filter: blur(5px);
  pointer-events: none;
  transition: opacity 0.1s ease, transform 0.1s ease, filter 0.1s ease;
}
.styles-module__palette___C7iSH.styles-module__light___ORIft {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}

.styles-module__paletteSection___V8DEA {
  padding: 0 1rem;
}
.styles-module__paletteSection___V8DEA + .styles-module__paletteSection___V8DEA {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
}
.styles-module__light___ORIft .styles-module__paletteSection___V8DEA + .styles-module__paletteSection___V8DEA {
  border-top-color: rgba(0, 0, 0, 0.07);
}

.styles-module__paletteSectionTitle___PqnjX {
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: -0.0094em;
  padding: 0 0 3px 3px;
}
.styles-module__light___ORIft .styles-module__paletteSectionTitle___PqnjX {
  color: rgba(0, 0, 0, 0.4);
}

.styles-module__paletteItem___6TlnA {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.25rem;
  margin-bottom: 1px;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
  border: 1px solid transparent;
  user-select: none;
  min-height: 24px;
}
.styles-module__paletteItem___6TlnA:hover {
  background: rgba(255, 255, 255, 0.1);
}
.styles-module__paletteItem___6TlnA.styles-module__active___hosp7 {
  background: #3c82f7;
  border-color: transparent;
}
.styles-module__paletteItem___6TlnA.styles-module__wireframe___itvQU.styles-module__active___hosp7 {
  background: #f97316;
}
.styles-module__light___ORIft .styles-module__paletteItem___6TlnA:hover {
  background: rgba(0, 0, 0, 0.05);
}
.styles-module__light___ORIft .styles-module__paletteItem___6TlnA.styles-module__active___hosp7 {
  background: #3c82f7;
  border-color: transparent;
}
.styles-module__light___ORIft .styles-module__paletteItem___6TlnA.styles-module__wireframe___itvQU.styles-module__active___hosp7 {
  background: #f97316;
}

.styles-module__paletteItemIcon___0NPQK {
  width: 20px;
  height: 16px;
  border-radius: 2px;
  border: 1px dashed rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  color: rgba(255, 255, 255, 0.45);
}
.styles-module__paletteItemIcon___0NPQK svg {
  display: block;
  width: 20px;
  height: 16px;
}
.styles-module__active___hosp7 .styles-module__paletteItemIcon___0NPQK {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}
.styles-module__light___ORIft .styles-module__paletteItemIcon___0NPQK {
  border-color: rgba(0, 0, 0, 0.12);
  background: rgba(0, 0, 0, 0.02);
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___ORIft .styles-module__active___hosp7 .styles-module__paletteItemIcon___0NPQK {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.styles-module__paletteItemLabel___6ncO4 {
  font-size: 0.8125rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  letter-spacing: -0.0094em;
  line-height: 1;
  min-width: 0;
}
.styles-module__active___hosp7 .styles-module__paletteItemLabel___6ncO4 {
  color: #fff;
  font-weight: 600;
}
.styles-module__light___ORIft .styles-module__paletteItemLabel___6ncO4 {
  color: rgba(0, 0, 0, 0.7);
}
.styles-module__light___ORIft .styles-module__active___hosp7 .styles-module__paletteItemLabel___6ncO4 {
  color: #fff;
  font-weight: 600;
}

.styles-module__placeScroll___7sClM {
  max-height: 240px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 0.25rem;
}
.styles-module__placeScroll___7sClM.styles-module__fadeTop___KT9tF {
  -webkit-mask-image: linear-gradient(to bottom, transparent 0, black 32px);
  mask-image: linear-gradient(to bottom, transparent 0, black 32px);
}
.styles-module__placeScroll___7sClM.styles-module__fadeBottom___x3ShT {
  -webkit-mask-image: linear-gradient(to bottom, black calc(100% - 32px), transparent 100%);
  mask-image: linear-gradient(to bottom, black calc(100% - 32px), transparent 100%);
}
.styles-module__placeScroll___7sClM.styles-module__fadeTop___KT9tF.styles-module__fadeBottom___x3ShT {
  -webkit-mask-image: linear-gradient(to bottom, transparent 0, black 32px, black calc(100% - 32px), transparent 100%);
  mask-image: linear-gradient(to bottom, transparent 0, black 32px, black calc(100% - 32px), transparent 100%);
}
.styles-module__placeScroll___7sClM::-webkit-scrollbar {
  width: 3px;
}
.styles-module__placeScroll___7sClM::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 2px;
}
.styles-module__light___ORIft .styles-module__placeScroll___7sClM::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
}

.styles-module__paletteFooterWrap___71-fI {
  display: grid;
  grid-template-rows: 1fr;
  transition: grid-template-rows 0.25s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__paletteFooterWrap___71-fI.styles-module__footerHidden___fJUik {
  grid-template-rows: 0fr;
}

.styles-module__paletteFooterInnerContent___VC26h {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.styles-module__footerHidden___fJUik .styles-module__paletteFooterInnerContent___VC26h {
  opacity: 0;
  transform: translateY(4px);
}

.styles-module__paletteFooterInner___dfylY {
  overflow: hidden;
}

.styles-module__paletteFooter___QYnAG {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
  padding: 0 1rem;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
}
.styles-module__light___ORIft .styles-module__paletteFooter___QYnAG {
  border-top-color: rgba(0, 0, 0, 0.07);
}

.styles-module__paletteFooterCount___D3Fia {
  font-size: 0.8125rem;
  font-weight: 400;
  letter-spacing: -0.0094em;
  color: rgba(255, 255, 255, 0.5);
}
.styles-module__light___ORIft .styles-module__paletteFooterCount___D3Fia {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__paletteFooterClear___ybBoa {
  font-size: 0.8125rem;
  font-weight: 400;
  letter-spacing: -0.0094em;
  color: rgba(255, 255, 255, 0.5);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-family: inherit;
  transition: color 0.15s ease;
}
.styles-module__paletteFooterClear___ybBoa:hover {
  color: rgba(255, 255, 255, 0.7);
}
.styles-module__light___ORIft .styles-module__paletteFooterClear___ybBoa {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___ORIft .styles-module__paletteFooterClear___ybBoa:hover {
  color: rgba(0, 0, 0, 0.6);
}

.styles-module__paletteFooterActions___fLzv8 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.styles-module__rollingWrap___S75jM {
  display: inline-block;
  overflow: hidden;
  height: 1.15em;
  position: relative;
  vertical-align: bottom;
}

.styles-module__rollingNum___1RKDx {
  position: absolute;
  left: 0;
  top: 0;
}

.styles-module__exitUp___AFDRW {
  animation: styles-module__numExitUp___FRQqx 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.styles-module__enterUp___CPlXb {
  animation: styles-module__numEnterUp___2Yd-w 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.styles-module__exitDown___-1yAy {
  animation: styles-module__numExitDown___xm5by 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.styles-module__enterDown___DDuFR {
  animation: styles-module__numEnterDown___hpxBk 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes styles-module__numExitUp___FRQqx {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(-110%);
    opacity: 0;
  }
}
@keyframes styles-module__numEnterUp___2Yd-w {
  from {
    transform: translateY(110%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
@keyframes styles-module__numExitDown___xm5by {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(110%);
    opacity: 0;
  }
}
@keyframes styles-module__numEnterDown___hpxBk {
  from {
    transform: translateY(-110%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.styles-module__rearrangeOverlay___-3R3t {
  position: fixed;
  inset: 0;
  z-index: 99995;
  pointer-events: none;
  cursor: default;
  user-select: none;
  animation: styles-module__overlayFadeIn___aECVy 0.15s ease;
}

.styles-module__hoverHighlight___8eT-v {
  position: fixed;
  pointer-events: none;
  z-index: 99994;
  border: 2px dashed rgba(59, 130, 246, 0.5);
  border-radius: 4px;
  background: rgba(59, 130, 246, 0.06);
  animation: styles-module__highlightFadeIn___Lg7KY 0.12s ease;
}

.styles-module__sectionOutline___s0hy- {
  position: fixed;
  border: 2px solid;
  border-radius: 4px;
  cursor: grab;
}
.styles-module__sectionOutline___s0hy-:active {
  cursor: grabbing;
}
.styles-module__sectionOutline___s0hy- {
  transition: box-shadow 0.15s, border-color 0.3s, background-color 0.3s, border-style 0s;
  user-select: none;
  pointer-events: auto;
  animation: styles-module__sectionEnter___-8BXT 0.2s ease;
}
.styles-module__sectionOutline___s0hy-:hover {
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1), 0 4px 12px rgba(0, 0, 0, 0.15);
}
.styles-module__sectionOutline___s0hy-.styles-module__selected___6yrp6 {
  border-style: solid;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.15);
}
.styles-module__sectionOutline___s0hy-.styles-module__selected___6yrp6:hover {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.15);
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6) {
  border: 1.5px dashed rgba(150, 150, 150, 0.35);
  background-color: transparent !important;
  box-shadow: none;
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6):hover {
  border-color: rgba(150, 150, 150, 0.6);
  box-shadow: none;
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6) .styles-module__sectionLabel___F80HQ {
  opacity: 0;
  transition: opacity 0.15s ease;
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6):hover .styles-module__sectionLabel___F80HQ {
  opacity: 1;
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6) .styles-module__movedBadge___s8z-q,
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6) .styles-module__sectionDimensions___RcJSL {
  opacity: 0;
  transition: opacity 0.15s ease;
}
.styles-module__sectionOutline___s0hy-.styles-module__settled___b5U5o:not(.styles-module__selected___6yrp6):hover .styles-module__sectionDimensions___RcJSL {
  opacity: 1;
}
.styles-module__sectionOutline___s0hy-.styles-module__exiting___YrM8F {
  opacity: 0;
  transform: scale(0.97);
  pointer-events: none;
  animation: none;
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.32, 0.72, 0, 1);
}

.styles-module__sectionLabel___F80HQ {
  position: absolute;
  top: 4px;
  left: 4px;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  max-width: calc(100% - 8px);
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__movedBadge___s8z-q {
  position: absolute;
  bottom: 22px;
  right: 4px;
  font-size: 9px;
  font-weight: 700;
  color: #fff;
  background: #22c55e;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  opacity: 0;
  transform: scale(0.8);
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.styles-module__movedBadge___s8z-q.styles-module__badgeVisible___npbdS {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.2s cubic-bezier(0.34, 1.2, 0.64, 1), transform 0.2s cubic-bezier(0.34, 1.2, 0.64, 1);
}

.styles-module__resizedBadge___u51V8 {
  background: #3c82f7;
  bottom: 40px;
}

.styles-module__sectionDimensions___RcJSL {
  position: absolute;
  bottom: 4px;
  right: 4px;
  font-size: 9px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(0, 0, 0, 0.5);
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.styles-module__light___ORIft .styles-module__sectionDimensions___RcJSL {
  color: rgba(0, 0, 0, 0.5);
  background: rgba(255, 255, 255, 0.7);
}

.styles-module__wireframeNotice___4GJyB {
  position: fixed;
  bottom: 16px;
  left: 24px;
  z-index: 99995;
  font-size: 9.5px;
  font-weight: 400;
  color: rgba(0, 0, 0, 0.4);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  pointer-events: auto;
  animation: styles-module__overlayFadeIn___aECVy 0.3s ease;
  line-height: 1.5;
  max-width: 280px;
}

.styles-module__wireframeOpacityRow___CJXzi {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.styles-module__wireframeOpacityLabel___afkfT {
  font-size: 9px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.32);
  letter-spacing: 0.02em;
  white-space: nowrap;
  user-select: none;
}

.styles-module__wireframeOpacitySlider___YcoEs {
  -webkit-appearance: none;
  appearance: none;
  width: 56px;
  height: 4px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s ease;
}
.styles-module__wireframeOpacitySlider___YcoEs:hover {
  background: rgba(0, 0, 0, 0.13);
}
.styles-module__wireframeOpacitySlider___YcoEs::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f97316;
  cursor: pointer;
  transition: background 0.15s ease;
}
.styles-module__wireframeOpacitySlider___YcoEs::-webkit-slider-thumb:hover {
  background: rgb(224.4209205021, 95.3548117155, 5.7790794979);
}
.styles-module__wireframeOpacitySlider___YcoEs::-moz-range-thumb {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #f97316;
  border: none;
  cursor: pointer;
}
.styles-module__wireframeOpacitySlider___YcoEs::-moz-range-track {
  background: rgba(0, 0, 0, 0.08);
  height: 4px;
  border-radius: 2px;
}

.styles-module__wireframeNoticeTitleRow___PJqyG {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 2px;
}

.styles-module__wireframeNoticeTitle___okr08 {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.55);
}

.styles-module__wireframeNoticeDivider___PNKQ6 {
  width: 1px;
  height: 8px;
  background: rgba(0, 0, 0, 0.12);
  margin: 0 8px;
  flex-shrink: 0;
}

.styles-module__wireframeStartOver___YFk-I {
  font-size: 9.5px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.35);
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  font-family: inherit;
  text-decoration: none;
  transition: color 0.12s ease;
  white-space: nowrap;
}
.styles-module__wireframeStartOver___YFk-I:hover {
  color: rgba(0, 0, 0, 0.6);
}

.styles-module__ghostOutline___po-kO {
  position: fixed;
  border: 1.5px dashed rgba(59, 130, 246, 0.4);
  border-radius: 4px;
  background: rgba(59, 130, 246, 0.04);
  cursor: grab;
  opacity: 0.5;
  user-select: none;
  pointer-events: auto;
  animation: styles-module__ghostEnter___EC3Mb 0.25s ease;
  transition: box-shadow 0.15s, border-color 0.3s, opacity 0.25s;
}
.styles-module__ghostOutline___po-kO:active {
  cursor: grabbing;
}
.styles-module__ghostOutline___po-kO:hover {
  opacity: 0.7;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.1), 0 4px 12px rgba(0, 0, 0, 0.08);
}
.styles-module__ghostOutline___po-kO.styles-module__selected___6yrp6 {
  opacity: 1;
  border-style: solid;
  border-width: 2px;
  border-color: #3c82f7;
  background: rgba(59, 130, 246, 0.08);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.15);
}
.styles-module__ghostOutline___po-kO.styles-module__exiting___YrM8F {
  opacity: 0;
  transform: scale(0.97);
  pointer-events: none;
  animation: none;
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.32, 0.72, 0, 1);
}

.styles-module__ghostBadge___tsQUK {
  position: absolute;
  bottom: calc(100% + 4px);
  left: -1px;
  font-size: 9px;
  font-weight: 600;
  color: rgba(59, 130, 246, 0.9);
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  letter-spacing: 0.02em;
  line-height: 1.2;
  animation: styles-module__badgeSlideIn___typJ7 0.2s ease both;
}

@keyframes styles-module__badgeSlideIn___typJ7 {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.styles-module__ghostBadgeExtra___6CVoD {
  display: inline;
  animation: styles-module__badgeExtraIn___i4W8F 0.2s ease both;
}

@keyframes styles-module__badgeExtraIn___i4W8F {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.styles-module__originalOutline___Y6DD1 {
  position: fixed;
  border: 1.5px dashed rgba(150, 150, 150, 0.3);
  border-radius: 4px;
  background: transparent;
  pointer-events: none;
  user-select: none;
  animation: styles-module__sectionEnter___-8BXT 0.2s ease;
}

.styles-module__originalLabel___HqI9g {
  position: absolute;
  top: 4px;
  left: 4px;
  font-size: 9px;
  font-weight: 500;
  color: rgba(150, 150, 150, 0.5);
  padding: 1px 6px;
  border-radius: 3px;
  white-space: nowrap;
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: rgba(150, 150, 150, 0.08);
}

.styles-module__connectorSvg___Lovld {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 99996;
}

.styles-module__connectorLine___XeWh- {
  transition: opacity 0.2s ease;
  animation: styles-module__connectorDraw___8sK5I 0.3s ease both;
}

.styles-module__connectorDot___yvf7C {
  transform-box: fill-box;
  transform-origin: center;
  animation: styles-module__connectorDotIn___NwTUq 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s both;
}

@keyframes styles-module__connectorDraw___8sK5I {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes styles-module__connectorDotIn___NwTUq {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
.styles-module__connectorExiting___2lLOs {
  animation: styles-module__connectorOut___5QoPl 0.2s ease forwards;
}
.styles-module__connectorExiting___2lLOs .styles-module__connectorDot___yvf7C {
  animation: styles-module__connectorDotOut___FEq7e 0.2s ease forwards;
}

@keyframes styles-module__connectorOut___5QoPl {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@keyframes styles-module__connectorDotOut___FEq7e {
  from {
    transform: scale(1);
    opacity: 1;
  }
  to {
    transform: scale(0);
    opacity: 0;
  }
}
@keyframes styles-module__placementEnter___TdRhf {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__sectionEnter___-8BXT {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__highlightFadeIn___Lg7KY {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes styles-module__overlayFadeIn___aECVy {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes styles-module__ghostEnter___EC3Mb {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 0.6;
    transform: scale(1);
  }
}`,Kx={overlayExiting:"styles-module__overlayExiting___iEmYr",overlay:"styles-module__overlay___aWh-q",overlayFadeIn:"styles-module__overlayFadeIn___aECVy",light:"styles-module__light___ORIft",wireframe:"styles-module__wireframe___itvQU",placing:"styles-module__placing___45yD8",passthrough:"styles-module__passthrough___xaFeE",blankCanvas:"styles-module__blankCanvas___t2Eue",visible:"styles-module__visible___OKKqX",gridActive:"styles-module__gridActive___OZ-cf",paletteHeader:"styles-module__paletteHeader___-Q5gQ",paletteHeaderTitle:"styles-module__paletteHeaderTitle___oHqZC",paletteHeaderDesc:"styles-module__paletteHeaderDesc___6i74T",wireframePurposeWrap:"styles-module__wireframePurposeWrap___To-tS",collapsed:"styles-module__collapsed___Ms9vS",wireframePurposeInner:"styles-module__wireframePurposeInner___Lrahs",wireframePurposeInput:"styles-module__wireframePurposeInput___7EtBN",canvasToggle:"styles-module__canvasToggle___-QqSy",active:"styles-module__active___hosp7",canvasToggleIcon:"styles-module__canvasToggleIcon___7pJ82",canvasToggleLabel:"styles-module__canvasToggleLabel___OanpY",canvasPurposeWrap:"styles-module__canvasPurposeWrap___hj6zk",canvasPurposeInner:"styles-module__canvasPurposeInner___VWiyu",canvasPurposeToggle:"styles-module__canvasPurposeToggle___byDH2",canvasPurposeCheck:"styles-module__canvasPurposeCheck___xqd7l",checked:"styles-module__checked___-1JGH",canvasPurposeLabel:"styles-module__canvasPurposeLabel___Zu-tD",canvasPurposeHelp:"styles-module__canvasPurposeHelp___jijwR",placement:"styles-module__placement___zcxv8",placementEnter:"styles-module__placementEnter___TdRhf",selected:"styles-module__selected___6yrp6",dragging:"styles-module__dragging___le6KZ",exiting:"styles-module__exiting___YrM8F",placementContent:"styles-module__placementContent___f64A4",placementLabel:"styles-module__placementLabel___0KvWl",placementAnnotation:"styles-module__placementAnnotation___78pTr",annotationVisible:"styles-module__annotationVisible___mrUyA",sectionAnnotation:"styles-module__sectionAnnotation___aUIs0",handle:"styles-module__handle___Ikbxm",sectionOutline:"styles-module__sectionOutline___s0hy-",ghostOutline:"styles-module__ghostOutline___po-kO",handleNw:"styles-module__handleNw___4TMIj",handleNe:"styles-module__handleNe___mnsTh",handleSe:"styles-module__handleSe___oSFnk",handleSw:"styles-module__handleSw___pi--Z",handleN:"styles-module__handleN___aBA-Q",handleE:"styles-module__handleE___0hM5u",handleS:"styles-module__handleS___JjDRv",handleW:"styles-module__handleW___ERWGQ",edgeHandle:"styles-module__edgeHandle___XxXdT",edgeN:"styles-module__edgeN___-JJDj",edgeS:"styles-module__edgeS___66lMX",edgeE:"styles-module__edgeE___1bGDa",edgeW:"styles-module__edgeW___lHQNo",deleteButton:"styles-module__deleteButton___LkGCb",rearrangeOverlay:"styles-module__rearrangeOverlay___-3R3t",drawBox:"styles-module__drawBox___BrVAa",selectBox:"styles-module__selectBox___Iu8kB",sizeIndicator:"styles-module__sizeIndicator___7zJ4y",guideLine:"styles-module__guideLine___DUQY2",dragPreview:"styles-module__dragPreview___onPbU",dragPreviewWireframe:"styles-module__dragPreviewWireframe___jsg0G",palette:"styles-module__palette___C7iSH",paletteItem:"styles-module__paletteItem___6TlnA",paletteItemLabel:"styles-module__paletteItemLabel___6ncO4",paletteSectionTitle:"styles-module__paletteSectionTitle___PqnjX",paletteFooter:"styles-module__paletteFooter___QYnAG",enter:"styles-module__enter___6LYk5",exit:"styles-module__exit___iSGRw",paletteSection:"styles-module__paletteSection___V8DEA",paletteItemIcon:"styles-module__paletteItemIcon___0NPQK",placeScroll:"styles-module__placeScroll___7sClM",fadeTop:"styles-module__fadeTop___KT9tF",fadeBottom:"styles-module__fadeBottom___x3ShT",paletteFooterWrap:"styles-module__paletteFooterWrap___71-fI",footerHidden:"styles-module__footerHidden___fJUik",paletteFooterInnerContent:"styles-module__paletteFooterInnerContent___VC26h",paletteFooterInner:"styles-module__paletteFooterInner___dfylY",paletteFooterCount:"styles-module__paletteFooterCount___D3Fia",paletteFooterClear:"styles-module__paletteFooterClear___ybBoa",paletteFooterActions:"styles-module__paletteFooterActions___fLzv8",rollingWrap:"styles-module__rollingWrap___S75jM",rollingNum:"styles-module__rollingNum___1RKDx",exitUp:"styles-module__exitUp___AFDRW",numExitUp:"styles-module__numExitUp___FRQqx",enterUp:"styles-module__enterUp___CPlXb",numEnterUp:"styles-module__numEnterUp___2Yd-w",exitDown:"styles-module__exitDown___-1yAy",numExitDown:"styles-module__numExitDown___xm5by",enterDown:"styles-module__enterDown___DDuFR",numEnterDown:"styles-module__numEnterDown___hpxBk",hoverHighlight:"styles-module__hoverHighlight___8eT-v",highlightFadeIn:"styles-module__highlightFadeIn___Lg7KY",sectionEnter:"styles-module__sectionEnter___-8BXT",settled:"styles-module__settled___b5U5o",sectionLabel:"styles-module__sectionLabel___F80HQ",movedBadge:"styles-module__movedBadge___s8z-q",sectionDimensions:"styles-module__sectionDimensions___RcJSL",badgeVisible:"styles-module__badgeVisible___npbdS",resizedBadge:"styles-module__resizedBadge___u51V8",wireframeNotice:"styles-module__wireframeNotice___4GJyB",wireframeOpacityRow:"styles-module__wireframeOpacityRow___CJXzi",wireframeOpacityLabel:"styles-module__wireframeOpacityLabel___afkfT",wireframeOpacitySlider:"styles-module__wireframeOpacitySlider___YcoEs",wireframeNoticeTitleRow:"styles-module__wireframeNoticeTitleRow___PJqyG",wireframeNoticeTitle:"styles-module__wireframeNoticeTitle___okr08",wireframeNoticeDivider:"styles-module__wireframeNoticeDivider___PNKQ6",wireframeStartOver:"styles-module__wireframeStartOver___YFk-I",ghostEnter:"styles-module__ghostEnter___EC3Mb",ghostBadge:"styles-module__ghostBadge___tsQUK",badgeSlideIn:"styles-module__badgeSlideIn___typJ7",ghostBadgeExtra:"styles-module__ghostBadgeExtra___6CVoD",badgeExtraIn:"styles-module__badgeExtraIn___i4W8F",originalOutline:"styles-module__originalOutline___Y6DD1",originalLabel:"styles-module__originalLabel___HqI9g",connectorSvg:"styles-module__connectorSvg___Lovld",connectorLine:"styles-module__connectorLine___XeWh-",connectorDraw:"styles-module__connectorDraw___8sK5I",connectorDot:"styles-module__connectorDot___yvf7C",connectorDotIn:"styles-module__connectorDotIn___NwTUq",connectorExiting:"styles-module__connectorExiting___2lLOs",connectorOut:"styles-module__connectorOut___5QoPl",connectorDotOut:"styles-module__connectorDotOut___FEq7e"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-design-mode-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-design-mode-styles",document.head.appendChild(e)),e.textContent=Zx}var R=Kx,bi=24,Hc=5;function Gg(e,t,n,l,o){let a=1/0,i=1/0,s=e.x,r=e.x+e.width,p=e.x+e.width/2,f=e.y,b=e.y+e.height,_=e.y+e.height/2,w=!l,C=w?[s,r,p]:[...l.left?[s]:[],...l.right?[r]:[]],z=w?[f,b,_]:[...l.top?[f]:[],...l.bottom?[b]:[]],D=[];for(let he of t)n.has(he.id)||D.push(he);o&&D.push(...o);for(let he of D){let et=he.x,ft=he.x+he.width,Re=he.x+he.width/2,Ie=he.y,Ee=he.y+he.height,Pe=he.y+he.height/2;for(let W of C)for(let ge of[et,ft,Re]){let Ze=ge-W;Math.abs(Ze)<Hc&&Math.abs(Ze)<Math.abs(a)&&(a=Ze)}for(let W of z)for(let ge of[Ie,Ee,Pe]){let Ze=ge-W;Math.abs(Ze)<Hc&&Math.abs(Ze)<Math.abs(i)&&(i=Ze)}}let h=Math.abs(a)<Hc?a:0,y=Math.abs(i)<Hc?i:0,k=[],E=new Set,Q=s+h,oe=r+h,L=p+h,K=f+y,ee=b+y,F=_+y;for(let he of D){let et=he.x,ft=he.x+he.width,Re=he.x+he.width/2,Ie=he.y,Ee=he.y+he.height,Pe=he.y+he.height/2;for(let W of[et,Re,ft])for(let ge of[Q,L,oe])if(Math.abs(ge-W)<.5){let Ze=`x:${Math.round(W)}`;E.has(Ze)||(E.add(Ze),k.push({axis:"x",pos:W}))}for(let W of[Ie,Pe,Ee])for(let ge of[K,F,ee])if(Math.abs(ge-W)<.5){let Ze=`y:${Math.round(W)}`;E.has(Ze)||(E.add(Ze),k.push({axis:"y",pos:W}))}}return{dx:h,dy:y,guides:k}}function Vg(){return`dp-${Date.now()}-${Math.random().toString(36).slice(2,7)}`}function Fx({placements:e,onChange:t,activeComponent:n,onActiveComponentChange:l,isDarkMode:o,exiting:a,onInteractionChange:i,className:s,passthrough:r,extraSnapRects:p,onSelectionChange:f,deselectSignal:b,onDragMove:_,onDragEnd:w,clearSignal:C,wireframe:z}){let[D,h]=(0,Je.useState)(new Set),[y,k]=(0,Je.useState)(null),[E,Q]=(0,Je.useState)(null),[oe,L]=(0,Je.useState)(null),[K,ee]=(0,Je.useState)([]),[F,he]=(0,Je.useState)(null),[et,ft]=(0,Je.useState)(!1),Re=(0,Je.useRef)(!1),[Ie,Ee]=(0,Je.useState)(new Set),Pe=(0,Je.useRef)(new Map),W=(0,Je.useRef)(null),ge=(0,Je.useRef)(null),Ze=(0,Je.useRef)(e);Ze.current=e;let Bt=(0,Je.useRef)(f);Bt.current=f;let vn=(0,Je.useRef)(_);vn.current=_;let hn=(0,Je.useRef)(w);hn.current=w;let oo=(0,Je.useRef)(b);(0,Je.useEffect)(()=>{b!==oo.current&&(oo.current=b,h(new Set))},[b]);let In=(0,Je.useRef)(C);(0,Je.useEffect)(()=>{if(C!==void 0&&C!==In.current){In.current=C;let I=new Set(Ze.current.map(de=>de.id));I.size>0&&(Ee(I),h(new Set),ge.current=null,fe(()=>{t([]),Ee(new Set)},180))}},[C,t]),(0,Je.useEffect)(()=>{let I=de=>{let pe=de.target;if(!(pe.tagName==="INPUT"||pe.tagName==="TEXTAREA"||pe.isContentEditable)){if((de.key==="Backspace"||de.key==="Delete")&&D.size>0){de.preventDefault();let be=new Set(D);Ee(be),h(new Set),fe(()=>{t(Ze.current.filter(tt=>!be.has(tt.id))),Ee(new Set)},180);return}if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(de.key)&&D.size>0){de.preventDefault();let be=de.shiftKey?20:1,tt=de.key==="ArrowLeft"?-be:de.key==="ArrowRight"?be:0,it=de.key==="ArrowUp"?-be:de.key==="ArrowDown"?be:0;t(e.map(Ke=>D.has(Ke.id)?{...Ke,x:Math.max(0,Ke.x+tt),y:Math.max(0,Ke.y+it)}:Ke));return}if(de.key==="Escape"){n?l(null):D.size>0&&h(new Set);return}}};return document.addEventListener("keydown",I),()=>document.removeEventListener("keydown",I)},[D,n,e,t,l]);let ao=(0,Je.useCallback)(I=>{if(I.button!==0||r||I.target.closest(`.${R.placement}`))return;I.preventDefault(),I.stopPropagation();let pe=window.scrollY,Ae=I.clientX,be=I.clientY;if(n){ge.current="place",i?.(!0);let tt=!1,it=Ae,Ke=be,Ue=M=>{it=M.clientX,Ke=M.clientY;let N=Math.abs(it-Ae),$=Math.abs(Ke-be);if((N>5||$>5)&&(tt=!0),tt){let U=Math.min(Ae,it),J=Math.min(be,Ke),ae=Math.abs(it-Ae),X=Math.abs(Ke-be);k({x:U,y:J,w:ae,h:X}),L({x:M.clientX+12,y:M.clientY+12,text:`${Math.round(ae)} \xD7 ${Math.round(X)}`})}},me=M=>{window.removeEventListener("mousemove",Ue),window.removeEventListener("mouseup",me),k(null),L(null),ge.current=null,i?.(!1);let N=P[n],$,U,J,ae;tt?($=Math.min(Ae,it),U=Math.min(be,Ke)+pe,J=Math.max(bi,Math.abs(it-Ae)),ae=Math.max(bi,Math.abs(Ke-be))):(J=N.width,ae=N.height,$=Ae-J/2,U=be+pe-ae/2),$=Math.max(0,$),U=Math.max(0,U);let X={id:Vg(),type:n,x:$,y:U,width:J,height:ae,scrollY:pe,timestamp:Date.now()},ie=[...e,X];t(ie),h(new Set([X.id])),l(null)};window.addEventListener("mousemove",Ue),window.addEventListener("mouseup",me)}else{I.shiftKey||h(new Set),ge.current="select";let tt=!1,it=Ue=>{let me=Math.abs(Ue.clientX-Ae),M=Math.abs(Ue.clientY-be);if((me>4||M>4)&&(tt=!0),tt){let N=Math.min(Ae,Ue.clientX),$=Math.min(be,Ue.clientY);Q({x:N,y:$,w:Math.abs(Ue.clientX-Ae),h:Math.abs(Ue.clientY-be)})}},Ke=Ue=>{if(window.removeEventListener("mousemove",it),window.removeEventListener("mouseup",Ke),ge.current=null,tt){let me=Math.min(Ae,Ue.clientX),M=Math.min(be,Ue.clientY)+pe,N=Math.abs(Ue.clientX-Ae),$=Math.abs(Ue.clientY-be),U=new Set(I.shiftKey?D:new Set);for(let J of e){let ae=J.y-pe;J.x+J.width>me&&J.x<me+N&&J.y+J.height>M&&J.y<M+$&&U.add(J.id)}h(U)}Q(null)};window.addEventListener("mousemove",it),window.addEventListener("mouseup",Ke)}},[n,r,e,t,D]),il=(0,Je.useCallback)((I,de)=>{if(I.button!==0)return;let pe=I.target;if(pe.closest(`.${R.handle}`)||pe.closest(`.${R.deleteButton}`))return;I.preventDefault(),I.stopPropagation();let Ae;I.shiftKey?(Ae=new Set(D),Ae.has(de)?Ae.delete(de):Ae.add(de)):D.has(de)?Ae=new Set(D):Ae=new Set([de]),h(Ae),(Ae.size!==D.size||[...Ae].some(ie=>!D.has(ie)))&&Bt.current?.(Ae,I.shiftKey);let tt=window.scrollY,it=I.clientX,Ke=I.clientY,Ue=new Map;for(let ie of e)Ae.has(ie.id)&&Ue.set(ie.id,{x:ie.x,y:ie.y});ge.current="move",i?.(!0);let me=!1,M=!1,N=e,$=0,U=0,J=new Map;for(let ie of e)Ue.has(ie.id)&&J.set(ie.id,{w:ie.width,h:ie.height});let ae=ie=>{let Ce=ie.clientX-it,qe=ie.clientY-Ke;if((Math.abs(Ce)>2||Math.abs(qe)>2)&&(me=!0),!me)return;if(ie.altKey&&!M){M=!0;let xe=[];for(let vt of e)Ue.has(vt.id)&&xe.push({...vt,id:Vg(),timestamp:Date.now()});N=[...e,...xe]}let nt=1/0,se=1/0,st=-1/0,Oe=-1/0;for(let[xe,vt]of Ue){let tn=J.get(xe);tn&&(nt=Math.min(nt,vt.x+Ce),se=Math.min(se,vt.y+qe),st=Math.max(st,vt.x+Ce+tn.w),Oe=Math.max(Oe,vt.y+qe+tn.h))}let Te={x:nt,y:se,width:st-nt,height:Oe-se},{dx:re,dy:rt,guides:Ge}=Gg(Te,N,new Set(Ue.keys()),void 0,p);ee(Ge);let De=Ce+re,Fe=qe+rt;$=De,U=Fe,t(N.map(xe=>{let vt=Ue.get(xe.id);return vt?{...xe,x:Math.max(0,vt.x+De),y:Math.max(0,vt.y+Fe)}:xe})),vn.current?.(De,Fe)},X=()=>{window.removeEventListener("mousemove",ae),window.removeEventListener("mouseup",X),ge.current=null,i?.(!1),ee([]),hn.current?.($,U,me)};window.addEventListener("mousemove",ae),window.addEventListener("mouseup",X)},[D,e,t,i]),Rl=(0,Je.useCallback)((I,de,pe)=>{I.preventDefault(),I.stopPropagation();let Ae=e.find(U=>U.id===de);if(!Ae)return;h(new Set([de])),ge.current="resize",i?.(!0);let be=I.clientX,tt=I.clientY,it=Ae.width,Ke=Ae.height,Ue=Ae.x,me=Ae.y,M={left:pe.includes("w"),right:pe.includes("e"),top:pe.includes("n"),bottom:pe.includes("s")},N=U=>{let J=U.clientX-be,ae=U.clientY-tt,X=it,ie=Ke,Ce=Ue,qe=me;pe.includes("e")&&(X=Math.max(bi,it+J)),pe.includes("w")&&(X=Math.max(bi,it-J),Ce=Ue+it-X),pe.includes("s")&&(ie=Math.max(bi,Ke+ae)),pe.includes("n")&&(ie=Math.max(bi,Ke-ae),qe=me+Ke-ie);let nt={x:Ce,y:qe,width:X,height:ie},{dx:se,dy:st,guides:Oe}=Gg(nt,Ze.current,new Set([de]),M,p);ee(Oe),se!==0&&(M.right?X+=se:M.left&&(Ce+=se,X-=se)),st!==0&&(M.bottom?ie+=st:M.top&&(qe+=st,ie-=st)),t(Ze.current.map(Te=>Te.id===de?{...Te,x:Ce,y:qe,width:X,height:ie}:Te)),L({x:U.clientX+12,y:U.clientY+12,text:`${Math.round(X)} \xD7 ${Math.round(ie)}`})},$=()=>{window.removeEventListener("mousemove",N),window.removeEventListener("mouseup",$),L(null),ge.current=null,i?.(!1),ee([])};window.addEventListener("mousemove",N),window.addEventListener("mouseup",$)},[e,t,i]),io=(0,Je.useCallback)(I=>{ge.current=null,Ee(de=>{let pe=new Set(de);return pe.add(I),pe}),h(de=>{let pe=new Set(de);return pe.delete(I),pe}),fe(()=>{t(Ze.current.filter(de=>de.id!==I)),Ee(de=>{let pe=new Set(de);return pe.delete(I),pe})},180)},[t]),Uo=new Set(["text","hero","button","badge","cta","toast","modal","card","navigation","tabs","input","search","breadcrumb","pricing","testimonial","alert","banner","tag","notification","stat","productCard"]),zn={hero:"Headline text",button:"Button label",badge:"Badge label",cta:"Call to action text",toast:"Notification message",modal:"Dialog title",card:"Card title",navigation:"Brand / nav items",tabs:"Tab labels",input:"Placeholder text",search:"Search placeholder",pricing:"Plan name or price",testimonial:"Quote text",alert:"Alert message",banner:"Banner text",tag:"Tag label",notification:"Notification message",stat:"Metric value",productCard:"Product name"},sl=(0,Je.useCallback)(I=>{let de=e.find(pe=>pe.id===I);de&&(Re.current=!!de.text,he(I),ft(!1))},[e]),wn=(0,Je.useCallback)(()=>{F&&(ft(!0),fe(()=>{he(null),ft(!1)},150))},[F]);(0,Je.useEffect)(()=>{a&&F&&wn()},[a]);let yl=(0,Je.useCallback)(I=>{F&&(t(e.map(de=>de.id===F?{...de,text:I.trim()||void 0}:de)),wn())},[F,e,t,wn]),pl=typeof window<"u"?window.scrollY:0,ba=["nw","ne","se","sw"],rl=z?"#f97316":"#3c82f7",Be=[{dir:"n",cls:R.edgeN,arrow:(0,xt.jsx)("svg",{width:"8",height:"6",viewBox:"0 0 8 6",fill:"none",children:(0,xt.jsx)("path",{d:"M4 0.5L1 4.5h6z",fill:rl})})},{dir:"e",cls:R.edgeE,arrow:(0,xt.jsx)("svg",{width:"6",height:"8",viewBox:"0 0 6 8",fill:"none",children:(0,xt.jsx)("path",{d:"M5.5 4L1.5 1v6z",fill:rl})})},{dir:"s",cls:R.edgeS,arrow:(0,xt.jsx)("svg",{width:"8",height:"6",viewBox:"0 0 8 6",fill:"none",children:(0,xt.jsx)("path",{d:"M4 5.5L1 1.5h6z",fill:rl})})},{dir:"w",cls:R.edgeW,arrow:(0,xt.jsx)("svg",{width:"6",height:"8",viewBox:"0 0 6 8",fill:"none",children:(0,xt.jsx)("path",{d:"M0.5 4L4.5 1v6z",fill:rl})})}];return(0,xt.jsxs)(xt.Fragment,{children:[(0,xt.jsx)("div",{ref:W,className:`${R.overlay} ${o?"":R.light} ${n?R.placing:""} ${r?R.passthrough:""} ${a?R.overlayExiting:""} ${z?R.wireframe:""}${s?` ${s}`:""}`,"data-feedback-toolbar":!0,onMouseDown:ao,children:e.map(I=>{let de=D.has(I.id),pe=gl[I.type]?.label||I.type,Ae=I.y-pl;return(0,xt.jsxs)("div",{"data-design-placement":I.id,className:`${R.placement} ${de?R.selected:""} ${Ie.has(I.id)?R.exiting:""}`,style:{left:I.x,top:Ae,width:I.width,height:I.height,position:"fixed"},onMouseDown:be=>il(be,I.id),onDoubleClick:()=>sl(I.id),children:[(0,xt.jsx)("span",{className:R.placementLabel,children:pe}),(0,xt.jsx)("span",{className:`${R.placementAnnotation} ${I.text?R.annotationVisible:""}`,children:(I.text&&Pe.current.set(I.id,I.text),I.text||Pe.current.get(I.id)||"")}),(0,xt.jsx)("div",{className:R.placementContent,children:(0,xt.jsx)(Vx,{type:I.type,width:I.width,height:I.height,text:I.text})}),(0,xt.jsx)("div",{className:R.deleteButton,onMouseDown:be=>be.stopPropagation(),onClick:()=>io(I.id),children:"\u2715"}),ba.map(be=>(0,xt.jsx)("div",{className:`${R.handle} ${R[`handle${be.charAt(0).toUpperCase()}${be.slice(1)}`]}`,onMouseDown:tt=>Rl(tt,I.id,be)},be)),Be.map(({dir:be,cls:tt,arrow:it})=>(0,xt.jsx)("div",{className:`${R.edgeHandle} ${tt}`,onMouseDown:Ke=>Rl(Ke,I.id,be),children:it},be))]},I.id)})}),F&&(()=>{let I=e.find(me=>me.id===F);if(!I)return null;let de=I.y-pl,pe=I.x+I.width/2,Ae=de-8,be=de+I.height+8,tt=Ae>200,it=be<window.innerHeight-100,Ke=Math.max(160,Math.min(window.innerWidth-160,pe)),Ue;return tt?Ue={left:Ke,bottom:window.innerHeight-Ae}:it?Ue={left:Ke,top:be}:Ue={left:Ke,top:Math.max(80,window.innerHeight/2-80)},(0,xt.jsx)(Kc,{element:gl[I.type]?.label||I.type,placeholder:zn[I.type]||"Label or content text",initialValue:I.text??"",submitLabel:Re.current?"Save":"Set",onSubmit:yl,onCancel:wn,onDelete:Re.current?()=>{yl("")}:void 0,isExiting:et,lightMode:!o,style:Ue})})(),y&&(0,xt.jsx)("div",{className:R.drawBox,style:{left:y.x,top:y.y,width:y.w,height:y.h},"data-feedback-toolbar":!0}),E&&(0,xt.jsx)("div",{className:R.selectBox,style:{left:E.x,top:E.y,width:E.w,height:E.h},"data-feedback-toolbar":!0}),oe&&(0,xt.jsx)("div",{className:R.sizeIndicator,style:{left:oe.x,top:oe.y},"data-feedback-toolbar":!0,children:oe.text}),K.map((I,de)=>(0,xt.jsx)("div",{className:R.guideLine,style:I.axis==="x"?{position:"fixed",left:I.pos,top:0,width:1,bottom:0}:{position:"fixed",left:0,top:I.pos-pl,right:0,height:1},"data-feedback-toolbar":!0},`${I.axis}-${I.pos}-${de}`))]})}function Jx(e){if(!e)return"";let t=e.scrollTop>2,n=e.scrollTop+e.clientHeight<e.scrollHeight-2;return`${t?R.fadeTop:""} ${n?R.fadeBottom:""}`}var m="currentColor",A="0.5";function Px({type:e}){switch(e){case"navigation":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"4",width:"18",height:"8",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2.5",y:"7",width:"3",height:"1.5",rx:".5",fill:m,opacity:".4"}),(0,c.jsx)("rect",{x:"7",y:"7",width:"2.5",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"11",y:"7",width:"2.5",height:"1.5",rx:".5",fill:m,opacity:".25"})]});case"header":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"2",width:"18",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3",y:"5.5",width:"8",height:"2",rx:".5",fill:m,opacity:".35"}),(0,c.jsx)("rect",{x:"3",y:"9",width:"12",height:"1",rx:".5",fill:m,opacity:".15"})]});case"hero":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"1",width:"18",height:"14",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"5",width:"10",height:"1.5",rx:".5",fill:m,opacity:".35"}),(0,c.jsx)("rect",{x:"7",y:"8",width:"6",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"7.5",y:"10.5",width:"5",height:"2.5",rx:"1",stroke:m,strokeWidth:A})]});case"section":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"1",width:"18",height:"14",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3",y:"4",width:"6",height:"1",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"3",y:"6.5",width:"14",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"3",y:"9",width:"10",height:"1",rx:".5",fill:m,opacity:".15"})]});case"sidebar":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"1",width:"7",height:"14",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2.5",y:"4",width:"4",height:"1",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"2.5",y:"6.5",width:"3.5",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"2.5",y:"9",width:"4",height:"1",rx:".5",fill:m,opacity:".15"})]});case"footer":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"7",width:"18",height:"8",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3",y:"9.5",width:"4",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"9.5",width:"4",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"15",y:"9.5",width:"3",height:"1",rx:".5",fill:m,opacity:".2"})]});case"modal":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"2",width:"14",height:"12",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"4.5",width:"7",height:"1",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"5",y:"7",width:"10",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"11",y:"11",width:"5",height:"2",rx:".75",stroke:m,strokeWidth:A})]});case"divider":return(0,c.jsx)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:(0,c.jsx)("line",{x1:"2",y1:"8",x2:"18",y2:"8",stroke:m,strokeWidth:"0.5",opacity:".3"})});case"card":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"5.5",rx:"1",fill:m,opacity:".04"}),(0,c.jsx)("rect",{x:"4",y:"8.5",width:"8",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"4",y:"11",width:"11",height:"1",rx:".5",fill:m,opacity:".12"})]});case"text":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"4",width:"14",height:"1.5",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"2",y:"7",width:"11",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"2",y:"9.5",width:"13",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"2",y:"12",width:"8",height:"1",rx:".5",fill:m,opacity:".12"})]});case"image":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"2",y1:"2",x2:"18",y2:"14",stroke:m,strokeWidth:".3",opacity:".25"}),(0,c.jsx)("line",{x1:"18",y1:"2",x2:"2",y2:"14",stroke:m,strokeWidth:".3",opacity:".25"})]});case"video":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M8.5 5.5v5l4.5-2.5z",stroke:m,strokeWidth:A,fill:m,opacity:".15"})]});case"table":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"2",width:"18",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"1",y1:"5.5",x2:"19",y2:"5.5",stroke:m,strokeWidth:".3",opacity:".25"}),(0,c.jsx)("line",{x1:"1",y1:"9",x2:"19",y2:"9",stroke:m,strokeWidth:".3",opacity:".25"}),(0,c.jsx)("line",{x1:"7",y1:"2",x2:"7",y2:"14",stroke:m,strokeWidth:".3",opacity:".25"}),(0,c.jsx)("line",{x1:"13",y1:"2",x2:"13",y2:"14",stroke:m,strokeWidth:".3",opacity:".25"})]});case"grid":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1.5",y:"2",width:"7",height:"5.5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"11.5",y:"2",width:"7",height:"5.5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"1.5",y:"9.5",width:"7",height:"5.5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"11.5",y:"9.5",width:"7",height:"5.5",rx:"1",stroke:m,strokeWidth:A})]});case"list":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"3.5",cy:"4.5",r:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"4",width:"10",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"3.5",cy:"8",r:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"7.5",width:"8",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"3.5",cy:"11.5",r:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"11",width:"11",height:"1",rx:".5",fill:m,opacity:".2"})]});case"chart":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"9",width:"2.5",height:"4",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"7",y:"6",width:"2.5",height:"7",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"11",y:"3",width:"2.5",height:"10",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"15",y:"5",width:"2.5",height:"8",rx:".5",fill:m,opacity:".2"})]});case"accordion":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1.5",y:"2",width:"17",height:"4",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3",y:"3.5",width:"6",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"1.5",y:"7.5",width:"17",height:"3",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"1.5",y:"12",width:"17",height:"3",rx:"1",stroke:m,strokeWidth:A})]});case"carousel":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"2",width:"14",height:"10",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M1.5 7L3 8.5 1.5 10",stroke:m,strokeWidth:A,opacity:".35"}),(0,c.jsx)("path",{d:"M18.5 7L17 8.5 18.5 10",stroke:m,strokeWidth:A,opacity:".35"}),(0,c.jsx)("circle",{cx:"8.5",cy:"14",r:".6",fill:m,opacity:".35"}),(0,c.jsx)("circle",{cx:"10",cy:"14",r:".6",fill:m,opacity:".15"}),(0,c.jsx)("circle",{cx:"11.5",cy:"14",r:".6",fill:m,opacity:".15"})]});case"button":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"5",width:"14",height:"6",rx:"2",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"7.5",width:"7",height:"1",rx:".5",fill:m,opacity:".25"})]});case"input":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"4",width:"5.5",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"2",y:"6.5",width:"16",height:"5.5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3.5",y:"8.5",width:"7",height:"1",rx:".5",fill:m,opacity:".12"})]});case"search":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"4.5",width:"16",height:"7",rx:"3.5",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"6",cy:"8",r:"2",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("line",{x1:"7.5",y1:"9.5",x2:"9",y2:"11",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("rect",{x:"9.5",y:"7.5",width:"6",height:"1",rx:".5",fill:m,opacity:".12"})]});case"form":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1.5",width:"5.5",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"2",y:"3.5",width:"16",height:"3",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2",y:"8",width:"7",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"2",y:"10",width:"16",height:"3",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"12",y:"14",width:"6",height:"2",rx:".75",stroke:m,strokeWidth:A})]});case"tabs":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"5",width:"18",height:"10",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"1",y:"2",width:"6",height:"3.5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2.5",y:"3.25",width:"3",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"7",y:"2",width:"6",height:"3.5",rx:".75",stroke:m,strokeWidth:A})]});case"dropdown":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"4",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3.5",y:"3.5",width:"7",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("path",{d:"M15 3.5l1.5 1.5L18 3.5",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("rect",{x:"2",y:"7",width:"16",height:"7",rx:"1",stroke:m,strokeWidth:A,strokeDasharray:"2 1",opacity:".3"})]});case"toggle":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"4",y:"5",width:"12",height:"6",rx:"3",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"13",cy:"8",r:"2",fill:m,opacity:".3"})]});case"avatar":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"10",cy:"8",r:"6",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"10",cy:"6.5",r:"2",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M6.5 13c0-2 1.5-3.5 3.5-3.5s3.5 1.5 3.5 3.5",stroke:m,strokeWidth:A})]});case"badge":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"5",width:"14",height:"6",rx:"3",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6",y:"7.5",width:"8",height:"1",rx:".5",fill:m,opacity:".25"})]});case"breadcrumb":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1.5",y:"7",width:"3.5",height:"1",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("path",{d:"M6.5 7l1 1-1 1",stroke:m,strokeWidth:A,opacity:".2"}),(0,c.jsx)("rect",{x:"9",y:"7",width:"3.5",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("path",{d:"M14 7l1 1-1 1",stroke:m,strokeWidth:A,opacity:".2"}),(0,c.jsx)("rect",{x:"16.5",y:"7",width:"2",height:"1",rx:".5",fill:m,opacity:".15"})]});case"pagination":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"5.5",width:"3.5",height:"5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"5.5",width:"3.5",height:"5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"11",y:"5.5",width:"3.5",height:"5",rx:"1",fill:m,opacity:".15",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"15.5",y:"5.5",width:"3.5",height:"5",rx:"1",stroke:m,strokeWidth:A})]});case"progress":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"7",width:"16",height:"2",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2",y:"7",width:"10",height:"2",rx:"1",fill:m,opacity:".2"})]});case"toast":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"4",width:"16",height:"8",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"5",cy:"8",r:"1.5",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("rect",{x:"8",y:"6.5",width:"7",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"8",y:"9",width:"5",height:"1",rx:".5",fill:m,opacity:".12"})]});case"tooltip":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"3",width:"14",height:"7",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5.5",y:"5.5",width:"9",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("path",{d:"M9 10l1 2.5 1-2.5",stroke:m,strokeWidth:A})]});case"pricing":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6",y:"3",width:"8",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"7",y:"5.5",width:"6",height:"2",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"5",y:"9",width:"10",height:"1",rx:".5",fill:m,opacity:".1"}),(0,c.jsx)("rect",{x:"5",y:"11",width:"10",height:"1",rx:".5",fill:m,opacity:".1"}),(0,c.jsx)("rect",{x:"6",y:"13",width:"8",height:"1.5",rx:".5",fill:m,opacity:".2"})]});case"testimonial":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("text",{x:"4",y:"5.5",fontSize:"4",fill:m,opacity:".2",fontFamily:"serif",children:"\u201C"}),(0,c.jsx)("rect",{x:"4",y:"7",width:"12",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"4",y:"9",width:"9",height:"1",rx:".5",fill:m,opacity:".12"}),(0,c.jsx)("circle",{cx:"5.5",cy:"12.5",r:"1.5",stroke:m,strokeWidth:A,opacity:".25"}),(0,c.jsx)("rect",{x:"8",y:"12",width:"5",height:"1",rx:".5",fill:m,opacity:".15"})]});case"cta":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"2",width:"18",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"4.5",width:"10",height:"1.5",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"6",y:"7.5",width:"8",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"7",y:"10",width:"6",height:"2.5",rx:"1",stroke:m,strokeWidth:A})]});case"alert":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"4",width:"16",height:"8",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"6",cy:"8",r:"2",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("line",{x1:"6",y1:"7",x2:"6",y2:"8.5",stroke:m,strokeWidth:"0.6",opacity:".5"}),(0,c.jsx)("circle",{cx:"6",cy:"9.3",r:".3",fill:m,opacity:".5"}),(0,c.jsx)("rect",{x:"9.5",y:"7",width:"6",height:"1",rx:".5",fill:m,opacity:".2"})]});case"banner":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"5",width:"18",height:"6",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"4",y:"7.5",width:"8",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"14",y:"7",width:"3.5",height:"2",rx:".75",stroke:m,strokeWidth:A})]});case"stat":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"2",width:"14",height:"12",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6",y:"4.5",width:"8",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"5",y:"7",width:"10",height:"2.5",rx:".5",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"7",y:"11",width:"6",height:"1",rx:".5",fill:m,opacity:".12"})]});case"stepper":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"4",cy:"8",r:"2",fill:m,opacity:".2",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"6",y1:"8",x2:"8",y2:"8",stroke:m,strokeWidth:".4",opacity:".3"}),(0,c.jsx)("circle",{cx:"10",cy:"8",r:"2",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"12",y1:"8",x2:"14",y2:"8",stroke:m,strokeWidth:".4",opacity:".3"}),(0,c.jsx)("circle",{cx:"16",cy:"8",r:"2",stroke:m,strokeWidth:A})]});case"tag":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"5",width:"14",height:"6",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5.5",y:"7.5",width:"6",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("line",{x1:"14",y1:"6.5",x2:"15.5",y2:"9.5",stroke:m,strokeWidth:A,opacity:".2"}),(0,c.jsx)("line",{x1:"15.5",y1:"6.5",x2:"14",y2:"9.5",stroke:m,strokeWidth:A,opacity:".2"})]});case"rating":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("path",{d:"M4 5.5l1 2 2.2.3-1.6 1.5.4 2.2L4 10.3l-2 1.2.4-2.2L.8 7.8 3 7.5z",fill:m,opacity:".25"}),(0,c.jsx)("path",{d:"M10 5.5l1 2 2.2.3-1.6 1.5.4 2.2L10 10.3l-2 1.2.4-2.2L6.8 7.8 9 7.5z",fill:m,opacity:".25"}),(0,c.jsx)("path",{d:"M16 5.5l1 2 2.2.3-1.6 1.5.4 2.2L16 10.3l-2 1.2.4-2.2-1.6-1.5 2.2-.3z",stroke:m,strokeWidth:A,opacity:".25"})]});case"map":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"2",y1:"6",x2:"18",y2:"10",stroke:m,strokeWidth:".3",opacity:".15"}),(0,c.jsx)("line",{x1:"7",y1:"2",x2:"11",y2:"14",stroke:m,strokeWidth:".3",opacity:".15"}),(0,c.jsx)("path",{d:"M10 5c-1.7 0-3 1.3-3 3 0 2.5 3 5 3 5s3-2.5 3-5c0-1.7-1.3-3-3-3z",fill:m,opacity:".15",stroke:m,strokeWidth:A})]});case"timeline":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("line",{x1:"5",y1:"2",x2:"5",y2:"14",stroke:m,strokeWidth:".4",opacity:".25"}),(0,c.jsx)("circle",{cx:"5",cy:"4",r:"1.5",fill:m,opacity:".2",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"8",y:"3",width:"8",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("circle",{cx:"5",cy:"8.5",r:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"8",y:"7.5",width:"6",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("circle",{cx:"5",cy:"13",r:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"8",y:"12",width:"7",height:"1",rx:".5",fill:m,opacity:".15"})]});case"fileUpload":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"2",width:"14",height:"12",rx:"1.5",stroke:m,strokeWidth:A,strokeDasharray:"2 1"}),(0,c.jsx)("path",{d:"M10 10V5.5m0 0L7.5 8m2.5-2.5L12.5 8",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("rect",{x:"7",y:"11.5",width:"6",height:"1",rx:".5",fill:m,opacity:".15"})]});case"codeBlock":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"4",cy:"4",r:".6",fill:m,opacity:".3"}),(0,c.jsx)("circle",{cx:"5.5",cy:"4",r:".6",fill:m,opacity:".3"}),(0,c.jsx)("circle",{cx:"7",cy:"4",r:".6",fill:m,opacity:".3"}),(0,c.jsx)("rect",{x:"4",y:"7",width:"7",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"6",y:"9",width:"5",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"4",y:"11",width:"8",height:"1",rx:".5",fill:m,opacity:".12"})]});case"calendar":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"3",width:"16",height:"12",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("line",{x1:"2",y1:"6.5",x2:"18",y2:"6.5",stroke:m,strokeWidth:".4",opacity:".25"}),(0,c.jsx)("rect",{x:"5",y:"4",width:"1",height:"1.5",rx:".3",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"14",y:"4",width:"1",height:"1.5",rx:".3",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"7",cy:"9",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"10",cy:"9",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"13",cy:"9",r:".6",fill:m,opacity:".3"}),(0,c.jsx)("circle",{cx:"7",cy:"12",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"10",cy:"12",r:".6",fill:m,opacity:".2"})]});case"notification":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"3",width:"16",height:"10",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"5.5",cy:"8",r:"2",stroke:m,strokeWidth:A,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"6",width:"6",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"8.5",width:"4.5",height:"1",rx:".5",fill:m,opacity:".12"}),(0,c.jsx)("circle",{cx:"16.5",cy:"4.5",r:"1.5",fill:m,opacity:".25"})]});case"productCard":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"1",width:"14",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3",y:"1",width:"14",height:"6",rx:"1",fill:m,opacity:".04"}),(0,c.jsx)("rect",{x:"5",y:"8.5",width:"7",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"5",y:"10.5",width:"4",height:"1.5",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"12",y:"12",width:"4",height:"2",rx:".75",stroke:m,strokeWidth:A})]});case"profile":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"10",cy:"5",r:"3",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"10",width:"10",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"7",y:"12.5",width:"6",height:"1",rx:".5",fill:m,opacity:".12"})]});case"drawer":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"9",y:"1",width:"10",height:"14",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"10.5",y:"4",width:"5",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"10.5",y:"6.5",width:"7",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"10.5",y:"9",width:"6",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"1",y:"1",width:"7",height:"14",rx:"1",stroke:m,strokeWidth:A,opacity:".15"})]});case"popover":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"2",width:"14",height:"9",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"4.5",width:"8",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"5",y:"7",width:"6",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("path",{d:"M9 11l1 2.5 1-2.5",stroke:m,strokeWidth:A})]});case"logo":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"3",width:"10",height:"10",rx:"2",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M5 9.5l2-4 2 4",stroke:m,strokeWidth:A,opacity:".3"}),(0,c.jsx)("rect",{x:"14",y:"6",width:"4",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"14",y:"8.5",width:"3",height:"1",rx:".5",fill:m,opacity:".12"})]});case"faq":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("text",{x:"2.5",y:"5.5",fontSize:"4",fill:m,opacity:".3",fontWeight:"bold",children:"?"}),(0,c.jsx)("rect",{x:"7",y:"3",width:"10",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"7",y:"5.5",width:"8",height:"1",rx:".5",fill:m,opacity:".12"}),(0,c.jsx)("text",{x:"2.5",y:"11.5",fontSize:"4",fill:m,opacity:".3",fontWeight:"bold",children:"?"}),(0,c.jsx)("rect",{x:"7",y:"9",width:"9",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"7",y:"11.5",width:"7",height:"1",rx:".5",fill:m,opacity:".12"})]});case"gallery":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1.5",y:"1.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"7.5",y:"1.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"13.5",y:"1.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"1.5",y:"9.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"7.5",y:"9.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"13.5",y:"9.5",width:"5",height:"5",rx:".75",stroke:m,strokeWidth:A})]});case"checkbox":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"5",y:"4",width:"8",height:"8",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M7.5 8l1.5 1.5 3-3",stroke:m,strokeWidth:A,opacity:".35"})]});case"radio":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"10",cy:"8",r:"4",stroke:m,strokeWidth:A}),(0,c.jsx)("circle",{cx:"10",cy:"8",r:"2",fill:m,opacity:".3"})]});case"slider":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"7.5",width:"16",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"2",y:"7.5",width:"10",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("circle",{cx:"12",cy:"8",r:"2.5",stroke:m,strokeWidth:A})]});case"datePicker":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"5",rx:"1",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"3.5",y:"3",width:"5",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"14",y:"2.5",width:"2.5",height:"2",rx:".5",fill:m,opacity:".12"}),(0,c.jsx)("rect",{x:"2",y:"7",width:"16",height:"8",rx:"1",stroke:m,strokeWidth:A,strokeDasharray:"2 1",opacity:".3"}),(0,c.jsx)("circle",{cx:"6",cy:"10",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"10",cy:"10",r:".6",fill:m,opacity:".3"}),(0,c.jsx)("circle",{cx:"14",cy:"10",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"6",cy:"13",r:".6",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"10",cy:"13",r:".6",fill:m,opacity:".2"})]});case"skeleton":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"16",height:"3",rx:"1",fill:m,opacity:".08"}),(0,c.jsx)("rect",{x:"2",y:"7",width:"10",height:"2",rx:".75",fill:m,opacity:".08"}),(0,c.jsx)("rect",{x:"2",y:"11",width:"13",height:"2",rx:".75",fill:m,opacity:".08"})]});case"chip":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"1.5",y:"5",width:"10",height:"6",rx:"3",fill:m,opacity:".08",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"4",y:"7.5",width:"4",height:"1",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("line",{x1:"9.5",y1:"6.5",x2:"10.5",y2:"9.5",stroke:m,strokeWidth:A,opacity:".2"}),(0,c.jsx)("line",{x1:"10.5",y1:"6.5",x2:"9.5",y2:"9.5",stroke:m,strokeWidth:A,opacity:".2"}),(0,c.jsx)("rect",{x:"13",y:"5",width:"5.5",height:"6",rx:"3",stroke:m,strokeWidth:A,opacity:".25"})]});case"icon":return(0,c.jsx)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:(0,c.jsx)("path",{d:"M10 3l1.5 3 3.5.5-2.5 2.5.5 3.5L10 11l-3 1.5.5-3.5L5 6.5l3.5-.5z",stroke:m,strokeWidth:A,opacity:".3"})});case"spinner":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"10",cy:"8",r:"5",stroke:m,strokeWidth:A,opacity:".12"}),(0,c.jsx)("path",{d:"M10 3a5 5 0 0 1 5 5",stroke:m,strokeWidth:A,opacity:".35",strokeLinecap:"round"})]});case"feature":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"2",width:"5",height:"5",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("path",{d:"M4.5 3.5v3m-1.5-1.5h3",stroke:m,strokeWidth:A,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"2.5",width:"8",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"5.5",width:"6",height:"1",rx:".5",fill:m,opacity:".12"}),(0,c.jsx)("rect",{x:"2",y:"10",width:"5",height:"5",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"9",y:"10.5",width:"7",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"9",y:"13.5",width:"5",height:"1",rx:".5",fill:m,opacity:".12"})]});case"team":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("circle",{cx:"5",cy:"5",r:"2.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"2.5",y:"9",width:"5",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"15",cy:"5",r:"2.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"12.5",y:"9",width:"5",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("circle",{cx:"10",cy:"5",r:"2.5",stroke:m,strokeWidth:A,opacity:".5"}),(0,c.jsx)("rect",{x:"7.5",y:"9",width:"5",height:"1",rx:".5",fill:m,opacity:".15"}),(0,c.jsx)("rect",{x:"4",y:"12",width:"12",height:"1",rx:".5",fill:m,opacity:".1"})]});case"login":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"3",y:"1",width:"14",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6",y:"3",width:"8",height:"1.5",rx:".5",fill:m,opacity:".25"}),(0,c.jsx)("rect",{x:"5",y:"5.5",width:"10",height:"3",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"5",y:"9.5",width:"10",height:"3",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"6.5",y:"13.5",width:"7",height:"2",rx:".75",fill:m,opacity:".2"})]});case"contact":return(0,c.jsxs)("svg",{viewBox:"0 0 20 16",width:"20",height:"16",fill:"none",children:[(0,c.jsx)("rect",{x:"2",y:"1",width:"16",height:"14",rx:"1.5",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"4",y:"3",width:"5",height:"1",rx:".5",fill:m,opacity:".2"}),(0,c.jsx)("rect",{x:"4",y:"5",width:"12",height:"2.5",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"4",y:"8.5",width:"12",height:"4",rx:".75",stroke:m,strokeWidth:A}),(0,c.jsx)("rect",{x:"11",y:"13.5",width:"5",height:"1.5",rx:".5",fill:m,opacity:".2"})]});default:return null}}function ev({activeType:e,onSelect:t,onDragStart:n,scrollRef:l,fadeClass:o,blankCanvas:a}){return(0,c.jsx)("div",{ref:l,className:`${R.placeScroll} ${o||""}`,children:xy.map(i=>(0,c.jsxs)("div",{className:R.paletteSection,children:[(0,c.jsx)("div",{className:R.paletteSectionTitle,children:i.section}),i.items.map(s=>(0,c.jsxs)("div",{className:`${R.paletteItem} ${e===s.type?R.active:""} ${a?R.wireframe:""}`,onClick:()=>t(s.type),onMouseDown:r=>{r.button===0&&n(s.type,r)},children:[(0,c.jsx)("div",{className:R.paletteItemIcon,children:(0,c.jsx)(Px,{type:s.type})}),(0,c.jsx)("span",{className:R.paletteItemLabel,children:s.label})]},s.type))]},i.section))})}function tv({value:e,suffix:t}){let[n,l]=(0,Rt.useState)(null),[o,a]=(0,Rt.useState)(t),[i,s]=(0,Rt.useState)("up"),r=(0,Rt.useRef)(e),p=(0,Rt.useRef)(t),f=(0,Rt.useRef)(),b=n!==null&&o!==t;return(0,Rt.useEffect)(()=>{if(e!==r.current){if(e===0){r.current=e,p.current=t,l(null);return}s(e>r.current?"up":"down"),l(r.current),a(p.current),r.current=e,p.current=t,clearTimeout(f.current),f.current=fe(()=>l(null),250)}else p.current=t},[e,t]),n===null?(0,c.jsxs)(c.Fragment,{children:[e,t?` ${t}`:""]}):b?(0,c.jsxs)("span",{className:R.rollingWrap,children:[(0,c.jsxs)("span",{style:{visibility:"hidden"},children:[e," ",t]}),(0,c.jsxs)("span",{className:`${R.rollingNum} ${i==="up"?R.exitUp:R.exitDown}`,children:[n," ",o]},`o${n}-${e}`),(0,c.jsxs)("span",{className:`${R.rollingNum} ${i==="up"?R.enterUp:R.enterDown}`,children:[e," ",t]},`n${e}`)]}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)("span",{className:R.rollingWrap,children:[(0,c.jsx)("span",{style:{visibility:"hidden"},children:e}),(0,c.jsx)("span",{className:`${R.rollingNum} ${i==="up"?R.exitUp:R.exitDown}`,children:n},`o${n}-${e}`),(0,c.jsx)("span",{className:`${R.rollingNum} ${i==="up"?R.enterUp:R.enterDown}`,children:e},`n${e}`)]}),t?` ${t}`:""]})}function nv({activeType:e,onSelect:t,isDarkMode:n,sectionCount:l,onDetectSections:o,visible:a,onExited:i,placementCount:s,onClearPlacements:r,onDragStart:p,blankCanvas:f,onBlankCanvasChange:b,wireframePurpose:_,onWireframePurposeChange:w,Tooltip:C}){let[z,D]=(0,Rt.useState)(!1),[h,y]=(0,Rt.useState)("exit"),[k,E]=(0,Rt.useState)(!1),[Q,oe]=(0,Rt.useState)(!0),L=(0,Rt.useRef)(0),K=(0,Rt.useRef)(""),ee=(0,Rt.useRef)(0),F=(0,Rt.useRef)(),he=(0,Rt.useRef)(null),[et,ft]=(0,Rt.useState)("");(0,Rt.useEffect)(()=>(a?(D(!0),clearTimeout(F.current),cancelAnimationFrame(ee.current),ee.current=wi(()=>{ee.current=wi(()=>{y("enter")})})):(cancelAnimationFrame(ee.current),y("exit"),clearTimeout(F.current),F.current=fe(()=>{D(!1),i?.()},200)),()=>cancelAnimationFrame(ee.current)),[a]);let Re=s>0||l>0,Ie=s+l;if(Ie>0&&(L.current=Ie,K.current=f?Ie===1?"Component":"Components":Ie===1?"Change":"Changes"),(0,Rt.useEffect)(()=>{if(Re)k?oe(!1):(oe(!0),E(!0),wi(()=>{wi(()=>{oe(!1)})}));else{oe(!0);let Pe=fe(()=>E(!1),300);return()=>clearTimeout(Pe)}},[Re]),(0,Rt.useEffect)(()=>{if(!z)return;let Pe=he.current;if(!Pe)return;let W=()=>ft(Jx(Pe));W(),Pe.addEventListener("scroll",W,{passive:!0});let ge=new ResizeObserver(W);return ge.observe(Pe),()=>{Pe.removeEventListener("scroll",W),ge.disconnect()}},[z]),!z)return null;let Ee=[];return s>0&&Ee.push("placed"),l>0&&Ee.push("captured"),(0,c.jsxs)("div",{className:`${R.palette} ${R[h]} ${n?"":R.light}`,"data-feedback-toolbar":!0,"data-agentation-palette":!0,onClick:Pe=>Pe.stopPropagation(),onMouseDown:Pe=>Pe.stopPropagation(),onTransitionEnd:Pe=>{Pe.target===Pe.currentTarget&&(a||(clearTimeout(F.current),D(!1),y("exit"),i?.()))},children:[(0,c.jsxs)("div",{className:R.paletteHeader,children:[(0,c.jsx)("div",{className:R.paletteHeaderTitle,children:"Layout Mode"}),(0,c.jsxs)("div",{className:R.paletteHeaderDesc,children:["Rearrange and resize existing elements, add new components, and explore layout ideas. Agent results may vary."," ",(0,c.jsx)("a",{href:"https://agentation.dev/features#layout-mode",target:"_blank",rel:"noopener noreferrer",children:"Learn more."})]})]}),(0,c.jsxs)("div",{className:`${R.canvasToggle} ${f?R.active:""}`,onClick:()=>b(!f),children:[(0,c.jsx)("span",{className:R.canvasToggleIcon,children:(0,c.jsxs)("svg",{viewBox:"0 0 14 14",width:"14",height:"14",fill:"none",children:[(0,c.jsx)("rect",{x:"1",y:"1",width:"12",height:"12",rx:"2",stroke:"currentColor",strokeWidth:"1"}),(0,c.jsx)("circle",{cx:"4.5",cy:"4.5",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"7",cy:"4.5",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"9.5",cy:"4.5",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"4.5",cy:"7",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"7",cy:"7",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"9.5",cy:"7",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"4.5",cy:"9.5",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"7",cy:"9.5",r:"0.8",fill:"currentColor",opacity:".6"}),(0,c.jsx)("circle",{cx:"9.5",cy:"9.5",r:"0.8",fill:"currentColor",opacity:".6"})]})}),(0,c.jsx)("span",{className:R.canvasToggleLabel,children:"Wireframe New Page"})]}),(0,c.jsx)("div",{className:`${R.wireframePurposeWrap} ${f?"":R.collapsed}`,children:(0,c.jsx)("div",{className:R.wireframePurposeInner,children:(0,c.jsx)("textarea",{className:R.wireframePurposeInput,placeholder:"Describe this page to provide additional context for your agent.",value:_,onChange:Pe=>w(Pe.target.value),rows:2})})}),(0,c.jsx)(ev,{activeType:e,onSelect:t,onDragStart:p,scrollRef:he,fadeClass:et,blankCanvas:f}),k&&(0,c.jsx)("div",{className:`${R.paletteFooterWrap} ${Q?R.footerHidden:""}`,children:(0,c.jsx)("div",{className:R.paletteFooterInner,children:(0,c.jsx)("div",{className:R.paletteFooterInnerContent,children:(0,c.jsxs)("div",{className:R.paletteFooter,children:[(0,c.jsx)("span",{className:R.paletteFooterCount,children:(0,c.jsx)(tv,{value:L.current,suffix:K.current})}),(0,c.jsx)("button",{className:R.paletteFooterClear,onClick:r,children:"Clear"})]})})})})]})}function Mi(e){if(e.parentElement)return e.parentElement;let t=e.getRootNode();return t instanceof ShadowRoot?t.host:null}function bn(e,t){let n=e;for(;n;){if(n.matches(t))return n;n=Mi(n)}return null}function lv(e,t=4){let n=[],l=e,o=0;for(;l&&o<t;){let a=l.tagName.toLowerCase();if(a==="html"||a==="body")break;let i=a;if(l.id)i=`#${l.id}`;else if(l.className&&typeof l.className=="string"){let r=l.className.split(/\s+/).find(p=>p.length>2&&!p.match(/^[a-z]{1,2}$/)&&!p.match(/[A-Z0-9]{5,}/));r&&(i=`.${r.split("_")[0]}`)}let s=Mi(l);!l.parentElement&&s&&(i=`\u27E8shadow\u27E9 ${i}`),n.unshift(i),l=s,o++}return n.join(" > ")}function ki(e){let t=lv(e);if(e.dataset.element)return{name:e.dataset.element,path:t};let n=e.tagName.toLowerCase();if(["path","circle","rect","line","g"].includes(n)){let l=bn(e,"svg");if(l){let o=Mi(l);if(o instanceof HTMLElement)return{name:`graphic in ${ki(o).name}`,path:t}}return{name:"graphic element",path:t}}if(n==="svg"){let l=Mi(e);if(l?.tagName.toLowerCase()==="button"){let o=l.textContent?.trim();return{name:o?`icon in "${o}" button`:"button icon",path:t}}return{name:"icon",path:t}}if(n==="button"){let l=e.textContent?.trim(),o=e.getAttribute("aria-label");return o?{name:`button [${o}]`,path:t}:{name:l?`button "${l.slice(0,25)}"`:"button",path:t}}if(n==="a"){let l=e.textContent?.trim(),o=e.getAttribute("href");return l?{name:`link "${l.slice(0,25)}"`,path:t}:o?{name:`link to ${o.slice(0,30)}`,path:t}:{name:"link",path:t}}if(n==="input"){let l=e.getAttribute("type")||"text",o=e.getAttribute("placeholder"),a=e.getAttribute("name");return o?{name:`input "${o}"`,path:t}:a?{name:`input [${a}]`,path:t}:{name:`${l} input`,path:t}}if(["h1","h2","h3","h4","h5","h6"].includes(n)){let l=e.textContent?.trim();return{name:l?`${n} "${l.slice(0,35)}"`:n,path:t}}if(n==="p"){let l=e.textContent?.trim();return l?{name:`paragraph: "${l.slice(0,40)}${l.length>40?"...":""}"`,path:t}:{name:"paragraph",path:t}}if(n==="span"||n==="label"){let l=e.textContent?.trim();return l&&l.length<40?{name:`"${l}"`,path:t}:{name:n,path:t}}if(n==="li"){let l=e.textContent?.trim();return l&&l.length<40?{name:`list item: "${l.slice(0,35)}"`,path:t}:{name:"list item",path:t}}if(n==="blockquote")return{name:"blockquote",path:t};if(n==="code"){let l=e.textContent?.trim();return l&&l.length<30?{name:`code: \`${l}\``,path:t}:{name:"code",path:t}}if(n==="pre")return{name:"code block",path:t};if(n==="img"){let l=e.getAttribute("alt");return{name:l?`image "${l.slice(0,30)}"`:"image",path:t}}if(n==="video")return{name:"video",path:t};if(["div","section","article","nav","header","footer","aside","main"].includes(n)){let l=e.className,o=e.getAttribute("role"),a=e.getAttribute("aria-label");if(a)return{name:`${n} [${a}]`,path:t};if(o)return{name:`${o}`,path:t};if(typeof l=="string"&&l){let i=l.split(/[\s_-]+/).map(s=>s.replace(/[A-Z0-9]{5,}.*$/,"")).filter(s=>s.length>2&&!/^[a-z]{1,2}$/.test(s)).slice(0,2);if(i.length>0)return{name:i.join(" "),path:t}}return{name:n==="div"?"container":n,path:t}}return{name:n,path:t}}function Us(e){let t=[],n=e.textContent?.trim();n&&n.length<100&&t.push(n);let l=e.previousElementSibling;if(l){let a=l.textContent?.trim();a&&a.length<50&&t.unshift(`[before: "${a.slice(0,40)}"]`)}let o=e.nextElementSibling;if(o){let a=o.textContent?.trim();a&&a.length<50&&t.push(`[after: "${a.slice(0,40)}"]`)}return t.join(" ")}function Uc(e){let t=Mi(e);if(!t)return"";let o=(e.getRootNode()instanceof ShadowRoot&&e.parentElement?Array.from(e.parentElement.children):Array.from(t.children)).filter(f=>f!==e&&f instanceof HTMLElement);if(o.length===0)return"";let a=o.slice(0,4).map(f=>{let b=f.tagName.toLowerCase(),_=f.className,w="";if(typeof _=="string"&&_){let C=_.split(/\s+/).map(z=>z.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(z=>z.length>2&&!/^[a-z]{1,2}$/.test(z));C&&(w=`.${C}`)}if(b==="button"||b==="a"){let C=f.textContent?.trim().slice(0,15);if(C)return`${b}${w} "${C}"`}return`${b}${w}`}),s=t.tagName.toLowerCase();if(typeof t.className=="string"&&t.className){let f=t.className.split(/\s+/).map(b=>b.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(b=>b.length>2&&!/^[a-z]{1,2}$/.test(b));f&&(s=`.${f}`)}let r=t.children.length,p=r>a.length+1?` (${r} total in ${s})`:"";return a.join(", ")+p}function Ys(e){let t=e.className;return typeof t!="string"||!t?"":t.split(/\s+/).filter(l=>l.length>0).map(l=>{let o=l.match(/^([a-zA-Z][a-zA-Z0-9_-]*?)(?:_[a-zA-Z0-9]{5,})?$/);return o?o[1]:l}).filter((l,o,a)=>a.indexOf(l)===o).join(", ")}var vy=new Set(["none","normal","auto","0px","rgba(0, 0, 0, 0)","transparent","static","visible"]),ov=new Set(["p","span","h1","h2","h3","h4","h5","h6","label","li","td","th","blockquote","figcaption","caption","legend","dt","dd","pre","code","em","strong","b","i","a","time","cite","q"]),av=new Set(["input","textarea","select"]),iv=new Set(["img","video","canvas","svg"]),sv=new Set(["div","section","article","nav","header","footer","aside","main","ul","ol","form","fieldset"]);function Yc(e){if(typeof window>"u")return{};let t=window.getComputedStyle(e),n={},l=e.tagName.toLowerCase(),o;ov.has(l)?o=["color","fontSize","fontWeight","fontFamily","lineHeight"]:l==="button"||l==="a"&&e.getAttribute("role")==="button"?o=["backgroundColor","color","padding","borderRadius","fontSize"]:av.has(l)?o=["backgroundColor","color","padding","borderRadius","fontSize"]:iv.has(l)?o=["width","height","objectFit","borderRadius"]:sv.has(l)?o=["display","padding","margin","gap","backgroundColor"]:o=["color","fontSize","margin","padding","backgroundColor"];for(let a of o){let i=a.replace(/([A-Z])/g,"-$1").toLowerCase(),s=t.getPropertyValue(i);s&&!vy.has(s)&&(n[a]=s)}return n}var rv=["color","backgroundColor","borderColor","fontSize","fontWeight","fontFamily","lineHeight","letterSpacing","textAlign","width","height","padding","margin","border","borderRadius","display","position","top","right","bottom","left","zIndex","flexDirection","justifyContent","alignItems","gap","opacity","visibility","overflow","boxShadow","transform"];function jc(e){if(typeof window>"u")return"";let t=window.getComputedStyle(e),n=[];for(let l of rv){let o=l.replace(/([A-Z])/g,"-$1").toLowerCase(),a=t.getPropertyValue(o);a&&!vy.has(a)&&n.push(`${o}: ${a}`)}return n.join("; ")}function cv(e){if(!e)return;let t={},n=e.split(";").map(l=>l.trim()).filter(Boolean);for(let l of n){let o=l.indexOf(":");if(o>0){let a=l.slice(0,o).trim(),i=l.slice(o+1).trim();a&&i&&(t[a]=i)}}return Object.keys(t).length>0?t:void 0}function Xc(e){let t=[],n=e.getAttribute("role"),l=e.getAttribute("aria-label"),o=e.getAttribute("aria-describedby"),a=e.getAttribute("tabindex"),i=e.getAttribute("aria-hidden");return n&&t.push(`role="${n}"`),l&&t.push(`aria-label="${l}"`),o&&t.push(`aria-describedby="${o}"`),a&&t.push(`tabindex=${a}`),i==="true"&&t.push("aria-hidden"),e.matches("a, button, input, select, textarea, [tabindex]")&&t.push("focusable"),t.join(", ")}function Ic(e){let t=[],n=e;for(;n&&n.tagName.toLowerCase()!=="html";){let l=n.tagName.toLowerCase(),o=l;if(n.id)o=`${l}#${n.id}`;else if(n.className&&typeof n.className=="string"){let i=n.className.split(/\s+/).map(s=>s.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(s=>s.length>2);i&&(o=`${l}.${i}`)}let a=Mi(n);!n.parentElement&&a&&(o=`\u27E8shadow\u27E9 ${o}`),t.unshift(o),n=a}return t.join(" > ")}var uv=new Set(["nav","header","main","section","article","footer","aside"]),mf={banner:"Header",navigation:"Navigation",main:"Main Content",contentinfo:"Footer",complementary:"Sidebar",region:"Section"},Zg={nav:"Navigation",header:"Header",main:"Main Content",section:"Section",article:"Article",footer:"Footer",aside:"Sidebar"},dv=new Set(["script","style","noscript","link","meta"]),_v=40;function wy(e){let t=e;for(;t&&t!==document.body&&t!==document.documentElement;){let n=window.getComputedStyle(t).position;if(n==="fixed"||n==="sticky")return!0;t=t.parentElement}return!1}function pa(e){let t=e.tagName.toLowerCase();if(["nav","header","footer","main"].includes(t)&&document.querySelectorAll(t).length===1)return t;if(e.id)return`#${CSS.escape(e.id)}`;if(e.className&&typeof e.className=="string"){let o=e.className.split(/\s+/).filter(a=>a.length>0).find(a=>a.length>2&&!/^[a-zA-Z0-9]{6,}$/.test(a)&&!/^[a-z]{1,2}$/.test(a));if(o){let a=`${t}.${CSS.escape(o)}`;if(document.querySelectorAll(a).length===1)return a}}let n=e.parentElement;if(n){let o=Array.from(n.children).indexOf(e)+1;return`${n===document.body?"body":pa(n)} > ${t}:nth-child(${o})`}return t}function Fc(e){let t=e.tagName.toLowerCase(),n=e.getAttribute("aria-label");if(n)return n;let l=e.getAttribute("role");if(l&&mf[l])return mf[l];if(Zg[t])return Zg[t];let o=e.querySelector("h1, h2, h3, h4, h5, h6");if(o){let i=o.textContent?.trim();if(i&&i.length<=50)return i;if(i)return i.slice(0,47)+"..."}let{name:a}=ki(e);return a.charAt(0).toUpperCase()+a.slice(1)}function ky(e){let t=e.className;return typeof t!="string"||!t?null:t.split(/\s+/).map(l=>l.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(l=>l.length>2&&!/^[a-z]{1,2}$/.test(l))||null}function Sy(e){let t=e.textContent?.trim();if(!t)return null;let n=t.replace(/\s+/g," ");return n.length<=30?n:n.slice(0,30)+"\u2026"}function fv(){let e=document.querySelector("main")||document.body,t=Array.from(e.children),n=t;e!==document.body&&t.length<3&&(n=Array.from(document.body.children));let l=[];return n.forEach((o,a)=>{if(!(o instanceof HTMLElement))return;let i=o.tagName.toLowerCase();if(dv.has(i)||o.hasAttribute("data-feedback-toolbar")||o.closest("[data-feedback-toolbar]"))return;let s=window.getComputedStyle(o);if(s.display==="none"||s.visibility==="hidden")return;let r=o.getBoundingClientRect();if(r.height<_v)return;let p=uv.has(i),f=o.getAttribute("role")&&mf[o.getAttribute("role")],b=i==="div"&&r.height>=60;if(!p&&!f&&!b)return;let _=window.scrollY,w=wy(o),C={x:r.x,y:w?r.y:r.y+_,width:r.width,height:r.height};l.push({id:`rs-${Date.now()}-${Math.random().toString(36).slice(2,7)}`,label:Fc(o),tagName:i,selector:pa(o),role:o.getAttribute("role"),className:ky(o),textSnippet:Sy(o),originalRect:C,currentRect:{...C},originalIndex:a,isFixed:w})}),l}function hv(e){let t=window.scrollY,n=e.getBoundingClientRect(),l=wy(e),o={x:n.x,y:l?n.y:n.y+t,width:n.width,height:n.height},a=e.parentElement,i=0;return a&&(i=Array.from(a.children).indexOf(e)),{id:`rs-${Date.now()}-${Math.random().toString(36).slice(2,7)}`,label:Fc(e),tagName:e.tagName.toLowerCase(),selector:pa(e),role:e.getAttribute("role"),className:ky(e),textSnippet:Sy(e),originalRect:o,currentRect:{...o},originalIndex:i,isFixed:l}}var Kg={bg:"rgba(59, 130, 246, 0.08)",border:"rgba(59, 130, 246, 0.5)",pill:"#3b82f6"},Fg=["nw","n","ne","e","se","s","sw","w"],qc=24,Jg=16,Qc=5;function Pg(e,t,n,l){let o=1/0,a=1/0,i=e.x,s=e.x+e.width,r=e.x+e.width/2,p=e.y,f=e.y+e.height,b=e.y+e.height/2,_=[];for(let L of t)n.has(L.id)||_.push(L.currentRect);l&&_.push(...l);for(let L of _){let K=L.x,ee=L.x+L.width,F=L.x+L.width/2,he=L.y,et=L.y+L.height,ft=L.y+L.height/2;for(let Re of[i,s,r])for(let Ie of[K,ee,F]){let Ee=Ie-Re;Math.abs(Ee)<Qc&&Math.abs(Ee)<Math.abs(o)&&(o=Ee)}for(let Re of[p,f,b])for(let Ie of[he,et,ft]){let Ee=Ie-Re;Math.abs(Ee)<Qc&&Math.abs(Ee)<Math.abs(a)&&(a=Ee)}}let w=Math.abs(o)<Qc?o:0,C=Math.abs(a)<Qc?a:0,z=[],D=new Set,h=i+w,y=s+w,k=r+w,E=p+C,Q=f+C,oe=b+C;for(let L of _){let K=L.x,ee=L.x+L.width,F=L.x+L.width/2,he=L.y,et=L.y+L.height,ft=L.y+L.height/2;for(let Re of[K,F,ee])for(let Ie of[h,k,y])if(Math.abs(Ie-Re)<.5){let Ee=`x:${Math.round(Re)}`;D.has(Ee)||(D.add(Ee),z.push({axis:"x",pos:Re}))}for(let Re of[he,ft,et])for(let Ie of[E,oe,Q])if(Math.abs(Ie-Re)<.5){let Ee=`y:${Math.round(Re)}`;D.has(Ee)||(D.add(Ee),z.push({axis:"y",pos:Re}))}}return{dx:w,dy:C,guides:z}}var mv=new Set(["script","style","noscript","link","meta","br","hr"]);function ey(e){let t=e;for(;t&&t!==document.body&&t!==document.documentElement;){if(t.closest("[data-feedback-toolbar]"))return null;if(mv.has(t.tagName.toLowerCase())){t=t.parentElement;continue}let n=t.getBoundingClientRect();if(n.width>=Jg&&n.height>=Jg)return t;t=t.parentElement}return null}function gv({rearrangeState:e,onChange:t,isDarkMode:n,exiting:l,className:o,blankCanvas:a,extraSnapRects:i,onSelectionChange:s,deselectSignal:r,onDragMove:p,onDragEnd:f,clearSignal:b}){let{sections:_}=e,w=(0,ke.useRef)(e);w.current=e;let[C,z]=(0,ke.useState)(new Set),[D,h]=(0,ke.useState)(!1),y=(0,ke.useRef)(b);(0,ke.useEffect)(()=>{b!==void 0&&b!==y.current&&(y.current=b,_.length>0&&h(!0))},[b,_.length]);let k=(0,ke.useRef)(r);(0,ke.useEffect)(()=>{r!==k.current&&(k.current=r,z(new Set))},[r]);let[E,Q]=(0,ke.useState)(null),[oe,L]=(0,ke.useState)(!1),K=(0,ke.useRef)(!1),ee=(0,ke.useCallback)(M=>{let N=_.find($=>$.id===M);N&&(K.current=!!N.note,Q(M),L(!1))},[_]),F=(0,ke.useCallback)(()=>{E&&(L(!0),fe(()=>{Q(null),L(!1)},150))},[E]),he=(0,ke.useCallback)(M=>{E&&(t({...e,sections:_.map(N=>N.id===E?{...N,note:M.trim()||void 0}:N)}),F())},[E,_,e,t,F]);(0,ke.useEffect)(()=>{l&&E&&F()},[l]);let[et,ft]=(0,ke.useState)(new Set),Re=(0,ke.useRef)(new Map),[Ie,Ee]=(0,ke.useState)(null),[Pe,W]=(0,ke.useState)(null),[ge,Ze]=(0,ke.useState)([]),[Bt,vn]=(0,ke.useState)(0),hn=(0,ke.useRef)(null),oo=(0,ke.useRef)(new Set),In=(0,ke.useRef)(new Map),[ao,il]=(0,ke.useState)(new Map),[Rl,io]=(0,ke.useState)(new Map),Uo=(0,ke.useRef)(new Set),zn=(0,ke.useRef)(new Map),sl=(0,ke.useRef)(s);sl.current=s;let wn=(0,ke.useRef)(p);wn.current=p;let yl=(0,ke.useRef)(f);yl.current=f,(0,ke.useEffect)(()=>{a&&z(new Set)},[a]);let[pl,ba]=(0,ke.useState)(()=>!e.sections.some(M=>{let N=M.originalRect,$=M.currentRect;return Math.abs(N.x-$.x)>1||Math.abs(N.y-$.y)>1||Math.abs(N.width-$.width)>1||Math.abs(N.height-$.height)>1}));(0,ke.useEffect)(()=>{if(!pl){let M=fe(()=>ba(!0),380);return()=>clearTimeout(M)}},[]);let rl=(0,ke.useRef)(new Set);(0,ke.useEffect)(()=>{rl.current=new Set(_.map(M=>M.selector))},[_]),(0,ke.useEffect)(()=>{let M=()=>vn(window.scrollY);return M(),window.addEventListener("scroll",M,{passive:!0}),window.addEventListener("resize",M,{passive:!0}),()=>{window.removeEventListener("scroll",M),window.removeEventListener("resize",M)}},[]),(0,ke.useEffect)(()=>{let M=N=>{if(hn.current){Ee(null);return}let $=document.elementFromPoint(N.clientX,N.clientY);if(!$){Ee(null);return}if($.closest("[data-feedback-toolbar]")){Ee(null);return}if($.closest("[data-design-placement]")){Ee(null);return}if($.closest("[data-annotation-popup]")){Ee(null);return}let U=ey($);if(!U){Ee(null);return}for(let ae of rl.current)try{let X=document.querySelector(ae);if(X&&(X===U||U.contains(X))){Ee(null);return}}catch{}let J=U.getBoundingClientRect();Ee({x:J.x,y:J.y,w:J.width,h:J.height})};return document.addEventListener("mousemove",M,{passive:!0}),()=>document.removeEventListener("mousemove",M)},[_]),(0,ke.useEffect)(()=>{let M=document.body.style.userSelect;return document.body.style.userSelect="none",()=>{document.body.style.userSelect=M}},[]),(0,ke.useEffect)(()=>{let M=N=>{if(hn.current||N.button!==0)return;let $=N.target;if(!$||$.closest("[data-feedback-toolbar]")||$.closest("[data-design-placement]")||$.closest("[data-annotation-popup]"))return;let U=ey($),J=!1;if(U)for(let X of rl.current)try{let ie=document.querySelector(X);if(ie&&(ie===U||U.contains(ie))){J=!0;break}}catch{}let ae=!!(N.shiftKey||N.metaKey||N.ctrlKey);if(U&&!J){N.preventDefault(),N.stopPropagation();let X=hv(U),ie=[..._,X],Ce=[...e.originalOrder,X.id];t({...e,sections:ie,originalOrder:Ce});let qe=new Set([X.id]);z(qe),sl.current?.(qe,ae),Ee(null);let nt=N.clientX,se=N.clientY,st={x:X.currentRect.x,y:X.currentRect.y},Oe=X.originalRect,Te=!1,re=0,rt=0;hn.current="move";let Ge=Fe=>{let xe=Fe.clientX-nt,vt=Fe.clientY-se;if(!Te&&(Math.abs(xe)>2||Math.abs(vt)>2)&&(Te=!0),!Te)return;let tn={x:st.x+xe,y:st.y+vt,width:X.currentRect.width,height:X.currentRect.height},qn=Pg(tn,ie,new Set([X.id]),i);Ze(qn.guides);let bl=xe+qn.dx,kn=vt+qn.dy;re=bl,rt=kn;let Bl=document.querySelector(`[data-rearrange-section="${X.id}"]`);Bl&&(Bl.style.transform=`translate(${bl}px, ${kn}px)`),il(new Map([[X.id,{x:st.x+bl,y:st.y+kn,width:X.currentRect.width,height:X.currentRect.height}]])),wn.current?.(bl,kn)},De=()=>{window.removeEventListener("mousemove",Ge),window.removeEventListener("mouseup",De),hn.current=null,Ze([]),il(new Map);let Fe=document.querySelector(`[data-rearrange-section="${X.id}"]`);Fe&&(Fe.style.transform=""),Te&&t({...e,sections:ie.map(xe=>xe.id===X.id?{...xe,currentRect:{...xe.currentRect,x:Math.max(0,st.x+re),y:Math.max(0,st.y+rt)}}:xe),originalOrder:Ce}),yl.current?.(re,rt,Te)};window.addEventListener("mousemove",Ge),window.addEventListener("mouseup",De)}else if(J&&U){N.preventDefault();for(let X of _)try{let ie=document.querySelector(X.selector);if(ie&&ie===U){let Ce=new Set([X.id]);z(Ce),sl.current?.(Ce,ae);return}}catch{}ae||(z(new Set),sl.current?.(new Set,!1))}else ae||(z(new Set),sl.current?.(new Set,!1))};return document.addEventListener("mousedown",M,!0),()=>document.removeEventListener("mousedown",M,!0)},[_,e,t]),(0,ke.useEffect)(()=>{let M=N=>{let $=N.target;if(!($.tagName==="INPUT"||$.tagName==="TEXTAREA"||$.isContentEditable)){if((N.key==="Backspace"||N.key==="Delete")&&C.size>0){N.preventDefault();let U=new Set(C);ft(J=>{let ae=new Set(J);for(let X of U)ae.add(X);return ae}),z(new Set),fe(()=>{let J=w.current;t({...J,sections:J.sections.filter(ae=>!U.has(ae.id)),originalOrder:J.originalOrder.filter(ae=>!U.has(ae))}),ft(ae=>{let X=new Set(ae);for(let ie of U)X.delete(ie);return X})},180);return}if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(N.key)&&C.size>0){N.preventDefault();let U=N.shiftKey?20:1,J=N.key==="ArrowLeft"?-U:N.key==="ArrowRight"?U:0,ae=N.key==="ArrowUp"?-U:N.key==="ArrowDown"?U:0;t({...e,sections:_.map(X=>C.has(X.id)?{...X,currentRect:{...X.currentRect,x:Math.max(0,X.currentRect.x+J),y:Math.max(0,X.currentRect.y+ae)}}:X)});return}N.key==="Escape"&&C.size>0&&z(new Set)}};return document.addEventListener("keydown",M),()=>document.removeEventListener("keydown",M)},[C,_,e,t]);let Be=(0,ke.useCallback)((M,N)=>{if(M.button!==0)return;let $=M.target;if($.closest(`.${R.handle}`)||$.closest(`.${R.deleteButton}`))return;M.preventDefault(),M.stopPropagation();let U;M.shiftKey||M.metaKey||M.ctrlKey?(U=new Set(C),U.has(N)?U.delete(N):U.add(N)):C.has(N)?U=new Set(C):U=new Set([N]),z(U),(U.size!==C.size||[...U].some(Te=>!C.has(Te)))&&sl.current?.(U,!!(M.shiftKey||M.metaKey||M.ctrlKey));let ae=M.clientX,X=M.clientY,ie=new Map;for(let Te of _)U.has(Te.id)&&ie.set(Te.id,{x:Te.currentRect.x,y:Te.currentRect.y});hn.current="move";let Ce=!1,qe=0,nt=0,se=new Map;for(let Te of _)if(U.has(Te.id)){let re=document.querySelector(`[data-rearrange-section="${Te.id}"]`);se.set(Te.id,{outlineEl:re,curW:Te.currentRect.width,curH:Te.currentRect.height})}let st=Te=>{let re=Te.clientX-ae,rt=Te.clientY-X;if(re===0&&rt===0)return;Ce=!0;let Ge=1/0,De=1/0,Fe=-1/0,xe=-1/0;for(let[kn,{curW:Bl,curH:Vs}]of se){let Ut=ie.get(kn);if(!Ut)continue;let Ol=Ut.x+re,Zs=Ut.y+rt;Ge=Math.min(Ge,Ol),De=Math.min(De,Zs),Fe=Math.max(Fe,Ol+Bl),xe=Math.max(xe,Zs+Vs)}let vt=Pg({x:Ge,y:De,width:Fe-Ge,height:xe-De},_,U,i),tn=re+vt.dx,qn=rt+vt.dy;qe=tn,nt=qn,Ze(vt.guides);for(let[,{outlineEl:kn}]of se)kn&&(kn.style.transform=`translate(${tn}px, ${qn}px)`);let bl=new Map;for(let[kn,{curW:Bl,curH:Vs}]of se){let Ut=ie.get(kn);if(Ut){let Ol={x:Math.max(0,Ut.x+tn),y:Math.max(0,Ut.y+qn),width:Bl,height:Vs};bl.set(kn,Ol)}}il(bl),wn.current?.(tn,qn)},Oe=Te=>{window.removeEventListener("mousemove",st),window.removeEventListener("mouseup",Oe),hn.current=null,Ze([]),il(new Map);for(let[,{outlineEl:re}]of se)re&&(re.style.transform="");if(Ce){let re=Te.clientX-ae,rt=Te.clientY-X;if(Math.abs(re)<5&&Math.abs(rt)<5)t({...e,sections:_.map(Ge=>{let De=ie.get(Ge.id);return De?{...Ge,currentRect:{...Ge.currentRect,x:De.x,y:De.y}}:Ge})});else{t({...e,sections:_.map(Ge=>{let De=ie.get(Ge.id);return De?{...Ge,currentRect:{...Ge.currentRect,x:Math.max(0,De.x+qe),y:Math.max(0,De.y+nt)}}:Ge})}),yl.current?.(qe,nt,!0);return}}yl.current?.(0,0,!1)};window.addEventListener("mousemove",st),window.addEventListener("mouseup",Oe)},[C,_,e,t]),I=(0,ke.useCallback)((M,N,$)=>{M.preventDefault(),M.stopPropagation();let U=_.find(Oe=>Oe.id===N);if(!U)return;z(new Set([N])),hn.current="resize";let J=M.clientX,ae=M.clientY,X={...U.currentRect},ie=U.originalRect,Ce=X.width/X.height,qe={...X},nt=document.querySelector(`[data-rearrange-section="${N}"]`),se=Oe=>{let Te=Oe.clientX-J,re=Oe.clientY-ae,rt=X.x,Ge=X.y,De=X.width,Fe=X.height;if($.includes("e")&&(De=Math.max(qc,X.width+Te)),$.includes("w")&&(De=Math.max(qc,X.width-Te),rt=X.x+X.width-De),$.includes("s")&&(Fe=Math.max(qc,X.height+re)),$.includes("n")&&(Fe=Math.max(qc,X.height-re),Ge=X.y+X.height-Fe),Oe.shiftKey)if($.length===2){let vt=Math.abs(De-X.width),tn=Math.abs(Fe-X.height);vt>tn?Fe=De/Ce:De=Fe*Ce,$.includes("w")&&(rt=X.x+X.width-De),$.includes("n")&&(Ge=X.y+X.height-Fe)}else $==="e"||$==="w"?Fe=De/Ce:De=Fe*Ce,$==="w"&&(rt=X.x+X.width-De),$==="n"&&(Ge=X.y+X.height-Fe);qe={x:rt,y:Ge,width:De,height:Fe},nt&&(nt.style.left=`${rt}px`,nt.style.top=`${Ge-Bt}px`,nt.style.width=`${De}px`,nt.style.height=`${Fe}px`),W({x:Oe.clientX+12,y:Oe.clientY+12,text:`${Math.round(De)} \xD7 ${Math.round(Fe)}`}),il(new Map([[N,qe]]))},st=()=>{window.removeEventListener("mousemove",se),window.removeEventListener("mouseup",st),W(null),hn.current=null,il(new Map),t({...e,sections:_.map(Oe=>Oe.id===N?{...Oe,currentRect:qe}:Oe)})};window.addEventListener("mousemove",se),window.addEventListener("mouseup",st)},[_,e,t,Bt]),de=(0,ke.useCallback)(M=>{ft(N=>{let $=new Set(N);return $.add(M),$}),z(N=>{let $=new Set(N);return $.delete(M),$}),fe(()=>{let N=w.current;t({...N,sections:N.sections.filter($=>$.id!==M),originalOrder:N.originalOrder.filter($=>$!==M)}),ft($=>{let U=new Set($);return U.delete(M),U})},180)},[t]),pe=M=>{let N=M.originalRect,$=M.currentRect;return Math.abs(N.x-$.x)>1||Math.abs(N.y-$.y)>1||Math.abs(N.width-$.width)>1||Math.abs(N.height-$.height)>1},Ae=M=>{let N=M.originalRect,$=M.currentRect;return Math.abs(N.x-$.x)>1||Math.abs(N.y-$.y)>1},be=M=>{let N=M.originalRect,$=M.currentRect;return Math.abs(N.width-$.width)>1||Math.abs(N.height-$.height)>1};for(let M of _)In.current.has(M.id)||(Ae(M)?In.current.set(M.id,"move"):be(M)&&In.current.set(M.id,"resize"));for(let M of In.current.keys())_.some(N=>N.id===M)||In.current.delete(M);let tt=_.filter(M=>{try{if(et.has(M.id)||C.has(M.id))return!0;let N=document.querySelector(M.selector);if(!N)return!1;let $=N.getBoundingClientRect(),U=M.originalRect;return Math.abs($.width-U.width)+Math.abs($.height-U.height)<200}catch{return!1}}),it=tt.filter(M=>pe(M)),Ke=tt.filter(M=>!pe(M)),Ue=new Set(it.map(M=>M.id));for(let M of oo.current)Ue.has(M)||oo.current.delete(M);let me=[...Ue].sort().join(",");for(let M of it)zn.current.set(M.id,{currentRect:M.currentRect,originalRect:M.originalRect,isFixed:M.isFixed});return(0,ke.useEffect)(()=>{let M=Uo.current;Uo.current=Ue;let N=new Map;for(let $ of M)if(!Ue.has($)){if(!_.some(J=>J.id===$))continue;let U=zn.current.get($);U&&(N.set($,{orig:U.originalRect,target:U.currentRect,isFixed:U.isFixed}),zn.current.delete($))}if(N.size>0){io(U=>{let J=new Map(U);for(let[ae,X]of N)J.set(ae,X);return J});let $=fe(()=>{io(U=>{let J=new Map(U);for(let ae of N.keys())J.delete(ae);return J})},250);return()=>clearTimeout($)}},[me,_]),(0,Ve.jsxs)(Ve.Fragment,{children:[(0,Ve.jsxs)("div",{className:`${R.rearrangeOverlay} ${n?"":R.light} ${l?R.overlayExiting:""}${o?` ${o}`:""}`,"data-feedback-toolbar":!0,children:[Ie&&(0,Ve.jsx)("div",{className:R.hoverHighlight,style:{left:Ie.x,top:Ie.y,width:Ie.w,height:Ie.h}}),Ke.map(M=>{let N=M.currentRect,$=M.isFixed?N.y:N.y-Bt,U=Kg,J=C.has(M.id);return(0,Ve.jsxs)("div",{"data-rearrange-section":M.id,className:`${R.sectionOutline} ${J?R.selected:""} ${D||l||et.has(M.id)?R.exiting:""}`,style:{left:N.x,top:$,width:N.width,height:N.height,borderColor:U.border,backgroundColor:U.bg,...pl?{}:{opacity:0,animation:"none",transition:"none"}},onMouseDown:ae=>Be(ae,M.id),onDoubleClick:()=>ee(M.id),children:[(0,Ve.jsx)("span",{className:R.sectionLabel,style:{backgroundColor:U.pill},children:M.label}),(0,Ve.jsx)("span",{className:`${R.sectionAnnotation} ${M.note?R.annotationVisible:""}`,children:(M.note&&Re.current.set(M.id,M.note),M.note||Re.current.get(M.id)||"")}),(0,Ve.jsxs)("span",{className:R.sectionDimensions,children:[Math.round(N.width)," \xD7 ",Math.round(N.height)]}),(0,Ve.jsx)("div",{className:R.deleteButton,onMouseDown:ae=>ae.stopPropagation(),onClick:()=>de(M.id),children:"\u2715"}),Fg.map(ae=>(0,Ve.jsx)("div",{className:`${R.handle} ${R[`handle${ae.charAt(0).toUpperCase()}${ae.slice(1)}`]}`,onMouseDown:X=>I(X,M.id,ae)},ae))]},M.id)}),it.map(M=>{let N=M.currentRect,$=M.isFixed?N.y:N.y-Bt,U=C.has(M.id),J=Ae(M),ae=be(M);if(a&&!U)return null;let ie=!oo.current.has(M.id);return ie&&oo.current.add(M.id),(0,Ve.jsxs)("div",{"data-rearrange-section":M.id,className:`${R.ghostOutline} ${U?R.selected:""} ${D||l||et.has(M.id)?R.exiting:""}`,style:{left:N.x,top:$,width:N.width,height:N.height,...pl?{}:{opacity:0,animation:"none",transition:"none"},...ie?{}:{animation:"none"}},onMouseDown:Ce=>Be(Ce,M.id),onDoubleClick:()=>ee(M.id),children:[(0,Ve.jsx)("span",{className:R.sectionLabel,style:{backgroundColor:Kg.pill},children:M.label}),(0,Ve.jsx)("span",{className:`${R.sectionAnnotation} ${M.note?R.annotationVisible:""}`,children:(M.note&&Re.current.set(M.id,M.note),M.note||Re.current.get(M.id)||"")}),(0,Ve.jsxs)("span",{className:R.sectionDimensions,children:[Math.round(N.width)," \xD7 ",Math.round(N.height)]}),(0,Ve.jsx)("div",{className:R.deleteButton,onMouseDown:Ce=>Ce.stopPropagation(),onClick:()=>de(M.id),children:"\u2715"}),Fg.map(Ce=>(0,Ve.jsx)("div",{className:`${R.handle} ${R[`handle${Ce.charAt(0).toUpperCase()}${Ce.slice(1)}`]}`,onMouseDown:qe=>I(qe,M.id,Ce)},Ce)),(0,Ve.jsx)("span",{className:R.ghostBadge,children:(()=>{let Ce=In.current.get(M.id);if(J&&ae){let[qe,nt]=Ce==="resize"?["Resize","Move"]:["Move","Resize"];return(0,Ve.jsxs)(Ve.Fragment,{children:["Suggested ",qe," ",(0,Ve.jsxs)("span",{className:R.ghostBadgeExtra,children:["& ",nt]})]})}return`Suggested ${ae?"Resize":"Move"}`})()})]},M.id)})]}),!a&&(()=>{let M=[];for(let N of it){let $=ao.get(N.id);M.push({id:N.id,orig:N.originalRect,target:$||N.currentRect,isFixed:N.isFixed,isSelected:C.has(N.id),isExiting:et.has(N.id)})}for(let[N,$]of ao)if(!M.some(U=>U.id===N)){let U=_.find(J=>J.id===N);U&&M.push({id:N,orig:U.originalRect,target:$,isFixed:U.isFixed,isSelected:C.has(N)})}for(let[N,$]of Rl)M.some(U=>U.id===N)||M.push({id:N,orig:$.orig,target:$.target,isFixed:$.isFixed,isSelected:!1,isExiting:!0});return M.length===0?null:(0,Ve.jsxs)("svg",{className:`${R.connectorSvg} ${D||l?R.connectorExiting:""}`,children:[M.map(({id:N,orig:$,target:U,isFixed:J,isSelected:ae,isExiting:X})=>{let ie=$.x+$.width/2,Ce=(J?$.y:$.y-Bt)+$.height/2,qe=U.x+U.width/2,nt=(J?U.y:U.y-Bt)+U.height/2,se=qe-ie,st=nt-Ce,Oe=Math.sqrt(se*se+st*st);if(Oe<2)return null;let Te=Math.min(1,Oe/40),re=Math.min(Oe*.3,60),rt=Oe>0?-st/Oe:0,Ge=Oe>0?se/Oe:0,De=(ie+qe)/2+rt*re,Fe=(Ce+nt)/2+Ge*re,xe=ao.has(N),vt=xe||ae?1:.4,tn=xe||ae?1:.5;return(0,Ve.jsxs)("g",{className:X?R.connectorExiting:"",children:[(0,Ve.jsx)("path",{className:R.connectorLine,d:`M ${ie} ${Ce} Q ${De} ${Fe} ${qe} ${nt}`,fill:"none",stroke:"rgba(59, 130, 246, 0.45)",strokeWidth:"1.5",opacity:vt*Te}),(0,Ve.jsx)("circle",{className:R.connectorDot,cx:ie,cy:Ce,r:4*Te,fill:"rgba(59, 130, 246, 0.8)",stroke:"#fff",strokeWidth:"1.5",opacity:tn*Te,filter:"url(#connDotShadow)"}),(0,Ve.jsx)("circle",{className:R.connectorDot,cx:qe,cy:nt,r:4*Te,fill:"rgba(59, 130, 246, 0.8)",stroke:"#fff",strokeWidth:"1.5",opacity:tn*Te,filter:"url(#connDotShadow)"})]},`conn-${N}`)}),(0,Ve.jsx)("defs",{children:(0,Ve.jsx)("filter",{id:"connDotShadow",x:"-50%",y:"-50%",width:"200%",height:"200%",children:(0,Ve.jsx)("feDropShadow",{dx:"0",dy:"0.5",stdDeviation:"1",floodOpacity:"0.15"})})})]})})(),E&&(()=>{let M=_.find(nt=>nt.id===E);if(!M)return null;let N=M.currentRect,$=M.isFixed?N.y:N.y-Bt,U=N.x+N.width/2,J=$-8,ae=$+N.height+8,X=J>200,ie=ae<window.innerHeight-100,Ce=Math.max(160,Math.min(window.innerWidth-160,U)),qe;return X?qe={left:Ce,bottom:window.innerHeight-J}:ie?qe={left:Ce,top:ae}:qe={left:Ce,top:Math.max(80,window.innerHeight/2-80)},(0,Ve.jsx)(Kc,{element:M.label,placeholder:"Add a note about this section",initialValue:M.note??"",submitLabel:K.current?"Save":"Set",onSubmit:he,onCancel:F,onDelete:K.current?()=>{he("")}:void 0,isExiting:oe,lightMode:!n,style:qe})})(),Pe&&(0,Ve.jsx)("div",{className:R.sizeIndicator,style:{left:Pe.x,top:Pe.y},"data-feedback-toolbar":!0,children:Pe.text}),ge.map((M,N)=>(0,Ve.jsx)("div",{className:R.guideLine,style:M.axis==="x"?{position:"fixed",left:M.pos,top:0,width:1,height:"100vh"}:{position:"fixed",left:0,top:M.pos-Bt,width:"100vw",height:1}},`${M.axis}-${M.pos}-${N}`))]})}var gf=new Set(["script","style","noscript","link","meta","br","hr"]);function yv(){let e=document.querySelector("main")||document.body,t=[],n=Array.from(e.children),l=e!==document.body&&n.length<3?Array.from(document.body.children):n;for(let o of l){if(!(o instanceof HTMLElement)||gf.has(o.tagName.toLowerCase())||o.hasAttribute("data-feedback-toolbar"))continue;let a=window.getComputedStyle(o);if(a.display==="none"||a.visibility==="hidden")continue;let i=o.getBoundingClientRect();if(!(i.height<10||i.width<10)){t.push({label:Fc(o),selector:pa(o),top:i.top,bottom:i.bottom,left:i.left,right:i.right,area:i.width*i.height});for(let s of Array.from(o.children)){if(!(s instanceof HTMLElement)||gf.has(s.tagName.toLowerCase())||s.hasAttribute("data-feedback-toolbar"))continue;let r=window.getComputedStyle(s);if(r.display==="none"||r.visibility==="hidden")continue;let p=s.getBoundingClientRect();p.height<10||p.width<10||t.push({label:Fc(s),selector:pa(s),top:p.top,bottom:p.bottom,left:p.left,right:p.right,area:p.width*p.height})}}}return t}function pv(e){let t=window.scrollY;return e.map(({label:n,selector:l,rect:o})=>{let a=o.y-t;return{label:n,selector:l,top:a,bottom:a+o.height,left:o.x,right:o.x+o.width,area:o.width*o.height}})}function bv(e){let t=window.scrollY,n=e.y-t,l=e.x;return{top:n,bottom:n+e.height,left:l,right:l+e.width,area:e.width*e.height}}function yf(e,t){let n=t?pv(t):yv(),l=bv(e),o=null,a=null,i=null,s=null,r=null;for(let C of n){if(Math.abs(C.left-l.left)<2&&Math.abs(C.top-l.top)<2&&Math.abs(C.right-C.left-e.width)<2&&Math.abs(C.bottom-C.top-e.height)<2)continue;C.left<=l.left+2&&C.right>=l.right-2&&C.top<=l.top+2&&C.bottom>=l.bottom-2&&C.area>l.area*1.5&&(!r||C.area<r._area)&&(r={label:C.label,selector:C.selector,_area:C.area});let z=l.right>C.left+5&&l.left<C.right-5,D=l.bottom>C.top+5&&l.top<C.bottom-5;if(z&&C.bottom<=l.top+5){let h=Math.round(l.top-C.bottom);(!o||h<o._dist)&&(o={label:C.label,selector:C.selector,gap:Math.max(0,h),_dist:h})}if(z&&C.top>=l.bottom-5){let h=Math.round(C.top-l.bottom);(!a||h<a._dist)&&(a={label:C.label,selector:C.selector,gap:Math.max(0,h),_dist:h})}if(D&&C.right<=l.left+5){let h=Math.round(l.left-C.right);(!i||h<i._dist)&&(i={label:C.label,selector:C.selector,gap:Math.max(0,h),_dist:h})}if(D&&C.left>=l.right-5){let h=Math.round(C.left-l.right);(!s||h<s._dist)&&(s={label:C.label,selector:C.selector,gap:Math.max(0,h),_dist:h})}}let p=window.innerWidth,f=window.innerHeight,b=vv(e,p),_=C=>C?{label:C.label,selector:C.selector,gap:C.gap}:null,w=xv(l,e,p,f,r?{label:r.label,selector:r.selector,_area:r._area}:null,n);return{above:_(o),below:_(a),left:_(i),right:_(s),alignment:b,containedIn:r?{label:r.label,selector:r.selector}:null,outOfBounds:w}}function xv(e,t,n,l,o,a){let i={},s=!1,r=[];if(e.left<-2&&r.push("left"),e.right>n+2&&r.push("right"),e.top<-2&&r.push("top"),e.bottom>l+2&&r.push("bottom"),r.length>0&&(i.viewport=r,s=!0),o){let p=a.find(f=>f.label===o.label&&f.selector===o.selector&&Math.abs(f.area-o._area)<10);if(p){let f=[];e.left<p.left-2&&f.push("left"),e.right>p.right+2&&f.push("right"),e.top<p.top-2&&f.push("top"),e.bottom>p.bottom+2&&f.push("bottom"),f.length>0&&(i.container={label:o.label,edges:f},s=!0)}}return s?i:null}function vv(e,t){if(e.width/t>.85)return"full-width";let l=e.x+e.width/2,o=t/2,a=l-o,i=t*.08;return Math.abs(a)<i?"center":a<0?"left":"right"}function Cy(e){switch(e){case"full-width":return"full-width";case"center":return"centered";case"left":return"left-aligned";case"right":return"right-aligned"}}function My(e,t={}){let n=[];e.above&&n.push(`Below \`${e.above.label}\`${e.above.gap>0?` (${e.above.gap}px gap)`:""}`),e.below&&n.push(`Above \`${e.below.label}\`${e.below.gap>0?` (${e.below.gap}px gap)`:""}`),t.includeLeftRight&&(e.left&&n.push(`Right of \`${e.left.label}\`${e.left.gap>0?` (${e.left.gap}px gap)`:""}`),e.right&&n.push(`Left of \`${e.right.label}\`${e.right.gap>0?` (${e.right.gap}px gap)`:""}`));let l=Cy(e.alignment);return e.containedIn?n.push(`${l.charAt(0).toUpperCase()+l.slice(1)} in \`${e.containedIn.label}\``):n.push(`${l.charAt(0).toUpperCase()+l.slice(1)} in page`),t.includePixelRef&&t.pixelRef&&n.push(`Pixel ref: \`${t.pixelRef}\``),e.outOfBounds&&(e.outOfBounds.viewport&&n.push(`**Outside viewport** (${e.outOfBounds.viewport.join(", ")} edge${e.outOfBounds.viewport.length>1?"s":""})`),e.outOfBounds.container&&n.push(`**Outside \`${e.outOfBounds.container.label}\`** (${e.outOfBounds.container.edges.join(", ")} edge${e.outOfBounds.container.edges.length>1?"s":""})`)),n}function wv(e,t,n){let l=[];e.above&&l.push(`below \`${e.above.label}\``),e.below&&l.push(`above \`${e.below.label}\``),e.left&&l.push(`right of \`${e.left.label}\``),e.right&&l.push(`left of \`${e.right.label}\``),e.containedIn&&l.push(`inside \`${e.containedIn.label}\``),l.push(Cy(e.alignment)),e.outOfBounds?.viewport&&l.push(`**outside viewport** (${e.outOfBounds.viewport.join(", ")})`),e.outOfBounds?.container&&l.push(`**outside \`${e.outOfBounds.container.label}\`** (${e.outOfBounds.container.edges.join(", ")})`);let o=n?`, ${Math.round(n.width)}\xD7${Math.round(n.height)}px`:"";return`at (${Math.round(t.x)}, ${Math.round(t.y)})${o}: ${l.join(", ")}`}var ty=15;function ny(e){if(e.length<2)return[];let t=[],n=new Set;for(let l=0;l<e.length;l++){if(n.has(l))continue;let o=[l];for(let a=l+1;a<e.length;a++)n.has(a)||Math.abs(e[l].rect.y-e[a].rect.y)<ty&&o.push(a);if(o.length>=2){let a=o.map(r=>e[r]);a.sort((r,p)=>r.rect.x-p.rect.x);let i=[];for(let r=0;r<a.length-1;r++)i.push(Math.round(a[r+1].rect.x-(a[r].rect.x+a[r].rect.width)));let s=Math.round(a.reduce((r,p)=>r+p.rect.y,0)/a.length);t.push({labels:a.map(r=>r.label),type:"row",sharedEdge:s,gaps:i,avgGap:i.length?Math.round(i.reduce((r,p)=>r+p,0)/i.length):0}),o.forEach(r=>n.add(r))}}for(let l=0;l<e.length;l++){if(n.has(l))continue;let o=[l];for(let a=l+1;a<e.length;a++)n.has(a)||Math.abs(e[l].rect.x-e[a].rect.x)<ty&&o.push(a);if(o.length>=2){let a=o.map(r=>e[r]);a.sort((r,p)=>r.rect.y-p.rect.y);let i=[];for(let r=0;r<a.length-1;r++)i.push(Math.round(a[r+1].rect.y-(a[r].rect.y+a[r].rect.height)));let s=Math.round(a.reduce((r,p)=>r+p.rect.x,0)/a.length);t.push({labels:a.map(r=>r.label),type:"column",sharedEdge:s,gaps:i,avgGap:i.length?Math.round(i.reduce((r,p)=>r+p,0)/i.length):0}),o.forEach(r=>n.add(r))}}return t}function kv(e){if(e.length<2)return[];let t=ny(e.map(i=>({label:i.label,rect:i.originalRect}))),n=ny(e.map(i=>({label:i.label,rect:i.currentRect}))),l=[],o=new Set;for(let i of t){let s=new Set(i.labels),r=null,p=0;for(let f of n){let b=f.labels.filter(_=>s.has(_)).length;b>=2&&b>p&&(r=f,p=b)}if(r){let f=r.labels.filter(_=>s.has(_)),b=f.join(", ");if(r.type!==i.type){let _=i.type==="row"?"y":"x",w=r.type==="row"?"y":"x";l.push(`**${b}**: ${i.type} (${_}\u2248${i.sharedEdge}, ${i.avgGap}px gaps) \u2192 ${r.type} (${w}\u2248${r.sharedEdge}, ${r.avgGap}px gaps)`)}else if(Math.abs(i.sharedEdge-r.sharedEdge)>20||Math.abs(i.avgGap-r.avgGap)>5){let _=i.type==="row"?"y":"x",w=Math.abs(i.sharedEdge-r.sharedEdge)>20?` ${_}: ${i.sharedEdge} \u2192 ${r.sharedEdge}`:"",C=Math.abs(i.avgGap-r.avgGap)>5?` gaps: ${i.avgGap}px \u2192 ${r.avgGap}px`:"";l.push(`**${b}**: ${i.type} shifted \u2014${w}${C}`)}f.forEach(_=>o.add(_))}else{let f=i.labels.join(", "),b=i.type==="row"?"y":"x";l.push(`**${f}**: ${i.type} (${b}\u2248${i.sharedEdge}) dissolved`),i.labels.forEach(_=>o.add(_))}}for(let i of n){if(i.labels.every(p=>o.has(p))||i.labels.filter(p=>!o.has(p)).length<2)continue;if(!t.some(p=>p.labels.filter(b=>i.labels.includes(b)).length>=2)){let p=i.type==="row"?"y":"x";l.push(`**${i.labels.join(", ")}**: new ${i.type} (${p}\u2248${i.sharedEdge}, ${i.avgGap}px gaps)`),i.labels.forEach(f=>o.add(f))}}let a=e.filter(i=>!o.has(i.label));if(a.length>=2){let i={};for(let s of a){let r=Math.round(s.currentRect.x/5)*5;(i[r]??(i[r]=[])).push(s.label)}for(let[s,r]of Object.entries(i))r.length>=2&&l.push(`**${r.join(", ")}**: shared left edge at x\u2248${s}`)}return l}function Ey(e){if(typeof document>"u")return{viewport:e,contentArea:null};let t=[],n=new Set,l=s=>{n.has(s)||s instanceof HTMLElement&&(s.hasAttribute("data-feedback-toolbar")||gf.has(s.tagName.toLowerCase())||(n.add(s),t.push(s)))},o=document.querySelector("main");o&&l(o);let a=document.querySelector("[role='main']");a&&l(a);for(let s of Array.from(document.body.children))if(l(s),s.children){for(let r of Array.from(s.children))if(l(r),r.children)for(let p of Array.from(r.children))l(p)}let i=null;for(let s of t){let r=s.getBoundingClientRect();if(r.height<50)continue;let p=getComputedStyle(s);if(p.maxWidth&&p.maxWidth!=="none"&&p.maxWidth!=="0px"){(!i||r.width<i.rect.width)&&(i={el:s,rect:r});continue}!i&&r.width<e.width-20&&r.width>100&&(i={el:s,rect:r})}if(i){let{el:s,rect:r}=i;return{viewport:e,contentArea:{width:Math.round(r.width),left:Math.round(r.left),right:Math.round(r.right),centerX:Math.round(r.left+r.width/2),selector:pa(s)}}}return{viewport:e,contentArea:null}}function Sv(e){if(typeof document>"u")return null;let t=document.querySelector(e);if(!t?.parentElement)return null;let n=getComputedStyle(t.parentElement),l={parentDisplay:n.display,parentSelector:pa(t.parentElement)};return n.display.includes("flex")&&(l.flexDirection=n.flexDirection),n.display.includes("grid")&&n.gridTemplateColumns!=="none"&&(l.gridCols=n.gridTemplateColumns),n.gap&&n.gap!=="normal"&&n.gap!=="0px"&&(l.gap=n.gap),l}function Ty(e,t){let n=t.contentArea,l=n?n.width:t.viewport.width,o=n?n.left:0,a=n?n.centerX:Math.round(t.viewport.width/2),i=Math.round(e.x-o),s=Math.round(o+l-(e.x+e.width)),r=(e.width/l*100).toFixed(1),p=e.x+e.width/2,f=Math.abs(p-a)<20,b=e.width/l>.95,_=[];return b?_.push("`width: 100%` of container"):_.push(`left \`${i}px\` in container, right \`${s}px\`, width \`${r}%\` (\`${Math.round(e.width)}px\`)`),f&&!b&&_.push("centered \u2014 `margin-inline: auto`"),_.join(" \u2014 ")}function Dy(e){let{viewport:t,contentArea:n}=e,l=`### Reference Frame
`;if(l+=`- Viewport: \`${t.width}\xD7${t.height}px\`
`,n){let o=n;l+=`- Content area: \`${o.width}px\` wide, left edge at \`x=${o.left}\`, right at \`x=${o.right}\` (\`${o.selector}\`)
`,l+=`- Pixel \u2192 CSS translation:
`,l+=`  - **Horizontal position in container**: \`element.x - ${o.left}\` \u2192 use as \`margin-left\` or \`left\`
`,l+=`  - **Width as % of container**: \`element.width / ${o.width} \xD7 100\` \u2192 use as \`width: X%\`
`,l+="  - **Vertical gap between elements**: `nextElement.y - (prevElement.y + prevElement.height)` \u2192 use as `margin-top` or `gap`\n",l+=`  - **Centered**: if \`|element.centerX - ${o.centerX}| < 20px\` \u2192 use \`margin-inline: auto\`
`}else l+=`- No distinct content container \u2014 elements positioned relative to full viewport
`,l+=`- Pixel \u2192 CSS translation:
`,l+=`  - **Width as % of viewport**: \`element.width / ${t.width} \xD7 100\` \u2192 use as \`width: X%\`
`,l+=`  - **Centered**: if \`|(element.x + element.width/2) - ${Math.round(t.width/2)}| < 20px\` \u2192 use \`margin-inline: auto\`
`;return l+=`
`,l}function Cv(e){let t=Sv(e);if(!t)return null;let n=`\`${t.parentDisplay}\``;return t.flexDirection&&(n+=`, flex-direction: \`${t.flexDirection}\``),t.gridCols&&(n+=`, grid-template-columns: \`${t.gridCols}\``),t.gap&&(n+=`, gap: \`${t.gap}\``),`Parent: ${n} (\`${t.parentSelector}\`)`}function ly(e,t,n,l="standard"){if(e.length===0)return"";let o=[...e].sort((D,h)=>Math.abs(D.y-h.y)<20?D.x-h.x:D.y-h.y),a="";if(n?.blankCanvas?(a+=`## Wireframe: New Page

`,n.wireframePurpose&&(a+=`> **Purpose:** ${n.wireframePurpose}
>
`),a+=`> ${e.length} component${e.length!==1?"s":""} placed \u2014 this is a standalone wireframe, not related to the current page.
>
> This wireframe is a rough sketch for exploring ideas.

`):a+=`## Design Layout

> ${e.length} component${e.length!==1?"s":""} placed

`,l==="compact")return a+=`### Components
`,o.forEach((D,h)=>{let y=gl[D.type]?.label||D.type;a+=`${h+1}. **${y}** \u2014 \`${Math.round(D.width)}\xD7${Math.round(D.height)}px\` at \`(${Math.round(D.x)}, ${Math.round(D.y)})\`
`}),a;let i=Ey(t);a+=Dy(i),a+=`### Components
`,o.forEach((D,h)=>{let y=gl[D.type]?.label||D.type,k={x:D.x,y:D.y,width:D.width,height:D.height};a+=`${h+1}. **${y}** \u2014 \`${Math.round(D.width)}\xD7${Math.round(D.height)}px\` at \`(${Math.round(D.x)}, ${Math.round(D.y)})\`
`;let E=yf(k),oe=My(E,{includeLeftRight:l==="detailed"||l==="forensic"});for(let K of oe)a+=`   - ${K}
`;let L=Ty(k,i);L&&(a+=`   - CSS: ${L}
`)}),a+=`
### Layout Analysis
`;let s=[];for(let D of o){let h=s.find(y=>Math.abs(y.y-D.y)<30);h?h.items.push(D):s.push({y:D.y,items:[D]})}if(s.sort((D,h)=>D.y-h.y),s.forEach((D,h)=>{D.items.sort((k,E)=>k.x-E.x);let y=D.items.map(k=>gl[k.type]?.label||k.type);if(D.items.length===1){let E=D.items[0].width>t.width*.8;a+=`- Row ${h+1} (y\u2248${Math.round(D.y)}): ${y[0]}${E?" \u2014 full width":""}
`}else a+=`- Row ${h+1} (y\u2248${Math.round(D.y)}): ${y.join(" | ")} \u2014 ${D.items.length} items side by side
`}),l==="detailed"||l==="forensic"){a+=`
### Spacing & Gaps
`;for(let D=0;D<o.length-1;D++){let h=o[D],y=o[D+1],k=gl[h.type]?.label||h.type,E=gl[y.type]?.label||y.type,Q=Math.round(y.y-(h.y+h.height)),oe=Math.round(y.x-(h.x+h.width));Math.abs(h.y-y.y)<30?a+=`- ${k} \u2192 ${E}: \`${oe}px\` horizontal gap
`:a+=`- ${k} \u2192 ${E}: \`${Q}px\` vertical gap
`}if(l==="forensic"&&o.length>2){a+=`
### All Pairwise Gaps
`;for(let D=0;D<o.length;D++)for(let h=D+1;h<o.length;h++){let y=o[D],k=o[h],E=gl[y.type]?.label||y.type,Q=gl[k.type]?.label||k.type,oe=Math.round(k.y-(y.y+y.height)),L=Math.round(k.x-(y.x+y.width));a+=`- ${E} \u2194 ${Q}: h=\`${L}px\` v=\`${oe}px\`
`}}l==="forensic"&&(a+=`
### Z-Order (placement order)
`,e.forEach((D,h)=>{let y=gl[D.type]?.label||D.type;a+=`${h}. ${y} at \`(${Math.round(D.x)}, ${Math.round(D.y)})\`
`}))}a+=`
### Suggested Implementation
`;let r=o.some(D=>D.type==="navigation"),p=o.some(D=>D.type==="hero"),f=o.some(D=>D.type==="sidebar"),b=o.some(D=>D.type==="footer"),_=o.filter(D=>D.type==="card"),w=o.filter(D=>D.type==="form"),C=o.filter(D=>D.type==="table"),z=o.filter(D=>D.type==="modal");if(r&&(a+=`- Top navigation bar with logo + nav links + CTA
`),p&&(a+=`- Hero section with heading, subtext, and call-to-action
`),f&&(a+=`- Sidebar layout \u2014 use CSS Grid with sidebar + main content area
`),_.length>1?a+=`- ${_.length}-column card grid \u2014 use CSS Grid or Flexbox
`:_.length===1&&(a+=`- Card component with image + content area
`),w.length>0&&(a+=`- ${w.length} form${w.length>1?"s":""} \u2014 add proper labels, validation, and submit handling
`),C.length>0&&(a+=`- Data table \u2014 consider sortable columns and pagination
`),z.length>0&&(a+=`- Modal dialog \u2014 add overlay backdrop and focus trapping
`),b&&(a+=`- Multi-column footer with links
`),l==="detailed"||l==="forensic"){if(a+=`
### CSS Suggestions
`,f){let D=o.find(h=>h.type==="sidebar");a+=`- \`display: grid; grid-template-columns: ${Math.round(D.width)}px 1fr;\`
`}if(_.length>1){let D=Math.round(_[0].width);a+=`- \`display: grid; grid-template-columns: repeat(${_.length}, ${D}px); gap: 16px;\`
`}r&&(a+="- Navigation: `position: sticky; top: 0; z-index: 50;`\n")}return a}function oy(e,t="standard",n){let{sections:l}=e,o=[];for(let f of l){let b=f.originalRect,_=f.currentRect,w=Math.abs(b.x-_.x)>1||Math.abs(b.y-_.y)>1,C=Math.abs(b.width-_.width)>1||Math.abs(b.height-_.height)>1;if(!w&&!C){t==="forensic"&&o.push({section:f,posMoved:!1,sizeChanged:!1});continue}o.push({section:f,posMoved:w,sizeChanged:C})}if(o.length===0||t!=="forensic"&&o.every(f=>!f.posMoved&&!f.sizeChanged))return"";let a=`## Suggested Layout Changes

`,i=n?n.width:typeof window<"u"?window.innerWidth:0,s=n?n.height:typeof window<"u"?window.innerHeight:0,r=Ey({width:i,height:s});t!=="compact"&&(a+=Dy(r)),t==="forensic"&&(a+=`> Detected at: \`${new Date(e.detectedAt).toISOString()}\`
`,a+=`> Total sections: ${l.length}

`);let p=f=>l.map(b=>({label:b.label,selector:b.selector,rect:f==="original"?b.originalRect:b.currentRect}));a+=`**Changes:**
`;for(let{section:f,posMoved:b,sizeChanged:_}of o){let w=f.originalRect,C=f.currentRect;if(!b&&!_){a+=`- ${f.label} \u2014 unchanged at (${Math.round(C.x)}, ${Math.round(C.y)}) ${Math.round(C.width)}\xD7${Math.round(C.height)}px
`;continue}if(t==="compact"){b&&_?a+=`- Suggested: move **${f.label}** to (${Math.round(C.x)}, ${Math.round(C.y)}) ${Math.round(C.width)}\xD7${Math.round(C.height)}px
`:b?a+=`- Suggested: move **${f.label}** to (${Math.round(C.x)}, ${Math.round(C.y)})
`:a+=`- Suggested: resize **${f.label}** to ${Math.round(C.width)}\xD7${Math.round(C.height)}px
`;continue}if(b&&_?a+=`- Suggested: move and resize **${f.label}**
`:b?a+=`- Suggested: move **${f.label}**
`:a+=`- Suggested: resize **${f.label}** from ${Math.round(w.width)}\xD7${Math.round(w.height)}px to ${Math.round(C.width)}\xD7${Math.round(C.height)}px
`,b){let D=yf(w,p("original")),h=yf(C,p("current")),y=_?{width:w.width,height:w.height}:void 0;a+=`  - Currently ${wv(D,{x:w.x,y:w.y},y)}
`;let k=_?{width:C.width,height:C.height}:void 0,E=`at (${Math.round(C.x)}, ${Math.round(C.y)})`,Q=k?`, ${Math.round(k.width)}\xD7${Math.round(k.height)}px`:"",L=My(h,{includeLeftRight:t==="detailed"||t==="forensic"});if(L.length>0){a+=`  - Suggested position ${E}${Q}: ${L[0]}
`;for(let ee=1;ee<L.length;ee++)a+=`    ${L[ee]}
`}else a+=`  - Suggested position ${E}${Q}
`;let K=Ty(C,r);K&&(a+=`  - CSS: ${K}
`)}let z=Cv(f.selector);if(z&&(a+=`  - ${z}
`),a+=`  - Selector: \`${f.selector}\`
`,t==="detailed"||t==="forensic"){let D=f.className?`${f.tagName}.${f.className.split(" ")[0]}`:f.tagName;D!==f.selector&&(a+=`  - Element: \`${D}\`
`),f.role&&(a+=`  - Role: \`${f.role}\`
`),t==="forensic"&&f.textSnippet&&(a+=`  - Text: "${f.textSnippet}"
`)}t==="forensic"&&(a+=`  - Original rect: \`{ x: ${Math.round(w.x)}, y: ${Math.round(w.y)}, w: ${Math.round(w.width)}, h: ${Math.round(w.height)} }\`
`,a+=`  - Current rect: \`{ x: ${Math.round(C.x)}, y: ${Math.round(C.y)}, w: ${Math.round(C.width)}, h: ${Math.round(C.height)} }\`
`)}if(t!=="compact"){let f=o.filter(_=>_.posMoved).map(_=>({label:_.section.label,originalRect:_.section.originalRect,currentRect:_.section.currentRect})),b=kv(f);if(b.length>0){a+=`
### Layout Summary
`;for(let _ of b)a+=`- ${_}
`}}if(t!=="compact"&&l.length>1){a+=`
### All Sections (current positions)
`;let f=[...l].sort((b,_)=>Math.abs(b.currentRect.y-_.currentRect.y)<20?b.currentRect.x-_.currentRect.x:b.currentRect.y-_.currentRect.y);for(let b of f){let _=b.currentRect,w=Math.abs(_.x-b.originalRect.x)>1||Math.abs(_.y-b.originalRect.y)>1||Math.abs(_.width-b.originalRect.width)>1||Math.abs(_.height-b.originalRect.height)>1;a+=`- ${b.label}: \`${Math.round(_.width)}\xD7${Math.round(_.height)}px\` at \`(${Math.round(_.x)}, ${Math.round(_.y)})\`${w?" \u2190 suggested":""}
`}}return a}var pf="feedback-annotations-",Ny=7;function Jc(e){return`${pf}${e}`}function lf(e){if(typeof window>"u")return[];try{let t=localStorage.getItem(Jc(e));if(!t)return[];let n=JSON.parse(t),l=Date.now()-Ny*24*60*60*1e3;return n.filter(o=>!o.timestamp||o.timestamp>l)}catch{return[]}}function zy(e,t){if(!(typeof window>"u"))try{localStorage.setItem(Jc(e),JSON.stringify(t))}catch{}}function Mv(){let e=new Map;if(typeof window>"u")return e;try{let t=Date.now()-Ny*24*60*60*1e3;for(let n=0;n<localStorage.length;n++){let l=localStorage.key(n);if(l?.startsWith(pf)){let o=l.slice(pf.length),a=localStorage.getItem(l);if(a){let s=JSON.parse(a).filter(r=>!r.timestamp||r.timestamp>t);s.length>0&&e.set(o,s)}}}}catch{}return e}function js(e,t,n){let l=t.map(o=>({...o,_syncedTo:n}));zy(e,l)}var vf="agentation-design-";function Ev(e){if(typeof window>"u")return[];try{let t=localStorage.getItem(`${vf}${e}`);return t?JSON.parse(t):[]}catch{return[]}}function Tv(e,t){if(!(typeof window>"u"))try{localStorage.setItem(`${vf}${e}`,JSON.stringify(t))}catch{}}function Dv(e){if(!(typeof window>"u"))try{localStorage.removeItem(`${vf}${e}`)}catch{}}var wf="agentation-rearrange-";function Nv(e){if(typeof window>"u")return null;try{let t=localStorage.getItem(`${wf}${e}`);return t?JSON.parse(t):null}catch{return null}}function zv(e,t){if(!(typeof window>"u"))try{localStorage.setItem(`${wf}${e}`,JSON.stringify(t))}catch{}}function Av(e){if(!(typeof window>"u"))try{localStorage.removeItem(`${wf}${e}`)}catch{}}var kf="agentation-wireframe-";function Lv(e){if(typeof window>"u")return null;try{let t=localStorage.getItem(`${kf}${e}`);return t?JSON.parse(t):null}catch{return null}}function ay(e,t){if(!(typeof window>"u"))try{localStorage.setItem(`${kf}${e}`,JSON.stringify(t))}catch{}}function Wc(e){if(!(typeof window>"u"))try{localStorage.removeItem(`${kf}${e}`)}catch{}}var Ay="agentation-session-";function Sf(e){return`${Ay}${e}`}function Rv(e){if(typeof window>"u")return null;try{return localStorage.getItem(Sf(e))}catch{return null}}function of(e,t){if(!(typeof window>"u"))try{localStorage.setItem(Sf(e),t)}catch{}}function Bv(e){if(!(typeof window>"u"))try{localStorage.removeItem(Sf(e))}catch{}}var bf=`${Ay}toolbar-hidden`;function Ov(){if(typeof window>"u")return!1;try{return sessionStorage.getItem(bf)==="1"}catch{return!1}}function $v(e){if(!(typeof window>"u"))try{e?sessionStorage.setItem(bf,"1"):sessionStorage.removeItem(bf)}catch{}}async function af(e,t){let n=await fetch(`${e}/sessions`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:t})});if(!n.ok)throw new Error(`Failed to create session: ${n.status}`);return n.json()}async function iy(e,t){let n=await fetch(`${e}/sessions/${t}`);if(!n.ok)throw new Error(`Failed to get session: ${n.status}`);return n.json()}async function xi(e,t,n){let l=await fetch(`${e}/sessions/${t}/annotations`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!l.ok)throw new Error(`Failed to sync annotation: ${l.status}`);return l.json()}async function sy(e,t,n){let l=await fetch(`${e}/annotations/${t}`,{method:"PATCH",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!l.ok)throw new Error(`Failed to update annotation: ${l.status}`);return l.json()}async function Ho(e,t){let n=await fetch(`${e}/annotations/${t}`,{method:"DELETE"});if(!n.ok)throw new Error(`Failed to delete annotation: ${n.status}`)}var at={FunctionComponent:0,ClassComponent:1,IndeterminateComponent:2,HostRoot:3,HostPortal:4,HostComponent:5,HostText:6,Fragment:7,Mode:8,ContextConsumer:9,ContextProvider:10,ForwardRef:11,Profiler:12,SuspenseComponent:13,MemoComponent:14,SimpleMemoComponent:15,LazyComponent:16,IncompleteClassComponent:17,DehydratedFragment:18,SuspenseListComponent:19,ScopeComponent:21,OffscreenComponent:22,LegacyHiddenComponent:23,CacheComponent:24,TracingMarkerComponent:25,HostHoistable:26,HostSingleton:27,IncompleteFunctionComponent:28,Throw:29,ViewTransitionComponent:30,ActivityComponent:31},ry=new Set(["Component","PureComponent","Fragment","Suspense","Profiler","StrictMode","Routes","Route","Outlet","Root","ErrorBoundaryHandler","HotReload","Hot"]),cy=[/Boundary$/,/BoundaryHandler$/,/Provider$/,/Consumer$/,/^(Inner|Outer)/,/Router$/,/^Client(Page|Segment|Root)/,/^Segment(ViewNode|Node)$/,/^LayoutSegment/,/^Server(Root|Component|Render)/,/^RSC/,/Context$/,/^Hot(Reload)?$/,/^(Dev|React)(Overlay|Tools|Root)/,/Overlay$/,/Handler$/,/^With[A-Z]/,/Wrapper$/,/^Root$/],Hv=[/Page$/,/View$/,/Screen$/,/Section$/,/Card$/,/List$/,/Item$/,/Form$/,/Modal$/,/Dialog$/,/Button$/,/Nav$/,/Header$/,/Footer$/,/Layout$/,/Panel$/,/Tab$/,/Menu$/];function Uv(e){let t=e?.mode??"filtered",n=ry;if(e?.skipExact){let l=e.skipExact instanceof Set?e.skipExact:new Set(e.skipExact);n=new Set([...ry,...l])}return{maxComponents:e?.maxComponents??6,maxDepth:e?.maxDepth??30,mode:t,skipExact:n,skipPatterns:e?.skipPatterns?[...cy,...e.skipPatterns]:cy,userPatterns:e?.userPatterns??Hv,filter:e?.filter}}function Yv(e){return e.replace(/([a-z])([A-Z])/g,"$1-$2").replace(/([A-Z])([A-Z][a-z])/g,"$1-$2").toLowerCase()}function jv(e,t=10){let n=new Set,l=e,o=0;for(;l&&o<t;)l.className&&typeof l.className=="string"&&l.className.split(/\s+/).forEach(a=>{if(a.length>1){let i=a.replace(/[_][a-zA-Z0-9]{5,}.*$/,"").toLowerCase();i.length>1&&n.add(i)}}),l=l.parentElement,o++;return n}function Xv(e,t){let n=Yv(e);for(let l of t){if(l===n)return!0;let o=n.split("-").filter(i=>i.length>2),a=l.split("-").filter(i=>i.length>2);for(let i of o)for(let s of a)if(i===s||i.includes(s)||s.includes(i))return!0}return!1}function Iv(e,t,n,l){if(n.filter)return n.filter(e,t);switch(n.mode){case"all":return!0;case"filtered":return!(n.skipExact.has(e)||n.skipPatterns.some(o=>o.test(e)));case"smart":return n.skipExact.has(e)||n.skipPatterns.some(o=>o.test(e))?!1:!!(l&&Xv(e,l)||n.userPatterns.some(o=>o.test(e)));default:return!0}}var vi=null,qv=new WeakMap;function sf(e){return Object.keys(e).some(t=>t.startsWith("__reactFiber$")||t.startsWith("__reactInternalInstance$")||t.startsWith("__reactProps$"))}function Qv(){if(vi!==null)return vi;if(typeof document>"u")return!1;if(document.body&&sf(document.body))return vi=!0,!0;let e=["#root","#app","#__next","[data-reactroot]"];for(let t of e){let n=document.querySelector(t);if(n&&sf(n))return vi=!0,!0}if(document.body){for(let t of document.body.children)if(sf(t))return vi=!0,!0}return vi=!1,!1}var Xs={map:qv};function Wv(e){return Object.keys(e).find(n=>n.startsWith("__reactFiber$")||n.startsWith("__reactInternalInstance$"))||null}function Gv(e){let t=Wv(e);return t?e[t]:null}function fa(e){return e?e.displayName?e.displayName:e.name?e.name:null:null}function Vv(e){let{tag:t,type:n,elementType:l}=e;if(t===at.HostComponent||t===at.HostText||t===at.HostHoistable||t===at.HostSingleton||t===at.Fragment||t===at.Mode||t===at.Profiler||t===at.DehydratedFragment||t===at.HostRoot||t===at.HostPortal||t===at.ScopeComponent||t===at.OffscreenComponent||t===at.LegacyHiddenComponent||t===at.CacheComponent||t===at.TracingMarkerComponent||t===at.Throw||t===at.ViewTransitionComponent||t===at.ActivityComponent)return null;if(t===at.ForwardRef){let o=l;if(o?.render){let a=fa(o.render);if(a)return a}return o?.displayName?o.displayName:fa(n)}if(t===at.MemoComponent||t===at.SimpleMemoComponent){let o=l;if(o?.type){let a=fa(o.type);if(a)return a}return o?.displayName?o.displayName:fa(n)}if(t===at.ContextProvider){let o=n;return o?._context?.displayName?`${o._context.displayName}.Provider`:null}if(t===at.ContextConsumer){let o=n;return o?.displayName?`${o.displayName}.Consumer`:null}if(t===at.LazyComponent){let o=l;return o?._status===1&&o._result?fa(o._result):null}return t===at.SuspenseComponent||t===at.SuspenseListComponent?null:t===at.IncompleteClassComponent||t===at.IncompleteFunctionComponent||t===at.FunctionComponent||t===at.ClassComponent||t===at.IndeterminateComponent?fa(n):null}function Zv(e){return e.length<=2||e.length<=3&&e===e.toLowerCase()}function Kv(e,t){let n=Uv(t),l=n.mode==="all";if(l){let r=Xs.map.get(e);if(r!==void 0)return r}if(!Qv()){let r={path:null,components:[]};return l&&Xs.map.set(e,r),r}let o=n.mode==="smart"?jv(e):void 0,a=[];try{let r=Gv(e),p=0;for(;r&&p<n.maxDepth&&a.length<n.maxComponents;){let f=Vv(r);f&&!Zv(f)&&Iv(f,p,n,o)&&a.push(f),r=r.return,p++}}catch{let r={path:null,components:[]};return l&&Xs.map.set(e,r),r}if(a.length===0){let r={path:null,components:[]};return l&&Xs.map.set(e,r),r}let s={path:a.slice().reverse().map(r=>`<${r}>`).join(" "),components:a};return l&&Xs.map.set(e,s),s}var Is={FunctionComponent:0,ClassComponent:1,IndeterminateComponent:2,HostRoot:3,HostPortal:4,HostComponent:5,HostText:6,Fragment:7,Mode:8,ContextConsumer:9,ContextProvider:10,ForwardRef:11,Profiler:12,SuspenseComponent:13,MemoComponent:14,SimpleMemoComponent:15,LazyComponent:16};function Fv(e){if(!e||typeof e!="object")return null;let t=Object.keys(e),n=t.find(a=>a.startsWith("__reactFiber$"));if(n)return e[n]||null;let l=t.find(a=>a.startsWith("__reactInternalInstance$"));if(l)return e[l]||null;let o=t.find(a=>{if(!a.startsWith("__react"))return!1;let i=e[a];return i&&typeof i=="object"&&"_debugSource"in i});return o&&e[o]||null}function Ws(e){if(!e.type||typeof e.type=="string")return null;if(typeof e.type=="object"||typeof e.type=="function"){let t=e.type;if(t.displayName)return t.displayName;if(t.name)return t.name}return null}function Jv(e,t=50){let n=e,l=0;for(;n&&l<t;){if(n._debugSource)return{source:n._debugSource,componentName:Ws(n)};if(n._debugOwner?._debugSource)return{source:n._debugOwner._debugSource,componentName:Ws(n._debugOwner)};n=n.return,l++}return null}function Pv(e){let t=e,n=0,l=50;for(;t&&n<l;){let o=t,a=["_debugSource","__source","_source","debugSource"];for(let i of a){let s=o[i];if(s&&typeof s=="object"&&"fileName"in s)return{source:s,componentName:Ws(t)}}if(t.memoizedProps){let i=t.memoizedProps;if(i.__source&&typeof i.__source=="object"){let s=i.__source;if(s.fileName&&s.lineNumber)return{source:{fileName:s.fileName,lineNumber:s.lineNumber,columnNumber:s.columnNumber},componentName:Ws(t)}}}t=t.return,n++}return null}var Gc=new Map;function e4(e){let t=e.tag,n=e.type,l=e.elementType;if(typeof n=="string"||n==null||typeof n=="function"&&n.prototype?.isReactComponent)return null;if((t===Is.FunctionComponent||t===Is.IndeterminateComponent)&&typeof n=="function")return n;if(t===Is.ForwardRef&&l){let o=l.render;if(typeof o=="function")return o}if((t===Is.MemoComponent||t===Is.SimpleMemoComponent)&&l){let o=l.type;if(typeof o=="function")return o}return typeof n=="function"?n:null}function t4(){let e=Ly.default,t=e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;if(t&&"H"in t)return{get:()=>t.H,set:l=>{t.H=l}};let n=e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;if(n){let l=n.ReactCurrentDispatcher;if(l&&"current"in l)return{get:()=>l.current,set:o=>{l.current=o}}}return null}function n4(e){let t=e.split(`
`),n=[/source-location/,/\/dist\/index\./,/node_modules\//,/react-dom/,/react\.development/,/react\.production/,/chunk-[A-Z0-9]+/i,/react-stack-bottom-frame/,/react-reconciler/,/scheduler/,/<anonymous>/],l=/^\s*at\s+(?:.*?\s+\()?(.+?):(\d+):(\d+)\)?$/,o=/^[^@]*@(.+?):(\d+):(\d+)$/;for(let a of t){let i=a.trim();if(!i||n.some(r=>r.test(i)))continue;let s=l.exec(i)||o.exec(i);if(s)return{fileName:s[1],line:parseInt(s[2],10),column:parseInt(s[3],10)}}return null}function l4(e){let t=e;return t=t.replace(/[?#].*$/,""),t=t.replace(/^turbopack:\/\/\/\[project\]\//,""),t=t.replace(/^webpack-internal:\/\/\/\.\//,""),t=t.replace(/^webpack-internal:\/\/\//,""),t=t.replace(/^webpack:\/\/\/\.\//,""),t=t.replace(/^webpack:\/\/\//,""),t=t.replace(/^turbopack:\/\/\//,""),t=t.replace(/^https?:\/\/[^/]+\//,""),t=t.replace(/^file:\/\/\//,"/"),t=t.replace(/^\([^)]+\)\/\.\//,""),t=t.replace(/^\.\//,""),t}function o4(e){let t=e4(e);if(!t)return null;if(Gc.has(t))return Gc.get(t);let n=t4();if(!n)return Gc.set(t,null),null;let l=n.get(),o=null;try{let a=new Proxy({},{get(){throw new Error("probe")}});n.set(a);try{t({})}catch(i){if(i instanceof Error&&i.message==="probe"&&i.stack){let s=n4(i.stack);s&&(o={fileName:l4(s.fileName),lineNumber:s.line,columnNumber:s.column,componentName:Ws(e)||void 0})}}}finally{n.set(l)}return Gc.set(t,o),o}function a4(e,t=15){let n=e,l=0;for(;n&&l<t;){let o=o4(n);if(o)return o;n=n.return,l++}return null}function xf(e){let t=Fv(e);if(!t)return{found:!1,reason:"no-fiber",isReactApp:!1,isProduction:!1};let n=Jv(t);if(n||(n=Pv(t)),n?.source)return{found:!0,source:{fileName:n.source.fileName,lineNumber:n.source.lineNumber,columnNumber:n.source.columnNumber,componentName:n.componentName||void 0},isReactApp:!0,isProduction:!1};let l=a4(t);return l?{found:!0,source:l,isReactApp:!0,isProduction:!1}:{found:!1,reason:"no-debug-source",isReactApp:!0,isProduction:!1}}function i4(e,t="path"){let{fileName:n,lineNumber:l,columnNumber:o}=e,a=`${n}:${l}`;return o!==void 0&&(a+=`:${o}`),t==="vscode"?`vscode://file${n.startsWith("/")?"":"/"}${a}`:a}function s4(e,t=10){let n=e,l=0;for(;n&&l<t;){let o=xf(n);if(o.found)return o;n=n.parentElement,l++}return xf(e)}var r4=`.styles-module__toolbar___wNsdK svg[fill=none],
.styles-module__markersLayer___-25j1 svg[fill=none],
.styles-module__fixedMarkersLayer___ffyX6 svg[fill=none] {
  fill: none !important;
}
.styles-module__toolbar___wNsdK svg[fill=none] :not([fill]),
.styles-module__markersLayer___-25j1 svg[fill=none] :not([fill]),
.styles-module__fixedMarkersLayer___ffyX6 svg[fill=none] :not([fill]) {
  fill: none !important;
}

.styles-module__controlsContent___9GJWU :where(button, input, select, textarea, label) {
  background: unset;
  border: unset;
  border-radius: unset;
  padding: unset;
  margin: unset;
  color: unset;
  font-family: unset;
  font-weight: unset;
  font-style: unset;
  line-height: unset;
  letter-spacing: unset;
  text-transform: unset;
  text-decoration: unset;
  box-shadow: unset;
  outline: unset;
}

@keyframes styles-module__toolbarEnter___u8RRu {
  from {
    opacity: 0;
    transform: scale(0.5) rotate(90deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}
@keyframes styles-module__toolbarHide___y8kaT {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.8);
  }
}
@keyframes styles-module__badgeEnter___mVQLj {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__scaleIn___c-r1K {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__scaleOut___Wctwz {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.85);
  }
}
@keyframes styles-module__slideUp___kgD36 {
  from {
    opacity: 0;
    transform: scale(0.85) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
@keyframes styles-module__slideDown___zcdje {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.85) translateY(8px);
  }
}
@keyframes styles-module__fadeIn___b9qmf {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes styles-module__fadeOut___6Ut6- {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@keyframes styles-module__hoverHighlightIn___6WYHY {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__hoverTooltipIn___FYGQx {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
.styles-module__disableTransitions___EopxO :is(*, *::before, *::after) {
  transition: none !important;
}

.styles-module__toolbar___wNsdK {
  position: fixed;
  bottom: 1.25rem;
  right: 1.25rem;
  width: 337px;
  z-index: 100000;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  pointer-events: none;
  transition: left 0s, top 0s, right 0s, bottom 0s;
}

:where(.styles-module__toolbar___wNsdK) {
  bottom: 1.25rem;
  right: 1.25rem;
}

.styles-module__toolbarContainer___dIhma {
  position: relative;
  user-select: none;
  margin-left: auto;
  align-self: flex-end;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a1a;
  color: #fff;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 4px 16px rgba(0, 0, 0, 0.1);
  pointer-events: auto;
  transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1), transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__toolbarContainer___dIhma.styles-module__entrance___sgHd8 {
  animation: styles-module__toolbarEnter___u8RRu 0.5s cubic-bezier(0.34, 1.2, 0.64, 1) forwards;
}
.styles-module__toolbarContainer___dIhma.styles-module__hiding___1td44 {
  animation: styles-module__toolbarHide___y8kaT 0.4s cubic-bezier(0.4, 0, 1, 1) forwards;
  pointer-events: none;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn {
  width: 44px;
  height: 44px;
  border-radius: 22px;
  padding: 0;
  cursor: pointer;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn svg {
  margin-top: -1px;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:hover {
  background: #2a2a2a;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:active {
  transform: scale(0.95);
}
.styles-module__toolbarContainer___dIhma.styles-module__expanded___ofKPx {
  height: 44px;
  border-radius: 1.5rem;
  padding: 0.375rem;
  width: 297px;
}
.styles-module__toolbarContainer___dIhma.styles-module__expanded___ofKPx.styles-module__serverConnected___Gfbou {
  width: 337px;
}

.styles-module__toggleContent___0yfyP {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.1s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__toggleContent___0yfyP.styles-module__visible___KHwEW {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}
.styles-module__toggleContent___0yfyP.styles-module__hidden___Ae8H4 {
  opacity: 0;
  pointer-events: none;
}

.styles-module__controlsContent___9GJWU {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: filter 0.8s cubic-bezier(0.19, 1, 0.22, 1), opacity 0.8s cubic-bezier(0.19, 1, 0.22, 1), transform 0.6s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__controlsContent___9GJWU.styles-module__visible___KHwEW {
  opacity: 1;
  filter: blur(0px);
  transform: scale(1);
  visibility: visible;
  pointer-events: auto;
}
.styles-module__controlsContent___9GJWU.styles-module__hidden___Ae8H4 {
  pointer-events: none;
  opacity: 0;
  filter: blur(10px);
  transform: scale(0.4);
}

.styles-module__badge___2XsgF {
  position: absolute;
  top: -13px;
  right: -13px;
  user-select: none;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background-color: var(--agentation-color-accent);
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
  opacity: 1;
  transition: transform 0.3s ease, opacity 0.2s ease;
  transform: scale(1);
}
.styles-module__badge___2XsgF.styles-module__fadeOut___6Ut6- {
  opacity: 0;
  transform: scale(0);
  pointer-events: none;
}
.styles-module__badge___2XsgF.styles-module__entrance___sgHd8 {
  animation: styles-module__badgeEnter___mVQLj 0.3s cubic-bezier(0.34, 1.2, 0.64, 1) 0.4s both;
}

.styles-module__controlButton___8Q0jc {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.85);
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease, opacity 0.2s ease;
}
.styles-module__controlButton___8Q0jc:hover:not(:disabled):not([data-active=true]):not([data-failed=true]):not([data-auto-sync=true]):not([data-error=true]):not([data-no-hover=true]) {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}
.styles-module__controlButton___8Q0jc:active:not(:disabled) {
  transform: scale(0.92);
}
.styles-module__controlButton___8Q0jc:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.styles-module__controlButton___8Q0jc[data-active=true] {
  color: var(--agentation-color-blue);
  background-color: color-mix(in srgb, var(--agentation-color-blue) 25%, transparent);
}
.styles-module__controlButton___8Q0jc[data-error=true] {
  color: var(--agentation-color-red);
  background-color: color-mix(in srgb, var(--agentation-color-red) 25%, transparent);
}
.styles-module__controlButton___8Q0jc[data-danger]:hover:not(:disabled):not([data-active=true]):not([data-failed=true]) {
  background-color: color-mix(in srgb, var(--agentation-color-red) 25%, transparent);
  color: var(--agentation-color-red);
}
.styles-module__controlButton___8Q0jc[data-no-hover=true], .styles-module__controlButton___8Q0jc.styles-module__statusShowing___te6iu {
  cursor: default;
  pointer-events: none;
  background: transparent !important;
}
.styles-module__controlButton___8Q0jc[data-auto-sync=true] {
  color: var(--agentation-color-green);
  background: transparent;
  cursor: default;
}
.styles-module__controlButton___8Q0jc[data-failed=true] {
  color: var(--agentation-color-red);
  background-color: color-mix(in srgb, var(--agentation-color-red) 25%, transparent);
}

.styles-module__buttonBadge___NeFWb {
  position: absolute;
  top: 0px;
  right: 0px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 8px;
  background-color: var(--agentation-color-accent);
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 2px #1a1a1a, 0 1px 3px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}
[data-agentation-theme=light] .styles-module__buttonBadge___NeFWb {
  box-shadow: 0 0 0 2px #fff, 0 1px 3px rgba(0, 0, 0, 0.2);
}

@keyframes styles-module__mcpIndicatorPulseConnected___EDodZ {
  0%, 100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-green) 50%, transparent);
  }
  50% {
    box-shadow: 0 0 0 5px color-mix(in srgb, var(--agentation-color-green) 0%, transparent);
  }
}
@keyframes styles-module__mcpIndicatorPulseConnecting___cCYte {
  0%, 100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-yellow) 50%, transparent);
  }
  50% {
    box-shadow: 0 0 0 5px color-mix(in srgb, var(--agentation-color-yellow) 0%, transparent);
  }
}
.styles-module__mcpIndicator___zGJeL {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  pointer-events: none;
  transition: background-color 0.3s ease, opacity 0.15s ease, transform 0.15s ease;
  opacity: 1;
  transform: scale(1);
}
.styles-module__mcpIndicator___zGJeL.styles-module__connected___7c28g {
  background-color: var(--agentation-color-green);
  animation: styles-module__mcpIndicatorPulseConnected___EDodZ 2.5s ease-in-out infinite;
}
.styles-module__mcpIndicator___zGJeL.styles-module__connecting___uo-CW {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__mcpIndicatorPulseConnecting___cCYte 1.5s ease-in-out infinite;
}
.styles-module__mcpIndicator___zGJeL.styles-module__hidden___Ae8H4 {
  opacity: 0;
  transform: scale(0);
  animation: none;
}

@keyframes styles-module__connectionPulse___-Zycw {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.9);
  }
}
.styles-module__connectionIndicatorWrapper___L-e-3 {
  width: 8px;
  height: 34px;
  margin-left: 6px;
  margin-right: 6px;
}

.styles-module__connectionIndicator___afk9p {
  position: relative;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease, background-color 0.3s ease;
  cursor: default;
}

.styles-module__connectionIndicatorVisible___C-i5B {
  opacity: 1;
}

.styles-module__connectionIndicatorConnected___IY8pR {
  background-color: var(--agentation-color-green);
  animation: styles-module__connectionPulse___-Zycw 2.5s ease-in-out infinite;
}

.styles-module__connectionIndicatorDisconnected___kmpaZ {
  background-color: var(--agentation-color-red);
  animation: none;
}

.styles-module__connectionIndicatorConnecting___QmSLH {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__connectionPulse___-Zycw 1s ease-in-out infinite;
}

.styles-module__buttonWrapper___rBcdv {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) scale(1);
  transition-delay: 0.85s;
}
.styles-module__buttonWrapper___rBcdv:has(.styles-module__controlButton___8Q0jc:disabled):hover .styles-module__buttonTooltip___Burd9 {
  opacity: 0;
  visibility: hidden;
}

.styles-module__tooltipsInSession___-0lHH .styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  transition-delay: 0s;
}

.styles-module__sendButtonWrapper___UUxG6 {
  width: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  margin-left: -0.375rem;
  transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1), opacity 0.3s cubic-bezier(0.19, 1, 0.22, 1), margin 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__sendButtonWrapper___UUxG6 .styles-module__controlButton___8Q0jc {
  transform: scale(0.8);
  transition: transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__sendButtonWrapper___UUxG6.styles-module__sendButtonVisible___WPSQU {
  width: 34px;
  opacity: 1;
  overflow: visible;
  pointer-events: auto;
  margin-left: 0;
}
.styles-module__sendButtonWrapper___UUxG6.styles-module__sendButtonVisible___WPSQU .styles-module__controlButton___8Q0jc {
  transform: scale(1);
}

.styles-module__buttonTooltip___Burd9 {
  position: absolute;
  bottom: calc(100% + 14px);
  left: 50%;
  transform: translateX(-50%) scale(0.95);
  padding: 6px 10px;
  background: #1a1a1a;
  color: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  font-weight: 500;
  border-radius: 8px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  z-index: 100001;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: opacity 0.135s ease, transform 0.135s ease, visibility 0.135s ease;
}
.styles-module__buttonTooltip___Burd9::after {
  content: "";
  position: absolute;
  top: calc(100% - 4px);
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 8px;
  height: 8px;
  background: #1a1a1a;
  border-radius: 0 0 2px 0;
}

.styles-module__shortcut___lEAQk {
  margin-left: 4px;
  opacity: 0.5;
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonTooltip___Burd9 {
  bottom: auto;
  top: calc(100% + 14px);
  transform: translateX(-50%) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonTooltip___Burd9::after {
  top: -4px;
  bottom: auto;
  border-radius: 2px 0 0 0;
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-50%) scale(1);
}

.styles-module__tooltipsHidden___VtLJG .styles-module__buttonTooltip___Burd9 {
  opacity: 0 !important;
  visibility: hidden !important;
  transition: none !important;
}

.styles-module__tooltipVisible___0jcCv,
.styles-module__tooltipsHidden___VtLJG .styles-module__tooltipVisible___0jcCv {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateX(-50%) scale(1) !important;
  transition-delay: 0s !important;
}

.styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9 {
  left: 50%;
  transform: translateX(-12px) scale(0.95);
}
.styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9::after {
  left: 16px;
}
.styles-module__buttonWrapperAlignLeft___myzIp:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(1);
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignLeft___myzIp:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(1);
}

.styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9 {
  left: 50%;
  transform: translateX(calc(-100% + 12px)) scale(0.95);
}
.styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9::after {
  left: auto;
  right: 8px;
}
.styles-module__buttonWrapperAlignRight___HCQFR:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(1);
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignRight___HCQFR:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(1);
}

.styles-module__divider___c--s1 {
  width: 1px;
  height: 12px;
  background: rgba(255, 255, 255, 0.15);
  margin: 0 0.125rem;
}

.styles-module__overlay___Q1O9y {
  position: fixed;
  inset: 0;
  z-index: 99997;
  pointer-events: none;
}
.styles-module__overlay___Q1O9y > * {
  pointer-events: auto;
}

.styles-module__hoverHighlight___ogakW {
  position: fixed;
  border: 2px solid color-mix(in srgb, var(--agentation-color-accent) 50%, transparent);
  border-radius: 4px;
  background-color: color-mix(in srgb, var(--agentation-color-accent) 4%, transparent);
  pointer-events: none !important;
  box-sizing: border-box;
  will-change: opacity;
  contain: layout style;
}
.styles-module__hoverHighlight___ogakW.styles-module__enter___WFIki {
  animation: styles-module__hoverHighlightIn___6WYHY 0.12s ease-out forwards;
}

.styles-module__multiSelectOutline___cSJ-m {
  position: fixed;
  border: 2px dashed color-mix(in srgb, var(--agentation-color-green) 60%, transparent);
  border-radius: 4px;
  pointer-events: none !important;
  background-color: color-mix(in srgb, var(--agentation-color-green) 5%, transparent);
  box-sizing: border-box;
  will-change: opacity;
}
.styles-module__multiSelectOutline___cSJ-m.styles-module__enter___WFIki {
  animation: styles-module__fadeIn___b9qmf 0.15s ease-out forwards;
}
.styles-module__multiSelectOutline___cSJ-m.styles-module__exit___fyOJ0 {
  animation: styles-module__fadeOut___6Ut6- 0.15s ease-out forwards;
}

.styles-module__singleSelectOutline___QhX-O {
  position: fixed;
  border: 2px solid color-mix(in srgb, var(--agentation-color-blue) 60%, transparent);
  border-radius: 4px;
  pointer-events: none !important;
  background-color: color-mix(in srgb, var(--agentation-color-blue) 5%, transparent);
  box-sizing: border-box;
  will-change: opacity;
}
.styles-module__singleSelectOutline___QhX-O.styles-module__enter___WFIki {
  animation: styles-module__fadeIn___b9qmf 0.15s ease-out forwards;
}
.styles-module__singleSelectOutline___QhX-O.styles-module__exit___fyOJ0 {
  animation: styles-module__fadeOut___6Ut6- 0.15s ease-out forwards;
}

.styles-module__hoverTooltip___bvLk7 {
  position: fixed;
  font-size: 0.6875rem;
  font-weight: 500;
  color: #fff;
  background: rgba(0, 0, 0, 0.85);
  padding: 0.35rem 0.6rem;
  border-radius: 0.375rem;
  pointer-events: none !important;
  white-space: nowrap;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.styles-module__hoverTooltip___bvLk7.styles-module__enter___WFIki {
  animation: styles-module__hoverTooltipIn___FYGQx 0.1s ease-out forwards;
}

.styles-module__hoverReactPath___gx1IJ {
  font-size: 0.625rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.15rem;
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__hoverElementName___QMLMl {
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__markersLayer___-25j1 {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 0;
  z-index: 99998;
  pointer-events: none;
}
.styles-module__markersLayer___-25j1 > * {
  pointer-events: auto;
}

.styles-module__fixedMarkersLayer___ffyX6 {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99998;
  pointer-events: none;
}
.styles-module__fixedMarkersLayer___ffyX6 > * {
  pointer-events: auto;
}

.styles-module__marker___6sQrs {
  position: absolute;
  width: 22px;
  height: 22px;
  background: var(--agentation-color-blue);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6875rem;
  font-weight: 600;
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2), inset 0 0 0 1px rgba(0, 0, 0, 0.04);
  user-select: none;
  will-change: transform, opacity;
  contain: layout style;
  z-index: 1;
}
.styles-module__marker___6sQrs:hover {
  z-index: 2;
}
.styles-module__marker___6sQrs:not(.styles-module__enter___WFIki):not(.styles-module__exit___fyOJ0):not(.styles-module__clearing___FQ--7) {
  transition: background-color 0.15s ease, transform 0.1s ease;
}
.styles-module__marker___6sQrs.styles-module__enter___WFIki {
  animation: styles-module__markerIn___5FaAP 0.25s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.styles-module__marker___6sQrs.styles-module__exit___fyOJ0 {
  animation: styles-module__markerOut___GU5jX 0.2s ease-out both;
  pointer-events: none;
}
.styles-module__marker___6sQrs.styles-module__clearing___FQ--7 {
  animation: styles-module__markerOut___GU5jX 0.15s ease-out both;
  pointer-events: none;
}
.styles-module__marker___6sQrs:not(.styles-module__enter___WFIki):not(.styles-module__exit___fyOJ0):not(.styles-module__clearing___FQ--7):hover {
  transform: translate(-50%, -50%) scale(1.1);
}
.styles-module__marker___6sQrs.styles-module__pending___2IHLC {
  position: fixed;
  background-color: var(--agentation-color-blue);
  cursor: default;
}
.styles-module__marker___6sQrs.styles-module__fixed___dBMHC {
  position: fixed;
}
.styles-module__marker___6sQrs.styles-module__multiSelect___YWiuz {
  background-color: var(--agentation-color-green);
  width: 26px;
  height: 26px;
  border-radius: 6px;
  font-size: 0.75rem;
}
.styles-module__marker___6sQrs.styles-module__multiSelect___YWiuz.styles-module__pending___2IHLC {
  background-color: var(--agentation-color-green);
}
.styles-module__marker___6sQrs.styles-module__hovered___ZgXIy {
  background-color: var(--agentation-color-red);
}

.styles-module__renumber___nCTxD {
  display: block;
  animation: styles-module__renumberRoll___Wgbq3 0.2s ease-out;
}

@keyframes styles-module__renumberRoll___Wgbq3 {
  0% {
    transform: translateX(-40%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}
.styles-module__markerTooltip___aLJID {
  position: absolute;
  top: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%) scale(0.909);
  z-index: 100002;
  background: #1a1a1a;
  padding: 8px 0.75rem;
  border-radius: 0.75rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-weight: 400;
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
  min-width: 120px;
  max-width: 200px;
  pointer-events: none;
  cursor: default;
}
.styles-module__markerTooltip___aLJID.styles-module__enter___WFIki {
  animation: styles-module__tooltipIn___0N31w 0.1s ease-out forwards;
}

.styles-module__markerQuote___FHmrz {
  display: block;
  font-size: 12px;
  font-style: italic;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.3125rem;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__markerNote___QkrrS {
  display: block;
  font-size: 13px;
  font-weight: 400;
  line-height: 1.4;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 2px;
}

.styles-module__markerHint___2iF-6 {
  display: block;
  font-size: 0.625rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 0.375rem;
  white-space: nowrap;
}

.styles-module__settingsPanel___OxX3Y {
  position: absolute;
  right: 5px;
  bottom: calc(100% + 0.5rem);
  z-index: 1;
  overflow: hidden;
  background: #1c1c1c;
  border-radius: 1rem;
  padding: 13px 0 16px;
  min-width: 205px;
  cursor: default;
  opacity: 1;
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: background-color 0.25s ease, box-shadow 0.25s ease;
}
.styles-module__settingsPanel___OxX3Y::before, .styles-module__settingsPanel___OxX3Y::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 16px;
  z-index: 2;
  pointer-events: none;
}
.styles-module__settingsPanel___OxX3Y::before {
  left: 0;
  background: linear-gradient(to right, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___OxX3Y::after {
  right: 0;
  background: linear-gradient(to left, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___OxX3Y .styles-module__settingsHeader___pwDY9,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrand___0gJeM,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrandSlash___uTG18,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsVersion___TUcFq,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsSection___m-YM2,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsLabel___8UjfX,
.styles-module__settingsPanel___OxX3Y .styles-module__cycleButton___FMKfw,
.styles-module__settingsPanel___OxX3Y .styles-module__cycleDot___nPgLY,
.styles-module__settingsPanel___OxX3Y .styles-module__dropdownButton___16NPz,
.styles-module__settingsPanel___OxX3Y .styles-module__toggleLabel___Xm8Aa,
.styles-module__settingsPanel___OxX3Y .styles-module__customCheckbox___U39ax,
.styles-module__settingsPanel___OxX3Y .styles-module__sliderLabel___U8sPr,
.styles-module__settingsPanel___OxX3Y .styles-module__slider___GLdxp,
.styles-module__settingsPanel___OxX3Y .styles-module__themeToggle___2rUjA {
  transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
}
.styles-module__settingsPanel___OxX3Y.styles-module__enter___WFIki {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0px);
  transition: opacity 0.2s ease, transform 0.2s ease, filter 0.2s ease;
}
.styles-module__settingsPanel___OxX3Y.styles-module__exit___fyOJ0 {
  opacity: 0;
  transform: translateY(8px) scale(0.95);
  filter: blur(5px);
  pointer-events: none;
  transition: opacity 0.1s ease, transform 0.1s ease, filter 0.1s ease;
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y {
  background: #1a1a1a;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y .styles-module__settingsLabel___8UjfX {
  color: rgba(255, 255, 255, 0.6);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y .styles-module__settingsOption___UNa12 {
  color: rgba(255, 255, 255, 0.85);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y .styles-module__settingsOption___UNa12:hover {
  background: rgba(255, 255, 255, 0.1);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y .styles-module__settingsOption___UNa12.styles-module__selected___OwRqP {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}
[data-agentation-theme=dark] .styles-module__settingsPanel___OxX3Y .styles-module__toggleLabel___Xm8Aa {
  color: rgba(255, 255, 255, 0.85);
}

.styles-module__settingsPanelContainer___Xksv8 {
  overflow: visible;
  position: relative;
  display: flex;
  padding: 0 1rem;
}

.styles-module__settingsPage___6YfHH {
  min-width: 100%;
  flex-shrink: 0;
  transition: transform 0.2s ease, opacity 0.2s ease;
  transition-delay: 0s;
  opacity: 1;
}

.styles-module__settingsPage___6YfHH.styles-module__slideLeft___Ps01J {
  transform: translateX(-24px);
  opacity: 0;
  pointer-events: none;
}

.styles-module__automationsPage___uvCq6 {
  position: absolute;
  top: 0;
  left: 24px;
  width: 100%;
  height: 100%;
  padding: 3px 1rem 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, opacity 0.2s ease;
  opacity: 0;
  pointer-events: none;
}

.styles-module__automationsPage___uvCq6.styles-module__slideIn___4-qXe {
  transform: translateX(-24px);
  opacity: 1;
  pointer-events: auto;
}

.styles-module__settingsNavLink___wCzJt {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0;
  border: none;
  background: transparent;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: color 0.15s ease;
}
.styles-module__settingsNavLink___wCzJt:hover {
  color: rgba(255, 255, 255, 0.9);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___wCzJt {
  color: rgba(0, 0, 0, 0.5);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___wCzJt:hover {
  color: rgba(0, 0, 0, 0.8);
}
.styles-module__settingsNavLink___wCzJt svg {
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s ease;
}
.styles-module__settingsNavLink___wCzJt:hover svg {
  color: #fff;
}
[data-agentation-theme=light] .styles-module__settingsNavLink___wCzJt svg {
  color: rgba(0, 0, 0, 0.25);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___wCzJt:hover svg {
  color: rgba(0, 0, 0, 0.8);
}

.styles-module__settingsNavLinkRight___ZWwhj {
  display: flex;
  align-items: center;
  gap: 6px;
}

.styles-module__mcpNavIndicator___cl9pO {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpNavIndicator___cl9pO.styles-module__connected___7c28g {
  background-color: var(--agentation-color-green);
  animation: styles-module__mcpPulse___uNggr 2.5s ease-in-out infinite;
}
.styles-module__mcpNavIndicator___cl9pO.styles-module__connecting___uo-CW {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__mcpPulse___uNggr 1.5s ease-in-out infinite;
}

.styles-module__settingsBackButton___bIe2j {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 0 12px 0;
  margin: -6px 0 0.5rem 0;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 0;
  background: transparent;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 500;
  letter-spacing: -0.15px;
  color: #fff;
  cursor: pointer;
  transition: transform 0.12s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___bIe2j svg {
  opacity: 0.4;
  flex-shrink: 0;
  transition: opacity 0.15s ease, transform 0.18s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___bIe2j:hover {
  border-bottom-color: rgba(255, 255, 255, 0.07);
}
.styles-module__settingsBackButton___bIe2j:hover svg {
  opacity: 1;
}
[data-agentation-theme=light] .styles-module__settingsBackButton___bIe2j {
  color: rgba(0, 0, 0, 0.85);
  border-bottom-color: rgba(0, 0, 0, 0.08);
}
[data-agentation-theme=light] .styles-module__settingsBackButton___bIe2j:hover {
  border-bottom-color: rgba(0, 0, 0, 0.08);
}

.styles-module__automationHeader___InP0r {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  font-size: 0.8125rem;
  font-weight: 400;
  color: #fff;
}
[data-agentation-theme=light] .styles-module__automationHeader___InP0r {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__automationDescription___NKlmo {
  font-size: 0.6875rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 2px;
  line-height: 14px;
}
[data-agentation-theme=light] .styles-module__automationDescription___NKlmo {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__learnMoreLink___8xv-x {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: underline dotted;
  text-decoration-color: rgba(255, 255, 255, 0.2);
  text-underline-offset: 2px;
  transition: color 0.15s ease;
}
.styles-module__learnMoreLink___8xv-x:hover {
  color: #fff;
}
[data-agentation-theme=light] .styles-module__learnMoreLink___8xv-x {
  color: rgba(0, 0, 0, 0.6);
  text-decoration-color: rgba(0, 0, 0, 0.2);
}
[data-agentation-theme=light] .styles-module__learnMoreLink___8xv-x:hover {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__autoSendRow___UblX5 {
  display: flex;
  align-items: center;
  gap: 8px;
}

.styles-module__autoSendLabel___icDc2 {
  font-size: 0.6875rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s ease;
}
.styles-module__autoSendLabel___icDc2.styles-module__active___-zoN6 {
  color: #66b8ff;
  color: color(display-p3 0.4 0.72 1);
}
[data-agentation-theme=light] .styles-module__autoSendLabel___icDc2 {
  color: rgba(0, 0, 0, 0.4);
}
[data-agentation-theme=light] .styles-module__autoSendLabel___icDc2.styles-module__active___-zoN6 {
  color: var(--agentation-color-blue);
}

.styles-module__webhookUrlInput___2375C {
  display: block;
  width: 100%;
  flex: 1;
  min-height: 60px;
  box-sizing: border-box;
  margin-top: 11px;
  padding: 8px 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  font-family: inherit;
  font-size: 0.75rem;
  font-weight: 400;
  color: #fff;
  outline: none;
  resize: none;
  user-select: text;
  transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
}
.styles-module__webhookUrlInput___2375C::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.styles-module__webhookUrlInput___2375C:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___2375C {
  border-color: rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.03);
  color: rgba(0, 0, 0, 0.85);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___2375C::placeholder {
  color: rgba(0, 0, 0, 0.3);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___2375C:focus {
  border-color: rgba(0, 0, 0, 0.25);
  background: rgba(0, 0, 0, 0.05);
}

.styles-module__settingsHeader___pwDY9 {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
  margin-bottom: 0.5rem;
  padding-bottom: 9px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.styles-module__settingsBrand___0gJeM {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: -0.0094em;
  color: #fff;
  text-decoration: none;
}

.styles-module__settingsBrandSlash___uTG18 {
  color: var(--agentation-color-accent);
  transition: color 0.2s ease;
}

.styles-module__settingsVersion___TUcFq {
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  margin-left: auto;
  letter-spacing: -0.0094em;
}

.styles-module__settingsSection___m-YM2 + .styles-module__settingsSection___m-YM2 {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
}
.styles-module__settingsSection___m-YM2.styles-module__settingsSectionExtraPadding___jdhFV {
  padding-top: calc(0.5rem + 4px);
}

.styles-module__settingsSectionGrow___h-5HZ {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.styles-module__settingsRow___3sdhc {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
}
.styles-module__settingsRow___3sdhc.styles-module__settingsRowMarginTop___zA0Sp {
  margin-top: 8px;
}

.styles-module__dropdownContainer___BVnxe {
  position: relative;
}

.styles-module__dropdownButton___16NPz {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
  letter-spacing: -0.0094em;
}
.styles-module__dropdownButton___16NPz:hover {
  background: rgba(255, 255, 255, 0.08);
}
.styles-module__dropdownButton___16NPz svg {
  opacity: 0.6;
}

.styles-module__cycleButton___FMKfw {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  border: none;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  letter-spacing: -0.0094em;
}
[data-agentation-theme=light] .styles-module__cycleButton___FMKfw {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__cycleButton___FMKfw:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.styles-module__settingsRowDisabled___EgS0V .styles-module__settingsLabel___8UjfX {
  color: rgba(255, 255, 255, 0.2);
}
[data-agentation-theme=light] .styles-module__settingsRowDisabled___EgS0V .styles-module__settingsLabel___8UjfX {
  color: rgba(0, 0, 0, 0.2);
}
.styles-module__settingsRowDisabled___EgS0V .styles-module__toggleSwitch___l4Ygm {
  opacity: 0.4;
  cursor: not-allowed;
}

@keyframes styles-module__cycleTextIn___Q6zJf {
  0% {
    opacity: 0;
    transform: translateY(-6px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.styles-module__cycleButtonText___fD1LR {
  display: inline-block;
  animation: styles-module__cycleTextIn___Q6zJf 0.2s ease-out;
}

.styles-module__cycleDots___LWuoQ {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.styles-module__cycleDot___nPgLY {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0.667);
  transition: background-color 0.25s ease-out, transform 0.25s ease-out;
}
.styles-module__cycleDot___nPgLY.styles-module__active___-zoN6 {
  background: #fff;
  transform: scale(1);
}
[data-agentation-theme=light] .styles-module__cycleDot___nPgLY {
  background: rgba(0, 0, 0, 0.2);
}
[data-agentation-theme=light] .styles-module__cycleDot___nPgLY.styles-module__active___-zoN6 {
  background: rgba(0, 0, 0, 0.7);
}

.styles-module__dropdownMenu___k73ER {
  position: absolute;
  right: 0;
  top: calc(100% + 0.25rem);
  background: #1a1a1a;
  border-radius: 0.5rem;
  padding: 0.25rem;
  min-width: 120px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
  z-index: 10;
  animation: styles-module__scaleIn___c-r1K 0.15s ease-out;
}

.styles-module__dropdownItem___ylsLj {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.625rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  text-align: left;
  transition: background-color 0.15s ease, color 0.15s ease;
  letter-spacing: -0.0094em;
}
.styles-module__dropdownItem___ylsLj:hover {
  background: rgba(255, 255, 255, 0.08);
}
.styles-module__dropdownItem___ylsLj.styles-module__selected___OwRqP {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-weight: 600;
}

.styles-module__settingsLabel___8UjfX {
  font-size: 0.8125rem;
  font-weight: 400;
  letter-spacing: -0.0094em;
  color: rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  gap: 0.125rem;
}
[data-agentation-theme=light] .styles-module__settingsLabel___8UjfX {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__settingsLabelMarker___ewdtV {
  padding-top: 3px;
  margin-bottom: 10px;
}

.styles-module__settingsOptions___LyrBA {
  display: flex;
  gap: 0.25rem;
}

.styles-module__settingsOption___UNa12 {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.375rem 0.5rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.7);
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}
.styles-module__settingsOption___UNa12:hover {
  background: rgba(0, 0, 0, 0.05);
}
.styles-module__settingsOption___UNa12.styles-module__selected___OwRqP {
  background: color-mix(in srgb, var(--agentation-color-blue) 15%, transparent);
  color: var(--agentation-color-blue);
}

.styles-module__sliderContainer___ducXj {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.styles-module__slider___GLdxp {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
.styles-module__slider___GLdxp::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
.styles-module__slider___GLdxp::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
.styles-module__slider___GLdxp:hover::-webkit-slider-thumb {
  transform: scale(1.15);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}
.styles-module__slider___GLdxp:hover::-moz-range-thumb {
  transform: scale(1.15);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

.styles-module__sliderLabels___FhLDB {
  display: flex;
  justify-content: space-between;
}

.styles-module__sliderLabel___U8sPr {
  font-size: 0.625rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: color 0.15s ease;
}
.styles-module__sliderLabel___U8sPr:hover {
  color: rgba(255, 255, 255, 0.7);
}
.styles-module__sliderLabel___U8sPr.styles-module__active___-zoN6 {
  color: rgba(255, 255, 255, 0.9);
}

.styles-module__colorOptions___iHCNX {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.375rem;
  margin-bottom: 1px;
}

.styles-module__colorOption___IodiY {
  display: block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid transparent;
  background-color: var(--swatch);
  cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}
@supports (color: color(display-p3 0 0 0)) {
  .styles-module__colorOption___IodiY {
    background-color: var(--swatch-p3);
  }
}
.styles-module__colorOption___IodiY:hover {
  transform: scale(1.15);
}
.styles-module__colorOption___IodiY.styles-module__selected___OwRqP {
  transform: scale(0.83);
}

.styles-module__colorOptionRing___U2xpo {
  display: flex;
  width: 24px;
  height: 24px;
  border: 2px solid transparent;
  border-radius: 50%;
  transition: border-color 0.3s ease;
}
.styles-module__colorOptionRing___U2xpo.styles-module__selected___OwRqP {
  border-color: var(--swatch);
}
@supports (color: color(display-p3 0 0 0)) {
  .styles-module__colorOptionRing___U2xpo.styles-module__selected___OwRqP {
    border-color: var(--swatch-p3);
  }
}

.styles-module__settingsToggle___fBrFn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
.styles-module__settingsToggle___fBrFn + .styles-module__settingsToggle___fBrFn {
  margin-top: calc(0.5rem + 6px);
}
.styles-module__settingsToggle___fBrFn input[type=checkbox] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.styles-module__settingsToggle___fBrFn.styles-module__settingsToggleMarginBottom___MZUyF {
  margin-bottom: calc(0.5rem + 6px);
}

.styles-module__customCheckbox___U39ax {
  position: relative;
  width: 14px;
  height: 14px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background-color 0.25s ease, border-color 0.25s ease;
}
.styles-module__customCheckbox___U39ax svg {
  color: #1a1a1a;
  opacity: 1;
  transition: opacity 0.15s ease;
}
input[type=checkbox]:checked + .styles-module__customCheckbox___U39ax {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgb(255, 255, 255);
}
[data-agentation-theme=light] .styles-module__customCheckbox___U39ax {
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: #fff;
}
[data-agentation-theme=light] .styles-module__customCheckbox___U39ax.styles-module__checked___mnZLo {
  border-color: #1a1a1a;
  background: #1a1a1a;
}
[data-agentation-theme=light] .styles-module__customCheckbox___U39ax.styles-module__checked___mnZLo svg {
  color: #fff;
}

.styles-module__toggleLabel___Xm8Aa {
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: -0.0094em;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
[data-agentation-theme=light] .styles-module__toggleLabel___Xm8Aa {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__toggleSwitch___l4Ygm {
  position: relative;
  display: inline-block;
  width: 24px;
  height: 16px;
  flex-shrink: 0;
  cursor: pointer;
  transition: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.styles-module__toggleSwitch___l4Ygm input {
  opacity: 0;
  width: 0;
  height: 0;
}
.styles-module__toggleSwitch___l4Ygm input:checked + .styles-module__toggleSlider___wprIn {
  background-color: var(--agentation-color-blue);
}
.styles-module__toggleSwitch___l4Ygm input:checked + .styles-module__toggleSlider___wprIn::before {
  transform: translateX(8px);
}
.styles-module__toggleSwitch___l4Ygm.styles-module__disabled___332Jw {
  opacity: 0.4;
}
.styles-module__toggleSwitch___l4Ygm.styles-module__disabled___332Jw .styles-module__toggleSlider___wprIn {
  cursor: not-allowed;
}

.styles-module__toggleSlider___wprIn {
  position: absolute;
  cursor: pointer;
  inset: 0;
  border-radius: 16px;
  background: #484848;
}
[data-agentation-theme=light] .styles-module__toggleSlider___wprIn {
  background: #dddddd;
}
.styles-module__toggleSlider___wprIn::before {
  content: "";
  position: absolute;
  height: 12px;
  width: 12px;
  left: 2px;
  bottom: 2px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes styles-module__mcpPulse___uNggr {
  0% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-green) 50%, transparent);
  }
  70% {
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--agentation-color-green) 0%, transparent);
  }
  100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-green) 0%, transparent);
  }
}
@keyframes styles-module__mcpPulseError___fov9B {
  0% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-red) 50%, transparent);
  }
  70% {
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--agentation-color-red) 0%, transparent);
  }
  100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-red) 0%, transparent);
  }
}
.styles-module__mcpStatusDot___ibgkc {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__connecting___uo-CW {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__mcpPulse___uNggr 1.5s infinite;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__connected___7c28g {
  background-color: var(--agentation-color-green);
  animation: styles-module__mcpPulse___uNggr 2.5s ease-in-out infinite;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__disconnected___cHPxR {
  background-color: var(--agentation-color-red);
  animation: styles-module__mcpPulseError___fov9B 2s infinite;
}

.styles-module__drawCanvas___7cG9U {
  position: fixed;
  inset: 0;
  z-index: 99996;
  pointer-events: none !important;
}
.styles-module__drawCanvas___7cG9U.styles-module__active___-zoN6 {
  pointer-events: auto !important;
  cursor: crosshair !important;
}
.styles-module__drawCanvas___7cG9U.styles-module__active___-zoN6[data-stroke-hover] {
  cursor: pointer !important;
}

.styles-module__dragSelection___kZLq2 {
  position: fixed;
  top: 0;
  left: 0;
  border: 2px solid color-mix(in srgb, var(--agentation-color-green) 60%, transparent);
  border-radius: 4px;
  background-color: color-mix(in srgb, var(--agentation-color-green) 8%, transparent);
  pointer-events: none;
  z-index: 99997;
  will-change: transform, width, height;
  contain: layout style;
}

.styles-module__dragCount___KM90j {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--agentation-color-green);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  min-width: 1.5rem;
  text-align: center;
}

.styles-module__highlightsContainer___-0xzG {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 99996;
}

.styles-module__selectedElementHighlight___fyVlI {
  position: fixed;
  top: 0;
  left: 0;
  border: 2px solid color-mix(in srgb, var(--agentation-color-green) 50%, transparent);
  border-radius: 4px;
  background: color-mix(in srgb, var(--agentation-color-green) 6%, transparent);
  pointer-events: none;
  will-change: transform, width, height;
  contain: layout style;
}

[data-agentation-theme=light] .styles-module__toolbarContainer___dIhma {
  background: #fff;
  color: rgba(0, 0, 0, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
[data-agentation-theme=light] .styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:hover {
  background: #f5f5f5;
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc {
  color: rgba(0, 0, 0, 0.5);
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc:hover:not(:disabled):not([data-active=true]):not([data-failed=true]):not([data-auto-sync=true]):not([data-error=true]):not([data-no-hover=true]) {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.85);
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc[data-active=true] {
  color: var(--agentation-color-blue);
  background: color-mix(in srgb, var(--agentation-color-blue) 15%, transparent);
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc[data-error=true] {
  color: var(--agentation-color-red);
  background: color-mix(in srgb, var(--agentation-color-red) 15%, transparent);
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc[data-danger]:hover:not(:disabled):not([data-active=true]):not([data-failed=true]) {
  color: var(--agentation-color-red);
  background: color-mix(in srgb, var(--agentation-color-red) 15%, transparent);
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc[data-auto-sync=true] {
  color: var(--agentation-color-green);
  background: transparent;
}
[data-agentation-theme=light] .styles-module__controlButton___8Q0jc[data-failed=true] {
  color: var(--agentation-color-red);
  background: color-mix(in srgb, var(--agentation-color-red) 15%, transparent);
}
[data-agentation-theme=light] .styles-module__buttonTooltip___Burd9 {
  background: #fff;
  color: rgba(0, 0, 0, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
[data-agentation-theme=light] .styles-module__buttonTooltip___Burd9::after {
  background: #fff;
}
[data-agentation-theme=light] .styles-module__divider___c--s1 {
  background: rgba(0, 0, 0, 0.1);
}`,c4={toolbar:"styles-module__toolbar___wNsdK",markersLayer:"styles-module__markersLayer___-25j1",fixedMarkersLayer:"styles-module__fixedMarkersLayer___ffyX6",controlsContent:"styles-module__controlsContent___9GJWU",disableTransitions:"styles-module__disableTransitions___EopxO",toolbarContainer:"styles-module__toolbarContainer___dIhma",entrance:"styles-module__entrance___sgHd8",toolbarEnter:"styles-module__toolbarEnter___u8RRu",hiding:"styles-module__hiding___1td44",toolbarHide:"styles-module__toolbarHide___y8kaT",collapsed:"styles-module__collapsed___Rydsn",expanded:"styles-module__expanded___ofKPx",serverConnected:"styles-module__serverConnected___Gfbou",toggleContent:"styles-module__toggleContent___0yfyP",visible:"styles-module__visible___KHwEW",hidden:"styles-module__hidden___Ae8H4",badge:"styles-module__badge___2XsgF",fadeOut:"styles-module__fadeOut___6Ut6-",badgeEnter:"styles-module__badgeEnter___mVQLj",controlButton:"styles-module__controlButton___8Q0jc",statusShowing:"styles-module__statusShowing___te6iu",buttonBadge:"styles-module__buttonBadge___NeFWb",mcpIndicator:"styles-module__mcpIndicator___zGJeL",connected:"styles-module__connected___7c28g",mcpIndicatorPulseConnected:"styles-module__mcpIndicatorPulseConnected___EDodZ",connecting:"styles-module__connecting___uo-CW",mcpIndicatorPulseConnecting:"styles-module__mcpIndicatorPulseConnecting___cCYte",connectionIndicatorWrapper:"styles-module__connectionIndicatorWrapper___L-e-3",connectionIndicator:"styles-module__connectionIndicator___afk9p",connectionIndicatorVisible:"styles-module__connectionIndicatorVisible___C-i5B",connectionIndicatorConnected:"styles-module__connectionIndicatorConnected___IY8pR",connectionPulse:"styles-module__connectionPulse___-Zycw",connectionIndicatorDisconnected:"styles-module__connectionIndicatorDisconnected___kmpaZ",connectionIndicatorConnecting:"styles-module__connectionIndicatorConnecting___QmSLH",buttonWrapper:"styles-module__buttonWrapper___rBcdv",buttonTooltip:"styles-module__buttonTooltip___Burd9",tooltipsInSession:"styles-module__tooltipsInSession___-0lHH",sendButtonWrapper:"styles-module__sendButtonWrapper___UUxG6",sendButtonVisible:"styles-module__sendButtonVisible___WPSQU",shortcut:"styles-module__shortcut___lEAQk",tooltipBelow:"styles-module__tooltipBelow___m6ats",tooltipsHidden:"styles-module__tooltipsHidden___VtLJG",tooltipVisible:"styles-module__tooltipVisible___0jcCv",buttonWrapperAlignLeft:"styles-module__buttonWrapperAlignLeft___myzIp",buttonWrapperAlignRight:"styles-module__buttonWrapperAlignRight___HCQFR",divider:"styles-module__divider___c--s1",overlay:"styles-module__overlay___Q1O9y",hoverHighlight:"styles-module__hoverHighlight___ogakW",enter:"styles-module__enter___WFIki",hoverHighlightIn:"styles-module__hoverHighlightIn___6WYHY",multiSelectOutline:"styles-module__multiSelectOutline___cSJ-m",fadeIn:"styles-module__fadeIn___b9qmf",exit:"styles-module__exit___fyOJ0",singleSelectOutline:"styles-module__singleSelectOutline___QhX-O",hoverTooltip:"styles-module__hoverTooltip___bvLk7",hoverTooltipIn:"styles-module__hoverTooltipIn___FYGQx",hoverReactPath:"styles-module__hoverReactPath___gx1IJ",hoverElementName:"styles-module__hoverElementName___QMLMl",marker:"styles-module__marker___6sQrs",clearing:"styles-module__clearing___FQ--7",markerIn:"styles-module__markerIn___5FaAP",markerOut:"styles-module__markerOut___GU5jX",pending:"styles-module__pending___2IHLC",fixed:"styles-module__fixed___dBMHC",multiSelect:"styles-module__multiSelect___YWiuz",hovered:"styles-module__hovered___ZgXIy",renumber:"styles-module__renumber___nCTxD",renumberRoll:"styles-module__renumberRoll___Wgbq3",markerTooltip:"styles-module__markerTooltip___aLJID",tooltipIn:"styles-module__tooltipIn___0N31w",markerQuote:"styles-module__markerQuote___FHmrz",markerNote:"styles-module__markerNote___QkrrS",markerHint:"styles-module__markerHint___2iF-6",settingsPanel:"styles-module__settingsPanel___OxX3Y",settingsHeader:"styles-module__settingsHeader___pwDY9",settingsBrand:"styles-module__settingsBrand___0gJeM",settingsBrandSlash:"styles-module__settingsBrandSlash___uTG18",settingsVersion:"styles-module__settingsVersion___TUcFq",settingsSection:"styles-module__settingsSection___m-YM2",settingsLabel:"styles-module__settingsLabel___8UjfX",cycleButton:"styles-module__cycleButton___FMKfw",cycleDot:"styles-module__cycleDot___nPgLY",dropdownButton:"styles-module__dropdownButton___16NPz",toggleLabel:"styles-module__toggleLabel___Xm8Aa",customCheckbox:"styles-module__customCheckbox___U39ax",sliderLabel:"styles-module__sliderLabel___U8sPr",slider:"styles-module__slider___GLdxp",themeToggle:"styles-module__themeToggle___2rUjA",settingsOption:"styles-module__settingsOption___UNa12",selected:"styles-module__selected___OwRqP",settingsPanelContainer:"styles-module__settingsPanelContainer___Xksv8",settingsPage:"styles-module__settingsPage___6YfHH",slideLeft:"styles-module__slideLeft___Ps01J",automationsPage:"styles-module__automationsPage___uvCq6",slideIn:"styles-module__slideIn___4-qXe",settingsNavLink:"styles-module__settingsNavLink___wCzJt",settingsNavLinkRight:"styles-module__settingsNavLinkRight___ZWwhj",mcpNavIndicator:"styles-module__mcpNavIndicator___cl9pO",mcpPulse:"styles-module__mcpPulse___uNggr",settingsBackButton:"styles-module__settingsBackButton___bIe2j",automationHeader:"styles-module__automationHeader___InP0r",automationDescription:"styles-module__automationDescription___NKlmo",learnMoreLink:"styles-module__learnMoreLink___8xv-x",autoSendRow:"styles-module__autoSendRow___UblX5",autoSendLabel:"styles-module__autoSendLabel___icDc2",active:"styles-module__active___-zoN6",webhookUrlInput:"styles-module__webhookUrlInput___2375C",settingsSectionExtraPadding:"styles-module__settingsSectionExtraPadding___jdhFV",settingsSectionGrow:"styles-module__settingsSectionGrow___h-5HZ",settingsRow:"styles-module__settingsRow___3sdhc",settingsRowMarginTop:"styles-module__settingsRowMarginTop___zA0Sp",dropdownContainer:"styles-module__dropdownContainer___BVnxe",settingsRowDisabled:"styles-module__settingsRowDisabled___EgS0V",toggleSwitch:"styles-module__toggleSwitch___l4Ygm",cycleButtonText:"styles-module__cycleButtonText___fD1LR",cycleTextIn:"styles-module__cycleTextIn___Q6zJf",cycleDots:"styles-module__cycleDots___LWuoQ",dropdownMenu:"styles-module__dropdownMenu___k73ER",scaleIn:"styles-module__scaleIn___c-r1K",dropdownItem:"styles-module__dropdownItem___ylsLj",settingsLabelMarker:"styles-module__settingsLabelMarker___ewdtV",settingsOptions:"styles-module__settingsOptions___LyrBA",sliderContainer:"styles-module__sliderContainer___ducXj",sliderLabels:"styles-module__sliderLabels___FhLDB",colorOptions:"styles-module__colorOptions___iHCNX",colorOption:"styles-module__colorOption___IodiY",colorOptionRing:"styles-module__colorOptionRing___U2xpo",settingsToggle:"styles-module__settingsToggle___fBrFn",settingsToggleMarginBottom:"styles-module__settingsToggleMarginBottom___MZUyF",checked:"styles-module__checked___mnZLo",toggleSlider:"styles-module__toggleSlider___wprIn",disabled:"styles-module__disabled___332Jw",mcpStatusDot:"styles-module__mcpStatusDot___ibgkc",disconnected:"styles-module__disconnected___cHPxR",mcpPulseError:"styles-module__mcpPulseError___fov9B",drawCanvas:"styles-module__drawCanvas___7cG9U",dragSelection:"styles-module__dragSelection___kZLq2",dragCount:"styles-module__dragCount___KM90j",highlightsContainer:"styles-module__highlightsContainer___-0xzG",selectedElementHighlight:"styles-module__selectedElementHighlight___fyVlI",scaleOut:"styles-module__scaleOut___Wctwz",slideUp:"styles-module__slideUp___kgD36",slideDown:"styles-module__slideDown___zcdje"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-page-toolbar-css-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-page-toolbar-css-styles",document.head.appendChild(e)),e.textContent=r4}var Y=c4,qs=[{value:"compact",label:"Compact"},{value:"standard",label:"Standard"},{value:"detailed",label:"Detailed"},{value:"forensic",label:"Forensic"}];function uy(e,t,n="standard"){if(e.length===0)return"";let l=typeof window<"u"?`${window.innerWidth}\xD7${window.innerHeight}`:"unknown",o=`## Page Feedback: ${t}
`;return n==="forensic"?(o+=`
**Environment:**
`,o+=`- Viewport: ${l}
`,typeof window<"u"&&(o+=`- URL: ${window.location.href}
`,o+=`- User Agent: ${navigator.userAgent}
`,o+=`- Timestamp: ${new Date().toISOString()}
`,o+=`- Device Pixel Ratio: ${window.devicePixelRatio}
`),o+=`
---
`):n!=="compact"&&(o+=`**Viewport:** ${l}
`),o+=`
`,e.forEach((a,i)=>{n==="compact"?(o+=`${i+1}. **${a.element}**${a.sourceFile?` (${a.sourceFile})`:""}: ${a.comment}`,a.selectedText&&(o+=` (re: "${a.selectedText.slice(0,30)}${a.selectedText.length>30?"...":""}")`),o+=`
`):n==="forensic"?(o+=`### ${i+1}. ${a.element}
`,a.isMultiSelect&&a.fullPath&&(o+=`*Forensic data shown for first element of selection*
`),a.fullPath&&(o+=`**Full DOM Path:** ${a.fullPath}
`),a.cssClasses&&(o+=`**CSS Classes:** ${a.cssClasses}
`),a.boundingBox&&(o+=`**Position:** x:${Math.round(a.boundingBox.x)}, y:${Math.round(a.boundingBox.y)} (${Math.round(a.boundingBox.width)}\xD7${Math.round(a.boundingBox.height)}px)
`),o+=`**Annotation at:** ${a.x.toFixed(1)}% from left, ${Math.round(a.y)}px from top
`,a.selectedText&&(o+=`**Selected text:** "${a.selectedText}"
`),a.nearbyText&&!a.selectedText&&(o+=`**Context:** ${a.nearbyText.slice(0,100)}
`),a.computedStyles&&(o+=`**Computed Styles:** ${a.computedStyles}
`),a.accessibility&&(o+=`**Accessibility:** ${a.accessibility}
`),a.nearbyElements&&(o+=`**Nearby Elements:** ${a.nearbyElements}
`),a.sourceFile&&(o+=`**Source:** ${a.sourceFile}
`),a.reactComponents&&(o+=`**React:** ${a.reactComponents}
`),o+=`**Feedback:** ${a.comment}

`):(o+=`### ${i+1}. ${a.element}
`,o+=`**Location:** ${a.elementPath}
`,a.sourceFile&&(o+=`**Source:** ${a.sourceFile}
`),a.reactComponents&&(o+=`**React:** ${a.reactComponents}
`),n==="detailed"&&(a.cssClasses&&(o+=`**Classes:** ${a.cssClasses}
`),a.boundingBox&&(o+=`**Position:** ${Math.round(a.boundingBox.x)}px, ${Math.round(a.boundingBox.y)}px (${Math.round(a.boundingBox.width)}\xD7${Math.round(a.boundingBox.height)}px)
`)),a.selectedText&&(o+=`**Selected text:** "${a.selectedText}"
`),n==="detailed"&&a.nearbyText&&!a.selectedText&&(o+=`**Context:** ${a.nearbyText.slice(0,100)}
`),o+=`**Feedback:** ${a.comment}

`)}),o.trim()}var u4=`@keyframes styles-module__markerIn___x4G8D {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.3);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}
@keyframes styles-module__markerOut___6VhQN {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.3);
  }
}
@keyframes styles-module__tooltipIn___aJslQ {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(2px) scale(0.891);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0) scale(0.909);
  }
}
@keyframes styles-module__renumberRoll___akV9B {
  0% {
    transform: translateX(-40%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}
.styles-module__marker___9CKF7 {
  position: absolute;
  width: 22px;
  height: 22px;
  background: var(--agentation-color-blue);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6875rem;
  font-weight: 600;
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2), inset 0 0 0 1px rgba(0, 0, 0, 0.04);
  user-select: none;
  will-change: transform, opacity;
  contain: layout style;
  z-index: 1;
}
.styles-module__marker___9CKF7:hover {
  z-index: 2;
}
.styles-module__marker___9CKF7:not(.styles-module__enter___8kI3q):not(.styles-module__exit___KBdR3):not(.styles-module__clearing___8rM7K) {
  transition: background-color 0.15s ease, transform 0.1s ease;
}
.styles-module__marker___9CKF7.styles-module__enter___8kI3q {
  animation: styles-module__markerIn___x4G8D 0.25s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.styles-module__marker___9CKF7.styles-module__exit___KBdR3 {
  animation: styles-module__markerOut___6VhQN 0.2s ease-out both;
  pointer-events: none;
}
.styles-module__marker___9CKF7.styles-module__clearing___8rM7K {
  animation: styles-module__markerOut___6VhQN 0.15s ease-out both;
  pointer-events: none;
}
.styles-module__marker___9CKF7:not(.styles-module__enter___8kI3q):not(.styles-module__exit___KBdR3):not(.styles-module__clearing___8rM7K):hover {
  transform: translate(-50%, -50%) scale(1.1);
}
.styles-module__marker___9CKF7.styles-module__pending___BiY-U {
  position: fixed;
  background-color: var(--agentation-color-blue);
  cursor: default;
}
.styles-module__marker___9CKF7.styles-module__fixed___aKrQO {
  position: fixed;
}
.styles-module__marker___9CKF7.styles-module__multiSelect___CPfTC {
  background-color: var(--agentation-color-green);
  width: 26px;
  height: 26px;
  border-radius: 6px;
  font-size: 0.75rem;
}
.styles-module__marker___9CKF7.styles-module__multiSelect___CPfTC.styles-module__pending___BiY-U {
  background-color: var(--agentation-color-green);
}
.styles-module__marker___9CKF7.styles-module__hovered___-mg2N {
  background-color: var(--agentation-color-red);
}

.styles-module__renumber___16lvD {
  display: block;
  animation: styles-module__renumberRoll___akV9B 0.2s ease-out;
}

.styles-module__markerTooltip___-VUm- {
  position: absolute;
  top: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%) scale(0.909);
  z-index: 100002;
  background: #1a1a1a;
  padding: 8px 0.75rem;
  border-radius: 0.75rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-weight: 400;
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
  min-width: 120px;
  max-width: 200px;
  pointer-events: none;
  cursor: default;
}
.styles-module__markerTooltip___-VUm-.styles-module__enter___8kI3q {
  animation: styles-module__tooltipIn___aJslQ 0.1s ease-out forwards;
}

.styles-module__markerQuote___tQake {
  display: block;
  font-size: 12px;
  font-style: italic;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.3125rem;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__markerNote___Rh4eI {
  display: block;
  font-size: 13px;
  font-weight: 400;
  line-height: 1.4;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 2px;
}

[data-agentation-theme=light] .styles-module__markerTooltip___-VUm- {
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.06);
}
[data-agentation-theme=light] .styles-module__markerTooltip___-VUm- .styles-module__markerQuote___tQake {
  color: rgba(0, 0, 0, 0.5);
}
[data-agentation-theme=light] .styles-module__markerTooltip___-VUm- .styles-module__markerNote___Rh4eI {
  color: rgba(0, 0, 0, 0.85);
}`,d4={marker:"styles-module__marker___9CKF7",enter:"styles-module__enter___8kI3q",exit:"styles-module__exit___KBdR3",clearing:"styles-module__clearing___8rM7K",markerIn:"styles-module__markerIn___x4G8D",markerOut:"styles-module__markerOut___6VhQN",pending:"styles-module__pending___BiY-U",fixed:"styles-module__fixed___aKrQO",multiSelect:"styles-module__multiSelect___CPfTC",hovered:"styles-module__hovered___-mg2N",renumber:"styles-module__renumber___16lvD",renumberRoll:"styles-module__renumberRoll___akV9B",markerTooltip:"styles-module__markerTooltip___-VUm-",tooltipIn:"styles-module__tooltipIn___aJslQ",markerQuote:"styles-module__markerQuote___tQake",markerNote:"styles-module__markerNote___Rh4eI"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-annotation-marker-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-annotation-marker-styles",document.head.appendChild(e)),e.textContent=u4}var qt=d4;function dy({annotation:e,globalIndex:t,layerIndex:n,layerSize:l,isExiting:o,isClearing:a,isAnimated:i,isHovered:s,isDeleting:r,isEditingAny:p,renumberFrom:f,markerClickBehavior:b,tooltipStyle:_,onHoverEnter:w,onHoverLeave:C,onClick:z,onContextMenu:D}){let h=(s||r)&&!p,y=h&&b==="delete",k=e.isMultiSelect,E=k?"var(--agentation-color-green)":"var(--agentation-color-accent)",Q=o?qt.exit:a?qt.clearing:i?"":qt.enter,oe=o?`${(l-1-n)*20}ms`:`${n*20}ms`;return(0,Xn.jsxs)("div",{className:`${qt.marker} ${k?qt.multiSelect:""} ${Q} ${y?qt.hovered:""}`,"data-annotation-marker":!0,style:{left:`${e.x}%`,top:e.y,backgroundColor:y?void 0:E,animationDelay:oe},onMouseEnter:()=>w(e),onMouseLeave:C,onClick:L=>{L.stopPropagation(),o||z(e)},onContextMenu:D?L=>{b==="delete"&&(L.preventDefault(),L.stopPropagation(),o||D(e))}:void 0,children:[h?y?(0,Xn.jsx)(yy,{size:k?18:16}):(0,Xn.jsx)(Sb,{size:16}):(0,Xn.jsx)("span",{className:f!==null&&t>=f?qt.renumber:void 0,children:t+1}),s&&!p&&(0,Xn.jsxs)("div",{className:`${qt.markerTooltip} ${qt.enter}`,style:_,children:[(0,Xn.jsxs)("span",{className:qt.markerQuote,children:[e.element,e.selectedText&&` "${e.selectedText.slice(0,30)}${e.selectedText.length>30?"...":""}"`]}),(0,Xn.jsx)("span",{className:qt.markerNote,children:e.comment})]})]})}function _4({x:e,y:t,isMultiSelect:n,isExiting:l}){return(0,Xn.jsx)("div",{className:`${qt.marker} ${qt.pending} ${n?qt.multiSelect:""} ${l?qt.exit:qt.enter}`,style:{left:`${e}%`,top:t,backgroundColor:n?"var(--agentation-color-green)":"var(--agentation-color-accent)"},children:(0,Xn.jsx)(_b,{size:12})})}function _y({annotation:e,fixed:t}){let n=e.isMultiSelect;return(0,Xn.jsx)("div",{className:`${qt.marker} ${t?qt.fixed:""} ${qt.hovered} ${n?qt.multiSelect:""} ${qt.exit}`,"data-annotation-marker":!0,style:{left:`${e.x}%`,top:e.y},children:(0,Xn.jsx)(yy,{size:n?12:10})})}var f4=`.styles-module__switchContainer___Ka-AB {
  display: flex;
  align-items: center;
  position: relative;
  padding: 2px;
  width: 24px;
  height: 16px;
  border-radius: 8px;
  background-color: #cdcdcd;
  transition: background-color 0.15s, opacity 0.15s;
}
[data-agentation-theme=dark] .styles-module__switchContainer___Ka-AB {
  background-color: #484848;
}
.styles-module__switchContainer___Ka-AB:has(.styles-module__switchInput___kYDSD:checked) {
  background-color: var(--agentation-color-blue);
}
.styles-module__switchContainer___Ka-AB:has(.styles-module__switchInput___kYDSD:disabled) {
  opacity: 0.3;
}

.styles-module__switchInput___kYDSD {
  position: absolute;
  z-index: 1;
  inset: 0;
  border-radius: inherit;
  opacity: 0;
  cursor: pointer;
}
.styles-module__switchInput___kYDSD:disabled {
  cursor: not-allowed;
}

.styles-module__switchThumb___4sCPH {
  border-radius: 50%;
  width: 12px;
  height: 12px;
  background-color: #fff;
  transition: transform 0.15s;
}
.styles-module__switchContainer___Ka-AB:has(.styles-module__switchInput___kYDSD:checked) .styles-module__switchThumb___4sCPH {
  transform: translateX(8px);
}`,h4={switchContainer:"styles-module__switchContainer___Ka-AB",switchInput:"styles-module__switchInput___kYDSD",switchThumb:"styles-module__switchThumb___4sCPH"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-switch-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-switch-styles",document.head.appendChild(e)),e.textContent=f4}var rf=h4,cf=({className:e="",...t})=>(0,Gs.jsxs)("div",{className:`${rf.switchContainer} ${e}`,children:[(0,Gs.jsx)("input",{className:rf.switchInput,type:"checkbox",...t}),(0,Gs.jsx)("div",{className:rf.switchThumb})]}),m4=`.styles-module__checkboxContainer___joqZk {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border: 1px solid rgba(26, 26, 26, 0.2);
  border-radius: 4px;
  width: 14px;
  height: 14px;
  background-color: #fff;
  transition: background-color 0.2s ease;
}
[data-agentation-theme=dark] .styles-module__checkboxContainer___joqZk {
  border-color: rgba(255, 255, 255, 0.2);
  background-color: #252525;
}
.styles-module__checkboxContainer___joqZk:has(.styles-module__checkboxInput___ECzzO:checked) {
  background-color: #1a1a1a;
}
[data-agentation-theme=dark] .styles-module__checkboxContainer___joqZk:has(.styles-module__checkboxInput___ECzzO:checked) {
  background-color: #fff;
}

.styles-module__checkboxInput___ECzzO {
  position: absolute;
  z-index: 1;
  inset: -1px;
  border-radius: inherit;
  opacity: 0;
  cursor: pointer;
}

.styles-module__checkboxCheck___fUXpr {
  color: #fafafa;
}
[data-agentation-theme=dark] .styles-module__checkboxCheck___fUXpr {
  color: #1a1a1a;
}

.styles-module__checkboxCheckPath___cDyh8 {
  stroke-dasharray: 9.29px;
  stroke-dashoffset: 9.29px;
  color: #fafafa;
  transition: stroke-dashoffset 0.1s ease;
}
[data-agentation-theme=dark] .styles-module__checkboxCheckPath___cDyh8 {
  color: #1a1a1a;
}
.styles-module__checkboxContainer___joqZk:has(.styles-module__checkboxInput___ECzzO:checked) .styles-module__checkboxCheckPath___cDyh8 {
  transition-duration: 0.2s;
  stroke-dashoffset: 0;
}`,g4={checkboxContainer:"styles-module__checkboxContainer___joqZk",checkboxInput:"styles-module__checkboxInput___ECzzO",checkboxCheck:"styles-module__checkboxCheck___fUXpr",checkboxCheckPath:"styles-module__checkboxCheckPath___cDyh8"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-checkbox-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-checkbox-styles",document.head.appendChild(e)),e.textContent=m4}var Vc=g4,y4=({className:e="",...t})=>(0,Si.jsxs)("div",{className:`${Vc.checkboxContainer} ${e}`,children:[(0,Si.jsx)("input",{className:Vc.checkboxInput,type:"checkbox",...t}),(0,Si.jsx)("svg",{className:Vc.checkboxCheck,width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",children:(0,Si.jsx)("path",{className:Vc.checkboxCheckPath,d:"M3.94 7L6.13 9.19L10.5 4.81",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})})]}),p4=`.styles-module__container___w8eAF {
  display: flex;
  align-items: center;
  height: 24px;
}

.styles-module__label___J5mxE {
  padding-inline: 8px 2px;
  line-height: 20px;
  font-size: 13px;
  letter-spacing: -0.15px;
  color: rgba(26, 26, 26, 0.5);
  cursor: pointer;
}
[data-agentation-theme=dark] .styles-module__label___J5mxE {
  color: rgba(255, 255, 255, 0.5);
}`,b4={container:"styles-module__container___w8eAF",label:"styles-module__label___J5mxE"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-checkbox-field-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-checkbox-field-styles",document.head.appendChild(e)),e.textContent=p4}var fy=b4,hy=({className:e="",label:t,tooltip:n,checked:l,onChange:o,...a})=>{let i=(0,Ry.useId)();return(0,Ci.jsxs)("div",{className:`${fy.container} ${e}`,...a,children:[(0,Ci.jsx)(y4,{id:i,onChange:o,checked:l}),(0,Ci.jsx)("label",{className:fy.label,htmlFor:i,children:t}),n&&(0,Ci.jsx)(ga,{content:n})]})},x4=`@keyframes styles-module__cycleTextIn___VBNTi {
  0% {
    opacity: 0;
    transform: translateY(-6px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes styles-module__scaleIn___QpQ8E {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__mcpPulse___5Q3Jj {
  0% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-green) 50%, transparent);
  }
  70% {
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--agentation-color-green) 0%, transparent);
  }
  100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-green) 0%, transparent);
  }
}
@keyframes styles-module__mcpPulseError___VHxhx {
  0% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-red) 50%, transparent);
  }
  70% {
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--agentation-color-red) 0%, transparent);
  }
  100% {
    box-shadow: 0 0 0 0 color-mix(in srgb, var(--agentation-color-red) 0%, transparent);
  }
}
@keyframes styles-module__themeIconIn___qUWMV {
  0% {
    opacity: 0;
    transform: scale(0.8) rotate(-30deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}
.styles-module__settingsPanel___qNkn- {
  position: absolute;
  right: 5px;
  bottom: calc(100% + 0.5rem);
  z-index: 1;
  overflow: hidden;
  background: #1c1c1c;
  border-radius: 16px;
  padding: 12px 0;
  width: 100%;
  max-width: 253px;
  min-width: 205px;
  cursor: default;
  opacity: 1;
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: background-color 0.25s ease, box-shadow 0.25s ease;
}
.styles-module__settingsPanel___qNkn-::before, .styles-module__settingsPanel___qNkn-::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 16px;
  z-index: 2;
  pointer-events: none;
}
.styles-module__settingsPanel___qNkn-::before {
  left: 0;
  background: linear-gradient(to right, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___qNkn-::after {
  right: 0;
  background: linear-gradient(to left, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___qNkn- .styles-module__settingsHeader___Fn1DP,
.styles-module__settingsPanel___qNkn- .styles-module__settingsBrand___OoKlM,
.styles-module__settingsPanel___qNkn- .styles-module__settingsBrandSlash___Q-AU9,
.styles-module__settingsPanel___qNkn- .styles-module__settingsVersion___rXmL9,
.styles-module__settingsPanel___qNkn- .styles-module__settingsSection___n5V-4,
.styles-module__settingsPanel___qNkn- .styles-module__settingsLabel___VCVOQ,
.styles-module__settingsPanel___qNkn- .styles-module__cycleButton___XMBx3,
.styles-module__settingsPanel___qNkn- .styles-module__cycleDot___zgSXY,
.styles-module__settingsPanel___qNkn- .styles-module__dropdownButton___mKHe8,
.styles-module__settingsPanel___qNkn- .styles-module__sliderLabel___6K5v1,
.styles-module__settingsPanel___qNkn- .styles-module__slider___v5z-c,
.styles-module__settingsPanel___qNkn- .styles-module__themeToggle___3imlT {
  transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
}
.styles-module__settingsPanel___qNkn-.styles-module__enter___wginS {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0px);
  transition: opacity 0.2s ease, transform 0.2s ease, filter 0.2s ease;
}
.styles-module__settingsPanel___qNkn-.styles-module__exit___A4iJc {
  opacity: 0;
  transform: translateY(8px) scale(0.95);
  filter: blur(5px);
  pointer-events: none;
  transition: opacity 0.1s ease, transform 0.1s ease, filter 0.1s ease;
}
[data-agentation-theme=dark] .styles-module__settingsPanel___qNkn- {
  background: #1a1a1a;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___qNkn- .styles-module__settingsLabel___VCVOQ {
  color: rgba(255, 255, 255, 0.6);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___qNkn- .styles-module__settingsOption___JoyH- {
  color: rgba(255, 255, 255, 0.85);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___qNkn- .styles-module__settingsOption___JoyH-:hover {
  background: rgba(255, 255, 255, 0.1);
}
[data-agentation-theme=dark] .styles-module__settingsPanel___qNkn- .styles-module__settingsOption___JoyH-.styles-module__selected___k1-Vq {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.styles-module__settingsPanelContainer___5it-H {
  overflow: visible;
  position: relative;
  display: flex;
  padding: 0 16px;
}

.styles-module__settingsPage___BMn-3 {
  min-width: 100%;
  flex-basis: 0;
  flex-shrink: 0;
  transition: transform 0.2s ease, opacity 0.2s ease;
  transition-delay: 0s;
  opacity: 1;
}

.styles-module__settingsPage___BMn-3.styles-module__slideLeft___qUvW4 {
  transform: translateX(-24px);
  opacity: 0;
  pointer-events: none;
}

.styles-module__automationsPage___N7By0 {
  position: absolute;
  top: 0;
  left: 24px;
  width: 100%;
  height: 100%;
  padding: 0 16px 4px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, opacity 0.2s ease;
  opacity: 0;
  pointer-events: none;
}

.styles-module__automationsPage___N7By0.styles-module__slideIn___uXDSu {
  transform: translateX(-24px);
  opacity: 1;
  pointer-events: auto;
}

.styles-module__settingsHeader___Fn1DP {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 24px;
}

.styles-module__settingsBrand___OoKlM {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: -0.0094em;
  color: #fff;
  text-decoration: none;
}

.styles-module__settingsBrandSlash___Q-AU9 {
  color: var(--agentation-color-accent);
  transition: color 0.2s ease;
}

.styles-module__settingsVersion___rXmL9 {
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  margin-left: auto;
  letter-spacing: -0.0094em;
}

.styles-module__themeToggle___3imlT {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin-left: 8px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  transition: background-color 0.15s ease, color 0.15s ease;
  cursor: pointer;
}
.styles-module__themeToggle___3imlT:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}
[data-agentation-theme=light] .styles-module__themeToggle___3imlT {
  color: rgba(0, 0, 0, 0.4);
}
[data-agentation-theme=light] .styles-module__themeToggle___3imlT:hover {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.7);
}

.styles-module__themeIconWrapper___pyaYa {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 20px;
  height: 20px;
}

.styles-module__themeIcon___w7lAm {
  display: flex;
  align-items: center;
  justify-content: center;
  animation: styles-module__themeIconIn___qUWMV 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.styles-module__settingsSectionGrow___eZTRw {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.styles-module__settingsRow___y-tDE {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
}
.styles-module__settingsRow___y-tDE.styles-module__settingsRowMarginTop___uLpGb {
  margin-top: 8px;
}

.styles-module__settingsRowDisabled___ydl3Q .styles-module__settingsLabel___VCVOQ {
  color: rgba(255, 255, 255, 0.2);
}
[data-agentation-theme=light] .styles-module__settingsRowDisabled___ydl3Q .styles-module__settingsLabel___VCVOQ {
  color: rgba(0, 0, 0, 0.2);
}

.styles-module__settingsLabel___VCVOQ {
  display: flex;
  align-items: center;
  column-gap: 2px;
  line-height: 20px;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: -0.15px;
  color: rgba(255, 255, 255, 0.5);
}
[data-agentation-theme=light] .styles-module__settingsLabel___VCVOQ {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__cycleButton___XMBx3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  border: none;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  letter-spacing: -0.0094em;
}
[data-agentation-theme=light] .styles-module__cycleButton___XMBx3 {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__cycleButton___XMBx3:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.styles-module__cycleButtonText___mbbnD {
  display: inline-block;
  animation: styles-module__cycleTextIn___VBNTi 0.2s ease-out;
}

.styles-module__cycleDots___ehp6i {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.styles-module__cycleDot___zgSXY {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0.667);
  transition: background-color 0.25s ease-out, transform 0.25s ease-out;
}
.styles-module__cycleDot___zgSXY.styles-module__active___dpAhM {
  background: #fff;
  transform: scale(1);
}
[data-agentation-theme=light] .styles-module__cycleDot___zgSXY {
  background: rgba(0, 0, 0, 0.2);
}
[data-agentation-theme=light] .styles-module__cycleDot___zgSXY.styles-module__active___dpAhM {
  background: rgba(0, 0, 0, 0.7);
}

.styles-module__colorOptions___pbxZx {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  height: 26px;
}

.styles-module__colorOption___Co955 {
  padding: 0;
  position: relative;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  background-color: #fff;
  cursor: pointer;
}
[data-agentation-theme=dark] .styles-module__colorOption___Co955 {
  background-color: #1a1a1a;
}
.styles-module__colorOption___Co955::before, .styles-module__colorOption___Co955::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background-color: var(--swatch);
  transition: opacity 0.2s, transform 0.2s;
}
@supports (color: color(display-p3 0 0 0)) {
  .styles-module__colorOption___Co955::before, .styles-module__colorOption___Co955::after {
    --color: var(--swatch-p3);
  }
}
.styles-module__colorOption___Co955::after {
  z-index: -1;
  transform: scale(1.2);
  opacity: 0;
}
.styles-module__colorOption___Co955.styles-module__selected___k1-Vq::before {
  transform: scale(0.8);
}
.styles-module__colorOption___Co955.styles-module__selected___k1-Vq::after {
  opacity: 1;
}

.styles-module__settingsNavLink___uYIwM {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 24px;
  padding: 0;
  border: none;
  background: transparent;
  font-family: inherit;
  line-height: 20px;
  font-size: 13px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  transition: color 0.15s ease;
  cursor: pointer;
}
.styles-module__settingsNavLink___uYIwM:hover {
  color: rgba(255, 255, 255, 0.9);
}
.styles-module__settingsNavLink___uYIwM svg {
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s ease;
}
.styles-module__settingsNavLink___uYIwM:hover svg {
  color: #fff;
}
[data-agentation-theme=light] .styles-module__settingsNavLink___uYIwM {
  color: rgba(0, 0, 0, 0.5);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___uYIwM:hover {
  color: rgba(0, 0, 0, 0.8);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___uYIwM svg {
  color: rgba(0, 0, 0, 0.25);
}
[data-agentation-theme=light] .styles-module__settingsNavLink___uYIwM:hover svg {
  color: rgba(0, 0, 0, 0.8);
}

.styles-module__settingsNavLinkRight___XBUzC {
  display: flex;
  align-items: center;
  gap: 6px;
}

.styles-module__settingsBackButton___fflll {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 24px;
  background: transparent;
  font-family: inherit;
  line-height: 20px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.15px;
  color: #fff;
  cursor: pointer;
  transition: transform 0.12s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___fflll svg {
  opacity: 0.4;
  flex-shrink: 0;
  transition: opacity 0.15s ease, transform 0.18s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___fflll:hover svg {
  opacity: 1;
}
[data-agentation-theme=light] .styles-module__settingsBackButton___fflll {
  color: rgba(0, 0, 0, 0.85);
  border-bottom-color: rgba(0, 0, 0, 0.08);
}

.styles-module__automationHeader___Avra9 {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  font-size: 0.8125rem;
  font-weight: 400;
  color: #fff;
}
[data-agentation-theme=light] .styles-module__automationHeader___Avra9 {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__automationDescription___vFTmJ {
  font-size: 0.6875rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 2px;
  line-height: 14px;
}
[data-agentation-theme=light] .styles-module__automationDescription___vFTmJ {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__learnMoreLink___cG7OI {
  color: rgba(255, 255, 255, 0.8);
  text-decoration-line: underline;
  text-decoration-style: dotted;
  text-decoration-color: rgba(255, 255, 255, 0.2);
  text-underline-offset: 2px;
  transition: color 0.15s ease;
}
.styles-module__learnMoreLink___cG7OI:hover {
  color: #fff;
}
[data-agentation-theme=light] .styles-module__learnMoreLink___cG7OI {
  color: rgba(0, 0, 0, 0.6);
  text-decoration-color: rgba(0, 0, 0, 0.2);
}
[data-agentation-theme=light] .styles-module__learnMoreLink___cG7OI:hover {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__autoSendContainer___VpkXk {
  display: flex;
  align-items: center;
}

.styles-module__autoSendLabel___ngNdC {
  padding-inline-end: 8px;
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s, opacity 0.15s;
  cursor: pointer;
}
.styles-module__autoSendLabel___ngNdC.styles-module__active___dpAhM {
  color: #66b8ff;
  color: color(display-p3 0.4 0.72 1);
}
[data-agentation-theme=light] .styles-module__autoSendLabel___ngNdC {
  color: rgba(0, 0, 0, 0.4);
}
[data-agentation-theme=light] .styles-module__autoSendLabel___ngNdC.styles-module__active___dpAhM {
  color: var(--agentation-color-blue);
}
.styles-module__autoSendLabel___ngNdC.styles-module__disabled___9AZYS {
  opacity: 0.3;
  cursor: not-allowed;
}

.styles-module__mcpStatusDot___8AMxP {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpStatusDot___8AMxP.styles-module__connecting___QEO1r {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__mcpPulse___5Q3Jj 1.5s infinite;
}
.styles-module__mcpStatusDot___8AMxP.styles-module__connected___WyFkx {
  background-color: var(--agentation-color-green);
  animation: styles-module__mcpPulse___5Q3Jj 2.5s ease-in-out infinite;
}
.styles-module__mcpStatusDot___8AMxP.styles-module__disconnected___mvmvQ {
  background-color: var(--agentation-color-red);
  animation: styles-module__mcpPulseError___VHxhx 2s infinite;
}

.styles-module__mcpNavIndicator___auBHI {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpNavIndicator___auBHI.styles-module__connected___WyFkx {
  background-color: var(--agentation-color-green);
  animation: styles-module__mcpPulse___5Q3Jj 2.5s ease-in-out infinite;
}
.styles-module__mcpNavIndicator___auBHI.styles-module__connecting___QEO1r {
  background-color: var(--agentation-color-yellow);
  animation: styles-module__mcpPulse___5Q3Jj 1.5s ease-in-out infinite;
}

.styles-module__webhookUrlInput___WDDDC {
  display: block;
  width: 100%;
  flex: 1;
  min-height: 60px;
  box-sizing: border-box;
  margin-top: 11px;
  padding: 8px 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  font-family: inherit;
  font-size: 0.75rem;
  font-weight: 400;
  color: #fff;
  outline: none;
  resize: none;
  user-select: text;
  transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
}
.styles-module__webhookUrlInput___WDDDC::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.styles-module__webhookUrlInput___WDDDC:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___WDDDC {
  border-color: rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.03);
  color: rgba(0, 0, 0, 0.85);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___WDDDC::placeholder {
  color: rgba(0, 0, 0, 0.3);
}
[data-agentation-theme=light] .styles-module__webhookUrlInput___WDDDC:focus {
  border-color: rgba(0, 0, 0, 0.25);
  background: rgba(0, 0, 0, 0.05);
}

[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn-::before {
  background: linear-gradient(to right, #fff 0%, transparent 100%);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn-::after {
  background: linear-gradient(to left, #fff 0%, transparent 100%);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__settingsHeader___Fn1DP {
  border-bottom-color: rgba(0, 0, 0, 0.08);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__settingsBrand___OoKlM {
  color: #E5484D;
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__settingsVersion___rXmL9 {
  color: rgba(0, 0, 0, 0.4);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__settingsSection___n5V-4 {
  border-top-color: rgba(0, 0, 0, 0.08);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__settingsLabel___VCVOQ {
  color: rgba(0, 0, 0, 0.5);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__cycleButton___XMBx3 {
  color: rgba(0, 0, 0, 0.85);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__cycleDot___zgSXY {
  background: rgba(0, 0, 0, 0.2);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__cycleDot___zgSXY.styles-module__active___dpAhM {
  background: rgba(0, 0, 0, 0.7);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__dropdownButton___mKHe8 {
  color: rgba(0, 0, 0, 0.85);
}
[data-agentation-theme=light] .styles-module__settingsPanel___qNkn- .styles-module__dropdownButton___mKHe8:hover {
  background: rgba(0, 0, 0, 0.05);
}

.styles-module__checkboxField___ZrSqv:not(:first-child) {
  margin-top: 8px;
}

.styles-module__divider___h6Yux {
  margin-block: 8px;
  width: 100%;
  height: 1px;
  background-color: rgba(26, 26, 26, 0.07);
}
[data-agentation-theme=dark] .styles-module__divider___h6Yux {
  background-color: rgba(255, 255, 255, 0.07);
}`,v4={settingsPanel:"styles-module__settingsPanel___qNkn-",settingsHeader:"styles-module__settingsHeader___Fn1DP",settingsBrand:"styles-module__settingsBrand___OoKlM",settingsBrandSlash:"styles-module__settingsBrandSlash___Q-AU9",settingsVersion:"styles-module__settingsVersion___rXmL9",settingsSection:"styles-module__settingsSection___n5V-4",settingsLabel:"styles-module__settingsLabel___VCVOQ",cycleButton:"styles-module__cycleButton___XMBx3",cycleDot:"styles-module__cycleDot___zgSXY",dropdownButton:"styles-module__dropdownButton___mKHe8",sliderLabel:"styles-module__sliderLabel___6K5v1",slider:"styles-module__slider___v5z-c",themeToggle:"styles-module__themeToggle___3imlT",enter:"styles-module__enter___wginS",exit:"styles-module__exit___A4iJc",settingsOption:"styles-module__settingsOption___JoyH-",selected:"styles-module__selected___k1-Vq",settingsPanelContainer:"styles-module__settingsPanelContainer___5it-H",settingsPage:"styles-module__settingsPage___BMn-3",slideLeft:"styles-module__slideLeft___qUvW4",automationsPage:"styles-module__automationsPage___N7By0",slideIn:"styles-module__slideIn___uXDSu",themeIconWrapper:"styles-module__themeIconWrapper___pyaYa",themeIcon:"styles-module__themeIcon___w7lAm",themeIconIn:"styles-module__themeIconIn___qUWMV",settingsSectionGrow:"styles-module__settingsSectionGrow___eZTRw",settingsRow:"styles-module__settingsRow___y-tDE",settingsRowMarginTop:"styles-module__settingsRowMarginTop___uLpGb",settingsRowDisabled:"styles-module__settingsRowDisabled___ydl3Q",cycleButtonText:"styles-module__cycleButtonText___mbbnD",cycleTextIn:"styles-module__cycleTextIn___VBNTi",cycleDots:"styles-module__cycleDots___ehp6i",active:"styles-module__active___dpAhM",colorOptions:"styles-module__colorOptions___pbxZx",colorOption:"styles-module__colorOption___Co955",settingsNavLink:"styles-module__settingsNavLink___uYIwM",settingsNavLinkRight:"styles-module__settingsNavLinkRight___XBUzC",settingsBackButton:"styles-module__settingsBackButton___fflll",automationHeader:"styles-module__automationHeader___Avra9",automationDescription:"styles-module__automationDescription___vFTmJ",learnMoreLink:"styles-module__learnMoreLink___cG7OI",autoSendContainer:"styles-module__autoSendContainer___VpkXk",autoSendLabel:"styles-module__autoSendLabel___ngNdC",disabled:"styles-module__disabled___9AZYS",mcpStatusDot:"styles-module__mcpStatusDot___8AMxP",connecting:"styles-module__connecting___QEO1r",mcpPulse:"styles-module__mcpPulse___5Q3Jj",connected:"styles-module__connected___WyFkx",disconnected:"styles-module__disconnected___mvmvQ",mcpPulseError:"styles-module__mcpPulseError___VHxhx",mcpNavIndicator:"styles-module__mcpNavIndicator___auBHI",webhookUrlInput:"styles-module__webhookUrlInput___WDDDC",checkboxField:"styles-module__checkboxField___ZrSqv",divider:"styles-module__divider___h6Yux",scaleIn:"styles-module__scaleIn___QpQ8E"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-settings-panel-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-settings-panel-styles",document.head.appendChild(e)),e.textContent=x4}var ne=v4;function w4({settings:e,onSettingsChange:t,isDarkMode:n,onToggleTheme:l,isDevMode:o,connectionStatus:a,endpoint:i,isVisible:s,toolbarNearBottom:r,settingsPage:p,onSettingsPageChange:f,onHideToolbar:b}){return(0,Z.jsx)("div",{className:`${ne.settingsPanel} ${s?ne.enter:ne.exit}`,style:r?{bottom:"auto",top:"calc(100% + 0.5rem)"}:void 0,"data-agentation-settings-panel":!0,children:(0,Z.jsxs)("div",{className:ne.settingsPanelContainer,children:[(0,Z.jsxs)("div",{className:`${ne.settingsPage} ${p==="automations"?ne.slideLeft:""}`,children:[(0,Z.jsxs)("div",{className:ne.settingsHeader,children:[(0,Z.jsx)("a",{className:ne.settingsBrand,href:"https://agentation.com",target:"_blank",rel:"noopener noreferrer",children:(0,Z.jsx)("svg",{width:"72",height:"16",viewBox:"0 0 676 151",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,Z.jsx)("path",{d:"M79.6666 100.561L104.863 15.5213C107.828 4.03448 99.1201 -3.00582 88.7449 1.25541L3.52015 39.6065C1.48217 40.5329 0 42.7562 0 45.1647C0 48.6848 2.77907 51.4639 6.29922 51.4639C7.22558 51.4639 8.15193 51.2786 9.07829 50.9081L93.7472 12.7422C97.2674 11.0748 93.7472 8.29572 92.6356 12.1864L67.624 97.2259C66.5123 100.931 69.4767 105.193 73.7379 105.193C76.517 105.193 79.1108 103.155 79.6666 100.561ZM663.641 100.005C665.679 107.231 677.537 104.081 675.499 96.8553L666.05 66.2856C663.456 57.7631 655.489 55.7251 648.82 61.098L618.991 86.6654C617.324 87.9623 621.029 89.815 621.214 88.1476L625.846 61.6538C626.958 55.3546 624.179 50.5375 615.841 50.5375L579.158 51.0934C576.008 51.0934 578.417 53.8724 578.417 57.022C578.417 60.1716 580.825 61.6538 583.975 61.6538L616.212 60.9127C616.397 60.9127 614.544 59.6158 614.544 59.8011L609.727 88.7034C607.875 99.6344 617.694 102.784 626.031 95.7437L655.86 70.1763L654.192 69.6205L663.641 100.005ZM571.191 89.0739C555.443 88.7034 562.298 61.4685 578.787 61.8391C594.72 62.0243 587.124 89.2592 571.191 89.0739ZM571.006 100.375C601.575 100.931 611.024 51.6492 579.158 51.0934C547.847 50.5375 540.065 99.8197 571.006 100.375ZM521.909 46.4616C525.985 46.4616 529.505 42.9414 529.505 38.6802C529.505 34.4189 525.985 31.0841 521.909 31.0841C517.833 31.0841 514.127 34.6042 514.127 38.6802C514.127 42.7562 517.648 46.4616 521.909 46.4616ZM472.256 103.525C493.192 103.71 515.98 73.3259 519.13 62.3949L509.866 60.9127C505.234 73.3259 497.638 101.672 519.871 102.043C536.545 102.228 552.479 85.3685 563.595 70.1763C564.151 69.2499 564.706 68.1383 564.706 66.8414C564.706 63.6918 563.965 61.098 560.816 61.098C558.963 61.098 557.296 62.0243 556.184 63.5065C546.365 77.0313 530.802 90.9266 522.094 90.7414C511.904 90.5561 517.462 71.4732 519.871 64.9887C523.391 55.7251 512.831 53.5019 509.681 60.9127C506.531 68.6941 488.19 92.4088 475.035 92.2235C467.439 92.0383 464.29 83.8863 472.441 59.9864L486.707 17.7445C487.634 14.4097 485.41 10.519 481.334 10.519C478.741 10.519 476.517 12.1864 475.962 14.4097L461.696 56.4662C451.506 86.4801 455.211 103.155 472.256 103.525ZM447.43 42.5709L496.527 41.4593C499.306 41.4593 501.529 39.0507 501.529 36.2717C501.529 33.3073 499.306 31.0841 496.341 31.0841L447.245 32.1957C444.466 32.1957 442.242 34.4189 442.242 37.3833C442.242 40.1624 444.466 42.5709 447.43 42.5709ZM422.974 106.304C435.387 106.489 457.249 94.8173 472.441 53.8724C473.553 50.7228 472.071 48.3143 468.365 48.3143C466.142 48.3143 464.29 49.6112 463.548 51.6492C450.394 87.2212 431.682 96.1142 424.456 95.929C419.454 95.929 417.972 93.3352 418.713 85.5538C419.454 78.1429 410.376 74.9933 406.114 81.1073C401.297 87.777 394.442 94.2615 385.549 94.0763C370.172 93.891 376.471 67.0267 399.815 67.3972C408.338 67.5825 414.452 71.4732 417.045 76.6608C417.786 78.3282 419.454 79.6251 421.492 79.6251C424.271 79.6251 426.679 77.2166 426.679 74.4375C426.679 73.6964 426.494 72.9553 426.124 72.2143C421.862 63.6918 412.414 57.3926 400 57.2073C363.502 56.6515 353.497 104.451 383.326 104.822C397.036 105.193 410.005 94.0763 413.34 85.9243C412.599 86.8507 408.338 86.6654 408.523 84.4422C407.411 97.4111 410.931 106.119 422.974 106.304ZM335.897 104.266C335.897 115.012 347.569 117.606 347.569 103.34C347.569 89.0739 358.5 54.4282 361.464 45.1647L396.666 43.6825C405.929 43.1267 404.262 33.1221 397.036 33.3073L364.984 34.4189L368.875 22.7469C369.801 20.1531 370.542 17.9298 370.542 16.2624C370.542 13.4833 368.504 11.8159 365.911 11.8159C362.946 11.8159 360.352 12.7422 357.573 21.0794L352.942 35.16L330.153 36.0864C326.263 36.4569 323.483 38.1244 323.483 41.6445C323.483 45.5352 326.448 47.0174 330.709 46.8321L349.421 45.9058C345.901 56.6515 335.897 90.7414 335.897 104.266ZM186.939 78.6988C193.979 56.4662 212.877 54.984 212.877 62.9507C212.877 68.3236 203.984 77.0313 186.939 78.6988ZM113.942 150.955C142.844 152.437 159.704 111.492 160.63 80.5515C161.556 73.3259 153.96 70.3616 148.773 75.7344C141.918 83.1453 129.505 93.1499 119.685 93.1499C103.011 93.1499 116.165 59.8011 143.956 59.8011C149.514 59.8011 153.59 61.6538 156.184 64.0623C160.815 68.3236 170.82 62.0243 165.818 56.0957C161.927 51.4639 155.072 48.129 144.882 48.129C102.455 48.129 83.7426 105.007 116.721 105.007C134.692 105.007 151.367 88.3329 155.257 82.7747C154.516 83.5158 149.329 81.2925 149.699 79.4398L149.143 83.5158C148.958 107.045 134.322 141.506 116.536 139.838C113.386 139.468 112.089 137.43 112.089 134.836C112.089 128.907 122.094 119.273 145.067 113.53C159.518 109.824 152.293 101.487 143.4 104.081C111.163 113.53 99.6759 127.425 99.6759 137.8C99.6759 145.026 105.605 150.584 113.942 150.955ZM194.72 109.454C214.359 109.454 239 95.3732 251.228 77.9577C250.301 82.96 246.596 96.8553 246.596 101.487C246.596 110.01 254.748 109.454 261.232 102.784L288.097 75.5491L290.32 85.7391C293.284 99.4491 299.213 104.822 308.847 104.822C326.263 104.822 342.196 85.7391 349.421 74.8081L344.049 63.6918C339.787 74.8081 321.631 92.5941 311.626 92.5941C306.994 92.5941 304.771 89.815 303.289 83.7011L300.325 71.2879C297.916 60.7275 289.023 58.3189 279.018 68.1383L261.788 84.8127L264.382 69.991C266.235 59.2453 255.674 58.1337 250.116 65.915C241.779 77.0313 216.767 97.7817 196.387 97.7817C187.865 97.7817 185.456 93.7057 185.456 88.3329C230.848 84.998 239.185 47.2027 208.986 47.2027C172.858 47.2027 157.11 109.454 194.72 109.454Z",fill:"currentColor"})})}),(0,Z.jsxs)("p",{className:ne.settingsVersion,children:["v","3.0.2"]}),(0,Z.jsx)("button",{className:ne.themeToggle,onClick:l,title:n?"Switch to light mode":"Switch to dark mode",children:(0,Z.jsx)("span",{className:ne.themeIconWrapper,children:(0,Z.jsx)("span",{className:ne.themeIcon,children:n?(0,Z.jsx)(wb,{size:20}):(0,Z.jsx)(kb,{size:20})},n?"sun":"moon")})})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("div",{className:ne.settingsSection,children:[(0,Z.jsxs)("div",{className:ne.settingsRow,children:[(0,Z.jsxs)("div",{className:ne.settingsLabel,children:["Output Detail",(0,Z.jsx)(ga,{content:"Controls how much detail is included in the copied output"})]}),(0,Z.jsxs)("button",{className:ne.cycleButton,onClick:()=>{let w=(qs.findIndex(C=>C.value===e.outputDetail)+1)%qs.length;t({outputDetail:qs[w].value})},children:[(0,Z.jsx)("span",{className:ne.cycleButtonText,children:qs.find(_=>_.value===e.outputDetail)?.label},e.outputDetail),(0,Z.jsx)("span",{className:ne.cycleDots,children:qs.map(_=>(0,Z.jsx)("span",{className:`${ne.cycleDot} ${e.outputDetail===_.value?ne.active:""}`},_.value))})]})]}),(0,Z.jsxs)("div",{className:`${ne.settingsRow} ${ne.settingsRowMarginTop} ${o?"":ne.settingsRowDisabled}`,children:[(0,Z.jsxs)("div",{className:ne.settingsLabel,children:["React Components",(0,Z.jsx)(ga,{content:o?"Include React component names in annotations":"Disabled \u2014 production builds minify component names, making detection unreliable. Use in development mode."})]}),(0,Z.jsx)(cf,{checked:o&&e.reactEnabled,onChange:_=>t({reactEnabled:_.target.checked}),disabled:!o})]}),(0,Z.jsxs)("div",{className:`${ne.settingsRow} ${ne.settingsRowMarginTop}`,children:[(0,Z.jsxs)("div",{className:ne.settingsLabel,children:["Hide Until Restart",(0,Z.jsx)(ga,{content:"Hides the toolbar until you open a new tab"})]}),(0,Z.jsx)(cf,{checked:!1,onChange:_=>{_.target.checked&&b()}})]})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("div",{className:ne.settingsSection,children:[(0,Z.jsx)("div",{className:`${ne.settingsLabel} ${ne.settingsLabelMarker}`,children:"Marker Color"}),(0,Z.jsx)("div",{className:ne.colorOptions,children:Qs.map(_=>(0,Z.jsx)("button",{className:`${ne.colorOption} ${e.annotationColorId===_.id?ne.selected:""}`,style:{"--swatch":_.srgb,"--swatch-p3":_.p3},onClick:()=>t({annotationColorId:_.id}),title:_.label,type:"button"},_.id))})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("div",{className:ne.settingsSection,children:[(0,Z.jsx)(hy,{className:"checkbox-field",label:"Clear on copy/send",checked:e.autoClearAfterCopy,onChange:_=>t({autoClearAfterCopy:_.target.checked}),tooltip:"Automatically clear annotations after copying"}),(0,Z.jsx)(hy,{className:ne.checkboxField,label:"Block page interactions",checked:e.blockInteractions,onChange:_=>t({blockInteractions:_.target.checked})})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("button",{className:ne.settingsNavLink,onClick:()=>f("automations"),children:[(0,Z.jsx)("span",{children:"Manage MCP & Webhooks"}),(0,Z.jsxs)("span",{className:ne.settingsNavLinkRight,children:[i&&a!=="disconnected"&&(0,Z.jsx)("span",{className:`${ne.mcpNavIndicator} ${ne[a]}`}),(0,Z.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,Z.jsx)("path",{d:"M7.5 12.5L12 8L7.5 3.5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})})]})]})]}),(0,Z.jsxs)("div",{className:`${ne.settingsPage} ${ne.automationsPage} ${p==="automations"?ne.slideIn:""}`,children:[(0,Z.jsxs)("button",{className:ne.settingsBackButton,onClick:()=>f("main"),children:[(0,Z.jsx)(Mb,{size:16}),(0,Z.jsx)("span",{children:"Manage MCP & Webhooks"})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("div",{className:ne.settingsSection,children:[(0,Z.jsxs)("div",{className:ne.settingsRow,children:[(0,Z.jsxs)("span",{className:ne.automationHeader,children:["MCP Connection",(0,Z.jsx)(ga,{content:"Connect via Model Context Protocol to let AI agents like Claude Code receive annotations in real-time."})]}),i&&(0,Z.jsx)("div",{className:`${ne.mcpStatusDot} ${ne[a]}`,title:a==="connected"?"Connected":a==="connecting"?"Connecting...":"Disconnected"})]}),(0,Z.jsxs)("p",{className:ne.automationDescription,style:{paddingBottom:6},children:["MCP connection allows agents to receive and act on annotations."," ",(0,Z.jsx)("a",{href:"https://agentation.dev/mcp",target:"_blank",rel:"noopener noreferrer",className:ne.learnMoreLink,children:"Learn more"})]})]}),(0,Z.jsx)("div",{className:ne.divider}),(0,Z.jsxs)("div",{className:`${ne.settingsSection} ${ne.settingsSectionGrow}`,children:[(0,Z.jsxs)("div",{className:ne.settingsRow,children:[(0,Z.jsxs)("span",{className:ne.automationHeader,children:["Webhooks",(0,Z.jsx)(ga,{content:"Send annotation data to any URL endpoint when annotations change. Useful for custom integrations."})]}),(0,Z.jsxs)("div",{className:ne.autoSendContainer,children:[(0,Z.jsx)("label",{htmlFor:"agentation-auto-send",className:`${ne.autoSendLabel} ${e.webhooksEnabled?ne.active:""} ${e.webhookUrl?"":ne.disabled}`,children:"Auto-Send"}),(0,Z.jsx)(cf,{id:"agentation-auto-send",checked:e.webhooksEnabled,onChange:_=>t({webhooksEnabled:_.target.checked}),disabled:!e.webhookUrl})]})]}),(0,Z.jsx)("p",{className:ne.automationDescription,children:"The webhook URL will receive live annotation changes and annotation data."}),(0,Z.jsx)("textarea",{className:ne.webhookUrlInput,placeholder:"Webhook URL",value:e.webhookUrl,onKeyDown:_=>_.stopPropagation(),onChange:_=>t({webhookUrl:_.target.value})})]})]})]})})}function uf(e,t="filtered"){let{name:n,path:l}=ki(e);if(t==="off")return{name:n,elementName:n,path:l,reactComponents:null};let o=Kv(e,{mode:t});return{name:o.path?`${o.path} ${n}`:n,elementName:n,path:l,reactComponents:o.path}}var my=!1,df={outputDetail:"standard",autoClearAfterCopy:!1,annotationColorId:"blue",blockInteractions:!0,reactEnabled:!0,markerClickBehavior:"edit",webhookUrl:"",webhooksEnabled:!0},Al=e=>{if(!e||!e.trim())return!1;try{let t=new URL(e.trim());return t.protocol==="http:"||t.protocol==="https:"}catch{return!1}},k4={compact:"off",standard:"filtered",detailed:"smart",forensic:"all"},Qs=[{id:"indigo",label:"Indigo",srgb:"#6155F5",p3:"color(display-p3 0.38 0.33 0.96)"},{id:"blue",label:"Blue",srgb:"#0088FF",p3:"color(display-p3 0.00 0.53 1.00)"},{id:"cyan",label:"Cyan",srgb:"#00C3D0",p3:"color(display-p3 0.00 0.76 0.82)"},{id:"green",label:"Green",srgb:"#34C759",p3:"color(display-p3 0.20 0.78 0.35)"},{id:"yellow",label:"Yellow",srgb:"#FFCC00",p3:"color(display-p3 1.00 0.80 0.00)"},{id:"orange",label:"Orange",srgb:"#FF8D28",p3:"color(display-p3 1.00 0.55 0.16)"},{id:"red",label:"Red",srgb:"#FF383C",p3:"color(display-p3 1.00 0.22 0.24)"}],S4=()=>{if(typeof document>"u"||document.getElementById("agentation-color-tokens"))return;let e=document.createElement("style");e.id="agentation-color-tokens",e.textContent=[...Qs.map(t=>`
      [data-agentation-accent="${t.id}"] {
        --agentation-color-accent: ${t.srgb};
      }

      @supports (color: color(display-p3 0 0 0)) {
        [data-agentation-accent="${t.id}"] {
          --agentation-color-accent: ${t.p3};
        }
      }
    `),`:root {
      ${Qs.map(t=>`--agentation-color-${t.id}: ${t.srgb};`).join(`
`)}
    }`,`@supports (color: color(display-p3 0 0 0)) {
      :root {
        ${Qs.map(t=>`--agentation-color-${t.id}: ${t.p3};`).join(`
`)}
      }
    }`].join(""),document.head.appendChild(e)};S4();function ha(e,t){let n=document.elementFromPoint(e,t);if(!n)return null;for(;n?.shadowRoot;){let l=n.shadowRoot.elementFromPoint(e,t);if(!l||l===n)break;n=l}return n}function _f(e){let t=e;for(;t&&t!==document.body;){let l=window.getComputedStyle(t).position;if(l==="fixed"||l==="sticky")return!0;t=t.parentElement}return!1}function ma(e){return e.status!=="resolved"&&e.status!=="dismissed"}function Zc(e){let t=xf(e),n=t.found?t:s4(e);if(n.found&&n.source)return i4(n.source,"path")}function By({demoAnnotations:e,demoDelay:t=1e3,enableDemoMode:n=!1,onAnnotationAdd:l,onAnnotationDelete:o,onAnnotationUpdate:a,onAnnotationsClear:i,onCopy:s,onSubmit:r,copyToClipboard:p=!0,endpoint:f,sessionId:b,onSessionCreated:_,webhookUrl:w,className:C}={}){let[z,D]=(0,T.useState)(!1),[h,y]=(0,T.useState)([]),[k,E]=(0,T.useState)(!0),[Q,oe]=(0,T.useState)(()=>Ov()),[L,K]=(0,T.useState)(!1),ee=(0,T.useRef)(null);(0,T.useEffect)(()=>{let d=x=>{let v=ee.current;v&&v.contains(x.target)&&x.stopPropagation()},g=["mousedown","click","pointerdown"];return g.forEach(x=>document.body.addEventListener(x,d)),()=>{g.forEach(x=>document.body.removeEventListener(x,d))}},[]);let[F,he]=(0,T.useState)(!1),[et,ft]=(0,T.useState)(!1),[Re,Ie]=(0,T.useState)(null),[Ee,Pe]=(0,T.useState)({x:0,y:0}),[W,ge]=(0,T.useState)(null),[Ze,Bt]=(0,T.useState)(!1),[vn,hn]=(0,T.useState)("idle"),[oo,In]=(0,T.useState)(!1),[ao,il]=(0,T.useState)(!1),[Rl,io]=(0,T.useState)(null),[Uo,zn]=(0,T.useState)(null),[sl,wn]=(0,T.useState)([]),[yl,pl]=(0,T.useState)(null),[ba,rl]=(0,T.useState)(null),[Be,I]=(0,T.useState)(null),[de,pe]=(0,T.useState)(null),[Ae,be]=(0,T.useState)([]),[tt,it]=(0,T.useState)(0),[Ke,Ue]=(0,T.useState)(!1),[me,M]=(0,T.useState)(!1),[N,$]=(0,T.useState)(!1),[U,J]=(0,T.useState)(!1),[ae,X]=(0,T.useState)(!1),[ie,Ce]=(0,T.useState)("main"),[qe,nt]=(0,T.useState)(!1),[se,st]=(0,T.useState)(!1),[Oe,Te]=(0,T.useState)(!1),[re,rt]=(0,T.useState)([]),[Ge,De]=(0,T.useState)(null),Fe=(0,T.useRef)(!1),[xe,vt]=(0,T.useState)(!1),[tn,qn]=(0,T.useState)(!1),[bl,kn]=(0,T.useState)(1),[Bl,Vs]=(0,T.useState)("new-page"),[Ut,Ol]=(0,T.useState)(""),[Zs,Hy]=(0,T.useState)(!1),[Se,Qn]=(0,T.useState)(null),Pc=(0,T.useRef)(!1),eu=(0,T.useRef)({rearrange:null,placements:[]}),Yo=(0,T.useRef)({rearrange:null,placements:[]}),[Uy,Mf]=(0,T.useState)(0),[Yy,jy]=(0,T.useState)(0),[Xy,tu]=(0,T.useState)(0),[Iy,Ef]=(0,T.useState)(0),Ei=(0,T.useRef)(new Set),Ks=(0,T.useRef)(new Set),cl=(0,T.useRef)(null),Fs=(0,T.useRef)(),Tf=se&&z&&!Oe&&xe;(0,T.useEffect)(()=>{if(Tf){qn(!1);let d=wi(()=>{qn(!0)});return()=>cancelAnimationFrame(d)}else qn(!1)},[Tf]);let Ti=(0,T.useRef)(new Map),Di=(0,T.useRef)(new Map),Ni=(0,T.useRef)(),[ul,nu]=(0,T.useState)(!1),[Wn,qy]=(0,T.useState)([]),Qy=(0,T.useRef)(Wn);Qy.current=Wn;let[Df,M4]=(0,T.useState)(null),lu=(0,T.useRef)(null),E4=(0,T.useRef)(!1),T4=(0,T.useRef)([]),D4=(0,T.useRef)(0),N4=(0,T.useRef)(null),z4=(0,T.useRef)(null),A4=(0,T.useRef)(1),[Nf,zf]=(0,T.useState)(!1),xa=(0,T.useRef)(null),[Qt,va]=(0,T.useState)([]),xl=(0,T.useRef)({cmd:!1,shift:!1}),_n=()=>{nt(!0)},Wy=()=>{nt(!1)},Gy=()=>{Nf||(xa.current=fe(()=>zf(!0),850))},Vy=()=>{xa.current&&(clearTimeout(xa.current),xa.current=null),zf(!1),Wy()};(0,T.useEffect)(()=>()=>{xa.current&&clearTimeout(xa.current)},[]);let[$e,Zy]=(0,T.useState)(()=>{try{let d=JSON.parse(localStorage.getItem("feedback-toolbar-settings")??"");return{...df,...d,annotationColorId:Qs.find(g=>g.id===d.annotationColorId)?d.annotationColorId:df.annotationColorId}}catch{return df}}),[vl,Af]=(0,T.useState)(!0),[Lf,Rf]=(0,T.useState)(!1),Ky=()=>{ee.current?.classList.add(Y.disableTransitions),Af(d=>!d),wi(()=>{ee.current?.classList.remove(Y.disableTransitions)})},Bf=!1,jo=Bf&&$e.reactEnabled?k4[$e.outputDetail]:"off",[Ft,ou]=(0,T.useState)(b??null),Of=(0,T.useRef)(!1),[dl,Xo]=(0,T.useState)(f?"connecting":"disconnected"),[zt,au]=(0,T.useState)(null),[Io,$f]=(0,T.useState)(!1),[wa,Hf]=(0,T.useState)(null),iu=(0,T.useRef)(!1),[Uf,zi]=(0,T.useState)(new Set),[Yf,Js]=(0,T.useState)(new Set),[Ai,Ps]=(0,T.useState)(!1),[Fy,ka]=(0,T.useState)(!1),[$l,jf]=(0,T.useState)(!1),Sa=(0,T.useRef)(null),wl=(0,T.useRef)(null),Li=(0,T.useRef)(null),Ri=(0,T.useRef)(null),er=(0,T.useRef)(!1),Xf=(0,T.useRef)(0),tr=(0,T.useRef)(null),If=(0,T.useRef)(null),su=8,Jy=50,qf=(0,T.useRef)(null),Qf=(0,T.useRef)(null),Bi=(0,T.useRef)(null),ye=typeof window<"u"?window.location.pathname:"/";(0,T.useEffect)(()=>{if(U)X(!0);else{nt(!1),Ce("main");let d=fe(()=>X(!1),0);return()=>clearTimeout(d)}},[U]);let ru=z&&k&&!se;(0,T.useEffect)(()=>{if(ru){ft(!1),he(!0),zi(new Set);let d=fe(()=>{zi(g=>{let x=new Set(g);return h.forEach(v=>x.add(v.id)),x})},350);return()=>clearTimeout(d)}else if(F){ft(!0);let d=fe(()=>{he(!1),ft(!1)},250);return()=>clearTimeout(d)}},[ru]),(0,T.useEffect)(()=>{M(!0),it(window.scrollY);let d=lf(ye);y(d.filter(ma)),my||(Rf(!0),my=!0,fe(()=>Rf(!1),750));try{let g=localStorage.getItem("feedback-toolbar-theme");g!==null&&Af(g==="dark")}catch{}try{let g=localStorage.getItem("feedback-toolbar-position");if(g){let x=JSON.parse(g);typeof x.x=="number"&&typeof x.y=="number"&&au(x)}}catch{}},[ye]),(0,T.useEffect)(()=>{me&&localStorage.setItem("feedback-toolbar-settings",JSON.stringify($e))},[$e,me]),(0,T.useEffect)(()=>{me&&localStorage.setItem("feedback-toolbar-theme",vl?"dark":"light")},[vl,me]);let Wf=(0,T.useRef)(!1);(0,T.useEffect)(()=>{let d=Wf.current;Wf.current=Io,d&&!Io&&zt&&me&&localStorage.setItem("feedback-toolbar-position",JSON.stringify(zt))},[Io,zt,me]),(0,T.useEffect)(()=>{if(!f||!me||Of.current)return;Of.current=!0,Xo("connecting"),(async()=>{try{let g=Rv(ye),x=b||g,v=!1;if(x)try{let S=await iy(f,x);ou(S.id),Xo("connected"),of(ye,S.id),v=!0;let B=lf(ye),q=new Set(S.annotations.map(le=>le.id)),V=B.filter(le=>!q.has(le.id));if(V.length>0){let ce=`${typeof window<"u"?window.location.origin:""}${ye}`,Me=(await Promise.allSettled(V.map(_e=>xi(f,S.id,{..._e,sessionId:S.id,url:ce})))).map((_e,te)=>_e.status==="fulfilled"?_e.value:(console.warn("[Agentation] Failed to sync annotation:",_e.reason),V[te])),Ye=[...S.annotations,...Me];y(Ye.filter(ma)),js(ye,Ye.filter(ma),S.id)}else y(S.annotations.filter(ma)),js(ye,S.annotations.filter(ma),S.id)}catch(S){console.warn("[Agentation] Could not join session, creating new:",S),Bv(ye)}if(!v){let S=typeof window<"u"?window.location.href:"/",B=await af(f,S);ou(B.id),Xo("connected"),of(ye,B.id),_?.(B.id);let q=Mv(),V=typeof window<"u"?window.location.origin:"",le=[];for(let[ce,ue]of q){let Me=ue.filter(te=>!te._syncedTo);if(Me.length===0)continue;let Ye=`${V}${ce}`,_e=ce===ye;le.push((async()=>{try{let te=_e?B:await af(f,Ye),Jt=(await Promise.allSettled(Me.map(ct=>xi(f,te.id,{...ct,sessionId:te.id,url:Ye})))).map((ct,jt)=>ct.status==="fulfilled"?ct.value:(console.warn("[Agentation] Failed to sync annotation:",ct.reason),Me[jt])).filter(ma);if(js(ce,Jt,te.id),_e){let ct=new Set(Me.map(jt=>jt.id));y(jt=>{let ve=jt.filter(Ne=>!ct.has(Ne.id));return[...Jt,...ve]})}}catch(te){console.warn(`[Agentation] Failed to sync annotations for ${ce}:`,te)}})())}await Promise.allSettled(le)}}catch(g){Xo("disconnected"),console.warn("[Agentation] Failed to initialize session, using local storage:",g)}})()},[f,b,me,_,ye]),(0,T.useEffect)(()=>{if(!f||!me)return;let d=async()=>{try{(await fetch(`${f}/health`)).ok?Xo("connected"):Xo("disconnected")}catch{Xo("disconnected")}};d();let g=Db(d,1e4);return()=>clearInterval(g)},[f,me]),(0,T.useEffect)(()=>{if(!f||!me||!Ft)return;let d=new EventSource(`${f}/sessions/${Ft}/events`),g=["resolved","dismissed"],x=v=>{try{let S=JSON.parse(v.data);if(g.includes(S.payload?.status)){let B=S.payload.id,q=S.payload.kind;if(q==="placement"){for(let[V,le]of Ti.current)if(le===B){Ti.current.delete(V),rt(ce=>ce.filter(ue=>ue.id!==V));break}}else if(q==="rearrange"){for(let[V,le]of Di.current)if(le===B){Di.current.delete(V),Qn(ce=>{if(!ce)return null;let ue=ce.sections.filter(Me=>Me.id!==V);return ue.length===0?null:{...ce,sections:ue}});break}}else Js(V=>new Set(V).add(B)),fe(()=>{y(V=>V.filter(le=>le.id!==B)),Js(V=>{let le=new Set(V);return le.delete(B),le})},150)}}catch{}};return d.addEventListener("annotation.updated",x),()=>{d.removeEventListener("annotation.updated",x),d.close()}},[f,me,Ft]),(0,T.useEffect)(()=>{if(!f||!me)return;let d=If.current==="disconnected",g=dl==="connected";If.current=dl,d&&g&&(async()=>{try{let v=lf(ye);if(v.length===0)return;let B=`${typeof window<"u"?window.location.origin:""}${ye}`,q=Ft,V=[];if(q)try{V=(await iy(f,q)).annotations}catch{q=null}q||(q=(await af(f,B)).id,ou(q),of(ye,q));let le=new Set(V.map(ue=>ue.id)),ce=v.filter(ue=>!le.has(ue.id));if(ce.length>0){let Me=(await Promise.allSettled(ce.map(te=>xi(f,q,{...te,sessionId:q,url:B})))).map((te,Yt)=>te.status==="fulfilled"?te.value:(console.warn("[Agentation] Failed to sync annotation on reconnect:",te.reason),ce[Yt])),_e=[...V,...Me].filter(ma);y(_e),js(ye,_e,q)}}catch(v){console.warn("[Agentation] Failed to sync on reconnect:",v)}})()},[dl,f,me,Ft,ye]);let Py=(0,T.useCallback)(()=>{L||(K(!0),J(!1),D(!1),fe(()=>{$v(!0),oe(!0),K(!1)},400))},[L]);(0,T.useEffect)(()=>{if(!n||!me||!e||e.length===0||h.length>0)return;let d=[];return d.push(fe(()=>{D(!0)},t-200)),e.forEach((g,x)=>{let v=t+x*300;d.push(fe(()=>{let S=document.querySelector(g.selector);if(!S)return;let B=S.getBoundingClientRect(),{name:q,path:V}=ki(S),le={id:`demo-${Date.now()}-${x}`,x:(B.left+B.width/2)/window.innerWidth*100,y:B.top+B.height/2+window.scrollY,comment:g.comment,element:q,elementPath:V,timestamp:Date.now(),selectedText:g.selectedText,boundingBox:{x:B.left,y:B.top+window.scrollY,width:B.width,height:B.height},nearbyText:Us(S),cssClasses:Ys(S)};y(ce=>[...ce,le])},v))}),()=>{d.forEach(clearTimeout)}},[n,me,e,t]),(0,T.useEffect)(()=>{let d=()=>{it(window.scrollY),Ue(!0),Bi.current&&clearTimeout(Bi.current),Bi.current=fe(()=>{Ue(!1)},150)};return window.addEventListener("scroll",d,{passive:!0}),()=>{window.removeEventListener("scroll",d),Bi.current&&clearTimeout(Bi.current)}},[]),(0,T.useEffect)(()=>{me&&h.length>0?Ft?js(ye,h,Ft):zy(ye,h):me&&h.length===0&&localStorage.removeItem(Jc(ye))},[h,ye,me,Ft]),(0,T.useEffect)(()=>{if(me&&!Fe.current){Fe.current=!0;let d=Ev(ye);d.length>0&&rt(d)}},[me,ye]),(0,T.useEffect)(()=>{me&&Fe.current&&!xe&&(re.length>0?Tv(ye,re):Dv(ye))},[re,ye,me,xe]),(0,T.useEffect)(()=>{if(me&&!Pc.current){Pc.current=!0;let d=Nv(ye);if(d){let g={...d,sections:d.sections.map(x=>({...x,currentRect:x.currentRect??{...x.originalRect}}))};Qn(g)}}},[me,ye]),(0,T.useEffect)(()=>{me&&Pc.current&&!xe&&(Se?zv(ye,Se):Av(ye))},[Se,ye,me,xe]);let cu=(0,T.useRef)(!1);(0,T.useEffect)(()=>{if(me&&!cu.current){cu.current=!0;let d=Lv(ye);d&&(Yo.current={rearrange:d.rearrange,placements:d.placements||[]},d.purpose&&Ol(d.purpose))}},[me,ye]),(0,T.useEffect)(()=>{if(!me||!cu.current)return;let d=Yo.current;xe?(Se?.sections?.length??0)>0||re.length>0||Ut?ay(ye,{rearrange:Se,placements:re,purpose:Ut}):Wc(ye):(d.rearrange?.sections?.length??0)>0||d.placements.length>0||Ut?ay(ye,{rearrange:d.rearrange,placements:d.placements,purpose:Ut}):Wc(ye)},[Se,re,Ut,xe,ye,me]),(0,T.useEffect)(()=>{se&&!Se&&Qn({sections:[],originalOrder:[],detectedAt:Date.now()})},[se,Se]),(0,T.useEffect)(()=>{if(!f||!Ft)return;let d=Ti.current,g=new Set(re.map(x=>x.id));for(let x of re){if(d.has(x.id))continue;d.set(x.id,"");let v=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye;xi(f,Ft,{id:x.id,x:x.x/window.innerWidth*100,y:x.y,comment:`Place ${x.type} at (${Math.round(x.x)}, ${Math.round(x.y)}), ${x.width}\xD7${x.height}px${x.text?` \u2014 "${x.text}"`:""}`,element:`[design:${x.type}]`,elementPath:"[placement]",timestamp:x.timestamp,url:v,intent:"change",severity:"important",kind:"placement",placement:{componentType:x.type,width:x.width,height:x.height,scrollY:x.scrollY,text:x.text}}).then(S=>{d.has(x.id)&&d.set(x.id,S.id)}).catch(S=>{console.warn("[Agentation] Failed to sync placement annotation:",S),d.delete(x.id)})}for(let[x,v]of d)g.has(x)||(d.delete(x),v&&Ho(f,v).catch(()=>{}))},[re,f,Ft,ye]),(0,T.useEffect)(()=>{if(!(!f||!Ft))return Ni.current&&clearTimeout(Ni.current),Ni.current=fe(()=>{let d=Di.current;if(!Se||Se.sections.length===0){for(let[,v]of d)v&&Ho(f,v).catch(()=>{});d.clear();return}let g=new Set(Se.sections.map(v=>v.id)),x=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye;for(let v of Se.sections){let S=v.originalRect,B=v.currentRect;if(!(Math.abs(S.x-B.x)>1||Math.abs(S.y-B.y)>1||Math.abs(S.width-B.width)>1||Math.abs(S.height-B.height)>1)){let le=d.get(v.id);le&&(d.delete(v.id),Ho(f,le).catch(()=>{}));continue}let V=d.get(v.id);V?sy(f,V,{comment:`Move ${v.label} section (${v.tagName}) \u2014 from (${Math.round(S.x)},${Math.round(S.y)}) ${Math.round(S.width)}\xD7${Math.round(S.height)} to (${Math.round(B.x)},${Math.round(B.y)}) ${Math.round(B.width)}\xD7${Math.round(B.height)}`}).catch(le=>{console.warn("[Agentation] Failed to update rearrange annotation:",le)}):(d.set(v.id,""),xi(f,Ft,{id:v.id,x:B.x/window.innerWidth*100,y:B.y,comment:`Move ${v.label} section (${v.tagName}) \u2014 from (${Math.round(S.x)},${Math.round(S.y)}) ${Math.round(S.width)}\xD7${Math.round(S.height)} to (${Math.round(B.x)},${Math.round(B.y)}) ${Math.round(B.width)}\xD7${Math.round(B.height)}`,element:v.selector,elementPath:"[rearrange]",timestamp:Date.now(),url:x,intent:"change",severity:"important",kind:"rearrange",rearrange:{selector:v.selector,label:v.label,tagName:v.tagName,originalRect:S,currentRect:B}}).then(le=>{d.has(v.id)&&d.set(v.id,le.id)}).catch(le=>{console.warn("[Agentation] Failed to sync rearrange annotation:",le),d.delete(v.id)}))}for(let[v,S]of d)g.has(v)||(d.delete(v),S&&Ho(f,S).catch(()=>{}))},300),()=>{Ni.current&&clearTimeout(Ni.current)}},[Se,f,Ft,ye]);let Ca=(0,T.useRef)(new Map);(0,T.useLayoutEffect)(()=>{let d=Se?.sections??[],g=new Set;if((se||Oe)&&z)for(let x of d){g.add(x.id);try{let v=document.querySelector(x.selector);if(!v)continue;if(!Ca.current.has(x.id)){let S={transform:v.style.transform,transformOrigin:v.style.transformOrigin,opacity:v.style.opacity,position:v.style.position,zIndex:v.style.zIndex,display:v.style.display},B=[],q=v.parentElement;for(;q&&q!==document.body;){let le=getComputedStyle(q);(le.overflow!=="visible"||le.overflowX!=="visible"||le.overflowY!=="visible")&&(B.push({el:q,overflow:q.style.overflow}),q.style.overflow="visible"),q=q.parentElement}getComputedStyle(v).display==="inline"&&(v.style.display="inline-block"),Ca.current.set(x.id,{el:v,origStyles:S,ancestors:B}),v.style.transformOrigin="top left",v.style.zIndex="9999"}}catch{}}for(let[x,v]of Ca.current)if(!g.has(x)){let{el:S,origStyles:B,ancestors:q}=v;S.style.transition="transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1)",S.style.transform=B.transform,S.style.transformOrigin=B.transformOrigin,S.style.opacity=B.opacity,S.style.position=B.position,S.style.zIndex=B.zIndex,Ca.current.delete(x),fe(()=>{S.style.transition="",S.style.display=B.display;for(let V of q)V.el.style.overflow=V.overflow},450)}},[Se,se,Oe,z]),(0,T.useEffect)(()=>()=>{for(let[,d]of Ca.current){let{el:g,origStyles:x,ancestors:v}=d;g.style.transition="transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.4s cubic-bezier(0.22, 1, 0.36, 1)",g.style.transform=x.transform,g.style.transformOrigin=x.transformOrigin,g.style.opacity=x.opacity,g.style.position=x.position,g.style.zIndex=x.zIndex,fe(()=>{g.style.transition="",g.style.display=x.display;for(let S of v)S.el.style.overflow=S.overflow},450)}Ca.current.clear()},[]);let nr=(0,T.useCallback)(()=>{Te(!0),st(!1),De(null),clearTimeout(Fs.current),Fs.current=fe(()=>{Te(!1)},300)},[]),Gf=(0,T.useCallback)(()=>{se&&(Te(!0),st(!1),De(null),clearTimeout(Fs.current),Fs.current=fe(()=>{Te(!1)},300)),D(!1)},[se]),Vf=(0,T.useCallback)(()=>{N||(zb(),$(!0))},[N]),lr=(0,T.useCallback)(()=>{N&&(Qg(),$(!1))},[N]),uu=(0,T.useCallback)(()=>{N?lr():Vf()},[N,Vf,lr]),Zf=(0,T.useCallback)(()=>{if(Qt.length===0)return;let d=Qt[0],g=d.element,x=Qt.length>1,v=Qt.map(S=>S.element.getBoundingClientRect());if(x){let S={left:Math.min(...v.map(te=>te.left)),top:Math.min(...v.map(te=>te.top)),right:Math.max(...v.map(te=>te.right)),bottom:Math.max(...v.map(te=>te.bottom))},B=Qt.slice(0,5).map(te=>te.name).join(", "),q=Qt.length>5?` +${Qt.length-5} more`:"",V=v.map(te=>({x:te.left,y:te.top+window.scrollY,width:te.width,height:te.height})),ce=Qt[Qt.length-1].element,ue=v[v.length-1],Me=ue.left+ue.width/2,Ye=ue.top+ue.height/2,_e=_f(ce);ge({x:Me/window.innerWidth*100,y:_e?Ye:Ye+window.scrollY,clientY:Ye,element:`${Qt.length} elements: ${B}${q}`,elementPath:"multi-select",boundingBox:{x:S.left,y:S.top+window.scrollY,width:S.right-S.left,height:S.bottom-S.top},isMultiSelect:!0,isFixed:_e,elementBoundingBoxes:V,multiSelectElements:Qt.map(te=>te.element),targetElement:ce,fullPath:Ic(g),accessibility:Xc(g),computedStyles:jc(g),computedStylesObj:Yc(g),nearbyElements:Uc(g),cssClasses:Ys(g),nearbyText:Us(g),sourceFile:Zc(g)})}else{let S=v[0],B=_f(g);ge({x:S.left/window.innerWidth*100,y:B?S.top:S.top+window.scrollY,clientY:S.top,element:d.name,elementPath:d.path,boundingBox:{x:S.left,y:B?S.top:S.top+window.scrollY,width:S.width,height:S.height},isFixed:B,fullPath:Ic(g),accessibility:Xc(g),computedStyles:jc(g),computedStylesObj:Yc(g),nearbyElements:Uc(g),cssClasses:Ys(g),nearbyText:Us(g),reactComponents:d.reactComponents,sourceFile:Zc(g)})}va([]),Ie(null)},[Qt]);(0,T.useEffect)(()=>{z||(ge(null),I(null),pe(null),be([]),Ie(null),J(!1),va([]),xl.current={cmd:!1,shift:!1},N&&lr())},[z,N,lr]),(0,T.useEffect)(()=>()=>{Qg()},[]),(0,T.useEffect)(()=>{if(!z)return;let d=["p","span","h1","h2","h3","h4","h5","h6","li","td","th","label","blockquote","figcaption","caption","legend","dt","dd","pre","code","em","strong","b","i","u","s","a","time","address","cite","q","abbr","dfn","mark","small","sub","sup","[contenteditable]"].join(", "),g=":not([data-agentation-root]):not([data-agentation-root] *)",x=document.createElement("style");return x.id="feedback-cursor-styles",x.textContent=`
      body ${g} {
        cursor: crosshair !important;
      }

      body :is(${d})${g} {
        cursor: text !important;
      }
    `,document.head.appendChild(x),()=>{let v=document.getElementById("feedback-cursor-styles");v&&v.remove()}},[z]),(0,T.useEffect)(()=>{if(Df!==null&&z)return document.documentElement.setAttribute("data-drawing-hover",""),()=>document.documentElement.removeAttribute("data-drawing-hover")},[Df,z]),(0,T.useEffect)(()=>{if(!z||W||ul||se)return;let d=g=>{let x=g.composedPath()[0]||g.target;if(bn(x,"[data-feedback-toolbar]")){Ie(null);return}let v=ha(g.clientX,g.clientY);if(!v||bn(v,"[data-feedback-toolbar]")){Ie(null);return}let{name:S,elementName:B,path:q,reactComponents:V}=uf(v,jo),le=v.getBoundingClientRect();Ie({element:S,elementName:B,elementPath:q,rect:le,reactComponents:V}),Pe({x:g.clientX,y:g.clientY})};return document.addEventListener("mousemove",d),()=>document.removeEventListener("mousemove",d)},[z,W,ul,se,jo,Wn]);let or=(0,T.useCallback)(d=>{if(I(d),io(null),zn(null),wn([]),d.elementBoundingBoxes?.length){let g=[];for(let x of d.elementBoundingBoxes){let v=x.x+x.width/2,S=x.y+x.height/2-window.scrollY,B=ha(v,S);B&&g.push(B)}be(g),pe(null)}else if(d.boundingBox){let g=d.boundingBox,x=g.x+g.width/2,v=d.isFixed?g.y+g.height/2:g.y+g.height/2-window.scrollY,S=ha(x,v);if(S){let B=S.getBoundingClientRect(),q=B.width/g.width,V=B.height/g.height;q<.5||V<.5?pe(null):pe(S)}else pe(null);be([])}else pe(null),be([])},[]);(0,T.useEffect)(()=>{if(!z||ul||se)return;let d=g=>{if(er.current){er.current=!1;return}let x=g.composedPath()[0]||g.target;if(bn(x,"[data-feedback-toolbar]")||bn(x,"[data-annotation-popup]")||bn(x,"[data-annotation-marker]"))return;if(g.metaKey&&g.shiftKey&&!W&&!Be){g.preventDefault(),g.stopPropagation();let ht=ha(g.clientX,g.clientY);if(!ht)return;let Jt=ht.getBoundingClientRect(),{name:ct,path:jt,reactComponents:ve}=uf(ht,jo),Ne=Qt.findIndex(At=>At.element===ht);Ne>=0?va(At=>At.filter((Ot,_l)=>_l!==Ne)):va(At=>[...At,{element:ht,rect:Jt,name:ct,path:jt,reactComponents:ve??void 0}]);return}let v=bn(x,"button, a, input, select, textarea, [role='button'], [onclick]");if($e.blockInteractions&&v&&(g.preventDefault(),g.stopPropagation()),W){if(v&&!$e.blockInteractions)return;g.preventDefault(),qf.current?.shake();return}if(Be){if(v&&!$e.blockInteractions)return;g.preventDefault(),Qf.current?.shake();return}g.preventDefault();let S=ha(g.clientX,g.clientY);if(!S)return;let{name:B,path:q,reactComponents:V}=uf(S,jo),le=S.getBoundingClientRect(),ce=g.clientX/window.innerWidth*100,ue=_f(S),Me=ue?g.clientY:g.clientY+window.scrollY,Ye=window.getSelection(),_e;Ye&&Ye.toString().trim().length>0&&(_e=Ye.toString().trim().slice(0,500));let te=Yc(S),Yt=jc(S);ge({x:ce,y:Me,clientY:g.clientY,element:B,elementPath:q,selectedText:_e,boundingBox:{x:le.left,y:ue?le.top:le.top+window.scrollY,width:le.width,height:le.height},nearbyText:Us(S),cssClasses:Ys(S),isFixed:ue,fullPath:Ic(S),accessibility:Xc(S),computedStyles:Yt,computedStylesObj:te,nearbyElements:Uc(S),reactComponents:V??void 0,sourceFile:Zc(S),targetElement:S}),Ie(null)};return document.addEventListener("click",d,!0),()=>document.removeEventListener("click",d,!0)},[z,ul,se,W,Be,$e.blockInteractions,jo,Qt]),(0,T.useEffect)(()=>{if(!z)return;let d=v=>{v.key==="Meta"&&(xl.current.cmd=!0),v.key==="Shift"&&(xl.current.shift=!0)},g=v=>{let S=xl.current.cmd&&xl.current.shift;v.key==="Meta"&&(xl.current.cmd=!1),v.key==="Shift"&&(xl.current.shift=!1);let B=xl.current.cmd&&xl.current.shift;S&&!B&&Qt.length>0&&Zf()},x=()=>{xl.current={cmd:!1,shift:!1},va([])};return document.addEventListener("keydown",d),document.addEventListener("keyup",g),window.addEventListener("blur",x),()=>{document.removeEventListener("keydown",d),document.removeEventListener("keyup",g),window.removeEventListener("blur",x)}},[z,Qt,Zf]),(0,T.useEffect)(()=>{if(!z||W||ul||se)return;let d=g=>{let x=g.composedPath()[0]||g.target;bn(x,"[data-feedback-toolbar]")||bn(x,"[data-annotation-marker]")||bn(x,"[data-annotation-popup]")||new Set(["P","SPAN","H1","H2","H3","H4","H5","H6","LI","TD","TH","LABEL","BLOCKQUOTE","FIGCAPTION","CAPTION","LEGEND","DT","DD","PRE","CODE","EM","STRONG","B","I","U","S","A","TIME","ADDRESS","CITE","Q","ABBR","DFN","MARK","SMALL","SUB","SUP"]).has(x.tagName)||x.isContentEditable||(g.preventDefault(),Sa.current={x:g.clientX,y:g.clientY})};return document.addEventListener("mousedown",d),()=>document.removeEventListener("mousedown",d)},[z,W,ul,se]),(0,T.useEffect)(()=>{if(!z||W)return;let d=g=>{if(!Sa.current)return;let x=g.clientX-Sa.current.x,v=g.clientY-Sa.current.y,S=x*x+v*v,B=su*su;if(!$l&&S>=B&&(wl.current=Sa.current,jf(!0),g.preventDefault()),($l||S>=B)&&wl.current){if(Li.current){let ve=Math.min(wl.current.x,g.clientX),Ne=Math.min(wl.current.y,g.clientY),At=Math.abs(g.clientX-wl.current.x),Ot=Math.abs(g.clientY-wl.current.y);Li.current.style.transform=`translate(${ve}px, ${Ne}px)`,Li.current.style.width=`${At}px`,Li.current.style.height=`${Ot}px`}let q=Date.now();if(q-Xf.current<Jy)return;Xf.current=q;let V=wl.current.x,le=wl.current.y,ce=Math.min(V,g.clientX),ue=Math.min(le,g.clientY),Me=Math.max(V,g.clientX),Ye=Math.max(le,g.clientY),_e=(ce+Me)/2,te=(ue+Ye)/2,Yt=new Set,ht=[[ce,ue],[Me,ue],[ce,Ye],[Me,Ye],[_e,te],[_e,ue],[_e,Ye],[ce,te],[Me,te]];for(let[ve,Ne]of ht){let At=document.elementsFromPoint(ve,Ne);for(let Ot of At)Ot instanceof HTMLElement&&Yt.add(Ot)}let Jt=document.querySelectorAll("button, a, input, img, p, h1, h2, h3, h4, h5, h6, li, label, td, th, div, span, section, article, aside, nav");for(let ve of Jt)if(ve instanceof HTMLElement){let Ne=ve.getBoundingClientRect(),At=Ne.left+Ne.width/2,Ot=Ne.top+Ne.height/2,_l=At>=ce&&At<=Me&&Ot>=ue&&Ot<=Ye,Gn=Math.min(Ne.right,Me)-Math.max(Ne.left,ce),an=Math.min(Ne.bottom,Ye)-Math.max(Ne.top,ue),$i=Gn>0&&an>0?Gn*an:0,Qo=Ne.width*Ne.height,so=Qo>0?$i/Qo:0;(_l||so>.5)&&Yt.add(ve)}let ct=[],jt=new Set(["BUTTON","A","INPUT","IMG","P","H1","H2","H3","H4","H5","H6","LI","LABEL","TD","TH","SECTION","ARTICLE","ASIDE","NAV"]);for(let ve of Yt){if(bn(ve,"[data-feedback-toolbar]")||bn(ve,"[data-annotation-marker]"))continue;let Ne=ve.getBoundingClientRect();if(!(Ne.width>window.innerWidth*.8&&Ne.height>window.innerHeight*.5)&&!(Ne.width<10||Ne.height<10)&&Ne.left<Me&&Ne.right>ce&&Ne.top<Ye&&Ne.bottom>ue){let At=ve.tagName,Ot=jt.has(At);if(!Ot&&(At==="DIV"||At==="SPAN")){let _l=ve.textContent&&ve.textContent.trim().length>0,Gn=ve.onclick!==null||ve.getAttribute("role")==="button"||ve.getAttribute("role")==="link"||ve.classList.contains("clickable")||ve.hasAttribute("data-clickable");(_l||Gn)&&!ve.querySelector("p, h1, h2, h3, h4, h5, h6, button, a")&&(Ot=!0)}if(Ot){let _l=!1;for(let Gn of ct)if(Gn.left<=Ne.left&&Gn.right>=Ne.right&&Gn.top<=Ne.top&&Gn.bottom>=Ne.bottom){_l=!0;break}_l||ct.push(Ne)}}}if(Ri.current){let ve=Ri.current;for(;ve.children.length>ct.length;)ve.removeChild(ve.lastChild);ct.forEach((Ne,At)=>{let Ot=ve.children[At];Ot||(Ot=document.createElement("div"),Ot.className=Y.selectedElementHighlight,ve.appendChild(Ot)),Ot.style.transform=`translate(${Ne.left}px, ${Ne.top}px)`,Ot.style.width=`${Ne.width}px`,Ot.style.height=`${Ne.height}px`})}}};return document.addEventListener("mousemove",d,{passive:!0}),()=>document.removeEventListener("mousemove",d)},[z,W,$l,su]),(0,T.useEffect)(()=>{if(!z)return;let d=g=>{let x=$l,v=wl.current;if($l&&v){er.current=!0;let S=Math.min(v.x,g.clientX),B=Math.min(v.y,g.clientY),q=Math.max(v.x,g.clientX),V=Math.max(v.y,g.clientY),le=[];document.querySelectorAll("button, a, input, img, p, h1, h2, h3, h4, h5, h6, li, label, td, th").forEach(_e=>{if(!(_e instanceof HTMLElement)||bn(_e,"[data-feedback-toolbar]")||bn(_e,"[data-annotation-marker]"))return;let te=_e.getBoundingClientRect();te.width>window.innerWidth*.8&&te.height>window.innerHeight*.5||te.width<10||te.height<10||te.left<q&&te.right>S&&te.top<V&&te.bottom>B&&le.push({element:_e,rect:te})});let ue=le.filter(({element:_e})=>!le.some(({element:te})=>te!==_e&&_e.contains(te))),Me=g.clientX/window.innerWidth*100,Ye=g.clientY+window.scrollY;if(ue.length>0){let _e=ue.reduce((jt,{rect:ve})=>({left:Math.min(jt.left,ve.left),top:Math.min(jt.top,ve.top),right:Math.max(jt.right,ve.right),bottom:Math.max(jt.bottom,ve.bottom)}),{left:1/0,top:1/0,right:-1/0,bottom:-1/0}),te=ue.slice(0,5).map(({element:jt})=>ki(jt).name).join(", "),Yt=ue.length>5?` +${ue.length-5} more`:"",ht=ue[0].element,Jt=Yc(ht),ct=jc(ht);ge({x:Me,y:Ye,clientY:g.clientY,element:`${ue.length} elements: ${te}${Yt}`,elementPath:"multi-select",boundingBox:{x:_e.left,y:_e.top+window.scrollY,width:_e.right-_e.left,height:_e.bottom-_e.top},isMultiSelect:!0,fullPath:Ic(ht),accessibility:Xc(ht),computedStyles:ct,computedStylesObj:Jt,nearbyElements:Uc(ht),cssClasses:Ys(ht),nearbyText:Us(ht),sourceFile:Zc(ht)})}else{let _e=Math.abs(q-S),te=Math.abs(V-B);_e>20&&te>20&&ge({x:Me,y:Ye,clientY:g.clientY,element:"Area selection",elementPath:`region at (${Math.round(S)}, ${Math.round(B)})`,boundingBox:{x:S,y:B+window.scrollY,width:_e,height:te},isMultiSelect:!0})}Ie(null)}else x&&(er.current=!0);Sa.current=null,wl.current=null,jf(!1),Ri.current&&(Ri.current.innerHTML="")};return document.addEventListener("mouseup",d),()=>document.removeEventListener("mouseup",d)},[z,$l]);let kl=(0,T.useCallback)(async(d,g,x)=>{let v=$e.webhookUrl||w;if(!v||!$e.webhooksEnabled&&!x)return!1;try{return(await fetch(v,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:d,timestamp:Date.now(),url:typeof window<"u"?window.location.href:void 0,...g})})).ok}catch(S){return console.warn("[Agentation] Webhook failed:",S),!1}},[w,$e.webhookUrl,$e.webhooksEnabled]),ep=(0,T.useCallback)(d=>{if(!W)return;let g={id:Date.now().toString(),x:W.x,y:W.y,comment:d,element:W.element,elementPath:W.elementPath,timestamp:Date.now(),selectedText:W.selectedText,boundingBox:W.boundingBox,nearbyText:W.nearbyText,cssClasses:W.cssClasses,isMultiSelect:W.isMultiSelect,isFixed:W.isFixed,fullPath:W.fullPath,accessibility:W.accessibility,computedStyles:W.computedStyles,nearbyElements:W.nearbyElements,reactComponents:W.reactComponents,sourceFile:W.sourceFile,elementBoundingBoxes:W.elementBoundingBoxes,...f&&Ft?{sessionId:Ft,url:typeof window<"u"?window.location.href:void 0,status:"pending"}:{}};y(x=>[...x,g]),tr.current=g.id,fe(()=>{tr.current=null},300),fe(()=>{zi(x=>new Set(x).add(g.id))},250),l?.(g),kl("annotation.add",{annotation:g}),Ps(!0),fe(()=>{ge(null),Ps(!1)},150),window.getSelection()?.removeAllRanges(),f&&Ft&&xi(f,Ft,g).then(x=>{x.id!==g.id&&(y(v=>v.map(S=>S.id===g.id?{...S,id:x.id}:S)),zi(v=>{let S=new Set(v);return S.delete(g.id),S.add(x.id),S}))}).catch(x=>{console.warn("[Agentation] Failed to sync annotation:",x)})},[W,l,kl,f,Ft]),du=(0,T.useCallback)(()=>{Ps(!0),fe(()=>{ge(null),Ps(!1)},150)},[]),_u=(0,T.useCallback)(d=>{let g=h.findIndex(v=>v.id===d),x=h[g];Be?.id===d&&(ka(!0),fe(()=>{I(null),pe(null),be([]),ka(!1)},150)),pl(d),Js(v=>new Set(v).add(d)),x&&(o?.(x),kl("annotation.delete",{annotation:x})),f&&Ho(f,d).catch(v=>{console.warn("[Agentation] Failed to delete annotation from server:",v)}),fe(()=>{y(v=>v.filter(S=>S.id!==d)),Js(v=>{let S=new Set(v);return S.delete(d),S}),pl(null),g<h.length-1&&(rl(g),fe(()=>rl(null),200))},150)},[h,Be,o,kl,f]),ar=(0,T.useCallback)(d=>{if(!d){io(null),zn(null),wn([]);return}if(io(d.id),d.elementBoundingBoxes?.length){let g=[];for(let x of d.elementBoundingBoxes){let v=x.x+x.width/2,S=x.y+x.height/2-window.scrollY,q=document.elementsFromPoint(v,S).find(V=>!V.closest("[data-annotation-marker]")&&!V.closest("[data-agentation-root]"));q&&g.push(q)}wn(g),zn(null)}else if(d.boundingBox){let g=d.boundingBox,x=g.x+g.width/2,v=d.isFixed?g.y+g.height/2:g.y+g.height/2-window.scrollY,S=ha(x,v);if(S){let B=S.getBoundingClientRect(),q=B.width/g.width,V=B.height/g.height;q<.5||V<.5?zn(null):zn(S)}else zn(null);wn([])}else zn(null),wn([])},[]),tp=(0,T.useCallback)(d=>{if(!Be)return;let g={...Be,comment:d};y(x=>x.map(v=>v.id===Be.id?g:v)),a?.(g),kl("annotation.update",{annotation:g}),f&&sy(f,Be.id,{comment:d}).catch(x=>{console.warn("[Agentation] Failed to update annotation on server:",x)}),ka(!0),fe(()=>{I(null),pe(null),be([]),ka(!1)},150)},[Be,a,kl,f]),np=(0,T.useCallback)(()=>{ka(!0),fe(()=>{I(null),pe(null),be([]),ka(!1)},150)},[]),qo=(0,T.useCallback)(()=>{let d=h.length,g=re.length>0||!!Se;if(d===0&&Wn.length===0&&!g)return;if(i?.(h),kl("annotations.clear",{annotations:h}),f){Promise.all(h.map(S=>Ho(f,S.id).catch(B=>{console.warn("[Agentation] Failed to delete annotation from server:",B)})));for(let[,S]of Ti.current)S&&Ho(f,S).catch(()=>{});Ti.current.clear();for(let[,S]of Di.current)S&&Ho(f,S).catch(()=>{});Di.current.clear()}il(!0),In(!0),qy([]);let x=lu.current;if(x){let S=x.getContext("2d");S&&S.clearRect(0,0,x.width,x.height)}(re.length>0||Se)&&(tu(S=>S+1),Ef(S=>S+1),fe(()=>{rt([]),Qn(null)},200)),xe&&vt(!1),Ut&&Ol(""),Yo.current={rearrange:null,placements:[]},Wc(ye);let v=d*30+200;fe(()=>{y([]),zi(new Set),localStorage.removeItem(Jc(ye)),il(!1)},v),fe(()=>In(!1),1500)},[ye,h,Wn,re,Se,xe,Ut,i,kl,f]),fu=(0,T.useCallback)(async()=>{let d=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye,g=se&&xe,x;if(g){if(re.length===0&&!Se&&!Ut)return;x=""}else{if(x=uy(h,d,$e.outputDetail),!x&&Wn.length===0&&re.length===0&&!Se)return;x||(x=`## Page Feedback: ${d}
`)}if(!g&&Wn.length>0){let v=new Set;for(let V of h)V.drawingIndex!=null&&v.add(V.drawingIndex);let S=lu.current;S&&(S.style.visibility="hidden");let B=[],q=window.scrollY;for(let V=0;V<Wn.length;V++){if(v.has(V))continue;let le=Wn[V];if(le.points.length<2)continue;let ce=le.fixed?le.points:le.points.map(Wt=>({x:Wt.x,y:Wt.y-q})),ue=1/0,Me=1/0,Ye=-1/0,_e=-1/0;for(let Wt of ce)ue=Math.min(ue,Wt.x),Me=Math.min(Me,Wt.y),Ye=Math.max(Ye,Wt.x),_e=Math.max(_e,Wt.y);let te=Ye-ue,Yt=_e-Me,ht=Math.hypot(te,Yt),Jt=ce[0],ct=ce[ce.length-1],jt=Math.hypot(ct.x-Jt.x,ct.y-Jt.y),ve,Ne=jt<ht*.35,At=te/Math.max(Yt,1);if(Ne&&ht>20){let Wt=Math.max(te,Yt)*.15,ro=0;for(let Wo of ce){let ap=Wo.x-ue<Wt,ip=Ye-Wo.x<Wt,sp=Wo.y-Me<Wt,rp=_e-Wo.y<Wt;(ap||ip)&&(sp||rp)&&ro++}ve=ro>ce.length*.15?"box":"circle"}else At>3&&Yt<40?ve="underline":jt>ht*.5?ve="arrow":ve="drawing";let Ot=Math.min(10,ce.length),_l=Math.max(1,Math.floor(ce.length/Ot)),Gn=new Set,an=[],$i=[Jt];for(let Wt=_l;Wt<ce.length-1;Wt+=_l)$i.push(ce[Wt]);$i.push(ct);for(let Wt of $i){let ro=ha(Wt.x,Wt.y);if(!ro||Gn.has(ro)||bn(ro,"[data-feedback-toolbar]"))continue;Gn.add(ro);let{name:Wo}=ki(ro);an.includes(Wo)||an.push(Wo)}let Qo=`${Math.round(ue)},${Math.round(Me)} \u2192 ${Math.round(Ye)},${Math.round(_e)}`,so;(ve==="circle"||ve==="box")&&an.length>0?so=`${ve==="box"?"Boxed":"Circled"} **${an[0]}**${an.length>1?` (and ${an.slice(1).join(", ")})`:""} (region: ${Qo})`:ve==="underline"&&an.length>0?so=`Underlined **${an[0]}** (${Qo})`:ve==="arrow"&&an.length>=2?so=`Arrow from **${an[0]}** to **${an[an.length-1]}** (${Math.round(Jt.x)},${Math.round(Jt.y)} \u2192 ${Math.round(ct.x)},${Math.round(ct.y)})`:an.length>0?so=`${ve==="arrow"?"Arrow":"Drawing"} near **${an.join("**, **")}** (region: ${Qo})`:so=`Drawing at ${Qo}`,B.push(so)}S&&(S.style.visibility=""),B.length>0&&(x+=`
**Drawings:**
`,B.forEach((V,le)=>{x+=`${le+1}. ${V}
`}))}if((re.length>0||g&&Ut)&&(x+=`
`+ly(re,{width:window.innerWidth,height:window.innerHeight},{blankCanvas:xe,wireframePurpose:Ut||void 0},$e.outputDetail)),Se){let v=oy(Se,$e.outputDetail,{width:window.innerWidth,height:window.innerHeight});v&&(x+=`
`+v)}if(p)try{await navigator.clipboard.writeText(x)}catch{}s?.(x),Bt(!0),fe(()=>Bt(!1),2e3),$e.autoClearAfterCopy&&fe(()=>qo(),500)},[h,Wn,re,Se,xe,se,Bl,Ut,ye,$e.outputDetail,jo,$e.autoClearAfterCopy,qo,p,s]),hu=(0,T.useCallback)(async()=>{let d=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye,g=uy(h,d,$e.outputDetail);if(!g&&re.length===0&&!Se)return;if(g||(g=`## Page Feedback: ${d}
`),re.length>0&&(g+=`
`+ly(re,{width:window.innerWidth,height:window.innerHeight},{blankCanvas:xe,wireframePurpose:Ut||void 0},$e.outputDetail)),Se){let v=oy(Se,$e.outputDetail,{width:window.innerWidth,height:window.innerHeight});v&&(g+=`
`+v)}r&&r(g,h),hn("sending"),await new Promise(v=>fe(v,150));let x=await kl("submit",{output:g,annotations:h},!0);hn(x?"sent":"failed"),fe(()=>hn("idle"),2500),x&&$e.autoClearAfterCopy&&fe(()=>qo(),500)},[r,kl,h,re,Se,xe,Bl,ye,$e.outputDetail,jo,$e.autoClearAfterCopy,qo]);(0,T.useEffect)(()=>{if(!wa)return;let d=10,g=v=>{let S=v.clientX-wa.x,B=v.clientY-wa.y,q=Math.sqrt(S*S+B*B);if(!Io&&q>d&&$f(!0),Io||q>d){let V=wa.toolbarX+S,le=wa.toolbarY+B,ce=20,ue=337,Me=44,_e=ue-(z?dl==="connected"?297:257:44),te=ce-_e,Yt=window.innerWidth-ce-ue;V=Math.max(te,Math.min(Yt,V)),le=Math.max(ce,Math.min(window.innerHeight-Me-ce,le)),au({x:V,y:le})}},x=()=>{Io&&(iu.current=!0),$f(!1),Hf(null)};return document.addEventListener("mousemove",g),document.addEventListener("mouseup",x),()=>{document.removeEventListener("mousemove",g),document.removeEventListener("mouseup",x)}},[wa,Io,z,dl]);let lp=(0,T.useCallback)(d=>{if(d.target.closest("button")||d.target.closest("[data-agentation-settings-panel]"))return;let g=d.currentTarget.parentElement;if(!g)return;let x=g.getBoundingClientRect(),v=zt?.x??x.left,S=zt?.y??x.top;Hf({x:d.clientX,y:d.clientY,toolbarX:v,toolbarY:S})},[zt]);if((0,T.useEffect)(()=>{if(!zt)return;let d=()=>{let S=zt.x,B=zt.y,le=20-(337-(z?dl==="connected"?297:257:44)),ce=window.innerWidth-20-337;S=Math.max(le,Math.min(ce,S)),B=Math.max(20,Math.min(window.innerHeight-44-20,B)),(S!==zt.x||B!==zt.y)&&au({x:S,y:B})};return d(),window.addEventListener("resize",d),()=>window.removeEventListener("resize",d)},[zt,z,dl]),(0,T.useEffect)(()=>{let d=g=>{let x=g.target,v=x.tagName==="INPUT"||x.tagName==="TEXTAREA"||x.isContentEditable;if(g.key==="Escape"){if(se){Ge?De(null):nr();return}if(ul){nu(!1);return}if(Qt.length>0){va([]);return}W||z&&(_n(),D(!1))}if((g.metaKey||g.ctrlKey)&&g.shiftKey&&(g.key==="f"||g.key==="F")){g.preventDefault(),_n(),z?Gf():D(!0);return}if(!(v||g.metaKey||g.ctrlKey)&&((g.key==="p"||g.key==="P")&&(g.preventDefault(),_n(),uu()),(g.key==="l"||g.key==="L")&&(g.preventDefault(),_n(),ul&&nu(!1),U&&J(!1),W&&du(),se?nr():st(!0)),(g.key==="h"||g.key==="H")&&h.length>0&&(g.preventDefault(),_n(),E(S=>!S)),(g.key==="c"||g.key==="C")&&(h.length>0||re.length>0||Se)&&(g.preventDefault(),_n(),fu()),(g.key==="x"||g.key==="X")&&(h.length>0||re.length>0||Se)&&(g.preventDefault(),_n(),qo(),re.length>0&&rt([]),Se&&Qn(null)),g.key==="s"||g.key==="S")){let S=Al($e.webhookUrl)||Al(w||"");h.length>0&&S&&vn==="idle"&&(g.preventDefault(),_n(),hu())}};return document.addEventListener("keydown",d),()=>document.removeEventListener("keydown",d)},[z,ul,se,Ge,re,Se,W,h.length,$e.webhookUrl,w,vn,hu,uu,fu,qo,Qt]),!me||Q)return null;let Oi=h.length>0,Ma=h.filter(d=>!Yf.has(d.id)&&d.kind!=="placement"&&d.kind!=="rearrange"),op=Ma.length>0,Kf=h.filter(d=>Yf.has(d.id)),Ff=d=>{let B=d.x/100*window.innerWidth,q=typeof d.y=="string"?parseFloat(d.y):d.y,V={};window.innerHeight-q-22-10<80&&(V.top="auto",V.bottom="calc(100% + 10px)");let ce=B-200/2,ue=10;if(ce<ue){let Me=ue-ce;V.left=`calc(50% + ${Me}px)`}else if(ce+200>window.innerWidth-ue){let Me=ce+200-(window.innerWidth-ue);V.left=`calc(50% - ${Me}px)`}return V};return(0,gy.createPortal)((0,j.jsxs)("div",{ref:ee,style:{display:"contents"},"data-agentation-theme":vl?"dark":"light","data-agentation-accent":$e.annotationColorId,"data-agentation-root":"",children:[(0,j.jsx)("div",{className:`${Y.toolbar}${C?` ${C}`:""}`,"data-feedback-toolbar":!0,"data-agentation-toolbar":!0,style:zt?{left:zt.x,top:zt.y,right:"auto",bottom:"auto"}:void 0,children:(0,j.jsxs)("div",{className:`${Y.toolbarContainer} ${z?Y.expanded:Y.collapsed} ${Lf?Y.entrance:""} ${L?Y.hiding:""} ${!$e.webhooksEnabled&&(Al($e.webhookUrl)||Al(w||""))?Y.serverConnected:""}`,onClick:z?void 0:d=>{if(iu.current){iu.current=!1,d.preventDefault();return}D(!0)},onMouseDown:lp,role:z?void 0:"button",tabIndex:z?-1:0,title:z?void 0:"Start feedback mode",children:[(0,j.jsxs)("div",{className:`${Y.toggleContent} ${z?Y.hidden:Y.visible}`,children:[(0,j.jsx)(fb,{size:24}),op&&(0,j.jsx)("span",{className:`${Y.badge} ${z?Y.fadeOut:""} ${Lf?Y.entrance:""}`,children:Ma.length})]}),(0,j.jsxs)("div",{className:`${Y.controlsContent} ${z?Y.visible:Y.hidden} ${zt&&zt.y<100?Y.tooltipBelow:""} ${qe||U?Y.tooltipsHidden:""} ${Nf?Y.tooltipsInSession:""}`,onMouseEnter:Gy,onMouseLeave:Vy,children:[(0,j.jsxs)("div",{className:`${Y.buttonWrapper} ${zt&&zt.x<120?Y.buttonWrapperAlignLeft:""}`,children:[(0,j.jsx)("button",{className:Y.controlButton,onClick:d=>{d.stopPropagation(),_n(),uu()},"data-active":N,children:(0,j.jsx)(pb,{size:24,isPaused:N})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:[N?"Resume animations":"Pause animations",(0,j.jsx)("span",{className:Y.shortcut,children:"P"})]})]}),(0,j.jsxs)("div",{className:Y.buttonWrapper,children:[(0,j.jsx)("button",{className:`${Y.controlButton} ${vl?"":Y.light}`,onClick:d=>{d.stopPropagation(),_n(),ul&&nu(!1),U&&J(!1),W&&du(),se?nr():st(!0)},"data-active":se,style:se&&xe?{color:"#f97316",background:"rgba(249, 115, 22, 0.25)"}:void 0,children:(0,j.jsx)(Eb,{size:21})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:[se?"Exit layout mode":"Layout mode",(0,j.jsx)("span",{className:Y.shortcut,children:"L"})]})]}),(0,j.jsxs)("div",{className:Y.buttonWrapper,children:[(0,j.jsx)("button",{className:Y.controlButton,onClick:d=>{d.stopPropagation(),_n(),E(!k)},disabled:!Oi||se,children:(0,j.jsx)(yb,{size:24,isOpen:k})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:[k?"Hide markers":"Show markers",(0,j.jsx)("span",{className:Y.shortcut,children:"H"})]})]}),(0,j.jsxs)("div",{className:Y.buttonWrapper,children:[(0,j.jsx)("button",{className:`${Y.controlButton} ${Ze?Y.statusShowing:""}`,onClick:d=>{d.stopPropagation(),_n(),fu()},disabled:se&&xe?re.length===0&&!Se?.sections?.length:!Oi&&Wn.length===0&&re.length===0&&!Se?.sections?.length,"data-active":Ze,children:(0,j.jsx)(mb,{size:24,copied:Ze,tint:se&&xe&&(re.length>0||Se?.sections?.length)?"#f97316":void 0})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:[se&&xe?"Copy layout":"Copy feedback",(0,j.jsx)("span",{className:Y.shortcut,children:"C"})]})]}),(0,j.jsxs)("div",{className:`${Y.buttonWrapper} ${Y.sendButtonWrapper} ${z&&!$e.webhooksEnabled&&(Al($e.webhookUrl)||Al(w||""))?Y.sendButtonVisible:""}`,children:[(0,j.jsxs)("button",{className:`${Y.controlButton} ${vn==="sent"||vn==="failed"?Y.statusShowing:""}`,onClick:d=>{d.stopPropagation(),_n(),hu()},disabled:!Oi||!Al($e.webhookUrl)&&!Al(w||"")||vn==="sending","data-no-hover":vn==="sent"||vn==="failed",tabIndex:Al($e.webhookUrl)||Al(w||"")?0:-1,children:[(0,j.jsx)(gb,{size:24,state:vn}),Oi&&vn==="idle"&&(0,j.jsx)("span",{className:Y.buttonBadge,children:h.length})]}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:["Send Annotations",(0,j.jsx)("span",{className:Y.shortcut,children:"S"})]})]}),(0,j.jsxs)("div",{className:Y.buttonWrapper,children:[(0,j.jsx)("button",{className:Y.controlButton,onClick:d=>{d.stopPropagation(),_n(),qo()},disabled:!Oi&&Wn.length===0&&re.length===0&&!Se?.sections?.length,"data-danger":!0,children:(0,j.jsx)(xb,{size:24})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:["Clear all",(0,j.jsx)("span",{className:Y.shortcut,children:"X"})]})]}),(0,j.jsxs)("div",{className:Y.buttonWrapper,children:[(0,j.jsx)("button",{className:Y.controlButton,onClick:d=>{d.stopPropagation(),_n(),se&&nr(),J(!U)},children:(0,j.jsx)(bb,{size:24})}),f&&dl!=="disconnected"&&(0,j.jsx)("span",{className:`${Y.mcpIndicator} ${Y[dl]} ${U?Y.hidden:""}`,title:dl==="connected"?"MCP Connected":"MCP Connecting..."}),(0,j.jsx)("span",{className:Y.buttonTooltip,children:"Settings"})]}),(0,j.jsx)("div",{className:Y.divider}),(0,j.jsxs)("div",{className:`${Y.buttonWrapper} ${zt&&typeof window<"u"&&zt.x>window.innerWidth-120?Y.buttonWrapperAlignRight:""}`,children:[(0,j.jsx)("button",{className:Y.controlButton,onClick:d=>{d.stopPropagation(),_n(),Gf()},children:(0,j.jsx)(vb,{size:24})}),(0,j.jsxs)("span",{className:Y.buttonTooltip,children:["Exit",(0,j.jsx)("span",{className:Y.shortcut,children:"Esc"})]})]})]}),(0,j.jsx)(nv,{visible:se&&z,activeType:Ge,onSelect:d=>{De(Ge===d?null:d)},isDarkMode:vl,sectionCount:Se?.sections.length??0,onDetectSections:()=>{let d=fv(),g=Se?.sections??[],x=new Set(g.map(q=>q.selector)),v=d.filter(q=>!x.has(q.selector)),S=[...g,...v],B=[...Se?.originalOrder??[],...v.map(q=>q.id)];Qn({sections:S,originalOrder:B,detectedAt:Date.now()})},placementCount:re.length,onClearPlacements:()=>{tu(d=>d+1),Ef(d=>d+1),fe(()=>{Qn({sections:[],originalOrder:[],detectedAt:Date.now()})},200)},blankCanvas:xe,onBlankCanvasChange:d=>{let g={sections:[],originalOrder:[],detectedAt:Date.now()};d?(eu.current={rearrange:Se,placements:re},Qn(Yo.current.rearrange||g),rt(Yo.current.placements),De(null)):(Yo.current={rearrange:Se,placements:re},Qn(eu.current.rearrange||g),rt(eu.current.placements)),vt(d)},wireframePurpose:Ut,onWireframePurposeChange:Ol,Tooltip:ga,onDragStart:(d,g)=>{g.preventDefault();let x=P[d],v=null,S=!1,B=g.clientX,q=g.clientY,le=g.target.closest("[data-feedback-toolbar]")?.getBoundingClientRect().top??window.innerHeight,ce=Me=>{let Ye=Me.clientX-B,_e=Me.clientY-q;if(!S&&(Math.abs(Ye)>4||Math.abs(_e)>4)&&(S=!0,v=document.createElement("div"),v.className=`${R.dragPreview}${xe?` ${R.dragPreviewWireframe}`:""}`,document.body.appendChild(v)),!v)return;let te=Math.max(0,le-Me.clientY),Yt=Math.min(1,te/180),ht=1-Math.pow(1-Yt,2),Jt=28,ct=20,jt=Math.min(140,x.width*.18),ve=Math.min(90,x.height*.18),Ne=Jt+(jt-Jt)*ht,At=ct+(ve-ct)*ht;v.style.width=`${Ne}px`,v.style.height=`${At}px`,v.style.left=`${Me.clientX-Ne/2}px`,v.style.top=`${Me.clientY-At/2}px`,v.style.opacity=`${.5+.5*ht}`,v.textContent=ht>.25?d:""},ue=Me=>{if(window.removeEventListener("mousemove",ce),window.removeEventListener("mouseup",ue),v&&document.body.removeChild(v),S){let Ye=x.width,_e=x.height,te=window.scrollY,Yt=Math.max(0,Me.clientX-Ye/2),ht=Math.max(0,Me.clientY+te-_e/2),Jt={id:`dp-${Date.now()}-${Math.random().toString(36).slice(2,7)}`,type:d,x:Yt,y:ht,width:Ye,height:_e,scrollY:te,timestamp:Date.now()};rt(ct=>[...ct,Jt]),De(null),Ei.current=new Set,Mf(ct=>ct+1)}};window.addEventListener("mousemove",ce),window.addEventListener("mouseup",ue)}}),(0,j.jsx)(w4,{settings:$e,onSettingsChange:d=>Zy(g=>({...g,...d})),isDarkMode:vl,onToggleTheme:Ky,isDevMode:Bf,connectionStatus:dl,endpoint:f,isVisible:ae,toolbarNearBottom:!!zt&&zt.y<230,settingsPage:ie,onSettingsPageChange:Ce,onHideToolbar:Py})]})}),(se||Oe)&&(0,j.jsx)("div",{className:`${R.blankCanvas} ${tn?R.visible:""} ${Zs?R.gridActive:""}`,style:{"--canvas-opacity":bl},"data-feedback-toolbar":!0}),se&&xe&&tn&&(0,j.jsxs)("div",{className:R.wireframeNotice,"data-feedback-toolbar":!0,children:[(0,j.jsxs)("div",{className:R.wireframeOpacityRow,children:[(0,j.jsx)("span",{className:R.wireframeOpacityLabel,children:"Toggle Opacity"}),(0,j.jsx)("input",{type:"range",className:R.wireframeOpacitySlider,min:0,max:1,step:.01,value:bl,onChange:d=>kn(Number(d.target.value))})]}),(0,j.jsxs)("div",{className:R.wireframeNoticeTitleRow,children:[(0,j.jsx)("span",{className:R.wireframeNoticeTitle,children:"Wireframe Mode"}),(0,j.jsx)("span",{className:R.wireframeNoticeDivider}),(0,j.jsx)("button",{className:R.wireframeStartOver,onClick:()=>{tu(d=>d+1),Qn({sections:[],originalOrder:[],detectedAt:Date.now()}),Yo.current={rearrange:null,placements:[]},Ol(""),Wc(ye)},children:"Start Over"})]}),"Drag components onto the canvas.",(0,j.jsx)("br",{}),"Copied output will only include the wireframed layout."]}),(se||Oe)&&(0,j.jsx)(Fx,{placements:re,onChange:rt,activeComponent:Oe?null:Ge,onActiveComponentChange:De,isDarkMode:vl,exiting:Oe,onInteractionChange:Hy,passthrough:!Ge,extraSnapRects:Se?.sections.map(d=>d.currentRect),deselectSignal:Uy,clearSignal:Xy,wireframe:xe,onSelectionChange:(d,g)=>{Ei.current=d,g||(Ks.current=new Set,jy(x=>x+1))},onDragMove:(d,g)=>{let x=Ks.current;if(!(!x.size||!Se)){if(!cl.current){cl.current=new Map;for(let v of Se.sections)x.has(v.id)&&cl.current.set(v.id,{x:v.currentRect.x,y:v.currentRect.y})}for(let v of Se.sections){if(!x.has(v.id)||!cl.current.get(v.id))continue;let B=document.querySelector(`[data-rearrange-section="${v.id}"]`);B&&(B.style.transform=`translate(${d}px, ${g}px)`)}}},onDragEnd:(d,g,x)=>{let v=Ks.current,S=cl.current;if(cl.current=null,!(!v.size||!Se||!S)){for(let B of v){let q=document.querySelector(`[data-rearrange-section="${B}"]`);q&&(q.style.transform="")}x&&Qn(B=>B&&{...B,sections:B.sections.map(q=>{let V=S.get(q.id);return V?{...q,currentRect:{...q.currentRect,x:Math.max(0,V.x+d),y:Math.max(0,V.y+g)}}:q})})}}}),(se||Oe)&&Se&&(0,j.jsx)(gv,{rearrangeState:Se,onChange:Qn,isDarkMode:vl,exiting:Oe,blankCanvas:xe,extraSnapRects:re.map(d=>({x:d.x,y:d.y,width:d.width,height:d.height})),clearSignal:Iy,deselectSignal:Yy,onSelectionChange:(d,g)=>{Ks.current=d,g||(Ei.current=new Set,Mf(x=>x+1))},onDragMove:(d,g)=>{let x=Ei.current;if(x.size){if(!cl.current){cl.current=new Map;for(let v of re)x.has(v.id)&&cl.current.set(v.id,{x:v.x,y:v.y})}for(let v of x){let S=document.querySelector(`[data-design-placement="${v}"]`);S&&(S.style.transform=`translate(${d}px, ${g}px)`)}}},onDragEnd:(d,g,x)=>{let v=Ei.current,S=cl.current;if(cl.current=null,!(!v.size||!S)){for(let B of v){let q=document.querySelector(`[data-design-placement="${B}"]`);q&&(q.style.transform="")}x&&rt(B=>B.map(q=>{let V=S.get(q.id);return V?{...q,x:Math.max(0,V.x+d),y:Math.max(0,V.y+g)}:q}))}}}),(0,j.jsx)("canvas",{ref:lu,className:`${Y.drawCanvas} ${ul?Y.active:""}`,style:{opacity:ru?1:0,transition:"opacity 0.15s ease"},"data-feedback-toolbar":!0}),(0,j.jsxs)("div",{className:Y.markersLayer,"data-feedback-toolbar":!0,children:[F&&Ma.filter(d=>!d.isFixed).map((d,g,x)=>(0,j.jsx)(dy,{annotation:d,globalIndex:Ma.findIndex(v=>v.id===d.id),layerIndex:g,layerSize:x.length,isExiting:et,isClearing:ao,isAnimated:Uf.has(d.id),isHovered:!et&&Rl===d.id,isDeleting:yl===d.id,isEditingAny:!!Be,renumberFrom:ba,markerClickBehavior:$e.markerClickBehavior,tooltipStyle:Ff(d),onHoverEnter:v=>!et&&v.id!==tr.current&&ar(v),onHoverLeave:()=>ar(null),onClick:v=>$e.markerClickBehavior==="delete"?_u(v.id):or(v),onContextMenu:or},d.id)),F&&!et&&Kf.filter(d=>!d.isFixed).map(d=>(0,j.jsx)(_y,{annotation:d},d.id))]}),(0,j.jsxs)("div",{className:Y.fixedMarkersLayer,"data-feedback-toolbar":!0,children:[F&&Ma.filter(d=>d.isFixed).map((d,g,x)=>(0,j.jsx)(dy,{annotation:d,globalIndex:Ma.findIndex(v=>v.id===d.id),layerIndex:g,layerSize:x.length,isExiting:et,isClearing:ao,isAnimated:Uf.has(d.id),isHovered:!et&&Rl===d.id,isDeleting:yl===d.id,isEditingAny:!!Be,renumberFrom:ba,markerClickBehavior:$e.markerClickBehavior,tooltipStyle:Ff(d),onHoverEnter:v=>!et&&v.id!==tr.current&&ar(v),onHoverLeave:()=>ar(null),onClick:v=>$e.markerClickBehavior==="delete"?_u(v.id):or(v),onContextMenu:or},d.id)),F&&!et&&Kf.filter(d=>d.isFixed).map(d=>(0,j.jsx)(_y,{annotation:d,fixed:!0},d.id))]}),z&&(0,j.jsxs)("div",{className:Y.overlay,"data-feedback-toolbar":!0,style:W||Be?{zIndex:99999}:void 0,children:[Re?.rect&&!W&&!Ke&&!$l&&(0,j.jsx)("div",{className:`${Y.hoverHighlight} ${Y.enter}`,style:{left:Re.rect.left,top:Re.rect.top,width:Re.rect.width,height:Re.rect.height,borderColor:"color-mix(in srgb, var(--agentation-color-accent) 50%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 4%, transparent)"}}),Qt.filter(d=>document.contains(d.element)).map((d,g)=>{let x=d.element.getBoundingClientRect(),v=Qt.length>1;return(0,j.jsx)("div",{className:v?Y.multiSelectOutline:Y.singleSelectOutline,style:{position:"fixed",left:x.left,top:x.top,width:x.width,height:x.height,...v?{}:{borderColor:"color-mix(in srgb, var(--agentation-color-accent) 60%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 5%, transparent)"}}},g)}),Rl&&!W&&(()=>{let d=h.find(S=>S.id===Rl);if(!d?.boundingBox)return null;if(d.elementBoundingBoxes?.length)return sl.length>0?sl.filter(S=>document.contains(S)).map((S,B)=>{let q=S.getBoundingClientRect();return(0,j.jsx)("div",{className:`${Y.multiSelectOutline} ${Y.enter}`,style:{left:q.left,top:q.top,width:q.width,height:q.height}},`hover-outline-live-${B}`)}):d.elementBoundingBoxes.map((S,B)=>(0,j.jsx)("div",{className:`${Y.multiSelectOutline} ${Y.enter}`,style:{left:S.x,top:S.y-tt,width:S.width,height:S.height}},`hover-outline-${B}`));let g=Uo&&document.contains(Uo)?Uo.getBoundingClientRect():null,x=g?{x:g.left,y:g.top,width:g.width,height:g.height}:{x:d.boundingBox.x,y:d.isFixed?d.boundingBox.y:d.boundingBox.y-tt,width:d.boundingBox.width,height:d.boundingBox.height},v=d.isMultiSelect;return(0,j.jsx)("div",{className:`${v?Y.multiSelectOutline:Y.singleSelectOutline} ${Y.enter}`,style:{left:x.x,top:x.y,width:x.width,height:x.height,...v?{}:{borderColor:"color-mix(in srgb, var(--agentation-color-accent) 60%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 5%, transparent)"}}})})(),Re&&!W&&!Ke&&!$l&&(0,j.jsxs)("div",{className:`${Y.hoverTooltip} ${Y.enter}`,style:{left:Math.max(8,Math.min(Ee.x,window.innerWidth-100)),top:Math.max(Ee.y-(Re.reactComponents?48:32),8)},children:[Re.reactComponents&&(0,j.jsx)("div",{className:Y.hoverReactPath,children:Re.reactComponents}),(0,j.jsx)("div",{className:Y.hoverElementName,children:Re.elementName})]}),W&&(0,j.jsxs)(j.Fragment,{children:[W.multiSelectElements?.length?W.multiSelectElements.filter(d=>document.contains(d)).map((d,g)=>{let x=d.getBoundingClientRect();return(0,j.jsx)("div",{className:`${Y.multiSelectOutline} ${Ai?Y.exit:Y.enter}`,style:{left:x.left,top:x.top,width:x.width,height:x.height}},`pending-multi-${g}`)}):W.targetElement&&document.contains(W.targetElement)?(()=>{let d=W.targetElement.getBoundingClientRect();return(0,j.jsx)("div",{className:`${Y.singleSelectOutline} ${Ai?Y.exit:Y.enter}`,style:{left:d.left,top:d.top,width:d.width,height:d.height,borderColor:"color-mix(in srgb, var(--agentation-color-accent) 60%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 5%, transparent)"}})})():W.boundingBox&&(0,j.jsx)("div",{className:`${W.isMultiSelect?Y.multiSelectOutline:Y.singleSelectOutline} ${Ai?Y.exit:Y.enter}`,style:{left:W.boundingBox.x,top:W.boundingBox.y-tt,width:W.boundingBox.width,height:W.boundingBox.height,...W.isMultiSelect?{}:{borderColor:"color-mix(in srgb, var(--agentation-color-accent) 60%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 5%, transparent)"}}}),(()=>{let d=W.x,g=W.isFixed?W.y:W.y-tt;return(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(_4,{x:d,y:g,isMultiSelect:W.isMultiSelect,isExiting:Ai}),(0,j.jsx)(Kc,{ref:qf,element:W.element,selectedText:W.selectedText,computedStyles:W.computedStylesObj,placeholder:W.element==="Area selection"?"What should change in this area?":W.isMultiSelect?"Feedback for this group of elements...":"What should change?",onSubmit:ep,onCancel:du,isExiting:Ai,lightMode:!vl,accentColor:W.isMultiSelect?"var(--agentation-color-green)":"var(--agentation-color-accent)",style:{left:Math.max(160,Math.min(window.innerWidth-160,d/100*window.innerWidth)),...g>window.innerHeight-290?{bottom:window.innerHeight-g+20}:{top:g+20}}})]})})()]}),Be&&(0,j.jsxs)(j.Fragment,{children:[Be.elementBoundingBoxes?.length?Ae.length>0?Ae.filter(d=>document.contains(d)).map((d,g)=>{let x=d.getBoundingClientRect();return(0,j.jsx)("div",{className:`${Y.multiSelectOutline} ${Y.enter}`,style:{left:x.left,top:x.top,width:x.width,height:x.height}},`edit-multi-live-${g}`)}):Be.elementBoundingBoxes.map((d,g)=>(0,j.jsx)("div",{className:`${Y.multiSelectOutline} ${Y.enter}`,style:{left:d.x,top:d.y-tt,width:d.width,height:d.height}},`edit-multi-${g}`)):(()=>{let d=de&&document.contains(de)?de.getBoundingClientRect():null,g=d?{x:d.left,y:d.top,width:d.width,height:d.height}:Be.boundingBox?{x:Be.boundingBox.x,y:Be.isFixed?Be.boundingBox.y:Be.boundingBox.y-tt,width:Be.boundingBox.width,height:Be.boundingBox.height}:null;return g?(0,j.jsx)("div",{className:`${Be.isMultiSelect?Y.multiSelectOutline:Y.singleSelectOutline} ${Y.enter}`,style:{left:g.x,top:g.y,width:g.width,height:g.height,...Be.isMultiSelect?{}:{borderColor:"color-mix(in srgb, var(--agentation-color-accent) 60%, transparent)",backgroundColor:"color-mix(in srgb, var(--agentation-color-accent) 5%, transparent)"}}}):null})(),(0,j.jsx)(Kc,{ref:Qf,element:Be.element,selectedText:Be.selectedText,computedStyles:cv(Be.computedStyles),placeholder:"Edit your feedback...",initialValue:Be.comment,submitLabel:"Save",onSubmit:tp,onCancel:np,onDelete:()=>_u(Be.id),isExiting:Fy,lightMode:!vl,accentColor:Be.isMultiSelect?"var(--agentation-color-green)":"var(--agentation-color-accent)",style:(()=>{let d=Be.isFixed?Be.y:Be.y-tt;return{left:Math.max(160,Math.min(window.innerWidth-160,Be.x/100*window.innerWidth)),...d>window.innerHeight-290?{bottom:window.innerHeight-d+20}:{top:d+20}}})()})]}),$l&&(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)("div",{ref:Li,className:Y.dragSelection}),(0,j.jsx)("div",{ref:Ri,className:Y.highlightsContainer})]})]})]}),document.body)}var Cf=document.createElement("div");Cf.id="agentation-root";document.body.appendChild(Cf);var C4=(0,$y.createRoot)(Cf);C4.render(Oy.default.createElement(By));})();
/*! Bundled license information:

react/cjs/react.production.js:
  (**
   * @license React
   * react.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

scheduler/cjs/scheduler.production.js:
  (**
   * @license React
   * scheduler.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react-dom/cjs/react-dom.production.js:
  (**
   * @license React
   * react-dom.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react-dom/cjs/react-dom-client.production.js:
  (**
   * @license React
   * react-dom-client.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react/cjs/react-jsx-runtime.production.js:
  (**
   * @license React
   * react-jsx-runtime.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
