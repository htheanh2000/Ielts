# Ielts

Slide-deck bài giảng IELTS 1-1. Static site deploy lên **Cloudflare Pages** (project `ielts`).

- **Live:** https://ielts.huynhtheanh.com
- **URL pattern:** `/<skill>/lesson/<n>/` (ví dụ `/reading/lesson/1/`, `/writing/lesson/2/`)
- **Landing:** `index.html` — danh sách toàn bộ lessons

> **Lịch sử hạ tầng:** GH Pages → VPS nginx+Traefik → **Cloudflare Pages** (migrate 2026-05-12 sau khi VPS Hostinger shutdown). Mọi tham chiếu VPS/nginx/Traefik/SSH đã ngừng dùng, chỉ còn trong git history.

## Cấu trúc

```
/
├── index.html                      # Landing — danh sách lessons
├── assets/
│   ├── deck-stage.js               # Web component <deck-stage> shared bởi mọi deck
│   ├── deck-styles.css             # Design tokens + component styles
│   └── images/                     # Ảnh trong deck (process diagrams, v.v.)
├── reading/lesson/<n>/
│   ├── index.html                  # Reading deck
│   └── no-answers/index.html       # Variant không đáp án (vài lesson)
├── writing/lesson/<n>/index.html   # Writing decks (Task 1 & Task 2)
├── listening/lesson/<n>/           # Listening decks
├── speaking/                       # Speaking lessons + topic cards
├── cloudflare-worker/              # Worker riêng — pronunciation scoring (TEACH-8)
├── scripts/
│   ├── build-static.sh             # rsync repo → dist/ (loại file non-static)
│   └── gen_*.py                    # Generator cho listening/speaking decks
└── .github/workflows/deploy.yml    # GH Actions → wrangler-action → CF Pages
```

## Deploy

Cả hai cách đều deploy lên CF Pages project `ielts` (custom domain `ielts.huynhtheanh.com` đã bind sẵn, propagate ~15–25s sau deploy).

### 1. Manual từ local — đường tin cậy nhất

```bash
bash scripts/build-static.sh
npx --yes wrangler@latest pages deploy dist \
  --project-name=ielts --branch=main --commit-dirty=true
```

CF Pages **không** bật git integration, nên `git push` một mình không deploy — phải chạy wrangler. Trên máy đã có Wrangler auth/CF env sẵn nên cách này luôn chạy.

### 2. CI khi push `main`

`.github/workflows/deploy.yml` build `dist/` rồi `cloudflare/wrangler-action@v3` deploy + smoke-test 4 URL.

**Yêu cầu repo secrets** (Settings → Secrets and variables → Actions):

| Secret | Lấy ở đâu |
|--------|-----------|
| `CLOUDFLARE_API_TOKEN` | CF Dashboard → My Profile → API Tokens (template "Edit Cloudflare Workers" hoặc scope Pages:Edit) |
| `CLOUDFLARE_ACCOUNT_ID` | CF Dashboard → account ID (`6c6182ba…`) |

> Thiếu/expired token → step deploy fail với `necessary to set a CLOUDFLARE_API_TOKEN`. Khi chưa set, dùng cách 1.

## Thêm lesson mới

1. Copy một deck hiện có làm template, đặt vào `<skill>/lesson/<n>/index.html`
2. Reference assets bằng absolute path: `/assets/deck-stage.js`, `/assets/deck-styles.css`
3. Cập nhật `index.html` (landing) để list lesson mới
4. Deploy (cách 1, hoặc push `main` nếu secrets CF đã set)

> **Gotcha `<deck-stage>`:** web component đếm *mọi* element trong slot là một slide (trừ `<template>/<script>/<style>`). Đặt mọi shared resource (SVG `<defs>`, hidden markup…) **NGOÀI** `<deck-stage>` — đặt bên trong sẽ tạo blank slide #1. Marker tham chiếu by ID vẫn hoạt động toàn document.

## Điều hướng deck

- `← →` / `PgUp` `PgDn` / `Space` — chuyển slide
- `Home` `End` — slide đầu / cuối
- Số `1`–`9`, `0` — nhảy tới slide theo số
- `R` — reset về slide 1
- `Cmd+P` — xuất PDF (1 slide = 1 page 1920×1080)

## Design DNA

Editorial-print aesthetic, 1920×1080 canvas, zero motion, accent đỏ `#C8202F` trên nền paper. Roboto Slab + Roboto + Roboto Mono. Design tokens trong `assets/deck-styles.css`; full profile extract sang `design-dna.json` (local, không commit).
