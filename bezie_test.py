from geomdl import NURBS
from geomdl import utilities
from geomdl import Multi
from geomdl.visualization import VisMPL
import math


def create_curve(N):
    print('Start create curve: ')
    P = list()
    a = math.pi / N
    for i in range(N + 1):
        P.append([round(math.cos(2 * i * a), 3), round(math.sin(2 * i * a), 3)])
        P.append([round(math.cos((2 * i * a + a)) * (1 / math.cos(a)), 3),
                  round(math.sin((2 * i * a + a)) * (1 / math.cos(a)), 3)])

    P.pop()
    print(P)
    return P


def create_bezie_curve(p0, p1, p2, w):
    curve = NURBS.Curve()
    curve.degree = 2
    curve.ctrlpts = [p0, p1, p2]
    curve.weights = [1, w, 1]
    curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))
    curve.sample_size = 200
    curve.evaluate()

    return curve


def run(N):
    N = N
    circle = create_curve(N)
    print(circle)
    weight = math.cos(math.pi / N)
    cv = Multi.MultiCurve()
    k = 0
    while k < len(circle) - 1:
        cv.add(create_bezie_curve(circle[k], circle[k + 1], circle[k + 2], weight))
        k = k + 2
    vis_compl = VisMPL.VisCurve2D()
    cv.vis = vis_compl
    cv.render()


run(3)