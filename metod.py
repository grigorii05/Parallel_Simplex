from copy import deepcopy
import pandas as pd
from numba import njit, set_num_threads
import time

@njit(parallel=True)
def findBaseSolution(b, c, table):
    for el in range(0, len(b)):  # Проверка на допустимость решения
        if (table[el][0] < 0):
            for i in range(0, len(c)):
                if (table[el][i + 1] < 0):
                    return [el, i + 1]
    return []

class Simplex:

    def __init__(self, c, a, b):
        self.c = c
        self.a = a
        self.b = b
        self.table = []

        for i in range(0, len(self.b)):
            self.table.append([b[i]] + a[i])

        self.table.append([0] + c)
        self.string1 = ["s0"]
        for i in range(0, len(c)):
            self.string1.append('x' + str(i + 1))

        self.string2 = []
        for i in range(0, len(b)):
            self.string2.append('x' + str(len(c) + i + 1))
        self.string2.append('F')

        print("Finish init")


    def findResolvingColumn(self):

        indexOfResolvingColumn = 0
        for i in range(0, len(self.c)):
            if (self.table[-1][i + 1] > 0):
                indexOfResolvingColumn = i + 1
                break

        return indexOfResolvingColumn

    # findResolvingString - функция нахождения разрешающей строки, использующая найденный ранее разрешающий столбец

    def findResolvingString(self, indexOfResolvingColumn):

        # listOfIndices - список, в который мы положим индексы тех строк, значения элементов разрешающего столбца которых не равны нулю. Это нужно для того,
        # чтобы избежать деления на ноль
        #
        # listOfValues - список,в который мы положим значения b/a для каждой строки, где a - элемент разрешающего столбца, а b - элемент столбца свободных
        # членов

        listOfIndices = []
        listOfValues = []

        indexOfResolvingString = 0

        for i in range(0, len(self.b)):
            if (self.table[i][indexOfResolvingColumn] != 0):
                listOfValues.append(self.table[i][0]/self.table[i][indexOfResolvingColumn])
                if (listOfValues[len(listOfValues) - 1] <= min(listOfValues)):
                    indexOfResolvingString = i

        return indexOfResolvingString

    def findResolvingElement(self):
        resolvingColumn = self.findResolvingColumn()
        resolvingString = self.findResolvingString(resolvingColumn)

        return [resolvingString, resolvingColumn]

    """
    @njit(parallel=True)
    def findBaseSolution(self):
        for el in range(0, len(self.b)): # Проверка на допустимость решения
            if (self.table[el][0] < 0):
                for i in range(0, len(self.c)):
                    if (self.table[el][i + 1] < 0):
                        return [el, i + 1]
        return []
    """

    def findOptSolution(self):
        for i in range(1, len(self.table[-1])):
            if (self.table[-1][i] > 0):
                return 1
        return 0

    def JordanExceptionsStep(self, resolvingElement):
        r = resolvingElement[0]
        k = resolvingElement[1]
        # Преобразуем разрешающую строку, выводим результат

        new_table = deepcopy(self.table)
        if (new_table[r][k] != 0):
            new_table[r][k] = 1/self.table[r][k]
        for j in range(0 ,len(self.table[0])):
            if (j != k):
                new_table[r][j] = self.table[r][j]/self.table[r][k]

        for i in range(0, len(self.table)):
            if (i != r):
                new_table[i][k] = (-1)*(self.table[i][k]/self.table[r][k])

        for i in range(0, len(self.table)):
            if (i != r):
                for j in range(0, len(self.table[0])):
                    if (j != k):
                        new_table[i][j] = self.table[i][j] - self.table[i][k]*self.table[r][j]/self.table[r][k]

        self.table = new_table
        buf = self.string1[k]
        self.string1[k] = self.string2[r]
        self.string2[r] = buf

    def RunSimplex(self):

        Solution = [1]
        resolvingElement = [0, 0]
        self.printTable()

        set_num_threads(2)
        while Solution != []:
            #Solution = self.findBaseSolution()
            Solution = findBaseSolution(self.b, self.c, self.table)
            if(Solution != []):
                self.JordanExceptionsStep(Solution)
                self.printTable()

        while self.findOptSolution():
            resolvingElement = self.findResolvingElement()
            self.JordanExceptionsStep(resolvingElement)
            self.printTable()


        print("     Оптимальное решение: \n")
        for i in range(0, len(self.table) - 1):
           print (self.string2[i] + " = ", self.table[i][0])
        print("F = " , self.table[len(self.b)][0])

    def printTable(self):
        print("_____")
        df = pd.DataFrame(self.table, columns=self.string1, index=self.string2)
        print(df)
        print("_____")
