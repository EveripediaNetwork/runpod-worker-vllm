#!/usr/bin/env python
import inference
import runpod
from runpod.serverless.utils.rp_validator import validate
from typing import Generator, Union
from schema import INPUT_SCHEMA

### Initialize the model to load it into memory
MODEL = inference.Predictor()
MODEL.setup()


async def run(job) -> Union[str, Generator[str, None, None]]:
    ### Validate the input
    validated_input = validate(job["input"], INPUT_SCHEMA)
    if "errors" in validated_input:
        yield {"error": validated_input["errors"]}
    validated_input = validated_input["validated_input"]

    ### Run the model depending on stream
    prediction = MODEL.predict(settings=validated_input)

    async for chunk in prediction:
        print(chunk, end="")
        output = chunk
        yield output


runpod.serverless.start({"handler": run, "return_aggregate_stream": True})
