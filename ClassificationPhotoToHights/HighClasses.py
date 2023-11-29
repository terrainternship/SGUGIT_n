# Этот код реализует процесс классификации изображений, используя модель YOLOv8 для детекции объектов.
# Каждый объект классифицируется на основе его размера на изображении (как "close", "medium" или "far").
# Результаты классификации суммируются, и итоговая классификация каждого изображения используется для копирования
# в соответствующие папки. Кроме того, создается отчет о классификации в формате CSV.


# Импорт необходимых библиотек
import shutil  # для работы с файловой системой
import cv2  # для работы с изображениями
from ultralytics import YOLO  # для использования модели YOLO
import os  # для работы с файловой системой
from glob import glob  # для поиска файлов
import pandas as pd  # для работы с данными в формате таблиц
import numpy as np  # для математических операций

# Загрузка модели YOLOv8
model = YOLO(r"D:\cabbageDopBig_yolov8\best.pt")  # Путь к файлу весов модели

# Функция для вычисления процента заполнения объектом
def compute_fill_percentage(polygon, image_dims):
    # Вычисление площади контура
    contour = cv2.contourArea(cv2.convexHull(np.array(polygon, dtype='int32')))
    # Вычисление площади изображения
    image_area = image_dims[0] * image_dims[1]
    # Расчет процента заполнения
    fill_percentage = (contour / image_area) * 100
    return fill_percentage

# Функция для классификации объекта по дистанции
def classify_distance(fill_percentage, close_threshold, far_threshold):
    # Определение классификации на основе пороговых значений
    if fill_percentage >= close_threshold:
        return "close"
    elif fill_percentage <= far_threshold:
        return "far"
    else:
        return "medium"

# Функция для агрегации результатов классификации
def aggregate_results(classifications):
    if not classifications:
        return "No objects detected"
    # Возвращение наиболее часто встречающейся классификации
    return max(set(classifications), key=classifications.count)

# Функция обработки изображения
def process_image(image_path, close_threshold, far_threshold, show_image=False):
    # Чтение изображения
    image = cv2.imread(image_path)
    image_dims = image.shape[:2]
    # Получение обнаруженных объектов
    detections = model(image)[0]
    classifications = []

    for data in detections.boxes.data.tolist():
        confidence = data[4]
        if float(confidence) < 0.4:  # Порог уверенности
            continue
        # Получение координат и вычисление процента заполнения
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        polygon = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        fill_percentage = compute_fill_percentage(polygon, image_dims)
        classification = classify_distance(fill_percentage, close_threshold, far_threshold)
        classifications.append(classification)
        # Отрисовка полигона и классификации на изображении
        cv2.polylines(image, [np.array(polygon, dtype='int32')], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(image, classification, polygon[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Получение итоговой классификации
    final_classification = aggregate_results(classifications)
    # Отображение изображения, если требуется
    if show_image:
        cv2.putText(image, f'Final Classification: {final_classification}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return final_classification

def main():
    # Путь к папке с изображениями
    image_folder = r"D:\Learning\UII\DataSets\DataSet_2.1_Train_Valid\train\images"
    # Список путей к изображениям
    image_paths = glob(os.path.join(image_folder, '*.jpg')) + glob(os.path.join(image_folder, '*.png'))
    # Задание пороговых значений
    close_threshold = 11
    far_threshold = 4
    # Подготовка данных для отчета
    report_data = []

    for image_path in image_paths:
        # Обработка каждого изображения
        final_classification = process_image(image_path, close_threshold, far_threshold, show_image=False)
        # Копирование изображений в соответствующие папки
        destination_folder = os.path.join("path_to_destination_folder", final_classification)
        os.makedirs(destination_folder, exist_ok=True)
        shutil.copy(image_path, destination_folder)

        # Добавление данных в отчет
        report_data.append({'Image Path': image_path, 'Classification': final_classification})

    # Создание и сохранение отчета
    report_df = pd.DataFrame(report_data)
    report_df.to_csv('classification_report.csv', index=False)

if __name__ == '__main__':
    main()
