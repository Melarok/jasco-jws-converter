import os
from os import listdir, chdir
import olefile as ofio
from struct import unpack
from tkinter import *
from tkinter import filedialog, messagebox


class JwsHeader:
    def __init__(self, channel_number, point_number,
                 x_for_first_point, x_for_last_point, x_increment,header_names,
                 data_size=None):
        self.channel_number = channel_number
        self.point_number = point_number
        self.x_for_first_point = x_for_first_point
        self.x_for_last_point = x_for_last_point
        self.x_increment = x_increment
        #only defined if this is the header of a v1.5 jws file
        self.data_size = data_size
        self.header_names = header_names

def data_definitions(x):
    return {
        268435715:"WAVELENGTH",
        4097:"CD",
        8193:"HT VOLTAGE",
        3:"ABSORBANCE",
        14:"FLUORESCENCE"
    }.get(x,'undefined')

def _unpack_ole_jws_header(data):
    try:
        data_tuple = unpack('<LLLLLLddd', data[0:48])
        channels = data_tuple[3]
        nxtfmt = '<L'+'L'*channels
        header_names = list(unpack(nxtfmt, data[48:48+4*(channels+1)]))
        for i,e in enumerate(header_names):
            header_names[i] = data_definitions(e)
        data_tuple += tuple(header_names)
        lastPos = 48+4*(channels+1)
        nxtfmt = '<LLdddd'
        for pos in range(channels):
            data_tuple = data_tuple + unpack(nxtfmt, data[lastPos:lastPos+40])
        return JwsHeader(data_tuple[3], data_tuple[5],
                         data_tuple[6], data_tuple[7], data_tuple[8],header_names)

    except:
        return messagebox.showinfo(title="Error", message="Could not read DataInfo from jws header")

def select_folder():
    global infolder

    infolder = filedialog.askdirectory(title="Select the folder containing .jws files to be converted")
    pathExists = os.path.exists(infolder)
    if not pathExists:
        return messagebox.showinfo(title="Error", message="Could not open input directory. Please try another one.")
    else:
        text.insert(INSERT, f"Selected path {infolder} as input directory\n")
        return infolder

def convert(infolder):
    folders_found=[z for z in listdir(infolder) if os.path.isdir(f"{infolder}/{z}") == True]
    for foldername in folders_found:
        #text.insert(INSERT, f"Entering folder {foldername}\n")
        
        if os.path.exists(f"{infolder}/{foldername}/csv") != True: os.makedirs(f"{infolder}/{foldername}/csv")

        files_found=[x for x in listdir(f"{infolder}/{foldername}") if x.lower().endswith(".jws")]
        if files_found.__len__() == 0: text.insert(INSERT, f"No .jws files found in folder {infolder}/{foldername}. Continuing.\n")
        for filename in files_found:
            #text.insert(INSERT, f"Found file {infolder}/{foldername}/{filename}\n")
            chdir(f"{infolder}/{foldername}")
            with open(filename,"rb") as f:
                #text.insert(INSERT, f"Opend file {infolder}/{foldername}/{filename}\n")
                f.seek(0)
                oleobj = ofio.OleFileIO(f)
                data = oleobj.openstream('DataInfo')
                header_data = data.read()
                header_obj = _unpack_ole_jws_header(header_data)
                fmt = 'f' * header_obj.point_number*header_obj.channel_number
                values = unpack(fmt, oleobj.openstream('Y-Data').read())
                chunks = [values[x:x + header_obj.point_number] for x in range(0, len(values), header_obj.point_number)]

            chdir(f"{infolder}/{foldername}/csv")
            new_filename = filename.rstrip("jws")+"csv"
            if os.path.exists(f"{infolder}/{foldername}/csv/{new_filename}") != True:
                with open(filename.rstrip("jws")+"csv","w") as r:
                    r.write( ",".join(str(x) for x in header_obj.header_names))
                    r.write("\n")
                    for line_no in range(header_obj.point_number):
                        r.write(str(header_obj.x_for_first_point+line_no*header_obj.x_increment))
                        r.write(",")
                        for c in range(header_obj.channel_number):
                            r.write(str(chunks[c][line_no]))
                            r.write(",")
                        r.write('\n')
                    text.insert(INSERT, f"Written file {infolder}/{foldername}/csv/{new_filename}\n")
            else: text.insert(INSERT, f"File {infolder}/{foldername}/{new_filename} already exists, not overwriting!\n")


root = Tk()
root.title(".jws to .csv converter")

Button(root, text="Select the folder containing .jws files", command=lambda: select_folder()).pack(padx=10, pady=5)
Button(root, text="Convert .jws to .csv", command=lambda: convert(infolder)).pack(padx=10, pady=5)
Button(root, text="Quit", command=root.quit).pack(padx=10, pady=5)
text = Text(root, width=150, height=20)
text.pack(padx=10, pady=5)

root.mainloop()