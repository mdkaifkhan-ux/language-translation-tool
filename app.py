from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# MyMemory is used instead of Google Cloud Translation so this demo
# does not require a Google Cloud billing account or API key.
MYMEMORY_URL = "https://api.mymemory.translated.net/get"

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa"
}


def translate_text(text, source, target):
    # MyMemory's public REST endpoint requires a language pair.
    # For "Auto Detect", use English as a simple demo fallback.
    if source == "auto":
        source = "en"

    params = {
        "q": text,
        "langpair": f"{source}|{target}",
        "mt": "1"
    }

    response = requests.get(MYMEMORY_URL, params=params, timeout=20)

    if not response.ok:
        raise RuntimeError(f"Translation service returned HTTP {response.status_code}.")

    data = response.json()

    if data.get("responseStatus") not in (200, "200"):
        raise RuntimeError(data.get("responseDetails") or "Translation failed.")

    translated = data.get("responseData", {}).get("translatedText")

    if not translated:
        raise RuntimeError("No translation was returned.")

    return translated


@app.route("/")
def home():
    return render_template("index.html", languages=LANGUAGES)


@app.post("/translate")
def translate():
    data = request.get_json(silent=True) or {}

    text = (data.get("text") or "").strip()
    source = data.get("source", "auto")
    target = data.get("target", "hi")

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    if len(text.encode("utf-8")) > 500:
        return jsonify({
            "error": "For this free demo, please keep the text under 500 bytes."
        }), 400

    if target not in LANGUAGES.values():
        return jsonify({"error": "Invalid target language."}), 400

    if source != "auto" and source not in LANGUAGES.values():
        return jsonify({"error": "Invalid source language."}), 400

    try:
        translated = translate_text(text, source, target)
        return jsonify({"translation": translated})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
