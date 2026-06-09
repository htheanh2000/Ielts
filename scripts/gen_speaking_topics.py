#!/usr/bin/env python3
"""Generate IELTS Speaking Part 1 topic-card decks.

Output: /speaking/topics/{slug}/index.html for each topic.

Each deck has: 10 questions × 5 slides (Q -> Full -> Hide some -> Hide more -> Recall) = 50 slides.

Markup syntax inside answers:
  ~~text~~  -> hide at level 1 onward (slide 3, 4)
  ==text==  -> hide at level 2 onward (slide 4 only)
  plain     -> shown until level 4 (everything hidden)

Persona "Nhut": 26, Backend Golang dev, lives Saigon, hometown Dong Thap,
likes coffee + travel + casual badminton.
"""

import json
from pathlib import Path

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>IELTS Speaking Part 1 — __TOPIC_TITLE__</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
    background: #f5f5f0;
    background-image:
      linear-gradient(rgba(30,58,138,0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(30,58,138,0.06) 1px, transparent 1px);
    background-size: 40px 40px;
    color: #1a1a1a;
    overflow: hidden;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.06);
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(8px);
  }
  .topic-tag {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #1e3a8a;
  }
  .topic-tag a { color: inherit; text-decoration: none; opacity: 0.7; }
  .topic-tag a:hover { opacity: 1; }
  .counter {
    font-size: 13px;
    color: #6b7280;
    font-variant-numeric: tabular-nums;
  }

  .slide-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
  }
  .card {
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 20px 60px rgba(30,58,138,0.08);
    width: 100%;
    max-width: 960px;
    min-height: 480px;
    padding: 80px 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
  }

  .label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 28px;
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
  }
  .label.q  { background: #fff3e0; color: #c2410c; }
  .label.a  { background: #e0f2fe; color: #1e3a8a; }
  .label.test { background: #fef3c7; color: #92400e; }
  .label.empty { background: #f3f4f6; color: #6b7280; }

  .question {
    font-size: 38px;
    font-weight: 600;
    line-height: 1.35;
    color: #111;
    letter-spacing: -0.5px;
  }
  .answer {
    font-size: 26px;
    line-height: 1.6;
    color: #1f2937;
    font-weight: 400;
  }
  .answer .vocab { background: rgba(30,58,138,0.10); color: #1e3a8a; border-radius: 4px; padding: 1px 3px; font-weight: 600; }
  .answer .keyphrase { background: rgba(194,65,12,0.12); color: #c2410c; border-radius: 4px; padding: 1px 3px; font-weight: 600; }

  .vi-prompt {
    margin-top: 34px;
    padding: 22px 26px;
    background: #fff7ed;
    border-left: 4px solid #c2410c;
    border-radius: 0 12px 12px 0;
  }
  .vi-prompt .vi-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #c2410c; margin-bottom: 10px;
  }
  .vi-prompt .vi-text { font-size: 22px; line-height: 1.55; color: #1f2937; font-weight: 500; }
  .model-hint { margin-top: 22px; font-size: 14px; color: #9ca3af; font-style: italic; }

  .word { transition: color 0.12s, background 0.12s; border-radius: 3px; cursor: pointer; }
  .word:hover { background: rgba(59, 130, 246, 0.12); border-radius: 3px; }
  .word.looked-up { text-decoration: underline dotted #1d4ed8; text-underline-offset: 4px; }

  .trans-popup {
    position: absolute;
    background: #111827;
    color: #fff;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 14px;
    z-index: 100;
    box-shadow: 0 12px 32px rgba(0,0,0,0.25);
    min-width: 180px;
    max-width: 360px;
    animation: trans-pop 0.18s ease-out;
  }
  @keyframes trans-pop {
    from { opacity: 0; transform: translateY(-4px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }
  .trans-popup .trans-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 6px;
  }
  .trans-popup .trans-en {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #93c5fd;
  }
  .trans-popup .word-play-btn {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(147, 197, 253, 0.18);
    color: #93c5fd;
    border: none;
    cursor: pointer;
    font-size: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.12s;
    font-family: inherit;
    padding: 0;
    flex-shrink: 0;
  }
  .trans-popup .word-play-btn:hover { background: rgba(147, 197, 253, 0.32); color: #fff; transform: scale(1.05); }
  .trans-popup .word-play-btn.playing { background: #c2410c; color: #fff; }
  .trans-popup .trans-phonetic {
    font-size: 13px;
    color: #d1d5db;
    font-family: 'Charter', 'Cambria', Georgia, serif;
    font-style: italic;
    margin-bottom: 8px;
  }
  .trans-popup .trans-phonetic:empty { display: none; }
  .trans-popup .trans-vi {
    font-size: 17px;
    line-height: 1.4;
    font-weight: 500;
  }
  .trans-popup .trans-vi.loading { opacity: 0.55; font-style: italic; font-weight: 400; }
  .trans-popup .trans-vi a { color: #93c5fd; text-decoration: underline; }
  .trans-popup .trans-syn {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 13px;
    color: #d1d5db;
    line-height: 1.5;
  }
  .trans-popup .trans-syn:empty { display: none; }
  .trans-popup .trans-syn-label {
    display: inline-block;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.3px;
    color: #6b7280;
    margin-right: 6px;
  }
  .trans-popup .trans-meta {
    margin-top: 8px;
    font-size: 11px;
    color: #9ca3af;
    display: flex;
    gap: 12px;
  }
  .trans-popup .trans-meta a { color: #9ca3af; text-decoration: none; }
  .trans-popup .trans-meta a:hover { color: #93c5fd; }
  .trans-popup::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 24px;
    border: 6px solid transparent;
    border-bottom-color: #111827;
    border-top: 0;
  }

  .progress {
    position: absolute;
    bottom: 24px;
    left: 80px;
    right: 80px;
    height: 4px;
    background: #f3f4f6;
    border-radius: 2px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: #1e3a8a;
    transition: width 0.3s ease;
  }

  footer {
    padding: 16px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #6b7280;
  }
  .nav-hint kbd {
    background: #fff;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    padding: 2px 6px;
    font-family: inherit;
    font-size: 11px;
    margin: 0 2px;
  }
  .nav-buttons button {
    background: #fff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 6px 14px;
    cursor: pointer;
    font-size: 13px;
    margin-left: 8px;
    transition: all 0.15s;
  }
  .nav-buttons button:hover { background: #1e3a8a; color: #fff; border-color: #1e3a8a; }

  .level-indicator {
    position: absolute;
    top: 24px;
    right: 80px;
    font-size: 11px;
    color: #9ca3af;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .header-right { display: flex; align-items: center; gap: 16px; }
  .hint-btn {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fff7ed; color: #c2410c; border: 1px solid #f0c9a8;
    border-radius: 999px; padding: 6px 14px; font-size: 13px; font-weight: 600;
    cursor: pointer; font-family: inherit; transition: all 0.15s;
  }
  .hint-btn:hover { background: #ffedd5; border-color: #c2410c; }
  .hint-btn.active { background: #c2410c; color: #fff; border-color: #c2410c; }

  #hint-drawer {
    position: fixed; top: 0; right: 0; height: 100%;
    width: var(--hint-w, 380px);
    background: #ffffff; border-left: 1px solid #e5e7eb;
    box-shadow: -16px 0 48px rgba(30,58,138,0.12);
    transform: translateX(100%); transition: transform 0.22s ease;
    z-index: 200; display: flex;
  }
  #hint-drawer.open { transform: translateX(0); }
  #hint-resize {
    width: 8px; flex: none; cursor: col-resize;
    background: linear-gradient(to right, transparent, rgba(30,58,138,0.05));
    border-right: 1px solid #eef0f4;
  }
  #hint-resize:hover { background: rgba(30,58,138,0.12); }
  .hint-inner { flex: 1; overflow-y: auto; padding: 28px 30px 48px; }
  .hint-head {
    display: flex; align-items: center; justify-content: space-between;
    font-size: 15px; font-weight: 700; color: #1e3a8a; margin-bottom: 24px; letter-spacing: 0.3px;
  }
  .hint-close {
    border: none; background: #f3f4f6; color: #6b7280; cursor: pointer;
    width: 28px; height: 28px; border-radius: 50%; font-size: 13px; font-family: inherit;
  }
  .hint-close:hover { background: #e5e7eb; color: #1e3a8a; }
  .hint-section { }
  .hint-section .hint-label {
    font-size: 11px; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase;
    color: #c2410c; margin-bottom: 12px;
  }
  .hint-section ul { margin: 0; padding-left: 18px; }
  .hint-section li { font-size: 16px; line-height: 1.9; color: #1f2937; }
  .hint-section .hint-sub { font-size: 12px; font-weight: 600; color: #6b7280; margin-top: 12px; margin-bottom: 2px; }
  .hint-section p { margin: 0; font-size: 15px; line-height: 1.6; color: #1e3a8a; font-weight: 500; }
  .hint-divider { height: 1px; background: #e5e7eb; margin: 24px 0; }
</style>
</head>
<body>

<header>
  <div class="topic-tag"><a href="/">← Decks</a> &nbsp;·&nbsp; <span id="topic-name">Topic __TOPIC_NUM__ · __TOPIC_TITLE__</span></div>
  <div class="header-right">
    <button class="hint-btn" id="hint-btn" onclick="toggleHint()" title="Mẹo trả lời">💡 <span>Mẹo trả lời</span></button>
    <div class="counter" id="counter">1 / 50</div>
  </div>
</header>

<div class="slide-container">
  <div class="card" id="card">
    <!-- slide rendered here -->
  </div>
</div>

<aside id="hint-drawer">
  <div id="hint-resize" title="Kéo để chỉnh độ rộng"></div>
  <div class="hint-inner">
    <div class="hint-head">
      <span>💡 Mẹo trả lời</span>
      <button class="hint-close" onclick="closeHint()" title="Đóng">✕</button>
    </div>
    <div class="hint-section">
      <div class="hint-label">Câu mở đầu</div>
      <ul>
        <li>Well, I'd say…</li>
        <li>To be honest,…</li>
        <li>Actually,…</li>
        <li>For me, personally,…</li>
        <li>That's a good question — I think…</li>
        <li>Hmm, let me think…</li>
      </ul>
    </div>
    <div class="hint-divider"></div>
    <div class="hint-section">
      <div class="hint-label">Linking words</div>
      <div class="hint-sub">Thêm ý</div><p>also · on top of that · what's more · besides</p>
      <div class="hint-sub">Tương phản</div><p>however · although · on the other hand · that said</p>
      <div class="hint-sub">Nhân–quả</div><p>because · so · that's why · as a result</p>
      <div class="hint-sub">Ví dụ</div><p>for example · for instance · such as · like</p>
      <div class="hint-sub">Trình tự</div><p>first of all · then · after that · eventually</p>
    </div>
    <div class="hint-divider"></div>
    <div class="hint-section">
      <div class="hint-label">Kéo dài câu trả lời</div>
      <ul>
        <li>Nêu lý do — because…</li>
        <li>Cho ví dụ cụ thể — for example…</li>
        <li>So sánh xưa và nay</li>
        <li>Thêm cảm xúc / quan điểm — I feel that…</li>
      </ul>
    </div>
  </div>
</aside>

<footer>
  <div class="nav-hint">
    <kbd>←</kbd> <kbd>→</kbd> chuyển slide ·
    <kbd>Space</kbd> next ·
    <kbd>Home</kbd> đầu ·
    <kbd>End</kbd> cuối
  </div>
  <div class="nav-buttons">
    <button onclick="prev()">← Prev</button>
    <button onclick="next()">Next →</button>
  </div>
</footer>

<script>
const TOPIC_NUM = __TOPIC_NUM__;
const TOPIC = "__TOPIC_TITLE__";


const QUESTIONS = __QUESTIONS_JSON__;

const slides = [];
QUESTIONS.forEach((item, qi) => {
  slides.push({ qIndex: qi, kind: 'q' });
  slides.push({ qIndex: qi, kind: 'model' });
});

let cursor = 0;

const NBSP_CHAR = ' ';
function escAttr(s) { return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
function stripMarkup(s) { return s.replace(/~~(.*?)~~/g, '$1').replace(/==(.*?)==/g, '$1'); }

let __wordIdx = 0;
function emitToken(tok, hideAtLevel, currentLevel) {
  if (/^\s+$/.test(tok) || !tok) return tok;
  const m = tok.match(/^([^\w]*)([\w'-]+)([^\w]*)$/);
  if (!m) return tok;
  const [, pre, word, post] = m;
  const idx = __wordIdx++;
  const hl = hideAtLevel === 1 ? ' vocab' : hideAtLevel === 2 ? ' keyphrase' : '';
  return pre + `<span class="word${hl}" data-idx="${idx}">${word}</span>` + post;
}

function parseSegments(raw) {
  const segs = [];
  let pos = 0;
  const re = /(~~([\s\S]*?)~~|==([\s\S]*?)==)/g;
  let m;
  while ((m = re.exec(raw)) !== null) {
    if (m.index > pos) segs.push({ text: raw.slice(pos, m.index), hide: 0 });
    if (m[2] !== undefined) segs.push({ text: m[2], hide: 1 });
    else segs.push({ text: m[3], hide: 2 });
    pos = m.index + m[0].length;
  }
  if (pos < raw.length) segs.push({ text: raw.slice(pos), hide: 0 });
  return segs;
}

function renderAnswer(raw, level) {
  if (level === 4) return null;
  __wordIdx = 0;
  const segs = parseSegments(raw);
  let html = '';
  for (const seg of segs) {
    const tokens = seg.text.split(/(\s+)/);
    for (const tok of tokens) html += emitToken(tok, seg.hide, level);
  }
  return html;
}

function renderQuestion(raw) {
  __wordIdx = 0;
  let html = '';
  const tokens = raw.split(/(\s+)/);
  for (const tok of tokens) html += emitToken(tok, 0, 0);
  return html;
}


document.addEventListener('click', (e) => {
  // Close translation popup if click outside
  if (!e.target.closest('.trans-popup, .word')) closeTranslation();

  // Close hint drawer if click outside it and outside its toggle button
  if (hintOpen && !e.target.closest('#hint-drawer, .hint-btn')) closeHint();

  // Word click → translate.
  const wordEl = e.target.closest('.word');
  if (wordEl && !e.target.closest('.trans-popup')) {
    showTranslation(wordEl);
  }
});

// --- Translation + Dictionary lookup ---
const __transCache = JSON.parse(localStorage.getItem('ielts_trans_cache') || '{}');
const __dictCache = JSON.parse(localStorage.getItem('ielts_dict_cache') || '{}');

async function lookupDict(word) {
  if (__dictCache[word]) return __dictCache[word]._miss ? null : __dictCache[word];
  try {
    const r = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`);
    if (!r.ok) {
      __dictCache[word] = { _miss: true };
      return null;
    }
    const data = await r.json();
    if (!Array.isArray(data) || !data[0]) return null;
    const entry = data[0];
    let phonetic = entry.phonetic || '';
    let audio = '';
    for (const p of (entry.phonetics || [])) {
      if (!phonetic && p.text) phonetic = p.text;
      if (!audio && p.audio) audio = p.audio;
    }
    const synonyms = [];
    for (const m of (entry.meanings || [])) {
      for (const s of (m.synonyms || [])) {
        if (synonyms.length < 6 && !synonyms.includes(s)) synonyms.push(s);
      }
      for (const d of (m.definitions || [])) {
        for (const s of (d.synonyms || [])) {
          if (synonyms.length < 6 && !synonyms.includes(s)) synonyms.push(s);
        }
      }
    }
    const result = { phonetic, audio, synonyms };
    __dictCache[word] = result;
    const keys = Object.keys(__dictCache);
    if (keys.length > 500) {
      const drop = keys.slice(0, keys.length - 500);
      for (const k of drop) delete __dictCache[k];
    }
    localStorage.setItem('ielts_dict_cache', JSON.stringify(__dictCache));
    return result;
  } catch (e) {
    return null;
  }
}

let __wordAudio = null;
let __wordBtn = null;
let __wordMode = null; // 'audio' | 'tts'

function setWordBtnIcon(btn, state) {
  // state: 'idle' | 'playing' | 'paused'
  btn.textContent = state === 'playing' ? '⏸' : '▶';
  btn.classList.toggle('playing', state === 'playing');
  btn.classList.toggle('paused', state === 'paused');
}

function stopWordPlay() {
  if (__wordAudio) { try { __wordAudio.pause(); } catch(e){} __wordAudio = null; }
  if (window.speechSynthesis) speechSynthesis.cancel();
  if (__wordBtn) setWordBtnIcon(__wordBtn, 'idle');
  __wordBtn = null;
  __wordMode = null;
}

function playWord(btn) {
  // Same button clicked while playing/paused → toggle
  if (__wordBtn === btn) {
    if (__wordMode === 'audio' && __wordAudio) {
      if (__wordAudio.paused) { __wordAudio.play(); setWordBtnIcon(btn, 'playing'); }
      else { __wordAudio.pause(); setWordBtnIcon(btn, 'paused'); }
      return;
    }
    if (__wordMode === 'tts') {
      if (speechSynthesis.paused) { speechSynthesis.resume(); setWordBtnIcon(btn, 'playing'); }
      else if (speechSynthesis.speaking) { speechSynthesis.pause(); setWordBtnIcon(btn, 'paused'); }
      else { stopWordPlay(); playWord(btn); }
      return;
    }
  }
  // New play (different btn or first time)
  stopWordPlay();
  const word = btn.dataset.word;
  const audioUrl = btn.dataset.audio;
  __wordBtn = btn;
  setWordBtnIcon(btn, 'playing');
  if (audioUrl) {
    __wordMode = 'audio';
    __wordAudio = new Audio(audioUrl);
    __wordAudio.addEventListener('ended', () => { setWordBtnIcon(btn, 'idle'); __wordBtn = null; __wordMode = null; });
    __wordAudio.addEventListener('error', () => { __wordMode = 'tts'; speakWord(word, btn); });
    __wordAudio.play().catch(() => { __wordMode = 'tts'; speakWord(word, btn); });
  } else {
    __wordMode = 'tts';
    speakWord(word, btn);
  }
}

function speakWord(word, btn) {
  if (!('speechSynthesis' in window)) { setWordBtnIcon(btn, 'idle'); return; }
  const u = new SpeechSynthesisUtterance(word);
  u.lang = 'en-GB';
  u.rate = 0.85;
  const voices = speechSynthesis.getVoices();
  const ukVoice = voices.find(v => v.lang && v.lang.startsWith('en-GB')) ||
                  voices.find(v => v.lang && v.lang.startsWith('en'));
  if (ukVoice) u.voice = ukVoice;
  u.onend = () => { setWordBtnIcon(btn, 'idle'); __wordBtn = null; __wordMode = null; };
  u.onerror = () => { setWordBtnIcon(btn, 'idle'); __wordBtn = null; __wordMode = null; };
  speechSynthesis.speak(u);
}

function getWordText(el) {
  return (el.dataset.word || el.textContent || '').trim().replace(/[^\w'-]/g, '').toLowerCase();
}

async function translateWord(word) {
  if (__transCache[word]) return __transCache[word];
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=${encodeURIComponent(word)}`;
    const r = await fetch(url);
    if (!r.ok) throw new Error('http ' + r.status);
    const data = await r.json();
    let trans = '';
    if (Array.isArray(data) && Array.isArray(data[0])) {
      trans = data[0].map(seg => Array.isArray(seg) ? (seg[0] || '') : '').join('').trim();
    }
    if (trans) {
      __transCache[word] = trans;
      // cap cache size to ~500 entries
      const keys = Object.keys(__transCache);
      if (keys.length > 500) {
        const drop = keys.slice(0, keys.length - 500);
        for (const k of drop) delete __transCache[k];
      }
      localStorage.setItem('ielts_trans_cache', JSON.stringify(__transCache));
    }
    return trans;
  } catch (e) {
    return null;
  }
}

function closeTranslation() {
  stopWordPlay();
  document.querySelectorAll('.trans-popup').forEach(p => p.remove());
}

function positionPopup(popup, target) {
  const r = target.getBoundingClientRect();
  popup.style.top = `${r.bottom + window.scrollY + 10}px`;
  popup.style.left = `${Math.max(8, r.left + window.scrollX - 8)}px`;
  // Clamp inside viewport horizontally
  const pr = popup.getBoundingClientRect();
  if (pr.right > window.innerWidth - 8) {
    popup.style.left = `${window.innerWidth - pr.width - 8}px`;
  }
}

function showTranslation(targetEl) {
  closeTranslation();
  const word = getWordText(targetEl);
  if (!word) return;
  targetEl.classList.add('looked-up');

  const popup = document.createElement('div');
  popup.className = 'trans-popup';
  popup.innerHTML = `
    <div class="trans-header">
      <div class="trans-en">${word}</div>
      <button class="word-play-btn" data-word="${word}" data-audio="" onclick="playWord(this)" title="Play pronunciation">▶</button>
    </div>
    <div class="trans-phonetic"></div>
    <div class="trans-vi loading">Đang tra…</div>
    <div class="trans-syn"></div>
    <div class="trans-meta">
      <a href="https://translate.google.com/?sl=en&tl=vi&text=${encodeURIComponent(word)}" target="_blank" rel="noopener">Google Translate ↗</a>
    </div>
  `;
  document.body.appendChild(popup);
  positionPopup(popup, targetEl);

  // Translation (parallel fetch)
  translateWord(word).then(trans => {
    const viEl = popup.querySelector('.trans-vi');
    if (!viEl) return;
    viEl.classList.remove('loading');
    if (trans) viEl.textContent = trans;
    else viEl.innerHTML = `<span style="opacity:0.7">Không tra được — </span><a href="https://translate.google.com/?sl=en&tl=vi&text=${encodeURIComponent(word)}" target="_blank" rel="noopener">tra trên Google ↗</a>`;
  });

  // Dictionary (parallel fetch)
  lookupDict(word).then(dict => {
    if (!dict) return;
    const phEl = popup.querySelector('.trans-phonetic');
    if (phEl && dict.phonetic) phEl.textContent = dict.phonetic;
    if (dict.audio) {
      const btn = popup.querySelector('.word-play-btn');
      if (btn) btn.dataset.audio = dict.audio;
    }
    if (dict.synonyms && dict.synonyms.length) {
      const synEl = popup.querySelector('.trans-syn');
      if (synEl) {
        synEl.innerHTML = `<span class="trans-syn-label">SYNONYMS</span>${dict.synonyms.slice(0, 5).join(', ')}`;
      }
    }
    // Re-position because content height likely changed
    positionPopup(popup, targetEl);
  });
}

function render() {
  closeTranslation();
  const slide = slides[cursor];
  const item = QUESTIONS[slide.qIndex];
  const card = document.getElementById('card');
  document.getElementById('counter').textContent = `${cursor + 1} / ${slides.length}`;
  document.getElementById('topic-name').textContent = `Topic ${TOPIC_NUM} · ${TOPIC} · Q${slide.qIndex + 1}`;

  const qNum = slide.qIndex + 1;
  let html = '';

  if (slide.kind === 'q') {
    html = `
      <div class="level-indicator">Question</div>
      <span class="label q">Question ${qNum}</span>
      <div class="question">${renderQuestion(item.q)}</div>
      <div class="vi-prompt">
        <div class="vi-label">Gợi ý — dịch sang English</div>
        <div class="vi-text">${item.vi}</div>
      </div>
    `;
  } else {
    html = `
      <div class="level-indicator">Đáp án mẫu · English</div>
      <span class="label a">Answer ${qNum} · Model</span>
      <div class="answer">${renderAnswer(item.a, 1)}</div>
      <div class="model-hint">Đối chiếu với bản dịch của bạn · bấm vào từ để tra nghĩa.</div>
    `;
  }

  const progressPct = ((cursor + 1) / slides.length) * 100;
  html += `<div class="progress"><div class="progress-fill" style="width:${progressPct}%"></div></div>`;

  card.innerHTML = html;
}

function next() { if (cursor < slides.length - 1) { cursor++; render(); } }
function prev() { if (cursor > 0) { cursor--; render(); } }

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
  else if (e.key === 'Home') { cursor = 0; render(); }
  else if (e.key === 'End') { cursor = slides.length - 1; render(); }
  else if (e.key === 'Escape') { closeTranslation(); closeHint(); }
});

// --- Hint drawer (shared answer template) ---
let hintOpen = false;
function openHint() {
  const d = document.getElementById('hint-drawer'); if (d) d.classList.add('open');
  const b = document.getElementById('hint-btn'); if (b) b.classList.add('active');
  hintOpen = true;
}
function closeHint() {
  const d = document.getElementById('hint-drawer'); if (d) d.classList.remove('open');
  const b = document.getElementById('hint-btn'); if (b) b.classList.remove('active');
  hintOpen = false;
}
function toggleHint() { hintOpen ? closeHint() : openHint(); }

(function initHintResize() {
  const saved = parseInt(localStorage.getItem('ielts_hint_w') || '0', 10);
  if (saved >= 300 && saved <= 680) document.documentElement.style.setProperty('--hint-w', saved + 'px');
  const handle = document.getElementById('hint-resize');
  if (!handle) return;
  let dragging = false;
  handle.addEventListener('mousedown', (e) => { dragging = true; e.preventDefault(); document.body.style.userSelect = 'none'; });
  window.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    let w = window.innerWidth - e.clientX;
    w = Math.max(300, Math.min(680, w));
    document.documentElement.style.setProperty('--hint-w', w + 'px');
  });
  window.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    document.body.style.userSelect = '';
    const px = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hint-w'), 10);
    if (px) localStorage.setItem('ielts_hint_w', String(px));
  });
})();

render();
</script>

</body>
</html>
"""

TOPICS = [
    {"n": 1, "slug": "hometown", "title": "Hometown", "questions": [
        {"q": "Where is your hometown?",
         "vi": "Quê mình ở Đồng Tháp, một tỉnh nhỏ thuộc vùng Đồng bằng sông Cửu Long ở miền Nam Việt Nam. Từ đó lên Thành phố Hồ Chí Minh đi xe khoảng ba tiếng, hiện mình đang sống và làm backend developer ở Sài Gòn.",
         "a": "My hometown is ~~Dong Thap~~, a ~~small province~~ in the ~~Mekong Delta~~ region of ~~southern Vietnam~~. It's about a ==three-hour drive== from ~~Ho Chi Minh City~~, where I currently ==live and work== as a ~~backend developer~~."},
        {"q": "What's your hometown like?",
         "vi": "Đó là một vùng quê yên tĩnh, xung quanh toàn ruộng lúa, ao sen và sông nước. Nhịp sống chậm hơn Sài Gòn nhiều, người dân thân thiện, đồ ăn tươi, buổi sáng nghe tiếng chim hót chứ không phải tiếng xe máy.",
         "a": "It's a ~~quiet, rural area~~ surrounded by ~~rice fields~~, ~~lotus ponds~~, and ~~rivers~~. The ==pace of life== is ~~super slow~~ compared to ~~Saigon~~ — people are ~~friendly~~, the food is ~~fresh~~, and you can hear ~~birds~~ in the morning instead of ~~motorbikes~~."},
        {"q": "Is your hometown a popular place?",
         "vi": "Cũng không hẳn, quê mình không phải điểm du lịch lớn. Nhưng Sa Đéc, một làng hoa ở tỉnh mình, thì khá đông khách vào dịp Tết để xem mùa hoa. Đa số người ngoài tỉnh thậm chí còn chưa nghe tới Đồng Tháp.",
         "a": "Not really, it's not a ~~major tourist destination~~. But ~~Sa Dec~~ — a ~~flower village~~ in my province — gets a ==fair number== of visitors during ~~Tet~~ for the ~~flower season~~. Most outsiders haven't really ==heard of== ~~Dong Thap~~."},
        {"q": "Do you like your hometown?",
         "vi": "Có chứ, mình thích lắm. Đồ ăn ngon tuyệt, nhất là hủ tiếu Sa Đéc, và mình mê cái cảm giác bình yên ở đó. Mỗi khi Sài Gòn làm mình thấy quá tải, về quê một cuối tuần là nạp lại năng lượng hoàn toàn.",
         "a": "Yeah, I really do. The food is ~~incredible~~ — especially ~~hu tieu Sa Dec~~ — and I love how ~~peaceful~~ it feels. Whenever ~~Saigon~~ gets too ~~overwhelming~~, going home for a ==weekend== ~~recharges~~ me completely."},
        {"q": "Has your hometown changed much in recent years?",
         "vi": "Có thay đổi chút ít, nhưng không nhiều. Đường mới giúp đi lại dễ hơn, vài quán cà phê mới mở trong thị trấn. Nhưng cái chất quê, chậm rãi, nông nghiệp, thì gần như vẫn vậy. Thật ra mình thấy đó là điều tốt.",
         "a": "A bit, but not ~~dramatically~~. ~~New roads~~ make travel ~~easier~~, and a few ~~coffee shops~~ have opened up in town. But the core feel — ~~rural, slow, agricultural~~ — has stayed ==pretty much the same==. Honestly I think that's a ~~good thing~~."},
        {"q": "What do you like most about your hometown?",
         "vi": "Thành thật mà nói, mình thích nhất là đồ ăn và sự yên tĩnh. Mình có thể dậy, làm một ly cà phê phin ở quán ven sông, rồi ngồi ngắm ghe thuyền qua lại hàng giờ. Cái tĩnh lặng đó ở Sài Gòn không tìm đâu ra.",
         "a": "==Honestly==, the ~~food and the quietness~~. I can wake up, grab a ~~Vietnamese drip coffee~~ at a ~~riverside cafe~~, and just ~~watch boats~~ pass by for hours. That kind of ~~stillness~~ is ==impossible to find== in ~~Saigon~~."},
        {"q": "Is there anything you don't like about it?",
         "vi": "Về mặt sự nghiệp thì hơi khó. Ở đó không có nhiều việc liên quan công nghệ, mình làm backend Golang nên buộc phải lên Sài Gòn. Với lại cái nóng mùa hè ở miền Tây cũng khá gắt.",
         "a": "Career-wise, it's ~~tough~~. There aren't many ~~tech jobs~~ in the area — I work as a ~~backend Golang developer~~, so I had to ~~move to Saigon~~. Also, the ~~summer heat~~ in the ~~Mekong~~ can be ==pretty intense==."},
        {"q": "Would you like to live there in the future?",
         "vi": "Có thể về lâu dài. Bây giờ mình cần ở Sài Gòn vì công việc, nhưng khi nào ổn định hơn hoặc làm việc từ xa toàn thời gian, mình rất muốn về lại. Chất lượng sống ở quê khó nơi nào bì được.",
         "a": "Maybe in the ~~long run~~. Right now I need to be in ~~Saigon~~ for my ~~career~~, but once I'm more ~~established~~ or working ~~remotely~~ full-time, I'd love to ~~move back~~. The ~~quality of life~~ there is ==hard to beat==."},
        {"q": "What's the best thing about living there?",
         "vi": "Với mình, đó là chi phí sinh hoạt rẻ và mọi người sống gần nhau. Cả gia đình mình ở trong bán kính vài cây số, đồ ăn rẻ bèo, gần như không kẹt xe. Cuộc sống đơn giản hơn nhiều.",
         "a": "For me, it's the ~~cost of living~~ and how ~~close everyone~~ is. My whole ~~family~~ lives within a ~~few kilometers~~, food is ~~dirt cheap~~, and there's almost no ~~traffic~~. Life is just ==a lot simpler==."},
        {"q": "How long have you lived there?",
         "vi": "Mình lớn lên ở đó tới năm 18 tuổi, nên tổng cộng khoảng 18 năm. Học xong cấp ba thì mình lên Sài Gòn học đại học và ở đó từ đó tới giờ, nhưng vẫn về quê hai ba lần mỗi năm.",
         "a": "I grew up there until I was ~~18~~, so about ~~18 years~~ in total. After ~~high school~~ I moved to ~~Saigon~~ for ~~university~~, and I've been ==based== there ever since — but I still go back ~~two or three times a year~~."},
    ]},

    {"n": 2, "slug": "work", "title": "Work", "questions": [
        {"q": "What do you do?",
         "vi": "Mình làm backend developer ở một công ty công nghệ tại Sài Gòn. Cụ thể là mình viết code bằng Go, hay còn gọi là Golang, xây dựng các API và service chạy nền cho web và ứng dụng di động.",
         "a": "I work as a ~~backend developer~~ at a ~~tech company~~ in ~~Saigon~~. Specifically, I write code in ~~Go — or Golang~~, building ~~APIs and services~~ that ==power web and mobile apps==."},
        {"q": "Why did you choose that job?",
         "vi": "Thật ra mình luôn thích giải quyết vấn đề và xây dựng mọi thứ từ con số không. Backend giống như buồng máy của sản phẩm, vô hình nhưng cực kỳ quan trọng. Với lại lương trong ngành công nghệ ở Việt Nam cũng khá ổn.",
         "a": "Honestly, I've always loved ~~problem-solving~~ and ~~building things from scratch~~. ~~Backend~~ feels like the ~~engine room~~ of any product — ~~invisible but critical~~. Also, the ~~pay~~ in ==Vietnam's tech industry== is pretty solid."},
        {"q": "Do you like your job?",
         "vi": "Ừ, đa số ngày mình thấy thích công việc. Lúc nào cũng có cái mới để học, một framework mới, một con bug khó, hay một hệ thống cần tối ưu. Mấy ngày tệ thường là khi họp hành ngốn hết thời gian code.",
         "a": "Yeah, most days I really enjoy it. There's always something ~~new to learn~~ — a ~~new framework~~, a ~~tricky bug~~, or a ~~system to optimize~~. The ~~bad days~~ are usually when ==meetings eat up== all my ~~coding time~~."},
        {"q": "What's a typical day like at work?",
         "vi": "Mình thường bắt đầu khoảng 9 giờ với buổi họp stand-up, rồi dành phần lớn buổi sáng để code. Buổi chiều thường là review code hoặc debug. Mình cố xong việc trước 6 giờ để đi ăn tối và thư giãn.",
         "a": "I usually start around ~~9 with a stand-up meeting~~, then I spend most of the morning ~~coding~~. Afternoons are often for ~~code reviews~~ or ~~debugging~~. I try to ==wrap up by 6== so I can grab ~~dinner~~ and relax."},
        {"q": "Do you work with a team or alone?",
         "vi": "Chủ yếu làm theo nhóm. Nhóm mình có khoảng sáu engineer, cộng thêm một product manager và một designer. Cả ngày tụi mình trao đổi qua Slack và GitHub, nên làm việc từ xa khá trơn tru.",
         "a": "Mostly with a team. There are about ~~six engineers~~ on my squad, plus a ~~product manager~~ and a ~~designer~~. We collaborate on ~~Slack and GitHub~~ all day, which makes ==remote work pretty smooth==."},
        {"q": "What's the best thing about your job?",
         "vi": "Chắc là sự linh hoạt. Miễn mình giao việc đúng hạn thì không ai quản lý vặt mình làm thế nào hay ở đâu. Mình có thể ăn trưa lâu một chút để đi cà phê, hoặc ngồi làm ở quán, kiểu tự do đó với mình rất quý.",
         "a": "Probably the ~~flexibility~~. As long as I ~~deliver on time~~, no one ~~micromanages~~ how or where I work. I can take a ~~long lunch~~ for ~~coffee~~ or ~~work from a cafe~~ — that ==kind of freedom== matters a lot."},
        {"q": "Is there anything you don't like about it?",
         "vi": "Đôi khi deadline khá khắc nghiệt, nhất là trước khi ra mắt sản phẩm. Với lại ngồi trước màn hình chín tiếng liên tục cũng hại mắt và lưng.",
         "a": "Sometimes the ~~deadlines~~ can be ~~brutal~~, especially before a ~~product launch~~. Also, sitting in front of a ~~screen~~ for ~~nine hours straight~~ is ==rough on== the ~~eyes and the back~~."},
        {"q": "Do you plan to stay in this field?",
         "vi": "Ừ, chắc chắn rồi. Công nghệ thay đổi nhanh đến mức ngay trong mảng backend cũng có vô vàn chỗ để phát triển, như thiết kế hệ thống ở quy mô lớn hay chuyển sang mảng hạ tầng. Mình thấy mình gắn bó với ngành này lâu dài.",
         "a": "Yeah, definitely. ~~Tech moves so fast~~ that even within ~~backend~~ there's ~~endless room to grow~~ — like ~~system design at scale~~ or moving into ~~infrastructure~~. I see myself in this field for ==the long haul==."},
        {"q": "What skills do you need for your job?",
         "vi": "Tư duy logic tốt là điều hiển nhiên, nhưng kỹ năng giao tiếp cũng quan trọng không kém. Mình phải giải thích các quyết định kỹ thuật cho người không rành kỹ thuật mà không tỏ ra kẻ cả. Ngoài ra tiếng Anh là bắt buộc.",
         "a": "~~Strong logical thinking~~ is the obvious one, but ~~communication~~ matters just as much. You have to ~~explain technical decisions~~ to ~~non-technical people~~ without ==sounding condescending==. Also, ~~English~~ is essential."},
        {"q": "Did you study something related to your current job?",
         "vi": "Có, mình học chuyên ngành Khoa học Máy tính ở một trường đại học tại Sài Gòn. Phần lý thuyết như thuật toán và cấu trúc dữ liệu thì hữu ích, nhưng thật ra phần lớn kỹ năng thực tế mình học được qua các dự án cá nhân và khóa học online.",
         "a": "Yes, I majored in ~~Computer Science~~ at ~~university in Saigon~~. The theoretical stuff — ~~algorithms and data structures~~ — was useful, but honestly I learned most ~~practical skills~~ through ==side projects and online courses==."},
    ]},

    {"n": 3, "slug": "hobbies", "title": "Hobbies", "questions": [
        {"q": "What do you do in your free time?",
         "vi": "Tùy ngày. Ngày thường thì mình thư giãn với một ly cà phê và một cuốn sách. Cuối tuần thì hoặc đi đánh cầu lông với bạn bè, hoặc đi mấy chuyến ngắn ra ngoài thành phố.",
         "a": "It depends on the day. On ~~weekdays~~, I usually wind down with a ~~quiet coffee and a book~~. On ~~weekends~~, I either go out for ~~badminton with friends~~ or take ~~short trips~~ ==somewhere outside the city==."},
        {"q": "Do you have any hobbies?",
         "vi": "Có vài cái. Mình mê cà phê đặc sản, kiểu thử các loại hạt khác nhau và tự pha ở nhà. Mình cũng chơi cầu lông cho vui, và đi du lịch mỗi khi dành dụm đủ ngày phép.",
         "a": "Yeah, a few. I'm really into ~~specialty coffee~~ — like ~~trying different beans~~ and ~~brewing methods at home~~. I also play ~~badminton casually~~, and ~~travel~~ whenever I can ==save up enough vacation days==."},
        {"q": "How long have you had this hobby?",
         "vi": "Cà phê thì mình theo được khoảng năm sáu năm rồi. Ban đầu chỉ là uống cho tỉnh táo để làm việc, rồi dần dần thành một sở thích thực sự. Còn du lịch thì mình mê từ hồi đại học.",
         "a": "~~Coffee~~ has been a thing for me for about ~~five or six years~~ now. It started as just ~~caffeine for work~~ but slowly turned into ==a proper interest==. ~~Travel~~ — I've loved that since ~~university~~."},
        {"q": "Why do you enjoy it?",
         "vi": "Cà phê có gì đó rất tĩnh tâm. Cả quá trình xay hạt, cân, rồi pha buộc mình phải chậm lại, trái ngược hẳn với việc code cả ngày. Còn du lịch thì giúp mình thoát khỏi nhịp sống lặp đi lặp lại.",
         "a": "~~Coffee~~ is ~~meditative~~. The whole process of ~~grinding beans~~, ~~weighing~~, and ~~brewing~~ forces me to ~~slow down~~ — a nice contrast to ==coding all day==. With ~~travel~~, it gets me out of my ~~routine~~."},
        {"q": "Do you do it alone or with others?",
         "vi": "Cà phê chủ yếu là chuyện một mình, mình thật sự thích cái nghi thức buổi sáng yên tĩnh đó. Cầu lông thì lúc nào cũng chơi với bạn, thường nhóm bốn năm người. Du lịch thì tùy tâm trạng, có thể đi một mình hoặc đi cùng bạn.",
         "a": "~~Coffee~~ is mostly a ~~solo thing~~ — I genuinely enjoy that ~~quiet morning ritual~~. ~~Badminton~~ I always play with ~~friends~~, usually a group of ~~four or five~~. ~~Travel~~ can be either, ==depending on my mood==."},
        {"q": "Is it expensive?",
         "vi": "Cà phê có thể tốn kém nếu lún sâu vào, nào là hạt ngon, máy xay xịn, đồ nghề cộng lại cũng nhiều. Cầu lông thì rẻ, chỉ tốn tiền sân với cầu. Du lịch là tốn nhất.",
         "a": "~~Coffee~~ can get pricey if you go down the ~~rabbit hole~~ — ~~good beans~~, a ~~decent grinder~~, all that gear adds up. ~~Badminton~~ is cheap — just ~~court fees and shuttlecocks~~. ~~Travel~~ is ==the most expensive==."},
        {"q": "Has your hobby changed over the years?",
         "vi": "Có chút thay đổi. Hồi đại học mình chơi cầu lông nghiêm túc hơn, giờ chỉ chơi cho vui. Với cà phê thì mình đi sâu hơn, từ cà phê gói chuyển sang tự pha kiểu pour-over. Du lịch thì chuyển từ kiểu bụi bặm tiết kiệm sang những chuyến thoải mái hơn.",
         "a": "A bit. I used to play ~~badminton more seriously~~ in ~~college~~, but now it's just ~~casual~~. With ~~coffee~~, I've gone deeper — from ~~instant~~ to ~~hand-brewed pour-overs~~. Travel-wise, I've shifted from ~~cheap backpacking~~ to ==more comfortable trips==."},
        {"q": "Would you recommend it to others?",
         "vi": "Cà phê thì chắc chắn nên, kể cả ở mức nghiệp dư, học cách pha một ly ngon ở nhà cũng rất đáng. Cầu lông thì hợp với ai muốn vận động mà không cần tới phòng gym. Còn du lịch thì khỏi cần nói.",
         "a": "~~Coffee~~, absolutely — even casually, learning to make a ~~decent cup at home~~ is ~~rewarding~~. ~~Badminton~~ is great for anyone who wants ~~exercise without joining a gym~~. ~~Travel~~ ==speaks for itself==."},
        {"q": "Do you spend a lot of time on it?",
         "vi": "Cà phê chắc khoảng một tiếng mỗi ngày, vừa pha vừa thưởng thức. Cầu lông thì hai tiếng, một hai lần một tuần. Du lịch thì thất thường hơn, kiểu mỗi tháng một chuyến cuối tuần và vài tháng một chuyến dài.",
         "a": "Maybe ~~an hour a day~~ on ~~coffee~~, between ~~brewing~~ and just enjoying it. ~~Badminton~~ is ~~two hours once or twice a week~~. ~~Travel~~ is more sporadic — ==a weekend trip a month== and a longer trip every few months."},
        {"q": "Did your hobby change during the pandemic?",
         "vi": "Chắc chắn rồi. Du lịch thì gần như đứng hình suốt mấy năm dịch, nên mình dồn vào cà phê tại nhà, đó cũng là lúc mình mua cái máy pha espresso đầu tiên. Cầu lông thì quay lại ngay khi sân mở cửa lại.",
         "a": "Definitely. ~~Travel~~ obviously got ~~killed~~ for a couple of years, so I doubled down on ~~home coffee~~ — that's actually when I bought my first ~~espresso machine~~. ~~Badminton~~ came back ==the moment courts reopened==."},
    ]},

    {"n": 4, "slug": "family", "title": "Family", "questions": [
        {"q": "Do you have a big family?",
         "vi": "Gia đình mình cũng tầm trung như đa số ở Việt Nam, gồm ba mẹ, một chị gái và mình. Nhưng họ hàng ở Đồng Tháp thì đông, nào anh chị em họ, cô dì chú bác, nên mỗi lần họp mặt gia đình khá đông vui.",
         "a": "Mine is ~~pretty average~~ for Vietnam — my ~~parents~~, an ~~older sister~~, and me. We have a lot of ~~relatives in Dong Thap~~ though, like ~~cousins, aunts and uncles~~, so ==family gatherings get pretty crowded==."},
        {"q": "Who do you live with now?",
         "vi": "Mình sống một mình ở Sài Gòn, thuê một căn hộ nhỏ gần chỗ làm. Gia đình mình ở Đồng Tháp, nên trong tuần chỉ có mình, bộ đồ pha cà phê và một đống hộp đồ ăn mang về.",
         "a": "I live ~~alone in Saigon~~. I rent a ~~small apartment~~ near my office. My family is back in ~~Dong Thap~~, so it's just me, ~~a coffee setup~~, and ==a lot of takeout boxes== during the week."},
        {"q": "Are you close to your family?",
         "vi": "Có, rất thân. Tụi mình không phải kiểu ngày nào cũng nói chuyện, nhưng sự gắn kết thì rất mạnh. Mẹ mình gọi mình hai lần mỗi tuần để chắc là mình ăn uống đàng hoàng, mà nói thật thì mình không phải lúc nào cũng vậy.",
         "a": "Yeah, very. We're not the type that talks ~~every single day~~, but there's a ~~strong sense of connection~~. My ~~mom calls me twice a week~~ to make sure I'm ==eating properly== — which honestly, I'm not always."},
        {"q": "How often do you see your family?",
         "vi": "Chắc khoảng một tháng một lần nếu thu xếp được. Xe từ Sài Gòn về Đồng Tháp mất khoảng ba tiếng, nên đi được vào một cuối tuần dài. Dịp Tết thì mình luôn về ít nhất một tuần.",
         "a": "Probably ~~once a month~~ if I can manage it. The ~~bus from Saigon to Dong Thap~~ takes about ~~three hours~~, so it's doable for a ~~long weekend~~. ~~Tet holiday~~ I always go back for ==at least a week==."},
        {"q": "Who are you closest to in your family?",
         "vi": "Chắc chắn là chị gái mình. Chị chỉ lớn hơn mình hai tuổi nên tụi mình lớn lên làm gì cũng cùng nhau. Tới giờ mỗi khi cần lời khuyên về công việc, cuộc sống hay bất cứ chuyện gì, chị là người mình gọi đầu tiên.",
         "a": "Definitely my ~~older sister~~. She's only ~~two years older~~, so we ~~grew up doing everything together~~. Even now, she's the one I ~~call first~~ when I need ~~advice~~ — about ==work, life, or anything==."},
        {"q": "Do you spend much time with your family?",
         "vi": "Thật lòng là ít hơn mình muốn. Sống xa khiến việc liên lạc hằng ngày khó. Nhưng khi về nhà mình cố gắng có mặt trọn vẹn, cất điện thoại đi, phụ bếp, cứ quây quần chứ không dán mắt vào laptop.",
         "a": "~~Less than I'd like~~, honestly. ~~Living far away~~ makes ~~daily contact~~ tough. But I try to be ~~fully present~~ when I am home — ~~phone away~~, ==helping in the kitchen==, just hanging out instead of being on my laptop."},
        {"q": "What activities do you do together?",
         "vi": "Chủ yếu là nấu ăn và ăn uống cùng nhau. Mẹ mình nấu ăn rất ngon và bữa cơm gia đình gần như là thiêng liêng. Thỉnh thoảng tụi mình xem phim sau bữa tối, hoặc đi dạo dọc bờ sông khi trời đẹp.",
         "a": "Mostly ~~cooking and eating~~. My ~~mom is an amazing cook~~ and ~~family meals~~ are kind of ~~sacred~~. Sometimes we ~~watch movies after dinner~~, or ==take walks along the river== when the weather's nice."},
        {"q": "Has your family influenced your career?",
         "vi": "Một cách gián tiếp thì có. Ba mẹ mình luôn coi trọng việc học hơn mọi thứ, điều đó đẩy mình đến đại học và cuối cùng là sự nghiệp công nghệ. Họ không bảo mình phải học gì, nhưng giá trị của việc học là điều không thể thương lượng.",
         "a": "~~Indirectly~~, yeah. My parents always emphasized ~~education over everything~~, which pushed me toward ~~university~~ and ultimately a ~~tech career~~. They didn't ~~tell me what to study~~, but ==the value of learning== was non-negotiable."},
        {"q": "Do you want to have your own family in the future?",
         "vi": "Rồi cũng sẽ, nhưng mình không vội. Mình muốn ổn định tài chính hơn và có lẽ có nhà riêng trước khi yên bề gia thất. Chắc khoảng năm sáu năm nữa, để xem sao.",
         "a": "~~Eventually~~, yeah, though I'm not in a ~~rush~~. I want to be more ~~financially stable~~ and probably ~~own a place~~ before ~~settling down~~. Maybe in ==five or six years== — we'll see."},
        {"q": "Has your family changed in recent years?",
         "vi": "Có chút thay đổi. Chị mình lấy chồng năm ngoái và giờ có nhà riêng, nên mỗi lần mình về thấy vắng hơn. Ba mẹ mình cũng có tuổi rồi, điều đó khiến mình nghĩ nhiều hơn đến chuyện cuối cùng sẽ về quê.",
         "a": "A bit. My ~~sister got married~~ last year and has her ~~own place~~ now, so it's quieter when I visit. My ~~parents are getting older~~ too, which makes me think more about ==going back home eventually==."},
    ]},

    {"n": 5, "slug": "daily-routine", "title": "Daily Routine", "questions": [
        {"q": "What's your daily routine like?",
         "vi": "Ngày thường thì khá đều đặn. Mình dậy khoảng 7 giờ, pha cà phê, kiểm tra Slack, rồi code từ 9 giờ tới 6 giờ với một bữa trưa. Buổi tối thì linh hoạt, lúc thì tập thể dục, lúc thì chỉ ăn tối và xem Netflix.",
         "a": "On ~~weekdays~~ it's pretty consistent. I ~~wake up around 7~~, ~~brew coffee~~, ~~check Slack~~, then ~~code from 9 to 6~~ with a lunch break. Evenings are flexible — sometimes ==a workout==, sometimes just ~~dinner and Netflix~~."},
        {"q": "Are you a morning person or a night person?",
         "vi": "Hồi đại học mình là cú đêm, nhưng giờ mình thiên về người dậy sớm hơn. Mình thấy đầu óc minh mẫn hơn trước trưa, nên mình cố làm những phần code khó nhất vào đầu ngày.",
         "a": "I used to be a ~~night owl in college~~, but these days I'm more of a ~~morning person~~. I find I ~~think more clearly before noon~~, so I try to do my ~~hardest coding work~~ ==early in the day==."},
        {"q": "What time do you usually wake up?",
         "vi": "Khoảng 7 giờ sáng ngày thường. Cuối tuần thì mình cho phép ngủ nướng tới 8 hay 9 giờ, nhưng hiếm khi trễ hơn vì mình thấy bứt rứt nếu phí cả buổi sáng. Việc đầu tiên mình làm luôn là pha cà phê, không ngoại lệ.",
         "a": "Around ~~7am on weekdays~~. On ~~weekends~~ I let myself sleep in until ~~8 or 9~~, but rarely later — I get ~~restless~~ if I waste the morning. The first thing I do is ==make coffee, no exceptions==."},
        {"q": "Do you have the same routine every day?",
         "vi": "Gần như vậy, từ thứ Hai tới thứ Sáu. Cuối tuần thì khác, mình có thể đánh cầu lông buổi sáng, ăn brunch với bạn, hoặc bắt xe đi đâu đó. Cái nếp đó giúp mình giữ được năng suất.",
         "a": "Pretty much, ~~Monday through Friday~~. ~~Weekends~~ are different — I might have ~~badminton in the morning~~, ~~brunch with friends~~, or ~~hop on a bus somewhere~~. The routine ==helps me stay productive==."},
        {"q": "What's the most important part of your day?",
         "vi": "Thật ra là nghi thức cà phê buổi sáng. Chỉ mười lăm phút thôi nhưng nó đặt nhịp cho cả ngày, mình thấy bình tĩnh, tập trung và không vội vã lao vào việc. Bỏ qua nó là mình thấy cả ngày lệch nhịp.",
         "a": "Honestly, my ~~morning coffee ritual~~. It's only ~~fifteen minutes~~, but it ~~sets the tone for the whole day~~ — I'm ~~calm, focused, and not rushing~~ into work. Skipping it ==makes me feel off==."},
        {"q": "Do you ever change your routine?",
         "vi": "Có chứ, nhất là khi mình đi du lịch hay về quê. Cái nếp bị phá vỡ, mà thật ra mấy ngày đầu lại thấy dễ chịu. Nhưng sau khoảng một tuần thì mình bắt đầu thèm cái sự quy củ trở lại.",
         "a": "Yeah, especially when I'm ~~traveling~~ or ~~visiting home~~. The routine gets ~~thrown out~~, which is actually ~~nice for a few days~~. After about a week though, I ==start craving the structure== again."},
        {"q": "What do you usually do on weekends?",
         "vi": "Thứ Bảy là dành cho hoạt động, đánh cầu lông, khám phá quán cà phê mới, hoặc một chuyến đi gần. Chủ Nhật thì mình sống chậm, giặt giũ, chuẩn bị đồ ăn, có khi ăn trưa thong thả và đi dạo buổi tối.",
         "a": "~~Saturdays~~ are for activities — ~~badminton~~, ~~exploring a new cafe~~, or a ~~short trip nearby~~. ~~Sundays~~ I keep slow — ~~laundry~~, ~~meal prep~~, maybe a ~~long lunch~~, and ==an evening walk==."},
        {"q": "How do you usually relax in the evening?",
         "vi": "Sau bữa tối mình hoặc đọc sách, xem một series, hoặc đôi khi gọi điện về cho gia đình. Khoảng 10 giờ mình cố cất điện thoại và thư giãn cho dễ ngủ, dù nói thật là lúc được lúc không.",
         "a": "After dinner I'll either ~~read~~, ~~watch a series~~, or sometimes ~~call my family~~. Around ~~10~~ I try to ~~put my phone away~~ and ~~wind down~~ — though that's ==hit or miss==, I'll be honest."},
        {"q": "Has your routine changed over the years?",
         "vi": "Thay đổi nhiều. Hồi sinh viên lịch của mình loạn cả lên, thức khuya, ăn uống thất thường. Từ khi đi làm toàn thời gian, nhất là sau dịch, mình xây dựng được một ngày quy củ hơn nhiều.",
         "a": "A lot. As a ~~student~~, my schedule was ~~all over the place~~ — ~~late nights~~, ~~no consistent meals~~. Once I started ~~working full-time~~ and especially since ~~the pandemic~~, I built a ==much more structured day==."},
        {"q": "Would you like to change your routine?",
         "vi": "Có lẽ thêm vận động. Mình ngồi quá nhiều vì công việc, nên thêm chạy bộ buổi sáng hay tập yoga sẽ là điều nên làm. Còn lại thì mình khá hài lòng với cách một ngày của mình diễn ra.",
         "a": "Maybe ~~add more exercise~~. I sit too much because of my job, so adding ~~morning runs or yoga~~ would be a ~~good move~~. Otherwise, I'm pretty content with ==how my days look==."},
    ]},

    {"n": 6, "slug": "food", "title": "Food", "questions": [
        {"q": "What kind of food do you like?",
         "vi": "Mình mê đồ Việt, có thể nói là khá trung thành với món địa phương. Mình cũng thích ẩm thực Nhật, nhất là ramen và sushi. Sài Gòn nhiều món đa dạng nên mình hiếm khi hết lựa chọn.",
         "a": "I love anything ~~Vietnamese~~ — I'd say I'm ~~pretty loyal~~ to ~~local food~~. I'm also into ~~Japanese cuisine~~, especially ~~ramen and sushi~~. ~~Saigon~~ has a great variety, so I ==rarely run out of options==."},
        {"q": "What's your favorite dish?",
         "vi": "Phải là hủ tiếu Sa Đéc, món hủ tiếu ở quê mình tại Đồng Tháp. Nước lèo trong mà rất đậm đà, và không có chỗ nào ở Sài Gòn sánh được với món mẹ mình nấu. Đúng kiểu món ăn an ủi tâm hồn.",
         "a": "Has to be ~~hu tieu Sa Dec~~ — a ~~noodle soup from my hometown~~ in ~~Dong Thap~~. The ~~broth is clear but really flavorful~~, and nothing made in Saigon quite matches ==what my mom makes==. Pure comfort food."},
        {"q": "Do you cook at home or eat out?",
         "vi": "Thật ra chủ yếu là ăn ngoài. Mình sống một mình mà Sài Gòn thì góc nào cũng có đồ ăn đường phố ngon. Cuối tuần mình cũng nấu, mấy món đơn giản như cơm chiên, nhưng mình không phải kiểu nấu ăn tại nhà nghiêm túc.",
         "a": "Mostly ~~eat out~~, honestly. I ~~live alone~~ and there's ~~amazing street food on every corner~~ in Saigon. I do cook on ~~weekends~~ sometimes — ~~simple stuff like fried rice~~ — but ==I'm not a serious home cook==."},
        {"q": "Are you a picky eater?",
         "vi": "Hoàn toàn không. Cái gì mình cũng thử ít nhất một lần. Chỉ có vài thứ mình thật sự né là đồ siêu cay và một số món nội tạng, mấy món đó phổ biến ở đây nhưng mình chưa bao giờ hợp.",
         "a": "~~Not at all~~. I'll try ~~almost anything once~~. The only things I really avoid are ~~super spicy food~~ and ~~certain organ meats~~ — those are ~~common here~~ but ==never grew on me==."},
        {"q": "Do you prefer Vietnamese food or foreign food?",
         "vi": "Đồ Việt, không bàn cãi. Nó cứ như hương vị quê nhà. Nhưng nói thực tế thì mình vẫn vui vẻ ăn đồ ngoại vài lần một tuần cho đổi vị. Sự đa dạng chính là điều làm ẩm thực Sài Gòn hay đến vậy.",
         "a": "~~Vietnamese, hands down~~. It just ~~tastes like home~~. But if I'm being practical, I'll happily eat ~~foreign food a few times a week~~ for ~~variety~~. Variety is ==what makes Saigon's food scene so good==."},
        {"q": "Do you like trying new food?",
         "vi": "Có, nhất là khi đi du lịch. Thử đồ ăn địa phương gần như là một nửa lý do mình đi du lịch. Ngay cả ở Sài Gòn, khi có quán mới mở, mình thường ghé thử trong tháng đầu tiên.",
         "a": "Yeah, especially when I ~~travel~~. ~~Trying local food~~ is ~~half the reason~~ I travel in the first place. Even in ~~Saigon~~, when a ~~new restaurant opens~~, I'll usually go check it out ==within the first month==."},
        {"q": "Has your taste in food changed?",
         "vi": "Có chút thay đổi. Hồi nhỏ mình kén ăn hơn nhiều, không đụng tới cá hay đồ chua. Giờ thì mê cả hai. Cà phê cũng vậy, hồi đó ghét vị đắng, nhưng tới khoảng đầu hai mươi tuổi thì mình học được cách thưởng thức nó.",
         "a": "A bit. As a kid I was ~~way pickier~~ — wouldn't ~~touch fish~~ or anything ~~sour~~. Now I love both. ~~Coffee~~ is another one — used to ~~hate the bitterness~~, but somewhere in ==my early 20s== I learned to appreciate it."},
        {"q": "Do you eat healthy food?",
         "vi": "Cũng tạm. Mình cố cân bằng, nếu trưa ăn đồ đường phố thì tối mình nấu một đĩa salad hoặc kiếm gì đó nhẹ nhàng. Mình không khắt khe lắm, nhưng có để ý.",
         "a": "~~Sort of~~. I try to ~~balance things out~~ — if I have ~~street food for lunch~~, I'll cook a ~~salad~~ or grab ~~something light for dinner~~. I'm ~~not strict~~ about it, but ==I pay attention==."},
        {"q": "What food don't you like?",
         "vi": "Mình không khoái đồ quá cay, cái gì nhiều ớt quá là làm tê hết vị giác. Còn nữa là sầu riêng. Mình biết nó là đặc sản Việt Nam, nhưng mình thật sự không vượt qua được cái mùi của nó.",
         "a": "I'm not a fan of ~~really spicy food~~ — anything with ~~too much chili~~ just ~~kills my taste buds~~. Also, ~~durian~~. I know it's a ~~Vietnamese specialty~~, but I really cannot ==get past the smell==."},
        {"q": "Did your parents teach you to cook?",
         "vi": "Mẹ mình dạy mình mấy cái cơ bản, như nấu cơm cho đúng, mấy món xào đơn giản, kiểu vậy. Còn lại mình học qua YouTube và tự mò mẫm sau khi lên Sài Gòn.",
         "a": "My ~~mom~~ taught me the ~~basics~~ — how to ~~cook rice properly~~, ~~simple stir-fries~~, that kind of thing. The rest I picked up from ~~YouTube and trial and error~~ after ==moving to Saigon==."},
    ]},

    {"n": 7, "slug": "music", "title": "Music", "questions": [
        {"q": "Do you like listening to music?",
         "vi": "Chắc chắn rồi. Hầu như cả ngày làm việc mình đều mở nhạc, nó giúp mình tập trung khi code. Không có nhạc thì văn phòng hay căn hộ của mình nghe yên ắng đến lạ.",
         "a": "~~Definitely~~. Music is on for ~~most of my workday~~ — it helps me ~~focus when I'm coding~~. Without music, the ~~office or my apartment~~ feels ==too quiet, weirdly==."},
        {"q": "What kind of music do you like?",
         "vi": "Chủ yếu là nhạc nhẹ nhàng, kiểu lo-fi, indie, acoustic singer-songwriter. Khi code thì mình cần nhạc không lời. Cuối tuần thì mình mở indie Việt hoặc nhạc pop.",
         "a": "Mostly ~~chill stuff~~ — ~~lo-fi~~, ~~indie~~, ~~acoustic singer-songwriter~~. When I'm coding I need something ~~without lyrics~~. On weekends I'll throw on ==Vietnamese indie or some pop==."},
        {"q": "When do you usually listen to music?",
         "vi": "Gần như cả ngày. Nhạc lúc làm việc, nhạc lúc tập gym, thậm chí nhạc lúc nấu ăn. Lúc duy nhất mình không nghe là trong các buổi họp, hoặc khi đang cố dỗ giấc ngủ.",
         "a": "Pretty much ~~all day~~. Music ~~while I work~~, music ~~in the gym~~, even music ~~while I'm cooking~~. The only time I don't listen is during ~~meetings~~, or ==when I'm trying to fall asleep==."},
        {"q": "Do you play any musical instruments?",
         "vi": "Mình tập guitar hồi cấp ba và chơi cũng tạm được. Nhưng từ hồi đại học tới giờ mình ít đụng tới, cây đàn đang phủ bụi ở góc nhà. Mình cứ tự nhủ là sẽ chơi lại.",
         "a": "I picked up the ~~guitar in high school~~ and got ~~reasonably okay~~ at it. I haven't ~~touched it much since university~~ though — it's ~~collecting dust in the corner~~. I keep telling myself ==I'll start again==."},
        {"q": "Has your taste in music changed?",
         "vi": "Thay đổi nhiều. Hồi tuổi teen mình mê rock và metal, kiểu Linkin Park, Green Day. Lớn lên mình chuyển sang mấy thể loại nhẹ nhàng hơn. Giờ cái gì quá dữ dội nghe là thấy mệt.",
         "a": "A lot. As a teenager I was into ~~rock and metal~~ — ~~Linkin Park, Green Day~~. As I got older I shifted toward ~~calmer genres~~. Now anything ~~too aggressive~~ just feels ==exhausting to listen to==."},
        {"q": "Do you like live music?",
         "vi": "Có chứ, khi có dịp. Sài Gòn không có quá nhiều concert, nhưng mình từng đi vài show acoustic nhỏ ở quán cà phê. Nhạc sống có cái gì đó mà bản thu không tài nào lột tả được.",
         "a": "Yeah, when I get the chance. There aren't ~~tons of concerts in Saigon~~, but I've been to a few ~~small acoustic shows at cafes~~. There's something about ~~live performance~~ that ==recordings can't capture==."},
        {"q": "Is music important in your daily life?",
         "vi": "Cực kỳ quan trọng. Nó như tiếng nền định hình tâm trạng của mình. Một playlist hay có thể biến một việc nhàm chán thành gần như thú vị. Không có nó thì cả ngày cứ nhạt đi.",
         "a": "~~Hugely~~. It's like ~~background noise that shapes my mood~~. A ~~good playlist~~ can turn a ~~tedious task~~ into something ~~almost enjoyable~~. Without it, the day just ==feels flatter==."},
        {"q": "Do you sing?",
         "vi": "Chỉ hát trong lúc tắm hoặc khi không có ai xung quanh. Karaoke ở Việt Nam phổ biến lắm, đám bạn thỉnh thoảng lôi mình đi, mình chỉ hát khi đã đủ vài chai bia. Mình tự biết là hát không hay.",
         "a": "Only in the ~~shower~~ or when ~~no one's around~~. ~~Karaoke is huge in Vietnam~~, and my friends drag me out sometimes — I'll do it once ==enough beer is involved==. I'm aware I'm not good."},
        {"q": "What music was popular when you were young?",
         "vi": "V-pop và rất nhiều K-pop, nhất là khoảng đầu những năm 2010. Big Bang với Super Junior ở đâu cũng thấy. Hồi đó mình không mê, nhưng giờ mấy bài đó gợi lại bao kỷ niệm.",
         "a": "~~V-pop~~ and a lot of ~~K-pop~~, especially around the ~~early 2010s~~. ~~Big Bang and Super Junior~~ were everywhere. I wasn't into it then, but those songs ==trigger major nostalgia== now."},
        {"q": "Do people in your country listen to a lot of music?",
         "vi": "Chắc chắn rồi, nhạc ở Việt Nam chỗ nào cũng có. Quán cà phê, taxi, đám cưới, thậm chí mấy hàng quán vỉa hè. Karaoke đặc biệt là một nét văn hóa lớn, gần như cuộc tụ họp nào cũng kết thúc bằng việc ai đó cầm micro.",
         "a": "~~Absolutely~~, music is everywhere in Vietnam. ~~Cafes, taxis, weddings~~, even ~~sidewalk shops~~. ~~Karaoke~~ especially is a ~~huge cultural thing~~ — almost every gathering ends with ==someone grabbing a microphone==."},
    ]},

    {"n": 8, "slug": "weather", "title": "Weather", "questions": [
        {"q": "What's the weather like in your country?",
         "vi": "Việt Nam chủ yếu là khí hậu nhiệt đới, nên nóng quanh năm. Miền Nam, nơi mình sống, về cơ bản chỉ có hai mùa, mùa khô và mùa mưa. Miền Bắc thì có mùa đông thật sự, cái đó mình chưa từng thật sự trải nghiệm.",
         "a": "Vietnam is mostly ~~tropical~~, so it's ~~warm year-round~~. The ~~south~~, where I live, basically has ~~two seasons~~ — ~~dry and rainy~~. The ~~north~~ gets ~~actual winter~~, which I've ==never really experienced==."},
        {"q": "Do you prefer hot or cold weather?",
         "vi": "Thật lòng là thời tiết mát hơn. Mình sống cả đời ở miền Nam nóng nực, nên cái gì dưới 25 độ là thấy như món quà. Mỗi lần đi Đà Lạt hay Sa Pa mình luôn mang dư áo khoác chỉ để tận hưởng cái lạnh.",
         "a": "~~Cooler weather~~, honestly. I've lived my ~~whole life in the hot south~~, so anything ~~below 25 feels like a gift~~. When I travel to ~~Da Lat or Sapa~~ I always overpack jackets just to ==enjoy the chill==."},
        {"q": "What's your favorite season?",
         "vi": "Mùa khô, từ tháng Giêng tới tháng Ba. Buổi sáng mát, độ ẩm giảm, và có thể ra ngoài mà không đến nỗi ướt đẫm áo. Đó là thời điểm đẹp nhất để ở Sài Gòn.",
         "a": "The ~~dry season~~, ~~January through March~~. The ~~mornings are cool~~, the ~~humidity drops~~, and you can actually go outside ~~without sweating through your shirt~~. It's the ==best time to be in Saigon==."},
        {"q": "Does weather affect your mood?",
         "vi": "Có, nhiều hơn mình muốn thừa nhận. Một tuần xám xịt mưa gió có thể khiến mình tụt năng lượng hẳn, nhất là khi mình hay ra ngoài uống cà phê. Mấy buổi sáng nắng đẹp thì cảm giác khác hẳn.",
         "a": "Yeah, more than I want to admit. A ~~grey, rainy week~~ can really ~~drag my energy down~~, especially with how much I rely on ~~going out for coffee~~. ~~Sunny mornings~~ just ==hit different==."},
        {"q": "Do you check the weather forecast?",
         "vi": "Gần như sáng nào cũng xem, nhất là mùa mưa. Mưa Sài Gòn dữ lắm, không xem là dính mưa ướt nhẹp khi chạy xe máy đi làm. Dự báo ở đây không phải lúc nào cũng chính xác, nhưng còn hơn không.",
         "a": "Almost every morning, especially during ~~rainy season~~. ~~Saigon rain is intense~~ — if I don't check, I'll get ~~drenched on my motorbike commute~~. The ~~forecasts here aren't always accurate~~, but ==better than nothing==."},
        {"q": "Has the weather changed in your country?",
         "vi": "Chắc chắn rồi. Mùa mưa giờ nặng hơn và khó đoán hơn so với hồi mình còn nhỏ. Các đợt nắng nóng thì dài hơn và gay gắt hơn. Khó mà phủ nhận biến đổi khí hậu khi mình cảm nhận được nó.",
         "a": "Definitely. The ~~rainy season~~ feels ~~heavier and less predictable~~ than I remember as a kid. ~~Heat waves~~ are ~~longer and more intense~~. Hard to ==deny climate change== when you can feel it."},
        {"q": "What do you do in bad weather?",
         "vi": "Nếu là ngày mưa to thì mình chỉ ở nhà. Nấu gì đó, pha thêm một ly cà phê, làm việc tại căn hộ nếu được. Có cái gì đó ấm cúng một khi mình không bị kẹt ngoài mưa.",
         "a": "If it's a ~~heavy rain day~~, I just ~~stay in~~. ~~Cook something at home~~, brew an ~~extra cup of coffee~~, ~~work from the apartment~~ if possible. There's something ==cozy about it== once you're not stuck out in it."},
        {"q": "Is there a season you don't like?",
         "vi": "Mấy tháng mưa cao điểm, khoảng tháng Tám tháng Chín. Ngập ở vài quận Sài Gòn kinh khủng, và đi lại trở thành ác mộng. Mấy chuyến chạy xe máy của mình biến thành cả một cuộc sinh tồn.",
         "a": "The ~~peak rainy months~~, around ~~August and September~~. The ~~flooding in some Saigon districts~~ is ~~brutal~~, and ~~getting around becomes a nightmare~~. My motorbike rides become ==a whole survival event==."},
        {"q": "Do you like rainy days?",
         "vi": "Thỉnh thoảng, khi mình đã ở nhà sẵn. Tiếng mưa nghe rất êm, và một ly cà phê nóng với cuốn sách vào buổi chiều mưa thật sự là một trong những điều mình thích nhất. Nhưng mình ghét bị dính mưa ngoài đường.",
         "a": "Occasionally, when I'm ~~already at home~~. The ~~sound of rain is calming~~, and a ~~hot coffee plus a book on a rainy afternoon~~ is genuinely one of my favorite things. But I hate ==getting caught in it outside==."},
        {"q": "Does the weather affect your activities?",
         "vi": "Có, rất nhiều. Ngày mưa là phá hỏng kế hoạch đánh cầu lông hay mọi hoạt động ngoài trời. Ngược lại, sáng mát thì mình dễ đi dạo hơn hẳn, thời tiết về cơ bản quyết định cuối tuần của mình.",
         "a": "Yeah, a lot. ~~Rainy days~~ kill my plans for ~~badminton or any outdoor activity~~. On the flip side, ~~cool mornings~~ make me much more likely to ~~go for a walk~~ — weather basically ==dictates my weekends==."},
    ]},

    {"n": 9, "slug": "sports", "title": "Sports", "questions": [
        {"q": "Do you play any sports?",
         "vi": "Mình chơi cầu lông cho vui với bạn bè, thường một hai lần một tuần. Mình không ở đội nào cả, chỉ là một cách vui để vận động và gặp gỡ ngoài giờ làm. Với mình nó hay hơn đi gym.",
         "a": "I play ~~badminton casually~~ with friends, usually ~~once or twice a week~~. I'm not on any team — just a ~~fun way to get exercise~~ and ~~hang out outside of work~~. It ==beats the gym for me==."},
        {"q": "What sports do you like to watch?",
         "vi": "Bóng đá là môn lớn nhất. Nhất là các trận của đội tuyển Việt Nam, nửa nước dán mắt vào TV. Mình cũng xem chút Premier League, chủ yếu Manchester United, dù mấy năm nay họ làm mình thất vọng.",
         "a": "~~Football~~ is the big one. ~~Vietnamese national team matches~~ especially — ~~half the country~~ is glued to the TV. I also watch a bit of ~~Premier League~~, mostly ~~Manchester United~~, though they've been ==disappointing for years==."},
        {"q": "Did you play sports as a kid?",
         "vi": "Khá nhiều. Mình đá bóng ngoài đồng trong làng với mấy anh chị em họ, còn cầu lông thì đã phổ biến ở trường. Tụi mình không có sân bãi tử tế, cứ căng cái lưới giữa hai cái cây mà chơi. Rất giản dị.",
         "a": "Quite a bit. I played ~~football in the village fields~~ with my ~~cousins~~, and ~~badminton~~ was already big in school. We didn't have ~~proper facilities~~ — we'd hang a net between ==two trees==. Super casual."},
        {"q": "Are sports popular in your country?",
         "vi": "Bóng đá thì cực kỳ phổ biến, gần như là niềm đam mê quốc dân. Cầu lông đứng ngay sau, nhất là trong các sân chơi cộng đồng. Người Việt thích xem cũng nhiều như thích chơi, đường nào cũng có quán cà phê có màn hình.",
         "a": "~~Football~~ is huge — it's ~~basically the national obsession~~. ~~Badminton~~ is a ~~close second~~, especially in ~~casual community settings~~. Vietnamese people love watching as much as playing — every street ==has a cafe with a screen==."},
        {"q": "Do you think sports are important?",
         "vi": "Chắc chắn rồi. Ngoài rèn thể lực, thể thao còn dạy tinh thần đồng đội, kỷ luật và cách thua một cách đàng hoàng, điều mà thật ra bị đánh giá thấp. Mình nghĩ nhiều kỹ năng sống đến từ việc đều đặn xuất hiện luyện tập.",
         "a": "Absolutely. Beyond ~~fitness~~, sports teach ~~teamwork, discipline~~, and ~~how to lose gracefully~~ — which is honestly underrated. I think a lot of ==life skills== come from showing up regularly."},
        {"q": "Have you tried any new sports recently?",
         "vi": "Mình thử pickleball vài tháng trước, môn này đang bùng nổ ở đây, và chơi vui bất ngờ. Mình có thể chơi nghiêm túc hơn nếu có sân mở gần chỗ mình ở. Ngoài ra thì vẫn gắn với cầu lông.",
         "a": "I tried ~~pickleball~~ a few months ago — it's ~~blowing up here~~, and it was ~~surprisingly fun~~. I might pick it up more seriously if a ~~court opens nearer~~ to where I live. Other than that, ==stuck to badminton==."},
        {"q": "Do you watch sports on TV?",
         "vi": "Chủ yếu trong các giải lớn, World Cup, Euro, SEA Games. Mình không còn theo các giải hằng tuần sát sao nữa. Với công việc bận rộn, kiếm ba tiếng cho một trận đấu đều đặn giờ khó hơn trước.",
         "a": "Mostly during ~~big tournaments~~ — ~~World Cup, Euro, SEA Games~~. I don't ~~follow weekly leagues~~ that closely anymore. With work, finding ~~three hours for a regular match~~ feels ==harder than it used to==."},
        {"q": "Do you prefer team sports or individual sports?",
         "vi": "Chắc chắn là thể thao đồng đội. Yếu tố giao lưu chiếm một nửa niềm vui với mình. Đánh đôi cầu lông hay đá bóng với bạn bè cảm giác hay hơn nhiều so với chạy một mình trên máy chạy bộ.",
         "a": "~~Team sports, for sure~~. The ~~social aspect~~ is half the fun for me. Playing ~~badminton doubles~~ or ~~kicking a ball around with friends~~ feels much better than ==running on a treadmill alone==."},
        {"q": "Do you think kids should play sports?",
         "vi": "Chắc chắn rồi. Trẻ con bây giờ dành quá nhiều thời gian cho màn hình, và thể thao là một trong những cách tốt nhất để cân bằng lại. Đó cũng là nơi tụi nhỏ kết bạn và học cách đối mặt với cạnh tranh từ sớm.",
         "a": "~~Definitely~~. Kids today spend way too much time on ~~screens~~, and sports are one of the best ways to ~~balance that out~~. It's also where they ~~make friends~~ and ==learn how to handle competition== early."},
        {"q": "What sport would you like to learn?",
         "vi": "Có lẽ là tennis. Nhìn nó thanh lịch và kỹ thuật ấn tượng. Rào cản chỉ là chi phí, sân và học phí ở Sài Gòn đắt lên nhanh lắm. Có thể đợi khi sự nghiệp ổn định hơn.",
         "a": "~~Tennis~~, probably. It looks ~~elegant~~ and the ~~technique is impressive~~. The barrier is just ~~cost~~ — courts and lessons in ~~Saigon get expensive fast~~. Maybe once ==my career is more settled==."},
    ]},

    {"n": 10, "slug": "travel", "title": "Travel", "questions": [
        {"q": "Do you like to travel?",
         "vi": "Mình mê lắm, thật ra đó có lẽ là điều mình thích nhất trong đời. Du lịch là thứ mình để dành tiền và mong chờ cả năm. Dù là chuyến cuối tuần hay kỳ nghỉ dài ở nước ngoài, lúc nào cũng thấy đáng.",
         "a": "I love it, honestly it's ~~probably my favorite thing in life~~. Travel is what I ~~save for and look forward to~~ all year. Whether it's a ~~weekend trip~~ or a ~~longer overseas vacation~~, it always ==feels worth it==."},
        {"q": "Where was your last trip?",
         "vi": "Tháng trước mình đi Đà Lạt với vài người bạn đồng nghiệp. Ba ngày, uống cà phê đã đời, đi bộ quanh hồ Tuyền Lâm, đúng kiểu trốn khỏi Sài Gòn. Riêng cái thời tiết mát đã đáng chuyến đi rồi.",
         "a": "I went to ~~Da Lat~~ last month with a ~~couple of friends from work~~. ~~Three days~~, ~~lots of coffee~~, ~~hiking around Tuyen Lam Lake~~ — proper escape from Saigon. The ==cool weather alone== was worth the trip."},
        {"q": "Do you prefer to travel alone or with others?",
         "vi": "Cả hai, tùy chuyến. Đi một mình thì hay ở chỗ được tự suy ngẫm và đi theo nhịp của mình. Đi nhóm với bạn thân thì vui hơn nhiều, nhất là những nơi có đồ ăn ngon hoặc về đêm sôi động.",
         "a": "Both, depending on the trip. ~~Solo travel~~ is great for ~~self-reflection~~ and ~~going at my own pace~~. ~~Group trips with close friends~~ are way more fun, especially for places with ==good food or nightlife==."},
        {"q": "What kind of places do you like to visit?",
         "vi": "Mình thích những nơi yên tĩnh, thiên nhiên đẹp, kiểu núi, biển, thị trấn nhỏ. Mấy thành phố du lịch lớn thì thú vị một lần thôi, chứ mình chán đám đông nhanh lắm. Một nơi có cà phê ngon và buổi sáng thong thả là lý tưởng với mình.",
         "a": "I love ~~quieter places with good nature~~ — ~~mountains, beaches, small towns~~. ~~Big tourist cities~~ are ~~interesting once~~ but I get tired of crowds quickly. A place with ==great coffee and slow mornings== is my ideal."},
        {"q": "Do you prefer domestic or international travel?",
         "vi": "Trong nước thì tiện và hợp túi tiền, còn nước ngoài thì có cái sốc văn hóa và sự háo hức. Việt Nam còn nhiều nơi tuyệt vời mình chưa đi hết, nhưng mỗi chuyến ra nước ngoài đều dạy mình điều gì đó mà ở nhà không có được.",
         "a": "~~Domestic~~ for the ~~convenience and budget~~, ~~international~~ for the ~~culture shock and excitement~~. Vietnam has ~~incredible places I haven't seen yet~~, but every overseas trip ==teaches me something== I couldn't get at home."},
        {"q": "What do you usually do when you travel?",
         "vi": "Mình không phải kiểu mê tham quan, mình thà ngồi một quán cà phê địa phương còn hơn lướt qua mười cái bảo tàng. Mình thích thử mọi món ăn đường phố, đi dạo không theo kế hoạch cứng nhắc, và trò chuyện với người địa phương khi có thể.",
         "a": "I'm ~~not a huge sightseer~~ — I'd rather ~~sit in a local cafe~~ than ~~rush through ten museums~~. I love ~~trying every street food~~, ~~walking around without a strict plan~~, and ==chatting with locals when possible==."},
        {"q": "Where would you like to go in the future?",
         "vi": "Nhật Bản đứng đầu danh sách của mình, nhất là Kyoto. Cái sự hòa quyện giữa văn hóa cổ, đồ ăn ngon và vẻ đẹp tĩnh lặng đó hợp với mình. Về lâu dài mình muốn làm một chuyến châu Âu tử tế, có thể đi bụi cả tháng.",
         "a": "~~Japan~~ is at the top of my list, especially ~~Kyoto~~. The ~~mix of old culture, great food~~, and that ~~calm aesthetic~~ just speaks to me. Long-term I'd love to do a ==proper Europe trip==, maybe a month backpacking."},
        {"q": "Did you travel when you were a child?",
         "vi": "Thật ra là không nhiều. Gia đình mình không có điều kiện cho mấy chuyến đi đàng hoàng, và Đồng Tháp thì khá xa xôi. Mấy chuyến lớn nhất thường là về thăm họ hàng ở các tỉnh lân cận, vui đấy, nhưng không hẳn là du lịch.",
         "a": "~~Not much~~, honestly. My family didn't have the ~~budget for proper trips~~, and ~~Dong Thap is pretty remote~~. The biggest trips were usually to ~~relatives in nearby provinces~~ — fun, but ==not really travel==."},
        {"q": "What do you remember most about a trip?",
         "vi": "Chuyến đi Đà Nẵng một mình đầu tiên của mình là đáng nhớ nhất. Lúc đó mình 22 tuổi, vừa đi làm công việc đầu tiên, và đi đó một mình vào một cuối tuần dài. Không có gì kịch tính cả, nhưng cái cảm giác tự xoay xở mọi thứ một mình thì không thể quên.",
         "a": "My ~~first solo trip to Da Nang~~ stands out. I was ~~22~~, just ~~started my first job~~, and went there alone for a ~~long weekend~~. Nothing dramatic happened — but the ==freedom of figuring everything out alone== was unforgettable."},
        {"q": "How do you usually plan your trips?",
         "vi": "Mình là kiểu nghiên cứu kỹ, mình có thể bỏ ra hàng tuần đọc blog, xem video YouTube và lưu các điểm trên Google Maps trước mỗi chuyến đi. Mình luôn có một kế hoạch sơ bộ, nhưng vẫn chừa nhiều chỗ cho sự ngẫu hứng khi tới nơi.",
         "a": "I'm a ~~research nerd~~ — I'll spend weeks ~~reading blogs~~, ~~watching YouTube videos~~, and ~~saving Google Maps pins~~ before any trip. I always have a ~~rough plan~~, but I leave plenty of room for ==spontaneity on the ground==."},
    ]},

]


def main():
    out_root = Path(__file__).resolve().parent.parent / "speaking" / "topics"
    out_root.mkdir(parents=True, exist_ok=True)
    for topic in TOPICS:
        folder = out_root / topic["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        qs_json = json.dumps(topic["questions"], indent=2, ensure_ascii=False)
        html = (TEMPLATE
                .replace("__TOPIC_NUM__", str(topic["n"]))
                .replace("__TOPIC_TITLE__", topic["title"])
                .replace("__QUESTIONS_JSON__", qs_json))
        (folder / "index.html").write_text(html, encoding="utf-8")
        print(f"  wrote {folder.relative_to(out_root.parent.parent)}/index.html  ({len(topic['questions'])} questions)")

    print(f"\nDone. {len(TOPICS)} topic decks generated under speaking/topics/")


if __name__ == "__main__":
    main()
