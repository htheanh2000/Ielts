# IELTS Pronunciation Worker (Azure Speech)

Cloudflare Worker that proxies browser audio recordings to Azure Speech [Pronunciation Assessment](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment). Hides the Azure subscription key from the browser and adds CORS headers for the deck site.

## Free tier

Azure Speech **F0** SKU = **5 hours of audio / month free**, no card charge. Each Recall slide is ~10–15 seconds, so you get roughly **1500 free assessments / month**.

## One-time setup

### 1. Get an Azure Speech subscription key

1. Sign up / sign in at <https://portal.azure.com>
2. **Create resource** → search "Speech" → **Speech (Microsoft)** → Create
3. Pick a **region** close to you (Vietnam → `Southeast Asia`)
4. **Pricing tier** → `Free F0` (5h/month free)
5. Once deployed, open the resource → **Keys and Endpoint** → copy `KEY 1`

### 2. Deploy the worker

```bash
cd cloudflare-worker
wrangler login                                      # browser opens, login to Cloudflare
echo "<your-azure-key>" | wrangler secret put AZURE_SPEECH_KEY
# If your Azure region differs, edit AZURE_REGION in wrangler.toml first
wrangler deploy
```

After deploy you'll see a URL like `https://ielts-pronunciation.<your-subdomain>.workers.dev`.

Verify it's alive:

```bash
curl https://ielts-pronunciation.<subdomain>.workers.dev/health
# {"ok":true,"service":"ielts-pronunciation-azure","region":"southeastasia"}
```

### 3. Wire the worker URL into the deck

Edit `scripts/gen_speaking_topics.py`, find:

```python
const PRONUNCIATION_WORKER_URL = "";
```

Set it to your worker URL:

```python
const PRONUNCIATION_WORKER_URL = "https://ielts-pronunciation.<subdomain>.workers.dev/score";
```

Regenerate decks and push:

```bash
python3 scripts/gen_speaking_topics.py
git add -A && git commit -m "config: pronunciation worker URL"
git push origin main
```

## API

`POST /score`

Multipart form fields:

- `audio`    — **WAV PCM 16-bit mono 16kHz**. The deck JS converts MediaRecorder output to this format client-side via `OfflineAudioContext`.
- `text`     — reference sentence the student was reading (the unmarked answer text)
- `language` — optional, `en-GB` (default) or `en-US`

Returns Azure's JSON unchanged. Key fields used by the deck UI:

```
data.NBest[0].PronunciationAssessment.PronScore        // 0–100 overall
data.NBest[0].PronunciationAssessment.AccuracyScore    // 0–100
data.NBest[0].PronunciationAssessment.FluencyScore     // 0–100
data.NBest[0].PronunciationAssessment.CompletenessScore // 0–100
data.NBest[0].Words[].Word
data.NBest[0].Words[].PronunciationAssessment.AccuracyScore
data.NBest[0].Words[].PronunciationAssessment.ErrorType  // None | Mispronunciation | Omission | Insertion | UnexpectedBreak | MissingBreak
```

## Region matters

The worker URL embeds the Azure region. If you create your Speech resource in `eastus` but leave `AZURE_REGION = "southeastasia"` in `wrangler.toml`, every request will 401. Match them.

## CORS

Origin allow-listed via `ALLOWED_ORIGIN` in `wrangler.toml` (default `https://ielts.huynhtheanh.com`). To add localhost or another domain, edit `corsHeaders()` in `src/index.js`.

## Local testing

```bash
wrangler dev   # http://localhost:8787

# Test with a local WAV file
curl -F text="Hello world" -F audio=@/tmp/test.wav http://localhost:8787/score
```
