import os

def get_files(path, ext):
    # Список файлов
    files = os.listdir(path)
    # Только файлы с расширением .py
    files = [file for file in files if file.endswith(ext)]
    for i in range(0, len(files)):
        # Удаляем расширение
        files[i] = os.path.splitext(files[i])[0]
    return files

def get_py_files(path):
    return get_files(path, '.py')