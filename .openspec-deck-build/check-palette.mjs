import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const root='/Users/ratipcanuysal/Documents/ChatGPT/openspec';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
await page.goto('file://'+root+'/output/openspec-pm/openspec-pm.html');
const issues=[];let minimum=100,checked=0;
async function audit(label){
 const result=await page.evaluate(()=>{
  const rgba=s=>{const v=s.match(/[\d.]+/g)?.map(Number)||[];return [v[0]||0,v[1]||0,v[2]||0,v[3]??1];};
  const blend=(a,b)=>[0,1,2].map(i=>a[i]*a[3]+b[i]*(1-a[3]));
  const lum=c=>c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0);
  const issues=[];let minimum=100,checked=0;
  for(const e of document.querySelectorAll('body *')){
   const text=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
   if(!text||['SCRIPT','STYLE','OPTION'].includes(e.tagName)||e.closest('[hidden]')||e.closest('dialog:not([open])'))continue;
   const rect=e.getBoundingClientRect();if(!rect.width||!rect.height)continue;
   let layers=[],alpha=1;for(let n=e;n;n=n.parentElement){const cs=getComputedStyle(n);layers.push(rgba(cs.backgroundColor));alpha*=Number(cs.opacity);}
   let bg=[255,255,255];for(const color of layers.reverse())bg=blend(color,bg);
   const cs=getComputedStyle(e);const fg=blend(rgba(cs.color),bg);const l1=lum(fg),l2=lum(bg);const ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
   const large=parseFloat(cs.fontSize)>=24||(parseFloat(cs.fontSize)>=18.66&&Number(cs.fontWeight)>=700);
   minimum=Math.min(minimum,ratio);checked++;
   if(ratio<(large?3:4.5)-.02||alpha<.99)issues.push({text:text.slice(0,80),selector:e.tagName+'.'+e.className,ratio:+ratio.toFixed(2),alpha,color:cs.color,bg});
  }
  return {issues,minimum,checked};
 });
 checked+=result.checked;minimum=Math.min(minimum,result.minimum);issues.push(...result.issues.map(x=>({label,...x})));
}
const count=await page.locator('.scene').count();
for(let i=0;i<count;i++){
 const steps=await page.evaluate(i=>Number(slides[i].dataset.steps),i);
 for(let t=0;t<=steps;t++){await page.evaluate(({i,t})=>go(i,t),{i,t});await audit(`scene-${i+1}-step-${t}`);}
}
for(let i=0;i<await page.locator('#atlasMenu button').count();i++){await page.evaluate(i=>showAtlas(i),i);await audit(`atlas-${i+1}`);}
for(let i=0;i<await page.evaluate(()=>guidePages.length);i++){await page.evaluate(i=>showGuide(i),i);await page.locator('#guideArticle details').evaluateAll(es=>es.forEach(e=>e.open=true));if(i===14)await page.locator('#gradeQuiz').click();await audit(`guide-${i+1}`);}
await page.evaluate(()=>{closeDialogs();go(20,0);});await page.screenshot({path:root+'/.openspec-deck-build/html-preview/palette-context-step0.png'});
await page.evaluate(()=>go(20,2));await page.screenshot({path:root+'/.openspec-deck-build/html-preview/palette-context-step2.png'});
await page.setViewportSize({width:390,height:844});await page.evaluate(()=>go(20,0));await page.screenshot({path:root+'/.openspec-deck-build/html-preview/palette-mobile.png',fullPage:true});
await fs.writeFile(root+'/.openspec-deck-build/html-preview/palette-audit.json',JSON.stringify({minimumContrast:+minimum.toFixed(2),checked,issues},null,2));
console.log(JSON.stringify({minimumContrast:+minimum.toFixed(2),checked,issues},null,2));
await browser.close();if(issues.length)process.exitCode=1;
