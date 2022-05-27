from turtle import position
from manim import *


def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = np.linalg.norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func

class MakeBarMagnet(Scene):
    def construct(self):
        north_monopole = Circle()
        north_monopole.set_fill(opacity=0.5)
        self.play(Create(north_monopole))

        north_circle_label = Text("N")
        self.play(Write(north_circle_label))

        north_monopole_group = Group(north_monopole, north_circle_label)
        
        self.wait()

        # Monopole Field
        func = get_force_field_func(
            (ORIGIN, +1)
        )

        vector_field = ArrowVectorField(func)

        self.play(FadeIn(vector_field))

        self.wait()

        # Bar Magnet Field
        func = get_force_field_func(
            (3 * LEFT, +1), (3 * RIGHT, -1)
        )

        south_monopole = Circle(color=BLUE)
        south_monopole.set_fill(opacity=0.5)

        south_circle_label = Text("S")

        south_monopole_group = Group(south_monopole, south_circle_label)
        south_monopole_group.move_to(3 * RIGHT)

        monopole_to_bar_magnet_field = AnimationGroup(
            vector_field.animate.become(ArrowVectorField(func)),
            north_monopole_group.animate.shift(3 * LEFT),
            FadeIn(south_monopole_group)
        )
        
        self.play(monopole_to_bar_magnet_field)

        self.wait()

        north_monopole_bar_magnet = Rectangle(color=RED, width=4, height=2)
        north_monopole_bar_magnet.move_to(2 * LEFT)
        north_monopole_bar_magnet.set_fill(color=RED, opacity=0.5)


        south_monopole_bar_magnet = Rectangle(color=BLUE, width=4, height=2)
        south_monopole_bar_magnet.move_to(2 * RIGHT)
        south_monopole_bar_magnet.set_fill(color=BLUE, opacity=0.5)

        create_bar_magnet = AnimationGroup(
            Transform(north_monopole, north_monopole_bar_magnet),
            Transform(south_monopole, south_monopole_bar_magnet)
        )

        self.play(create_bar_magnet)
        
        self.wait()


def draw_bar_magnet(width=4, height=1, south_left=False):
    north_monopole_bar_magnet = Rectangle(color=RED, width=width/2, height=height)
    north_monopole_bar_magnet.move_to(width/4 * RIGHT if south_left else LEFT)
    north_monopole_bar_magnet.set_fill(color=RED, opacity=0.5)

    north_label = Text("N")
    north_label.move_to((width/2-1) * RIGHT if south_left else LEFT)


    south_monopole_bar_magnet = Rectangle(color=BLUE, width=width/2, height=height)
    south_monopole_bar_magnet.move_to(width/4 * LEFT if south_left else RIGHT)
    south_monopole_bar_magnet.set_fill(color=BLUE, opacity=0.5)

    south_label = Text("S")
    south_label.move_to((width/2-1) * LEFT if south_left else RIGHT)

    return Group(north_monopole_bar_magnet, north_label, south_monopole_bar_magnet, south_label)

class Repulsion(Scene):
    def construct(self):
        bar_magnet_one = draw_bar_magnet().move_to(4 * LEFT)
        bar_magnet_two = draw_bar_magnet(south_left=True).move_to(4 * RIGHT)

        create_bar_magnets = AnimationGroup(
            FadeIn(bar_magnet_one),
            FadeIn(bar_magnet_two)
        )

        self.play(create_bar_magnets)

        self.wait()

        func = get_force_field_func(
            (3 * LEFT, -1), (5 * LEFT, +1),
            (3 * RIGHT, -1), (5 * RIGHT, +1)
        )

        vector_field = ArrowVectorField(func)

        self.play(FadeIn(vector_field))

        self.wait()

        func = get_force_field_func(
            (3 * LEFT, -1), (5 * LEFT, +1),
            (3 * RIGHT, +1), (5 * RIGHT, -1)
        )

        flip_bar_magnet = AnimationGroup(
            Rotate(bar_magnet_two, PI),
            vector_field.animate.become(ArrowVectorField(func))
        )

        self.play(flip_bar_magnet)


        func = get_force_field_func(
            (1 * LEFT, -1), (3 * LEFT, +1),
            (1 * RIGHT, +1), (3 * RIGHT, -1)
        )

        stick_bar_magnet = AnimationGroup(
            bar_magnet_one.animate.shift(2 * RIGHT),
            bar_magnet_two.animate.shift(2 * LEFT),
            vector_field.animate.become(ArrowVectorField(func))
        )

        self.play(stick_bar_magnet)

        self.wait()