// IELTS Pronunciation Scoring Worker
// Proxies browser audio uploads to Speechace API, hiding the API key.
//
// Endpoint: POST /score
//   multipart form fields:
//     audio: WAV/MP3/WEBM/OGG file (recorded via MediaRecorder)
//     text:  reference text the student is supposed to read
//     dialect: optional, "en-gb" (default) or "en-us"
//
// Returns: Speechace JSON (text_score, word_score_list, etc.)
//
// Environment:
//   SPEECHACE_API_KEY  (secret) — set with: wrangler secret put SPEECHACE_API_KEY
//   ALLOWED_ORIGIN     (var)    — production site origin, e.g. https://ielts.huynhtheanh.com

const SPEECHACE_ENDPOINT = "https://api.speechace.co/api/scoring/text/v9/json/";

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

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(env, origin) });
    }

    const url = new URL(request.url);

    if (url.pathname === "/" || url.pathname === "/health") {
      return jsonResponse({ ok: true, service: "ielts-pronunciation" }, 200, env, origin);
    }

    if (url.pathname !== "/score") {
      return jsonResponse({ error: "not_found" }, 404, env, origin);
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "method_not_allowed" }, 405, env, origin);
    }

    if (!env.SPEECHACE_API_KEY) {
      return jsonResponse({ error: "missing_api_key", hint: "wrangler secret put SPEECHACE_API_KEY" }, 500, env, origin);
    }

    let formData;
    try {
      formData = await request.formData();
    } catch (e) {
      return jsonResponse({ error: "invalid_form_data", detail: e.message }, 400, env, origin);
    }

    const audio = formData.get("audio");
    const text = formData.get("text");
    const dialect = (formData.get("dialect") || "en-gb").toString();

    if (!audio || !text) {
      return jsonResponse({ error: "missing_fields", required: ["audio", "text"] }, 400, env, origin);
    }

    // Forward to Speechace
    const speechaceForm = new FormData();
    speechaceForm.append("text", text.toString());
    speechaceForm.append("user_audio_file", audio, "speech.webm");
    speechaceForm.append("dialect", dialect);
    speechaceForm.append("user_id", "anon-" + crypto.randomUUID());
    // Optionally request additional response details
    speechaceForm.append("include_ielts_subscore", "1");
    speechaceForm.append("include_intonation", "1");

    const speechaceUrl = `${SPEECHACE_ENDPOINT}?key=${encodeURIComponent(env.SPEECHACE_API_KEY)}`;

    let upstream;
    try {
      upstream = await fetch(speechaceUrl, { method: "POST", body: speechaceForm });
    } catch (e) {
      return jsonResponse({ error: "upstream_fetch_failed", detail: e.message }, 502, env, origin);
    }

    let payload;
    try {
      payload = await upstream.json();
    } catch (e) {
      const txt = await upstream.text().catch(() => "");
      return jsonResponse({ error: "upstream_invalid_json", status: upstream.status, body: txt.slice(0, 500) }, 502, env, origin);
    }

    return jsonResponse(payload, upstream.status, env, origin);
  },
};
