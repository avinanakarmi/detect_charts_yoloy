#######################################################
#                                                     #
# Source: https://github.com/kdavila/CHART_Info_2024  #
#                                                     #
#######################################################

import os
import shutil
from pathlib import Path
from constants import CLASS_MAPPING

PATH_BASE = './datasets/'
DESTINATION = f"{PATH_BASE}charts/"
TRAIN_SOURCE = f"{PATH_BASE}CHARTINFO_2024_Train/"
TEST_SOURCE = f"{PATH_BASE}CHARTINFO_2024_Test/"

def copy_files(src, proportion_to_move, destination):
  os.makedirs(destination, exist_ok=True)
  files = os.listdir(src)
  total_files = len(files)

  num_files_to_move = int(proportion_to_move * total_files)

  files_to_move = sorted(files)[:num_files_to_move]

  for file_name in files_to_move:
      src_path = os.path.join(src, file_name)
      shutil.move(src_path, destination)

  print(f"Moved {num_files_to_move} out of {total_files} files from {src} to {destination}.")

def parse_path_copy(path, destination, amount):
  if path.is_dir():
      subdirs = [d for d in path.iterdir() if d.is_dir()]
      if subdirs:
          for subdir in subdirs:
            copy_files(subdir, amount, destination)
      else:
          copy_files(path, amount, destination);
  else:
      print(f"The path '{path}' is not a valid directory.")

## MOVE 80% of train images and 100% of test images
path = Path(f"{TRAIN_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/train", 0.8)
path = Path(f"{TEST_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/test", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE 80% of train annotation and 100% of test annotation
path = Path(f"{TRAIN_SOURCE}/annotations_XML/")
parse_path_copy(path, f"{DESTINATION}labels/train", 0.8)
path = Path(f"{TEST_SOURCE}/annotations_XML/")
parse_path_copy(path, f"{DESTINATION}labels/test", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE remaining train images to validation
path = Path(f"{TRAIN_SOURCE}/images/")
parse_path_copy(path, f"{DESTINATION}images/val", 1)

print("\n")
print("=" * 100)
print("\n")

## MOVE remaining train annotations to validation
path = Path(f"{TRAIN_SOURCE}/annotations_XML/")
parse_path_copy(path, f"{DESTINATION}labels/val", 1)

print("\n")
print("=" * 100)
print("\n")

### Validate copy
path = Path("./datasets/charts")
if path.is_dir():
      print(f"- {path}")
      subdirs = [d for d in path.iterdir() if d.is_dir()]
      if subdirs:
          for subdir in subdirs:
            print(f"\t|-> {subdir}")
            if subdir.is_dir():
                sds = [d for d in subdir.iterdir() if d.is_dir()]
                for sd in sds:
                    files = os.listdir(sd)
                    print(f"\t\t|-> {sd} ({len(files)})")
            else:
                files = os.listdir(subdir)
                print(f"\t|-> {subdir} ({len(files)})")
      else:
            files = os.listdir(path)
            print(f"\t|-> {path} ({len(files)})")
else:
  print(f"The path '{path}' is not a valid directory.")

print("\n")
print("=" * 100)
print("\n")

#### format annotations for yolo
import glob
import xml.etree.ElementTree as ET

PATH_BASE = './datasets/charts/labels'
FOLDERS = ['train', 'test', 'val']

for folder in FOLDERS:
  xml_files = glob.glob(f'{PATH_BASE}/{folder}/*.xml')
  for file in xml_files:
      tree = ET.parse(file)
      root = tree.getroot()
      panel_tree_node = root.find(".//PanelTreeNode")
      if panel_tree_node is not None:
          X1 = int(root.find(".//X1").text)
          Y1 = int(root.find(".//Y1").text)
          X2 = int(root.find(".//X2").text)
          Y2 = int(root.find(".//Y2").text)

          image_width = X2
          image_height = Y2

          class_name = root.find(".//Type").text.strip().lower()
          class_id = CLASS_MAPPING.get(class_name, -1)
          if class_id != -1:
            x_center = (X1 + X2) / 2
            y_center = (Y1 + Y2) / 2
            width = X2 - X1
            height = Y2 - Y1

            x_center_norm = x_center / image_width
            y_center_norm = y_center / image_height
            width_norm = width / image_width
            height_norm = height / image_height

            yolo_annotation = f"{class_id} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"
            filename = file.split('.xml')[0]
            with open(f"{filename}.txt", "w") as f:
                f.write(yolo_annotation + "\n")
      else:
            print("Class not found in CLASS_MAPPING.")
      os.remove(file)
  else:
        print(f"Bounding box data not found in the XML. {file}")
        path_parts = file.split('labels')
        image_to_remove = path_parts[0] + "images" + path_parts[1].split('.xml')[0] + '.jpg'
        os.remove(image_to_remove)
        print(f"Deleted {image_to_remove}\n")