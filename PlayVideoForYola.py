# В этом коде реализована загрузка и использование модели YOLOv8 для обработки видео. Для каждого кадра выполняется
# детекция объектов, их классификация (как "good" или "bad"), и визуализация результатов на кадре. Видео обрабатывается
# кадр за кадром, и результат сохраняется в выходной файл. Используется OpenCV для работы с видео и обработки
# изображений, а также YOLO для детекции объектов.


# Импорт необходимых библиотек
from ultralytics import YOLO  # для работы с моделью YOLO
import cv2  # для работы с видео и изображениями
import numpy as np  # для математических операций

# Загрузите YOLOv8 с пользовательскими весами
model = YOLO(r"D:\cabbageDopBig_yolov8\best_det_yaml_rep2.pt")

# Функция для обработки кадра
def process_frame(frame):
    # Выполнить вывод с помощью модели YOLO
    results = model(frame)[0]  # получить первый объект Results из списка

    # Обработка обнаруженных объектов
    for i, box in enumerate(results.boxes.xyxy):  # перебор по каждому прямоугольнику в атрибуте xyxy
        label = int(results.boxes.cls[i])  # получить метку класса для текущей детекции
        x1, y1, x2, y2 = map(int, box)
        # Задать цвет рамки: зеленый для 'good', красный для 'bad'
        color = (0, 255, 0) if label == 0 else (0, 0, 255)
        # Нарисовать рамку вокруг обнаруженного объекта
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Форматирование и отображение вероятности и названия класса
        class_name = "good" if label == 0 else "bad"
        score = f"{results.boxes.conf[i]:.2f}"  # форматирование вероятности до 2-х десятичных знаков
        label_text = f"{class_name} {score}"
        # Нанести текст на кадр
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame  # вернуть обработанный кадр

# ... остальной код ...

# Загрузите видео
cap = cv2.VideoCapture(r"D:\Learning\UII\Stashir\4 Крупные\Исходники и фреймы по папкам\DJI_0334.MP4")

# Получите параметры видео для создания VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(r"D:\cabbageDopBig_yolov8\ResultVideo\best_det_yaml_rep2_DJI_0334.avi", fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

# Цикл для обработки каждого кадра видео
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    out.write(processed_frame)  # Сохраните обработанный кадр в выходной файл

    # Показать обработанный кадр
    cv2.imshow('Video', processed_frame)

    # Прервать цикл при нажатии 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освободить ресурсы
cap.release()
out.release()  # Закройте VideoWriter
cv2.destroyAllWindows()
