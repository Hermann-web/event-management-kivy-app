import os
import shutil
import subprocess



def clean_pkg_dir(pkg_dir):
    # remove all files and directories from pkg
    for filename in os.listdir(pkg_dir):
        file_path = os.path.join(pkg_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    PKG_DIR = "pkg"
    SPEC_FILE = "main.spec"
    APP_NAME = ""

    # clean pkg directory
    clean_pkg_dir(PKG_DIR)

    # run pyinstaller in pkg directory
    subprocess.run(['pyinstaller', '--name=Event Management System', f'..\{SPEC_FILE}'], cwd=PKG_DIR)
    
    main_file= os.path.join(PKG_DIR, "dist\main.exe")
    print(f"the file can be found in {main_file}")
