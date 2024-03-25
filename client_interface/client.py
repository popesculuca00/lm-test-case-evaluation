import asyncio
import httpx

from openai import AsyncOpenAI

from client_interface.client_utils import detect_server_config


class ClientInterface:
    inference_server_types = ["llamacpp", "vllm"]

    def __init__(
        self,
        inference_server: str = None,
        api_key: str = "not_needed",
    ):
        """
        Attributes:
            - inference_server (str): A string denoting the inference server type.  Currently supported: [``llamacpp``, ``vllm``]
            - api_key (str): Key for the inference api. Not needed for local inference, defaults to `not_needed`.
        """

        if (
            inference_server is not None
            and inference_server not in self.inference_server_types
        ):
            raise AttributeError(
                f"Server mult be in `{self.inference_server_types}`, got `{inference_server}`"
            )

        self.model, self.inference_server = detect_server_config()
        self.api_key = api_key
        self._create_client()

    @property
    def create(self):
        return self.client.chat.completions.create

    def _create_client(self):
        if self.inference_server == "llamacpp":
            api_base = "http://localhost:1234/v1"
            self.model = "local-model"
            self.client = AsyncOpenAI(base_url=api_base, api_key=self.api_key)

        elif self.inference_server == "vllm" or self.model:
            self.inference_server = "vllm"
            api_base = "http://localhost:8000/v1"
            self.client = AsyncOpenAI(base_url=api_base, api_key=self.api_key)

    def __repr__(self):
        return f"ServerConfig(\n{self.inference_server=}\n{self.model=})".replace(
            "self.", "\t"
        )


if __name__ == "__main__":
    x = ClientInterface()
    print(x)
