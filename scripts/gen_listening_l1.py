#!/usr/bin/env python3
"""Generate listening/lesson/1/index.html — 25 slides (lý thuyết + chỉ Practice 01 / Cambridge 19 S1)."""

import os
from html import escape

FOOTER = "IELTS Listening · Lesson 01"
TOTAL_SLIDES = 25


def foot(n: int) -> str:
    return f'<div class="run-footer"><span class="footer-topic">{FOOTER}</span><span>{n} / {TOTAL_SLIDES}</span></div>'


HEAD = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>IELTS Listening — Predictions &amp; Form Completion · Lesson 01</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,400;1,500&family=Roboto+Slab:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<script src="/assets/deck-stage.js"></script>
<link rel="stylesheet" href="/assets/deck-styles.css">
<style>
  .script-box { background: var(--paper); border: 1px solid var(--rule-soft); padding: 28px 36px; font-family: var(--display); font-size: 22px; line-height: 1.55; color: var(--ink); max-height: 520px; overflow: hidden; }
  .script-box .ln { font-family: var(--mono); font-size: 16px; color: var(--accent); margin-right: 10px; user-select: none; }
  .audio-meta { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 16px; }
  .audio-meta .cell { border-top: 3px solid var(--accent); padding-top: 16px; }
  .audio-meta .k { font-family: var(--mono); font-size: 20px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 8px; }
  .audio-meta .v { font-family: var(--display); font-size: 32px; font-weight: 700; color: var(--ink); }
  .fine { font-family: var(--mono); font-size: 22px; color: var(--ink-muted); letter-spacing: 0.06em; margin-top: 28px; }
  .num-list.tight li { padding: 16px 0 !important; }
  .num-list.tight .step-title { font-size: 28px !important; margin-bottom: 2px !important; }
  .num-list.tight .step-body { font-size: 23px !important; line-height: 1.38 !important; }
  .num-list.tight li::before { font-size: 24px !important; }
  .q-strip { display: grid; grid-template-columns: 72px 1fr; gap: 16px; align-items: baseline; padding: 14px 0; border-top: 1px solid var(--rule-soft); font-size: 24px; }
  .q-strip .n { font-family: var(--mono); color: var(--accent); font-weight: 700; }
  .practice-audio { margin-top: 20px; }
  .practice-audio audio { width: 100%; max-width: 720px; height: 48px; }
  .source-note { font-family: var(--mono); font-size: 18px; color: var(--ink-muted); margin-top: 14px; line-height: 1.45; }
  /* Answer key grid — đủ lớn khi scale trong deck-stage */
  .key-grid { display: grid; gap: 20px 22px; margin-top: 12px; width: 100%; box-sizing: border-box; }
  .key-grid > .k {
    background: var(--paper); border: 1px solid var(--rule-soft); border-top: 4px solid var(--accent);
    padding: 22px 16px 24px; min-height: 112px; min-width: 0;
    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
    box-sizing: border-box;
  }
  .key-grid > .k .q { font-family: var(--mono); font-size: 24px; color: var(--accent); font-weight: 700; margin-bottom: 12px; letter-spacing: 0.06em; }
  .key-grid > .k .a { font-family: var(--display); font-size: clamp(28px, 2.6vw, 40px); font-weight: 700; color: var(--ink); line-height: 1.15; word-break: break-word; }
  .key-grid--5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
  .key-grid--4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .key-grid--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  /* Phân tích / walkthrough — đọc được trên slide */
  ul.annot-list { list-style: none; padding: 0; margin: 12px 0 0; }
  ul.annot-list li { padding: 18px 0; border-top: 1px solid var(--rule-soft); font-size: 26px; line-height: 1.48; color: var(--ink-soft); }
  ul.annot-list li:last-child { border-bottom: 1px solid var(--rule-soft); }
  ul.annot-list li .tag { display: inline-block; font-family: var(--mono); font-size: 20px; color: var(--accent); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-right: 12px; min-width: 52px; }
  ul.annot-list li b { color: var(--ink); font-weight: 600; }
  .script-box--full { max-height: 560px; overflow-y: auto; font-size: 21px; line-height: 1.52; }
  .script-box--full .ln { font-size: 15px; }
  /* Transcript boxes: giữ màu chữ nền; highlight + gạch chân từ khóa/đáp án */
  .script-box--full p { font-weight: 400; color: var(--ink); }
  .script-box .tx-hit {
    color: inherit;
    font-weight: inherit;
    font-style: inherit;
    text-decoration: underline;
    text-decoration-thickness: 2px;
    text-underline-offset: 0.2em;
    text-decoration-color: color-mix(in srgb, var(--accent) 55%, transparent);
    background: var(--accent-soft);
    border-radius: 4px;
    padding: 0 0.12em;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
  }
  .transcript-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px 28px; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid var(--rule-soft); }
  .transcript-head .h-section { margin: 0; flex: 1; min-width: 300px; }
  .transcript-meta-pill { font-family: var(--mono); font-size: 17px; letter-spacing: 0.06em; color: var(--ink-soft); border: 1px solid var(--rule-soft); padding: 10px 18px; border-radius: 999px; background: color-mix(in srgb, var(--accent-soft) 45%, transparent); white-space: nowrap; }
  ul.annot-list.annot-dense li { font-size: 21px; padding: 11px 0; line-height: 1.42; }
  .vocab-pair { font-size: 20px; color: var(--ink-muted); margin-top: 4px; }
  /* Pattern recap grid (Form completion) */
  .patt-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 28px 56px; align-content: start; }
  .patt { border-top: 3px solid var(--accent); padding-top: 18px; min-width: 0; }
  .patt .t { font-family: var(--mono); font-size: 20px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700; margin-bottom: 10px; }
  .patt .d { font-family: var(--display); font-size: 26px; line-height: 1.32; font-weight: 500; color: var(--ink); margin-bottom: 8px; }
  .patt .ex { font-size: 21px; color: var(--ink-soft); line-height: 1.45; font-style: italic; }
  .patt .ex .ex-line { display: block; margin: 0; padding: 4px 0 0; border-top: 1px dashed color-mix(in srgb, var(--rule-soft) 80%, transparent); }
  .patt .ex .ex-line:first-child { border-top: 0; padding-top: 0; }
  /* Walkthrough: 2 câu / slide — transcript rút gọn + tín hiệu → nghĩa → chọn */
  .tw-grid { display: grid; grid-template-columns: 1fr 1.08fr; gap: 28px 44px; margin-top: 10px; align-items: start; }
  .tw-tx-label { font-family: var(--mono); font-size: 16px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); font-weight: 600; margin-bottom: 8px; }
  .script-box.script-box--tw { max-height: 400px; overflow: hidden; padding: 20px 26px; font-size: 20px; line-height: 1.5; }
  .script-box.script-box--tw .ln { font-size: 14px; }
  .tw-explain { min-width: 0; }
  .tw-q { border-top: 1px solid var(--rule-soft); padding-top: 14px; margin-top: 14px; }
  .tw-q:first-child { border-top: 0; margin-top: 0; padding-top: 0; }
  .tw-n { font-family: var(--mono); font-size: 18px; color: var(--accent); font-weight: 700; letter-spacing: 0.08em; margin-bottom: 6px; display: block; }
  .tw-body { font-size: 22px; line-height: 1.42; color: var(--ink-soft); }
  .tw-body b { color: var(--ink); font-weight: 600; }
  .tw-pick { margin-top: 10px; font-family: var(--display); font-size: 26px; font-weight: 700; color: var(--ink); }
</style>
</head>
<body>

<deck-stage width="1920" height="1080">
"""

slides: list[str] = []

# 01 TITLE
slides.append(r"""<!-- 01 · TITLE -->
<section data-label="Title" class="slide title-slide">
  <div class="left">
    <div class="mark">IELTS Listening · Academic &amp; GT</div>
    <h1 class="main">Predictions<br>&amp; <em>Forms.</em></h1>
    <div class="mark">Lesson 01 · Lý thuyết + một bài Section 1</div>
  </div>
  <div class="right">
    <div class="mark">Thông tin buổi học</div>
    <dl class="meta-grid">
      <div><dt>Thời lượng</dt><dd>~60 phút</dd></div>
      <div><dt>Trình độ hiện tại</dt><dd>Band 4.5 → 5.5</dd></div>
      <div><dt>Mục tiêu</dt><dd>Band 5.5 → 6.0</dd></div>
      <div><dt>Lý thuyết</dt><dd>8 slide</dd></div>
      <div><dt>Thực hành</dt><dd>Cambridge 19 · Test 1 · Section 1 (audio + transcript)</dd></div>
      <div><dt>Từ vựng</dt><dd>Theo đúng băng + paraphrase trong đề</dd></div>
    </dl>
    <div class="mark">Giảng viên · IELTS Academy</div>
  </div>
</section>""")

# 02 AGENDA
slides.append(f"""<!-- 02 · AGENDA -->
<section data-label="Agenda" class="slide">
  <div class="run-header"><span>Chào mừng</span><span class="rule"></span><span>Lộ trình</span></div>
  <p class="eyebrow">Agenda · ~60 phút</p>
  <h2 class="h-section">Agenda</h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Lý thuyết.</span><span class="step-body">8 slide · ~15 phút. Cấu trúc 4 section · dự đoán loại từ · Form completion · tín hiệu discourse · spelling.</span></div></li>
    <li><div><span class="step-title">Practice 01 · Section 1 — Hinchingbrooke Country Park.</span><span class="step-body">11 slide · ~35 phút. Cambridge 19 Test 1 · 10 gap · audio · 5 slide listen-back (2 câu/slide: transcript rút gọn + tín hiệu → chọn đáp án) · từ vựng/paraphrase.</span></div></li>
    <li><div><span class="step-title">Tổng kết &amp; bài về nhà.</span><span class="step-body">4 slide. Ôn pattern · takeaways · lịch luyện tuần.</span></div></li>
  </ol>
  {foot(2)}
</section>""")

# 03 OBJECTIVES
slides.append(f"""<!-- 03 · OBJECTIVES -->
<section data-label="Objectives" class="slide slide--paper">
  <div class="run-header"><span>Chào mừng</span><span class="rule"></span><span>Mục tiêu</span></div>
  <p class="eyebrow">Learning Objectives</p>
  <h2 class="h-section">Sau buổi này, bạn <em class="hi">làm được</em> năm việc.</h2>
  <ol class="num-list">
    <li><div><span class="step-title">Đọc câu hỏi trước và đoán loại từ (word type) trong 60 giây.</span><span class="step-body">Số / tên / địa điểm / danh từ chung — giảm 50% lỗi spelling.</span></div></li>
    <li><div><span class="step-title">Theo dõi Section 1–2 mà không “đuổi” theo từng chữ.</span><span class="step-body">Nghe tín hiệu: số, tên riêng, từ đồng nghĩa với đề.</span></div></li>
    <li><div><span class="step-title">Làm đúng Form completion trong giới hạn 1 lần nghe + 10′ check.</span><span class="step-body">Đúng chính tả · đúng giới hạn từ (≤2 words) · không thêm mạo từ thừa.</span></div></li>
    <li><div><span class="step-title">Chọn đúng MCQ khi có distractor rõ ràng.</span><span class="step-body">Loại phương án nghe thấy nhưng sai ngữ cảnh / sai thì.</span></div></li>
    <li><div><span class="step-title">Hoàn thành note completion Section 4 với outline trên giấy nháp.</span><span class="step-body">Ghi khung bài giảng trước khi nghe lần 2.</span></div></li>
  </ol>
  {foot(3)}
</section>""")

# 04 TEST OVERVIEW
slides.append(f"""<!-- 04 · TEST OVERVIEW -->
<section data-label="Test Overview" class="slide">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Tổng quan đề</span></div>
  <p class="eyebrow">IELTS Listening · Test Overview</p>
  <h2 class="h-section">Bốn section. <em class="hi">Bốn mươi câu.</em> Ba mươi phút.</h2>
  <div class="timing" style="margin-top: 8px;">
    <div class="hdr">#</div><div class="hdr">Section</div><div class="hdr">Bối cảnh</div><div class="hdr">Độ khó · gợi ý</div>
    <div><strong style="color:var(--accent); font-family:var(--mono);">01</strong></div>
    <div class="passage-title">Section 1 — hội thoại xã hội · 2 người</div>
    <div class="minutes">10 câu</div>
    <div>Dễ nhất · form / table · chính xác spelling</div>
    <div><strong style="color:var(--accent); font-family:var(--mono);">02</strong></div>
    <div class="passage-title">Section 2 — độc thoại · 1 người</div>
    <div class="minutes">10 câu</div>
    <div>MCQ · map / diagram · matching features</div>
    <div><strong style="color:var(--accent); font-family:var(--mono);">03</strong></div>
    <div class="passage-title">Section 3 — hội thoại học thuật · 2–4 người</div>
    <div class="minutes">10 câu</div>
    <div>Matching · flow-chart · multiple select</div>
    <div><strong style="color:var(--accent); font-family:var(--mono);">04</strong></div>
    <div class="passage-title">Section 4 — bài giảng · 1 giảng viên</div>
    <div class="minutes">10 câu</div>
    <div>Khó nhất · note / summary completion</div>
  </div>
  <p class="fine">Có 10 phút cuối để chuyển đáp án sang answer sheet — trong lúc nghe không được dừng băng.</p>
  {foot(4)}
</section>""")

# 05 SCORING (simplified — raw score to band)
slides.append(f"""<!-- 05 · SCORING -->
<section data-label="Scoring" class="slide slide--paper">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Điểm &amp; band</span></div>
  <p class="eyebrow">Scoring · 40 raw points</p>
  <h2 class="h-section">Một điểm = <em class="hi">một câu đúng.</em> Không trừ điểm sai.</h2>
  <div class="stat-row" style="margin-top: 8px;">
    <div class="stat"><div class="k">Raw 23–25</div><div class="v">6.0</div><div class="d">Mục tiêu buổi này: ổn định mid-20s trước khi đẩy lên 26–30.</div></div>
    <div class="stat"><div class="k">Raw 26–29</div><div class="v">6.5</div><div class="d">Cần ít lỗi spelling + ít bị distractor.</div></div>
    <div class="stat"><div class="k">Raw 30+</div><div class="v">7.0+</div><div class="d">Section 4 phải “ăn” được 7–8/10.</div></div>
  </div>
  <p class="fine">Listening không có tiêu chí viết như Writing — chỉ cần <em class="hi">đúng đáp án + đúng chính tả theo audio</em>.</p>
  {foot(5)}
</section>""")

# 06 QUESTION TYPES GRID (kw-grid 4 tiles)
slides.append(f"""<!-- 06 · QUESTION FAMILIES -->
<section data-label="Question Families" class="slide">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>4 nhóm dạng</span></div>
  <p class="eyebrow">Question Families · High frequency</p>
  <h2 class="h-section">Bốn nhóm — <em class="hi">mỗi section ưu tiên một nhóm.</em></h2>
  <div class="kw-grid">
    <div class="kw-tile"><div class="k">01 · GAP</div><div class="ex">Form · Note · Table</div><div class="d">Điền từ nghe được. Rà soát: số ít/số nhiều, số, tên riêng, giới hạn từ.</div></div>
    <div class="kw-tile"><div class="k">02 · CHOICE</div><div class="ex">MCQ · Paired</div><div class="d">Đọc stem kỹ · loại đáp án “đúng một phần” · theo dõi thay đổi ý kiến.</div></div>
    <div class="kw-tile"><div class="k">03 · MAP</div><div class="ex">Plan / Diagram</div><div class="d">Định hướng trước (N/E/S/W) · ghi nhãn A–H trên sơ đồ trước khi nghe.</div></div>
    <div class="kw-tile"><div class="k">04 · MATCH</div><div class="ex">People · Endings</div><div class="d">Section 3: ai nói gì — theo dõi giọng nam/nữ và tên.</div></div>
  </div>
  {foot(6)}
</section>""")

# 07 PREDICTION
slides.append(f"""<!-- 07 · PREDICTION -->
<section data-label="Prediction" class="slide slide--paper">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Dự đoán</span></div>
  <p class="eyebrow">Prediction · Before you listen</p>
  <h2 class="h-section">60 giây đầu — <em class="hi">không để trống.</em></h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Khoanh loại từ cần điền.</span><span class="step-body">Danh từ / động từ / tính từ / số / ngày tháng / tên địa danh.</span></div></li>
    <li><div><span class="step-title">Đoán chủ đề từ tiêu đề bài + câu hỏi.</span><span class="step-body">Ví dụ “Riverdale Conference Centre” → đặt phòng, giá, ngày, loại phòng.</span></div></li>
    <li><div><span class="step-title">Ghi 3 từ khóa có thể paraphrase.</span><span class="step-body">“near the station” ↔ <em>close to the railway</em> — tai tìm cặp này.</span></div></li>
    <li><div><span class="step-title">Chuẩn bị chính tả số &amp; chữ cái.</span><span class="step-body">Double letters: <em>Millennium, accommodation</em> — IELTS thích bẫy chính tả.</span></div></li>
  </ol>
  {foot(7)}
</section>""")

# 08 SIGNALS
slides.append(f"""<!-- 08 · DISCOURSE SIGNALS -->
<section data-label="Signals" class="slide">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Tín hiệu</span></div>
  <p class="eyebrow">Discourse Signals · While you listen</p>
  <h2 class="h-section">Nghe <em class="hi">cụm</em> — không nghe từng âm.</h2>
  <div class="two-col" style="margin-top: 8px;">
    <div class="col-card"><p class="mono-label">Section 1–2</p><h3>Định vị câu trả lời</h3><ul><li><em>Actually / I mean</em> → sửa thông tin trước đó</li><li><em>So that’s / OK so</em> → kết luận nhỏ</li><li>Số đọc theo kiểu Anh/Mỹ — ghi đúng format đề yêu cầu</li></ul></div>
    <div class="col-card"><p class="mono-label">Section 3–4</p><h3>Theo dõi luận điểm</h3><ul><li><em>The main point is / What I’m saying is</em></li><li><em>However / On the other hand</em> → contrast = đáp án hay nằm sau</li><li><em>For instance</em> → ví dụ minh họa cho ý vừa rồi</li></ul></div>
  </div>
  {foot(8)}
</section>""")

# 09 SPELLING TRAPS
slides.append(f"""<!-- 09 · SPELLING -->
<section data-label="Spelling" class="slide slide--paper">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Chính tả</span></div>
  <p class="eyebrow">Spelling Traps · IELTS favourites</p>
  <h2 class="h-section">Sai chính tả = <em class="hi">sai cả câu.</em></h2>
  <div class="vocab-grid compact" style="margin-top: 8px;">
    <div class="vocab-item"><div class="vocab-word">accommodation</div><div class="vocab-meaning">Hai c, một m — không viết <em>acommodation</em>.</div></div>
    <div class="vocab-item"><div class="vocab-word">February</div><div class="vocab-meaning">R — hay bỏ quên khi đọc nhanh.</div></div>
    <div class="vocab-item"><div class="vocab-word">Wednesday</div><div class="vocab-meaning">d giữa n và s.</div></div>
    <div class="vocab-item"><div class="vocab-word">receipt</div><div class="vocab-meaning">ei — không phải <em>ie</em>.</div></div>
    <div class="vocab-item"><div class="vocab-word">environment</div><div class="vocab-meaning">n — không <em>enviroment</em>.</div></div>
    <div class="vocab-item"><div class="vocab-word">parallel</div><div class="vocab-meaning">Hai l — map / mô tả đường.</div></div>
  </div>
  <p class="fine">Luôn kiểm tra: <em class="hi">số từ cho phép</em> (NO MORE THAN TWO WORDS) — mạo từ <em>a/the</em> tính là một từ.</p>
  {foot(9)}
</section>""")

# 10 EXAM SEQUENCE
slides.append(f"""<!-- 10 · EXAM SEQUENCE -->
<section data-label="Exam Sequence" class="slide">
  <div class="run-header"><span>Phần I · Lý thuyết</span><span class="rule"></span><span>Trình tự 30′</span></div>
  <p class="eyebrow">Exam Sequence · Time budget</p>
  <h2 class="h-section">30 phút nghe — <em class="hi">chia theo section.</em></h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Giữa các section (pause).</span><span class="step-body">Đọc trước section kế · khoanh từ khóa · không sửa section cũ nếu không chắc.</span></div></li>
    <li><div><span class="step-title">Section 1: ổn định tâm lý.</span><span class="step-body">10 câu “warm-up” — mất 2 câu đầu thường ảnh hưởng cả bài.</span></div></li>
    <li><div><span class="step-title">Section 4: đọc summary trước khi nghe.</span><span class="step-body">Gạch đầu dòng chủ đề từng đoạn trong 45 giây pause trước S4.</span></div></li>
    <li><div><span class="step-title">Transfer time 10′.</span><span class="step-body">Chép cẩn thận ô đáp án — không để trống; đoán chữ cái nếu bắt buộc.</span></div></li>
  </ol>
  {foot(10)}
</section>""")


def practice_block(
    start_slide: int,
    practice_num: str,
    practice_title: str,
    section_name: str,
    band_side: str,
    toc_active_idx: int,
    toc_lines: list[str],
    h2_html: str,
    task_left_html: str,
    task_right_html: str,
    step1_html: str,
    step2_html: str,
    step3_html: str,
    sample_html: str,
    analysis_html: str,
    analysis_slides: list[str] | None,
    vocab_html: str,
    mistakes_html: str,
    extra_after_step3: list[tuple[str, str, str]] | None = None,
    *,
    include_sample_script: bool = True,
    include_mistakes: bool = True,
) -> None:
    toc = "\n".join(
        f'<div class="{"active" if i == toc_active_idx else ""}">{escape(line)}</div>'
        for i, line in enumerate(toc_lines)
    )
    # 11 section break -> relative numbers
    n = start_slide
    slides.append(f"""<!-- {n:02d} · SECTION BREAK -->
<section data-label="{n:02d} {practice_title}" class="slide section-break">
  <div class="band">
    <div class="lbl">Practice · {practice_num}</div>
    <div class="n">{practice_num}</div>
    <div class="lbl">{section_name}</div>
  </div>
  <div class="content">
    <p class="eyebrow">Practice {practice_num} · {section_name}</p>
    <h2>{h2_html}</h2>
    <div class="toc">{toc}</div>
  </div>
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · TASK -->
<section data-label="{n:02d} Task" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Task &amp; context</span></div>
  <p class="eyebrow">Task · {practice_title}</p>
  <div style="display:grid; grid-template-columns: 1fr 1.05fr; gap: 48px; margin-top: 8px;">
    <div>{task_left_html}</div>
    <div>{task_right_html}</div>
  </div>
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · STEP 1 -->
<section data-label="{n:02d} Step1" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Step 1 · Predict</span></div>
  <p class="eyebrow">Step 1 · Predict · 3 min</p>
  <h2 class="h-section">Before you press play — <em class="hi">finish the checklist.</em></h2>
  {step1_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · STEP 2 -->
<section data-label="{n:02d} Step2" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Step 2 · While listening</span></div>
  <p class="eyebrow">Step 2 · While listening · cues</p>
  <h2 class="h-section">Signals to <em class="hi">catch</em> on first listen</h2>
  {step2_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · STEP 3 -->
<section data-label="{n:02d} Step3" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Step 3 · Key</span></div>
  <p class="eyebrow">Step 3 · Key · spelling check</p>
  <h2 class="h-section">Answer key — <em class="hi">check spelling.</em></h2>
  {step3_html}
  {foot(n)}
</section>""")
    for extra_label, header_rhs, extra_inner in extra_after_step3 or ():
        n += 1
        safe_label = escape(extra_label)
        slides.append(f"""<!-- {n:02d} · {extra_label.upper()} -->
<section data-label="{n:02d} {safe_label}" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>{header_rhs}</span></div>
  {extra_inner}
  {foot(n)}
</section>""")
    if include_sample_script:
        n += 1
        slides.append(f"""<!-- {n:02d} · SAMPLE SCRIPT -->
<section data-label="{n:02d} Script" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Short transcript</span></div>
  <p class="eyebrow">Script excerpt · From the tape</p>
  <h2 class="h-section">Short script <em class="hi">excerpt</em> (exact wording)</h2>
  {sample_html}
  {foot(n)}
</section>""")
    if analysis_slides:
        for idx, inner in enumerate(analysis_slides, 1):
            n += 1
            slides.append(f"""<!-- {n:02d} · WALKTHROUGH {idx}/5 -->
<section data-label="{n:02d} Walkthrough{idx}" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Listen-back · {idx}/5</span></div>
  {inner}
  {foot(n)}
</section>""")
    elif analysis_html.strip():
        n += 1
        slides.append(f"""<!-- {n:02d} · ANALYSIS -->
<section data-label="{n:02d} Analysis" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Analysis</span></div>
  <p class="eyebrow">Language &amp; strategy</p>
  <h2 class="h-section">Why the answer <em class="hi">sits there</em></h2>
  {analysis_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · VOCAB -->
<section data-label="{n:02d} Vocab" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Vocabulary</span></div>
  <p class="eyebrow">Vocabulary · Paraphrase</p>
  <h2 class="h-section">Words &amp; <em class="hi">stem ↔ audio</em> pairs</h2>
  {vocab_html}
  {foot(n)}
</section>""")
    if include_mistakes:
        n += 1
        slides.append(f"""<!-- {n:02d} · MISTAKES -->
<section data-label="{n:02d} Mistakes" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Common mistakes</span></div>
  <p class="eyebrow">Common mistakes</p>
  <h2 class="h-section">Five traps <em class="hi">to avoid.</em></h2>
  {mistakes_html}
  {foot(n)}
</section>""")


TOC_P01 = [
    "01 · Section 1 — Hinchingbrooke (form)",
]

# Practice 01 — Section 1 (Cambridge IELTS 19 · Test 1 · Section 1 — Hinchingbrooke Country Park)
# Audio: copy from licensed pack (e.g. "Test1 Part1.mp3" from Cambridge IELTS 19 audio) to:
#   listening/lesson/1/audio/cam19-test1-part1.mp3
# Web path is relative to index.html (no spaces in filename for stable URLs).
_LISTENING_P1_MP3 = "audio/cam19-test1-part1.mp3"

# Five listen-back slides after Step 3: two questions each — short transcript + signals → meaning → answer (UI copy in English).
P01_ANALYSIS_SLIDES: list[str] = [
    r"""<p class="eyebrow">Q1–2 · Transcript + signals</p>
  <h2 class="h-section tidy-h2">Why clip the audio? — <em class="hi">signals</em> → meaning → pick</h2>
  <p class="small" style="margin-bottom: 10px;">Quote only the lines with gaps; underlined = exact wording on the tape (no off-tape guessing).</p>
  <div class="tw-grid">
    <div class="tw-tx">
      <div class="tw-tx-label">Transcript excerpt</div>
      <div class="script-box script-box--tw">
        <p><span class="ln">S</span>Altogether the park covers <span class="tx-hit">170 acres</span>, that&rsquo;s <span class="tx-hit">69 hectares</span>. There are three main types of habitat: wetland, grassland and woodland.</p>
        <p><span class="ln">S</span>There are also several smaller ones, ponds and a <span class="tx-hit">stream</span> that flows through the park.</p>
      </div>
    </div>
    <div class="tw-explain">
      <div class="tw-q">
        <span class="tw-n">Q1</span>
        <div class="tw-body"><b>Signal:</b> two numbers + two units (<em>acres</em> / <em>hectares</em>) in <strong>one sentence</strong>.<br>
        <b>Meaning:</b> the note asks for <strong>Area (hectares)</strong> → write the hectare figure only.<br>
        <b>Stem ↔ audio:</b> <em>Area (hectares)</em> ↔ <em>covers … that&rsquo;s … hectares</em>.</div>
        <div class="tw-pick">→ Pick: <strong>69</strong> (not 170 — that is acres).</div>
      </div>
      <div class="tw-q">
        <span class="tw-n">Q2</span>
        <div class="tw-body"><b>Signal:</b> landform chain <em>ponds and a ___</em> → noun + <em>flows through</em>.<br>
        <b>Meaning:</b> one word for a small watercourse between ponds.<br>
        <b>Stem ↔ audio:</b> <em>lakes, ponds and a ___</em> ↔ same clause on tape.</div>
        <div class="tw-pick">→ Pick: <strong>stream</strong></div>
      </div>
    </div>
  </div>""",
    r"""<p class="eyebrow">Q3–4 · Transcript + signals</p>
  <h2 class="h-section tidy-h2">Science → Geography — <em class="hi">one gap per block</em></h2>
  <div class="tw-grid">
    <div class="tw-tx">
      <div class="tw-tx-label">Transcript excerpt</div>
      <div class="script-box script-box--tw">
        <p><span class="ln">S</span>Well, one focus is on science, where we help children to discover and study plants, trees and insects. They also collect and analyse <span class="tx-hit">data</span> about the things they see.</p>
        <p><span class="ln">S</span>Another focus is on geography. The park is a great environment to learn and practice reading a <span class="tx-hit">map</span> and using a compass to navigate around the park.</p>
      </div>
    </div>
    <div class="tw-explain">
      <div class="tw-q">
        <span class="tw-n">Q3</span>
        <div class="tw-body"><b>Signal:</b> after <em>collect and analyse</em>, a noun for what they gather about what they see.<br>
        <b>Meaning:</b> stem says <em>look at ___ about plants</em>; tape has <em>analyse data about the things they see</em> (do not repeat <em>plants</em> in the gap).<br>
        <b>Stem ↔ audio:</b> <em>look at</em> ↔ <em>collect and analyse</em>.</div>
        <div class="tw-pick">→ Pick: <strong>data</strong></div>
      </div>
      <div class="tw-q">
        <span class="tw-n">Q4</span>
        <div class="tw-body"><b>Signal:</b> Geography + <em>reading a … and using a compass</em>.<br>
        <b>Meaning:</b> gap before <em>and compass</em> → one orientation tool.<br>
        <b>Stem ↔ audio:</b> <em>use a ___ and compass</em> ↔ <em>reading a map and using a compass</em>.</div>
        <div class="tw-pick">→ Pick: <strong>map</strong></div>
      </div>
    </div>
  </div>""",
    r"""<p class="eyebrow">Q5–6 · Transcript + signals</p>
  <h2 class="h-section tidy-h2">Leisure &amp; Music — <em class="hi">stem paraphrase</em></h2>
  <div class="tw-grid">
    <div class="tw-tx">
      <div class="tw-tx-label">Transcript excerpt</div>
      <div class="script-box script-box--tw">
        <p><span class="ln">J</span>That focuses on your <span class="tx-hit">visitors</span>, I would imagine.</p>
        <p><span class="ln">S</span>Yes, mostly. The children find out about them, their requirements, the problems they may cause and how we manage these. And another subject we cover is music: here the children experiment with natural materials to create <span class="tx-hit">sounds</span> and explore <span class="tx-hit">rhythm and tempo</span>.</p>
      </div>
    </div>
    <div class="tw-explain">
      <div class="tw-q">
        <span class="tw-n">Q5</span>
        <div class="tw-body"><b>Signal:</b> John: <em>focuses on your visitors</em> — Sally <em>Yes, mostly</em>, then detail.<br>
        <b>Meaning:</b> gap <em>concentrates on the park&rsquo;s ___</em> → noun for who visits.<br>
        <b>Stem ↔ audio:</b> <em>concentrates on</em> ↔ <em>focuses on your visitors</em>.</div>
        <div class="tw-pick">→ Pick: <strong>visitors</strong></div>
      </div>
      <div class="tw-q">
        <span class="tw-n">Q6</span>
        <div class="tw-body"><b>Signal:</b> Music + <em>create … with natural materials</em>; <em>rhythm and tempo</em> is printed on the form, so not the <em>make ___</em> gap.<br>
        <b>Meaning:</b> stem <em>make</em> = tape <em>create</em>; gap = noun for what they produce.<br>
        <b>Stem ↔ audio:</b> <em>make</em> ↔ <em>create</em>.</div>
        <div class="tw-pick">→ Pick: <strong>sounds</strong></div>
      </div>
    </div>
  </div>""",
    r"""<p class="eyebrow">Q7–8 · Transcript + signals</p>
  <h2 class="h-section tidy-h2">Benefits — <em class="hi">feeling / learn</em> reworded</h2>
  <div class="tw-grid">
    <div class="tw-tx">
      <div class="tw-tx-label">Transcript excerpt</div>
      <div class="script-box script-box--tw">
        <p><span class="ln">J</span>I would imagine they get a sense of <span class="tx-hit">freedom</span> that might not be a normal part of their lives.</p>
        <p><span class="ln">S</span>That&rsquo;s right. And very often the children discover that they can do things they didn&rsquo;t know they could do, and they develop new <span class="tx-hit">skills</span>. This gives them greater self-confidence.</p>
      </div>
    </div>
    <div class="tw-explain">
      <div class="tw-q">
        <span class="tw-n">Q7</span>
        <div class="tw-body"><b>Signal:</b> <em>a sense of ___</em> right after the outdoor-activity idea.<br>
        <b>Meaning:</b> stem <em>feeling of</em> = tape <em>sense of</em> — same idea (freedom).<br>
        <b>Stem ↔ audio:</b> <em>feeling of</em> ↔ <em>sense of</em>.</div>
        <div class="tw-pick">→ Pick: <strong>freedom</strong></div>
      </div>
      <div class="tw-q">
        <span class="tw-n">Q8</span>
        <div class="tw-body"><b>Signal:</b> <em>develop new ___</em> follows the freedom line; then <em>self-confidence</em>.<br>
        <b>Meaning:</b> stem <em>learn new</em> = tape <em>develop new</em> → plural noun (skills).<br>
        <b>Stem ↔ audio:</b> <em>learn</em> ↔ <em>develop</em>.</div>
        <div class="tw-pick">→ Pick: <strong>skills</strong></div>
      </div>
    </div>
  </div>""",
    r"""<p class="eyebrow">Q9–10 · Transcript + signals</p>
  <h2 class="h-section tidy-h2">Price &amp; adults — <em class="hi">conditional trigger + parallel nouns</em></h2>
  <div class="tw-grid">
    <div class="tw-tx">
      <div class="tw-tx-label">Transcript excerpt</div>
      <div class="script-box script-box--tw">
        <p><span class="ln">J</span>How much does it cost for a full-day visit? We would expect to bring between 30 and 40 children.</p>
        <p><span class="ln">S</span>If there are over 30, it costs <span class="tx-hit">&pound;4.95</span> for each child who attends on the day. We invoice you afterwards, so you don&rsquo;t pay for children who can&rsquo;t come because of sickness, for example. There&rsquo;s no charge for <span class="tx-hit">leaders</span> and other adults – as many as you want to bring.</p>
      </div>
    </div>
    <div class="tw-explain">
      <div class="tw-q">
        <span class="tw-n">Q9</span>
        <div class="tw-body"><b>Signal:</b> conditional <em>If there are over 30</em> → immediate price <em>£4.95 for each child</em> (trigger → answer).<br>
        <b>Meaning:</b> the form already prints <strong>£</strong> → usually digits only: <strong>4.95</strong>.<br>
        <b>Stem ↔ audio:</b> <em>Cost per child: £</em> ↔ <em>costs £4.95 for each child</em>.</div>
        <div class="tw-pick">→ Pick: <strong>4.95</strong></div>
      </div>
      <div class="tw-q">
        <span class="tw-n">Q10</span>
        <div class="tw-body"><b>Signal:</b> <em>no charge for leaders and other adults</em> — coordinated pair (<strong>leaders</strong> ‖ <strong>other adults</strong>); stem <em>Adults, such as ___</em> = one word.<br>
        <b>Meaning:</b> pick the first head noun Cambridge keys; do not invent <em>parents/teachers</em> — not on tape.<br>
        <b>Stem ↔ audio:</b> <em>such as</em> ↔ <em>leaders and other adults</em>.</div>
        <div class="tw-pick">→ Pick: <strong>leaders</strong></div>
      </div>
    </div>
  </div>""",
]

practice_block(
    11,
    "01",
    "Hinchingbrooke Country Park",
    "Section 1",
    "S1",
    0,
    TOC_P01,
    "<em>Hinchingbrooke</em><br>Country Park<br><span style=\"font-size:0.85em\">Cambridge IELTS 19 · Test 1 · S1</span>",
    f"""<h2 class="h-sub" style="font-size: 34px; margin-bottom: 16px;">Complete the notes below. Write <strong>ONE WORD AND/OR A NUMBER</strong> for each answer.</h2>
       <p class="small">You will hear Sally from Hinchingbrooke Country Park (ranger) and John Chapman (teaching assistant) arranging an educational visit for school classes.</p>
       <div class="audio-meta">
         <div class="cell"><div class="k">Voices</div><div class="v">2</div><div class="d">Ranger + teaching assistant</div></div>
         <div class="cell"><div class="k">Length</div><div class="v">~7′</div><div class="d">10 gaps · form</div></div>
         <div class="cell"><div class="k">Topic</div><div class="v">Nature park</div><div class="d">Habitats · school visit · practical info</div></div>
       </div>
       <div class="practice-audio"><audio controls preload="metadata" src="{_LISTENING_P1_MP3}">Your browser does not support the &lt;audio&gt; element.</audio></div>
       <p class="source-note">Recording from <strong>Cambridge IELTS 19</strong> (licensed pack) — project file: <code>listening/lesson/1/audio/cam19-test1-part1.mp3</code> (copy from <code>Test1 Part1.mp3</code> in your official audio folder).</p>""",
    """<div class="ex-card"><span class="tag">Hinchingbrooke Country Park · Q1–10</span>
       <div class="q-strip"><span class="n">1</span><span>The park — Area: ____________ hectares</span></div>
       <div class="q-strip"><span class="n">2</span><span>Wetland: lakes, ponds and a ____________</span></div>
       <div class="q-strip"><span class="n">3</span><span>Science: Children look at ____________ about plants, etc.</span></div>
       <div class="q-strip"><span class="n">4</span><span>Geography: includes learning to use a ____________ and compass</span></div>
       <div class="q-strip"><span class="n">5</span><span>Leisure and tourism: mostly concentrates on the park’s ____________</span></div>
       <div class="q-strip"><span class="n">6</span><span>Music: Children make ____________ with natural materials, and experiment with rhythm and tempo.</span></div>
       <div class="q-strip"><span class="n">7</span><span>Benefits: They give children a feeling of ____________</span></div>
       <div class="q-strip"><span class="n">8</span><span>Children learn new ____________ and gain self-confidence</span></div>
       <div class="q-strip"><span class="n">9</span><span>Cost per child: £ ____________</span></div>
       <div class="q-strip"><span class="n">10</span><span>Adults, such as ____________, free</span></div>
       </div>""",
    """<div class="qtype-grid" style="gap: 20px 48px;">
         <div class="qtype-item"><div class="n">Q1</div><div><div class="t">Number + unit</div><div class="s">One clause with both <em>acres</em> and <em>hectares</em> — the hectares gap takes the hectare figure only (not acres).</div></div></div>
         <div class="qtype-item"><div class="n">Q2–4</div><div><div class="t">Subject blocks</div><div class="s">Science → Geography → History — one short fact per subject line.</div></div></div>
         <div class="qtype-item"><div class="n">Q6</div><div><div class="t">Countable noun</div><div class="s">Collocation with <em>make … with materials</em> — do not fill <em>rhythm / tempo</em> (already printed).</div></div></div>
         <div class="qtype-item"><div class="n">Q9</div><div><div class="t">Price</div><div class="s">Pence precision — two digits after the decimal; often digits only if £ is printed.</div></div></div>
       </div>
       <p class="fine" style="margin-top: 28px;">Before listening: mark word type per gap (number / noun / person word).</p>""",
    """<ul class="num-list tight" style="margin-top: 8px;">
         <li><div><span class="step-title">Area units.</span><span class="step-body">Same line: <em>170 acres</em> and <em>69 hectares</em> — Area (hectares) gap → write <strong>69</strong> only.</span></div></li>
         <li><div><span class="step-title">Child price (conditional).</span><span class="step-body">If <em>over 30</em> children → <em>£4.95</em> each; pay by invoice — no fee for absent sick children.</span></div></li>
         <li><div><span class="step-title">Free adults (parallel nouns).</span><span class="step-body">Hear &ldquo;no charge for <strong>leaders</strong> and other adults&rdquo; — <em>Adults, such as ___</em> one word → <strong>leaders</strong>.</span></div></li>
       </ul>""",
    """<div class="key-grid key-grid--5">
         <div class="k"><div class="q">1</div><div class="a">69</div></div>
         <div class="k"><div class="q">2</div><div class="a">stream</div></div>
         <div class="k"><div class="q">3</div><div class="a">data</div></div>
         <div class="k"><div class="q">4</div><div class="a">map</div></div>
         <div class="k"><div class="q">5</div><div class="a">visitors</div></div>
         <div class="k"><div class="q">6</div><div class="a">sounds</div></div>
         <div class="k"><div class="q">7</div><div class="a">freedom</div></div>
         <div class="k"><div class="q">8</div><div class="a">skills</div></div>
         <div class="k"><div class="q">9</div><div class="a">4.95</div></div>
         <div class="k"><div class="q">10</div><div class="a">leaders</div></div>
       </div>
       <p class="fine">Keys match Cambridge IELTS 19 Test 1 Listening Section 1 — check spelling and numbers against the official transcript.</p>""",
    "",
    "",
    P01_ANALYSIS_SLIDES,
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">covers / area</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>Area</em> · Audio: <em>covers … hectares</em></span></div></div>
         <div class="vocab-item"><div class="vocab-word">hectare · acre</div><div class="vocab-meaning">Two units in one clause — match the unit printed in the gap.</div></div>
         <div class="vocab-item"><div class="vocab-word">wetland · ponds · stream</div><div class="vocab-meaning">Landform chain: lakes → ponds → <strong>stream</strong></div></div>
         <div class="vocab-item"><div class="vocab-word">collect &amp; analyse data</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>look at … about plants</em> · Audio: <em>data about the things they see</em></span></div></div>
         <div class="vocab-item"><div class="vocab-word">map · compass · navigate</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>use a … and compass</em> · Audio: <em>reading a map and using a compass</em></span></div></div>
         <div class="vocab-item"><div class="vocab-word">focus on · concentrates on</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>concentrates on</em> · Audio: <em>focuses on</em> (visitors)</span></div></div>
         <div class="vocab-item"><div class="vocab-word">create / make sounds</div><div class="vocab-meaning">music: natural materials + rhythm/tempo</div></div>
         <div class="vocab-item"><div class="vocab-word">sense of freedom</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>feeling of</em> · Audio: <em>sense of</em></span></div></div>
         <div class="vocab-item"><div class="vocab-word">develop / learn skills</div><div class="vocab-meaning">Self-confidence follows in the next clause.</div></div>
         <div class="vocab-item"><div class="vocab-word">over 30 · £4.95 each</div><div class="vocab-meaning">Count condition → price (Q9).</div></div>
         <div class="vocab-item"><div class="vocab-word">no charge · leaders · adults</div><div class="vocab-meaning"><span class="vocab-pair">Question: <em>Adults, such as …</em> · Audio: <em>leaders and other adults</em></span> (parallel nouns, Q10)</div></div>
         <div class="vocab-item"><div class="vocab-word">ranger · teaching assistant</div><div class="vocab-meaning">Two speaker roles (Section 1 booking context).</div></div>
       </div>""",
    "",
    extra_after_step3=None,
    include_sample_script=False,
    include_mistakes=False,
)

# 22 PATTERNS (sau Practice 01 — walkthrough kết thúc ở slide 21)
slides.append(f"""<!-- 22 · PATTERNS -->
<section data-label="22 Patterns" class="slide">
  <div class="run-header"><span>Wrap-up</span><span class="rule"></span><span>Patterns · Section 1</span></div>
  <p class="eyebrow">Patterns · Form completion</p>
  <h2 class="h-section">Four patterns to <em class="hi">review</em> from Hinchingbrooke</h2>
  <div class="patt-grid" style="margin-top: 8px;">
    <div class="patt"><div class="t">01 · Question stem vs audio</div><div class="d">The stem may change the verb or phrase; the gap still needs the exact word you hear.</div><div class="ex"><em>make</em> ↔ <em>create</em> · <em>learn</em> ↔ <em>develop</em></div></div>
    <div class="patt"><div class="t">02 · Two numbers, one sentence</div><div class="d">Acres and hectares in the same line — match the unit printed in the blank.</div><div class="ex">Area (hectares) → <strong>69</strong>, not <strong>170</strong> (acres)</div></div>
    <div class="patt"><div class="t">03 · Word / number limits</div><div class="d">ONE WORD AND/OR A NUMBER — count words; if the form already shows £, usually write digits only.</div><div class="ex"><span class="ex-line"><strong>£</strong> on the form → write <strong>4.95</strong> only.</span><span class="ex-line">One-word gap → <strong>leaders</strong> (heard on tape), not a longer paraphrase.</span></div></div>
    <div class="patt"><div class="t">04 · Parallel topics</div><div class="d">Science → Geography → History → Leisure → Music — often one gap per block.</div><div class="ex">Use subject headings on your notes as signposts.</div></div>
  </div>
  {foot(22)}
</section>""")

# 23 TAKEAWAYS (bốn ý — khớp bốn patterns)
slides.append(f"""<!-- 23 · TAKEAWAYS -->
<section data-label="23 Takeaways" class="slide slide--paper">
  <div class="run-header"><span>Wrap-up</span><span class="rule"></span><span>Takeaways</span></div>
  <p class="eyebrow">Key takeaways · Section 1</p>
  <h2 class="h-section">Four takeaways to <em class="hi">bring home</em></h2>
  <div class="take">
    <div class="item"><div class="k">01</div><div class="v">Đọc trước cả form — ghi loại từ (số / danh từ / tên) từng ô; theo dõi hai giọng (ai hỏi, ai cho đáp án).</div></div>
    <div class="item"><div class="k">02</div><div class="v">Hai con số / hai đơn vị trong một câu — khớp đúng đơn vị trên ô trống (vd. hectares vs acres).</div></div>
    <div class="item"><div class="k">03</div><div class="v">Đề paraphrase vẫn cần <strong>đúng từ trên băng</strong> trong giới hạn ONE WORD — spelling: stream, leaders, data.</div></div>
    <div class="item"><div class="k">04</div><div class="v">Điều kiện (over 30) + giá; nghe lại transcript rút gọn (highlight) — ghi cặp đề ↔ băng.</div></div>
  </div>
  {foot(23)}
</section>""")

# 24 WEEKLY PLAN
slides.append(f"""<!-- 24 · WEEKLY PLAN -->
<section data-label="24 Weekly Plan" class="slide">
  <div class="run-header"><span>Wrap-up</span><span class="rule"></span><span>Weekly plan</span></div>
  <div class="plan-grid" style="margin-top: 20px;">
    <div class="hdr">Day</div><div class="hdr">Task</div><div class="hdr">Focus</div><div class="hdr">Time</div>
    <div class="day">Thứ 2</div><div>S1 form</div><div>1 Test · Part 1 — chỉ ghi lỗi chính tả / số vào sổ.</div><div class="time">30′</div>
    <div class="day">Thứ 3</div><div>S1 + review</div><div>Nghe lại cùng transcript — khoanh paraphrase đề ↔ băng.</div><div class="time">30′</div>
    <div class="day">Thứ 4</div><div>S1 dictation</div><div>Chép 2 đoạn ngắn từ transcript — kiểm tra spelling.</div><div class="time">25′</div>
    <div class="day">Thứ 5</div><div>Mixed S1–S2</div><div>Một test: S1 full + 5 câu đầu S2 (nếu đã học S2).</div><div class="time">35′</div>
    <div class="day">Thứ 6</div><div>Full Listening</div><div>40 câu · timing thật · 10′ transfer.</div><div class="time">40′</div>
    <div class="day">Thứ 7</div><div>Error log</div><div>Tổng hợp từ tuần — đọc to các từ hay sai.</div><div class="time">20′</div>
    <div class="day">CN</div><div>Nghỉ / nhẹ</div><div>Shadowing 1 đoạn S1 5′ (tùy chọn).</div><div class="time">15′</div>
  </div>
  {foot(24)}
</section>""")

# 25 END
slides.append("""<!-- 25 · END -->
<section data-label="25 End" class="slide end-slide">
  <div>
    <h1>Keep<br>listening.</h1>
    <div class="hint">Lesson 01 · Listening · IELTS Academy</div>
  </div>
</section>""")

out = HEAD + "\n\n".join(slides) + "\n\n</deck-stage>\n\n</body>\n</html>\n"

path = "/Users/sophie/Desktop/Code/Ielts/listening/lesson/1/index.html"
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write(out)

# verify section count matches TOTAL_SLIDES
import re

sec = len(re.findall(r"<section\b", out))
if sec != TOTAL_SLIDES:
    raise SystemExit(f"Expected {TOTAL_SLIDES} sections, got {sec}")
print(path, "bytes", len(out), "sections", sec)
