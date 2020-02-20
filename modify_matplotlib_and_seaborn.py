# -*- coding: utf-8 -*-

"""
modify_matplotlib_and_seaborn.py

解决 matplotlib 和 seaborn 中文显示问题

@author: Wu Yudi
@email: wuyd@swsresearch.com
@date: 2020.02.12
"""

import os
import sys

def modify_matplotlib_and_seaborn(font="Microsoft YaHei Mono"):
    anaconda_path = [p for p in sys.path if p.endswith("Anaconda3")][0]
    pkgs_path = os.path.join(anaconda_path, "pkgs")

    matplotlib_folder = seaborn_folder = None
    for folder in os.listdir(pkgs_path):
        if folder.startswith("matplotlib"):
            matplotlib_folder = folder
        elif folder.startswith('seaborn'):
            seaborn_folder = folder

    assert matplotlib_folder is not None
    assert seaborn_folder is not None

    # modify matplotlib

    matplotlib_rcsetup = os.path.join(pkgs_path, matplotlib_folder, "Lib\\site-packages\\matplotlib\\rcsetup.py")

    with open(matplotlib_rcsetup, 'r') as file:
        data = file.readlines()
        
    for i, line in enumerate(data):
        if 'font.sans-serif' in line:
            if font not in line:
                data[i] = line.replace("[[", "[['{}', ".format(font))
            break

    with open(matplotlib_rcsetup, 'w') as file:
        file.writelines(data)

    print("Add [{}] into {} successfully!".format(font, matplotlib_rcsetup))

    # modify seaborn

    seaborn_rcmod = os.path.join(pkgs_path, seaborn_folder, "site-packages\\seaborn\\rcmod.py")

    with open(seaborn_rcmod, 'r') as file:
        data = file.readlines()

    for i, line in enumerate(data):
        if 'font.sans-serif\": [' in line:
            if font not in line:
                data[i] = line.replace(": [", ": [\"{}\", ".format(font))
            break

    with open(seaborn_rcmod, 'w') as file:
        file.writelines(data)

    print("Add [{}] into {} successfully!".format(font, seaborn_rcmod))


if __name__ == "__main__":
    modify_matplotlib_and_seaborn()
