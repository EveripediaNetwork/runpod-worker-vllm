import os
from huggingface_hub import snapshot_download

# Get the hugging face token
HUGGING_FACE_HUB_TOKEN = os.environ.get("HUGGING_FACE_HUB_TOKEN", None)
MODEL_BASE_PATH = os.environ.get("MODEL_BASE_PATH", "/runpod-volume/")


def download_model(model_name: str, model_revision: str):
    # Download the model from hugging face
    download_kwargs = {}

    if HUGGING_FACE_HUB_TOKEN:
        download_kwargs["token"] = HUGGING_FACE_HUB_TOKEN

    DOWNLOAD_PATH = f"{MODEL_BASE_PATH}{model_name.split('/')[1]}"

    print(f"Downloading model to: {DOWNLOAD_PATH}")

    downloaded_path = snapshot_download(
        repo_id=model_name,
        revision=model_revision,
        local_dir=DOWNLOAD_PATH,
        local_dir_use_symlinks=False,
        **download_kwargs,
    )

    print(f"Finished downloading to: {downloaded_path}")
