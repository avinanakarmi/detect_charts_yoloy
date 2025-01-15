from huggingface_hub import upload_file
from huggingface_hub import login
login(token="<token>")

repo_id = "an778/multivariate-chart-yolo"

upload_file(
    path_or_fileobj="./runs/detect/train15/weights/best.pt",
    path_in_repo="model.pt",
    repo_id=repo_id,
    repo_type="model",
    token="<token>"
)
