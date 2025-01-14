from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data="charts.yaml",
        epochs=20,
        batch=16,
        imgsz=640,
        device="cuda",
        workers=8,
        amp=False
    )

if __name__ == "__main__":
    main()
