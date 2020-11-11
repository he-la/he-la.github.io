from math import *
import random

from manim import *
import manim

from scipy.interpolate import CubicSpline
import numpy as np

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK


def zigzag(t):
    t = t % 2
    return t if t < 1 else 2 - t


class RepresentationPower(Scene):
    def construct(self):
        left = 5 * LEFT
        right = 5 * RIGHT

        red_start = Dot(color=RED).move_to(left + 2 * UP)
        red_end = Dot(color=RED).move_to(right + 2 * DOWN)
        start_one = MathTex('1').move_to(red_start).align_to(red_start, RIGHT).shift(0.25 * LEFT)
        end_zero = MathTex('0').move_to(red_end).align_to(red_end, LEFT).shift(0.25 * RIGHT)

        blue_start = Dot(color=BLUE).move_to(left + 2 * DOWN)
        blue_end = Dot(color=BLUE).move_to(right + 2 * UP)
        start_zero = MathTex('0').move_to(blue_start).align_to(blue_start, RIGHT).shift(0.25 * LEFT)
        end_one = MathTex('1').move_to(blue_end).align_to(blue_end, LEFT).shift(0.25 * RIGHT)

        time_arrow = Arrow(left + LEFT + 3 * DOWN, right + RIGHT + 3 * DOWN)
        time_label = MathTex("t").move_to(time_arrow.get_end() + 0.5 * RIGHT)

        self.play(
            LaggedStart(
                ShowCreation(red_start),
                ShowCreation(start_one),
                ShowCreation(red_end),
                ShowCreation(end_zero),
                ShowCreation(blue_start),
                ShowCreation(start_zero),
                ShowCreation(blue_end),
                ShowCreation(end_one),
                ShowCreation(time_arrow),
                ShowCreation(time_label),
            ))

        random.seed(9924)
        t_intersect = 0
        ys_red_rand = [random.random(), random.random()]
        ys_blue_rand = [random.random(), random.random()]

        def move_intersect(t_intersect):
            t_1 = 0.5 * (-5 + t_intersect)
            t_2 = 0.5 * (5 + t_intersect)

            def coord(x, y, z=0):
                return np.array([x, y, z])

            ts = [t_1, t_intersect, t_2]
            ys_red = [
                coord(_t, 2 - 4 * (_t + 5) / 10 + r - 0.5)
                for _t, r in zip([t_1, t_2], ys_red_rand)
            ]
            ys_blue = [
                coord(_t, -2 + 4 * (_t + 5) / 10 + r - 0.5)
                for _t, r in zip([t_1, t_2], ys_blue_rand)
            ]

            red_path = VMobject(color=RED)
            red_path.set_points_smoothly([
                red_start.get_center(), ys_red[0],
                coord(t_intersect, 0), ys_red[1],
                red_end.get_center()
            ])
            blue_path = VMobject(color=BLUE)
            blue_path.set_points_smoothly([
                blue_start.get_center(), ys_blue[0],
                coord(t_intersect, 0), ys_blue[1],
                blue_end.get_center()
            ])

            intersect = Dot(color=BLACK).move_to(coord(t_intersect, 0))

            return red_path, blue_path, intersect

        red_path, blue_path, intersect = move_intersect(t_intersect)
        self.play(
            LaggedStart(ShowCreation(red_path), ShowCreation(blue_path),
                        ShowCreation(intersect)))

        _t = 2

        def update_intersect(mobj, dt):
            nonlocal _t, t_intersect, red_path, blue_path, intersect

            _t += dt
            t_intersect = 6 * smooth(zigzag(_t / 4)) - 3

            self.remove(red_path, blue_path, intersect)
            red_path, blue_path, intersect = move_intersect(t_intersect)
            self.add(red_path, blue_path, intersect)

        red_start.add_updater(update_intersect)
        self.wait(8)
        red_start.remove_updater(update_intersect)

        def odefunc(point):
            x = point[0]
            y = point[1]
            return np.array([1, -y / 2, 0])

        vector_field = VectorField(odefunc)
        self.play(ShowCreation(vector_field))

        joint_path = VMobject(color=GREEN)
        joint_path.set_points_as_corners([
            intersect.get_center(),
            right,
        ])
        self.play(ShowCreation(joint_path))

        self.wait(2)
