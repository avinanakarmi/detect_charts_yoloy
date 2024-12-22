from huggingface_hub import HfApi, HfFolder
from ultralytics import YOLO
from constants import CLASS_MAPPING

classes = list(CLASS_MAPPING.keys())
with open("./charts.yaml", "w") as f:
    f.write(f"""
    train: charts/images/train
    val: charts/images/val
    test: charts/images/test
    nc: {len(classes)}
    names: {classes}
    """)

model = YOLO('yolov8n.pt')

model.train(
    data='charts.yaml',  
    epochs=10,           
    imgsz=640,          
    batch=8,           
    device='mps'         
)

results = model.val(data='charts.yaml')
print(results) 

# api = HfApi()
# repo_id = "an778/multivariate-chart-yolo"

# api.upload_file(
#     path_or_fileobj="runs/detect/train/weights/best.pt",
#     path_in_repo="best.pt",                   
#     repo_id=repo_id,
#     repo_type="model"
# )