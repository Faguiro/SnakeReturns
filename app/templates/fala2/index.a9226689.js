function e(e){return e&&e.__esModule?e.default:e}var t={};function n(n,i){const o=document.getElementsByTagName("main")[0],r=document.getElementById("voices");let c,s;const a=()=>{const e=speechSynthesis.getVoices();e.forEach((e=>{const t=document.createElement("option");let n=`${e.name} (${e.lang})`;e.default&&(n+=" [default]",void 0===s&&(s=e,t.selected=!0)),s===e&&(t.selected=!0),t.textContent=n,r.appendChild(t)})),c=e};a(),void 0!==speechSynthesis.onvoiceschanged&&(speechSynthesis.onvoiceschanged=a);const d=n;r.addEventListener("change",(n=>{const i=n.target.selectedIndex;e(t).set("vozes",i)})),s=e(t).get("vozes");const l=new SpeechSynthesisUtterance(d);l.voice=c[i],l.addEventListener("start",(e=>{o.classList.add("speaking")})),l.addEventListener("end",(e=>{o.addEventListener("animationiteration",(e=>{o.classList.remove("speaking")}),{once:!0})})),speechSynthesis.speak(l)}t=function(){function e(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var i in n)e[i]=n[i]}return e}function t(n,i){function o(t,o,r){if("undefined"!=typeof document){"number"==typeof(r=e({},i,r)).expires&&(r.expires=new Date(Date.now()+864e5*r.expires)),r.expires&&(r.expires=r.expires.toUTCString()),t=encodeURIComponent(t).replace(/%(2[346B]|5E|60|7C)/g,decodeURIComponent).replace(/[()]/g,escape);var c="";for(var s in r)r[s]&&(c+="; "+s,!0!==r[s]&&(c+="="+r[s].split(";")[0]));return document.cookie=t+"="+n.write(o,t)+c}}function r(e){if("undefined"!=typeof document&&(!arguments.length||e)){for(var t=document.cookie?document.cookie.split("; "):[],i={},o=0;o<t.length;o++){var r=t[o].split("="),c=r.slice(1).join("=");try{var s=decodeURIComponent(r[0]);if(i[s]=n.read(c,s),e===s)break}catch(e){}}return e?i[e]:i}}return Object.create({set:o,get:r,remove:function(t,n){o(t,"",e({},n,{expires:-1}))},withAttributes:function(n){return t(this.converter,e({},this.attributes,n))},withConverter:function(n){return t(e({},this.converter,n),this.attributes)}},{attributes:{value:Object.freeze(i)},converter:{value:Object.freeze(n)}})}return t({read:function(e){return'"'===e[0]&&(e=e.slice(1,-1)),e.replace(/(%[\dA-F]{2})+/gi,decodeURIComponent)},write:function(e){return encodeURIComponent(e).replace(/%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,decodeURIComponent)}},{path:"/"})}(),$(document).ready((function(){n("Bem vindo ao sistema!"),$(".start").click((function(){const i=$("#msg").val(),o=$("#lista");""!=i&&o.append(`<span class="lista-msg">\n            <div id="icon-play">🗣️</div>\n            <p id="x-msg" >${i}</p>\n            <h4 id="trash">🗑️</h4>\n            </span>`),function(i){this.element=document.querySelectorAll(i),this.element.forEach((function(i){let o=i.parentElement.firstElementChild,r=i.parentElement.lastElementChild;o.onmouseover=function(){n(i.innerText,e(t).get("bandeira"))},r.onclick=function(){r.parentElement.remove()}}))}("p"),n(i,e(t).get("bandeira"))})),$(".bandeiras").click((function(n){n.preventDefault();let i=n.target;i.classList.value,e(t).set("bandeira",i.classList.value),console.log(e(t).get("bandeira"))}))}));
//# sourceMappingURL=index.a9226689.js.map
