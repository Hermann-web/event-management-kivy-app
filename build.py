#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Application build

import shutil
import subprocess
from pathlib import Path


def clean_pkg_dir(pkg_dir: Path):
    # remove all files and directories from pkg
    if not pkg_dir.exists():
        pkg_dir.mkdir()
        return
    # try:
    #     shutil.rmtree(pkg_dir)
    #     pkg_dir.mkdir()
    # except Exception as e:
    #     print(f"Failed to delete {pkg_dir}. Reason: {e}")


if __name__ == "__main__":
    PKG_DIR = Path("pkg")
    SPEC_FILE = "main.spec"
    APP_NAME = ""

    # clean pkg directory
    clean_pkg_dir(PKG_DIR)

    # run pyinstaller in pkg directory
    # subprocess.run(['pyinstaller', '--name=Event Management System', f'..\{SPEC_FILE}'], cwd=PKG_DIR)
    subprocess.run(['pyinstaller', f'..\{SPEC_FILE}'],
                   cwd=PKG_DIR,
                   check=False)

    main_file = PKG_DIR / "dist" / "main.exe"  #main_file= os.path.join(PKG_DIR, "dist\main.exe")
    print(f"the file can be found in {main_file}")
