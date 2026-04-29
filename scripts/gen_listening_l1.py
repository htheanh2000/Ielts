#!/usr/bin/env python3
"""Generate listening/lesson/1/index.html — 50 slides, same spine as writing/lesson/2."""

import os
from html import escape

FOOTER = "IELTS Listening · Lesson 01"


def foot(n: int) -> str:
    return f'<div class="run-footer"><span class="footer-topic">{FOOTER}</span><span>{n} / 50</span></div>'


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
      <div><dt>Thực hành</dt><dd>4 bài (P1 có audio)</dd></div>
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
    <li><div><span class="step-title">Practice 01 · Section 1 — Hinchingbrooke Country Park.</span><span class="step-body">9 slide · 18 phút. Cambridge 19 Test 1 · form · 10 gap · audio + autoscript.</span></div></li>
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
    n += 1
    slides.append(f"""<!-- {n:02d} · SAMPLE SCRIPT -->
<section data-label="{n:02d} Script" class="slide">
  <div class="run-header"><span>Practice {practice_num} · {section_name}</span><span class="rule"></span><span>Transcript rút gọn</span></div>
  <p class="eyebrow">Script excerpt · Trainer version</p>
  <h2 class="h-section">Đoạn thoại <em class="hi">minh họa</em> (rút gọn)</h2>
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
       <p class="small">You will hear a park ranger, Sally, talking to John, a teaching assistant, about Hinchingbrooke Country Park — a day visit for school children.</p>
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
         <div class="qtype-item"><div class="n">Q1</div><div><div class="t">Số + đơn vị</div><div class="s">Hectares vs <em>acres</em> — nghe kỹ số cuối cùng sau chỗ “actually / but”.</div></div></div>
         <div class="qtype-item"><div class="n">Q2–4</div><div><div class="t">Môn học song song</div><div class="s">Science → Geography → History — mỗi môn một fact ngắn.</div></div></div>
         <div class="qtype-item"><div class="n">Q6</div><div><div class="t">Danh từ đếm được</div><div class="s">Collocation với <em>make … with materials</em> — không nhầm với <em>rhythm / tempo</em> (đã in trong đề).</div></div></div>
         <div class="qtype-item"><div class="n">Q9</div><div><div class="t">Giá</div><div class="s">Độ chính xác đến pence — hai phần số sau dấu chấm.</div></div></div>
       </div>
       <p class="fine" style="margin-top: 28px;">Trước khi nghe: đánh dấu từ loại cho từng ô (số / danh từ / từ chỉ người).</p>""",
    """<ul class="num-list tight" style="margin-top: 8px;">
         <li><div><span class="step-title">Đơn vị diện tích.</span><span class="step-body">Nghe <em>170 acres</em> xuất hiện trước — đáp án thường là thông tin được <strong>sửa</strong> sang hectares.</span></div></li>
         <li><div><span class="step-title">Giá vé trẻ em.</span><span class="step-body">Xác nhận <em>pounds and pence</em> — không tròn nếu audio đọc chính xác.</span></div></li>
         <li><div><span class="step-title">Người lớn miễn phí.</span><span class="step-body">Nghe cụm <em>parents or group leaders</em> — ô chỉ một từ → chọn từ cuối cụm được nêu làm ví dụ.</span></div></li>
       </ul>""",
    """<div class="key-grid" style="grid-template-columns: repeat(5, 1fr); margin-top: 12px;">
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
       <p class="fine">Đáp án khớp Cambridge IELTS 19 Test 1 Listening Section 1 — đối chiếu spelling / số với transcipt chính thức.</p>""",
    """<div class="script-box" style="max-height: 520px; overflow-y: auto;">
         <p><span class="ln">S</span>Good morning, everyone, and welcome to Hinchingbrooke Country Park. My name’s Sally… you <strong>follow me</strong>?</p>
         <p><span class="ln">J</span>…I’m interested in the area <strong>surrounding the lake</strong>… I believe … overall size increased … <strong>28 hectares</strong> … <strong>actually</strong> covers <strong>just under 70 hectares</strong>.</p>
         <p><span class="ln">S</span>There’s a <strong>stream</strong> … a number of small areas of trees … the study of plants, including finding out what they’re good for … collecting <strong>data</strong> to study …</p>
         <p><span class="ln">S</span>They can use a <strong>map</strong> and compass to learn about the countryside … leisure and tourism … focusing on <strong>visitors</strong> … making <strong>sounds</strong> with natural materials … rhythm and <em>tempo</em> …</p>
         <p><span class="ln">S</span>…sense of <strong>freedom</strong> they don’t get elsewhere… learn <strong>skills</strong> … <strong>four pounds and 95 pence</strong> per child … adults like parents or group <strong>leaders</strong> for free.</p>
       </div>""",
    """<div class="annot-list">
         <li><span class="tag">Q1</span><b>Correction:</b> 28 → “actually just under <strong>70</strong>” → ô hectares ghi <em>69</em>.</li>
         <li><span class="tag">Q2</span>Sau “lakes and ponds” → nối tiếp <em>a stream</em>.</li>
         <li><span class="tag">Q3</span><em>Collect data</em> about plants → một từ <strong>data</strong>.</li>
         <li><span class="tag">Q4</span><em>Use a map and compass</em> — từ khóa đứng ngay trước <em>and compass</em>.</li>
         <li><span class="tag">Q5</span>Leisure unit: trọng tâm là <em>visitors</em> (không phải staff).</li>
         <li><span class="tag">Q6</span><em>Make sounds</em> với materials; rhythm/tempo là phần thử nghiệm thêm.</li>
         <li><span class="tag">Q7–8</span><em>Feeling of freedom</em> · <em>learn new skills</em>.</li>
         <li><span class="tag">Q9–10</span><em>£4.95</em> · adults such as <em>leaders</em> (one word).</li>
       </div>""",
    """<div class="vocab-grid compact">
         <div class="vocab-item"><div class="vocab-word">ranger</div><div class="vocab-meaning">employee who protects / guides in a park</div></div>
         <div class="vocab-item"><div class="vocab-word">wetland · stream</div><div class="vocab-meaning">marshy area · small flowing water</div></div>
         <div class="vocab-item"><div class="vocab-word">hectare · acre</div><div class="vocab-meaning">area units — listen for correction</div></div>
         <div class="vocab-item"><div class="vocab-word">navigate · map + compass</div><div class="vocab-meaning">find direction in the field</div></div>
         <div class="vocab-item"><div class="vocab-word">make sounds</div><div class="vocab-meaning">collocation · music activity</div></div>
         <div class="vocab-item"><div class="vocab-word">group leaders</div><div class="vocab-meaning">adults supervising children on a trip</div></div>
       </div>""",
    """<div class="mistake-grid">
         <div class="mistake"><div class="x">×</div><div><h4>Ghi 170 hoặc acres</h4><p>Đó là distractor trước khi đổi sang <strong>69 hectares</strong>.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Điền river</h4><p>Audio nói <em>a stream</em> nối giữa lakes/ponds — chính tả pool/river nếu nghe nhầm.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Q6 điền tempo</h4><p>Ô cần danh từ cho “make ___ with materials”; tempo nằm ở mệnh đề sau.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Viết £4.95 trong ô chỉ cần số</h4><p>Nếu đề đã in £ — thường chỉ ghi <strong>4.95</strong>.</p></div></div>
         <div class="mistake"><div class="x">×</div><div><h4>Q10 parents</h4><p>Audio liệt kê parents <strong>or</strong> group leaders — đáp án một từ chuẩn là <strong>leaders</strong>.</p></div></div>
       </div>""",
)

# Practice 02 — Section 2
practice_block(
    20,
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
    """<div class="key-grid" style="grid-template-columns: repeat(3, 1fr);">
         <div class="k"><div class="q">6</div><div class="a">B</div></div>
         <div class="k"><div class="q">7</div><div class="a">A</div></div>
         <div class="k"><div class="q">8</div><div class="a">C</div></div>
       </div>
       <p class="fine">MCQ: đáp án đúng thường được <em>khẳng định lại</em> sau khi loại các lựa chọn còn lại.</p>""",
    """<div class="script-box">
         <p><span class="ln">G</span>…the workshop used to shut on Mondays, but <strong>from this month it’s Wednesday afternoons</strong> because of staff training…</p>
         <p><span class="ln">G</span>For the darkroom, you’ll need your <strong>student pass</strong> — the print studio is open to everyone.</p>
       </div>""",
    """<div class="annot-list">
         <li><span class="tag">Q6</span><b>Used to</b> vs <b>from this month</b> — đáp án theo thông tin mới nhất.</li>
         <li><span class="tag">Q7</span>Đối chiếu <em>darkroom</em> với “need pass” — studio không cần.</li>
       </div>""",
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
    29,
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
    """<div class="key-grid" style="grid-template-columns: repeat(4, 1fr);">
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
    """<div class="annot-list">
         <li><span class="tag">S3</span>Giảng viên thường mang <b>rubric</b> — ý chuẩn hay từ tutor.</li>
         <li><span class="tag">Para</span>“operationalise” = define key terms (academic paraphrase).</li>
       </div>""",
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
    38,
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
    """<div class="key-grid" style="grid-template-columns: repeat(3, 1fr);">
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
    """<div class="annot-list">
         <li><span class="tag">19</span>Sau “reduce” → danh từ / noun phrase.</li>
         <li><span class="tag">21</span>Từ chuyên ngành — tái hiện đúng spelling từ audio.</li>
       </div>""",
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

# 47 PATTERNS
slides.append(f"""<!-- 47 · PATTERNS -->
<section data-label="47 Patterns" class="slide">
  <div class="run-header"><span>Tổng kết</span><span class="rule"></span><span>Pattern chung</span></div>
  <p class="eyebrow">Patterns across 4 practices</p>
  <h2 class="h-section">Bốn điều <em class="hi">lặp lại</em> trong mọi section</h2>
  <div class="patt-grid" style="margin-top: 8px;">
    <div class="patt"><div class="t">01 · Paraphrase</div><div class="d">Đề không trùng audio — luôn đổi từ hoặc cấu trúc.</div><div class="ex">“near the centre” ↔ <em>close to the downtown campus</em></div></div>
    <div class="patt"><div class="t">02 · Correction</div><div class="d">Actually / sorry / I mean — thông tin đúng đến sau.</div><div class="ex">Giá / tên / ngày hay bị sửa.</div></div>
    <div class="patt"><div class="t">03 · Word limit</div><div class="d">Đếm từ trước khi chép sang answer sheet.</div><div class="ex">NO MORE THAN TWO WORDS</div></div>
    <div class="patt"><div class="t">04 · Spelling</div><div class="d">Proper nouns &amp; technical terms — độ khó tăng dần tới S4.</div><div class="ex">bioswales · accommodation</div></div>
  </div>
  {foot(47)}
</section>""")

# 48 TAKEAWAYS
slides.append(f"""<!-- 48 · TAKEAWAYS -->
<section data-label="48 Takeaways" class="slide slide--paper">
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
  {foot(48)}
</section>""")

# 49 WEEKLY PLAN
slides.append(f"""<!-- 49 · WEEKLY PLAN -->
<section data-label="49 Weekly Plan" class="slide">
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
  {foot(49)}
</section>""")

# 50 END
slides.append("""<!-- 50 · END -->
<section data-label="50 End" class="slide end-slide">
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

# verify 50 sections
import re
sec = len(re.findall(r"<section\b", out))
print(path, "bytes", len(out), "sections", sec)
