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
        """Initialize the main class for handling API calls to the server.

        Attributes:
            - sys_prompt (str): System prompt to be appended to all messages. Defaults to ``constants.EVALUATION_SYS_PROMPT`` if not provided.
            - inference_server (str): A string denoting the inference server type.  Currently supported: [``llamacpp``, ``vllm``]
            - api_key (str): Key for the api inference. Not needed for local inference, defaults to `not_needed`
            - client (ClientInterface): A ClientInterface object to avoid multiple detections. Will be generated automatically if not provided
        """
        self.sys_prompt = sys_prompt
        self.api_key = api_key

        if client and isinstance(client, ClientInterface):
            self.client = client
        else:
            self.client = ClientInterface(
                inference_server=inference_server, api_key=api_key
            )

        self.last_result = None


    def generate_response(
        self, user_query: str | list[str], n: int = 1, extract_code: bool = True
    ) -> list[str] | list[list[str]]:
        """
        Main method for handling model inference.
        Attributes:
            - user_query: either a string or a list of strings representing the model input alongside the system prompt. Handles batch data via continuous batching.
            - n: integer representing the number of choices to be generated
            - extract_code: boolean flag to switch code extraction from prompt for verbose models.
        """

        if isinstance(user_query, list):
            if self.client.inference_server != "VLLM":
                warnings.warn(
                    "Trying to do batch predictions on a server that does not support continuous batching. Execution will be very slow.."
                )

            return asyncio.run(
                self.async_generate_main(
                    user_query=user_query, n=n, extract_code=extract_code
                )
            )

        if not isinstance(user_query, str):
            raise TypeError(
                f"Trying user_query is of type {type(user_query)}, but type str was expected"
            )

        history = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": user_query},
        ]

        # multiple choice is available only via VLLM
        if self.client.inference_server != "vllm" and n > 1:
            client_type_warn = f"WARNING: n>1 for {self.client.inference_server=}, generation is limited to 1"
            warnings.warn(client_type_warn)
            n = 1

        completion = self.client.create(
            model=self.client.model,
            messages=history,
            temperature=0.7,
            stream=False,
            n=n,
        )

        model_response = {"role": "assistant", "content": ""}

        results = []
        for i in range(n):
            model_response["content"] = completion.choices[i].message.content
            if extract_code:
                result = extract_code_from_string(model_response["content"])
            else:
                result = model_response["content"]
            results.append(result)
        self.last_result = results

        return results


    async def async_generate_main(
        self, queries: list[str], n: int = 1, extract_code: bool = True
    ) -> list[str | list[str]]:
        """
        Aggregates and executes async generation for a batch generation. Best to be used with a server that supports continuous batching.
        """
        results = await asyncio.gather(
            *(
                self.async_generate(query=query, n=n, extract_code=extract_code)
                for query in queries
            )
        )
        self.last_result = results
        return results


    async def async_generate(
        self, user_query: str, n: int = 1, extract_code: bool = True
    ) -> (list[str] | list[list[str]]):
        return self.generate_response(
            user_query=user_query, n=n, extract_code=extract_code
        )


    def empty_history(self)->None:
        """Empties all chat history except the system prompt"""
        self.history = self.history[0]



if __name__ == "__main__":
    from constants import dummy_code
    import time

    client = ClientInterface()
    agent = CodeAgent(client=client)
    start = time.time()
    generated_pytest = agent.generate_response(dummy_code, n=2)
    # generated_pytest = agent.generate_response([dummy_code, dummy_code], n=2) # multiple predictions test

    print(
        f"Generation took {time.time() - start} seconds for {len(generated_pytest)} generations."
    )
    print(*generated_pytest, sep="\n\n" + "-" * 50 + "\n\n")
