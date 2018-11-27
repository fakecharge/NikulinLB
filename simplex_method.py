
class Simplex:
    def __init__(self):
        self.A = []  # переменная для матрицы
        self.m, self.n = 2, 2  # m - кол-во станков n - количество деталей
        self.bj = None
        self.x_value = {}
        self.k = 0
        self.A.append([])
        self.A[0].append("S\X")

        print(self.x_value)
        self.C = list()

        self.Z = ["Z"]
        self.input()
        for i in range(self.m):
            for j in range(self.n):
                self.A[0].append('X' + str(i) + str(j))
                string = 'X' + str(i) + str(j)

                self.x_value[string] = 0

        for i in self.C :
            print(i)
        self.preprocessCon(self.C)
        self.Z.append(0)
        self.A.append(self.Z)
        self.A[0].append("B")
        for i in self.A:
            string = ""
            for j in i:
                string = string + "\t\t" + str(j)
            print(string)
        self.simplex()
        for i in range(1, len(self.A) - 1):
            self.x_value[self.A[i][0]] = self.A[i][-1]

        self.x = list()
        for i in range(self.m):
            for j in range(self.n):
                string = 'X' + str(i) + str(j)
                self.x.append(self.x_value[string])

        self.goint()
        for i in range(self.m):
            for j in range(self.n):
                string = 'X' + str(i) + str(j)
                print(string + " = ", self.x[i * self.n + j])
        res = 0
        for i in range(1, len(self.Z) - 1):
            res = res + self.Z[i] * self.x[i - 1]

        print("Z = ", -1 * res)

    # проверка на оптимальность для двойственной таблицы
    def optimum2(self):
        for i in range(1, len(self.A) - 1):
            if self.A[i][-1] <= 0:
                print("Таблица не оптимальна!!!!")
                return True

        return False

    # поиск максимальной строки для двойственной таблицы
    def maximum_s(self):
        maximum = 1
        for i in range(2, len(self.A) - 1):
            if self.A[maximum][-1] >= 0:
                maximum = i
                continue
            if self.A[maximum][-1] > self.A[i][-1]:
                maximum = i
        return maximum

    """поиск минимального столбца для двойственной таблицы
        maximum  -> получается из self.maximum_s()"""

    def minimum_r(self, maximum):
        lst = list()
        for i in range(1, len(self.A[0]) - 1):
            if self.A[maximum][i] >= 0:
                lst.append(99999)
            else:
                lst.append(self.A[-1][i] / self.A[maximum][i])
        minimum = 0
        for i in range(1, len(lst)):
            if lst[minimum] > lst[i]:
                minimum = i

        return minimum + 1

    # Формируем Симплекс таблицу
    def preprocessCon(self, con):
        for cont in con:
            sign = cont[-2]
            if sign == "<=":
                self.A.append([])
                self.A[self.k + 1].append("S" + str(self.k))
                for i in range(len(cont) - 2):
                    self.A[self.k + 1].append(cont[i])
                self.A[self.k + 1].append(cont[-1])
                self.k += 1
            if sign == "=":
                self.A.append([])
                self.A[self.k + 1].append("0")
                for i in range(len(cont) - 2):
                    self.A[self.k + 1].append(cont[i])
                self.A[self.k + 1].append(cont[-1])
                self.k += 1
            if sign == ">=":
                for i in range(len(cont) - 2):
                    cont[i] = -1 * cont[i]
                cont[-1] = cont[-1] * -1
                self.A.append([])
                self.A[self.k + 1].append("S" + str(self.k))
                for i in range(len(cont) - 2):
                    self.A[self.k + 1].append(cont[i])
                self.A[self.k + 1].append(cont[-1])
                self.k += 1

    # Поиск разрешающего столбца
    def searchMin(self):
        Min = 1
        for i in range(2, len(self.A[-1]) - 1):
            if self.A[-1][i] > 0:
                if self.A[-1][i] > self.A[-1][Min]:
                    Min = i
        return Min

    # Поиск разрешающей строки
    def searchMin2(self, Min):
        lst = list()
        for i in range(1, len(self.A) - 1):
            if self.A[i][Min] != 0:
                lst.append(self.A[i][-1] / self.A[i][Min])
            else:
                lst.append(-1)
        maximum = 0
        for i in range(1, len(lst)):
            if lst[i] >= 0 and lst[i] <= lst[maximum]:
                maximum = i
        return maximum + 1

    # Строки и столбца в названиях
    def swap(self, Min1, Min2):
        self.A[0][Min1], self.A[Min2][0] = self.A[Min2][0], self.A[0][Min1]

    # Если переменная нуливая мы можем ее не учитывать, значит этот столбец можно удалить.
    def del_null(self, Min):
        if self.A[0][Min] == "0":
            for i in range(len(self.A)):
                del self.A[i][Min]

    # Проверка на оптимальность решения.
    def optimum(self):
        for i in range(1, len(self.A[-1]) - 1):
            if self.A[-1][i] >= 0:
                print("Таблица не оптимальна")
                return True
        print("Таблица Оптимальна ")
        return False

    # Пересчет таблицы относительно разрешающего элемента
    def calculate(self, max_r, min_s):
        new_a = []
        k = 0
        print("Разрешающий Элемент: ", min_s, max_r)
        for i in range(1, len(self.A) - 1):
            new_a.append([])
            new_a[k].append(self.A[i][0])
            for j in range(1, len(self.A[0]) - 1):
                if j == max_r:
                    if i == min_s:
                        new_a[k].append(1 / self.A[i][j])
                    else:
                        new_a[k].append(-1 * self.A[i][j] / self.A[min_s][max_r])
                else:
                    if i == min_s:
                        new_a[k].append(self.A[i][j] / self.A[min_s][max_r])
                    else:
                        new_a[k].append((self.A[i][j] * self.A[min_s][max_r] - (self.A[i][max_r] * self.A[min_s][j])) /
                                        self.A[min_s][max_r])

            k += 1
        new_a.append([])
        new_a[k].append("Z")
        for i in range(1, len(self.A[0]) - 1):
            if i == max_r:
                new_a[k].append(-1 * self.A[-1][i] / self.A[min_s][max_r])
            else:
                new_a[k].append(
                    (self.A[-1][i] * self.A[min_s][max_r] - self.A[-1][max_r] * self.A[min_s][i]) / self.A[min_s][
                        max_r])

            if i == min_s:
                new_a[i - 1].append(self.A[i][-1] / self.A[min_s][max_r])
            else:
                new_a[i - 1].append(
                    (self.A[i][-1] * self.A[min_s][max_r] - self.A[min_s][-1] * self.A[i][max_r]) / self.A[min_s][
                        max_r])

        new_a.insert(0, [])
        k += 1
        for i in self.A[0]:
            new_a[0].append(i)

        z = (self.A[-1][-1] * self.A[min_s][max_r] - self.A[-1][max_r] * self.A[min_s][-1]) / self.A[min_s][max_r]
        new_a[-1].append(z)
        for i in range(len(self.A)):
            self.A[i] = new_a[i]

    # Вывод таблицы
    def print_table(self):
        string = ""
        for i in self.A[0]:
            string = string + "\t\t\t" + i
        print(string)
        for i in range(1, len(self.A)):
            string = "\t\t\t" + self.A[i][0]
            for j in range(1, len(self.A[0])):
                string = string + "\t\t\t" + str(round(self.A[i][j], 2))
            print(string)



    """Метод для запуска подсчета симплекс методом для таблицы A
            s/x x1 x2 x3 x4 ... B
            s1  c1 c2 c3 c4 ... b1      
            s2  c5 c6 ...       b2
        A = s3  ...             b3
            s4  ...             b4
            ...                 ...
            Z   z1 z2 z3 z4 ... Zmax(min)
            """

    def simplex(self):
        k = 1
        while self.optimum2():
            print("ITER ", k)
            max_s = self.maximum_s()
            print("MAX_S: ", max_s)
            min_r = self.minimum_r(max_s)
            print("MIN_R", min_r)
            self.swap(min_r, max_s)
            self.calculate(min_r, max_s)
            self.print_table()
            k += 1

    # Функция ввода
    def input(self):
        print("\n".join((
            "*******************************************************************************",
            "Задача",
            "Имеется m - станков, на которых обрабатываются детали n - типов.",
            "На работу i-го станка отводится время ai",
            "По плану требуется отработать bj деталий j-го типа.",
            "Обработка i-м станком j-ой детали связана с подготовительными операциями",
            "требующие время tij, Сама обработка знамает время aij, а её стоимость равна cij",
            "Требуется составить оптимальный по стоимости план загрузки станков",
            "********************************************************************************"
        )))
        m = int(input("Введите m: "))
        n = int(input("Введите n: "))
        ai = []
        bj = []
        tij = []
        aij = []
        cij = []
        for i in range(m):
            string = "Введите a" + str((i + 1)) + ": "
            ai.append(float(input(string)))

        for j in range(n):
            string = "Введите b" + str((j + 1)) + ": "
            bj.append(float(input(string)))

        for i in range(m):
            lst1 = []
            lst2 = []
            lst3 = []
            for j in range(n):
                string1 = "Введите t" + str((i + 1)) + str((j + 1)) + ": "
                string2 = "Введите a" + str((i + 1)) + str((j + 1)) + ": "
                string3 = "Введите c" + str((i + 1)) + str((j + 1)) + ": "
                lst1.append(float(input(string1)))
                lst2.append(float(input(string2)))
                lst3.append(float(input(string3)))

            tij.append(lst1)
            aij.append(lst2)
            cij.append(lst3)
        string = "Z = "
        for ci in range(m):
            for c in range(n):
                string = string + " " + str(cij[ci][c]) + "x" + str(ci) + str(c)
        string = string + "-> min"
        print(string)
        for i in range(m):
            for j in range(n):
                self.Z.append(-1 * cij[i][j])
        full = n * m
        for i in range(n):
            lst1 = []
            for z in range(i * m):
                lst1.append(0)
            for j in range(m):
                lst1.append(1)
            for z in range(full - (i + 1) * m):
                lst1.append(0)

            lst1.append('>=')
            lst1.append(bj[i])
            self.C.append(lst1)

        for i in range(m):
            lst1 = []
            for j in range(n):
                lst1.append(tij[j][i] + aij[j][i])
                for z in range(m - 1):
                    lst1.append(0)
            if i == 1:
                lst1.pop()
                lst1.insert(0, 0)
            lst1.append('<=')
            lst1.append(ai[i])
            self.C.append(lst1)

        self.m, self.n = m, n
        self.bj = bj

    # Функция округления
    def goint(self):
        for i in range(self.n):
            z = self.bj[i]
            for j in range(self.m):
                self.x[i * self.m + j] = round(self.x[i * self.m + j])
                z = z - self.x[i * self.m + j]
            if z > 0:
                max = self.x[i * self.m]
                jmin = 0
                for j in range(1, self.m):
                    if max > self.x[i * self.m + j]:
                        jmin = j
                self.x[i * self.m + jmin] = self.x[i * self.m + jmin] - z
            else:
                max = self.x[i * self.m]
                jmin = 0
                for j in range(1, self.m):
                    if max < self.x[i * self.m + j]:
                        max = self.x[i * self.m + j]
                        jmin = j
                self.x[i * self.m + jmin] = self.x[i * self.m + jmin] + z


Simplex()
