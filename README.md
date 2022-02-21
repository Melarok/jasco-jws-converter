# Jasco .jws to .csv converter
This project aims to read jws files obtained from Jasco spectrometers and batch convert them to csv files.

## Dependencies
This project uses Python 3 and depends on the tkinter and the olefile python module

### Arch
```shell
# pacman -Syu tk
# pip install olefile
```

### Ubuntu / Debian
```shell
# apt install python3-tk
# pip install olefile
```

## How to use it
- clone this repository
- run "python jws-to-csv.py" from a terminal
- follow the GUI

## Credits
This Project is forked from https://github.com/odoluca/jasco_jws_reader and uses it's binary data extraction and conversion capability.
I basically ported it to Python 3, added the ability to choose an output folder and switched to a GUI for easier usage.