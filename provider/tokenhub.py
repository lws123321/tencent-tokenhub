from collections.abc import Mapping

from dify_plugin import ModelProvider
from dify_plugin.errors.model import CredentialsValidateFailedError
from openai import OpenAI

class TokenHubModelProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: Mapping) -> None:
        try:
            base_url = credentials.get("api_base", "").strip() or "https://tokenhub.tencentmaas.com/v1"
            client = OpenAI(api_key=credentials.get("api_key", ""), base_url=base_url, timeout=120)
            client.models.list()
        except Exception as ex:
            raise CredentialsValidateFailedError(f"Credentials validation failed: {ex}") from ex
