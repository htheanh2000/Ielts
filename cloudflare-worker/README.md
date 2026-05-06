# IELTS Pronunciation Worker

Cloudflare Worker that proxies browser audio recordings to the [Speechace](https://www.speechace.com/) pronunciation scoring API. Hides the Speechace API key from the browser and adds CORS headers for the deck site.

## One-time setup

### 1. Get a Speechace API key

- Sign up at <https://www.speechace.com/> (free tier: 200 scoring calls / month)
- Account dashboard → API Keys → copy the key

### 2. Deploy the worker

```bash
cd cloudflare-worker
wrangler login                                        # browser opens, login to Cloudflare
echo "<your-speechace-key>" | wrangler secret put SPEECHACE_API_KEY
wrangler deploy
```

After deploy you'll see a URL like `https://ielts-pronunciation.<your-subdomain>.workers.dev`.

### 3. Wire the worker URL into the deck

Edit `scripts/gen_speaking_topics.py`, find:

```python
WORKER_URL = "https://ielts-pronunciation.<your-subdomain>.workers.dev/score"
```

Set it to your actual worker URL. Then regenerate decks:

```bash
python3 scripts/gen_speaking_topics.py
git add -A && git commit -m "config: pronunciation worker URL"
git push origin main
```

## API

`POST /score`

Multipart form fields:

- `audio`  — WAV / MP3 / WEBM / OGG file (recorded via MediaRecorder in browser)
- `text`   — reference sentence the student was reading
- `dialect` — optional, `en-gb` (default) or `en-us`

Returns Speechace's JSON response unchanged. Key fields used by the deck UI:

- `text_score.ielts_score.pronunciation`  (band 0–9)
- `text_score.word_score_list[].word`
- `text_score.word_score_list[].quality_score`  (0–100)

## CORS

Origin allow-listed via `ALLOWED_ORIGIN` in `wrangler.toml` (default `https://ielts.huynhtheanh.com`). To add localhost or another domain, edit `corsHeaders()` in `src/index.js`.

## Local testing

```bash
wrangler dev
# Worker runs at http://localhost:8787
# Test:
curl -F text="Hello world" -F audio=@/tmp/test.wav http://localhost:8787/score
```
