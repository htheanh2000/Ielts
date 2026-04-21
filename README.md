# Ielts

Slide-deck bài giảng IELTS 1-1. Static site deploy qua GitHub Pages.

- Live: https://ielts.huynhtheanh.com
- Landing: danh sách toàn bộ lessons
- URL pattern: `/<skill>/lesson/<n>/` (ví dụ `/reading/lesson/1/`, `/writing/lesson/2/`)

## Cấu trúc

```
/
├── CNAME                         # ielts.huynhtheanh.com
├── index.html                    # Landing page — danh sách lessons
├── assets/
│   ├── deck-stage.js             # Web component <deck-stage> shared by all decks
│   └── deck-styles.css           # Design tokens + component styles (see design-dna.json)
├── reading/lesson/1/
│   ├── index.html                # Skimming & Scanning — full deck
│   └── no-answers/index.html     # Variant không đáp án P3, P4 để học viên tự luyện
└── writing/lesson/2/
    └── index.html                # Writing Task 1 Academic — Charts & Trends
```

## Design DNA

Mọi deck tuân theo design system 1920×1080, editorial-print aesthetic, zero-motion. Tokens nằm trong `assets/deck-styles.css`; pattern chi tiết extract sang `design-dna.json` (không commit — local reference).

## Thêm lesson mới

1. Copy một lesson hiện có làm template
2. Đặt vào folder `<skill>/lesson/<n>/index.html`
3. Reference assets bằng absolute path `/assets/deck-stage.js` và `/assets/deck-styles.css`
4. Cập nhật `index.html` (landing) để list lesson mới
5. Commit + push → GitHub Pages auto-deploy

## Điều hướng deck

- `← →` / `PgUp` `PgDn` / `Space` — chuyển slide
- `Home` `End` — slide đầu / cuối
- Số `1`-`9`, `0` — nhảy tới slide theo số
- `R` — reset về slide 1
- `Cmd+P` — xuất PDF (1 slide = 1 page 1920×1080)
