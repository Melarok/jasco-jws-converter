import tkinter
from tkinter import filedialog
from tkinter import ttk, BOTH
from tkinter.ttk import Frame, Button, Style
from tkinter import messagebox
import os
from os import chdir, listdir, makedirs

class Window(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.style = Style()
        self.style.theme_use("default")

        self.master.title("Quit button")
        self.pack(fill=BOTH, expand=1)

        open_input_button = Button(self, text="Select the folder containing .jws files to be converted", command=select_folder("Select input folder", True))
        open_input_button.pack(expand=True)
        open_input_button.place(x=20, y=20)

        open_output_button = Button(self, text="Select the folder where the .csv files should be saved", command=select_folder("Select output folder", False))
        open_output_button.pack(expand=True)
        open_output_button.place(x=20, y=60)

        convert_button = Button(self, text="Convert .jws to .csv", command=convert)
        convert_button.pack(expand=True)
        convert_button.place(x=20, y=100)

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.pack(expand=True)
        quit_button.place(x=20, y=140)

def select_folder(title_text,is_in):
    folder = filedialog.askdirectory(title=title_text)
    messagebox.showinfo(title="Selected a folder", message=folder)

def convert():
    lol = 1

def main():
    root = tkinter.Tk()
    root.title('Tkinter Open File Dialog')
    root.resizable(False, False)
    root.geometry('360x180')
    app = Window()
    root.mainloop()

if __name__ == '__main__':
    main()


