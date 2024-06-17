from dupes import *


def start():
    while True:
        print("Folder path:   ", end="")
        path_str = input()

        finder = HashDupeFinder(ImageFolder(path_str))
        groups = finder.start_searching()

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


if __name__ == "__main__":
    start()
