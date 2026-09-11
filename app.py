from flask import Flask, render_template, request, jsonify
import requests
from urllib.parse import quote

app = Flask(__name__)

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
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

LINGVA_URL = "https://lingva.ml/api/v1"


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

    if len(text) > 4000:
        return jsonify({"error": "Please keep text under 4000 characters."}), 400

    try:
        encoded_text = quote(text, safe="")
        url = f"{LINGVA_URL}/{source}/{target}/{encoded_text}"

        response = requests.get(url, timeout=20)

        if not response.ok:
            return jsonify({
                "error": f"Translation service returned HTTP {response.status_code}."
            }), 502

        result = response.json()
        translated = result.get("translation")

        if not translated:
            return jsonify({"error": "No translation was returned."}), 502

        return jsonify({"translation": translated})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
