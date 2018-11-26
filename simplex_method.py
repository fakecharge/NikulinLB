import numpy as np

class Simplex():
    def __init__(self):
        self.A = [] #переменная для матрицы
        Z = None #переменная для функции
        m , n = 2, 2
        self.k = 0
        self.A.append([])
        self.A[0].append("S\X")
        for i in range(m):
           for j in range(n):
               self.A[0].append('X' + str(i) + str(j))

        self.A[0].append("B")
        c1 = [1, 1, 0, 0, ">=", 3]
        c2 = [0, 0, 1, 1, ">=", 4]
        c3 = [2, 0, 3, 0, "<=", 30]
        c4 = [0, 4, 0, 1, "<=", 40]
        C = list()
        C.append(c1)
        C.append(c2)
        C.append(c3)
        C.append(c4)

        self.preprocessCon(C)
        Z = ["Z", 1, 1, 1, 1, 0]
        self.A.append(Z)
        for i in self.A:
            string = ""
            for j in i:
                string = string + "\t\t" + str(j)
            print(string)
        self.simplex()

    #Формируем Симплекс таблицу
    def preprocessCon(self, con):
        for cont in con:
            sign = cont[-2]
            if sign == "<=" :
                self.A.append([])
                self.A[self.k+1].append("S" + str(self.k))
                for i in range(len(cont) -2) :
                    self.A[self.k+1].append(cont[i])
                self.A[self.k+1].append(cont[-1])
                self.k+=1
            if sign == "=" :
                self.A.append([])
                self.A[self.k + 1].append("0")
                for i in range(len(cont)-2):
                    self.A[self.k+1].append(cont[i])
                self.A[self.k+1].append(cont[-1])
                self.k+=1
            if sign == ">=" :
                for i in range(len(cont)-2):
                    cont[i] = -1 * cont[i]
                cont[-1] = cont[-1] * -1
                self.A.append([])
                self.A[self.k + 1].append("S" + str(self.k))
                for i in range(len(cont) - 2):
                    self.A[self.k + 1].append(cont[i])
                self.A[self.k + 1].append(cont[-1])
                self.k += 1

    #Поиск разрешающего столбца
    def searchMin(self):
        Min = 1
        for i in range(2, len(self.A[-1]) -1):
            if self.A[-1][i] > 0:
                if self.A[-1][i] > self.A[-1][Min]:
                    Min = i
        return Min

    #Поиск разрешающей строки
    def searchMin2(self, Min):
        lst = list()
        for i in range(1, len(self.A)-1):
            if self.A[i][Min] != 0:
                lst.append(self.A[i][-1]/self.A[i][Min])
            else:
                lst.append(-1)
        maximum = 0
        for i in range(1,len(lst)):
            if lst[i] >= 0 and lst[i] <= lst[maximum]:
                maximum = i
        return maximum + 1

    #Строки и столбца в названиях
    def swap(self, Min1, Min2):
        self.A[0][Min1], self.A[Min2][0] = self.A[Min2][0], self.A[0][Min1]

    #Если переменная нуливая мы можем ее не учитывать, значит этот столбец можно удалить.
    def del_null(self, Min):
        if self.A[0][Min] == "0":
            for i in range(len(self.A)):
                del self.A[i][Min]

    #Проверка на оптимальность решения.
    def optimum(self):
        for i in range(1,len(self.A[-1]) -1):
            if self.A[-1][i] >= 0:
                print("Таблица не оптимальна")
                return True
        print("Таблица Оптимальна ")
        return False


    def calculate(self, max_r, min_s):
        new_a = []
        k = 0
        print("Разрешающий Элемент: ", max_r, min_s)
        for i in range(1, len(self.A) - 1):
            new_a.append([])
            new_a[k].append(self.A[i][0])
            for j in range(1, len(self.A[0]) - 1):
                if j == max_r:
                    if i == min_s:
                        new_a[k].append(1/self.A[i][j])
                    else:
                        new_a[k].append(-1 * self.A[i][j]/self.A[min_s][max_r])
                else:
                    if i == min_s:
                        new_a[k].append(self.A[i][j]/self.A[min_s][max_r])
                    else:
                        new_a[k].append((self.A[i][j]*self.A[min_s][max_r] - (self.A[i][max_r] * self.A[min_s][j]))/self.A[min_s][max_r])

            k += 1
        new_a.append([])
        new_a[k].append("Z")
        for i in range(1, len(self.A[0])-1):
            if i == max_r:
                new_a[k].append(-1 * self.A[-1][i]/self.A[min_s][max_r])
            else:
                new_a[k].append((self.A[-1][i]*self.A[min_s][max_r] - self.A[-1][max_r]*self.A[min_s][i])/self.A[min_s][max_r])

            if i == min_s:
                new_a[i-1].append(self.A[i][-1]/self.A[min_s][max_r])
            else:
                new_a[i-1].append((self.A[i][-1]*self.A[min_s][max_r] - self.A[min_s][-1]*self.A[i][max_r])/self.A[min_s][max_r])

        new_a.insert(0, [])
        k +=1
        for i in self.A[0]:
            new_a[0].append(i)

        z = (self.A[-1][-1]*self.A[min_s][max_r] - self.A[-1][max_r]*self.A[min_s][-1])/ self.A[min_s][max_r]
        new_a[-1].append(z)
        for i in range(len(self.A)):
            print(new_a[i])
            self.A[i] = new_a[i]


    def print_table(self):
        for i in self.A:
            string = ""
            for j in i:
                string = string + "\t\t" + str(j)
            print(string)

    def simplex(self):
            max_r = self.searchMin()
            min_s = self.searchMin2(max_r)
            self.swap(max_r, min_s)
            self.del_null(max_r)
            print("MIN_R: ", max_r)
            print("MIN_S: ", min_s)
            self.calculate(max_r, min_s)
            self.print_table()





Simplex()