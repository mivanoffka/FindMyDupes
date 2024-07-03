import shutil
import os


def create_or_clear_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    except Exception as e:
        print(f'Unable to clear or create {folder_path}: {e}')


def copy_files(src_folder, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)

        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
