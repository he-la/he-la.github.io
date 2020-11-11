from math import *
import random

from manim import *
import manim

from scipy.interpolate import CubicSpline
from scipy.integrate import odeint
import numpy as np

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK
config["frame_height"] = 10
config["frame_width"] = 10

class SpiralSample(Scene):
    def construct(self):
        ode = np.array([[-0.2, -1.0], [1.0, -0.2]])
        ode_func = lambda x, _: ode @ x
        
        ode3d = np.array([[-0.2, -1.0, 0], [1.0, -0.2, 0], [0, 0, 0]])
        ode3d_func = lambda pt: ode3d @ pt

        vector_field = VectorField(ode3d_func)

        self.add(vector_field)

        def to_3d(arr):
            return np.append(arr, np.zeros((arr.shape[0], 1)), axis=1)

        traj = VMobject(color=BLUE)
        traj.set_points_as_corners(to_3d(
            odeint(ode_func, np.array([4.5, 4]), np.linspace(0, 30, 200))))

        dots = to_3d(odeint(ode_func, np.array([4.5, 4]), np.linspace(0, 20, 50)))
        np.random.seed(41234)
        noise = to_3d(np.random.multivariate_normal([0,0],[[0.025, 0],
                                                     [0, 0.025]], 80))
        dots = VGroup(*[Dot(color=GREEN).move_to(p + n) for p, n in zip(dots, noise)])

        self.add(traj)

        self.wait()
        self.play(ShowCreation(dots))
