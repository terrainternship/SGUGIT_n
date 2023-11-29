import os
import shutil
import re

def shorten_filename(filename):
    # Получаем расширение файла
    extension = os.path.splitext(filename)[1]
    # Используем регулярное выражение для замены нежелательной части имени файла
    new_name = re.sub(r'_png\.rf\..+{}'.format(re.escape(extension)), extension, filename)
    return new_name

def process_directory(src_dir, dst_dir):
    for dirpath, dirnames, filenames in os.walk(src_dir):
        # Создаем аналогичную структуру папок в целевой директории
        structure = os.path.join(dst_dir, os.path.relpath(dirpath, src_dir))
        if not os.path.isdir(structure):
            os.mkdir(structure)
        # Обрабатываем каждый файл в текущей директории
        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            # Получаем новое имя файла
            new_name = shorten_filename(filename)
            dst_file = os.path.join(structure, new_name)
            # Копируем файл в новую директорию с новым именем
            shutil.copy2(src_file, dst_file)

# Исходная и целевая директории
src_dir = "D:\\Учеба\\УИИ\\Стажировка\\1000_Chosen\\cabbage50.v1i.yolov8\\train"
dst_dir = "D:\\Учеба\\УИИ\\Стажировка\\1000_Chosen\\cabbage50.v1i.yolov8\\train2"

# Вызов функции для обработки директории
process_directory(src_dir, dst_dir)
