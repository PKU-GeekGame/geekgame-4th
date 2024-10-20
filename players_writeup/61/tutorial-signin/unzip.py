# https://blog.csdn.net/acs04600/article/details/101645414

# -*- coding: utf-8 -*-
# 2019/8/13 14:57
import zipfile
import os

def unzip_file(path):
    '''解压zip包'''

    if os.path.exists(path):
        if path.endswith('.zip'):
            z = zipfile.ZipFile(path, 'r')
            unzip_path = os.path.split(path)[0]
            z.extractall(path=unzip_path)
            zip_list = z.namelist() # 返回解压后的所有文件夹和文件
            for zip_file in zip_list:
                new_path = os.path.join(unzip_path,zip_file)
                unzip_file(new_path)
        elif os.path.isdir(path):
            for file_name in os.listdir(path):
                unzip_file(os.path.join(path, file_name))
    else:
        print('the path is not exist!!!')


if __name__ == '__main__':
    unzip_file("./tutorial-signin.zip")