import os
import shutil

def copy_label_files(label_folder, image_folder, output_folder):
    # Проверяем, существует ли папка вывода, иначе создаем ее
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список файлов меток в папке
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

    # Проходим по каждому файлу меток
    for label_file in label_files:
        # Формируем полный путь к файлу изображения на основе названия метки
        image_file_jpg = os.path.join(image_folder, os.path.splitext(label_file)[0] + '.jpg')
        image_file_png = os.path.join(image_folder, os.path.splitext(label_file)[0] + '.png')

        # Проверяем существование файла изображения .jpg или .png
        if os.path.exists(image_file_jpg):
            image_file = image_file_jpg
        elif os.path.exists(image_file_png):
            image_file = image_file_png
        else:
            print(f"Файл изображения для метки {label_file} не найден.")
            continue

        # Копируем файл метки в папку вывода
        shutil.copy(os.path.join(label_folder, label_file), os.path.join(output_folder, label_file))
        print(f"Копирован файл метки для изображения {image_file}")

# Пример использования:
label_folder = r"D:\Learning\UII\DataSets\DataSet_2.1_Train_Valid\train\labels"
image_folder = r"D:\Learning\UII\DataSets\DataSet_2.1_Train_Valid\HighClasses\medium\train\images"
output_folder = r"D:\Learning\UII\DataSets\DataSet_2.1_Train_Valid\HighClasses\medium\train\labels"

copy_label_files(label_folder, image_folder, output_folder)
