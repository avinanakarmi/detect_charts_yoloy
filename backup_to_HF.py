from huggingface_hub import HfApi

api = HfApi()
repo_id = "an778/multivariate-chart-yolo"

api.upload_file(
    path_or_fileobj="runs/detect/train/weights/best.pt",
    path_in_repo="best.pt",                   
    repo_id=repo_id,
    repo_type="model"
)