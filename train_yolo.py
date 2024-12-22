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