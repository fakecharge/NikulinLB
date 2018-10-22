#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from numpy import *
from numpy.linalg import norm


class branch:
    def __init__(self, side, phi, k, m):
        self.side = side
        self.phi = phi
        self.k = k
        self.m = m


class test:
    def __init__(self):
        self.root = Tk()
        self.f1 = Frame(self.root, bd=4, bg='red',width=600, height=100)
        self.f2 = Frame(self.root)
        self.canvas = Canvas(self.f2, width=600, height=600)
        Button(self.f1, text='test', command=self.clear).grid(column=0, row=0)
        self.f1.pack()
        self.f2.pack()
        self.x1 = 0
        self.x2 = 0
        self.x3 = 300
        self.y1 = 0
        self.y2 = 0
        self.y3 = 600
        self.key = True
        self.listBranch = list()
        self.initTest()
        self.root.mainloop()

    def initTest(self):
        self.canvas.create_line(300, 600, 300, 100)
        self.canvas.bind('<Button-1>', self.cls)
        self.canvas.pack()

    def cls(self, event):
        if self.key:
            self.x1 = event.x
            self.y1 = event.y
            self.canvas.create_oval(self.x1-3, self.y1-3, self.x1+3, self.y1+3)
            self.key = False
        else:
            if event.y >= 100:
                self.y2 = event.y
            else:
                self.y2 = 100
            self.x2 = 300
            print(self.ygol())
            print(self.getK())
            print(self.getSid())
            print(self.getM())
            self.listBranch.append(branch(self.getSid(), self.ygol(), self.getK(), self.getM()))
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2)
            self.key = True
aaaaaaa
    def ygol(self):
        a = array([self.x1, self.y1])
        b = array([self.x2, self.y2])
        c = array([self.x3, self.y3])
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
        for i in self.listBranch:
            print(i.side, i.k, i.phi, i.m)
        self.printBranch()
        self.listBranch = list()
        self.canvas.pack_forget()
        self.canvas = Canvas(self.f2, width=600, height=600)
        self.canvas.pack()
        self.initTest()

    def printBranch(self):
        root2 = Tk()
        canvas = Canvas(root2, width=600, height=600)
        N = 300
        x0 = 300
        y0 = 100
        canvas.create_line(x0, 600, 300, 100)
        for i in self.listBranch:
            x1 = x0
            y1 = 500 * i.m
            px = x1 + ((i.k*N) * math.sin(i.phi))
            py = y1 + ((i.k*N) * math.cos(i.phi))
            canvas.create_line( x1, y1, px, py)
        canvas.pack()

    def getM(self):
        return math.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2) / 500

    def getK(self):
        return self.y2/500

    def getSid(self):
        if self.x1 >= 300:
            return 1
        else:
            return -1


print("math pi = ", math.pi/2)
test()
