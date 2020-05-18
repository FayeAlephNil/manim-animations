#!/usr/bin/env python

from manimlib.imports import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        tex = TextMobject("This too fades, even as $\mathbb{R}$ remains")

        # These are applied before the animation starts

        tex.to_corner(UP + LEFT)
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        # The animations start here

        self.add(tex)

        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(FadeOut(circle, tex))

        grid = NumberPlane()
        self.play(ShowCreation(grid, run_time=3, lag_ratio=0.1))
        grid.prepare_for_nonlinear_transform()
        self.play(grid.apply_function, lambda p: np.array([-p[1], p[0], 0]), run_time=3)
        self.wait()


class Transform(Scene):
    CONFIG = {
        "plane_kwargs": {
            "x_line_frequency": 0.2,
            "y_line_frequency": 0.2,
            "background_line_style": {
                "stroke_color": GREEN_D,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
        }
    }

    def construct(self):
        grid = ComplexPlane(**self.plane_kwargs)
        circle = Circle(color=RED)
        self.play(ShowCreation(grid, run_time=3, lag_ratio=0.1))
        self.wait()
        self.play(ShowCreation(circle))
        grid.prepare_for_nonlinear_transform()
        self.wait()
        self.play(
            grid.apply_function,
            lambda p: np.array([p[0], -p[1], 0]) / (p[0] ** 2 + p[1] ** 2),
            run_time=3,
        )
        self.wait()


class IterTransform(Scene):
    CONFIG = {
        "plane_kwargs": {
            "x_line_frequency": 0.5,
            "y_line_frequency": 0.5,
            "background_line_style": {
                "stroke_color": GREEN_D,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
        }
    }

    def apply_func(p):
        c = np.array([-0.122565, 0.744864, 0])
        return c + np.array([p[0] ** 2 - p[1] ** 2, 2 * p[0] * p[1], 0])

    def go(self, grid, circle, func):
        grid.prepare_for_nonlinear_transform()
        self.wait()
        start_dot = circle.get_center()
        end_dot = func(start_dot)

        self.play(
            MoveAlongPath(circle, ArcBetweenPoints(start_dot, end_dot, 0)),
            grid.apply_function,
            lambda p: func(p),
            run_time=3,
        )
        return grid, circle

    def construct(self):
        grid = ComplexPlane(**self.plane_kwargs)
        circle = Dot(color=PINK)
        boundary = Circle(color=WHITE, radius=2)

        self.play(ShowCreation(grid, run_time=3, lag_ratio=0.1))
        self.wait()
        self.play(ShowCreation(circle))
        self.play(ShowCreation(boundary))
        grid.prepare_for_nonlinear_transform()
        for n in range(1, 10):
            grid, circle = self.go(grid, circle, IterTransform.apply_func)

        self.wait()
