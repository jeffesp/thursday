import shutil
import sys
import os
from pathlib import Path
from pprint import pprint


def order(dir): 
    source_files = os.listdir(dir)
    names = map(lambda x: (x, x[3:]), source_files)
    files = sorted(names, key=lambda x: x[1])

    os.mkdir('./renamed')

    for f in zip(files, range(1, len(source_files)+1)):
        shutil.copy2(Path(f[0][0]), Path(os.path.join('./renamed', f'{f[1]:02d}_{f[0][1]}')))


if __name__ == "__main__":
    order(sys.argv[1])
