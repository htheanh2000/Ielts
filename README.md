# Ielts

Slide-deck bài giảng IELTS 1-1. Static site deployed to VPS (nginx + Traefik).

- **Live:** https://ielts.huynhtheanh.com
- **URL pattern:** `/<skill>/lesson/<n>/` (ví dụ `/reading/lesson/1/`, `/writing/lesson/2/`)
- **Landing:** danh sách toàn bộ lessons

## Cấu trúc

```
/
├── index.html                    # Landing — danh sách lessons
├── assets/
│   ├── deck-stage.js             # Web component <deck-stage> shared bởi mọi deck
│   └── deck-styles.css           # Design tokens + component styles
├── reading/lesson/1/
│   ├── index.html                # Skimming & Scanning — full deck
│   └── no-answers/index.html     # Variant không đáp án P3, P4
├── writing/lesson/2/
│   └── index.html                # Writing Task 1 Academic — Charts & Trends
├── deploy/
│   ├── nginx.conf                # Nginx server config (pretty URLs, cache headers)
│   └── traefik-ielts.yml         # Traefik dynamic config — Host routing + Let's Encrypt
├── docker-compose.yml            # nginx:alpine + proxy network
└── .github/workflows/deploy.yml  # GH Actions → SSH VPS → git pull + docker compose up
```

## Deploy pipeline

Push to `main` triggers GitHub Actions workflow (`appleboy/ssh-action`):

1. SSH to VPS (31.97.109.177) using `ielts_deploy` ed25519 key (secret `VPS_SSH_KEY`)
2. `cd /srv/ielts && git pull`
3. Copy Traefik dynamic config to `/srv/traefik/data/dynamic/ielts.yml` (idempotent)
4. `docker compose up -d` — nginx picks up volume-mounted files immediately; force-recreate only if `docker-compose.yml` hoặc `nginx.conf` thay đổi
5. Smoke test: curl `/`, `/reading/lesson/1/`, `/writing/lesson/2/` — expect 200

## Infra links

- VPS: Hostinger 31.97.109.177 · `/srv/ielts/` git-clone · shared `proxy` Docker network
- Traefik: SSL auto via Let's Encrypt (HTTP-01 challenge), file provider at `/srv/traefik/data/dynamic/`
- DNS: wildcard `*.huynhtheanh.com → VPS` catch-all (không cần CNAME riêng)

## Thêm lesson mới

1. Copy một deck hiện có làm template
2. Đặt vào folder `<skill>/lesson/<n>/index.html`
3. Reference assets bằng absolute path `/assets/deck-stage.js` và `/assets/deck-styles.css`
4. Cập nhật `index.html` (landing) để list lesson mới
5. `git push origin main` → GH Actions auto-deploy

## Điều hướng deck

- `← →` / `PgUp` `PgDn` / `Space` — chuyển slide
- `Home` `End` — slide đầu / cuối
- Số `1`-`9`, `0` — nhảy tới slide theo số
- `R` — reset về slide 1
- `Cmd+P` — xuất PDF (1 slide = 1 page 1920×1080)

## Design DNA

Editorial-print aesthetic, 1920×1080 canvas, zero motion. Design tokens trong `assets/deck-styles.css`; full profile extract sang `design-dna.json` (local, không commit).
