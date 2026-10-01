import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
def health():
    return "HAL backend is running!"


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
