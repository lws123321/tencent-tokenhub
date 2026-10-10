import binascii
import json
from collections.abc import Generator

import requests

from dify_plugin.errors.model import (
    CredentialsValidateFailedError,
    InvokeBadRequestError,
    InvokeConnectionError,
)
from dify_plugin.interfaces.model.tts_model import TTSModel


TOKENHUB_DEFAULT_BASE_URL = "https://tokenhub.tencentmaas.com/v1"


class TokenHubTTSModel(TTSModel):
    """TokenHub MiniMax Speech synchronous TTS implementation."""

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
        return f"{base_url.rstrip('/')}/wand/minimax-tts/sync_tts"

    def _invoke(
        self,
        model: str,
        tenant_id: str,
        credentials: dict,
        content_text: str,
        voice: str,
        user: str | None = None,
    ) -> Generator[bytes, None, None]:
        del tenant_id, user
        payload = {
            "model": model,
            "text": content_text,
            "voice_setting": {"voice_id": voice, "speed": 1, "vol": 1, "pitch": 0},
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1,
            },
            "output_format": "hex",
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
        base_resp = response_data.get("base_resp", {})
        if base_resp.get("status_code", 0) != 0:
            raise InvokeBadRequestError(base_resp.get("status_msg", "TokenHub TTS failed"))
        audio = response_data.get("data", {}).get("audio", "")
        try:
            if audio.startswith(("http://", "https://")):
                audio_response = requests.get(audio, timeout=(10, 300))
                audio_response.raise_for_status()
                audio_bytes = audio_response.content
            else:
                audio_bytes = binascii.unhexlify(audio)
        except (binascii.Error, requests.RequestException) as error:
            raise InvokeBadRequestError(f"Invalid TokenHub TTS audio response: {error}") from error
        yield audio_bytes