import zipfile
import os

def make_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, "w") as zf:
        for f in files:
            if os.path.exists(f):
                zf.write(f, os.path.basename(f))
    return zip_path

