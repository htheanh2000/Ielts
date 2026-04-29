#!/usr/bin/env python3
"""Generate listening/lesson/1/index.html — 54 slides (P01 có transcript đầy đủ + walkthrough)."""

import os
from html import escape

FOOTER = "IELTS Listening · Lesson 01"
TOTAL_SLIDES = 54


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
    <div class="mark">Lesson 01 · Bốn section · Bốn bài mẫu</div>
  </div>
  <div class="right">
    <div class="mark">Thông tin buổi học</div>
    <dl class="meta-grid">
      <div><dt>Thời lượng</dt><dd>90 phút</dd></div>
      <div><dt>Trình độ hiện tại</dt><dd>Band 4.5 → 5.5</dd></div>
      <div><dt>Mục tiêu</dt><dd>Band 5.5 → 6.0</dd></div>
      <div><dt>Lý thuyết</dt><dd>8 slide</dd></div>
      <div><dt>Thực hành</dt><dd>4 bài (P1 có audio + transcript đầy đủ)</dd></div>
      <div><dt>Từ vựng</dt><dd>28 từ · 16 collocations</dd></div>
    </dl>
    <div class="mark">Giảng viên · IELTS Academy</div>
  </div>
</section>""")

# 02 AGENDA
slides.append(f"""<!-- 02 · AGENDA -->
<section data-label="Agenda" class="slide">
  <div class="run-header"><span>Chào mừng</span><span class="rule"></span><span>Lộ trình</span></div>
  <p class="eyebrow">Agenda · 90 minutes</p>
  <h2 class="h-section">Agenda</h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Lý thuyết.</span><span class="step-body">8 slide · 15 phút. Cấu trúc 4 section · dự đoán loại từ · dạng Form completion · MCQ · map · note completion · chiến thuật spelling.</span></div></li>
    <li><div><span class="step-title">Practice 01 · Section 1 — Hinchingbrooke Country Park.</span><span class="step-body">13 slide · ~22 phút. Cambridge 19 Test 1 · form · 10 gap · audio · transcript đầy đủ · walkthrough từng câu.</span></div></li>
    <li><div><span class="step-title">Practice 02 · Section 2 — Campus tour.</span><span class="step-body">9 slide · 17 phút. MCQ + labelling plan · theo dõi tín hiệu chuyển ý.</span></div></li>
    <li><div><span class="step-title">Practice 03 · Section 3 — Assignment discussion.</span><span class="step-body">9 slide · 16 phút. Matching opinions · paraphrase giữa các giọng.</span></div></li>
    <li><div><span class="step-title">Practice 04 · Section 4 — Urban ecology lecture.</span><span class="step-body">9 slide · 16 phút. Note completion · một người nói · mật độ thông tin cao.</span></div></li>
    <li><div><span class="step-title">Tổng kết &amp; bài về nhà.</span><span class="step-body">4 slide · 8 phút. Pattern chung · takeaways · lịch luyện tuần.</span></div></li>
  </ol>
  {foot(2)}
</section>""")

# 03 OBJECTIVES
slides.append(f"""<!-- 03 · OBJECTIVES -->
<section data-label="Objectives" class="slide slide--paper">
  <div class="run-header"><span>Chào mừng</span><span class="rule"></span><span>Mục tiêu</span></div>
  <p class="eyebrow">Learning Objectives</p>
  <h2 class="h-section">Sau 90 phút, bạn <em class="hi">làm được</em> năm việc.</h2>
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
    vocab_html: str,
    mistakes_html: str,
    extra_after_step3: list[tuple[str, str, str]] | None = None,
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
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Đề + ngữ cảnh</span></div>
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
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Bước 1 · Dự đoán</span></div>
  <p class="eyebrow">Step 1 · Predict · 3 phút</p>
  <h2 class="h-section">Trước khi bấm play — <em class="hi">làm xong checklist.</em></h2>
  {step1_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · STEP 2 -->
<section data-label="{n:02d} Step2" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Bước 2 · While listening</span></div>
  <p class="eyebrow">Step 2 · While listening · cues</p>
  <h2 class="h-section">Tín hiệu cần <em class="hi">bắt</em> trong lần nghe 1</h2>
  {step2_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · STEP 3 -->
<section data-label="{n:02d} Step3" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Bước 3 · Đáp án</span></div>
  <p class="eyebrow">Step 3 · Key · spelling check</p>
  <h2 class="h-section">Đáp án mẫu — <em class="hi">đối chiếu chính tả.</em></h2>
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
    n += 1
    slides.append(f"""<!-- {n:02d} · SAMPLE SCRIPT -->
<section data-label="{n:02d} Script" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Transcript rút gọn</span></div>
  <p class="eyebrow">Script excerpt · Theo băng</p>
  <h2 class="h-section">Đoạn thoại <em class="hi">rút gọn</em> (đúng lời audio)</h2>
  {sample_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · ANALYSIS -->
<section data-label="{n:02d} Analysis" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Phân tích</span></div>
  <p class="eyebrow">Language &amp; strategy</p>
  <h2 class="h-section">Vì sao đáp án <em class="hi">nằm ở đó?</em></h2>
  {analysis_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · VOCAB -->
<section data-label="{n:02d} Vocab" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Từ vựng</span></div>
  <p class="eyebrow">Vocabulary · Collocations</p>
  <h2 class="h-section">Từ cần <em class="hi">thuộc</em> sau bài này</h2>
  {vocab_html}
  {foot(n)}
</section>""")
    n += 1
    slides.append(f"""<!-- {n:02d} · MISTAKES -->
<section data-label="{n:02d} Mistakes" class="slide slide--paper">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Lỗi thường gặp</span></div>
  <p class="eyebrow">Common mistakes</p>
  <h2 class="h-section">Năm lỗi <em class="hi">đừng lặp lại.</em></h2>
  {mistakes_html}
  {foot(n)}
</section>""")


TOC_ALL = [
    "01 · Section 1 — Hinchingbrooke (form)",
    "02 · Section 2 — MCQ + map",
    "03 · Section 3 — matching opinions",
    "04 · Section 4 — note completion",
]

# Practice 01 — Section 1 (Cambridge IELTS 19 · Test 1 · Section 1 — Hinchingbrooke Country Park)
# Audio: copy from licensed pack (e.g. "Test1 Part1.mp3" from Cambridge IELTS 19 audio) to:
#   listening/lesson/1/audio/cam19-test1-part1.mp3
# Web path is relative to index.html (no spaces in filename for stable URLs).
_LISTENING_P1_MP3 = "audio/cam19-test1-part1.mp3"

# Bốn slide chèn sau Step 3 (đáp án): transcript 2 phần (theo audioscript Cambridge) + walkthrough Q1–5 / Q6–10.
P01_EXTRA_AFTER_STEP3: list[tuple[str, str, str]] = [
    (
        "Transcript1",
        "Transcript · phần 1 / 2",
        """<p class="eyebrow">Full transcript · Cambridge 19 · Test 1 · Part 1 · 1/2</p>
  <h2 class="h-section">Theo băng — <em class="hi">mở bài đến Music</em></h2>
  <p class="small" style="margin-bottom: 16px;">Lời thoại trùng audioscript kèm sách / file audio bản quyền — từ <span class="tx-hit">highlight</span> là tín hiệu khớp ô trống trong đề.</p>
  <div class="script-box script-box--full">
    <p><span class="ln">S</span>Good morning. Hinchingbrooke Country Park, Sally speaking. I&rsquo;m one of the rangers.</p>
    <p><span class="ln">J</span>Oh hello. My name&rsquo;s John Chapman, and I&rsquo;m a teaching assistant at a local primary school. I&rsquo;ve been asked to arrange a visit to the park for two of our classes.</p>
    <p><span class="ln">S</span>OK. What would you like to know?</p>
    <p><span class="ln">J</span>Well, I&rsquo;m new to this area, so perhaps you could tell me something about the park first, please.</p>
    <p><span class="ln">S</span>Of course. Altogether the park covers <span class="tx-hit">170 acres</span>, that&rsquo;s <span class="tx-hit">69 hectares</span>. There are three main types of habitat: wetland, grassland and woodland. The woods are well established and varied, with an oak plantation, and other areas of mixed species.</p>
    <p><span class="ln">J</span>Right.</p>
    <p><span class="ln">S</span>The wetland is quite varied, too. The original farmland was dug up around 40 years ago to extract gravel. Once this work was completed, the gravel pits filled with water, forming the two large lakes. There are also several smaller ones, ponds and a <span class="tx-hit">stream</span> that flows through the park.</p>
    <p><span class="ln">J</span>OK, so I suppose with these different habitats there&rsquo;s quite a variety of wildlife.</p>
    <p><span class="ln">S</span>There certainly is – a lot of different species of birds and insects, and also animals like deer and rabbits.</p>
    <p><span class="ln">J</span>And I understand you organise educational visits for school parties.</p>
    <p><span class="ln">S</span>That&rsquo;s right. We can organise a wide range of activities and adapt them to suit all ages.</p>
    <p><span class="ln">J</span>Can you give me some examples of the activities?</p>
    <p><span class="ln">S</span>Well, one focus is on science, where we help children to discover and study plants, trees and insects. They also collect and analyse <span class="tx-hit">data</span> about the things they see.</p>
    <p><span class="ln">J</span>Uhuh.</p>
    <p><span class="ln">S</span>Another focus is on geography. The park is a great environment to learn and practice reading a <span class="tx-hit">map</span> and using a compass to navigate around the park.</p>
    <p><span class="ln">J</span>Do you do anything connected with history?</p>
    <p><span class="ln">S</span>Yes, we do. For instance, the children can explore how the use of the land has changed over time. Then there&rsquo;s leisure and tourism.</p>
    <p><span class="ln">J</span>That focuses on your <span class="tx-hit">visitors</span>, I would imagine.</p>
    <p><span class="ln">S</span>Yes, mostly. The children find out about them, their requirements, the problems they may cause and how we manage these. And another subject we cover is music: here the children experiment with natural materials to create <span class="tx-hit">sounds</span> and explore <span class="tx-hit">rhythm and tempo</span>.</p>
    <p><span class="ln">J</span>That must be fun!</p>
    <p><span class="ln">S</span>Most children really enjoy it.</p>
  </div>""",
    ),
    (
        "Transcript2",
        "Transcript · phần 2 / 2",
        """<p class="eyebrow">Full transcript · Cambridge 19 · Test 1 · Part 1 · 2/2</p>
  <h2 class="h-section">Theo băng — <em class="hi">lợi ích &amp; giá</em></h2>
  <div class="script-box script-box--full">
    <p><span class="ln">S</span>And of course, all the activities are educational, too. Learning outside the classroom encourages children to be creative, and to explore and discover for themselves.</p>
    <p><span class="ln">J</span>I would imagine they get a sense of <span class="tx-hit">freedom</span> that might not be a normal part of their lives.</p>
    <p><span class="ln">S</span>That&rsquo;s right. And very often the children discover that they can do things they didn&rsquo;t know they could do, and they develop new <span class="tx-hit">skills</span>. This gives them greater self-confidence.</p>
    <p><span class="ln">J</span>It sounds great. So, what about the practical side of it? How much does it cost for a full-day visit? We would expect to bring between 30 and 40 children.</p>
    <p><span class="ln">S</span>If there are over 30, it costs <span class="tx-hit">&pound;4.95</span> for each child who attends on the day. We invoice you afterwards, so you don&rsquo;t pay for children who can&rsquo;t come because of sickness, for example. There&rsquo;s no charge for <span class="tx-hit">leaders</span> and other adults – as many as you want to bring.</p>
    <p><span class="ln">J</span>That sounds very fair. Well, thanks for all the information. I&rsquo;ll need to discuss it with my colleagues, and I hope to get back to you soon to make a booking.</p>
    <p><span class="ln">S</span>We&rsquo;ll look forward to hearing from you. Goodbye.</p>
    <p><span class="ln">J</span>Goodbye, and thank you.</p>
  </div>
  <p class="fine">Q1: cùng một câu có cả <em>acres</em> và <em>hectares</em> — ô đề hỏi hectares → ghi số <strong>69</strong>. Q9: mức giá khi trên 30 trẻ.</p>""",
    ),
    (
        "Walkthrough15",
        "Giải từng câu · Q1–5",
        """<p class="eyebrow">Answer walkthrough · Q1–5</p>
  <h2 class="h-section">Năm ô đầu — <em class="hi">tín hiệu nghe</em></h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Q1 · <em class="hi">69</em></span><span class="step-body">Audio: &ldquo;Altogether the park covers <strong>170 acres</strong>, that&rsquo;s <strong>69 hectares</strong>.&rdquo; — ô Area (hectares) ghi <strong>69</strong>; đừng chép nhầm <strong>170</strong> hay đơn vị acres.</span></div></li>
    <li><div><span class="step-title">Q2 · <em class="hi">stream</em></span><span class="step-body">Sau hai hồ lớn: &ldquo;ponds and a <strong>stream</strong> that flows through the park&rdquo; — một từ cho ô wetland.</span></div></li>
    <li><div><span class="step-title">Q3 · <em class="hi">data</em></span><span class="step-body">Science: &ldquo;They also collect and analyse <strong>data</strong> about the things they see&rdquo; — đề paraphrase &ldquo;look at &hellip; about plants&rdquo; nhưng key vẫn là <strong>data</strong>.</span></div></li>
    <li><div><span class="step-title">Q4 · <em class="hi">map</em></span><span class="step-body">&ldquo;reading a <strong>map</strong> and using a compass&rdquo; — ô đứng trước <em>and compass</em>.</span></div></li>
    <li><div><span class="step-title">Q5 · <em class="hi">visitors</em></span><span class="step-body">John nói leisure &amp; tourism &ldquo;focuses on your <strong>visitors</strong>&rdquo; — Sally xác nhận &ldquo;Yes, mostly&rdquo; rồi giải thích thêm.</span></div></li>
  </ol>""",
    ),
    (
        "Walkthrough610",
        "Giải từng câu · Q6–10",
        """<p class="eyebrow">Answer walkthrough · Q6–10</p>
  <h2 class="h-section">Năm ô sau — <em class="hi">collocation &amp; giá</em></h2>
  <ol class="num-list tight">
    <li><div><span class="step-title">Q6 · <em class="hi">sounds</em></span><span class="step-body">Audio: &ldquo;create <strong>sounds</strong>&rdquo; với natural materials; đề dùng động từ <em>make</em> — cùng nghĩa; <em>rhythm and tempo</em> đã in trong đề.</span></div></li>
    <li><div><span class="step-title">Q7 · <em class="hi">freedom</em></span><span class="step-body">&ldquo;a sense of <strong>freedom</strong>&rdquo; — một từ trong Benefits.</span></div></li>
    <li><div><span class="step-title">Q8 · <em class="hi">skills</em></span><span class="step-body">&ldquo;develop new <strong>skills</strong>&rdquo; — ngay sau đoạn về freedom.</span></div></li>
    <li><div><span class="step-title">Q9 · <em class="hi">4.95</em></span><span class="step-body">&ldquo;If there are <strong>over 30</strong>, it costs <strong>&pound;4.95</strong> for each child&rdquo; — ô đã có ký hiệu £ → ghi <strong>4.95</strong>.</span></div></li>
    <li><div><span class="step-title">Q10 · <em class="hi">leaders</em></span><span class="step-body">&ldquo;no charge for <strong>leaders</strong> and other adults&rdquo; — đề &ldquo;Adults, such as &hellip;&rdquo; một từ; key Cambridge: <strong>leaders</strong>.</span></div></li>
  </ol>""",
    ),
]

practice_block(
    11,
    "01",
    "Hinchingbrooke Country Park",
    "Section 1",
    "S1",
    0,
    TOC_ALL,
    "<em>Hinchingbrooke</em><br>Country Park<br><span style=\"font-size:0.85em\">Cambridge IELTS 19 · Test 1 · S1</span>",
    f"""<h2 class="h-sub" style="font-size: 34px; margin-bottom: 16px;">Complete the notes below. Write <strong>ONE WORD AND/OR A NUMBER</strong> for each answer.</h2>
       <p class="small">You will hear Sally from Hinchingbrooke Country Park (ranger) and John Chapman (teaching assistant) arranging an educational visit for school classes.</p>
       <div class="audio-meta">
         <div class="cell"><div class="k">Giọng</div><div class="v">2</div><div class="d">Ranger + teaching assistant</div></div>
         <div class="cell"><div class="k">Độ dài</div><div class="v">~7′</div><div class="d">10 gaps · form</div></div>
         <div class="cell"><div class="k">Chủ đề</div><div class="v">Nature park</div><div class="d">Habitats · education visit · practical info</div></div>
       </div>
       <div class="practice-audio"><audio controls preload="metadata" src="{_LISTENING_P1_MP3}">Trình duyệt không hỗ trợ &lt;audio&gt;.</audio></div>
       <p class="source-note">Ghi âm từ <strong>bộ Cambridge IELTS 19</strong> bạn đã mua — file trong project: <code>listening/lesson/1/audio/cam19-test1-part1.mp3</code> (copy từ <code>Test1 Part1.mp3</code> trong thư mục audio bản quyền).</p>""",
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
         <div class="qtype-item"><div class="n">Q1</div><div><div class="t">Số + đơn vị</div><div class="s">Một câu có cả <em>acres</em> và <em>hectares</em> — ô hỏi hectares → ghi đúng số hectares, không chép nhầm acres.</div></div></div>
         <div class="qtype-item"><div class="n">Q2–4</div><div><div class="t">Môn học song song</div><div class="s">Science → Geography → History — mỗi môn một fact ngắn.</div></div></div>
         <div class="qtype-item"><div class="n">Q6</div><div><div class="t">Danh từ đếm được</div><div class="s">Collocation với <em>make … with materials</em> — không nhầm với <em>rhythm / tempo</em> (đã in trong đề).</div></div></div>
         <div class="qtype-item"><div class="n">Q9</div><div><div class="t">Giá</div><div class="s">Độ chính xác đến pence — hai phần số sau dấu chấm.</div></div></div>
       </div>
       <p class="fine" style="margin-top: 28px;">Trước khi nghe: đánh dấu từ loại cho từng ô (số / danh từ / từ chỉ người).</p>""",
    """<ul class="num-list tight" style="margin-top: 8px;">
         <li><div><span class="step-title">Đơn vị diện tích.</span><span class="step-body">Cùng lúc có <em>170 acres</em> và <em>69 hectares</em> — ô Area (hectares) chỉ ghi <strong>69</strong>.</span></div></li>
         <li><div><span class="step-title">Giá vé trẻ em.</span><span class="step-body">Điều kiện <em>over 30</em> children → <em>£4.95</em> each; invoice sau — không trả tiền trẻ vắng vì ốm.</span></div></li>
         <li><div><span class="step-title">Người lớn miễn phí.</span><span class="step-body">Nghe &ldquo;no charge for <strong>leaders</strong> and other adults&rdquo; — ô <em>such as …</em> một từ → <strong>leaders</strong>.</span></div></li>
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
       <p class="fine">Đáp án khớp Cambridge IELTS 19 Test 1 Listening Section 1 — đối chiếu spelling / số với transcript chính thức.</p>""",
    """<div class="script-box" style="max-height: 520px; overflow-y: auto;">
         <p><span class="ln">S</span>Hinchingbrooke Country Park, Sally speaking. I&rsquo;m one of the rangers.</p>
         <p><span class="ln">J</span>John Chapman — teaching assistant — arranging a visit for two classes.</p>
         <p><span class="ln">S</span>The park covers <span class="tx-hit">170 acres</span>, that&rsquo;s <span class="tx-hit">69 hectares</span> … wetland … ponds and a <span class="tx-hit">stream</span> … collect and analyse <span class="tx-hit">data</span> … read a <span class="tx-hit">map</span> and compass … leisure and tourism — your <span class="tx-hit">visitors</span> … create <span class="tx-hit">sounds</span>, <span class="tx-hit">rhythm and tempo</span>.</p>
         <p><span class="ln">J</span>Sense of <span class="tx-hit">freedom</span> … new <span class="tx-hit">skills</span> … over 30 children → <span class="tx-hit">&pound;4.95</span> each … no charge for <span class="tx-hit">leaders</span> and other adults.</p>
       </div>""",
    """<ul class="annot-list">
         <li><span class="tag">Q1</span><b>Acres + hectares:</b> &ldquo;<strong>170 acres</strong>, that&rsquo;s <strong>69 hectares</strong>&rdquo; — ô hectares ghi <em>69</em> (không chép 170).</li>
         <li><span class="tag">Q2</span>Sau “lakes and ponds” → nối tiếp <em>a stream</em>.</li>
         <li><span class="tag">Q3</span><em>Collect data</em> about plants → một từ <strong>data</strong>.</li>
         <li><span class="tag">Q4</span><em>Use a map and compass</em> — từ khóa đứng ngay trước <em>and compass</em>.</li>
         <li><span class="tag">Q5</span>Leisure unit: trọng tâm là <em>visitors</em> (không phải staff).</li>
         <li><span class="tag">Q6</span><em>Make sounds</em> với materials; rhythm/tempo là phần thử nghiệm thêm.</li>
         <li><span class="tag">Q7–8</span><em>Feeling of freedom</em> · <em>learn new skills</em>.</li>
         <li><span class="tag">Q9–10</span><em>£4.95</em> · adults such as <em>leaders</em> (one word).</li>
       </ul>""",
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">ranger</div><div class="vocab-meaning">employee who protects / guides in a park</div></div>
         <div class="vocab-item"><div class="vocab-word">wetland · stream</div><div class="vocab-meaning">marshy area · small flowing water</div></div>
         <div class="vocab-item"><div class="vocab-word">hectare · acre</div><div class="vocab-meaning">area units — same utterance may give both; match the gap unit</div></div>
         <div class="vocab-item"><div class="vocab-word">navigate · map + compass</div><div class="vocab-meaning">find direction in the field</div></div>
         <div class="vocab-item"><div class="vocab-word">make sounds</div><div class="vocab-meaning">collocation · music activity</div></div>
         <div class="vocab-item"><div class="vocab-word">group leaders</div><div class="vocab-meaning">adults supervising children on a trip</div></div>
       </div>""",
    """<div class="mistake-grid">
         <div class="mistake"><div class="x">×</div><div><h4>Ghi 170 hoặc &ldquo;acres&rdquo; vào ô hectares</h4><p><strong>170</strong> là số <em>acres</em> trong cùng câu; đáp án ô Area (hectares) là <strong>69</strong>.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Điền river</h4><p>Audio nói <em>a stream</em> nối giữa lakes/ponds — chính tả pool/river nếu nghe nhầm.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Q6 điền tempo</h4><p>Ô cần danh từ cho “make ___ with materials”; tempo nằm ở mệnh đề sau.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Viết £4.95 trong ô chỉ cần số</h4><p>Nếu đề đã in £ — thường chỉ ghi <strong>4.95</strong>.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Q10 parents</h4><p>Trên băng là <em>leaders and other adults</em> — key Cambridge một từ: <strong>leaders</strong>.</p></div></div>
       </div>""",
    extra_after_step3=P01_EXTRA_AFTER_STEP3,
)

# Practice 02 — Section 2
practice_block(
    24,
    "02",
    "Campus tour",
    "Section 2",
    "S2",
    1,
    TOC_ALL,
    "<em>New</em><br>Arts<br>Building tour.",
    """<h2 class="h-sub" style="font-size: 34px; margin-bottom: 16px;">Questions 6–10: multiple choice. Choose the correct letter <strong>A, B or C</strong>.</h2>
       <p class="small">You will hear a guide showing new students around the Arts Building.</p>
       <div class="audio-meta">
         <div class="cell"><div class="k">Giọng</div><div class="v">1</div><div class="d">Tour guide</div></div>
         <div class="cell"><div class="k">Bài liên quan</div><div class="v">Map</div><div class="d">Q11–14 trên sơ đồ (lớp khác)</div></div>
         <div class="cell"><div class="k">Focus</div><div class="v">Opinion</div><div class="d">So sánh A/B/C</div></div>
       </div>""",
    """<div class="ex-card"><span class="tag">MCQ stems · 6–8</span>
       <p style="margin:0 0 12px; font-size: 24px;"><strong>6</strong> The sculpture workshop is closed on …</p>
       <p style="margin:0 0 12px; font-size: 22px; color: var(--ink-soft);">A Mondays &nbsp; B Wednesdays &nbsp; C Fridays</p>
       <p style="margin:0 0 12px; font-size: 24px;"><strong>7</strong> Students need a pass to enter …</p>
       <p style="margin:0; font-size: 22px; color: var(--ink-soft);">A the darkroom &nbsp; B the print studio &nbsp; C the lecture theatre</p>
       </div>""",
    """<div class="qtype-grid">
         <div class="qtype-item"><div class="n">Q6</div><div><div class="t">Distractor pattern</div><div class="s">Nghe cả “Monday” và “Friday” — một ngày là lịch cũ</div></div></div>
         <div class="qtype-item"><div class="n">Q7</div><div><div class="t">Paraphrase “pass”</div><div class="s">access card / swipe card</div></div></div>
       </div>""",
    """<ol class="num-list tight"><li><div><span class="step-title">Đánh dấu từ khác biệt giữa A/B/C.</span><span class="step-body">Chỉ 1–2 từ / lựa chọn — Monday vs Wednesday vs Friday.</span></div></li>
         <li><div><span class="step-title">Chờ mệnh đề xác nhận cuối.</span><span class="step-body">“So from this term, it’s <strong>Wednesday</strong> afternoons only.”</span></div></li></ol>""",
    """<div class="key-grid key-grid--3">
         <div class="k"><div class="q">6</div><div class="a">B</div></div>
         <div class="k"><div class="q">7</div><div class="a">A</div></div>
         <div class="k"><div class="q">8</div><div class="a">C</div></div>
       </div>
       <p class="fine">MCQ: đáp án đúng thường được <em>khẳng định lại</em> sau khi loại các lựa chọn còn lại.</p>""",
    """<div class="script-box">
         <p><span class="ln">G</span>…the workshop used to shut on Mondays, but <strong>from this month it’s Wednesday afternoons</strong> because of staff training…</p>
         <p><span class="ln">G</span>For the darkroom, you’ll need your <strong>student pass</strong> — the print studio is open to everyone.</p>
       </div>""",
    """<ul class="annot-list">
         <li><span class="tag">Q6</span><b>Used to</b> vs <b>from this month</b> — đáp án theo thông tin mới nhất.</li>
         <li><span class="tag">Q7</span>Đối chiếu <em>darkroom</em> với “need pass” — studio không cần.</li>
       </ul>""",
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">used to</div><div class="vocab-meaning">past habit — thường đi kèm correction</div></div>
         <div class="vocab-item"><div class="vocab-word">from this term / month</div><div class="vocab-meaning">signal of updated rule</div></div>
         <div class="vocab-item"><div class="vocab-word">student pass</div><div class="vocab-meaning">= access card / ID swipe</div></div>
       </div>""",
    """<div class="mistake-grid">
         <div class="mistake"><div class="x">×</div><div><h4>Chọn đáp án nghe thấy đầu tiên</h4><p>IELTS hay đưa đúng thứ tự A/B/C trong audio nhưng <em>sai ngữ cảnh</em>.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Không đọc stem kỹ</h4><p>“need a pass to enter” vs “need a pass to borrow equipment” — khác hoàn toàn.</p></div></div>
       </div>""",
)

# Practice 03 — Section 3
practice_block(
    33,
    "03",
    "Assignment discussion",
    "Section 3",
    "S3",
    2,
    TOC_ALL,
    "<em>Marketing</em><br>essay<br>plan.",
    """<h2 class="h-sub" style="font-size: 34px; margin-bottom: 16px;">Who expresses which opinion? Match each opinion to <strong>A–D</strong> (students + tutor).</h2>
       <p class="small">You will hear three students and a tutor discussing an essay on consumer behaviour.</p>""",
    """<div class="ex-card"><span class="tag">Opinions · 15–18</span>
       <div class="q-strip"><span class="n">15</span><span>The introduction should define key terms.</span></div>
       <div class="q-strip"><span class="n">16</span><span>Case studies are more useful than surveys.</span></div>
       <div class="q-strip"><span class="n">17</span><span>The word limit is too tight for the topic.</span></div>
       <div class="q-strip"><span class="n">18</span><span>They should include a counter-argument paragraph.</span></div>
       <p class="small" style="margin-top:16px;">A Anna · B Ben · C Carla · D Tutor</p>
       </div>""",
    """<div class="two-col"><div class="col-card"><p class="mono-label">Trước khi nghe</p><h3>Ghi tên + vai trò</h3><ul><li>Anna: thích lý thuyết</li><li>Ben: thích dữ liệu thực địa</li><li>Carla: lo chữ</li><li>Tutor: đưa rubric</li></ul></div>
         <div class="col-card"><p class="mono-label">Paraphrase stem</p><h3>“define key terms”</h3><ul><li>nghe: <em>operationalise the concepts in the first paragraph</em></li></ul></div></div>""",
    """<p class="body">Theo dõi <em class="hi">chủ ngữ câu</em>: “I think / In my view / What I’d suggest is” — map về A–D trên giấy nháp trong lần nghe 1.</p>""",
    """<div class="key-grid key-grid--4">
         <div class="k"><div class="q">15</div><div class="a">D</div></div>
         <div class="k"><div class="q">16</div><div class="a">B</div></div>
         <div class="k"><div class="q">17</div><div class="a">C</div></div>
         <div class="k"><div class="q">18</div><div class="a">D</div></div>
       </div>""",
    """<div class="script-box">
         <p><span class="ln">T</span>In academic writing, you should <strong>operationalise your key concepts</strong> right at the start…</p>
         <p><span class="ln">B</span>I’m not convinced by surveys here — <strong>case studies</strong> give richer insight…</p>
         <p><span class="ln">C</span>Honestly, <strong>2,000 words feels tight</strong> for this topic…</p>
         <p><span class="ln">T</span>And yes, add <strong>a counter-argument section</strong> — the rubric rewards it.</p>
       </div>""",
    """<ul class="annot-list">
         <li><span class="tag">S3</span>Giảng viên thường mang <b>rubric</b> — ý chuẩn hay từ tutor.</li>
         <li><span class="tag">Para</span>“operationalise” = define key terms (academic paraphrase).</li>
       </ul>""",
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">operationalise</div><div class="vocab-meaning">define for use in the essay</div></div>
         <div class="vocab-item"><div class="vocab-word">case study</div><div class="vocab-meaning">deep example vs broad survey</div></div>
         <div class="vocab-item"><div class="vocab-word">counter-argument</div><div class="vocab-meaning"> opposing view then refute</div></div>
       </div>""",
    """<div class="mistake-grid">
         <div class="mistake"><div class="x">×</div><div><h4>Nhầm giọng nam/nữ</h4><p>Lập bảng 4 cột trước — mỗi ý kiến gạch tên ngay khi nghe.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Match theo từ giống stem</h4><p>IELTS paraphrase mạnh ở Section 3.</p></div></div>
       </div>""",
)

# Practice 04 — Section 4
practice_block(
    42,
    "04",
    "Urban ecology lecture",
    "Section 4",
    "S4",
    3,
    TOC_ALL,
    "<em>Green</em><br>infrastructure<br>lecture.",
    """<h2 class="h-sub" style="font-size: 34px; margin-bottom: 16px;">Complete the notes below. Write <strong>NO MORE THAN TWO WORDS</strong> for each answer.</h2>
       <p class="small">One speaker · academic lecture · dense information in the second half.</p>""",
    """<div class="ex-card"><span class="tag">Notes · gaps 19–24 (sample)</span>
       <p style="font-size:23px; line-height:1.55; color:var(--ink-soft); margin:0;">
         Green roofs reduce <strong>19 ……………</strong> in summer.<br>
         The main cost barrier is <strong>20 ……………</strong>.<br>
         Cities use <strong>21 ……………</strong> to manage stormwater.<br>
         Biodiversity improves when plants are <strong>22 ……………</strong>.<br>
       </p></div>""",
    """<div class="flow" style="margin-top:8px;">
         <div class="flow-step"><div class="n">01</div><div class="t">Skim headings</div><div class="d">3–4 ý lớn của bài giảng</div><div class="time">45″</div></div>
         <div class="flow-step"><div class="n">02</div><div class="t">Predict word class</div><div class="d">19: noun (heat? runoff?) · 20: noun phrase</div><div class="time">60″</div></div>
         <div class="flow-step"><div class="n">03</div><div class="t">Track signposts</div><div class="d">Firstly / However / In conclusion</div><div class="time">while</div></div>
         <div class="flow-step"><div class="n">04</div><div class="t">Second listen</div><div class="d">Chỉ điền chỗ trống — không sửa toàn bài</div><div class="time">replay</div></div>
       </div>""",
    """<p class="body">Section 4: <em class="hi">đáp án thường là cụm danh từ</em> ngay sau signpost “the key point is / what we call”.</p>""",
    """<div class="key-grid key-grid--3">
         <div class="k"><div class="q">19</div><div class="a">heat / heat gain</div></div>
         <div class="k"><div class="q">20</div><div class="a">maintenance / maintenance costs</div></div>
         <div class="k"><div class="q">21</div><div class="a">bioswales</div></div>
       </div>
       <p class="fine">Nếu audio nói <em>bioswales</em> — chính xác chính tả; nếu không chắc, ghi phiên âm gần đúng rồi đối chiếu lần 2.</p>""",
    """<div class="script-box">
         <p><span class="ln">L</span>…green roofs can significantly reduce <strong>heat gain</strong> in urban corridors…</p>
         <p><span class="ln">L</span>…the barrier most cities cite is not installation but <strong>ongoing maintenance</strong>…</p>
         <p><span class="ln">L</span>…<strong>bioswales</strong> are shallow vegetated channels used to slow runoff…</p>
       </div>""",
    """<ul class="annot-list">
         <li><span class="tag">19</span>Sau “reduce” → danh từ / noun phrase.</li>
         <li><span class="tag">21</span>Từ chuyên ngành — tái hiện đúng spelling từ audio.</li>
       </ul>""",
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">green infrastructure</div><div class="vocab-meaning">roofs · parks · drainage as a system</div></div>
         <div class="vocab-item"><div class="vocab-word">stormwater</div><div class="vocab-meaning">rainwater runoff in cities</div></div>
         <div class="vocab-item"><div class="vocab-word">biodiversity</div><div class="vocab-meaning">range of species — spelling with two i’s</div></div>
       </div>""",
    """<div class="mistake-grid">
         <div class="mistake"><div class="x">×</div><div><h4>Viết từ đồng nghĩa không có trong audio</h4><p>Đáp án phải <em>exact wording from recording</em> (trừ khi đề cho multiple acceptable answers).</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Mất chỗ ở S4 vì cố ghi hết</h4><p>Ưu tiên ô trống — bỏ qua 5 giây không hiểu, quay lại lần 2.</p></div></div>
       </div>""",
)

# 51 PATTERNS
slides.append(f"""<!-- 51 · PATTERNS -->
<section data-label="51 Patterns" class="slide">
  <div class="run-header"><span>Tổng kết</span><span class="rule"></span><span>Pattern chung</span></div>
  <p class="eyebrow">Patterns across 4 practices</p>
  <h2 class="h-section">Bốn điều <em class="hi">lặp lại</em> trong mọi section</h2>
  <div class="patt-grid" style="margin-top: 8px;">
    <div class="patt"><div class="t">01 · Paraphrase</div><div class="d">Đề không trùng audio — luôn đổi từ hoặc cấu trúc.</div><div class="ex">“near the centre” ↔ <em>close to the downtown campus</em></div></div>
    <div class="patt"><div class="t">02 · Correction</div><div class="d">Actually / sorry / I mean — thông tin đúng đến sau.</div><div class="ex">Giá / tên / ngày hay bị sửa.</div></div>
    <div class="patt"><div class="t">03 · Word limit</div><div class="d">Đếm từ trước khi chép sang answer sheet.</div><div class="ex">NO MORE THAN TWO WORDS</div></div>
    <div class="patt"><div class="t">04 · Spelling</div><div class="d">Proper nouns &amp; technical terms — độ khó tăng dần tới S4.</div><div class="ex">bioswales · accommodation</div></div>
  </div>
  {foot(51)}
</section>""")

# 52 TAKEAWAYS
slides.append(f"""<!-- 52 · TAKEAWAYS -->
<section data-label="52 Takeaways" class="slide slide--paper">
  <div class="run-header"><span>Tổng kết</span><span class="rule"></span><span>Takeaways</span></div>
  <p class="eyebrow">Key Takeaways · 8 điểm</p>
  <h2 class="h-section">Tám điều <em class="hi">mang về nhà.</em></h2>
  <div class="take">
    <div class="item"><div class="k">01</div><div class="v">Đọc trước — dự đoán loại từ mỗi ô trống.</div></div>
    <div class="item"><div class="k">02</div><div class="v">S1: spelling + số — không mất điểm “ngu”.</div></div>
    <div class="item"><div class="k">03</div><div class="v">S2: MCQ chờ xác nhận cuối — tránh distractor đầu.</div></div>
    <div class="item"><div class="k">04</div><div class="v">Map: định hướng + nhãn trước khi nghe.</div></div>
    <div class="item"><div class="k">05</div><div class="v">S3: bảng người — ý kiến paraphrase mạnh.</div></div>
    <div class="item"><div class="k">06</div><div class="v">S4: outline 3 ý lớn trong pause.</div></div>
    <div class="item"><div class="k">07</div><div class="v">Luôn kiểm tra giới hạn từ trước khi nộp bài.</div></div>
    <div class="item"><div class="k">08</div><div class="v">Nghe lại transcript sau buổi — sửa chỗ tai “trễ”.</div></div>
  </div>
  {foot(52)}
</section>""")

# 53 WEEKLY PLAN
slides.append(f"""<!-- 53 · WEEKLY PLAN -->
<section data-label="53 Weekly Plan" class="slide">
  <div class="run-header"><span>Tổng kết</span><span class="rule"></span><span>Lịch luyện tuần</span></div>
  <p class="eyebrow">Weekly Practice Plan · 7 days</p>
  <h2 class="h-section">25–30 phút/ngày — <em class="hi">tai quen tốc độ IELTS.</em></h2>
  <div class="plan-grid">
    <div class="hdr">Day</div><div class="hdr">Nhiệm vụ</div><div class="hdr">Nội dung</div><div class="hdr">Thời lượng</div>
    <div class="day">Thứ 2</div><div>S1 form completion</div><div>Cambridge Test · chỉ S1 · chép sai chính tả vào sổ.</div><div class="time">30′</div>
    <div class="day">Thứ 3</div><div>S2 MCQ + map</div><div>1 đề · khoanh distractor trong transcript.</div><div class="time">30′</div>
    <div class="day">Thứ 4</div><div>S3 matching</div><div>Nghe 1 lần không pause — lần 2 chỉ chỗ sai.</div><div class="time">30′</div>
    <div class="day">Thứ 5</div><div>S4 note completion</div><div>Outline trước khi nghe lần 1.</div><div class="time">30′</div>
    <div class="day">Thứ 6</div><div>Full test Listening</div><div>40 câu · timing thật · transfer 10′.</div><div class="time">40′</div>
    <div class="day">Thứ 7</div><div>Review transcript</div><div>Highlight paraphrase pairs (đề ↔ audio).</div><div class="time">45′</div>
    <div class="day">CN</div><div>Shadowing 10′</div><div>Đoạn S2 hoặc S4 — bắt chước stress &amp; chunking.</div><div class="time">25′</div>
  </div>
  {foot(53)}
</section>""")

# 54 END
slides.append("""<!-- 54 · END -->
<section data-label="54 End" class="slide end-slide">
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
