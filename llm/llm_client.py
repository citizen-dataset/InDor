import os
from typing import Dict, List, Any, Optional

from openai import OpenAI

class LLMClient:
    """Base LLM client class, handling shared logic for all providers"""

    DEFAULT_API_KEY_ENV_NAME: str = "OPENROUTER_API_KEY"
    DEFAULT_BASE_URL: str = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        """initialize the base client"""
        # get the API key
        if not api_key:
            remote_api_key = os.getenv(self.DEFAULT_API_KEY_ENV_NAME)
            if not remote_api_key:
                raise ValueError(f"{self.DEFAULT_API_KEY_ENV_NAME} not provided or found in environment variables.")
        # create the client instance
        client_kwargs = {"api_key": remote_api_key, "base_url": self.DEFAULT_BASE_URL}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

    def complete(self, model: str, messages: List[Dict[str, Any]], **kwargs) -> str:
        """use the API to generate a completion"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            if response.choices:
                return response.choices[0].message.content
            else:
                raise Exception("No response choices found.")
        except Exception as e:
            print(f"Error during API call: {e}")
            raise e