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

const QUESTIONS = __QUESTIONS_JSON__;

const slides = [];
QUESTIONS.forEach((item, qi) => {
  for (let lvl = 0; lvl <= 4; lvl++) {
    slides.push({ qIndex: qi, level: lvl });
  }
});

let cursor = 0;

function renderAnswer(raw, level) {
  if (level === 4) return null;
  let out = raw;
  out = out.replace(/~~(.*?)~~/g, (_, txt) => level >= 2 ? wrapBlank(txt) : txt);
  out = out.replace(/==(.*?)==/g, (_, txt) => level >= 3 ? wrapBlank(txt) : txt);
  return out;
}

function wrapBlank(txt) {
  const words = txt.split(/(\s+)/);
  return words.map(w => {
    if (/^\s+$/.test(w)) return w;
    if (!w) return w;
    const m = w.match(/^([^\w]*)([\w'-]+)([^\w]*)$/);
    const NBSP = ' ';
    if (m) {
      return m[1] + `<span class="blank">${NBSP.repeat(Math.max(3, m[2].length))}</span>` + m[3];
    }
    return `<span class="blank">${NBSP.repeat(Math.max(3, w.length))}</span>`;
  }).join('');
}

function render() {
  const slide = slides[cursor];
  const item = QUESTIONS[slide.qIndex];
  const card = document.getElementById('card');
  document.getElementById('counter').textContent = `${cursor + 1} / ${slides.length}`;
  document.getElementById('topic-name').textContent = `Topic ${TOPIC_NUM} · ${TOPIC} · Q${slide.qIndex + 1}`;

  let html = '';

  if (slide.level === 0) {
    html = `
      <div class="level-indicator">Question</div>
      <span class="label q">Question ${slide.qIndex + 1}</span>
      <div class="question">${item.q}</div>
    `;
  } else if (slide.level === 4) {
    html = `
      <div class="level-indicator">Recall · Level 4</div>
      <span class="label empty">Answer</span>
      <div class="answer hidden-all">— hãy tự nói câu trả lời —</div>
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
