"""
Client-credentials authentication for calls to the Copilot API server.

The chat and streamlit backends call the API server (API_BASE_URL) from
server-side code. The API has Entra ID Easy Auth enabled (unauthenticated
requests get 401), so every outgoing request must carry a Bearer token.

Configuration (all optional; if any of the first three is missing, requests
are sent WITHOUT an Authorization header, matching the pre-auth behavior):

    API_AUTH_TENANT_ID     Entra tenant id
    API_AUTH_CLIENT_ID     app registration id of the backend client
                           (copilot-backends in the tenant)
    API_AUTH_CLIENT_SECRET client secret (Key Vault reference in App Service,
                           ACA secret store for the streamlit app)
    API_AUTH_SCOPE         token scope, default api://<API app id>/.default
"""
import os
import time
import logging
import threading

import requests

TENANT = os.getenv("API_AUTH_TENANT_ID", "")
CLIENT_ID = os.getenv("API_AUTH_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("API_AUTH_CLIENT_SECRET", "")
SCOPE = os.getenv("API_AUTH_SCOPE", "")

_token_cache = {"token": None, "expires_at": 0.0}
_lock = threading.Lock()


def _fetch_token():
    response = requests.post(
        f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": SCOPE,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    # refresh 5 minutes before actual expiry
    return payload["access_token"], time.time() + payload.get("expires_in", 3600) - 300


def _get_token():
    if not (TENANT and CLIENT_ID and CLIENT_SECRET and SCOPE):
        return None
    with _lock:
        if _token_cache["token"] and time.time() < _token_cache["expires_at"]:
            return _token_cache["token"]
        try:
            token, expires_at = _fetch_token()
        except Exception as e:
            logging.error(f"api_auth: token fetch failed: {e}")
            # serve a stale token if we have one rather than failing outright
            if _token_cache["token"]:
                return _token_cache["token"]
            raise
        _token_cache["token"] = token
        _token_cache["expires_at"] = expires_at
        return token


class APIAuthSession(requests.Session):
    """requests.Session that injects a Bearer token into every request."""

    def request(self, method, url, **kwargs):
        token = _get_token()
        if token:
            headers = kwargs.setdefault("headers", {})
            headers["Authorization"] = f"Bearer {token}"
        return super().request(method, url, **kwargs)


def get_api_token():
    """Public accessor for the client-credentials token (or None when
    unconfigured). Use this for non-requests HTTP clients (e.g. httpx)."""
    return _get_token()


session = APIAuthSession()
