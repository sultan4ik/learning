import os
from PIL import Image


def converting_images(input_path: str, output_path: str):
    for tif_image in os.listdir(path=input_path):
        if 'tif' in tif_image:
            with Image.open(os.path.join(input_path, tif_image)) as image:
                dpi = image.info.get('dpi')
                icc_profile = image.info.get('icc_profile')
                new_file_name = f'new_{tif_image.replace("tif", "jpg")}'
                image.save(fp=os.path.join(output_path, new_file_name),
                           dpi=dpi,
                           quality=100,
                           format='JPEG',
                           icc_profile=icc_profile)
            print(f'Конвертирование {tif_image} готово!')


def main():
    converting_images(input_path='/Users/artursultanbaev/ирина/converter/tif_files',
                      output_path='/Users/artursultanbaev/ирина/converter/jpg_files')


if __name__ == '__main__':
    main()
