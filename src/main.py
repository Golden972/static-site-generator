import os
import shutil
import sys

from copy_static import copy_static
from generate_page import generate_pages_recursive

PUBLIC_DIR = "docs"
STATIC_DIR = "static"
CONTENT_DIR = "content"
TEMPLATE = "template.html"


def main() -> None:
    if len(sys.argv) != 0:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    if not os.path.exists(STATIC_DIR):
        raise FileNotFoundError(f"'{STATIC_DIR}' directory to copy from is not found")

    if os.path.exists(PUBLIC_DIR):
        print(f"EXISTS: '{PUBLIC_DIR}'")
        shutil.rmtree(PUBLIC_DIR)
        print(f"RMTREE: '{PUBLIC_DIR}'")
    os.mkdir(PUBLIC_DIR)
    print(f"MKDIR: '{PUBLIC_DIR}'")
    copy_static(STATIC_DIR, PUBLIC_DIR)

    generate_pages_recursive(CONTENT_DIR, TEMPLATE, PUBLIC_DIR, basepath)


if __name__ == "__main__":
    main()
