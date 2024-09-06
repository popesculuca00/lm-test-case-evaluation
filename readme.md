### Model Evaluation Benchmark


##### This benchmark tool evaluates the performance of language models in generating Python unit tests. It measures the models' ability to produce valid, executable test cases with high code coverage for given Python functions.

---

This benchmark assumes an OpenAI API compatible server is running locally to generate the test cases for evaluation.

#### Recommended Setup

It is highly recommended to use vLLM for continuous batching.

To initialize a vLLM instance:

```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model <model_card> \
    --gpu-memory-utilization 0.98 \
    --max-model-len 4096 \
    --max-num-seqs 110 \
    --disable-log-requests```


For custom LoRA models, add the following flags:

```bash
--lora-modules <module alias>=<module_path> --chat-template ""
```


#### Example Commands

1. For OpenCodeInterpreter-CL-7B:
```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model m-a-p/OpenCodeInterpreter-CL-7B \
    --gpu-memory-utilization 0.98 \
    --max-model-len 4096
```

2. For Phi-3-mini-4k-instruct with LoRA layers:

```bash
python3 -m vllm.entrypoints.openai.api_server \
    --model unsloth/Phi-3-mini-4k-instruct \
    --gpu-memory-utilization 0.98 \
    --max-model-len 4096 \
    --max-num-seqs 110 \
    --disable-log-requests \
    --lora-modules pytest_module=~/disertatie/outputs/checkpoint-7000/ \
    --chat-template ""
```

Pass ```input_prompt_template``` to benchmark constructor if model was fine-tuned on a different dataset from the tokenizer prompt