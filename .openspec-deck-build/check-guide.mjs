import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const root='/Users/ratipcanuysal/Documents/ChatGPT/openspec';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
const errors=[],overflow=[];page.on('pageerror',e=>errors.push(e.message));await page.route('http**',r=>r.abort());
await page.goto('file://'+root+'/output/openspec-pm/openspec-pm.html');
await page.locator('#guideBtn').click();if(!await page.locator('#guide').evaluate(e=>e.open))throw Error('Guide entry failed');
const count=await page.locator('#guideMenu button').count();
for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844},{width:320,height:740}]){
 await page.setViewportSize(viewport);
 for(let i=0;i<count;i++){
  await page.evaluate(i=>showGuide(i),i);await page.locator('#guideArticle details').evaluateAll(es=>es.forEach(e=>e.open=true));
  const geo=await page.evaluate(()=>{const d=document.getElementById('guide'),a=document.getElementById('guideArticle');return{w:innerWidth,doc:document.documentElement.scrollWidth,dialog:d.getBoundingClientRect().width,article:a.clientWidth,scroll:a.scrollWidth}});
  if(geo.doc>geo.w+1||geo.scroll>geo.article+1)overflow.push({page:i+1,viewport,...geo});
  if(viewport.width===1440&&[0,2,5,8,14].includes(i)){await page.screenshot({path:root+`/.openspec-deck-build/html-preview/guide-${i+1}.png`});}
 }
}
await page.setViewportSize({width:1440,height:900});
for(const os of ['mac','windows','linux']){
 await page.locator('#guideOS').selectOption(os);await page.evaluate(()=>showGuide(2));
 const install=await page.locator('#guide-install-home').innerText();if(!install.includes('\nopenspec --version')||install.includes('\\n'))throw Error('Multiline shell block broken');
 if(os==='windows'&&!install.includes('$HOME\\.npm-global'))throw Error('PowerShell path broken');
 for(const tool of ['codex','claude','cursor']){
  await page.locator('#guideTool').selectOption(tool);await page.evaluate(()=>showGuide(4));
  if(!await page.locator('#guide-init').innerText().then(t=>t.includes('--tools '+tool)))throw Error('Tool init mapping broken');
  const cmd=tool==='codex'?'$openspec-explore':tool==='claude'?'/opsx:explore':'/opsx-explore';
  if(!await page.locator('#guide-explore').innerText().then(t=>t.startsWith(cmd+'\n')))throw Error('Chat mapping broken');
  await page.evaluate(()=>showGuide(8));await page.locator('#guideArticle details').first().locator('summary').click();const practice=await page.locator('#guide-practice').innerText();if(!practice.includes('openspec init --tools '+tool)||os==='windows'&&!practice.includes('$HOME\\work\\openspec-practice'))throw Error('Practice setup broken');
 }
}
await page.locator('#guideOS').selectOption('mac');await page.locator('#guideTool').selectOption('codex');
await page.locator('#guideSearch').fill('atomik');if(await page.locator('#guideMenu button:visible').count()<1)throw Error('Guide full text search broken');await page.locator('#guideSearch').fill('');
await page.evaluate(()=>showGuide(13));await page.locator('#glossarySearch').fill('prefix');if(await page.locator('.glossary-item:visible').count()!==1)throw Error('Glossary search failed');
await page.evaluate(()=>showGuide(14));await page.locator('#gradeQuiz').click();if(!await page.locator('#quizResult').innerText().then(t=>t.startsWith('0 / 8')))throw Error('Empty quiz grading failed');
const keys=await page.evaluate(()=>guideQuestions.map(q=>q[2]));for(let i=0;i<keys.length;i++)await page.locator(`input[name="quiz-${i}"][value="${keys[i]}"]`).check();await page.locator('#gradeQuiz').click();if(!await page.locator('#quizResult').innerText().then(t=>t.startsWith('8 / 8')))throw Error('Correct quiz grading failed');
await page.evaluate(()=>showGuide(13));await page.evaluate(()=>showGuide(14));if(await page.locator('#guideQuiz input:checked').count()!==8)throw Error('Quiz state lost');
await page.locator('#resetQuiz').click();if(await page.locator('#guideQuiz input:checked').count()!==0)throw Error('Quiz reset failed');
await page.evaluate(()=>showGuide(8));await page.locator('#guideArticle details').nth(1).locator('summary').click();if(!await page.locator('#g-case-0').innerText().then(t=>t.includes('## Requirements')))throw Error('Full case rendering failed');
await page.locator('[data-copy-target="g-case-0"]').click();await page.locator('#toast').waitFor({state:'visible'});
const downloadEvent=page.waitForEvent('download');await page.locator('[data-case-download]').click();const download=await downloadEvent;await download.saveAs(root+'/.openspec-deck-build/html-preview/full-case.txt');
const downloaded=await fs.readFile(root+'/.openspec-deck-build/html-preview/full-case.txt','utf8');if(!downloaded.includes('===== openspec/specs/package-change/spec.md =====\n# Package Change'))throw Error('Case download damaged');
await page.evaluate(()=>showGuide(6));const kitEvent=page.waitForEvent('download');await page.locator('[data-kit-download]').click();const kit=await kitEvent;await kit.saveAs(root+'/.openspec-deck-build/html-preview/guide-kit.zip');
await page.locator('[data-atlas-jump="11"]').click();if(!await page.locator('#atlas').evaluate(e=>e.open))throw Error('Guide to atlas failed');await page.keyboard.press('Escape');await page.locator('#guideBtn').click();if(!await page.locator('#guide').evaluate(e=>e.open))throw Error('Guide resume failed');
await page.keyboard.press('Escape');if(await page.locator('#guide').evaluate(e=>e.open))throw Error('Guide Esc failed');
await page.locator('#guideBtn').click();await page.evaluate(()=>{window.print=()=>{};printLearnerGuide();});
if(await page.locator('#guidePrint article').count()!==15)throw Error('Guide print incomplete');if(await page.locator('#guidePrint details:not([open])').count())throw Error('Print case hidden');
const dup=await page.evaluate(()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.filter((id,i)=>ids.indexOf(id)!==i);});if(dup.length)throw Error('Duplicate IDs after print preparation: '+dup.join(','));
await page.emulateMedia({media:'print'});await page.pdf({path:root+'/.openspec-deck-build/html-preview/guide-print.pdf',printBackground:true,preferCSSPageSize:true});await page.emulateMedia({media:'screen'});await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
await page.setViewportSize({width:390,height:844});await page.evaluate(()=>showGuide(2));await page.screenshot({path:root+'/.openspec-deck-build/html-preview/guide-mobile.png'});
console.log(JSON.stringify({guidePages:count,toolOSCombinations:9,glossaryTerms:await page.evaluate(()=>guideGlossary.length),quizQuestions:8,errors,overflow,interactiveChecks:'passed'},null,2));
await browser.close();if(errors.length||overflow.length)process.exitCode=1;
