import fs from 'node:fs/promises';
import {chromium} from 'playwright';
const root='/Users/ratipcanuysal/Documents/ChatGPT/openspec';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('http**',r=>r.abort());
await page.goto('file://'+root+'/output/openspec-pm/openspec-pm.html');
const slideCount=await page.locator('.scene').count();
const atlasCount=await page.locator('#atlasMenu button').count();
await fs.mkdir(root+'/.openspec-deck-build/html-preview',{recursive:true});
const overflow=[];
for(const viewport of [{width:1440,height:900},{width:1280,height:720},{width:390,height:844},{width:320,height:740}]){
 await page.setViewportSize(viewport);
 for(let i=0;i<slideCount;i++){
  await page.evaluate(i=>{go(i,Number(slides[i].dataset.steps));},i);
  const geometry=await page.evaluate(()=>({scrollW:document.documentElement.scrollWidth,w:innerWidth,scrollH:document.documentElement.scrollHeight,h:innerHeight,footerBottom:document.querySelector('footer').getBoundingClientRect().bottom,sceneBottom:document.querySelector('.scene:not([hidden])').getBoundingClientRect().bottom}));
  if(geometry.scrollW>viewport.width+1||viewport.width>760&&geometry.scrollH>viewport.height+1)overflow.push({slide:i+1,viewport,...geometry});
  if(viewport.width===1440)await page.screenshot({path:root+`/.openspec-deck-build/html-preview/s${String(i+1).padStart(2,'0')}.png`,fullPage:true});
 }
}
console.log('GEOMETRY',JSON.stringify(overflow));
await page.setViewportSize({width:1440,height:900});
await page.evaluate(()=>go(0));
await page.keyboard.press('ArrowRight');if(!await page.locator('#counter').innerText().then(t=>t.includes('adım 1')))throw Error('Step navigation failed');
await page.keyboard.press('ArrowLeft');if(!await page.locator('#counter').innerText().then(t=>t.includes('adım 0')))throw Error('Step reverse failed');
await page.keyboard.press('a');if(!await page.locator('#atlas').evaluate(e=>e.open))throw Error('Atlas did not open');
for(let i=0;i<atlasCount;i++){await page.locator('#atlasMenu button').nth(i).click();if(!await page.locator('#atlasContent h2').isVisible())throw Error('Atlas section failed');}
await page.locator('#atlasSearch').fill('symlink');if(await page.locator('#atlasMenu button:visible').count()<1)throw Error('Atlas search failed');
await page.keyboard.press('Escape');
await page.waitForFunction(()=>!document.getElementById('atlas').open);
await page.keyboard.press('n');await page.waitForFunction(()=>document.getElementById('notes').open);await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.getElementById('notes').open);
await page.keyboard.press('i');await page.locator('#tocList button').nth(11).click();await page.locator('.review-hit').nth(0).click();if(!await page.locator('.review-row').nth(0).locator('.reason').isVisible())throw Error('Review failed');
await page.evaluate(()=>go(15));await page.locator('#domain').selectOption('sipariş iptali');if(!await page.locator('#starterPrompt').innerText().then(t=>t.includes('Sipariş iptali')))throw Error('Domain adaptation failed');
await page.evaluate(()=>showAtlas(7));await page.screenshot({path:root+'/.openspec-deck-build/html-preview/atlas.png'});await page.keyboard.press('Escape');
await page.waitForFunction(()=>!document.getElementById('atlas').open);
await page.evaluate(()=>go(15));await page.locator('#copyPrompt').click();await page.locator('#toast').waitFor({state:'visible',timeout:5000});
await page.locator('#workshopBtn').click();if(!await page.locator('#workshop-start').isVisible())throw Error('Workshop jump failed');
await page.evaluate(()=>go(23));await page.locator('#contextForm input[name="product"]').fill('Sipariş yönetimi');if(!await page.locator('#generatedContext').innerText().then(t=>t.includes('Sipariş yönetimi')))throw Error('Context generator failed');
await page.locator('[data-copy-target="generatedContext"]').click();await page.locator('#toast').waitFor({state:'visible',timeout:5000});
await page.evaluate(()=>go(25));await page.locator('.readiness-list input').nth(0).check();if(!await page.locator('#readinessStatus').innerText().then(t=>t.startsWith('1 / 5')))throw Error('Readiness counter failed');
const kitHref=await page.locator('.download-kit').getAttribute('href');if(!kitHref.startsWith('data:application/zip;base64,')||Buffer.from(kitHref.split(',')[1],'base64').subarray(0,2).toString()!=='PK')throw Error('Embedded starter kit failed');
await page.evaluate(()=>showAtlas(11));if(await page.locator('#atlas-config').innerText()!==await page.evaluate(()=>kit['openspec/config.example.yaml']))throw Error('Config rendering failed');
await page.locator('[data-copy-target="atlas-config"]').click();await page.locator('#toast').waitFor({state:'visible',timeout:5000});await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.getElementById('atlas').open);
await page.locator('#fullBtn').click();await page.waitForFunction(()=>!!document.fullscreenElement);await page.keyboard.press('f');await page.waitForFunction(()=>!document.fullscreenElement);
await page.evaluate(()=>go(18,1));await page.locator('[data-open-atlas="9"]:visible').click();if(!await page.locator('#atlas-user-skills').isVisible())throw Error('Workshop atlas link failed');await page.screenshot({path:root+'/.openspec-deck-build/html-preview/user-skills.png'});await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.getElementById('atlas').open);
const downloadEvent=page.waitForEvent('download');await page.evaluate(()=>go(25));await page.locator('.download-kit').click();const download=await downloadEvent;await download.saveAs(root+'/.openspec-deck-build/html-preview/downloaded-kit.zip');
for(const i of [17,23,25]){await page.setViewportSize({width:390,height:844});await page.evaluate(i=>go(i,Number(slides[i].dataset.steps)),i);await page.screenshot({path:root+`/.openspec-deck-build/html-preview/workshop-mobile-${i+1}.png`,fullPage:true});}
await page.setViewportSize({width:390,height:844});await page.evaluate(()=>go(0,2));await page.screenshot({path:root+'/.openspec-deck-build/html-preview/mobile.png',fullPage:true});
await page.evaluate(()=>showAtlas(0));if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw Error('Mobile atlas overflow');await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.getElementById('atlas').open);
await page.setViewportSize({width:1440,height:900});
await page.emulateMedia({media:'print'});await page.pdf({path:root+'/.openspec-deck-build/html-preview/print.pdf',printBackground:true,preferCSSPageSize:true});
console.log(JSON.stringify({errors,overflow,slideCount,atlasCount,interactiveChecks:'passed'},null,2));
if(errors.length||overflow.length)process.exitCode=1;
await browser.close();
