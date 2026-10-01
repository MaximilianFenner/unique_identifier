import os
import sys
import ctypes
import importlib.util
import subprocess


REQUIRED_PACKAGES = {
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'mss': 'mss',
    'playsound': 'playsound==1.2.2',
}


def install_missing_packages():
    """Install dependencies that are not available in the current interpreter."""
    if getattr(sys, 'frozen', False):
        return

    missing_packages = [
        package
        for module, package in REQUIRED_PACKAGES.items()
        if importlib.util.find_spec(module) is None
    ]

    if not missing_packages:
        return

    print(f'Installing missing packages: {", ".join(missing_packages)}')
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', *missing_packages]
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise RuntimeError(
            'Could not install the required Python packages. '
            'Install them manually with: '
            f'{sys.executable} -m pip install {" ".join(missing_packages)}'
        ) from error


install_missing_packages()

import cv2 as cv
import numpy as np
import mss
from playsound import playsound


bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
assets_dir = os.path.join(bundle_dir, 'assets')
path_to_headhunter = os.path.abspath(os.path.join(assets_dir, 'Headhunter.png'))
path_to_Mageblood = os.path.abspath(os.path.join(assets_dir, 'Mageblood.png'))
path_to_Soundfile = os.path.abspath(os.path.join(assets_dir, 'Meme_money.mp3'))


# get screen resolution and scaling factor
user32 = ctypes.windll.user32
screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
windows_scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
print(f'Windows scaling is set to {windows_scaling * 100}%')


flag_ultrawide = False
flag_1080p = False
flag_1440p = False
flag_4k = False


if screensize[0] * windows_scaling == 2560 or screensize[0] * windows_scaling == 3440:
    flag_ultrawide = True
    print('Ultrawide active')


if int(screensize[1] * windows_scaling) == 1080:
    flag_1080p = True
    print('1080p active')
elif int(screensize[1] * windows_scaling) == 1440:
    flag_1440p = True
    print('1440p active')
elif int(screensize[1] * windows_scaling) == 2160:
    flag_4k = True
    print('4k active')
else:
    print('Currently following Resolutions are supported: 1920x1080, 2560x1440, 2560x1080 and 3440x1440.')


# original image dimensions
scale_width = 200
scale_heigth = 100

# loading images.
img_Headhunter = cv.imread(path_to_headhunter)
img_Mageblood = cv.imread(path_to_Mageblood)


# resizing images based on screen resolution
if flag_1080p == True:
    scale_width_new = int(scale_width * 0.50)
    scale_height_new = int(scale_heigth * 0.50)

if flag_1440p == True:
    scale_width_new = int(scale_width * 0.66)
    scale_height_new = int(scale_heigth * 0.66)

img_Headhunter = cv.resize(img_Headhunter, (scale_width_new, scale_height_new), interpolation=cv.INTER_LINEAR)
img_Mageblood = cv.resize(img_Mageblood, (scale_width_new, scale_height_new), interpolation=cv.INTER_LINEAR)


# gray conversion for faster template matching
hh_gray = cv.cvtColor(img_Headhunter, cv.COLOR_BGR2GRAY)
mb_gray = cv.cvtColor(img_Mageblood, cv.COLOR_BGR2GRAY)

print('Checking for Belts! Make sure the splash art is visible in the preview window when hovering over Belts.')

# screen capture setup
with mss.mss() as sct:
    # 1080p
    if flag_1080p == True:
        monitor = {'top': int(screensize[1] * windows_scaling - 400), 'left': int(screensize[0] * windows_scaling - 410), 'width': scale_width_new + 10, 'height': scale_height_new + 10} # untested
    # 1440p
    elif flag_1440p == True:
        monitor = {'top': int(screensize[1] * windows_scaling - 520), 'left': int(screensize[0] * windows_scaling - 530), 'width': scale_width_new + 10, 'height': scale_height_new + 10} # only Ultrawide tested
    # 4k
    elif flag_4k == True:
        monitor = {'top': int(screensize[1] * windows_scaling - 800), 'left': int(screensize[0] * windows_scaling - 820), 'width': scale_width_new + 10, 'height': scale_height_new + 10} # untested

    while True:
        img = np.array(sct.grab(monitor))
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        hh_match = cv.matchTemplate(img_gray, hh_gray, cv.TM_CCOEFF_NORMED)
        mb_match = cv.matchTemplate(img_gray, mb_gray, cv.TM_CCOEFF_NORMED)
        
        if np.any(hh_match > 0.7):
            print('Headhunter!')
            playsound(path_to_Soundfile)
        if np.any(mb_match > 0.7):
            print('Mageblood!')
            playsound(path_to_Soundfile)
        cv.imshow('OpenCV/Numpy grayscale', cv.cvtColor(img, cv.COLOR_BGRA2GRAY))
        if cv.waitKey(25) & 255 == ord('q'):
            cv.destroyAllWindows()
            break
