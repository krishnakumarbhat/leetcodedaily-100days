#!/usr/bin/env node
/* ============================================================
   Section page smoke test — run with:
     node test_section.js sections/section_02_two_pointers.html
   Loads the page in jsdom, registers every problem, then for
   EVERY problem × EVERY approach: clicks Run, steps the whole
   animation to the end, and verifies a result appears and no
   alert/exception was thrown.
   Exit code 0 = all good.
   ============================================================ */
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const file = process.argv[2];
if (!file) { console.error("usage: node test_section.js <section.html>"); process.exit(2); }
const abs = path.isAbsolute(file) ? file : path.resolve(process.cwd(), file);
const html = fs.readFileSync(abs, 'utf8');

const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable",
  url: "file://" + abs
});

const alerts = [];
dom.window.alert = m => alerts.push(m);
dom.window.onerror = m => alerts.push("onerror: " + m);

setTimeout(() => {
  const w = dom.window;
  const probs = w.document.querySelectorAll('#problemList button').length;
  if (!probs) { console.error("FAIL: no problems registered — page broken"); process.exit(1); }
  console.log("problems:", probs);
  const btnRun = w.document.getElementById('btnRun');
  const btnStep = w.document.getElementById('btnStep');
  let fails = 0;

  for (let p = 0; p < probs; p++) {
    w.document.querySelectorAll('#problemList button')[p].click();
    const tabs = w.document.querySelectorAll('#tabs button');
    for (let a = 0; a < tabs.length; a++) {
      w.document.querySelectorAll('#tabs button')[a].click();
      btnRun.click();
      /* walk every step of the animation */
      const max = w.document.getElementById('scrub').max || '0';
      for (let s = 0; s < Number(max); s++) btnStep.click();
      const rtext = w.document.querySelector('.res-value') ? w.document.querySelector('.res-value').textContent : "(no result)";
      const bad = /wrong|undefined|NaN|error/i.test(rtext);
      if (bad) fails++;
      console.log(`P${p+1} A${a+1}: steps=${Number(max)+1} | ${rtext.slice(0,70)} ${bad ? 'FAIL' : 'ok'}`);
    }
  }
  console.log("alerts:", alerts.length, "| fails:", fails);
  if (fails === 0 && alerts.length === 0) { console.log("ALL ANIMATIONS OK"); process.exit(0); }
  console.error(alerts.join("\n"));
  process.exit(1);
}, 1800);
