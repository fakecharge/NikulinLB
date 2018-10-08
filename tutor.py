from tkinter import *
import random
import math


class Fern:

    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root)
        self.W = None
        self.eps = None
        self.Side = None

        self.N = None
        self.k1 = None
        self.k2 = None
        self.m1 = None
        self.m2 = None
        self.m3 = None
        self.phi0 = None
        self.phi1 = None
        self.phi2 = None
        self.phi3 = None
        self.random = False
        self.iter = None
        self.root2 = None
        self.canvas2 = None
        self.initStartUI()


    def initStartUI(self):
        self.root.title("Fern")
        # razmetka
        Label(self.canvas, text="Размер экрана").grid(column=0, row=0)
        Label(self.canvas, text='Глубина рекурсий').grid(column=0, row=1)
        Label(self.canvas, text='Направление изгиба').grid(column=0, row=2)
        Label(self.canvas, text='fi_0').grid(column=0, row=3)
        Label(self.canvas, text='fi_1').grid(column=0, row=4)
        Label(self.canvas, text='fi_2').grid(column=0, row=5)
        Label(self.canvas, text='fi_3').grid(column=0, row=6)
        Label(self.canvas, text='eps').grid(column=0, row=7)
        Label(self.canvas, text='k1').grid(column=0, row=8)
        Label(self.canvas, text='k2').grid(column=0, row=9)
        Label(self.canvas, text='m1').grid(column=0, row=10)
        Label(self.canvas, text='m2').grid(column=0, row=11)
        Label(self.canvas, text='m3').grid(column=0, row=12)
        ed1_str = StringVar()
        ed2_str = StringVar()
        ed3_str = StringVar()
        ed4_str = StringVar()
        ed5_str = StringVar()
        ed6_str = StringVar()
        ed7_str = StringVar()
        ed8_str = StringVar()
        ed9_str = StringVar()
        ed10_str = StringVar()
        ed11_str = StringVar()
        ed12_str = StringVar()
        ed13_str = StringVar()
        en = Entry(self.canvas, textvariable=ed1_str).grid(column=1, row=0)
        Entry(self.canvas, textvariable=ed2_str).grid(column=1, row=1)
        Entry(self.canvas, textvariable=ed3_str).grid(column=1, row=2)
        Entry(self.canvas, textvariable=ed4_str).grid(column=1, row=3)
        Entry(self.canvas, textvariable=ed5_str).grid(column=1, row=4)
        Entry(self.canvas, textvariable=ed6_str).grid(column=1, row=5)
        Entry(self.canvas, textvariable=ed7_str).grid(column=1, row=6)
        Entry(self.canvas, textvariable=ed8_str).grid(column=1, row=7)
        Entry(self.canvas, textvariable=ed9_str).grid(column=1, row=8)
        Entry(self.canvas, textvariable=ed10_str).grid(column=1, row=9)
        Entry(self.canvas, textvariable=ed11_str).grid(column=1, row=10)
        Entry(self.canvas, textvariable=ed12_str).grid(column=1, row=11)
        Entry(self.canvas, textvariable=ed13_str).grid(column=1, row=12)
        self.canvas.pack()
        #Button(self.canvas, text='Нарисовать', command=lambda: self.run(int(ed1_str.get()), int(ed2_str.get()),
         #                                                               int(ed3_str.get()),
          #                                                              float(ed4_str.get()),
           #                                                             float(ed5_str.get()),
            #                                                            float(ed6_str.get()),
             #                                                           float(ed7_str.get()),
              #                                                          float(ed8_str.get()),
               #                                                         float(ed9_str.get()),
                #                                                        float(ed10_str.get()),
                 #                                                       float(ed11_str.get()),
                  #                                                      float(ed12_str.get()),
                   #                                                     float(ed13_str.get()))).grid(column=0, row=13)
        Button(self.canvas, text='Нр', command=lambda: self.test(ed1_str.get())).grid(column=0, row=13)
        self.canvas.pack()
        self.root.mainloop()

    def draw(self, x0, y0, x1, y1):
        self.canvas2.create_line(x0, y0, x1, y1)

    def test(self, sl="none"):
        print(sl)

    def run(self, W, N, Side, phi0, phi1, phi2, phi3, eps, k1, k2, m1, m2, m3):
        self.W = W
        self.eps = eps
        self.Side = Side

        self.N = N
        self.k1 = k1
        self.k2 = k2
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.phi0 = phi0 * math.pi / 180.0
        self.phi1 = phi1 * math.pi / 180.0
        self.phi2 = phi2 * math.pi / 180.0
        self.phi3 = phi3 * math.pi / 180.0
        self.random = False
        self.iter = 0
        self.root2 = Tk()
        self.canvas2 = Canvas(self.root2, width=W, height=W)
        self.fern(300, 0, W, 0.0, self.Side, self.eps, self.N)
        self.canvas2.pack()
        self.root2.mainloop()

    def fern(self, x0, y0, h, psi, side, delta, rec):
        if (rec == 0) or (self.k2 * h < delta):
            return
        self.iter = self.iter + 1
        p1x = x0 - (self.k1 * h) * math.sin(psi)
        p1y = y0 + (self.k1 * h) * math.cos(psi)
        p2x = x0 - (self.k2 * h) * math.sin(psi)
        p2y = y0 + (self.k2 * h) * math.cos(psi)
        self.canvas2.create_line(x0, self.W - y0, p2x, self.W - p2y)
        self.fern(p1x, p1y, self.m1 * h, psi - side * (self.phi1 + self.phi0), (-1) * side, delta, rec - 1)
        self.fern(p2x, p2y, self.m2 * h, psi + side * (self.phi2 + self.phi0), side, delta, rec - 1)
        self.fern(p2x, p2y, self.m3 * h, psi - side * (self.phi3 - self.phi0), side, delta, rec - 1)


fern = Fern()
