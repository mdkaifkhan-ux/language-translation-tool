from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

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
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Google Translate API key is not configured. "
            "Set the GOOGLE_TRANSLATE_API_KEY environment variable."
        )

    params = {"key": api_key}
    data = {
        "q": text,
        "target": target,
        "format": "text"
    }

    # For automatic source-language detection, Google can omit "source".
    if source and source != "auto":
        data["source"] = source

    response = requests.post(
        GOOGLE_TRANSLATE_URL,
        params=params,
        json=data,
        timeout=20
    )

    if not response.ok:
        try:
            error = response.json()["error"]["message"]
        except Exception:
            error = response.text or "Translation API request failed."
        raise RuntimeError(error)

    result = response.json()
    return result["data"]["translations"][0]["translatedText"]


@app.route("/")
def home():
    return render_template(
        "index.html",
        languages=LANGUAGES
    )


@app.post("/translate")
def translate():
    data = request.get_json(silent=True) or {}

    text = (data.get("text") or "").strip()
    source = data.get("source", "auto")
    target = data.get("target", "hi")

    if not text:
        return jsonify({"error": "Please enter some text."}), 400

    if target not in LANGUAGES.values():
        return jsonify({"error": "Invalid target language."}), 400

    try:
        translated = translate_text(text, source, target)
        return jsonify({"translation": translated})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
