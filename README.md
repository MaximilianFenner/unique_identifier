# unique_identifier

A small tool for **Path of Exile** that helps you spot valuable unique items on the ground while hovering over them.  
Never miss a good unique again!

---

## Supported Resolutions
- Tested: **3440x1440**  
- Likely works: **2560x1440** (not verified)  
- Other resolutions (1080p, 4K) are untested - use at your own risk.  

---

## Usage
1. Clone the repository.  
2. Run `main_unique_identifier.py`.  
3. The script should auto-detect your resolution.  
4. A preview window shows whether unidentified items are recognized.
5. If items are not properly shown in the rectangle you can try to adjust the values by yourself at line ~77; change x and y to fit your resolution.
   `monitor = {'top': int(screensize[1] * windows_scaling - y), 'left': int(screensize[0] * windows_scaling - x), 'width': scale_width_new + 10, 'height': scale_height_new + 10}`

The required item images and sound file are stored in the `assets/` directory.

For compatibility reasons **playsound** needs to be on version 1.2.2.

When the script starts, it checks for the required Python packages and
automatically installs any that are missing. The installation uses the
currently selected Python interpreter and may require internet access.
