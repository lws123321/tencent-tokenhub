import base64
import json
from typing import IO

import requests

from dify_plugin.errors.model import (
    CredentialsValidateFailedError,
    InvokeBadRequestError,
    InvokeConnectionError,
)
from dify_plugin.interfaces.model.speech2text_model import Speech2TextModel


TOKENHUB_DEFAULT_BASE_URL = "https://tokenhub.tencentmaas.com/v1"


class TokenHubSpeech2TextModel(Speech2TextModel):
    """TokenHub synchronous WAND/Hy ASR implementation."""

    def validate_credentials(self, model: str, credentials: dict) -> None:
        del model
        if not credentials.get("api_key"):
            raise CredentialsValidateFailedError("TokenHub API Key is required")

    @property
    def _invoke_error_mapping(self) -> dict:
        return {
            InvokeBadRequestError: [InvokeBadRequestError, requests.HTTPError],
            InvokeConnectionError: [requests.ConnectionError, requests.Timeout],
        }

    def _endpoint(self, credentials: dict) -> str:
        base_url = credentials.get("api_base", "").strip() or TOKENHUB_DEFAULT_BASE_URL
        return f"{base_url.rstrip('/')}/wand/asrproxy/sync_transcribe"

    def _invoke(
        self,
        model: str,
        credentials: dict,
        file: IO[bytes],
        user: str | None = None,
    ) -> str:
        del user
        payload = {
            "model": model,
            "data": base64.b64encode(file.read()).decode("ascii"),
        }
        headers = {"Content-Type": "application/json"}
        if api_key := credentials.get("api_key"):
            headers["Authorization"] = f"Bearer {api_key}"
        response = requests.post(
            self._endpoint(credentials),
            headers=headers,
            data=json.dumps(payload),
            timeout=(10, 300),
        )
        if response.status_code != 200:
            raise InvokeBadRequestError(response.text)
        response_data = response.json()
        return response_data.get("output", {}).get("text", "")