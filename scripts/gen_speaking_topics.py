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
  .answer .blank {
    display: inline-block;
    background: #e5e7eb;
    color: transparent;
    border-radius: 4px;
    padding: 0 4px;
    margin: 0 1px;
    user-select: none;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, transform 0.05s;
  }
  .answer .blank:hover { background: #d1d5db; }
  .answer .blank:active { transform: scale(0.95); }
  .answer .blank.revealed {
    background: rgba(217, 119, 6, 0.16);
    color: #92400e;
    font-weight: 500;
    user-select: text;
    cursor: text;
  }
  .answer .blank.revealing { animation: blank-flip 0.36s cubic-bezier(0.4, 0.0, 0.2, 1); }
  @keyframes blank-flip {
    0%   { transform: rotateX(0); }
    50%  { transform: rotateX(90deg); }
    100% { transform: rotateX(0); }
  }

  .word { transition: color 0.12s, background 0.12s; border-radius: 3px; }
  .word.speaking,
  .question .word.speaking,
  .answer .blank.revealed.speaking {
    color: #1d4ed8;
    background: rgba(59, 130, 246, 0.18);
    font-weight: 600;
  }
  .answer .blank.speaking { background: rgba(59, 130, 246, 0.55); }

  .record-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #fff;
    color: #c2410c;
    border: 1.5px solid #c2410c;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
  }
  .record-btn:hover { background: #c2410c; color: #fff; }
  .record-btn.recording { background: #c2410c; color: #fff; animation: rec-pulse 1.2s ease-in-out infinite; }
  @keyframes rec-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(194, 65, 12, 0.4); }
    50%      { box-shadow: 0 0 0 10px rgba(194, 65, 12, 0); }
  }
  .record-btn .rec-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #c2410c;
    display: inline-block;
  }
  .record-btn.recording .rec-dot { background: #fff; }

  .score-result { margin-top: 28px; min-height: 0; }
  .score-loading {
    color: #6b7280;
    font-size: 14px;
    font-style: italic;
    padding: 12px 0;
  }
  .score-error {
    color: #b91c1c;
    background: #fef2f2;
    border-left: 3px solid #b91c1c;
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 13px;
  }
  .score-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 24px;
    animation: trans-pop 0.25s ease-out;
  }
  .score-card .band-row {
    display: flex;
    align-items: baseline;
    gap: 16px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid #e5e7eb;
  }
  .score-card .band-num {
    font-size: 38px;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1;
    letter-spacing: -1px;
  }
  .score-card .band-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #6b7280;
    text-transform: uppercase;
  }
  .score-card .sub-row { display: flex; gap: 24px; flex-wrap: wrap; margin-bottom: 16px; }
  .score-card .sub { font-size: 12px; color: #6b7280; }
  .score-card .sub b { display: block; font-size: 18px; color: #111827; font-weight: 600; }
  .score-card .words-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #6b7280;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .score-card .words { font-size: 17px; line-height: 1.7; }
  .score-card .score-word {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 4px;
    margin: 0 1px;
    font-weight: 500;
  }
  .score-card .score-word.good { background: #dcfce7; color: #14532d; }
  .score-card .score-word.ok   { background: #fef3c7; color: #78350f; }
  .score-card .score-word.poor { background: #fee2e2; color: #7f1d1d; }
  .score-card .replay-row { margin-top: 12px; }
  .score-card .replay-rec {
    background: transparent;
    border: 1px solid #d1d5db;
    color: #4b5563;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    cursor: pointer;
    font-family: inherit;
  }
  .score-card .replay-rec:hover { border-color: #1e3a8a; color: #1e3a8a; }

  .word, .blank.revealed { cursor: pointer; }
  .word:hover, .blank.revealed:hover {
    background: rgba(59, 130, 246, 0.12);
    border-radius: 3px;
  }
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
  .answer.hidden-all {
    color: #9ca3af;
    font-style: italic;
    font-size: 22px;
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

  .audio-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 24px;
    flex-wrap: wrap;
  }
  .play-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #1e3a8a;
    color: #fff;
    border: none;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
    letter-spacing: 0.3px;
  }
  .play-btn:hover { background: #1e40af; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(30,58,138,0.25); }
  .play-btn:active { transform: translateY(0); }
  .play-btn.playing { background: #c2410c; }
  .play-btn.playing:hover { background: #9a3412; }
  .play-btn.paused { background: #6366f1; }
  .play-btn.paused:hover { background: #4f46e5; }
  .play-btn .icon { font-size: 16px; line-height: 1; margin-right: 6px; }
  .play-btn .play-btn-text { display: inline-block; }
  .play-btn kbd {
    background: rgba(255,255,255,0.18);
    color: #fff;
    border: none;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-family: inherit;
    margin-left: 8px;
  }

  .speed-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
  }
  .speed-trigger {
    width: 38px;
    height: 38px;
    padding: 0;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 700;
    color: #4b5563;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.12s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    letter-spacing: -0.3px;
  }
  .speed-trigger:hover { background: #e5e7eb; color: #1e3a8a; border-color: #1e3a8a; }
  .speed-trigger.menu-open { background: #1e3a8a; color: #fff; border-color: #1e3a8a; }
  .speed-menu {
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    padding: 4px;
    display: none;
    min-width: 130px;
    z-index: 10;
  }
  .speed-menu.open { display: block; }
  .speed-menu .speed-opt {
    display: flex;
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 12px;
    font-weight: 500;
    color: #374151;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.1s;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }
  .speed-menu .speed-opt:hover { background: #f3f4f6; }
  .speed-menu .speed-opt.active { background: #1e3a8a; color: #fff; }
  .speed-menu .speed-opt .rate { font-weight: 700; }
  .speed-menu .speed-opt .name { font-size: 11px; opacity: 0.7; }
</style>
</head>
<body>

<header>
  <div class="topic-tag"><a href="/">← Decks</a> &nbsp;·&nbsp; <span id="topic-name">Topic __TOPIC_NUM__ · __TOPIC_TITLE__</span></div>
  <div class="counter" id="counter">1 / 50</div>
</header>

<div class="slide-container">
  <div class="card" id="card">
    <!-- slide rendered here -->
  </div>
</div>

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

// Cloudflare Worker URL for pronunciation scoring (Speechace proxy).
// Set after `wrangler deploy` (see cloudflare-worker/README.md). Empty -> recording UI hidden.
const PRONUNCIATION_WORKER_URL = "";

const QUESTIONS = __QUESTIONS_JSON__;

const slides = [];
QUESTIONS.forEach((item, qi) => {
  for (let lvl = 0; lvl <= 4; lvl++) {
    slides.push({ qIndex: qi, level: lvl });
  }
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
  const shouldHide = (hideAtLevel === 1 && currentLevel >= 2) ||
                     (hideAtLevel === 2 && currentLevel >= 3);
  if (shouldHide) {
    return pre + `<span class="blank" data-word="${escAttr(word)}" data-idx="${idx}">${NBSP_CHAR.repeat(Math.max(3, word.length))}</span>` + post;
  }
  return pre + `<span class="word" data-idx="${idx}">${word}</span>` + post;
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


let currentAudio = null;
let karaokeRAF = null;
let karaokeWords = [];
let playbackRate = parseFloat(localStorage.getItem('ielts_speed') || '1.0');

function setSpeed(rate) {
  playbackRate = rate;
  localStorage.setItem('ielts_speed', String(rate));
  if (currentAudio) currentAudio.playbackRate = rate;
  document.querySelectorAll('.speed-opt').forEach(b => {
    b.classList.toggle('active', parseFloat(b.dataset.rate) === rate);
  });
  document.querySelectorAll('.speed-trigger').forEach(l => {
    l.textContent = `${rate}×`;
  });
  closeSpeedMenu();
}

function toggleSpeedMenu(ev) {
  ev.stopPropagation();
  const menu = document.querySelector('.speed-menu');
  const trigger = document.querySelector('.speed-trigger');
  if (menu) menu.classList.toggle('open');
  if (trigger) trigger.classList.toggle('menu-open', menu && menu.classList.contains('open'));
}

function closeSpeedMenu() {
  const menu = document.querySelector('.speed-menu');
  const trigger = document.querySelector('.speed-trigger');
  if (menu) menu.classList.remove('open');
  if (trigger) trigger.classList.remove('menu-open');
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('.speed-wrap')) closeSpeedMenu();

  // Close translation popup if click outside
  if (!e.target.closest('.trans-popup, .word, .blank')) closeTranslation();

  const blank = e.target.closest('.blank');
  if (blank && blank.dataset.word && !blank.classList.contains('revealed')) {
    revealBlank(blank);
    return;
  }

  // Word click → translate. Also blanks already revealed.
  const wordEl = e.target.closest('.word, .blank.revealed');
  if (wordEl && !e.target.closest('.trans-popup')) {
    showTranslation(wordEl);
  }
});

function clearKaraoke() {
  document.querySelectorAll('.speaking').forEach(el => el.classList.remove('speaking'));
  if (karaokeRAF) { cancelAnimationFrame(karaokeRAF); karaokeRAF = null; }
}

function getWordWeight(el) {
  const txt = el.dataset.word || el.textContent.trim();
  // Base weight: phoneme-ish proxy via char count, clamped
  let w = Math.max(2, txt.length);
  // Plus extra "time" for trailing punctuation (acts like a pause)
  let n = el.nextSibling;
  let scanned = '';
  while (n && n.nodeType === 3 /* TEXT_NODE */ && scanned.length < 8) {
    scanned += n.textContent;
    if (/\S/.test(n.textContent)) break;
    n = n.nextSibling;
  }
  if (/[.!?]/.test(scanned))      w += 6;   // sentence end
  else if (/[—–]/.test(scanned))  w += 4;   // em/en dash
  else if (/[,;:]/.test(scanned)) w += 3;   // mid-clause comma
  return w;
}

function startKaraoke() {
  const container = document.querySelector('.answer') || document.querySelector('.question');
  if (!container) return;
  karaokeWords = Array.from(container.querySelectorAll('.word, .blank'));
  if (karaokeWords.length === 0) return;
  const dur = currentAudio.duration;
  if (!dur || !isFinite(dur)) return;

  // Empirical: Cori voice has a small lead-in pause; trim a touch off the start.
  const leadIn = Math.min(0.15, dur * 0.03);
  const usable = dur - leadIn;

  const weights = karaokeWords.map(getWordWeight);
  const total = weights.reduce((a, b) => a + b, 0);
  let cum = leadIn;
  karaokeWords.forEach((el, i) => {
    const slice = (weights[i] / total) * usable;
    el._s = cum;
    cum += slice;
    el._e = cum;
  });

  let lastIdx = -1;
  function tick() {
    if (!currentAudio || currentAudio.paused) return;
    const t = currentAudio.currentTime;
    // Linear scan from lastIdx forward (cheaper than binary search for small N)
    let idx = lastIdx;
    if (idx < 0 || t < karaokeWords[idx]._s || t >= karaokeWords[idx]._e) {
      idx = karaokeWords.findIndex(el => t < el._e);
      if (idx < 0) idx = karaokeWords.length - 1;
    }
    if (idx !== lastIdx) {
      if (lastIdx >= 0) karaokeWords[lastIdx].classList.remove('speaking');
      karaokeWords[idx].classList.add('speaking');
      lastIdx = idx;
    }
    karaokeRAF = requestAnimationFrame(tick);
  }
  karaokeRAF = requestAnimationFrame(tick);
}

function revealBlank(el) {
  if (!el.classList.contains('blank') || !el.dataset.word) return;
  el.classList.add('revealing');
  setTimeout(() => {
    el.textContent = el.dataset.word;
    el.classList.add('revealed');
  }, 175);
  setTimeout(() => el.classList.remove('revealing'), 360);
}

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

let currentSrc = null;

function setPlayBtnState(state) {
  const btn = document.querySelector('.play-btn');
  if (!btn) return;
  const iconEl = btn.querySelector('.icon');
  const textEl = btn.querySelector('.play-btn-text');
  const orig = btn.dataset.label || 'Play';
  btn.classList.toggle('playing', state === 'playing');
  btn.classList.toggle('paused', state === 'paused');
  if (state === 'playing') {
    if (iconEl) iconEl.textContent = '⏸';
    if (textEl) textEl.textContent = 'Pause';
  } else if (state === 'paused') {
    if (iconEl) iconEl.textContent = '▶';
    if (textEl) textEl.textContent = 'Resume';
  } else {
    if (iconEl) iconEl.textContent = '▶';
    if (textEl) textEl.textContent = orig;
  }
}

function playAudio(src) {
  if (currentAudio && currentSrc === src && !currentAudio.ended) {
    if (currentAudio.paused) currentAudio.play();
    else currentAudio.pause();
    return;
  }
  clearKaraoke();
  if (currentAudio) { try { currentAudio.pause(); } catch(e){} currentAudio = null; }
  currentSrc = src;
  currentAudio = new Audio(src);
  currentAudio.playbackRate = playbackRate;
  currentAudio.addEventListener('loadedmetadata', startKaraoke);
  currentAudio.addEventListener('play', () => { setPlayBtnState('playing'); startKaraoke(); });
  currentAudio.addEventListener('pause', () => {
    if (currentAudio && !currentAudio.ended) {
      setPlayBtnState('paused');
      if (karaokeRAF) { cancelAnimationFrame(karaokeRAF); karaokeRAF = null; }
    }
  });
  currentAudio.addEventListener('ended', () => { setPlayBtnState('idle'); clearKaraoke(); });
  currentAudio.addEventListener('error', () => { setPlayBtnState('idle'); clearKaraoke(); });
  currentAudio.play().catch(() => { setPlayBtnState('idle'); clearKaraoke(); });
}

function render() {
  if (currentAudio) { currentAudio.pause(); currentAudio = null; }
  clearKaraoke();
  closeTranslation();
  const slide = slides[cursor];
  const item = QUESTIONS[slide.qIndex];
  const card = document.getElementById('card');
  document.getElementById('counter').textContent = `${cursor + 1} / ${slides.length}`;
  document.getElementById('topic-name').textContent = `Topic ${TOPIC_NUM} · ${TOPIC} · Q${slide.qIndex + 1}`;

  const qNum = slide.qIndex + 1;
  const qAudio = `audio/q${qNum}.mp3`;
  const aAudio = `audio/a${qNum}.mp3`;

  let html = '';

  const speedHtml = `
    <div class="speed-wrap">
      <button class="speed-trigger" title="Playback speed" onclick="toggleSpeedMenu(event)">${playbackRate}×</button>
      <div class="speed-menu">
        <button class="speed-opt" data-rate="0.75" onclick="setSpeed(0.75)"><span class="rate">0.75×</span><span class="name">Slow</span></button>
        <button class="speed-opt" data-rate="1" onclick="setSpeed(1)"><span class="rate">1×</span><span class="name">Normal</span></button>
        <button class="speed-opt" data-rate="1.25" onclick="setSpeed(1.25)"><span class="rate">1.25×</span><span class="name">Faster</span></button>
        <button class="speed-opt" data-rate="1.5" onclick="setSpeed(1.5)"><span class="rate">1.5×</span><span class="name">Fast</span></button>
      </div>
    </div>
  `;

  function playBtnHtml(src, label) {
    return `<button class="play-btn" data-label="${label}" onclick="playAudio('${src}')">
        <span class="icon">▶</span><span class="play-btn-text">${label}</span><kbd>P</kbd>
      </button>`;
  }

  if (slide.level === 0) {
    html = `
      <div class="level-indicator">Question</div>
      <span class="label q">Question ${qNum}</span>
      <div class="question">${renderQuestion(item.q)}</div>
      <div class="audio-row">
        ${playBtnHtml(qAudio, 'Play question')}
        ${speedHtml}
      </div>
    `;
  } else if (slide.level === 4) {
    const refText = stripMarkup(item.a);
    const recordHtml = PRONUNCIATION_WORKER_URL ? `
      <button class="record-btn" onclick="toggleRecord(this)" data-text="${escAttr(refText)}">
        <span class="rec-dot"></span><span class="rec-text">Record &amp; score</span>
      </button>
    ` : '';
    html = `
      <div class="level-indicator">Recall · Level 4</div>
      <span class="label empty">Answer</span>
      <div class="answer hidden-all">— hãy tự nói câu trả lời —</div>
      <div class="audio-row">
        ${playBtnHtml(aAudio, 'Play answer')}
        ${speedHtml}
        ${recordHtml}
      </div>
      <div class="score-result"></div>
    `;
  } else {
    let labelText = '';
    let levelTxt = '';
    if (slide.level === 1) { labelText = 'Answer · Full'; levelTxt = 'Read · Level 1'; }
    if (slide.level === 2) { labelText = 'Answer · Hide a few'; levelTxt = 'Practice · Level 2'; }
    if (slide.level === 3) { labelText = 'Answer · Hide more'; levelTxt = 'Practice · Level 3'; }
    html = `
      <div class="level-indicator">${levelTxt}</div>
      <span class="label a">${labelText}</span>
      <div class="answer">${renderAnswer(item.a, slide.level)}</div>
      <div class="audio-row">
        ${playBtnHtml(aAudio, 'Play answer')}
        ${speedHtml}
      </div>
    `;
  }

  const progressPct = ((cursor + 1) / slides.length) * 100;
  html += `<div class="progress"><div class="progress-fill" style="width:${progressPct}%"></div></div>`;

  card.innerHTML = html;

  document.querySelectorAll('.speed-opt').forEach(b => {
    b.classList.toggle('active', parseFloat(b.dataset.rate) === playbackRate);
  });
}

function next() { if (cursor < slides.length - 1) { cursor++; render(); } }
function prev() { if (cursor > 0) { cursor--; render(); } }

// --- Pronunciation scoring (Speechace via Cloudflare Worker) ---
let __mediaRecorder = null;
let __recChunks = [];
let __recBlob = null;
let __recStream = null;

async function toggleRecord(btn) {
  if (__mediaRecorder && __mediaRecorder.state === 'recording') {
    __mediaRecorder.stop();
    return;
  }
  const refText = btn.dataset.text || '';
  const resultEl = document.querySelector('.score-result');

  try {
    __recStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (e) {
    if (resultEl) resultEl.innerHTML = `<div class="score-error">Cần cấp quyền microphone để chấm điểm.</div>`;
    return;
  }

  __recChunks = [];
  __recBlob = null;
  let mimeType = 'audio/webm';
  if (window.MediaRecorder && !MediaRecorder.isTypeSupported('audio/webm')) {
    if (MediaRecorder.isTypeSupported('audio/mp4')) mimeType = 'audio/mp4';
    else mimeType = '';
  }
  __mediaRecorder = mimeType ? new MediaRecorder(__recStream, { mimeType }) : new MediaRecorder(__recStream);
  __mediaRecorder.ondataavailable = (e) => { if (e.data && e.data.size > 0) __recChunks.push(e.data); };
  __mediaRecorder.onstop = async () => {
    if (__recStream) { __recStream.getTracks().forEach(t => t.stop()); __recStream = null; }
    btn.classList.remove('recording');
    btn.querySelector('.rec-text').textContent = 'Record again';
    __recBlob = new Blob(__recChunks, { type: __mediaRecorder.mimeType || 'audio/webm' });
    await uploadAndScore(__recBlob, refText);
  };
  __mediaRecorder.start();
  btn.classList.add('recording');
  btn.querySelector('.rec-text').textContent = 'Stop recording';
  if (resultEl) resultEl.innerHTML = '';
}

async function uploadAndScore(blob, refText) {
  const resultEl = document.querySelector('.score-result');
  if (!resultEl) return;
  if (!PRONUNCIATION_WORKER_URL) {
    resultEl.innerHTML = `<div class="score-error">Worker URL chưa được cấu hình. Xem cloudflare-worker/README.md</div>`;
    return;
  }
  resultEl.innerHTML = `<div class="score-loading">Đang phân tích phát âm…</div>`;

  const fd = new FormData();
  fd.append('audio', blob, 'speech.webm');
  fd.append('text', refText);
  fd.append('dialect', 'en-gb');

  try {
    const r = await fetch(PRONUNCIATION_WORKER_URL, { method: 'POST', body: fd });
    const data = await r.json();
    if (!r.ok || data.error) {
      resultEl.innerHTML = `<div class="score-error">Lỗi: ${data.error || 'HTTP ' + r.status}</div>`;
      return;
    }
    renderScore(resultEl, data, blob);
  } catch (e) {
    resultEl.innerHTML = `<div class="score-error">Lỗi mạng: ${e.message}</div>`;
  }
}

function bandFromQuality(q) {
  // Fallback IELTS estimate from overall quality_score (0-100)
  if (q >= 85) return 8.0;
  if (q >= 75) return 7.0;
  if (q >= 65) return 6.0;
  if (q >= 55) return 5.0;
  if (q >= 45) return 4.0;
  return 3.0;
}

function renderScore(container, data, blob) {
  const ts = data.text_score || data;
  const ielts = (ts.ielts_score) || (data.ielts_score) || {};
  const words = ts.word_score_list || [];
  const overall = ielts.pronunciation || ts.quality_score || 0;
  const fluency = ielts.fluency || (ts.fluency && ts.fluency.overall_metrics && ts.fluency.overall_metrics.fluency_score) || null;

  const band = (typeof overall === 'number' && overall <= 9) ? overall : bandFromQuality(overall);

  let wordsHtml = '';
  for (const w of words) {
    const q = (w.quality_score != null ? w.quality_score : (w.word_score && w.word_score.quality_score)) || 0;
    const cls = q >= 80 ? 'good' : q >= 60 ? 'ok' : 'poor';
    wordsHtml += `<span class="score-word ${cls}" title="quality ${q}">${w.word}</span> `;
  }

  let subRow = '';
  if (fluency != null) subRow += `<div class="sub">Fluency<b>${Math.round(fluency)}</b></div>`;
  if (ts.quality_score != null && typeof overall === 'number' && overall <= 9) {
    subRow += `<div class="sub">Quality<b>${Math.round(ts.quality_score)}/100</b></div>`;
  }

  const audioUrl = URL.createObjectURL(blob);

  container.innerHTML = `
    <div class="score-card">
      <div class="band-row">
        <div class="band-num">${band.toFixed(1)}</div>
        <div class="band-label">Pronunciation band</div>
      </div>
      ${subRow ? `<div class="sub-row">${subRow}</div>` : ''}
      <div class="words-label">Word-level</div>
      <div class="words">${wordsHtml || '<span style="color:#9ca3af">No word breakdown available.</span>'}</div>
      <div class="replay-row">
        <audio src="${audioUrl}" controls style="height:32px; vertical-align:middle"></audio>
      </div>
    </div>
  `;
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
  else if (e.key === 'Home') { cursor = 0; render(); }
  else if (e.key === 'End') { cursor = slides.length - 1; render(); }
  else if (e.key === 'p' || e.key === 'P') { e.preventDefault(); const btn = document.querySelector('.play-btn'); if (btn) btn.click(); }
  else if (e.key === 'Escape') { closeTranslation(); closeSpeedMenu(); }
});

render();
</script>

</body>
</html>
"""

TOPICS = [
    {"n": 1, "slug": "hometown", "title": "Hometown", "questions": [
        {"q": "Where is your hometown?",
         "a": "My hometown is ~~Dong Thap~~, a ~~small province~~ in the ~~Mekong Delta~~ region of ~~southern Vietnam~~. It's about a ==three-hour drive== from ~~Ho Chi Minh City~~, where I currently ==live and work== as a ~~backend developer~~."},
        {"q": "What's your hometown like?",
         "a": "It's a ~~quiet, rural area~~ surrounded by ~~rice fields~~, ~~lotus ponds~~, and ~~rivers~~. The ==pace of life== is ~~super slow~~ compared to ~~Saigon~~ — people are ~~friendly~~, the food is ~~fresh~~, and you can hear ~~birds~~ in the morning instead of ~~motorbikes~~."},
        {"q": "Is your hometown a popular place?",
         "a": "Not really, it's not a ~~major tourist destination~~. But ~~Sa Dec~~ — a ~~flower village~~ in my province — gets a ==fair number== of visitors during ~~Tet~~ for the ~~flower season~~. Most outsiders haven't really ==heard of== ~~Dong Thap~~."},
        {"q": "Do you like your hometown?",
         "a": "Yeah, I really do. The food is ~~incredible~~ — especially ~~hu tieu Sa Dec~~ — and I love how ~~peaceful~~ it feels. Whenever ~~Saigon~~ gets too ~~overwhelming~~, going home for a ==weekend== ~~recharges~~ me completely."},
        {"q": "Has your hometown changed much in recent years?",
         "a": "A bit, but not ~~dramatically~~. ~~New roads~~ make travel ~~easier~~, and a few ~~coffee shops~~ have opened up in town. But the core feel — ~~rural, slow, agricultural~~ — has stayed ==pretty much the same==. Honestly I think that's a ~~good thing~~."},
        {"q": "What do you like most about your hometown?",
         "a": "==Honestly==, the ~~food and the quietness~~. I can wake up, grab a ~~Vietnamese drip coffee~~ at a ~~riverside cafe~~, and just ~~watch boats~~ pass by for hours. That kind of ~~stillness~~ is ==impossible to find== in ~~Saigon~~."},
        {"q": "Is there anything you don't like about it?",
         "a": "Career-wise, it's ~~tough~~. There aren't many ~~tech jobs~~ in the area — I work as a ~~backend Golang developer~~, so I had to ~~move to Saigon~~. Also, the ~~summer heat~~ in the ~~Mekong~~ can be ==pretty intense==."},
        {"q": "Would you like to live there in the future?",
         "a": "Maybe in the ~~long run~~. Right now I need to be in ~~Saigon~~ for my ~~career~~, but once I'm more ~~established~~ or working ~~remotely~~ full-time, I'd love to ~~move back~~. The ~~quality of life~~ there is ==hard to beat==."},
        {"q": "What's the best thing about living there?",
         "a": "For me, it's the ~~cost of living~~ and how ~~close everyone~~ is. My whole ~~family~~ lives within a ~~few kilometers~~, food is ~~dirt cheap~~, and there's almost no ~~traffic~~. Life is just ==a lot simpler==."},
        {"q": "How long have you lived there?",
         "a": "I grew up there until I was ~~18~~, so about ~~18 years~~ in total. After ~~high school~~ I moved to ~~Saigon~~ for ~~university~~, and I've been ==based== there ever since — but I still go back ~~two or three times a year~~."},
    ]},

    {"n": 2, "slug": "work", "title": "Work", "questions": [
        {"q": "What do you do?",
         "a": "I work as a ~~backend developer~~ at a ~~tech company~~ in ~~Saigon~~. Specifically, I write code in ~~Go — or Golang~~, building ~~APIs and services~~ that ==power web and mobile apps==."},
        {"q": "Why did you choose that job?",
         "a": "Honestly, I've always loved ~~problem-solving~~ and ~~building things from scratch~~. ~~Backend~~ feels like the ~~engine room~~ of any product — ~~invisible but critical~~. Also, the ~~pay~~ in ==Vietnam's tech industry== is pretty solid."},
        {"q": "Do you like your job?",
         "a": "Yeah, most days I really enjoy it. There's always something ~~new to learn~~ — a ~~new framework~~, a ~~tricky bug~~, or a ~~system to optimize~~. The ~~bad days~~ are usually when ==meetings eat up== all my ~~coding time~~."},
        {"q": "What's a typical day like at work?",
         "a": "I usually start around ~~9 with a stand-up meeting~~, then I spend most of the morning ~~coding~~. Afternoons are often for ~~code reviews~~ or ~~debugging~~. I try to ==wrap up by 6== so I can grab ~~dinner~~ and relax."},
        {"q": "Do you work with a team or alone?",
         "a": "Mostly with a team. There are about ~~six engineers~~ on my squad, plus a ~~product manager~~ and a ~~designer~~. We collaborate on ~~Slack and GitHub~~ all day, which makes ==remote work pretty smooth==."},
        {"q": "What's the best thing about your job?",
         "a": "Probably the ~~flexibility~~. As long as I ~~deliver on time~~, no one ~~micromanages~~ how or where I work. I can take a ~~long lunch~~ for ~~coffee~~ or ~~work from a cafe~~ — that ==kind of freedom== matters a lot."},
        {"q": "Is there anything you don't like about it?",
         "a": "Sometimes the ~~deadlines~~ can be ~~brutal~~, especially before a ~~product launch~~. Also, sitting in front of a ~~screen~~ for ~~nine hours straight~~ is ==rough on== the ~~eyes and the back~~."},
        {"q": "Do you plan to stay in this field?",
         "a": "Yeah, definitely. ~~Tech moves so fast~~ that even within ~~backend~~ there's ~~endless room to grow~~ — like ~~system design at scale~~ or moving into ~~infrastructure~~. I see myself in this field for ==the long haul==."},
        {"q": "What skills do you need for your job?",
         "a": "~~Strong logical thinking~~ is the obvious one, but ~~communication~~ matters just as much. You have to ~~explain technical decisions~~ to ~~non-technical people~~ without ==sounding condescending==. Also, ~~English~~ is essential."},
        {"q": "Did you study something related to your current job?",
         "a": "Yes, I majored in ~~Computer Science~~ at ~~university in Saigon~~. The theoretical stuff — ~~algorithms and data structures~~ — was useful, but honestly I learned most ~~practical skills~~ through ==side projects and online courses==."},
    ]},

    {"n": 3, "slug": "hobbies", "title": "Hobbies", "questions": [
        {"q": "What do you do in your free time?",
         "a": "It depends on the day. On ~~weekdays~~, I usually wind down with a ~~quiet coffee and a book~~. On ~~weekends~~, I either go out for ~~badminton with friends~~ or take ~~short trips~~ ==somewhere outside the city==."},
        {"q": "Do you have any hobbies?",
         "a": "Yeah, a few. I'm really into ~~specialty coffee~~ — like ~~trying different beans~~ and ~~brewing methods at home~~. I also play ~~badminton casually~~, and ~~travel~~ whenever I can ==save up enough vacation days==."},
        {"q": "How long have you had this hobby?",
         "a": "~~Coffee~~ has been a thing for me for about ~~five or six years~~ now. It started as just ~~caffeine for work~~ but slowly turned into ==a proper interest==. ~~Travel~~ — I've loved that since ~~university~~."},
        {"q": "Why do you enjoy it?",
         "a": "~~Coffee~~ is ~~meditative~~. The whole process of ~~grinding beans~~, ~~weighing~~, and ~~brewing~~ forces me to ~~slow down~~ — a nice contrast to ==coding all day==. With ~~travel~~, it gets me out of my ~~routine~~."},
        {"q": "Do you do it alone or with others?",
         "a": "~~Coffee~~ is mostly a ~~solo thing~~ — I genuinely enjoy that ~~quiet morning ritual~~. ~~Badminton~~ I always play with ~~friends~~, usually a group of ~~four or five~~. ~~Travel~~ can be either, ==depending on my mood==."},
        {"q": "Is it expensive?",
         "a": "~~Coffee~~ can get pricey if you go down the ~~rabbit hole~~ — ~~good beans~~, a ~~decent grinder~~, all that gear adds up. ~~Badminton~~ is cheap — just ~~court fees and shuttlecocks~~. ~~Travel~~ is ==the most expensive==."},
        {"q": "Has your hobby changed over the years?",
         "a": "A bit. I used to play ~~badminton more seriously~~ in ~~college~~, but now it's just ~~casual~~. With ~~coffee~~, I've gone deeper — from ~~instant~~ to ~~hand-brewed pour-overs~~. Travel-wise, I've shifted from ~~cheap backpacking~~ to ==more comfortable trips==."},
        {"q": "Would you recommend it to others?",
         "a": "~~Coffee~~, absolutely — even casually, learning to make a ~~decent cup at home~~ is ~~rewarding~~. ~~Badminton~~ is great for anyone who wants ~~exercise without joining a gym~~. ~~Travel~~ ==speaks for itself==."},
        {"q": "Do you spend a lot of time on it?",
         "a": "Maybe ~~an hour a day~~ on ~~coffee~~, between ~~brewing~~ and just enjoying it. ~~Badminton~~ is ~~two hours once or twice a week~~. ~~Travel~~ is more sporadic — ==a weekend trip a month== and a longer trip every few months."},
        {"q": "Did your hobby change during the pandemic?",
         "a": "Definitely. ~~Travel~~ obviously got ~~killed~~ for a couple of years, so I doubled down on ~~home coffee~~ — that's actually when I bought my first ~~espresso machine~~. ~~Badminton~~ came back ==the moment courts reopened==."},
    ]},

    {"n": 4, "slug": "family", "title": "Family", "questions": [
        {"q": "Do you have a big family?",
         "a": "Mine is ~~pretty average~~ for Vietnam — my ~~parents~~, an ~~older sister~~, and me. We have a lot of ~~relatives in Dong Thap~~ though, like ~~cousins, aunts and uncles~~, so ==family gatherings get pretty crowded==."},
        {"q": "Who do you live with now?",
         "a": "I live ~~alone in Saigon~~. I rent a ~~small apartment~~ near my office. My family is back in ~~Dong Thap~~, so it's just me, ~~a coffee setup~~, and ==a lot of takeout boxes== during the week."},
        {"q": "Are you close to your family?",
         "a": "Yeah, very. We're not the type that talks ~~every single day~~, but there's a ~~strong sense of connection~~. My ~~mom calls me twice a week~~ to make sure I'm ==eating properly== — which honestly, I'm not always."},
        {"q": "How often do you see your family?",
         "a": "Probably ~~once a month~~ if I can manage it. The ~~bus from Saigon to Dong Thap~~ takes about ~~three hours~~, so it's doable for a ~~long weekend~~. ~~Tet holiday~~ I always go back for ==at least a week==."},
        {"q": "Who are you closest to in your family?",
         "a": "Definitely my ~~older sister~~. She's only ~~two years older~~, so we ~~grew up doing everything together~~. Even now, she's the one I ~~call first~~ when I need ~~advice~~ — about ==work, life, or anything==."},
        {"q": "Do you spend much time with your family?",
         "a": "~~Less than I'd like~~, honestly. ~~Living far away~~ makes ~~daily contact~~ tough. But I try to be ~~fully present~~ when I am home — ~~phone away~~, ==helping in the kitchen==, just hanging out instead of being on my laptop."},
        {"q": "What activities do you do together?",
         "a": "Mostly ~~cooking and eating~~. My ~~mom is an amazing cook~~ and ~~family meals~~ are kind of ~~sacred~~. Sometimes we ~~watch movies after dinner~~, or ==take walks along the river== when the weather's nice."},
        {"q": "Has your family influenced your career?",
         "a": "~~Indirectly~~, yeah. My parents always emphasized ~~education over everything~~, which pushed me toward ~~university~~ and ultimately a ~~tech career~~. They didn't ~~tell me what to study~~, but ==the value of learning== was non-negotiable."},
        {"q": "Do you want to have your own family in the future?",
         "a": "~~Eventually~~, yeah, though I'm not in a ~~rush~~. I want to be more ~~financially stable~~ and probably ~~own a place~~ before ~~settling down~~. Maybe in ==five or six years== — we'll see."},
        {"q": "Has your family changed in recent years?",
         "a": "A bit. My ~~sister got married~~ last year and has her ~~own place~~ now, so it's quieter when I visit. My ~~parents are getting older~~ too, which makes me think more about ==going back home eventually==."},
    ]},

    {"n": 5, "slug": "daily-routine", "title": "Daily Routine", "questions": [
        {"q": "What's your daily routine like?",
         "a": "On ~~weekdays~~ it's pretty consistent. I ~~wake up around 7~~, ~~brew coffee~~, ~~check Slack~~, then ~~code from 9 to 6~~ with a lunch break. Evenings are flexible — sometimes ==a workout==, sometimes just ~~dinner and Netflix~~."},
        {"q": "Are you a morning person or a night person?",
         "a": "I used to be a ~~night owl in college~~, but these days I'm more of a ~~morning person~~. I find I ~~think more clearly before noon~~, so I try to do my ~~hardest coding work~~ ==early in the day==."},
        {"q": "What time do you usually wake up?",
         "a": "Around ~~7am on weekdays~~. On ~~weekends~~ I let myself sleep in until ~~8 or 9~~, but rarely later — I get ~~restless~~ if I waste the morning. The first thing I do is ==make coffee, no exceptions==."},
        {"q": "Do you have the same routine every day?",
         "a": "Pretty much, ~~Monday through Friday~~. ~~Weekends~~ are different — I might have ~~badminton in the morning~~, ~~brunch with friends~~, or ~~hop on a bus somewhere~~. The routine ==helps me stay productive==."},
        {"q": "What's the most important part of your day?",
         "a": "Honestly, my ~~morning coffee ritual~~. It's only ~~fifteen minutes~~, but it ~~sets the tone for the whole day~~ — I'm ~~calm, focused, and not rushing~~ into work. Skipping it ==makes me feel off==."},
        {"q": "Do you ever change your routine?",
         "a": "Yeah, especially when I'm ~~traveling~~ or ~~visiting home~~. The routine gets ~~thrown out~~, which is actually ~~nice for a few days~~. After about a week though, I ==start craving the structure== again."},
        {"q": "What do you usually do on weekends?",
         "a": "~~Saturdays~~ are for activities — ~~badminton~~, ~~exploring a new cafe~~, or a ~~short trip nearby~~. ~~Sundays~~ I keep slow — ~~laundry~~, ~~meal prep~~, maybe a ~~long lunch~~, and ==an evening walk==."},
        {"q": "How do you usually relax in the evening?",
         "a": "After dinner I'll either ~~read~~, ~~watch a series~~, or sometimes ~~call my family~~. Around ~~10~~ I try to ~~put my phone away~~ and ~~wind down~~ — though that's ==hit or miss==, I'll be honest."},
        {"q": "Has your routine changed over the years?",
         "a": "A lot. As a ~~student~~, my schedule was ~~all over the place~~ — ~~late nights~~, ~~no consistent meals~~. Once I started ~~working full-time~~ and especially since ~~the pandemic~~, I built a ==much more structured day==."},
        {"q": "Would you like to change your routine?",
         "a": "Maybe ~~add more exercise~~. I sit too much because of my job, so adding ~~morning runs or yoga~~ would be a ~~good move~~. Otherwise, I'm pretty content with ==how my days look==."},
    ]},

    {"n": 6, "slug": "food", "title": "Food", "questions": [
        {"q": "What kind of food do you like?",
         "a": "I love anything ~~Vietnamese~~ — I'd say I'm ~~pretty loyal~~ to ~~local food~~. I'm also into ~~Japanese cuisine~~, especially ~~ramen and sushi~~. ~~Saigon~~ has a great variety, so I ==rarely run out of options==."},
        {"q": "What's your favorite dish?",
         "a": "Has to be ~~hu tieu Sa Dec~~ — a ~~noodle soup from my hometown~~ in ~~Dong Thap~~. The ~~broth is clear but really flavorful~~, and nothing made in Saigon quite matches ==what my mom makes==. Pure comfort food."},
        {"q": "Do you cook at home or eat out?",
         "a": "Mostly ~~eat out~~, honestly. I ~~live alone~~ and there's ~~amazing street food on every corner~~ in Saigon. I do cook on ~~weekends~~ sometimes — ~~simple stuff like fried rice~~ — but ==I'm not a serious home cook==."},
        {"q": "Are you a picky eater?",
         "a": "~~Not at all~~. I'll try ~~almost anything once~~. The only things I really avoid are ~~super spicy food~~ and ~~certain organ meats~~ — those are ~~common here~~ but ==never grew on me==."},
        {"q": "Do you prefer Vietnamese food or foreign food?",
         "a": "~~Vietnamese, hands down~~. It just ~~tastes like home~~. But if I'm being practical, I'll happily eat ~~foreign food a few times a week~~ for ~~variety~~. Variety is ==what makes Saigon's food scene so good==."},
        {"q": "Do you like trying new food?",
         "a": "Yeah, especially when I ~~travel~~. ~~Trying local food~~ is ~~half the reason~~ I travel in the first place. Even in ~~Saigon~~, when a ~~new restaurant opens~~, I'll usually go check it out ==within the first month==."},
        {"q": "Has your taste in food changed?",
         "a": "A bit. As a kid I was ~~way pickier~~ — wouldn't ~~touch fish~~ or anything ~~sour~~. Now I love both. ~~Coffee~~ is another one — used to ~~hate the bitterness~~, but somewhere in ==my early 20s== I learned to appreciate it."},
        {"q": "Do you eat healthy food?",
         "a": "~~Sort of~~. I try to ~~balance things out~~ — if I have ~~street food for lunch~~, I'll cook a ~~salad~~ or grab ~~something light for dinner~~. I'm ~~not strict~~ about it, but ==I pay attention==."},
        {"q": "What food don't you like?",
         "a": "I'm not a fan of ~~really spicy food~~ — anything with ~~too much chili~~ just ~~kills my taste buds~~. Also, ~~durian~~. I know it's a ~~Vietnamese specialty~~, but I really cannot ==get past the smell==."},
        {"q": "Did your parents teach you to cook?",
         "a": "My ~~mom~~ taught me the ~~basics~~ — how to ~~cook rice properly~~, ~~simple stir-fries~~, that kind of thing. The rest I picked up from ~~YouTube and trial and error~~ after ==moving to Saigon==."},
    ]},

    {"n": 7, "slug": "music", "title": "Music", "questions": [
        {"q": "Do you like listening to music?",
         "a": "~~Definitely~~. Music is on for ~~most of my workday~~ — it helps me ~~focus when I'm coding~~. Without music, the ~~office or my apartment~~ feels ==too quiet, weirdly==."},
        {"q": "What kind of music do you like?",
         "a": "Mostly ~~chill stuff~~ — ~~lo-fi~~, ~~indie~~, ~~acoustic singer-songwriter~~. When I'm coding I need something ~~without lyrics~~. On weekends I'll throw on ==Vietnamese indie or some pop==."},
        {"q": "When do you usually listen to music?",
         "a": "Pretty much ~~all day~~. Music ~~while I work~~, music ~~in the gym~~, even music ~~while I'm cooking~~. The only time I don't listen is during ~~meetings~~, or ==when I'm trying to fall asleep==."},
        {"q": "Do you play any musical instruments?",
         "a": "I picked up the ~~guitar in high school~~ and got ~~reasonably okay~~ at it. I haven't ~~touched it much since university~~ though — it's ~~collecting dust in the corner~~. I keep telling myself ==I'll start again==."},
        {"q": "Has your taste in music changed?",
         "a": "A lot. As a teenager I was into ~~rock and metal~~ — ~~Linkin Park, Green Day~~. As I got older I shifted toward ~~calmer genres~~. Now anything ~~too aggressive~~ just feels ==exhausting to listen to==."},
        {"q": "Do you like live music?",
         "a": "Yeah, when I get the chance. There aren't ~~tons of concerts in Saigon~~, but I've been to a few ~~small acoustic shows at cafes~~. There's something about ~~live performance~~ that ==recordings can't capture==."},
        {"q": "Is music important in your daily life?",
         "a": "~~Hugely~~. It's like ~~background noise that shapes my mood~~. A ~~good playlist~~ can turn a ~~tedious task~~ into something ~~almost enjoyable~~. Without it, the day just ==feels flatter==."},
        {"q": "Do you sing?",
         "a": "Only in the ~~shower~~ or when ~~no one's around~~. ~~Karaoke is huge in Vietnam~~, and my friends drag me out sometimes — I'll do it once ==enough beer is involved==. I'm aware I'm not good."},
        {"q": "What music was popular when you were young?",
         "a": "~~V-pop~~ and a lot of ~~K-pop~~, especially around the ~~early 2010s~~. ~~Big Bang and Super Junior~~ were everywhere. I wasn't into it then, but those songs ==trigger major nostalgia== now."},
        {"q": "Do people in your country listen to a lot of music?",
         "a": "~~Absolutely~~, music is everywhere in Vietnam. ~~Cafes, taxis, weddings~~, even ~~sidewalk shops~~. ~~Karaoke~~ especially is a ~~huge cultural thing~~ — almost every gathering ends with ==someone grabbing a microphone==."},
    ]},

    {"n": 8, "slug": "weather", "title": "Weather", "questions": [
        {"q": "What's the weather like in your country?",
         "a": "Vietnam is mostly ~~tropical~~, so it's ~~warm year-round~~. The ~~south~~, where I live, basically has ~~two seasons~~ — ~~dry and rainy~~. The ~~north~~ gets ~~actual winter~~, which I've ==never really experienced==."},
        {"q": "Do you prefer hot or cold weather?",
         "a": "~~Cooler weather~~, honestly. I've lived my ~~whole life in the hot south~~, so anything ~~below 25 feels like a gift~~. When I travel to ~~Da Lat or Sapa~~ I always overpack jackets just to ==enjoy the chill==."},
        {"q": "What's your favorite season?",
         "a": "The ~~dry season~~, ~~January through March~~. The ~~mornings are cool~~, the ~~humidity drops~~, and you can actually go outside ~~without sweating through your shirt~~. It's the ==best time to be in Saigon==."},
        {"q": "Does weather affect your mood?",
         "a": "Yeah, more than I want to admit. A ~~grey, rainy week~~ can really ~~drag my energy down~~, especially with how much I rely on ~~going out for coffee~~. ~~Sunny mornings~~ just ==hit different==."},
        {"q": "Do you check the weather forecast?",
         "a": "Almost every morning, especially during ~~rainy season~~. ~~Saigon rain is intense~~ — if I don't check, I'll get ~~drenched on my motorbike commute~~. The ~~forecasts here aren't always accurate~~, but ==better than nothing==."},
        {"q": "Has the weather changed in your country?",
         "a": "Definitely. The ~~rainy season~~ feels ~~heavier and less predictable~~ than I remember as a kid. ~~Heat waves~~ are ~~longer and more intense~~. Hard to ==deny climate change== when you can feel it."},
        {"q": "What do you do in bad weather?",
         "a": "If it's a ~~heavy rain day~~, I just ~~stay in~~. ~~Cook something at home~~, brew an ~~extra cup of coffee~~, ~~work from the apartment~~ if possible. There's something ==cozy about it== once you're not stuck out in it."},
        {"q": "Is there a season you don't like?",
         "a": "The ~~peak rainy months~~, around ~~August and September~~. The ~~flooding in some Saigon districts~~ is ~~brutal~~, and ~~getting around becomes a nightmare~~. My motorbike rides become ==a whole survival event==."},
        {"q": "Do you like rainy days?",
         "a": "Occasionally, when I'm ~~already at home~~. The ~~sound of rain is calming~~, and a ~~hot coffee plus a book on a rainy afternoon~~ is genuinely one of my favorite things. But I hate ==getting caught in it outside==."},
        {"q": "Does the weather affect your activities?",
         "a": "Yeah, a lot. ~~Rainy days~~ kill my plans for ~~badminton or any outdoor activity~~. On the flip side, ~~cool mornings~~ make me much more likely to ~~go for a walk~~ — weather basically ==dictates my weekends==."},
    ]},

    {"n": 9, "slug": "sports", "title": "Sports", "questions": [
        {"q": "Do you play any sports?",
         "a": "I play ~~badminton casually~~ with friends, usually ~~once or twice a week~~. I'm not on any team — just a ~~fun way to get exercise~~ and ~~hang out outside of work~~. It ==beats the gym for me==."},
        {"q": "What sports do you like to watch?",
         "a": "~~Football~~ is the big one. ~~Vietnamese national team matches~~ especially — ~~half the country~~ is glued to the TV. I also watch a bit of ~~Premier League~~, mostly ~~Manchester United~~, though they've been ==disappointing for years==."},
        {"q": "Did you play sports as a kid?",
         "a": "Quite a bit. I played ~~football in the village fields~~ with my ~~cousins~~, and ~~badminton~~ was already big in school. We didn't have ~~proper facilities~~ — we'd hang a net between ==two trees==. Super casual."},
        {"q": "Are sports popular in your country?",
         "a": "~~Football~~ is huge — it's ~~basically the national obsession~~. ~~Badminton~~ is a ~~close second~~, especially in ~~casual community settings~~. Vietnamese people love watching as much as playing — every street ==has a cafe with a screen==."},
        {"q": "Do you think sports are important?",
         "a": "Absolutely. Beyond ~~fitness~~, sports teach ~~teamwork, discipline~~, and ~~how to lose gracefully~~ — which is honestly underrated. I think a lot of ==life skills== come from showing up regularly."},
        {"q": "Have you tried any new sports recently?",
         "a": "I tried ~~pickleball~~ a few months ago — it's ~~blowing up here~~, and it was ~~surprisingly fun~~. I might pick it up more seriously if a ~~court opens nearer~~ to where I live. Other than that, ==stuck to badminton==."},
        {"q": "Do you watch sports on TV?",
         "a": "Mostly during ~~big tournaments~~ — ~~World Cup, Euro, SEA Games~~. I don't ~~follow weekly leagues~~ that closely anymore. With work, finding ~~three hours for a regular match~~ feels ==harder than it used to==."},
        {"q": "Do you prefer team sports or individual sports?",
         "a": "~~Team sports, for sure~~. The ~~social aspect~~ is half the fun for me. Playing ~~badminton doubles~~ or ~~kicking a ball around with friends~~ feels much better than ==running on a treadmill alone==."},
        {"q": "Do you think kids should play sports?",
         "a": "~~Definitely~~. Kids today spend way too much time on ~~screens~~, and sports are one of the best ways to ~~balance that out~~. It's also where they ~~make friends~~ and ==learn how to handle competition== early."},
        {"q": "What sport would you like to learn?",
         "a": "~~Tennis~~, probably. It looks ~~elegant~~ and the ~~technique is impressive~~. The barrier is just ~~cost~~ — courts and lessons in ~~Saigon get expensive fast~~. Maybe once ==my career is more settled==."},
    ]},

    {"n": 10, "slug": "travel", "title": "Travel", "questions": [
        {"q": "Do you like to travel?",
         "a": "I love it, honestly it's ~~probably my favorite thing in life~~. Travel is what I ~~save for and look forward to~~ all year. Whether it's a ~~weekend trip~~ or a ~~longer overseas vacation~~, it always ==feels worth it==."},
        {"q": "Where was your last trip?",
         "a": "I went to ~~Da Lat~~ last month with a ~~couple of friends from work~~. ~~Three days~~, ~~lots of coffee~~, ~~hiking around Tuyen Lam Lake~~ — proper escape from Saigon. The ==cool weather alone== was worth the trip."},
        {"q": "Do you prefer to travel alone or with others?",
         "a": "Both, depending on the trip. ~~Solo travel~~ is great for ~~self-reflection~~ and ~~going at my own pace~~. ~~Group trips with close friends~~ are way more fun, especially for places with ==good food or nightlife==."},
        {"q": "What kind of places do you like to visit?",
         "a": "I love ~~quieter places with good nature~~ — ~~mountains, beaches, small towns~~. ~~Big tourist cities~~ are ~~interesting once~~ but I get tired of crowds quickly. A place with ==great coffee and slow mornings== is my ideal."},
        {"q": "Do you prefer domestic or international travel?",
         "a": "~~Domestic~~ for the ~~convenience and budget~~, ~~international~~ for the ~~culture shock and excitement~~. Vietnam has ~~incredible places I haven't seen yet~~, but every overseas trip ==teaches me something== I couldn't get at home."},
        {"q": "What do you usually do when you travel?",
         "a": "I'm ~~not a huge sightseer~~ — I'd rather ~~sit in a local cafe~~ than ~~rush through ten museums~~. I love ~~trying every street food~~, ~~walking around without a strict plan~~, and ==chatting with locals when possible==."},
        {"q": "Where would you like to go in the future?",
         "a": "~~Japan~~ is at the top of my list, especially ~~Kyoto~~. The ~~mix of old culture, great food~~, and that ~~calm aesthetic~~ just speaks to me. Long-term I'd love to do a ==proper Europe trip==, maybe a month backpacking."},
        {"q": "Did you travel when you were a child?",
         "a": "~~Not much~~, honestly. My family didn't have the ~~budget for proper trips~~, and ~~Dong Thap is pretty remote~~. The biggest trips were usually to ~~relatives in nearby provinces~~ — fun, but ==not really travel==."},
        {"q": "What do you remember most about a trip?",
         "a": "My ~~first solo trip to Da Nang~~ stands out. I was ~~22~~, just ~~started my first job~~, and went there alone for a ~~long weekend~~. Nothing dramatic happened — but the ==freedom of figuring everything out alone== was unforgettable."},
        {"q": "How do you usually plan your trips?",
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
