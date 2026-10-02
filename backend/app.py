from flask import Flask, request, jsonify
from flask_cors import CORS

from analyzer import analyze_password


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "PasswordGuard API is running",
        "status": "healthy"
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not data or "password" not in data:
        return jsonify({
            "error": "Password field is required."
        }), 400

    password = data["password"]

    if not isinstance(password, str):
        return jsonify({
            "error": "Password must be a string."
        }), 400

    result = analyze_password(password)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)