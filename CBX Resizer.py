import os, sys
import subprocess
from glob     import glob
from shutil   import copy2, rmtree
from PIL      import Image
from zipfile  import ZipFile, ZIP_DEFLATED

def resized_image(_image, _path, _height):
    _full_path =_path+'\\'+_image
    if '.png' in _image or '.jpg' in _image or 'jpeg' in _image:
        image = Image.open(_full_path)

        ratio = (_height/ float(image.size[1]))
        width = int( float(image.size[0]) * float(ratio) )

        resized_image = image.resize((width,_height), Image.LANCZOS)

        print ('File {} has been resized.'.format(_image))

        if os.path.exists(_full_path):
            os.remove(_full_path)
        resized_image.save(_full_path)
    return _full_path

def delete_sub_folder(_path):
    if glob(_path+'/*/') != []:
        sub_dir = glob(_path+'/*/')[0]
        list_of_sub_files = sorted(filter(lambda x: os.path.isfile(os.path.join(sub_dir,x)), os.listdir(sub_dir)))

        for sub_file in list_of_sub_files:
            copy2(sub_dir+sub_file, _path)
            print('File {} was copied out of sub folder.'.format(sub_file))

        if os.path.exists(sub_dir):
            rmtree(sub_dir)
            print()
            print('Sub folder {} has been deleted.'.format(sub_dir))

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    unrar_dir = sys._MEIPASS+'\\UnRAR.exe'

current_dir = os.getcwd()
list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(current_dir,x)), os.listdir(current_dir)))
fixed_height = 2000

print('Current directory: {}'.format(current_dir))
print()


for file_name in list_of_files:
    if file_name.endswith('.cbz') or file_name.endswith('cbr'):
        print('Extracting', file_name)
    else: continue
    if file_name.endswith('_resized.cbz'): continue

    temp_file_name = file_name.replace('.cbz','')
    temp_file_name = temp_file_name.replace('.cbr','')
    temp_path = current_dir+'\\'+temp_file_name

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
        print('Temporary {} folder created.'.format(temp_file_name))

    if file_name.endswith('cbz'):
        with ZipFile(file_name) as zip_file:
            zip_file.extractall(temp_path)
        print('File {} has been extracted.'.format(temp_file_name))
    elif file_name.endswith('cbr'):
        subprocess.call([unrar_dir, 'e', file_name ,temp_path])
        print('File {} has been extracted.'.format(temp_file_name))
    else:
        print('File {} is not a CBX'.format(file_name))
    print()

    delete_sub_folder(temp_path)

    image_files = sorted(filter(lambda x: os.path.isfile(os.path.join(temp_path, x)), os.listdir(temp_path)))

    with ZipFile(temp_path+'_resized.cbz', 'w') as zip_file:
        for img in image_files:
            zip_file.write( resized_image(img, temp_path, fixed_height), compress_type=ZIP_DEFLATED)
            print('File {} has been compressed.'.format(img))

    rmtree(temp_path)
    print('Temporary folder {} has been deleted'.format(temp_file_name))

    print()
