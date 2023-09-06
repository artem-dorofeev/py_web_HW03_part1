import sys
from pathlib import Path
import os
# import uuid
import shutil
from time import time
from threading import Thread
import logging

from main_hw06_normalize import normalize

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


CATEGORIES = {"Audio": [".mp3", ".aiff", ".m3u"],
              "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".xls"],
              "Photo": [".jpg", ".raw", ".nef"],
              "Video": [".avi", ".mp4", ".mkv"],
              "Archives": [".zip", ".rar", ".tar", ".gz"]}

LIST_FOLDERS_SORT = ("Audio", "Documents", "Photo",
                     "Video", "Other", "Archives")

count_files = 0
count_unpack_arch = 0
count_del_folder = 0


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    index = None
    if new_name.exists():
        index = len([f for f in target_dir.glob(
            "*") if new_name.stem in f.stem])
    new_name = new_name.with_name(
        f"{new_name.stem}{index if index else ''}{file.suffix}")
    file.rename(new_name)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path, destination_path: Path) -> None:
    global count_files
    for item in path.glob("**/*"):
        if item.is_file():
            count_files += 1
            category = get_categories(item)
            move_file(item, destination_path, category)


def del_emppty_folders(path: Path) -> None:
    global count_del_folder
    for item in path.iterdir():
        if item.name not in LIST_FOLDERS_SORT:

            if item.is_dir():
                del_emppty_folders(item)
                try:
                    item.rmdir()
                    count_del_folder += 1
                except OSError:
                    print(f'folder {item.name} is not emppty')
                    continue

            continue


def upack_archive(path: Path) -> None:
    global count_unpack_arch
    arch_path = path.joinpath("Archives")
    if not arch_path.exists():
        arch_path.mkdir()
    for item in arch_path.iterdir():
        output_arch = arch_path.joinpath(item.stem)
        output_arch.mkdir()
        shutil.unpack_archive(item, output_arch)
        item.unlink()
        count_unpack_arch += 1


def main():
    global count_files
    global count_del_folder
    global count_unpack_arch

    st_time = time()

    logging.debug("\nProgramm Started")

    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} dos`n exists."
    
    items = os.listdir(path)

    threads = []
    i = 1
    for item in items:
        item_path = os.path.join(path, item)
        item_path = Path(item_path)
        if os.path.isdir(item_path):
            thread = Thread(
                name=f"thread0{i}", target=sort_folder, args=(item_path, path)
            )
            logging.debug(f"{thread.name} Started")
            i += 1
            threads.append(thread)
            thread.start()

        else:
            category = get_categories(item_path)
            move_file(item_path, path, category)

    for thread in threads:
        thread.join()

    del_emppty_folders(path)
    print(f'Deleted - {count_del_folder} folder')
    upack_archive(path)
    print(f'Unpack - {count_unpack_arch} archive and delete files')

    end_time = time()
    delta_time = end_time - st_time

    return f"All ok, time work - {delta_time}"


if __name__ == "__main__":
    print(main())

