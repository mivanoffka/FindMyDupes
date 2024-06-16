from dupes import *


def start():
    while True:
        print("Folder path:   ", end="")
        path_str = input()

        hash_finder = HashDupeFinder()
        groups = hash_finder.start_searching(ImageFolder(path_str))

        if len(groups) > 0:
            print(f"A total of {len(groups)} duplicate groups found.")
            for i, group in enumerate(groups):
                print(f"   ({i+1})")
                for path in group:
                    print(f"      {path}")
        else:
            print(f"No duplicates found")


if __name__ == "__main__":
    start()
