import os
import shutil


def copy_and_rename_images(source_directory, target_directory):
    # Если целевая директория не существует, создаем ее
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Получаем список всех поддиректорий
    subdirs = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(source_directory, subdir)

        # Получаем список всех файлов в поддиректории
        for filename in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, filename)

            # Проверяем, что это изображение (по расширению файла)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff')):
                # Конструируем новое имя файла и путь к файлу в целевой директории
                new_filename = f"{subdir}_{filename}"
                new_file_path = os.path.join(target_directory, new_filename)

                # Копируем файл
                shutil.copy2(file_path, new_file_path)

if __name__ == "__main__":
    source_directory = "D:/Учеба/УИИ/Стажировка/4 Крупные/Исходники и фреймы по папкам"
    target_directory = "D:/Учеба/УИИ/Стажировка/4 Крупные/Все фреймы"
    copy_and_rename_images(source_directory, target_directory)
