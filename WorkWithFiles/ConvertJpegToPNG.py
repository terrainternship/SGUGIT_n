from PIL import Image
import os

def convert_images(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".jpeg") or filename.endswith(".jpg"):
            img = Image.open(os.path.join(input_directory, filename))
            png_filename = os.path.splitext(filename)[0] + '.png'
            img.save(os.path.join(output_directory, png_filename))

# Укажите путь к каталогу, в котором находятся ваши изображения в формате JPEG
input_directory = "D:\\Учеба\\УИИ\\Стажировка\\cabbageFind.v1i.yolov8\\train\\images"
# Укажите путь к каталогу, в который следует сохранить изображения в формате PNG
output_directory = "D:\\Учеба\\УИИ\\Стажировка\\cabbageFind.v1i.yolov8\\train\\images_png"

convert_images(input_directory, output_directory)
