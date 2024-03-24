import asyncio
import httpx

from constants import SERVER_DETECTION_TIMEOUT


async def _detect_inference_server():
    results = await asyncio.gather(
        _get_vllm_model_name(),
        _get_llama_model_name(),
    )

    return results


async def _get_vllm_model_name(server_detection_timeout=SERVER_DETECTION_TIMEOUT):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/v1/models", timeout=server_detection_timeout
            )
            server_info = response.json()
            return server_info["data"][0]["id"], "vllm"
    except:
        return None, None


async def _get_llama_model_name(server_detection_timeout=SERVER_DETECTION_TIMEOUT):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:1234/v1/models", timeout=server_detection_timeout
            )
            server_info = response.json()
            if server_info["data"][0]["id"]:
                model_name = "local-model"
            return model_name, "llamacpp"
    except:
        return None, None


def detect_server_config():
    results = asyncio.run(_detect_inference_server())
    for result in results:
        if result[0] or result[1]:
            return result
    return None, None
