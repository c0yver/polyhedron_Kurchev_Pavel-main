from math import pi
from math import sqrt
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes

    # def _vert(self, k):
    #     n = (self.vertexes[k] - self.vertexes[k - 1]).cross(Polyedr.V)
    #     return n * \
    #         (-1.0) if n.dot(self.vertexes[k - 1] - self.center()) < 0.0 else n

    # # Центр грани
    # def center(self):
    #     return sum(self.vertexes, R3(0.0, 0.0, 0.0)) * \
    #         (1.0 / len(self.vertexes))


class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):

        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []
        # сумма площадей граней, которые содержат хорошую точу
        self.sum = 0

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    self.c = c
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    def is_good_point(self, x, y, z):
        return x*x + y*y + z*z < 4

    def sum_area(self):
        k = False
        t = 0
        for facet in self.facets:
            t += len(facet.vertexes)-1
            for vertex in facet.vertexes:
                if self.is_good_point(vertex.x, vertex.y, vertex.z):
                    k = True
            if k == True:
                # формула Гауса для площади многоугольника
                sum1 = 0
                sum2 = 0
                for i in range(len(facet.vertexes)-1):
                    sum1 += facet.vertexes[i].x*facet.vertexes[i+1].y + facet.vertexes[len(facet.vertexes)-1].x*facet.vertexes[0].y
                    sum2 += facet.vertexes[i+1].x*facet.vertexes[i].y - facet.vertexes[0].x*facet.vertexes[len(facet.vertexes)-1].y
                
                # for i in range(len(facet.vertexes)):
                #     print('---', facet.vertexes[i].x, facet.vertexes[i].y, facet.vertexes[i].z)

                n_ver = facet.vertexes[t].cross(facet.vertexes[t-1])
                p_ver = R3(n_ver.x, n_ver.y, 0.0)

                corner = (n_ver.dot(p_ver))/(sqrt(n_ver.x*n_ver.x + n_ver.y*n_ver.y + n_ver.z*n_ver.z) \
                    *sqrt(p_ver.x*p_ver.x + p_ver.y*p_ver.y + p_ver.z*p_ver.z))
                corner = sqrt(1 - corner*corner)

                # print(sum1, sum2, corner)

                if corner == 0:
                    area = 0.5*(abs(sum1 - sum2)/(self.c*self.c))
                else:
                    area = (0.5*(abs(sum1 - sum2)/(self.c*self.c)))/corner 

                # area = (facet.vertexes[1] - facet.vertexes[0]).cross(facet.vertexes[2] - facet.vertexes[0]) + \
                #  (facet.vertexes[1] - facet.vertexes[3]).cross(facet.vertexes[2] - facet.vertexes[3])
                self.sum += area
            k = False

        return self.sum

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)
