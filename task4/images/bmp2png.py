from PIL import Image
import os

for file in os.listdir('.'):
    if file.endswith('.bmp'):
        Image.open(file).save(file.replace('.bmp', '.png'))
