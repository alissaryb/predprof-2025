import os

def count_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        file_count = sum(1 for file in files if os.path.isfile(os.path.join(directory, file)))
        return file_count
    except Exception as e:
        print(f"Ошибка: {e}")
        return 0
