from tkinter import *
import random
import math


class Fern:

    def __init__(self):
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

        self.root = Tk()
        self.root.title("Fern")
        self.canvas = Canvas(self.root)
        # razmetka

        Label(self.root, text='Размер Экрана').grid(row=1, column=1)
        self.W_e = Entry(self.root).grid(row=1,column=2)
        Label(self.root, text="Глубина рекурсий").grid(row=2, column=1)
        self.N_e = Entry(self.root).grid(row=2,column=2)
        Label(self.root, text='Изгиб').grid(row=3, column=1)
        self.Side_e = Entry(self.root).grid(row=3,column=2)
        btn1 = Button(self.root, text='test', command=self.test(self.Side_e)).grid(row=4, column=1)
        self.root.mainloop()

    def draw(self, x0, y0, x1, y1):
        self.canvas2.create_line(x0, y0, x1, y1)

    def test(self, sl):
        print(sl.get())

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
