from math import *
import random

from manim import *
import manim

from scipy.interpolate import CubicSpline

import colour

Mobject.CONFIG['color'] = "#657b83"
Dot.CONFIG['color'] = PINK


class LatentODE(Scene):
    def construct(self):
        data_time_arrow = Arrow(
            ORIGIN + 5.5 * LEFT + 3 * UP,
            ORIGIN + 5.5 * RIGHT + 3 * UP,
        )
        data_time_label = MathTex("t").move_to(data_time_arrow.get_end() +
                                               0.5 * RIGHT)

        self.play(
            LaggedStart(ShowCreation(data_time_arrow),
                        ShowCreation(data_time_label)))

        random.seed(4299)
        t = [1.5 * i + 0.8 * random.random() for i in range(5)]

        def make_x(i):
            dot = Dot(color=BLUE).move_to(data_time_arrow.get_start() +
                                          t[i] * RIGHT)
            label = MathTex("\\mathbf{x_%d}" % i).move_to(dot).align_to(
                dot, DOWN).shift(0.25 * UP)
            return VGroup(dot, label)

        xs = VGroup(*[make_x(i) for i in range(len(t))])

        self.play(LaggedStart(*[ShowCreation(x) for x in xs.submobjects]))

        rnn_brace = Brace(VGroup(xs[0].submobjects[0], xs[-1].submobjects[0]),
                          direction=DOWN).shift(0.125 * UP)
        rnn_text = rnn_brace.get_text("RNN")
        rnn_frame = Rectangle(color=rnn_text.get_color()).surround(
            rnn_text, stretch=True)
        rnn = VGroup(rnn_text, rnn_frame)
        self.play(LaggedStart(ShowCreation(rnn_brace), ShowCreation(rnn)))

        rnn_out_arrow = Arrow(rnn.get_bottom() + 0.25 * UP,
                              rnn.get_bottom() + 0.75 * DOWN)
        rnn_out_params = MathTex(
            "\\mathbb{P}[\\mathbf{z}(0) \\mid \\mathbf{x_0}, \\ldots, \\mathbf{x_%d}]"
            % (len(t) - 1)).move_to(rnn_out_arrow.get_end()).align_to(
                rnn_out_arrow.get_end(), UP)
        self.play(
            LaggedStart(ShowCreation(rnn_out_arrow),
                        ShowCreation(rnn_out_params)))

        space_sep = DashedLine(ORIGIN + 5.5 * LEFT, ORIGIN + 5.5 * RIGHT)
        data_space_label = Tex("\\tiny Data Space").move_to(
            space_sep).align_to(space_sep, DOWN).shift(0.125 * UP)
        latent_space_label = Tex("\\tiny Latent Space").move_to(
            space_sep).align_to(space_sep, UP).shift(0.125 * DOWN)
        space_sep = VGroup(space_sep, data_space_label, latent_space_label)

        latent_time_arrow = Arrow(
            ORIGIN + 5.5 * LEFT + 3 * DOWN,
            ORIGIN + 5.5 * RIGHT + 3 * DOWN,
        )
        latent_time_label = MathTex("t").move_to(latent_time_arrow.get_end() +
                                                 0.5 * RIGHT)

        sampling_arrow = VMobject()
        p1 = rnn_out_params.get_bottom()
        p1[1] = data_space_label.get_y().copy()
        p2 = p1.copy()
        p2[0] = xs[0].submobjects[0].get_x()
        p3 = xs[0].submobjects[0].get_center().copy()
        p3[1] = latent_time_arrow.get_y()
        sampling_arrow.set_points_as_corners(
            [rnn_out_params.get_bottom(), p1, p2, p3])
        sampling_arrow_tip = manim.mobject.geometry.ArrowTriangleFilledTip(
            color=sampling_arrow.get_color()).rotate(
                PI / 2).move_to(p3).align_to(p3, DOWN)

        sampling_arrow = VGroup(sampling_arrow, sampling_arrow_tip)

        def make_z(i):
            dot = Dot(color=BLUE).move_to(latent_time_arrow.get_start() +
                                          t[i] * RIGHT)
            label = MathTex("\\mathbf{z_%d}" % i).move_to(dot).align_to(
                dot, UP).shift(0.25 * DOWN)
            return VGroup(dot, label)

        z0_dot = Dot(color=GREEN).move_to(latent_time_arrow.get_start() +
                                          t[0] * RIGHT)
        z0_label = MathTex("\\mathbf{z_0}").move_to(z0_dot).align_to(
            z0_dot, UP).shift(0.25 * DOWN)
        z0 = VGroup(z0_dot, z0_label)

        self.play(
            LaggedStart(ShowCreation(sampling_arrow), ShowCreation(z0),
                        ShowCreation(space_sep)))

        self.play(
            LaggedStart(
                ShowCreation(latent_time_arrow),
                ShowIncreasingSubsets(z0),
                ShowCreation(latent_time_label),
            ))

        left = (latent_time_arrow.get_start() + t[1] * RIGHT)[0]
        right = (latent_time_arrow.get_end() + 1 * LEFT)[0]

        travelling_z_dot = Dot(
            color=GREEN).move_to(latent_time_arrow.get_start() + t[1] * RIGHT).set_x(0.5 * (left + right))
        travelling_z_label = MathTex("\\mathbf{z}(t)").move_to(
            travelling_z_dot).align_to(travelling_z_dot, DOWN).shift(0.25 * UP)

        zgroup = VGroup(travelling_z_dot, travelling_z_label)

        _zt = 0
        def travel_z(zgroup, dt):
            nonlocal _zt
            _zt += dt
            alpha = 0.5 * (sin(_zt) + 1)
            zgroup.set_x((1 - alpha) * left + alpha * right)

        self.play(ShowCreation(zgroup))

        travelling_z_arrow = Arrow(travelling_z_label.get_top() + 0.125 * DOWN,
                                   travelling_z_label.get_top() + 0.875 * UP)
        travelling_z_decode_label = MathTex("\\mathbb{P}[\\mathbf{x}(t) \\mid \\mathbf{z}(t)]").move_to(travelling_z_arrow.get_end()).align_to(travelling_z_arrow.get_end(), DOWN).shift(0.125 * UP)
        x = travelling_z_decode_label.get_top().copy()
        x[1] = data_time_arrow.get_y()
        travelling_z_decode = Arrow(travelling_z_decode_label.get_top(), x,
                                    color=GREEN)
        travelling_x_dot = Dot(color=GREEN).move_to(x)
        travelling_x_label = MathTex("\\mathbf{x}(t)").move_to(travelling_x_dot).align_to(travelling_x_dot, DOWN).shift(0.25 * UP)

        decode_group = VGroup(
            travelling_z_arrow, travelling_z_decode_label, travelling_z_decode,
            travelling_x_dot, travelling_x_label
        )
        
        
        self.play(ShowCreation(decode_group))
        self.remove(decode_group)
        zgroup.add(decode_group)
        zgroup.add_updater(travel_z)

        self.wait(20)
