from math import *
import random

from manim import *
import manim

from scipy.interpolate import CubicSpline

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK


def zigzag(t):
    t = t % 2
    return t if t < 1 else 2 - t


class Car(Scene):
    def construct(self):
        dxdt = lambda t: 1. / (1 + (t - 0.5)**2)
        xt = lambda t: -1.0784 * atan(0.5 - t)

        time_arrow = Arrow(5 * LEFT + UP, 5 * RIGHT + UP)
        time_label = MathTex("t").move_to(time_arrow.get_end()).align_to(
            time_arrow.get_end(), LEFT).shift(0.25 * RIGHT)

        pos_arrow = Arrow(5 * LEFT + 3 * DOWN, 5 * RIGHT + 3 * DOWN)
        pos_label = MathTex("x").move_to(pos_arrow.get_end()).align_to(
            pos_arrow.get_end(), LEFT).shift(0.25 * RIGHT)

        car = SVGMobject('car.svg').set_height(1)
        car.move_to(pos_arrow.get_end()).align_to(pos_arrow.get_end(),
                                                  DOWN + RIGHT).shift(0.5 * UP)
        car_end = car.get_center()
        car.move_to(pos_arrow.get_start()).align_to(
            pos_arrow.get_start(), DOWN + LEFT).shift(0.5 * UP)
        car_start = car.get_center()

        dxdt_plot = ParametricFunction(
            lambda t: np.array([t, dxdt(t), 0]), xmin=0, xmax=1,
            color=BLUE).set_width(
                time_arrow.get_width(),
                stretch=True).set_height(1, stretch=True).align_to(
                    time_arrow.get_start(), LEFT + DOWN).shift(0.25 * UP)
        dxdt_label = MathTex('\\frac{d}{dt} x = f(x(t), t)',
                             color=BLUE).move_to(time_arrow.get_end() + 2 * UP)

        _t = 0
        rate = 0.5

        def get_integral(symbolic=False):
            nonlocal _t
            if not symbolic:
                t = '%.2f' % zigzag(_t)
            else:
                t = 't'
            return MathTex(
                'x(%s) = x(0) + \\int_0^{%s} \\frac{d}{d\\tau} f(x(\\tau), \\tau) d\\tau'
                % (t, t)).align_to(time_arrow.get_center(), UP).shift(0.5 * DOWN)

        integral = get_integral(True)

        self.play(
            LaggedStart(ShowCreation(time_arrow), ShowCreation(time_label),
                        ShowCreation(pos_arrow), ShowCreation(pos_label),
                        ShowCreation(car), ShowCreation(dxdt_plot),
                        ShowCreation(dxdt_label), ShowCreation(integral)))

        def get_dxdt_coords(t):
            start = time_arrow.get_start() + 0.25 * UP
            end = time_arrow.get_end() + 0.25 * UP
            return np.array([(1 - t) * start[0] + t * end[0],
                             start[1] + (dxdt(t) - dxdt(0)) / (1 - dxdt(0)),
                             0])

        def get_xt_coords(t):
            return np.array([(1 + xt(0) - xt(t)) * car_start[0] +
                             (xt(t) - xt(0)) * car_end[0], car_start[1], 0])

        dot = Dot(color=BLUE).move_to(get_dxdt_coords(0))

        def update_dot(dot, dt):
            nonlocal _t
            _t += rate * dt
            t = zigzag(_t)
            dot.move_to(get_dxdt_coords(t))

        def get_area():
            t = zigzag(_t)
            mesh = np.linspace(0, t, int(t * 50) + 2)
            final = get_dxdt_coords(0).copy()
            final[0] = get_dxdt_coords(t)[0]
            points = [get_dxdt_coords(t) for t in mesh] + [
                final, get_dxdt_coords(0)
            ]
            area = VMobject(stroke_color=None, stroke_opacity=0.0,
                            fill_color=BLUE, fill_opacity=0.3)
            area.set_points_as_corners(points)
            return area

        area = always_redraw(get_area)

        def update_car(car, dt):
            t = zigzag(_t)
            car.move_to(get_xt_coords(t))

        self.remove(integral)
        integral = always_redraw(get_integral)
        dot.add_updater(update_dot)
        car.add_updater(update_car)
        self.add(dot, area, integral)

        self.wait(10)
