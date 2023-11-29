import os
import shutil
import random

# Укажите путь к вашему каталогу train и valid
train_dir = 'E:/cabbageDopBig_yolov8/train'
valid_dir = 'E:/cabbageDopBig_yolov8/valid'

# Директории изображений и меток внутри train
train_images_dir = os.path.join(train_dir, 'images')
train_labels_dir = os.path.join(train_dir, 'labels')

# Если каталоги valid не существуют, создайте их
os.makedirs(os.path.join(valid_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(valid_dir, 'labels'), exist_ok=True)

# Директории изображений и меток внутри valid
valid_images_dir = os.path.join(valid_dir, 'images')
valid_labels_dir = os.path.join(valid_dir, 'labels')

# Получите список всех файлов изображений в каталоге train/images
image_files = [f for f in os.listdir(train_images_dir) if f.endswith('.png')]

# Перемешайте список файлов изображений
random.shuffle(image_files)

# Определите количество файлов для перемещения (20% от total)
num_to_move = int(len(image_files) * 0.2)

# Выберите файлы для перемещения
files_to_move = image_files[:num_to_move]

# Переместите выбранные файлы изображений и файлы аннотаций
for image_file in files_to_move:
    # Перемещение файла изображения
    shutil.move(os.path.join(train_images_dir, image_file), os.path.join(valid_images_dir, image_file))

    # Определение имени файла аннотации (предполагая, что расширение файла аннотации .txt)
    annotation_file = image_file.replace('.png', '.txt')

    # Перемещение файла аннотации
    shutil.move(os.path.join(train_labels_dir, annotation_file), os.path.join(valid_labels_dir, annotation_file))

print(f'Moved {num_to_move} image and annotation pairs to {valid_dir}')
