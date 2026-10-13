import os
import shutil


def copy_static(source_dir: str, destination_dir: str) -> None:
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
            copy_static(source, destination)
        else:
            shutil.copy(source, destination)
            print(f"COPY: from '{source}' to '{destination}'")
