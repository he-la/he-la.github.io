from math import *
import random

from manim import *
import manim

from scipy.interpolate import CubicSpline
import numpy as np

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK
config["frame_height"] = 10
config["frame_width"] = 10


class SpiralODE(MovingCameraScene):
    def construct(self):
        ode = np.array([[-0.2, -1.0], [1.0, -0.2]])
        ode3d = np.array([[-0.2, -1.0, 0], [1.0, -0.2, 0], [0, 0, 0]])

        ode3d_func = lambda pt: ode3d @ pt

        vector_field = VectorField(ode3d_func)

        self.add(vector_field)

        dot = Dot(color=BLUE).move_to(4.5 * RIGHT + 4 * UP)
        traj = VMobject(color=BLUE)
        traj.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_dot(dot, dt):
            # euler step
            dot.move_to(dot.get_center() + dt * ode3d @ dot.get_center())
            traj.add_points_as_corners([dot.get_center()])

        dot.add_updater(update_dot)
        self.add(traj, dot)

        self.wait(30)
