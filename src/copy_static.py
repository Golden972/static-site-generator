import os
import shutil

PUBLIC_DIR = "./public"
STATIC_DIR = "./static"


def copy_static() -> None:
    if not os.path.exists(STATIC_DIR):
        raise FileNotFoundError(f"'{STATIC_DIR}' directory to copy from is not found")

    if os.path.exists(PUBLIC_DIR):
        print(f"EXISTS: '{PUBLIC_DIR}'")
        shutil.rmtree(PUBLIC_DIR)
        print(f"RMTREE: '{PUBLIC_DIR}'")
    os.mkdir(PUBLIC_DIR)
    print(f"MKDIR: '{PUBLIC_DIR}'")

    def copy_recursively(source_dir: str, destination_dir: str) -> None:
        dir_entries = os.listdir(source_dir)
        if len(dir_entries) == 0:
            return
        for entry in dir_entries:
            source = os.path.join(source_dir, entry)
            destination = os.path.join(destination_dir, entry)
            if not os.path.isfile(source):
                if not os.path.isdir(source):
                    raise ValueError(f"Specified path {source} is not a file or directory")
                os.mkdir(destination)
                print(f"MKDIR: '{destination}'")
                copy_recursively(source, destination)
            else:
                shutil.copy(source, destination)
                print(f"COPY: from '{source}' to '{destination}'")

    copy_recursively(STATIC_DIR, PUBLIC_DIR)
