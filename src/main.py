import os
import shutil

from copy_static import copy_static
from generate_page import generate_page

PUBLIC_DIR = "public"
STATIC_DIR = "static"


def main() -> None:
    if not os.path.exists(STATIC_DIR):
        raise FileNotFoundError(f"'{STATIC_DIR}' directory to copy from is not found")

    if os.path.exists(PUBLIC_DIR):
        print(f"EXISTS: '{PUBLIC_DIR}'")
        shutil.rmtree(PUBLIC_DIR)
        print(f"RMTREE: '{PUBLIC_DIR}'")
    os.mkdir(PUBLIC_DIR)
    print(f"MKDIR: '{PUBLIC_DIR}'")
    copy_static(STATIC_DIR, PUBLIC_DIR)

    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
