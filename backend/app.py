from flask import Flask, request, jsonify
from flask_cors import CORS

from analyzer import analyze_password
from services.password_generator import generate_secure_password


app = Flask(__name__)

# Allow the frontend to communicate with the API.
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "PasswordGuard API",
        "status": "healthy",
        "version": "2.0"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Analyze a password in memory.

    The password is never written to a database,
    file, URL, or application log.
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    if "password" not in data:
        return jsonify({
            "error": "Password field is required."
        }), 400

    password = data["password"]

    if not isinstance(password, str):
        return jsonify({
            "error": "Password must be a string."
        }), 400

    if len(password) > 128:
        return jsonify({
            "error": "Password must not exceed 128 characters."
        }), 400

    # Optional personal context.
    # This is processed only in memory.
    context = data.get("context")

    if context is not None and not isinstance(context, dict):
        return jsonify({
            "error": "Context must be a JSON object."
        }), 400

    try:
        result = analyze_password(
            password,
            context=context
        )

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        # Do not expose internal errors or password data.
        return jsonify({
            "error": "Unable to analyze the password."
        }), 500


@app.route("/api/generate-password", methods=["POST"])
def generate_password():
    """
    Generate a cryptographically secure password.

    Uses Python's secrets module.
    Generated passwords are returned only in the response
    and are not stored by the application.
    """

    data = request.get_json(silent=True) or {}

    length = data.get("length", 20)

    if not isinstance(length, int) or isinstance(length, bool):
        return jsonify({
            "error": "Length must be an integer."
        }), 400

    if length < 12 or length > 128:
        return jsonify({
            "error": "Length must be between 12 and 128."
        }), 400

    use_uppercase = data.get("uppercase", True)
    use_lowercase = data.get("lowercase", True)
    use_numbers = data.get("numbers", True)
    use_symbols = data.get("symbols", True)

    if not all(
        isinstance(value, bool)
        for value in [
            use_uppercase,
            use_lowercase,
            use_numbers,
            use_symbols
        ]
    ):
        return jsonify({
            "error": "Character options must be boolean values."
        }), 400

    if not any([
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols
    ]):
        return jsonify({
            "error": "At least one character type must be enabled."
        }), 400

    try:
        password = generate_secure_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols
        )

        return jsonify({
            "password": password,
            "length": len(password),
            "stored": False
        }), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        return jsonify({
            "error": "Unable to generate password."
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "error": "HTTP method not allowed."
    }), 405


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )