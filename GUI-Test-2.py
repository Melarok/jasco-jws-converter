import os
import tkinter
import tkinter.filedialog
import tkinter.ttk

root = tkinter.Tk()
root.title(".jws to .csv converter")

def select_folder(is_in):
    if is_in == True:
        infolder = tkinter.filedialog.askdirectory(title="Select the folder containing .jws files to be converted")
        pathExists = os.path.exists(infolder)
        if not pathExists:
            return tkinter.messagebox.showinfo(title="Error", message="Could not open input directory. Please try another one.")
        else:
            display_text.insert("1.0", f"Selected path {infolder} as input directory")
    else:
        outfolder = filedialog.askdirectory(title="Select the folder where the .csv files should be saved")
        pathExists = os.path.exists(outfolder)
        if not pathExists:
            print("Output directory does not exist. Trying to create it ...")
            try:
                os.makedirs(outfolder)
                print("Output directory was created!")
            except:
                exit("Output directory could not be created! Exiting now.")

        return messagebox.showinfo(title="Status", message="Selected output folder")

def convert():




    return messagebox.showinfo(title="Status", message="Conversion successfull!")

tkinter.Button(root, text="Select the folder containing .jws files to be converted", command=lambda: select_folder(True)).pack(padx=10, pady=5)
tkinter.Button(root, text="Select the folder where the .csv files should be saved", command=lambda: select_folder(False)).pack(padx=10, pady=5)
tkinter.Button(root, text="Convert .jws to .csv", command=convert).pack(padx=10, pady=5)
tkinter.Button(root, text="Quit", command=root.quit).pack(padx=10, pady=5)

display_text = tkinter.Text(root, width=60, height=5).pack(padx=10, pady=5)

root.mainloop()