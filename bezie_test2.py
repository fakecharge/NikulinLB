from geomdl import NURBS
from geomdl import utilities
from geomdl import Multi
from geomdl.visualization import VisMPL
from tkinter import *
import math


class Bezie:
    
    def __init__(self):
        self.root3 = None
        self.fr1 = None
        self.fr2 = None
        self.canvas = None
        self.canvas2 = None
        self.lst = list()
        self.k = 0
        self.initUi()


    def create_bezie_curve(self,p0, p1, p2, w):
        curve = NURBS.Curve()
        curve.degree = 2
        curve.ctrlpts = [p0, p1, p2]
        curve.weights = [1, w, 1]
        curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))
        curve.sample_size = 200
        curve.evaluate()
    
        return curve
    
    
    def run(self, N, weight):
        cv = Multi.MultiCurve()
        cv.add(self.create_bezie_curve(self.lst[0], self.lst[1], self.lst[2], weight))
        vis_compl = VisMPL.VisCurve2D()
        cv.vis = vis_compl
        cv.render()
    
    
    def initUi(self):
        self.root3 = Tk()
        self.fr1 = Frame(self.root3)
        self.fr2 = Frame(self.root3)
        self.canvas = Canvas(self.fr2, width=600, height=600)
        self.canvas2 = Canvas(self.fr1)
        self.canvas2.pack()
        self.canvas.create_line(0, 10, 600 , 10)
        self.canvas.pack()
        wieght = StringVar()
        entr = Entry(self.canvas2, textvariable=wieght)
        entr.insert(0, "0.1")
        entr.grid(column=0, row=0)
        Label(self.canvas2, text='Вес второй точки ').grid(column=0, row=1)
        Button(self.canvas2, text="Нарисовать", command=lambda : self.run(0, float(wieght.get()))).grid(column=1, row=0)
        Button(self.canvas2, text="clear", command=lambda : self.clear()).grid(column=1, row=1)
        self.canvas.bind('<Button-1>', self.cls)
        self.fr1.pack()
        self.fr2.pack()
        self.root3.mainloop()

    def cls(self, event):
        self.k += 1
        if self.k <= 3:
            self.lst.append((event.x, 600 - event.y))
            self.canvas.create_oval(event.x-3, event.y-3,event.x + 3, event.y+3)
            self.canvas.pack()

    def clear(self):
        self.k = 0
        self.lst = list()
        self.canvas.pack_forget()
        self.canvas = Canvas(self.fr2, width=600, height=600)
        self.canvas.bind('<Button-1>', self.cls)
        self.canvas.create_line(0, 10, 600 , 10)
        self.canvas.pack()




if __name__ =='__main__':
    Bezie()

