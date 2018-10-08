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
        self.random1 = False
        self.iter = None
        self.root2 = None
        self.canvas2 = None
        self.initStartUI()

    def initStartUI(self):
        self.root.title("Fern")
        # razmetka
        Label(self.canvas, text="Размер").grid(column=0, row=0)
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
        en1 = Entry(self.canvas, textvariable=ed1_str)
        en1.insert(0, 600)
        en1.grid(column=1, row=0)
        en2 = Entry(self.canvas, textvariable=ed2_str)
        en2.insert(0, 70)
        en2.grid(column=1, row=1)
        en3 = Entry(self.canvas, textvariable=ed3_str)
        en3.insert(0, 1)
        en3.grid(column=1, row=2)
        en4 = Entry(self.canvas, textvariable=ed4_str)
        en4.insert(0, 14.9)
        en4.grid(column=1, row=3)
        en5 = Entry(self.canvas, textvariable=ed5_str)
        en5.insert(0, 37.7)
        en5.grid(column=1, row=4)
        en6 = Entry(self.canvas, textvariable=ed6_str)
        en6.insert(0, 36.8)
        en6.grid(column=1, row=5)
        en7 = Entry(self.canvas, textvariable=ed7_str)
        en7.insert(0, 17.6)
        en7.grid(column=1, row=6)
        en8 = Entry(self.canvas, textvariable=ed8_str)
        en8.insert(0, 0.5)
        en8.grid(column=1, row=7)
        en9 = Entry(self.canvas, textvariable=ed9_str)
        en9.insert(0, 0.0483)
        en9.grid(column=1, row=8)
        en10 = Entry(self.canvas, textvariable=ed10_str)
        en10.insert(0, 0.162)
        en10.grid(column=1, row=9)
        en11 = Entry(self.canvas, textvariable=ed11_str)
        en11.insert(0, 0.371)
        en11.grid(column=1, row=10)
        en12 = Entry(self.canvas, textvariable=ed12_str)
        en12.insert(0, 0.336)
        en12.grid(column=1, row=11)
        en13 = Entry(self.canvas, textvariable=ed13_str)
        en13.insert(0, 0.849)
        en13.grid(column=1, row=12)
        check = BooleanVar()
        Checkbutton(self.canvas, text="Случайные значение ветвей", variable=check).grid(column=1, row=13)
        Button(self.canvas, text='Test', command=lambda : self.test(check.get())).grid(column=0, row=13)
        self.canvas.pack()
        Button(self.canvas,
               text='Нарисовать',
               command=lambda: self.run(int(ed1_str.get()), int(ed2_str.get()),
                                        int(ed3_str.get()),
                                        float(ed4_str.get()),
                                        float(ed5_str.get()),
                                        float(ed6_str.get()),
                                        float(ed7_str.get()),
                                        float(ed8_str.get()),
                                        float(ed9_str.get()),
                                        float(ed10_str.get()),
                                        float(ed11_str.get()),
                                        float(ed12_str.get()),
                                        float(ed13_str.get()), check.get())).grid(column=0, row=14)
        Button(self.canvas,
               text='Нарисовать со случайными значениями',
               command=lambda : self.run(random.randint(300, 800), random.randint(50, 80), random.randint(-1, 1),
                                         random.uniform(13, 16),
                                         random.uniform(35, 39),
                                         random.uniform(35, 39),
                                         random.uniform(15, 18),
                                         random.uniform(0.4, 0.6),
                                         random.uniform(0.04, 0.05),
                                         random.uniform(0.1, 0.2),
                                         random.uniform(0.3, 0.4),
                                         random.uniform(0.3, 0.4),
                                         random.uniform(0.8, 0.9), check.get())).grid(column=1, row=14)
        self.canvas.pack()
        self.root.mainloop()

    def draw(self, x0, y0, x1, y1):
        self.canvas2.create_line(x0, y0, x1, y1)

    def test(self, sl="none"):
        print(sl)

    def run(self, W, N, Side, phi0, phi1, phi2, phi3, eps, k1, k2, m1, m2, m3, rnd):
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
        self.random1 = rnd
        self.iter = 0
        self.root2 = Tk()
        self.canvas2 = Canvas(self.root2, width=W + 200, height=W + 200)
        self.fern((W+200)/2.0, -200, W, 0.0, self.Side, self.eps, self.N)
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
        if self.random1:
            r1 = (random.randint(0, 2000)/100.0-10.0)*math.pi/180.0
            r2 = (random.randint(0, 2000)/100.0-10.0)*math.pi/180.0
            r3 = (random.randint(0, 2000)/100.0-10.0)*math.pi/180.0
        else:
            r1 = 0.0
            r2 = 0.0
            r3 = 0.0
        self.canvas2.create_line(x0, self.W - y0, p2x, self.W - p2y)
        self.fern(p1x, p1y, self.m1 * h, psi - side * (self.phi1 + self.phi0 + r1), (-1) * side, delta, rec - 1)
        self.fern(p2x, p2y, self.m2 * h, psi + side * (self.phi2 + self.phi0 + r2), side, delta, rec - 1)
        self.fern(p2x, p2y, self.m3 * h, psi - side * (self.phi3 - self.phi0 + r3), side, delta, rec - 1)


fern = Fern()
