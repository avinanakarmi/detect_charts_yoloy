from ultralytics import YOLO

def main():
    model = YOLO('./runs/detect/train15/weights/best.pt')
    results = model.val(data='charts.yaml', split='test')
    print(results)

if __name__ == "__main__":
    main()
