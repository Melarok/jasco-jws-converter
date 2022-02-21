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

def select_folder(is_in):
    global infolder
    global outfolder

    if is_in == True:
        infolder = filedialog.askdirectory(title="Select the folder containing .jws files to be converted")
        pathExists = os.path.exists(infolder)
        if not pathExists:
            return messagebox.showinfo(title="Error", message="Could not open input directory. Please try another one.")
        else:
            text.insert(INSERT, f"Selected path {infolder} as input directory\n")
            return infolder
    else:
        outfolder = filedialog.askdirectory(title="Select the folder where the .csv files should be saved")
        pathExists = os.path.exists(outfolder)
        if not pathExists:
            text.insert(INSERT, "Output directory does not exist. Trying to create it ...\n")
            try:
                os.makedirs(outfolder)
                text.insert(INSERT, "Output directory was created!\n")
                text.insert(INSERT, f"Selected path {outfolder} as output directory\n")
                return outfolder
            except:
                return messagebox.showinfo(title="Error", message="Output directory could not be created! Please select another one.")
        else:
            text.insert(INSERT, f"Selected path {outfolder} as output directory\n")
            return outfolder

def _unpack_ole_jws_header(data):
    try:
        data_tuple = unpack('<LLLLLLddd', data[0:48])
        # print(data_tuple)
        channels = data_tuple[3]
        nxtfmt = '<L'+'L'*channels
        header_names = list(unpack(nxtfmt, data[48:48+4*(channels+1)]))

        for i,e in enumerate(header_names):
            header_names[i] = data_definitions(e)


        data_tuple += tuple(header_names)
        # print(header_names)
        # print(data_tuple)

        lastPos = 48+4*(channels+1)
        nxtfmt = '<LLdddd'
        for pos in range(channels):
            data_tuple = data_tuple + unpack(nxtfmt, data[lastPos:lastPos+40])
            # print(data_tuple)

        # print(data_tuple[9:13])
        # I have only found spectra files with 1 channel
        # So we will only support 1 channel per file, at the moment
        return JwsHeader(data_tuple[3], data_tuple[5],
                         data_tuple[6], data_tuple[7], data_tuple[8],header_names)
    except:
        return messagebox.showinfo(title="Error", message="Could not read DataInfo from jws header")

def convert(infolder, outfolder):
    files_found=[x for x in listdir(infolder) if x.lower().endswith(".jws")]
    if files_found.__len__() == 0: return messagebox.showinfo(title="Error", message="No .jws files found in input folder. Please select another one.")
    for filename in files_found:
        chdir(infolder)
        with open(filename,"rb") as f:
            # print(f.read(4))
            f.seek(0)
            oleobj = ofio.OleFileIO(f)
            data = oleobj.openstream('DataInfo')
            header_data = data.read()
            header_obj = _unpack_ole_jws_header(header_data)
            # print(header_obj.point_number,header_obj.channel_number)
            # print(oleobj.openstream('Y-Data').read())
            fmt = 'f' * header_obj.point_number*header_obj.channel_number
            values = unpack(fmt, oleobj.openstream('Y-Data').read())
            chunks = [values[x:x + header_obj.point_number] for x in range(0, len(values), header_obj.point_number)]
            # print("len: %i*%i, %s" %(header_obj.point_number,header_obj.channel_number,chunks))
    
        chdir(outfolder)
        with open(filename.rstrip("jws")+"csv","w") as r:
            #print("file name: %s\t header names: %s" %(filename,header_obj.header_names))
            #r.write("sep=,\n")
            r.write( ",".join(str(x) for x in header_obj.header_names))
            r.write("\n")
            for line_no in range(header_obj.point_number):
                r.write(str(header_obj.x_for_first_point+line_no*header_obj.x_increment))
                r.write(",")
                for c in range(header_obj.channel_number):
                    r.write(str(chunks[c][line_no]))
                    r.write(",")
                r.write('\n')
            #print("%s is created." %r.name)
    
    text.insert(INSERT, "Conversion successfull!\n")

root = Tk()
root.title(".jws to .csv converter")

Button(root, text="Select the folder containing .jws files", command=lambda: select_folder(True)).pack(padx=10, pady=5)
Button(root, text="Select the folder where the .csv files should be saved", command=lambda: select_folder(False)).pack(padx=10, pady=5)
Button(root, text="Convert .jws to .csv", command=lambda: convert(infolder, outfolder)).pack(padx=10, pady=5)
Button(root, text="Quit", command=root.quit).pack(padx=10, pady=5)
text = Text(root, width=100, height=10)
text.pack(padx=10, pady=5)

root.mainloop()