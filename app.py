from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def translate_text(text, source, target):
    params = {
        "client": "gtx",
        "sl": source if source != "auto" else "auto",
        "tl": target,
        "dt": "t",
        "q": text
    }

    response = requests.get(
        GOOGLE_TRANSLATE_URL,
        params=params,
        timeout=20
    )

    if not response.ok:
        raise RuntimeError(
            f"Translation service returned HTTP {response.status_code}."
        )

    data = response.json()

    if not data or not data[0]:
        raise RuntimeError("No translation was returned.")

    translated = "".join(
        part[0] for part in data[0] if part and part[0]
    )

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

    if len(text) > 5000:
        return jsonify({
            "error": "Please keep the text under 5000 characters."
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
