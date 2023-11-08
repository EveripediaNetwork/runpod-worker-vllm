import os
from vllm import AsyncLLMEngine, SamplingParams, AsyncEngineArgs
from vllm.utils import random_uuid
from download_model import download_model
import time

MODEL_NAME = os.environ.get("MODEL_NAME")
MODEL_REVISION = os.environ.get("MODEL_REVISION", "main")
MODEL_BASE_PATH = os.environ.get("MODEL_BASE_PATH", "/runpod-volume/")
TOKENIZER = os.environ.get("TOKENIZER", None)
NUM_GPU_SHARD = int(os.environ.get("NUM_GPU_SHARD", 1))


class Predictor:
    def setup(self):
        # Model moved to network storage
        model_directory = f"{MODEL_BASE_PATH}{MODEL_NAME.split('/')[1]}"

        # check if model directory exists. else, download model
        if not os.path.isdir(model_directory):
            print("Downloading model...")
            try:
                download_model(model_name=MODEL_NAME, model_revision=MODEL_REVISION)
            except Exception as e:
                print(f"Error downloading model: {e}")
                # delete model directory if it exists
                if os.path.isdir(model_directory):
                    os.system(f"rm -rf {model_directory}")
                raise e

        # Prepare the engine's arguments
        engine_args = AsyncEngineArgs(
            model=f"{MODEL_BASE_PATH}{MODEL_NAME.split('/')[1]}",
            tokenizer=TOKENIZER,
            tokenizer_mode="auto",
            tensor_parallel_size=NUM_GPU_SHARD,
            dtype="auto",
            seed=0,
            disable_log_stats=False,
        )

        # Create the vLLM asynchronous engine
        self.llm = AsyncLLMEngine.from_engine_args(engine_args)

    async def predict(self, settings):
        ### Set the generation settings
        sampling_params = SamplingParams(
            temperature=settings["temperature"],
            top_p=settings["top_p"],
            top_k=settings["top_k"],
            n=settings["n"],
            best_of=settings["best_of"],
            presence_penalty=settings["presence_penalty"],
            frequency_penalty=settings["frequency_penalty"],
            use_beam_search=settings["use_beam_search"],
            stop=settings["stop"],
            ignore_eos=settings["ignore_eos"],
            max_tokens=settings["max_tokens"],
            logprobs=settings["logprobs"],
        )

        self.settings = sampling_params

        ### Generate
        output = None
        time_begin = time.time()
        results_generator = self.llm.generate(
            settings["prompt"], self.settings, random_uuid()
        )
        prev_text = ""
        async for request_output in results_generator:
            updated_text = request_output.outputs[0].text
            chunk = updated_text[len(prev_text) - 1 : -1]
            prev_text = updated_text
            yield chunk

        time_end = time.time()
        print(f"⏱️ Time taken for inference: {time_end - time_begin} seconds")
