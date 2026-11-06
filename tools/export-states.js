const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.2 });
  await page.goto('file://' + path.resolve('site/bitfest-2026/index.html')); await page.waitForTimeout(1500);
  await page.evaluate(()=>{document.body.classList.remove('show-hint');const h=document.getElementById('hint');if(h)h.style.display='none';});
  const info=await page.evaluate(()=>({ids:[...document.querySelectorAll('section.slide')].map(s=>s.id),steps:window.__deck.steps,
    notes:[...document.querySelectorAll('section.slide')].map(s=>{const a=s.querySelector('aside.m-notes');return a?a.textContent.trim():''}),
    frames:[...document.querySelectorAll('section.slide')].map(s=>{const f=s.querySelector('.frame video');return f?f.getAttribute('src'):null})}));
  const settle=async(extra)=>{for(let t=0;t<60;t++){const b=await page.evaluate(()=>window.__deck.busy);if(!b)break;await page.waitForTimeout(100);}await page.waitForTimeout(extra);};
  const freezeVideo=async()=>page.evaluate(()=>{document.querySelectorAll('video').forEach(v=>{v.pause();v.currentTime=0;});});
  const out={slides:[]};
  const only=process.argv[2];for(let i=0;i<info.ids.length;i++){ if(only&&info.ids[i]!==only)continue;
    const id=info.ids[i]; const n=Math.max(1,info.steps[i]);
    await page.evaluate(i=>window.__deck.go(i),i); await settle(id==='flight'?3600:id==='chain-agent'?4200:1400); await freezeVideo();
    const files=[]; let f=`pptx/states/${String(i+1).padStart(2,'0')}-${id}-0.png`; await page.screenshot({path:f}); files.push(f);
    for(let k=1;k<n;k++){ await page.evaluate(()=>window.__deck.next()); await settle(1400); await freezeVideo(); f=`pptx/states/${String(i+1).padStart(2,'0')}-${id}-${k}.png`; await page.screenshot({path:f}); files.push(f); }
    let frame=null; if(info.frames[i]){ frame=await page.evaluate(()=>{const r=document.querySelector('section.slide.cur .frame').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}); }
    out.slides.push({id,steps:n,files,notes:info.notes[i],video:info.frames[i],frame});
    console.log(i+1,id,n,'states');
  }
  if(!only)fs.writeFileSync('pptx/states.json',JSON.stringify(out,null,1));
  await browser.close(); })();
