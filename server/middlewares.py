import asyncio
import json
from okta_jwt_verifier import AccessTokenVerifier
from flask import request, jsonify


def load_okta_config(fname="./client_secrets.json"):
    config = None
    with open(fname) as f:
        config = json.load(f)
    return config


okta_config = load_okta_config()
loop = asyncio.get_event_loop()
jwt_verifier = AccessTokenVerifier(
    issuer=f"https://{okta_config['okta_domain']}/oauth2/default",
    audience="api://default",
)
PUBLIC_ROUTES = []


def is_access_token_valid(token):
    try:
        loop.run_until_complete(jwt_verifier.verify(token))
        return True
    except Exception:
        return False


def check_authorization(app):
    """Middleware to check authorization before each request."""

    @app.before_request
    def require_auth():
        try:
            if request.path in PUBLIC_ROUTES or request.method.lower() == "options":
                return None

            auth_header = request.headers.get("Authorization", None)

            if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401

            try:
                token = auth_header.split("Bearer ")[1]
            except IndexError:
                return jsonify({"error": "Invalid Authorization header format"}), 401

            # Validate the token
            if not is_access_token_valid(token):
                return jsonify({"error": "Unauthorized access"}), 401

            return None

        except Exception:
            return jsonify({"error": "Unauthorized access"}), 500


# TODO
class LoggingMiddleware:
    # Logs api request:
    # time of request
    # parameters
    # endpoint

    pass
