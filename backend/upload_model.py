from huggingface_hub import HfApi

api = HfApi()

api.upload_folder(
    folder_path="models",   # IMPORTANT: models folder inside backend
    repo_id="jyothimurali/hirematch-model",
    repo_type="model"
)

print("✅ Model uploaded successfully!")