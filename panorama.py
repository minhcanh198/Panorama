from tkinter import*
from tkinter import ttk
from tkinter import filedialog


import Image_Stitching
from tkinter import messagebox

import cv2
import numpy as np
from PIL import ImageTk,Image

class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.configure(background='black')
        self.linkList = []
        self.title("Panorama - Image Stitching")
        self.minsize(1200,600)
        self.maxsize(1200,600)

        self.canvas = Canvas(self)
        self.canvas.create_rectangle(0, 0, 1200, 600, outline="#6699ff", fill="#ccdcff")
        #draw left Panel
        self.canvas.create_rectangle(5, 40, 580, 595, outline="#6699ff", fill = "#ccdcff")
        #draw right Panel
        self.canvas.create_rectangle(590, 40, 1195, 595, outline="#6699ff")


        self.canvas.pack(fill=BOTH, expand=1)

        self.buttonBrowseFiles = ttk.Button(self, text= "Browse File", command = self.fileDialog)
        self.buttonBrowseFiles.place(x = 175, y = 68)

        lable = ttk.Label(self, text = "Open files to start stitching:",background = "#ccdcff")
        lable.place(x =15, y =70)
        lableTitle = ttk.Label(self, text="IMAGES STITCHING", font=("Helvetica", 40), background = "#ccdcff")
        lableTitle.place(x=320, y=10)
        self.lableTeam = ttk.Label(self, text = "This Product was developed by team: \n\t"
                                                "1. Nguyen Minh Canh - 16521493\n\t2. Tran Thien Trong - 16521541",
                                   background = "#ccdcff")
        self.lableTeam.place(x = 950, y = 530)

        self.buttonRunPano = ttk.Button(self, text= "Run Panorama",command = self.runPano)
        self.buttonRunPano.place(x=600,y = 70)

        self.buttonSaveFile =  ttk.Button(self, text= "Save image",command = self.saveFileDialog)
        self.buttonSaveFile.place(x = 600, y = 550)

    def runPano(self):
        var = StringVar()
        labelNotify = Label(self, textvariable=var, foreground="blue", font=20, background="#ccdcff")
        labelNotify.place(x=800, y=70)
        canvasImg = Image.new('RGB', (590, 430), color='#ccdcff')
        render = ImageTk.PhotoImage(canvasImg)
        canvasImg = ttk.Label(self, image=render)
        canvasImg.image = render
        canvasImg.place(x=600, y=98)
        if len(self.linkList)==1 :
            var.set("Sorry, please try again!!!")


        elif self.linkList:
            print("Panorama Running")
            linkLTemp = []
            for varL in self.linkList:
                linkLTemp.append(varL)

            Image_Stitching.runPano(linkLTemp)


            basewidth = 590
            img = Image.open('panorama.jpg')
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            if hsize > 430:
                hsize = 430
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)

            render = ImageTk.PhotoImage(img)
            img = ttk.Label(self, image=render)
            img.image = render
            img.place(x=600, y=100)
            var.set("Panorama sucessfully!!!")

        else :
            var.set("Sorry, please try again!!!")

    def fileDialog(self):
        # global my_image

        self.linkList = []
        self.filename = filedialog.askopenfilenames(initialdir = "/", title = "Select files", filetype = ( ("All Files", "*.*"),("JPEG", "*.jpeg"),("JPG", "*.jpg")))
        basewidth = 120
        x1 = 20
        y1 = 100
        canvasImg = Image.new('RGB',(555, 490), color = '#ccdcff')
        render = ImageTk.PhotoImage(canvasImg)
        canvasImg = ttk.Label(self, image=render)
        canvasImg.image = render
        canvasImg.place(x=15, y=95)
        for f in self.filename:
            self.linkList.append(f)
            img = Image.open(f)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)

            render = ImageTk.PhotoImage(img)
            img = ttk.Label(self, image=render)
            img.image = render
            img.place(x=x1, y=y1)
            x1 = x1+basewidth +10
            if (x1+basewidth > 599):
                x1 = 20
                y1 = y1 + hsize +20
    def saveFileDialog(self):
        img = Image.open("panorama.jpg")
        f =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if f :  # asksaveasfile return `None` if dialog closed with "cancel".
            img.save(f)


if __name__ == '__main__':
    root = Root()
    root.mainloop()

