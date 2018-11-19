from copy import deepcopy
from logging import debug

class SimplexSolverException(Exception):
    pass


class NoSolutionException(SimplexSolverException):
    pass

class SimplexSolver(object):
    valid_inequality_signs = ('>=', '<=', '=')

    def __init__(self):
        self._is_max = None  # Тип целевой функции
        self._target_multipliers = None  # коэффициенты целевой функции
        self._constraints = None  # Ограничения
        self._rows = []  # Матрица для решения

        # Эти счетчики нужны, чтобы ориентироваться по матрице. См. метод solve()
        self._constraints_counter = 0
        self._gte_constraints_counter = 0
        self._e_constraints_counter = 0
        self._lte_constraints_counter = 0

        self._involved_in_basis = []  # Переменные вошедшие в базис

        # Строки с искусственным базисом
        self._temporary_rows = []
        self._temporary_cols = []

        self._objective_row = None  # Строка целевой функции

    def _check_solution_optimal(self):
        """Проверяет оптимальность решения"""
        # Если есть временные переменные, строим строку оценки и проверяем оптимальность
        # по ней.
        if len(self._temporary_rows):
            score_row = self._build_score_row()
        # Иначе берем основную строку
        else:
            score_row = self._objective_row[0:-1]
        for idx, i in enumerate(score_row):
            if idx not in self._temporary_cols and i < 0:
                return False
        return True

    def _build_score_row(self):
        """Строит строку оценки, если в базисе есть искусственные переменные"""
        row_nums = self._temporary_rows
        result = [0] * (len(self._objective_row)-1)
        for idx, row in enumerate(self._rows):
            # Если это строка с искусственной переменной
            if idx in row_nums:
                for i, col in enumerate(row[:-1]):
                    result[i] += col
            # Меняем знак и возвращаем результат
        for i, col in enumerate(result):
            result[i] = -col
        debug("SCORE")
        debug(result)
        return result

    def _get_pivot_col(self):
        """Возвращает индекс ведущего столбца"""
        # Если в базисе присутствуют временные переменные, строим строку оценки
        if len(self._temporary_rows):
            score_row = self._build_score_row()
        else:
            score_row = self._objective_row[:-1]
        temp = 0.0
        result = None
        for i in range(0, len(score_row)):
            if score_row[i] < temp:
                temp = score_row[i]
                result = i
        return result

    def _get_pivot_row(self, pivot_col):
        """Возвращает индекс ведущей строки в переданном столбце"""
        b_col = []
        p_col = []
        for row in self._rows:
            b_col.append(row[-1])
            p_col.append(row[pivot_col])
        pos_found = False
        # Ищем числа > 0 в столбце. Если их нет, уравнение не имеет решений,
        # кидаем исключение.
        for i in p_col:
            if i > 0:
                pos_found = True
                break
        if not pos_found:
            raise NoSolutionException('Нет решения. Задача не ограничена.')
        ratio = []
        for i, b in enumerate(b_col):
            if p_col[i] <= 0:
                # Число отрицательное или ноль. Не наш клиент, делаем так, чтобы он
                # наверняка не стал ведущим )
                ratio.append(99999999 * max(b_col))
            else:
                ratio.append(b_col[i] / p_col[i])
        min_val = min(ratio)
        for idx, val in enumerate(ratio):
            if val == min_val:
                return idx

    def _pivot(self, pivot_row, pivot_col):
        """Оптимизирует таблицу. Принимает координаты ведущей ячейки"""
        pivot = self._rows[pivot_row][pivot_col]  # Опорное значение(разрешающий элемент)
        # Делим ведущую строку на разрешающий элемент
        rows = deepcopy(self._rows)
        for col_idx, col_val in enumerate(rows[pivot_row]):
            rows[pivot_row][col_idx] = float(col_val) / float(pivot)
        # Правило четырехугольника
        for row_idx in range(len(rows)):
            if row_idx == pivot_row:
                continue
            for col_idx, col_val in enumerate(rows[row_idx]):
                old_val = float(col_val)
                a = float(self._rows[pivot_row][col_idx])
                b = float(self._rows[row_idx][pivot_col])
                rows[row_idx][col_idx] = old_val - (a * b) / pivot
        # Строка функции пересчитывается по тому же правилу
        objective_row = deepcopy(self._objective_row)
        for idx, val in enumerate(objective_row):
            a = self._rows[pivot_row][idx]
            b = self._objective_row[pivot_col]
            objective_row[idx] = val - (a * b) / pivot
        self._rows = rows
        self._objective_row = objective_row
        for i, val in enumerate(self._temporary_rows):
            if val == pivot_row:
                del(self._temporary_rows[i])

    def _check_ready_to_solve(self):
        """Проверяет, что выполнены все предусловия перед началом решения задачи"""
        if self._is_max is None:
            raise SimplexSolverException('Не задан тип целевой функции')
        if self._target_multipliers is None or len(self._target_multipliers) < 2:
            raise SimplexSolverException('Не заданы коэффициенты целевой функции')
        if self._constraints_counter < 2:
            raise SimplexSolverException('Не заданы ограничения')

    def _solve(self):
        """Основная функция поиска решений. На выходе возвращает структуру
        ([X1, X2, XY], Значение Z)"""
        self._check_ready_to_solve()
        # Похоже, все в порядке. Пробуем решать.
        target_coefficients = self._target_multipliers
        # Переменные вошедшие в базис
        for i in range(len(target_coefficients)):
            self._involved_in_basis.append(None)
        # Если ищем максимум целевой функции, инвертируем коэффициенты целевой функции
        if self._is_max:
            for idx, coefficient in enumerate(target_coefficients):
                target_coefficients[idx] = -coefficient
        # Строка целевой функции
        self._objective_row = list(target_coefficients)
        # Добавляем ограничения
        lte_constraints = self._constraints.get('<=')
        e_constraints = self._constraints.get('=')
        gte_constraints = self._constraints.get('>=')
        self._objective_row += [0] * (self._gte_constraints_counter * 2 +
                                      self._lte_constraints_counter +
                                      self._e_constraints_counter + 1)
        # Строим матрицу коэфициентов
        self._rows = []
        if gte_constraints is not None:
            for idx, constraint in enumerate(gte_constraints):
                expression = list(constraint[:-2])
                value = constraint[-1]
                row = [0] * (len(self._objective_row) - 1 - len(expression))
                row[idx*2] = -1
                row[idx*2+1] = 1
                self._rows.append(expression+row+[value])
                # Заносим строку и столбец в список искусственных
                self._temporary_rows.append(len(self._rows) - 1)
                self._temporary_cols.append((len(self._target_multipliers)) + idx * 2 + 1)
        if e_constraints is not None:
            for idx, constraint in enumerate(e_constraints):
                expression = list(constraint[:-2])
                value = constraint[-1]
                row = [0]*(len(self._objective_row) - 1 - len(expression))
                row[idx + self._gte_constraints_counter * 2] = 1
                self._rows.append(expression+row+[value])
                # Заносим строку в список искусственных
                self._temporary_rows.append(len(self._rows)-1)
                self._temporary_cols.append(len(self._target_multipliers) + idx +
                                            self._gte_constraints_counter * 2)
        if lte_constraints is not None:
            for idx, constraint in enumerate(lte_constraints):
                expression = list(constraint[:-2])
                value = constraint[-1]
                row = [0] * (len(self._objective_row) - 1 - len(expression))
                row[idx + self._gte_constraints_counter * 2 + self._e_constraints_counter] = 1
                self._rows.append(expression+row+[value])
        rows = self._rows
        for row in rows:
            for i, col in enumerate(row):
                row[i] = float(col)
        i = 1
        while not self._check_solution_optimal():
            debug("STEP %s" % (i, ))
            print("STEP %s" % (i, ))
            for row in self._rows:
                debug(row)
                print(row)
            debug(self._objective_row)
            print(self._objective_row)
            # return
            pivot_col = self._get_pivot_col()
            pivot_row = self._get_pivot_row(pivot_col)
            print(pivot_col, pivot_row)
            if pivot_col <= len(self._target_multipliers)-1:
                self._involved_in_basis[pivot_col] = pivot_row
            self._pivot(pivot_row, pivot_col)
            i += 1
        debug("FINISHED")
        # Улучшение плана завершено.
        # Ищем вовлеченные в базис переменные и ответ
        x_values = []
        for row in self._rows:
            debug(row)
            print(row)
        debug(self._objective_row)
        print(self._objective_row)
        z_value = self._objective_row[-1]
        # Если ищется минимум ЦФ, инвертируем значение Z
        if not self._is_max:
            z_value = -z_value
        for i in self._involved_in_basis:
            if i is not None:
                x_values.append(self._rows[i][-1])
            else:
                x_values.append(0)
        return x_values, z_value

    def add_target_variable(self, multiplier):
        """Добавляет переменную в целевую функцию, ожидает на входе коэффициент этой
        переменной"""
        if self._target_multipliers is None:
            self._target_multipliers = []
        self._target_multipliers.append(float(multiplier))

    def add_constraint(self, *args):
        """Добавляет ограничение. Ожидает на входе коэфициенты неравенства, знак и
        правую часть неравенства. Например add_constraint(1,2,3,'<=',4) будет
        интерпретировано, как 1x + 2y + 3z <= 4"""
        if self._target_multipliers is None or len(self._target_multipliers) < 2:
            raise SimplexSolverException('Сначала добавьте переменные целевой функции')
        if len(args) != len(self._target_multipliers) + 2:
            raise SimplexSolverException(
                f"Количество аргументов не соответствует целевой функции."
                f"Ожидается {len(self._target_multipliers)} коэффициентов, знак неравенства и правая часть"
            )
        sign = args[-2]
        if sign not in self.valid_inequality_signs:
            raise SimplexSolverException('Недопустимый знак неравенства')
        if self._constraints is None:
            self._constraints = {}
        sign_constraints = self._constraints.get(sign, [])
        sign_constraints.append(args)
        self._constraints[sign] = sign_constraints
        self._constraints_counter += 1
        if sign == '=':
            self._e_constraints_counter += 1
        elif sign == '>=':
            self._gte_constraints_counter += 1
        elif sign == '<=':
            self._lte_constraints_counter += 1

    def solve_maximize(self):
        """Поиск максимума целевой функции"""
        self._is_max = True
        return self._solve()

    def solve_minimize(self):
        """Поиск минимума целевой функции"""
        self._is_max = False
        return self._solve()




def run():
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
    ai = list()
    bj = list()
    tij = list()
    aij = list()
    cij = list()
    for i in range(m):
        string = "Введите a" + str((i+1)) + ": "
        ai.append(float(input(string)))

    for j in range(n):
        string = "Введите b" + str((j + 1)) + ": "
        bj.append(float(input(string)))

    for i in range(m):
        lst1 = list()
        lst2 = list()
        lst3 = list()
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
    for ci in cij:
        for c in ci:
            string = string + " " + str(c)

    print(string)


run()