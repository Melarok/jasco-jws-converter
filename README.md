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
- run "python jws_to_csv.py" from a terminal
- select the folder which contains your .jws files
- your .csv files will be in the folder you selected earlier
