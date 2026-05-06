// IELTS Pronunciation Scoring Worker (Azure Speech)
// Proxies browser audio uploads to Azure Speech Pronunciation Assessment API.
// Hides the Azure subscription key from the browser and adds CORS headers.
//
// Endpoint: POST /score
//   multipart form fields:
//     audio:    WAV PCM 16-bit mono (browser-side conversion done by deck JS)
//     text:     reference text the student is supposed to read
//     language: optional, "en-GB" (default) or "en-US"
//
// Returns: Azure JSON (DisplayText, NBest[].PronunciationAssessment, NBest[].Words)
//
// Environment:
//   AZURE_SPEECH_KEY  (secret) — set with: wrangler secret put AZURE_SPEECH_KEY
//   AZURE_REGION      (var)    — Azure resource region, e.g. southeastasia, eastus
//   ALLOWED_ORIGIN    (var)    — production site origin

const AZURE_PATH = "/speech/recognition/conversation/cognitiveservices/v1";

function corsHeaders(env, origin) {
  const allow = origin === env.ALLOWED_ORIGIN || origin === "http://localhost:8000" || origin === "null";
  return {
    "Access-Control-Allow-Origin": allow ? (origin || env.ALLOWED_ORIGIN) : env.ALLOWED_ORIGIN,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function jsonResponse(body, status, env, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders(env, origin) },
  });
}

// Base64 encode a JSON string with UTF-8 awareness (btoa alone breaks on non-ASCII)
function b64encodeJson(obj) {
  const bytes = new TextEncoder().encode(JSON.stringify(obj));
  let binary = "";
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(env, origin) });
    }

    const url = new URL(request.url);

    if (url.pathname === "/" || url.pathname === "/health") {
      return jsonResponse(
        { ok: true, service: "ielts-pronunciation-azure", region: env.AZURE_REGION || null },
        200, env, origin
      );
    }

    if (url.pathname !== "/score") {
      return jsonResponse({ error: "not_found" }, 404, env, origin);
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "method_not_allowed" }, 405, env, origin);
    }

    if (!env.AZURE_SPEECH_KEY) {
      return jsonResponse(
        { error: "missing_api_key", hint: "wrangler secret put AZURE_SPEECH_KEY" },
        500, env, origin
      );
    }
    if (!env.AZURE_REGION) {
      return jsonResponse({ error: "missing_region", hint: "set AZURE_REGION in wrangler.toml" }, 500, env, origin);
    }

    let formData;
    try {
      formData = await request.formData();
    } catch (e) {
      return jsonResponse({ error: "invalid_form_data", detail: e.message }, 400, env, origin);
    }

    const audio = formData.get("audio");
    const text = formData.get("text");
    const language = (formData.get("language") || "en-GB").toString();

    if (!audio || !text) {
      return jsonResponse({ error: "missing_fields", required: ["audio", "text"] }, 400, env, origin);
    }

    const azureUrl =
      `https://${env.AZURE_REGION}.stt.speech.microsoft.com${AZURE_PATH}?language=${encodeURIComponent(language)}&format=detailed`;

    const paConfig = {
      ReferenceText: text.toString(),
      GradingSystem: "HundredMark",
      Granularity: "Phoneme",
      Dimension: "Comprehensive",
      EnableMiscue: "True",
    };
    const paHeader = b64encodeJson(paConfig);

    let audioBuffer;
    try {
      audioBuffer = await audio.arrayBuffer();
    } catch (e) {
      return jsonResponse({ error: "audio_read_failed", detail: e.message }, 400, env, origin);
    }

    let upstream;
    try {
      upstream = await fetch(azureUrl, {
        method: "POST",
        headers: {
          "Ocp-Apim-Subscription-Key": env.AZURE_SPEECH_KEY,
          "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
          "Pronunciation-Assessment": paHeader,
          Accept: "application/json",
        },
        body: audioBuffer,
      });
    } catch (e) {
      return jsonResponse({ error: "upstream_fetch_failed", detail: e.message }, 502, env, origin);
    }

    let payload;
    const ct = upstream.headers.get("Content-Type") || "";
    if (ct.includes("application/json")) {
      payload = await upstream.json().catch(() => null);
    } else {
      const txt = await upstream.text().catch(() => "");
      payload = { error: "upstream_non_json", status: upstream.status, body: txt.slice(0, 500) };
    }

    return jsonResponse(payload || { error: "empty_response" }, upstream.status, env, origin);
  },
};
