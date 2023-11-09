# vLLM Worker on Runpod Serverless

This is worker code which uses vLLM for inference on Runpod Serverless.

# 📝 Table of Contents
- [🌟 How to use](#-how-to-use)
- [🏗️ build docker image (Optional)](#️-build-docker-image-optional)
- [🚀 deploy to Runpod Serverless](#-deploy-to-runpod-serverless)
  - [1. Create a new Network Volume](#1-create-a-new-network-volume)
  - [2. Create a new Template](#2-create-a-new-template)
  - [3. Create a new Endpoint](#3-create-a-new-endpoint)
  - [4. Test your endpoint](#4-test-your-endpoint)
- [📦 Request Body](#-request-body)
- [🔗 Environment Variables](#-environment-variables)
- [🚀 GPU Type Guide](#-gpu-type-guide)
- [📝 License](#-license)
- [📚 References](#-references)
- [🙏 Thanks](#-thanks)

# 🌟 How to use
1. Clone this repository
1. build docker image
1. push docker image to your docker registry
1. deploy to Runpod Serverless

## 🏗️ build docker image (Optional)
```bash
docker build -t <your docker registry>/<your docker image name>:<your docker image tag> .
```
Push the image to docker with the following command:
```bash
docker push <your docker registry>/<your docker image name>:<your docker image tag>
```
> Or you can use [`lobstrate/runpod-worker-vllm`](https://hub.docker.com/repository/docker/lobstrate/runpod-worker-vllm) image from docker hub

## 🚀 deploy to Runpod Serverless
After having docker image on your docker registry, you can deploy to Runpod Serverless. Here is the step by step guide on how you can deploy this on runpod. In this guide, we will set up network volume so that we can download our model from huggingface hub into the network volume. At the end, when our endpoint gets its first request, it will download the model from huggingface hub into the network volume. After that, it will use the model from the network volume for inference. on subsequent requests. (Even if the worker gets scaled down to 0, the model will be persisted in the network volume)

### 1. Create a new Network Volume
You need to create a network volume for the worker to download your LLM model into from huggingface hub. You can create a network volume from the Runpod UI.

![Create New Network Volume](/assets/Create%20Network%20Storage.png)

1. Click on Storage from runpod sidebar under serverless tab.
1. Click on `+ Network Volume` button.
1. Select a datacenter region closest to your users.
1. Give a name to your network volume.
1. Select a size for your network volume.
1. Click on `Create` button.

> Note: To get a rough estimate on how much storage you need, you can check out your model size on https://huggingface.co. Click on files and Versions tab and check how much storage you need to store all the files.

### 2. Create a new Template
After creating a network volume, you need to create a template for your worker to use. For this,

![Create New Template](/assets/Create%20Template.png)

1. Click on Custom Templates from runpod sidebar under serverless tab.
1. Click on `New Template` button.
1. Give a name to your template.
1. Enter your docker image name in the `Container Image` field. This is the same image you pushed to your docker registry in the previous step. (Or you can enter [`lobstrate/runpod-worker-vllm:latest`](https://hub.docker.com/repository/docker/lobstrate/runpod-worker-vllm) image from docker hub)
1. Select Container disk size. (This doesn't matter much as we are using network volume for model storage)
1. **[IMPORTANT]** Enter environment variables for your model. `MODEL_NAME` is required. Which is used to download your model from huggingface hub. (refer [Environment Variables](#environment-variables) section for more details)

### 3. Create a new Endpoint
After creating a template, you need to create an endpoint for your worker to use. For this,

![Create New Endpoint](/assets/Create%20Endpoint.png)
1. Click on Endpoints from runpod sidebar under serverless tab.
1. Click on `New Endpoint` button.
1. Give a name to your endpoint.
1. Select template you created in the previous step.
1. Select GPU type. You can follow this guide to select the right GPU type for your model. [GPU Type Guide](#gpu-type-guide)
1. Select network volume you created in the previous step.
1. Click on `Create` button.

### 4. Test your endpoint
After creating an endpoint, you can test out your endpoint inside runpod UI. For this,

![Test Endpoint](/assets/Test%20Endpoint.png)
1. Click on Requests tab from your endpoint page.
1. Click on `Run` button.


You can also modify your request body. Check out [Request Body](#request-body) section for more details.


# 📦 Request Body
This is the request body you can send to your endpoint:

```json
{
  "input": {
    "prompt": "Say, Hello World!",
    "max_tokens": 50,
    // other params...
  } 
}
```

All the params you can send to your endpoint are listed here: 
1. `prompt`: The prompt you want to generate from.
1. `max_tokens`: Maximum number of tokens to generate per output sequence.
1. `n`: Number of output sequences to return for the given prompt.
1. `best_of`: Number of output sequences that are generated from the prompt. From these `best_of` sequences, the top `n` sequences are returned. `best_of` must be greater than or equal to `n`. This is treated as the beam width when `use_beam_search` is True. By default, `best_of` is set to `n`.
1. `presence_penalty`: Float that penalizes new tokens based on whether they appear in the generated text so far. Values > 0 encourage the model to use new tokens, while values < 0 encourage the model to repeat tokens.
1. `frequency_penalty`: Float that penalizes new tokens based on their frequency in the generated text so far. Values > 0 encourage the model to use new tokens, while values < 0 encourage the model to repeat tokens.
1. `repetition_penalty`: Float that penalizes new tokens based on whether they appear in the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens.
1. `temperature`: Float that controls the randomness of the sampling. Lower values make the model more deterministic, while higher values make the model more random. Zero means greedy sampling.
1. `top_p`: Float that controls the cumulative probability of the top tokens to consider. Must be in (0, 1]. Set to 1 to consider all tokens.
1. `top_k`: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens.
1. `use_beam_search`: Whether to use beam search instead of sampling.
1. `length_penalty`: Float that penalizes sequences based on their length. Used in beam search.
1. `early_stopping`: Controls the stopping condition for beam search. It accepts the following values: `True`, where the generation stops as soon as there are `best_of` complete candidates; `False`, where an heuristic is applied and the generation stops when is it very unlikely to find better candidates; `"never"`, where the beam search procedure only stops when there cannot be better candidates (canonical beam search algorithm).
1. `stop`: List of strings that stop the generation when they are generated. The returned output will not contain the stop strings.
1. `stop_token_ids`: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are sepcial tokens.
1. `ignore_eos`: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated.
1. `logprobs`: Number of log probabilities to return per output token. Note that the implementation follows the OpenAI API: The return result includes the log probabilities on the `logprobs` most likely tokens, as well the chosen tokens. The API will always return the log probability of the sampled token, so there may be up to `logprobs+1` elements in the response.
1. `prompt_logprobs`: Number of log probabilities to return per prompt token.
1. `skip_special_tokens`: Whether to skip special tokens in the output.
1. `spaces_between_special_tokens`: Whether to add spaces between special tokens in the output. Defaults to True.
1. `logits_processors`: List of functions that modify logits based on previously generated tokens.



    
# 🔗 Environment Variables
These are the environment variables you can define on your runpod template:

| key | value | optional |
| --- | --- | --- |
| MODEL_NAME | your model name | false |
| HF_HOME | /runpod-volume | true |
| HUGGING_FACE_HUB_TOKEN | your huggingface token | true |
| MODEL_REVISION | your model revision | true |
| MODEL_BASE_PATH | your model base path | true |
| TOKENIZER | your tokenizer | true |

> Note: You can get your huggingface token from https://huggingface.co/settings/token

# 🚀 GPU Type Guide
Here is a rough estimate on how much VRAM you need for your model. You can use this table to select the right GPU type for your model.
| Model Parameters | Storage & VRAM |
| --- | --- |
| 7B | 6GB |
| 13B | 9GB |
| 33B | 19GB |
| 65B | 35GB |
| 70B | 38GB |

# 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

# 📚 References
1. [Runpod Serverless](https://runpod.io)
1. [vLLM](https://github.com/vllm-project/vllm)
1. [Huggingface](https://huggingface.co)

# 🙏 Thanks
Special thanks to @Jorghi12 and @ashleykleynhans for helping out with this project.