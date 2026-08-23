/* ============================================================
   NeetCode 150 — Interactive Learning Engine (engine.js)
   ------------------------------------------------------------
   What this file does:
     • Renders the sticky top navigation (section links).
     • Renders the sidebar problem list with difficulty dots.
     • Renders each problem's input form, example chips, badges.
     • Renders memory visualizations with FAKE but realistic hex
       addresses so you can SEE how data lives in RAM and moves.
     • Plays/scrubs an animated "step script" produced by each
       problem's own step-generator function (written in JS).
     • Highlights the matching pseudocode line on every step.
     • Shows per-approach complexity, DS deep-dive and real-life
       usage panels (content provided by the problem definition).
   ------------------------------------------------------------
   How a section page works:
     const SECTION = {...}            // nav metadata
     NC150.register(problemDef)       // one call per problem
     NC150.init(SECTION)              // assemble the page
   ------------------------------------------------------------
   Step schema (what a problem's step-generator must return):
     {
       steps: [ {
         text: "HTML string explained in plain language",
         code: 3,                          // pseudocode line to highlight
         mem: [ { ...memory view... } ],   // zero or more views
         result: "final answer (only on last step)",
         correct: true/false               // optional verdict vs expected
       }, ... ],
       result: "...",                      // overall result string
       correct: true/false,
       memNote: "space explanation string"
     }
   Memory view types: 'array','string','hashmap','stack','queue',
     'list','tree','grid','heap'
   ============================================================ */

(function () {
  "use strict";

  /* ---------------- tiny utilities ---------------- */
  function el(tag, cls, html) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  /* Fake-but-consistent hex memory addresses. base = 0x7FFC, each
     element occupies `size` bytes, exactly like real RAM. */
  const ADDR_BASE = 0x7ffc0000;
  function addr(i, size) {
    return "0x" + (ADDR_BASE + i * size).toString(16).toUpperCase().padStart(8, "0");
  }

  /* ---------------- input parsing helpers ---------------- */
  /* Parses "[1,2,3]" or "1,2,3" or '["a","b"]' into a JS array.
     Handles nested arrays, numbers, quoted strings, null. */
  function parseList(str) {
    str = String(str).trim();
    if (str.startsWith("[")) {
      const tokens = [];
      let depth = 0, cur = "", inStr = false;
      for (let i = 0; i < str.length; i++) {
        const c = str[i];
        if (c === '"' || c === "'") { inStr = !inStr; cur += c; continue; }
        if (inStr) { cur += c; continue; }
        if (c === "[") { depth++; continue; }
        if (c === "]") { depth--; continue; }
        if (c === "," && depth === 1) { tokens.push(cur.trim()); cur = ""; continue; }
        cur += c;
      }
      if (cur.trim()) tokens.push(cur.trim());
      return tokens.map(t => {
        if (!t) return null;
        if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith("'") && t.endsWith("'"))) return t.slice(1, -1);
      if (t === "null" || t === "None") return null;
      if (t.startsWith("[") || t.includes(",")) return parseList(t);
      const n = Number(t);
        return Number.isNaN(n) ? t : n;
      });
    }
    return str.split(",").map(t => {
      t = t.trim();
      if (!t) return null;
      const n = Number(t);
      return Number.isNaN(n) ? t : n;
    });
  }
  function parseNum(str) { return Number(String(str).trim()); }
  function parseStr(str) { return String(str); }
  /* rows like "3,4" or "[3,4]" -> [3,4]; for grid dims */
  function parsePair(str) {
    const a = parseList(str);
    return [Number(a[0]), Number(a[1])];
  }
  /* builds a linked-list / tree node helper the step generators share */
  function ListNode(val, next) { this.val = val; this.next = next || null; }
  function TreeNode(val) { this.val = val; this.left = null; this.right = null; }

  /* ---------------- memory view renderers ---------------- */
  const Render = {
    /* generic horizontal array of cells with address labels */
    array(view) {
      const data = view.data || [];
      const size = view.size || 4;               // bytes per element (int=4, ptr=8, char=1)
      const block = el("div", "mem-block");
      block.appendChild(el("div", "mem-title", esc(view.title || "array")));
      const cells = el("div", "cells");
      data.forEach((v, i) => {
        const cls = ["cell"];
        if (view.cls && view.cls[i]) cls.push(view.cls[i]);
        if (v === null || v === undefined || v === "") cls.push("empty");
        const c = el("div", cls.join(" "));
        const showAddr = view.hideAddr ? "" : `<div class="addr">${addr(i, size)}</div>`;
        c.innerHTML = showAddr +
          `<div class="val">${esc(v === null || v === undefined ? "∅" : v)}</div>` +
          (view.showIdx ? `<div class="idx">[${i}]</div>` : "");
        cells.appendChild(c);
      });
      block.appendChild(cells);
      return block;
    },

    /* string = array of chars, size 1 */
    string(view) { return Render.array(Object.assign({ size: 1, showIdx: true }, view)); },

    /* heap = 1-indexed array (children at 2i, 2i+1) */
    heap(view) {
      const v = Object.assign({ showIdx: true }, view);
      v.data = view.data || [];
      return Render.array(v);
    },

    /* hash map: mode 'open'  = Python dict style (open addressing,
       linear probing) ; mode 'chaining' = C++ unordered_map style.
       slots: [{k,v}|null]. probe: [slotIdx,...] visited in order. */
    hashmap(view) {
      const mode = view.mode || "open";
      const slots = view.slots || [];
      const probe = view.probe || [];
      const block = el("div", "mem-block");
      const title = el("div", "mem-title", esc(view.title || "hashmap") +
        (mode === "open" ? " · open addressing (linear probing)" : " · separate chaining"));
      block.appendChild(title);
      const cells = el("div", "cells");
      slots.forEach((s, i) => {
        const probePos = probe.indexOf(i);
        const cell = el("div", "cell");
        if (probePos !== -1 && probePos === probe.length - 1 && view.hit === i) {
          cell.className = "cell done";
        } else if (probePos !== -1) {
          cell.className = "cell hot";
        } else if (s) {
          cell.className = "cell";
        } else {
          cell.className = "cell empty";
        }
        cell.innerHTML = `<div class="addr">${addr(i, 8)}</div>` +
          `<div class="val">${s ? esc(s.k) + ":" + esc(s.v) : "∅"}</div>` +
          (probePos !== -1 ? `<div class="idx">probe#${probePos + 1}</div>` : `<div class="idx">[${i}]</div>`);
        if (mode === "chaining" && s && s.chain) {
          /* extra chained entries stacked under the bucket */
          const chain = el("div", "cells");
          s.chain.forEach(c => {
            const cc = el("div", "cell");
            cc.innerHTML = `<div class="val" style="font-size:11px">${esc(c.k)}:${esc(c.v)}</div>`;
            chain.appendChild(cc);
          });
          cell.appendChild(chain);
        }
        cells.appendChild(cell);
      });
      block.appendChild(cells);
      if (view.formula) {
        block.appendChild(el("div", "equation", esc(view.formula)));
      }
      return block;
    },

    /* stack: vertical cells with TOP pointer */
    stack(view) {
      const data = view.data || [];
      const top = view.top !== undefined ? view.top : data.length - 1;
      const block = el("div", "mem-block");
      block.appendChild(el("div", "mem-title", esc(view.title || "stack") + " · LIFO"));
      const cols = el("div", "cells");
      for (let i = data.length - 1; i >= 0; i--) {
        const c = el("div", "cell" + (i === top ? " hot" : "") + (data[i] === null ? " empty" : ""));
        c.innerHTML = `<div class="addr">${addr(i, 8)}</div>` +
          `<div class="val">${esc(data[i] === null ? "∅" : data[i])}</div>` +
          (i === top ? `<div class="idx">TOP</div>` : `<div class="idx">[${i}]</div>`);
        cols.appendChild(c);
      }
      block.appendChild(cols);
      return block;
    },

    /* queue: horizontal cells with front/rear markers */
    queue(view) {
      const data = view.data || [];
      const front = view.front, rear = view.rear;
      const block = el("div", "mem-block");
      block.appendChild(el("div", "mem-title", esc(view.title || "queue") + " · FIFO"));
      const cells = el("div", "cells");
      data.forEach((v, i) => {
        const cls = ["cell"];
        if (i === front) cls.push("hot");
        if (i === rear) cls.push("done");
        if (v === null) cls.push("empty");
        const c = el("div", cls.join(" "));
        c.innerHTML = `<div class="addr">${addr(i, 8)}</div>` +
          `<div class="val">${esc(v === null ? "∅" : v)}</div>` +
          `<div class="idx">${i === front ? "FRONT" : i === rear ? "REAR" : "[" + i + "]"}</div>`;
        cells.appendChild(c);
      });
      block.appendChild(cells);
      return block;
    },

    /* linked list: horizontal nodes with → arrows and addresses.
       Each node: { v, next, hl, hot, done }.
       next semantics: null → pointer set to null (end of list);
       a STRING → treated as an explicit target address (use U.addr(i,8)
       of the real target so pointer flips / cycles are visible);
       any other truthy value → default forward pointer. */
    list(view) {
      const nodes = view.nodes || [];
      const block = el("div", "mem-block");
      block.appendChild(el("div", "mem-title", esc(view.title || "linked list") + " · nodes linked by next pointers"));
      const row = el("div", "cells");
      nodes.forEach((n, i) => {
        const c = el("div", "cell" + (n.hl ? " hl" : "") + (n.hot ? " hot" : "") + (n.done ? " done" : ""));
        const nxt = (n.next === null || n.next === undefined) ? "null"
          : (typeof n.next === "string" ? n.next : addr(i + 1, 8));
        c.innerHTML = `<div class="addr">${addr(i, 8)}</div>` +
          `<div class="val">${esc(n.v === null || n.v === undefined ? "∅" : n.v)}</div>` +
          `<div class="idx">next→${nxt}</div>`;
        row.appendChild(c);
        if (i < nodes.length - 1) row.appendChild(el("span", "ptr-svg", " → "));
      });
      block.appendChild(row);
      return block;
    },

    /* binary tree: absolute-positioned recursive layout */
    tree(view) {
      const root = view.root;
      const hl = view.hl || [];
      const block = el("div", "mem-block", "");
      block.appendChild(el("div", "mem-title", esc(view.title || "binary tree") + " · nodes in the heap"));
      const canvas = el("div", "viz", "");
      canvas.style.position = "relative";
      canvas.style.minHeight = "80px";
      canvas.style.margin = "6px";
      const NODE_W = 46, NODE_H = 34, LEVEL_H = 64, SIB_GAP = 26;

      /* layout: returns width of subtree and fills positions */
      function layout(node, depth, x) {
        if (!node) return { w: NODE_W, cx: x + NODE_W / 2, depth };
        const L = layout(node.left, depth + 1, x);
        const R = layout(node.right, depth + 1, x + L.w + SIB_GAP);
        const w = L.w + R.w + SIB_GAP;
        const cx = x + w / 2;
        node._x = cx - NODE_W / 2;
        node._y = depth * LEVEL_H;
        node._cx = cx; node._cy = depth * LEVEL_H + NODE_H / 2;
        return { w, cx, depth: Math.max(L.depth, R.depth) };
      }
      if (root) layout(root, 0, 0);

      /* edges first (SVG lines), then nodes */
      const svgNS = "http://www.w3.org/2000/svg";
      const edges = el("svg", "ptr-svg", "");
      edges.setAttribute("width", "1200");
      edges.setAttribute("height", "600");
      edges.style.position = "absolute";
      edges.style.left = "0";
      edges.style.top = "0";
      edges.style.overflow = "visible";
      canvas.appendChild(edges);
      function drawEdges(node) {
        if (!node) return;
        if (node.left) {
          const l = document.createElementNS(svgNS, "line");
          l.setAttribute("x1", node._cx); l.setAttribute("y1", node._cy);
          l.setAttribute("x2", node.left._cx); l.setAttribute("y2", node.left._cy);
          l.setAttribute("stroke", "#8b949e"); l.setAttribute("stroke-width", "1.5");
          edges.appendChild(l);
          drawEdges(node.left);
        }
        if (node.right) {
          const l = document.createElementNS(svgNS, "line");
          l.setAttribute("x1", node._cx); l.setAttribute("y1", node._cy);
          l.setAttribute("x2", node.right._cx); l.setAttribute("y2", node.right._cy);
          l.setAttribute("stroke", "#8b949e"); l.setAttribute("stroke-width", "1.5");
          edges.appendChild(l);
          drawEdges(node.right);
        }
      }
      drawEdges(root);
      /* node boxes */
      function drawNodes(node) {
        if (!node) return;
        const c = el("div", "cell" + (hl.indexOf(node.id) !== -1 ? " hot" : ""));
        c.style.position = "absolute";
        c.style.left = node._x + "px";
        c.style.top = node._y + "px";
        c.style.minWidth = NODE_W + "px";
        c.innerHTML = `<div class="addr">${addr(node.id || 0, 8)}</div>` +
          `<div class="val">${esc(node.val)}</div>` +
          `<div class="idx">id:${node.id}</div>`;
        canvas.appendChild(c);
        drawNodes(node.left);
        drawNodes(node.right);
      }
      drawNodes(root);
      block.appendChild(canvas);
      return block;
    },

    /* 2D grid (DP tables, sudoku boards) */
    grid(view) {
      const data = view.data || [];
      const cls = view.cls || {};
      const block = el("div", "mem-block");
      block.appendChild(el("div", "mem-title", esc(view.title || "grid") + " · rows are arrays, contiguous in memory"));
      const g = el("div", "grid2d");
      g.style.gridTemplateColumns = "repeat(" + (view.cols || data[0] ? data[0].length : 1) + ", 1fr)";
      data.forEach((row, r) => {
        row.forEach((v, c) => {
          const cell = el("div", "cell" + (cls[r + "," + c] ? " " + cls[r + "," + c] : "") + (v === null || v === undefined ? " empty" : ""));
          cell.innerHTML = `<div class="val">${esc(v === null || v === undefined ? "∅" : v)}</div>` +
            `<div class="idx">[${r}][${c}]</div>`;
          g.appendChild(cell);
        });
      });
      block.appendChild(g);
      return block;
    }
  };

  /* ---------------- StepPlayer ---------------- */
  class StepPlayer {
    constructor() {
      this.steps = [];
      this.i = -1;
      this.timer = null;
      this.ms = 900;
      this.onChange = null;
    }
    load(steps, ms) {
      this.steps = steps;
      this.ms = ms || 900;
      this.stop();
      this.i = 0;
      if (this.onChange) this.onChange(this.i);
    }
    play() {
      this.stop();
      this.timer = setInterval(() => {
        if (this.i >= this.steps.length - 1) { this.stop(); return; }
        this.i++;
        if (this.onChange) this.onChange(this.i);
      }, this.ms);
    }
    stop() { if (this.timer) { clearInterval(this.timer); this.timer = null; } }
    stepF() { if (this.i < this.steps.length - 1) { this.i++; if (this.onChange) this.onChange(this.i); } }
    stepB() { if (this.i > 0) { this.i--; if (this.onChange) this.onChange(this.i); } }
    reset() { this.stop(); this.i = 0; if (this.onChange) this.onChange(this.i); }
    setSpeed(ms) { this.ms = ms; if (this.timer) { this.stop(); this.play(); } }
    atEnd() { return this.steps.length && this.i >= this.steps.length - 1; }
  }

  /* ---------------- page assembly ---------------- */
  const state = { section: null, problems: [], current: null, approach: 0, player: new StepPlayer() };

  function renderNav() {
    const nav = document.getElementById("topnav");
    nav.innerHTML = "";
    nav.appendChild(el("span", "brand", "NeetCode 150 · Interactive"));
    (window.NC150_NAV || []).forEach(s => {
      const a = el("a", s.id === state.section.id ? "active" : "", esc(s.short));
      a.href = s.file;
      nav.appendChild(a);
    });
    const home = el("a", "", "⌂ Home");
    home.href = "../index.html";
    nav.appendChild(home);
  }

  function renderSidebar() {
    const list = document.getElementById("problemList");
    list.innerHTML = "";
    state.problems.forEach(p => {
      const li = el("li");
      const b = el("button", "", "");
      b.innerHTML = `<span class="diff-dot diff-${p.difficulty}"></span>${esc(p.title)}`;
      b.onclick = () => loadProblem(p.id);
      if (p.id === state.current.id) b.classList.add("active");
      li.appendChild(b);
      list.appendChild(li);
    });
  }

  function renderProblem() {
    const p = state.current;
    document.getElementById("problemTitle").innerHTML = `<span class="diff-dot diff-${p.difficulty}"></span> ${esc(p.title)}`;
    document.getElementById("problemSub").innerHTML = `LeetCode <a href="${p.url}" target="_blank">#${p.id}</a> · ${p.difficulty} · tags: ${p.tags.map(t => esc(t)).join(", ")}`;
    /* badges */
    const badges = document.getElementById("badges");
    badges.innerHTML = "";
    p.complexities.forEach((c, i) => {
      if (i === state.approach) {
        badges.appendChild(el("span", "badge time", "⏱ " + esc(c.time)));
        badges.appendChild(el("span", "badge mem", "🧠 " + esc(c.space)));
        if (c.note) badges.appendChild(el("span", "badge opt", esc(c.note)));
      }
    });
    /* input form */
    const form = document.getElementById("inputForm");
    form.innerHTML = "";
    p.inputs.forEach(inp => {
      const fld = el("div", "fld");
      fld.appendChild(el("label", "", esc(inp.label)));
      const tag = inp.type === "list" || inp.type === "str" ? "textarea" : "input";
      const input = el(tag, "", "");
      input.value = inp.default;
      input.dataset.name = inp.name;
      input.dataset.ptype = inp.type;
      fld.appendChild(input);
      form.appendChild(fld);
    });
    /* example chips */
    const tags = document.getElementById("exampleTags");
    tags.innerHTML = "";
    (p.examples || []).forEach((ex, i) => {
      const b = el("button", "", esc(ex.label));
      b.onclick = () => {
        Object.keys(ex.values).forEach(k => {
          const f = form.querySelector(`[data-name="${k}"]`);
          if (f) f.value = ex.values[k];
        });
        run();
      };
      tags.appendChild(b);
    });
    /* static panels */
    document.getElementById("realLife").innerHTML = p.realLife || "";
    document.getElementById("dsDive").innerHTML = p.dsDive || "";
    /* tabs */
    const tabs = document.getElementById("tabs");
    tabs.innerHTML = "";
    (p.approaches || ["Approach 1"]).forEach((name, i) => {
      const b = el("button", i === state.approach ? "active" : "", esc(name));
      b.onclick = () => selectApproach(i);
      tabs.appendChild(b);
    });
    /* code panel: p.code may be ONE array (both approaches share the
       pseudocode) or an ARRAY of arrays (one listing per approach) */
    const codePanel = document.getElementById("codePanel");
    codePanel.innerHTML = "";
    let codeLines = p.code;
    if (Array.isArray(p.code) && Array.isArray(p.code[0])) {
      codeLines = p.code[state.approach] || [];
    }
    codeLines.forEach(line => {
      codePanel.appendChild(el("span", "code-line", esc(line)));
    });
    /* approach compare table */
    const cmp = document.getElementById("approachTable");
    cmp.innerHTML = "";
    if (p.compare) {
      const t = el("table", "compare");
      let html = "<tr><th>Approach</th><th>Technique</th><th>Time</th><th>Space</th><th>Best when</th></tr>";
      p.compare.forEach(r => {
        html += `<tr class="${r.best ? "best" : ""}"><td>${esc(r.name)}</td><td>${esc(r.tech)}</td><td>${esc(r.time)}</td><td>${esc(r.space)}</td><td>${esc(r.when)}</td></tr>`;
      });
      t.innerHTML = html;
      cmp.appendChild(t);
    }
    /* reset viz + controls */
    document.getElementById("resultBox").className = "result-box";
    state.player.onChange = null;
    state.player.load([{ text: "Click ▶ Run to animate. Type your own input above.", code: -1, mem: [] }]);
    renderStep(0);
    bindControls();
  }

  function selectApproach(i) {
    state.approach = i;
    renderProblem();
  }

  /* read current form values into a values map */
  function readValues() {
    const form = document.getElementById("inputForm");
    const vals = {};
    form.querySelectorAll("[data-name]").forEach(f => {
      const t = f.dataset.ptype;
      vals[f.dataset.name] = t === "int" ? parseNum(f.value)
        : t === "pair" ? parsePair(f.value)
        : t === "str" ? parseStr(f.value)
        : parseList(f.value);
    });
    return vals;
  }

  function run() {
    const p = state.current;
    let vals;
    try { vals = readValues(); }
    catch (e) { alert("Could not parse input: " + e.message); return; }
    try {
      const gen = p.steps[state.approach];
      if (!gen) { alert("No animator for this approach yet."); return; }
      const out = gen(vals);
      if (!out.steps) out.steps = [];
      if (out.steps.length === 0) out.steps.push({ text: "No steps to animate.", code: -1, mem: [] });
      /* attach result to final step */
      const last = out.steps[out.steps.length - 1];
      last.result = out.result;
      last.correct = out.correct;
      last.memNote = out.memNote;
      state.player.load(out.steps, 900);
      renderStep(0);
    } catch (e) {
      alert("Animation error: " + e.message);
    }
  }

  function renderStep(i) {
    const st = state.steps()[i];
    if (!st) return;
    document.getElementById("stepText").innerHTML = st.text || "";
    const viz = document.getElementById("memoryView");
    viz.innerHTML = "";
    (st.mem || []).forEach(view => {
      const r = Render[view.type] || Render.array;
      viz.appendChild(r(view));
    });
    /* highlight code line */
    const lines = document.querySelectorAll("#codePanel .code-line");
    lines.forEach((l, li) => {
      l.classList.toggle("cur", li === st.code);
      if (li === st.code && l.scrollIntoView) l.scrollIntoView({ block: "nearest" });
    });
    /* result box */
    const box = document.getElementById("resultBox");
    if (st.result !== undefined) {
      box.className = "result-box show";
      const v = box.querySelector(".res-value");
      v.textContent = "Result: " + st.result;
      v.className = "res-value" + (st.correct === false ? " wrong" : "");
      box.querySelector(".mem-line").textContent = st.memNote || "";
    } else {
      box.className = "result-box";
    }
    document.getElementById("stepCounter").textContent = (i + 1) + " / " + state.steps().length;
    document.getElementById("scrub").max = state.steps().length - 1;
    document.getElementById("scrub").value = i;
    const end = state.player.atEnd();
    document.getElementById("btnPlay").textContent = end ? "↺ Replay" : "▶ Play";
  }

  function bindControls() {
    const play = document.getElementById("btnPlay");
    play.onclick = () => {
      if (state.player.timer || state.player.atEnd()) {
        state.player.reset();
        state.player.play();
      } else {
        state.player.play();
      }
    };
    document.getElementById("btnStep").onclick = () => { state.player.stop(); state.player.stepF(); };
    document.getElementById("btnBack").onclick = () => { state.player.stop(); state.player.stepB(); };
    document.getElementById("btnReset").onclick = () => state.player.reset();
    const speed = document.getElementById("speed");
    speed.oninput = () => state.player.setSpeed(Number(speed.value));
    const scrub = document.getElementById("scrub");
    scrub.oninput = () => { state.player.stop(); const i = Number(scrub.value); state.player.i = i; renderStep(i); };
    document.getElementById("btnRun").onclick = run;
  }

  function loadProblem(id) {
    const p = state.problems.find(x => x.id === id);
    if (!p) return;
    state.current = p;
    state.approach = 0;
    renderSidebar();
    renderProblem();
  }

  /* ---------------- public API ---------------- */
  window.NC150 = {
    register(problem) {
      state.problems.push(problem);
    },
    init(section) {
      state.section = section;
      state.steps = () => (state.player.steps || []);
      if (!state.current) state.current = state.problems[0];
      renderNav();
      renderSidebar();
      renderProblem();
      /* keep player's onChange wired to renderStep */
      state.player.onChange = i => renderStep(i);
    },
    /* helpers exposed to problem step-generators */
    utils: {
      addr, parseList, parseNum, parsePair, ListNode, TreeNode, esc
    }
  };
})();