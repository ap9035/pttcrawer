# -*- coding: utf-8 -*-

"""
    檔案名稱：Interpolation.py

    目的：使用內插法計算函數值

    輸入資料：
         存有資料點的檔案
         格點數
         計算範圍
         變數值

    輸出資料：
         位於輸入值處的函數值

    作者：
        李建德

    撰寫日期：
        2015/12/16

    使用限制：
        輸入資料必須事先以由小到大的方式排序好

    版權沒有，翻印不究
"""

# 引入函式庫
import numpy
import sys


"""
    class Interpolator，用於儲存資料點，會在初始化時計算範圍內
    所有格點上的函數值，並儲存起來，之後使用上萬次不用每次都重
    新計算內插法的數值

"""


class Interpolator:
    def __init__(self, data, construct, N, r):
        self.r = r
        self.X = numpy.linspace(r[0], r[1], num=N)
        self.Y = numpy.zeros(N)
#   使用輸入的內插法函數，計算所有函數值
        for i, x in enumerate(self.X):
            self.Y[i] = construct(data, x)

#   回傳數值用的函數

    def f(self, x):
        if x > self.r[1] or x < self.r[0]:
            print "out of range"
            return
        for i, X in enumerate(self.X):
            if x == X:
                return self.Y[i]
            if x < X:
                return self.Y[i-1]

"""
    Lagrange 函數
    演算法參考：https://en.wikipedia.org/wiki/Lagrange_polynomial
"""


def Lagrange(data, x):
    foo = 0
    for j, xy in enumerate(data):
        foo += Lagrange_basis(data, x, j)*xy[1]
    return foo


def Lagrange_basis(data, x, j):
    foo = 1
    xj = data[j, 0]
    for m, xy in enumerate(data):
        if m == j:
            continue
        xm = xy[0]
        foo *= (x-xm)/(xj-xm)
    return foo


def Newton(data, x):
    foo = 0
    for j, xy in enumerate(data):
        foo += Newton_basis(data, x, j)*Divided_difference(
            data[:j+1]
        )
    return foo


def Divided_difference(data):
    N = len(data)
    if N == 1:
        return data[0, 1]
    else:
        foo = Divided_difference(data[1:])-Divided_difference(data[:-1])
        foo /= (data[-1, 0]-data[0, 0])
        return foo


def Newton_basis(data, x, j):
    foo = 1
    for i, xy in enumerate(data[:j]):
        xi = xy[0]
        foo *= x-xi
    return foo

"""
    線性內插法函數
    演算法參考：https://en.wikipedia.org/wiki/Interpolation
"""


def Linear(data, x):
    length = len(data)
    for i in range(1, length):
        X = data[i, 0]
        Y = data[i, 1]
        pX = data[i-1, 0]
        pY = data[i-1, 1]
        if x == X:
            return Y
        elif X > x:
            return pY+(Y-pY)*(x-pX)/(X-pX)
    return pY+(Y-pY)/(X-pX)*(x-pX)


def Neivlle(data, x):
    N = len(data)
    return Neivlle_basis(data, 0, N-1, x)


def Neivlle_basis(data, i, j, x):
    if i == j:
        return data[i, 1]
    else:
        retvar = (
            (data[j, 0]-x)*Neivlle_basis(data, i, j-1, x)+(
                x-data[i, 0])*Neivlle_basis(
                data, i+1, j, x)
        )/(
            data[j, 0]-data[i, 0]
        )
        return retvar

if __name__ == '__main__':
    data = numpy.loadtxt(sys.argv[1])
    print Lagrange(data, float(sys.argv[2]))
#    print Newton(data, 15)
#    print Lagrange(data, 15)
#    print Linear(data, 15)
#    A = Interpolator(
#        data, Newton, 100, [float(sys.argv[3]), float(sys.argv[4])])
#    print A.f(float(sys.argv[2]))
#    data2 = numpy.loadtxt("test2.dat")
#    B = Interpolator(data2, Lagrange, 1000000, [-100, 100])
#    print B.f(32)
