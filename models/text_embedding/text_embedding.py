import json
import time

import requests

from dify_plugin.entities.model import EmbeddingInputType
from dify_plugin.entities.model.text_embedding import (
    MultiModalContent,
    MultiModalContentType,
    MultiModalEmbeddingResult,
    TextEmbeddingResult,
)
from dify_plugin.interfaces.model.openai_compatible.text_embedding import (
    OAICompatEmbeddingModel,
)


TOKENHUB_DEFAULT_BASE_URL = "https://tokenhub.tencentmaas.com/v1"


class TokenHubEmbeddingModel(OAICompatEmbeddingModel):
    """TokenHub text and multimodal embedding model implementation."""

    def _endpoint(self, credentials: dict, path: str) -> str:
        base_url = credentials.get("api_base", "").strip() or TOKENHUB_DEFAULT_BASE_URL
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    def _post(self, credentials: dict, path: str, payload: dict) -> dict:
        headers = {"Content-Type": "application/json"}
        if api_key := credentials.get("api_key"):
            headers["Authorization"] = f"Bearer {api_key}"
        response = requests.post(
            self._endpoint(credentials, path),
            headers=headers,
            data=json.dumps(payload),
            timeout=(10, 300),
        )
        response.raise_for_status()
        return response.json()

    def _invoke(
        self,
        model: str,
        credentials: dict,
        texts: list[str],
        user: str | None = None,
        input_type: EmbeddingInputType = EmbeddingInputType.DOCUMENT,
    ) -> TextEmbeddingResult:
        del input_type
        embeddings = []
        used_tokens = 0
        max_chunks = self._get_max_chunks(model, credentials)
        for offset in range(0, len(texts), max_chunks):
            payload = {
                "model": model,
                "input": texts[offset : offset + max_chunks],
                "encoding_format": "float",
            }
            if user:
                payload["user"] = user
            response = self._post(credentials, "embeddings", payload)
            embeddings.extend(item["embedding"] for item in response["data"])
            used_tokens += response.get("usage", {}).get("total_tokens", 0)

        return TextEmbeddingResult(
            model=model,
            embeddings=embeddings,
            usage=self._calc_response_usage(model, credentials, used_tokens),
        )

    def _invoke_multimodal(
        self,
        model: str,
        credentials: dict,
        documents: list[MultiModalContent],
        user: str | None = None,
        input_type: EmbeddingInputType = EmbeddingInputType.DOCUMENT,
    ) -> MultiModalEmbeddingResult:
        del input_type
        embeddings = []
        used_tokens = 0
        for document in documents:
            if document.content_type == MultiModalContentType.TEXT:
                item = {"type": "text", "text": document.content}
            else:
                image_url = document.content
                if not image_url.startswith(("http://", "https://", "data:")):
                    image_url = f"data:image/png;base64,{image_url}"
                item = {"type": "image_url", "image_url": {"url": image_url}}
            payload = {"model": model, "input": [item], "encoding_format": "float"}
            if user:
                payload["user"] = user
            response = self._post(credentials, "embeddings/multimodal", payload)
            embeddings.append(response["data"][0]["embedding"])
            used_tokens += response.get("usage", {}).get("total_tokens", 0)

        return MultiModalEmbeddingResult(
            model=model,
            embeddings=embeddings,
            usage=self._calc_response_usage(model, credentials, used_tokens),
        )

    def _request_credentials_validation(self, model: str, credentials: dict):
        return requests.post(
            self._endpoint(credentials, "embeddings"),
            headers={
                "Authorization": f"Bearer {credentials.get('api_key', '')}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"model": model, "input": ["ping"]}),
            timeout=(10, 300),
        )