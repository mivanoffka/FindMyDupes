import copy
import time
from typing import Optional

from dupes import *
import threading

result: Optional[list] = None


def start():
    global result

    while True:
        print("Folder path:   ", end="")
        path_str = input()

        finder = DupeFinderByPhash(ImageFolder(path_str))

        threading.Thread(target=search, args=(finder,)).start()

        while result is None:
            print(f"{round(finder.progress * 100, 3)}%")
            time.sleep(1)

        groups = copy.copy(result)
        result = None

        if groups is not None:
            if len(groups) > 0:
                print(f"\nA total of {len(groups)} duplicate groups found.")
                for i, group in enumerate(groups):
                    files_str = "   "
                    for path in group:
                        files_str += path.name + ", "
                    if len(files_str) > 2:
                        files_str = files_str[:-2]
                    print(f"   [{i+1}] {files_str}")
            else:
                print(f"No duplicates found")

        print("\nDo you wish to continue? (Y/n)")

        should_continue = input()

        if should_continue.lower() != "y":
            print("\nGoodbye!")
            break


def search(finder: DupeFinder):
    global result
    result = finder.start_searching()


if __name__ == "__main__":
    start()
