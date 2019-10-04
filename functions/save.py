from pathlib import Path, PurePath, PureWindowsPath
import platform
import time
import os


def getDownloadPath():
    date = time.strftime("%Y_%m_%d")
    end = os.path.join("Downloads", "contract" + "_" + str(date) + ".pdf")
    user = Path.home()
    downloads = str(PurePath(user).joinpath(end))
    windows_downloads = str(PureWindowsPath(user).joinpath(end))
    if platform.system() == "Windows":
        return windows_downloads
    else:
        return downloads
