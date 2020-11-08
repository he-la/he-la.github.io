from math import *

from manim import *

from scipy.interpolate import CubicSpline

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK


class AdjointMethod(GraphScene):
    CONFIG = {
        "x_axis_label": "t",
        "y_axis_label": "",
    }

    def show_traj(self, traj_f, T_MAX, rate):
        dot = Dot().move_to(self.coords_to_point(0, traj_f(0)))
        label = MathTex("\\mathbf{x}(t)",
                        color=BLUE).move_to(dot).shift(0.5 * UP)
        path = VMobject(color=BLUE)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        _t = 0

        def update_dot(dot, dt):
            nonlocal _t

            _t += rate * dt
            t = smooth(_t / T_MAX) * T_MAX
            dot.move_to(self.coords_to_point(t, traj_f(t)))

            label.move_to(dot).shift(0.5 * UP)

            prev_path = path.copy()
            prev_path.add_points_as_corners([dot.get_center()])
            path.become(prev_path)

        dot.add_updater(update_dot)

        self.add(label, path, dot)
        self.wait(T_MAX / rate)

        dot.remove_updater(update_dot)
        self.remove(dot, path)

        traj = self.get_graph(traj_f, x_min=0, x_max=T_MAX, color=BLUE)
        label.move_to(self.coords_to_point(T_MAX,
                                           traj_f(T_MAX))).shift(0.5 * UP)
        self.add(traj)
        return traj

    def show_adj(self, adj_f, T_MAX, rate):
        dot = Dot().move_to(self.coords_to_point(T_MAX, adj_f(T_MAX)))
        label = MathTex("\\partial_\\theta L",
                        color=GREEN).move_to(dot).shift(0.5 * UP)
        path = VMobject(color=GREEN)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        _t = T_MAX

        def update_dot(dot, dt):
            nonlocal _t

            _t -= rate * dt
            t = smooth(_t / T_MAX) * T_MAX
            dot.move_to(self.coords_to_point(t, adj_f(t)))

            label.move_to(dot).shift(0.5 * UP)

            prev_path = path.copy()
            prev_path.add_points_as_corners([dot.get_center()])
            path.become(prev_path)

        dot.add_updater(update_dot)

        self.add(label, path, dot)
        self.wait(T_MAX / rate)

        dot.remove_updater(update_dot)
        self.remove(dot, path)

        traj = self.get_graph(adj_f, x_min=0, x_max=T_MAX, color=GREEN)
        label.move_to(self.coords_to_point(0, adj_f(0))).shift(0.5 * UP)
        self.add(traj)
        return traj

    def show_reverse_area(self, area_mobj):
        rects = [*area_mobj]
        rects.reverse()
        alpha = 0

        def update_area(area, dt):
            nonlocal alpha
            alpha += dt
            index, subalpha = integer_interpolate(0, len(rects), smooth(alpha))
            area.become(VGroup(*rects[0:index]))

        area = VGroup().add_updater(update_area)
        self.add(area)
        self.wait(1)
        self.remove(area)
        self.add(area_mobj)

    def construct(self):
        T_MAX = 10

        self.setup_axes(animate=False)

        random.seed(4299)
        traj_f = CubicSpline(list(range(T_MAX)),
                             [1 + random.random() for _ in range(T_MAX)],
                             extrapolate='periodic')
        adj_f = CubicSpline(list(range(T_MAX)),
                            [4 + 2 * random.random() for _ in range(T_MAX)],
                            extrapolate='periodic')

        traj = self.show_traj(traj_f, T_MAX, 2.5)
        adj = self.show_adj(adj_f, T_MAX, 2.5)

        traj_f_upper = lambda t: traj_f(t) + t / 30
        traj_f_lower = lambda t: traj_f(t) - t / 30
        traj_upper = self.get_graph(traj_f_upper, x_min=0, x_max=T_MAX)
        traj_lower = self.get_graph(traj_f_lower, x_min=0, x_max=T_MAX)
        traj_err_area = self.get_area(traj_upper,
                                      0,
                                      T_MAX,
                                      bounded=traj_lower,
                                      dx_scaling=0.2)
        traj_err_area.set_color(BLUE)
        self.play(ShowCreation(traj_err_area))

        adj_f_upper = lambda t: adj_f(t) + (2 * T_MAX - t) / 30
        adj_f_lower = lambda t: adj_f(t) - (2 * T_MAX - t) / 30
        adj_upper = self.get_graph(adj_f_upper, x_min=0, x_max=T_MAX)
        adj_lower = self.get_graph(adj_f_lower, x_min=0, x_max=T_MAX)
        adj_err_area = self.get_area(adj_upper,
                                     0,
                                     T_MAX,
                                     bounded=adj_lower,
                                     dx_scaling=0.2).set_color(GREEN)
        self.show_reverse_area(adj_err_area)

        self.wait(2)
