from manim import *

from math import *

from scipy.interpolate import BarycentricInterpolator

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK


class RungeKuttaStep(GraphScene, MovingCameraScene):
    CONFIG = {
        "x_axis_label": "t",
        "y_axis_label": "",
        "y_min": -3,
        "y_max": 4,
        "graph_origin": ORIGIN + DOWN + 5 * LEFT,
    }

    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.camera_frame.save_state()

        X_MAX = 3 * PI

        def f(x):
            return cos(x) + 0.3 * sin(x) + cos(1.2 * x) - 3 * sin(1.4 * x) +\
                2 * cos(2 * x)

        interp_points = [0.2, 0.3, 0.4]
        poly = BarycentricInterpolator(interp_points,
                                       [f(x) for x in interp_points])

        self.setup_axes(animate=False)
        func_graph = self.get_graph(f, x_min=0, x_max=X_MAX)
        func_label = self.get_graph_label(func_graph, label="\\frac{d}{dt}x")

        poly_graph = self.get_graph(poly, x_min=0, x_max=X_MAX)
        area = self.get_area(poly_graph, interp_points[0], interp_points[-1])

        self.play(ShowCreation(func_graph), ShowCreation(func_label))

        dot = Dot().move_to(
            self.coords_to_point(interp_points[0], f(interp_points[0])))
        dots = [
            Dot(color=RED).move_to(self.coords_to_point(p, f(p)))
            for p in interp_points[1:]
        ]
        self.play(ShowCreation(dot))

        # func_graph2 = self.get_graph(f, x_min=0, x_max = 1)
        # self.play(Transform(func_graph, func_graph2))

        x_axis_l = self.x_axis.get_left()
        func_l = func_graph.get_left()

        def shift_x(mobj):
            mobj.set_x(X_MAX * mobj.get_x() + func_l[0] * (1 - X_MAX))

        self.play(func_graph.set_width, X_MAX * func_graph.get_width(), True,
                  func_graph.align_to, func_l, LEFT, self.x_axis.set_width,
                  X_MAX * self.x_axis.get_width(), True, self.x_axis.align_to,
                  x_axis_l, LEFT, dot.set_x,
                  X_MAX * dot.get_x() + func_l[0] * (1 - X_MAX))

        for d in dots:
            shift_x(d)
            self.play(ShowCreation(d))

        poly_graph.set_width(X_MAX * poly_graph.get_width(), True)
        poly_graph.align_to(func_l, LEFT)

        self.play(ShowCreation(poly_graph))

        area.set_color(poly_graph.get_color())
        area.set_width(X_MAX * area.get_width(), True)
        shift_x(area)
        self.play(ShowCreation(area))
