# Base image
FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel

# Use bash shell with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set the working directory
WORKDIR /


# Prepare the models inside the docker image
ARG HUGGING_FACE_HUB_TOKEN=
ENV HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN

# Prepare argument for the model and tokenizer
ARG MODEL_NAME=""
ENV MODEL_NAME=$MODEL_NAME
ARG MODEL_REVISION="main"
ENV MODEL_REVISION=$MODEL_REVISION
ARG MODEL_BASE_PATH="/runpod-volume/"
ENV MODEL_BASE_PATH=$MODEL_BASE_PATH

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Add src files (Worker Template)
ADD src .

# Download the model if defined
RUN if [ -n $MODEL_NAME ]; then \
    python3 download_model.py $MODEL_NAME $MODEL_REVISION; \
    fi

CMD ["bin/bash", "entrypoint.sh"]
