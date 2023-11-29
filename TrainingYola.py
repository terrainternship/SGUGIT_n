import os
#os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

from ultralytics import YOLO
import matplotlib.pyplot as plt
import torch

# Освобождение видеопамяти
torch.cuda.empty_cache()

results_path = r"D:\cabbageDopBig_yolov8\ResultTrain"

if __name__ == '__main__':
    # Загрузка модели.
    model = YOLO('yolov8n.pt')
    results = model.train(data=r"D:\Learning\UII\DataSets\1 Датасет 4.1\data (1).yaml",
                          epochs=80,
                          device=0,
                          imgsz=640,
                          iou=0.8,
                          name='runs_dataset4.1_pt_0.8_rep1',
                          project=results_path,
                          exist_ok=True)  # train the model


    # Сохранение весов модели с лучшей точностью валидации.
    best_weights = torch.load('runs/train/yolov8n_custom/weights/best.pt')
