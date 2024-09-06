import warnings
import asyncio

from constants import EVALUATION_SYS_PROMPT
from Agent.agent_utils import extract_code_from_string
from client_interface.client import ClientInterface


class CodeAgent:
    def __init__(
        self,
        sys_prompt: str = EVALUATION_SYS_PROMPT,
        inference_server: str = None,
        api_key: str = "not_needed",
        client: ClientInterface = None,
    ):
        self.sys_prompt = sys_prompt
        self.api_key = api_key

        if client and isinstance(client, ClientInterface):
            self.client = client
        else:
            self.client = ClientInterface(
                inference_server=inference_server, api_key=api_key
            )

        self.last_result = None
        self.history = []

    async def generate_response_async(
        self,
        user_query: str | list[str],
        n: int = 1,
        extract_code: bool = True,
        history: None | list[dict] = None,
    ):
        if isinstance(user_query, list):
            return await self.async_generate_main(
                queries=user_query, n=n, extract_code=extract_code, history=history
            )
        else:
            return await self.async_generate(
                user_query=user_query, n=n, extract_code=extract_code, history=history
            )

    async def async_generate_main(
        self,
        queries: list[str],
        n: int = 1,
        extract_code: bool = True,
        history: None | list[dict] = None,
    ):
        tasks = [
            self.async_generate(query, n, extract_code, history if history else None)
            for query in queries
        ]
        results = await asyncio.gather(*tasks)
        self.last_result = results
        return results

    async def async_generate(
        self,
        user_query: str,
        n: int = 1,
        extract_code: bool = True,
        history: None | list[dict] = None,
    ):
        if not isinstance(user_query, str):
            raise TypeError(f"user_query is of type {type(user_query)}, expected str.")

        if history is None:
            history = [
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": user_query},
            ]

        if self.client.inference_server != "vllm" and n > 1:
            warnings.warn(
                f"n>1 for {self.client.inference_server=}, generation is limited to 1"
            )
            n = 1

        completion = await self.client.create(
            model=self.client.model,
            messages=history,
            temperature=0.1,
            stream=False,
            frequency_penalty=1.05,
            n=n,
        )

        results = []
        for i in range(n):
            content = completion.choices[i].message.content
            result = extract_code_from_string(content) if extract_code else content
            results.append(result)
        self.last_result = results
        return results

    def generate_response(
        self,
        user_query: str | list[str],
        n: int = 1,
        extract_code: bool = True,
        history: None | list[dict] = None,
    ):
        return asyncio.run(
            self.generate_response_async(
                user_query=user_query, n=n, extract_code=extract_code, history=history
            )
        )

    def empty_history(self):
        """Empties all chat history except the system prompt"""
        if self.history:
            self.history = [self.history[0]]


if __name__ == "__main__":
    from constants import dummy_code
    import time

    client = ClientInterface()
    agent = CodeAgent(client=client)
    start = time.time()
    # generated_pytest = agent.generate_response(dummy_code, n=2)

    history = [
        {"role": "system", "content": EVALUATION_SYS_PROMPT},
        {"role": "user", "content": dummy_code},
    ]
    generated_pytest = agent.generate_response(
        [dummy_code, dummy_code], n=1, history=history
    )

    print(
        f"Generation took {time.time() - start} seconds for {len(generated_pytest)} generations."
    )
    print(*generated_pytest, sep="\n\n" + "-" * 50 + "\n\n")
