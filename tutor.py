from tkinter import *
import random
import math
from numpy import *
from numpy.linalg import norm

class branch:
    def __init__(self, side, phi, k, m, inverse):
        self.reverse = True
        self.side = side
        self.phi = math.pi - phi
        self.k = k
        self.m = m*1.2
        self.inverse = inverse


class Fern:

    def __init__(self):
        self.listBr = list()
        self.root = Tk()
        self.f1 = Frame(self.root, bd=4, bg='red', width=600, height=100)
        self.f2 = Frame(self.root)
        self.canvas = Canvas(self.f2, width=900, height=900)
        Button(self.f1, text='test', command=self.clear).grid(column=0, row=0)
        Button(self.f1, text='clear', command=self.clearall).grid(column=0, row=1)
        Label(self.f1, text='Глубина рекурсий').grid(column=1, row=1)
        self.ed2_str = StringVar()
        self.en2 = Entry(self.f1, textvariable=self.ed2_str)
        self.en2.insert(0, 70)
        self.en2.grid(column=1, row=2)
        self.f1.pack()
        self.f2.pack()
        self.x1 = 0
        self.x2 = 0
        self.x3 = 300
        self.y1 = 0
        self.y2 = 0
        self.y3 = 600
        self.W = None
        self.eps = None
        self.Side = None
        self.key = True
        self.N = None
        self.k1 = None
        self.k2 = 1
        self.m1 = None
        self.m2 = None
        self.m3 = 0.849
        self.phi0 = math.pi/300
        self.phi1 = math.pi/200
        self.phi2 = None
        self.phi3 = None
        self.random1 = False
        self.inverse = False
        self.iter = None
        self.root2 = None
        self.canvas2 = None
        self.initTest()
        self.root.mainloop()


    def initTest(self):
        self.canvas.create_line(300, 600, 300, 200)
        self.canvas.create_line(0,500, 600, 500)
        self.canvas.bind('<Button-1>', self.cls)
        self.canvas.pack()


    def cls2(self, event):
        if self.key:
            self.x1 = event.x
            self.y1 = event.y
            self.canvas.create_oval(self.x1 - 3, self.y1-3, self.x1+3, self.y1+3)
            self.key = False
        else:
            self.y2 = event.y
            self.x2 = event.x
            if math.sqrt((self.x1 - 300) ** 2) >= math.sqrt((self.x2-300) ** 2):
                self.x2 = 300
                if self.y2 < 200:
                    self.y2 = 200
                self.inverse = False
            else:
                self.x1 = 300
                if self.y1 < 200:
                    self.y1 = 200
                self.inverse = True
                self.listBr.append(branch(self.getSid(), self.ygol(), self.getK(), self.getM(), self.inverse))
                self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
                self.key = True



    def cls(self, event):
        if self.key:
            self.x1 = event.x
            self.y1 = event.y
            self.canvas.create_oval(self.x1-3, self.y1-3, self.x1+3, self.y1+3)
            self.key = False
        else:
            if event.y >= 200:
                self.y2 = event.y
            else:
                self.y2 = 200
            if self.y2 >= 600:
                self.y2 = 600
            self.x2 = 300
            print(self.ygol())
            print(self.getK())
            print(self.getSid())
            print(self.getM())
            self.listBr.append(branch(self.getSid(), self.ygol(), self.getK(), self.getM(), self.inverse))
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
            self.key = True

    def ygol(self):
        a = array([self.x1, self.y1])
        b = array([self.x2, self.y2])
        if self.y3 == 600 :
            c = array([self.x3, self.y3+100])
        f = b - a
        e = b - c
        abVec = norm(f)
        bcVec = norm(e)
        abNorm = f / abVec
        bcNorm = e / bcVec
        res = abNorm[0] * bcNorm[0] + abNorm[1] * bcNorm[1]
        angle = arccos(res)
        return angle

    def clear(self):
        for i in self.listBr:
            print(i.side, i.k, i.phi, i.m)
        self.run2(400, 70, self.listBr, True)
        self.listBr = list()
        self.canvas.pack_forget()
        self.canvas = Canvas(self.f2, width=900, height=900)
        self.canvas.pack()

    def getM(self):
        return math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) / 400

    def getK(self):
        k = math.sqrt((self.y2-600)**2)/400.0
        if k > 0:
            return k
        else:
            return 0.001
    def getSid(self):
        if self.x1 >= 300:
            return 1
        else:
            return -1

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
        Button(self.canvas, text='Test', command=lambda: self.test(check.get())).grid(column=0, row=13)
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
               command=lambda: self.run(random.randint(300, 800), random.randint(50, 80), random.randint(-1, 1),
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

    def clearall(self):
        self.canvas.pack_forget()
        self.canvas = Canvas(self.f2, width=900, height=900)
        self.listBr = list()
        self.initTest()
        self.canvas.pack()

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
        self.listBr.append(branch(1, self.phi1, self.k1, self.m2))
        self.iter = 0
        self.root2 = Tk()
        self.canvas2 = Canvas(self.root2, width=W + 200, height=W + 200)
        self.fern2((W + 100) / 2.0, -100, W, 0.0, self.Side, self.eps, self.N)
        self.canvas2.pack()
        self.root2.mainloop()

    def run2(self, W, N, listbr, rnd):
        self.W = W
        self.iter = 0
        self.listBr = listbr
        self.root2 = Tk()
        self.canvas2 = Canvas(self.root2, width=W + 500, height=W + 500)
        self.fern2((W)/2.0, 0.0, W/2.0 ,2* math.pi, 1, 0.5, int(self.ed2_str.get()))
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
        p3x = x0 - (0.07 * h) * math.sin(psi)
        p3y = y0 + (0.07 * h) * math.cos(psi)
        if self.random1:
            r1 = (random.randint(0, 2000) / 100.0 - 10.0) * math.pi / 180.0
            r2 = (random.randint(0, 2000) / 100.0 - 10.0) * math.pi / 180.0
            r3 = (random.randint(0, 2000) / 100.0 - 10.0) * math.pi / 180.0
        else:
            r1 = 0.0
            r2 = 0.0
            r3 = 0.0
        self.canvas2.create_line(x0, self.W - y0, p2x, self.W - p2y)
        self.fern(p1x, p1y, self.m1 * h, psi - side * (self.phi1 + self.phi0 + r1), (-1) * side, delta, rec - 1)
        self.fern(p3x, p3y, self.m2 * h, psi + side * (self.phi2 + self.phi0 + r2), side, delta, rec - 1)
        self.fern(p2x, p2y, self.m3 * h, psi - side * (self.phi3 - self.phi0 + r3), side, delta, rec - 1)

    def fern2(self, x0, y0, h, psi, side, delta, rec):
        if (rec == 0) or (self.k2 * h < delta): return
        self.iter = self.iter + 1
        print(self.iter)
        g_p_x = x0 + (h*self.k2) * math.sin(psi)
        g_p_y = y0 + (h*self.k2) * math.cos(psi * -1)
        print(x0, y0, g_p_x, g_p_y)
        self.canvas2.create_line(x0+200, self.W - y0 + 200, g_p_x+200, self.W - g_p_y + 200)
        for i in self.listBr:
            x = x0 + (i.k*h) * math.sin(psi)
            y = y0 + (i.k*h) * math.cos(psi)
            self.fern2(x, y, h*i.m, psi + i.side*(i.phi), i.side, delta, rec - 1)
        #self.fern2(g_p_x, g_p_y, self.m3*h, psi - side * (self.phi0+self.phi1), side, delta, rec - 1)

fern = Fern()
