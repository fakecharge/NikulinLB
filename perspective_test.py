import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
from tkinter import *


class perspectiv:
    def __init__(self):
        self.canvas3 = None
        self.fr3 = None
        self.root = None
        self.fr1 = None
        self.fr2 = None
        self.canvas = None
        self.pts2 = []
        self.k = 0
        self.initUi()

    def result(self, pts):
        img = cv.imread('test.png')

        rows, cols, ch = img.shape

        pts1 = np.float32([[0, 0], [0, 300], [300, 300], [300, 0]])
        pts2 = np.float32(pts)
        M = cv.getPerspectiveTransform(pts1, pts2)
        dst = cv.warpPerspective(img, M, (300, 300))
        plt.subplot(121), plt.imshow(img), plt.title('Input')
        plt.subplot(122), plt.imshow(dst), plt.title('Output')
        plt.show()

    def initUi(self):
        self.root = Tk()
        self.fr1 = Frame(self.root)
        self.fr3 = Frame(self.root)
        self.canvas3 = Canvas(self.fr3, width=400, height=400)
        self.canvas3.create_text(50, 30, text="0,0")
        self.canvas3.create_text(350, 360, text='300,300')
        self.canvas3.create_rectangle(50, 50, 350, 350)
        self.canvas3.create_oval(45,45,55,55 ,outline='red',
    fill='red')
        self.canvas3.create_oval(45, 345, 55, 355, outline='red',
                                 fill='red')
        self.canvas3.create_oval(345, 45, 355, 55, outline='red',
                                 fill='red')
        self.canvas3.create_oval(345, 345, 355, 355, outline='red',
                                 fill='red')
        self.canvas3.create_text(200, 200, text="IMAGE")
        self.canvas3.create_text(60,60, text='1', fill='red')
        self.canvas3.create_text(60,340, text='2', fill='red')
        self.canvas3.create_text(340,340, text='3', fill='red')
        self.canvas3.create_text(340,60, text='4', fill='red')
        Label(self.fr1, text="Задайте 4 точки для создания перспективы(1, 2, 3, 4):").grid(column=0, row=0)
        Button(self.fr1, text="print list", command=lambda: self.print()).grid(column=1, row=0)
        self.fr2 = Frame(self.root)
        self.canvas = Canvas(self.fr2, width=400, height=400)
        self.canvas.create_text(50, 30, text="0,0")
        self.canvas.create_text(350, 360, text='300,300')
        self.canvas.bind('<Button-1>', self.cls)
        self.canvas.create_rectangle(50, 50, 350, 350)
        self.canvas.pack()
        self.canvas3.pack()
        self.fr1.pack()
        self.fr3.pack()
        self.fr2.pack()
        self.root.mainloop()

    def print(self):
        pts = self.pts2
        self.pts2 = []
        self.canvas.pack_forget()
        self.canvas = Canvas(self.fr2, width=400, height=400)
        self.canvas.create_text(50, 30, text="0,0")
        self.canvas.create_text(350, 360, text='300,300')
        self.canvas.bind('<Button-1>', self.cls)
        self.canvas.create_rectangle(50, 50, 350, 350)
        self.canvas.pack()
        self.k = 0
        self.result(pts)


    def cls(self, event):
        txt = self.k + 1
        txt = str(txt)
        if 50 <= event.x <= 350 and 50 <= event.y <= 350 and self.k < 4:
            self.canvas.create_oval(event.x - 3, event.y - 3, event.x, event.y)
            self.canvas.create_text(event.x+5,event.y+5, text=txt)
            self.pts2.append([event.x - 50, event.y - 50])
            self.k = self.k + 1
            self.canvas.pack()


pr = perspectiv()
