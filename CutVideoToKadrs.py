# В этом коде реализована обработка видео с целью выделения и сохранения отдельных кадров, основываясь на их
# уникальности и резкости. Используются библиотеки OpenCV для работы с изображениями, MoviePy для работы с видео
# и PIL для сохранения кадров. Многопоточность обеспечивается с помощью ThreadPoolExecutor.


# Импорт необходимых библиотек
import cv2  # для работы с изображениями и видео
import numpy as np  # для математических операций
from moviepy.editor import VideoFileClip  # для работы с видеофайлами
from PIL import Image  # для работы с изображениями
import os  # для работы с файловой системой
from concurrent.futures import ThreadPoolExecutor  # для многопоточности

# Функция для расчета хэша изображения (d-hash)
def dhash(image, hash_size=8):
    # Уменьшаем изображение и преобразуем его в чёрно-белый формат
    resized = cv2.resize(image, (hash_size + 1, hash_size))
    # Вычисляем разницу между соседними пикселями
    diff = resized[:, 1:] > resized[:, :-1]
    # Преобразуем разницу в хеш
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

# Функция для определения, является ли изображение размытым
def is_blurry(image, threshold=100):
    # Преобразуем изображение в чёрно-белый формат
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Вычисляем вариацию Лапласиана (меру резкости)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    # Возвращаем, является ли изображение размытым
    return fm < threshold

# Функция для сохранения кадра видео в файл
def save_frame(frame_bgr, frame_count, output_dir):
    # Формируем имя файла кадра
    frame_filename = f'frame_{frame_count}.png'
    # Получаем полный путь к файлу
    file_path = os.path.join(output_dir, frame_filename)
    # Преобразуем изображение в формат PIL для сохранения
    im_pil = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    try:
        # Сохраняем изображение
        im_pil.save(file_path)
        print(f"Saved frame {frame_count} to {file_path}")
    except Exception as e:
        print(f"Failed to save frame: {frame_filename}, Error: {e}")

# Функция для обработки видео
def process_video(video_path, similarity_threshold=0.12, blur_threshold=100, frame_skip=1):
    # Загружаем видеофайл
    video_clip = VideoFileClip(video_path)

    # Вычисляем общее количество кадров в видео
    total_frames = int(video_clip.fps * video_clip.duration)
    print(f"Total frames in the video: {total_frames}")

    # Подготавливаем директорию для сохранения кадров
    video_name = os.path.basename(video_path).split('.')[0]
    output_dir = os.path.join(os.path.dirname(video_path), f'{video_name}_frames')
    print(f"Output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Инициализируем переменные для обработки кадров
    prev_frame = None
    prev_hash = None
    frame_count = 0
    saved_frames_count = 0
    skip_counter = 0

    # Создаем пул потоков для асинхронной обработки
    with ThreadPoolExecutor() as executor:
        # Перебираем кадры видео
        for frame in video_clip.iter_frames(fps=video_clip.fps, dtype='uint8'):
            frame_count += 1
            skip_counter += 1

            # Пропускаем кадры согласно frame_skip
            if skip_counter < frame_skip:
                continue
            skip_counter = 0

            # Конвертируем кадр в формат BGR для OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Проверяем, изменился ли кадр достаточно по сравнению с предыдущим
            if prev_frame is not None:
                h = dhash(frame_bgr)
                similarity = 1 - bin(prev_hash ^ h).count('1') / 64.0  # 64 - размер хэша

                if similarity < similarity_threshold and not is_blurry(frame_bgr, blur_threshold):
                    # Асинхронно сохраняем кадр
                    executor.submit(save_frame, frame_bgr, frame_count, output_dir)
                    saved_frames_count += 1

            prev_frame = frame_bgr
            prev_hash = dhash(frame_bgr)

    print(f"Processing completed. Total frames processed: {frame_count}, frames saved: {saved_frames_count}")

# Путь к видеофайлу
video_path = "D:\\Учеба\\УИИ\\Стажировка\\4 Крупные\\Исходники и фреймы по папкам\\DJI_0330.MP4"
# Запуск обработки видео
process_video(video_path, frame_skip=1)  # Пропуск каждого второго кадра
