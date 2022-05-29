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

def represent_current(current_value, scene, wire: Line, left_end: Dot, right_end: Dot):
    number_of_current_dots = 10

    current_spacing = wire.get_length() / number_of_current_dots

    def move_current(dot: Dot):
        dot.shift(current_value() * RIGHT)

        if dot.get_center()[0] >= wire.get_end()[0]:
            dot.move_to(wire.get_start())

    z_index = left_end.z_index
    left_end.set_z_index(z_index + 1)
    right_end.set_z_index(z_index + 1)

    dot_group = VGroup()
    for i in range(number_of_current_dots):
        dot = Dot(
                color=BLUE
            ).move_to(
                wire.get_start() + (i+1) * current_spacing * RIGHT
            ).set_z_index(
                z_index
            ).add_updater(move_current)

        dot_group.add(dot)

    scene.play(FadeIn(dot_group))
    

class CurrentInWire(Scene):
    def construct(self):
        scene_label = Text("Normal Metal").shift(3 * DOWN)
        self.play(Write(scene_label))

        length = 8
        
        wire = Line(length/2 * LEFT, length/2 * RIGHT)
        left_end = Dot(length/2 * LEFT)
        right_end = Dot(length/2 * RIGHT)

        wire.shift(1.5 * DOWN)
        left_end.shift(1.5 * DOWN)
        right_end.shift(1.5 * DOWN)

        self.play(Create(wire))

        make_wire_ends = AnimationGroup(
            FadeIn(left_end),
            FadeIn(right_end)
        )

        self.play(make_wire_ends)

        self.wait()

        def func(x):
            return 1 + (0.4 * x)**2 # Sketchy Plot

        temprature_value = ValueTracker(3)
        temprature_value.set_value(3)
        tracking_current = False
        
        def get_current():
            if not tracking_current:
                return 0.0
            else:
                return (0.2 * 1.0016) / func(temprature_value.get_value()) # I = V / R

        represent_current(get_current, self, wire, left_end, right_end)

        wire_label = MathTex("I = \\frac{V}{R}").next_to(wire, LEFT)

        self.play(Write(wire_label))

        self.wait()

        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 3, 0.5], x_length=5, y_length=3, axis_config={"include_tip": False}
        )        
        ax.shift(1.5 * UP)
        labels = ax.get_axis_labels(Text("Temprature").scale(0.4), Text("Resistivity").scale(0.4))

        graph = ax.plot(func, color=MAROON)

        initial_point = [ax.coords_to_point(temprature_value.get_value(), func(temprature_value.get_value()))]
        dot = Dot(point=initial_point)
        dot.add_updater(lambda x: x.move_to(ax.c2p(temprature_value.get_value(), func(temprature_value.get_value()))))

        self.play(Create(ax))
        self.play(Write(labels))
        self.play(Create(graph))
        self.play(Create(dot))

        tracking_current = True
        self.play(temprature_value.animate.set_value(0.1), run_time=5)
        self.play(temprature_value.animate.set_value(3), run_time=5)

        self.wait()


class CurrentInSuperconductor(Scene):
    def construct(self):
        scene_label = Text("Super Conductor").shift(3.5 * DOWN)

        self.play(Write(scene_label))

        length = 8  
        wire = Line(length/2 * LEFT, length/2 * RIGHT)

        wire_loop = Circle(radius=0.7, color=WHITE).shift(1.75 * DOWN)

        self.play(Create(wire))

        self.wait()

        self.play(Transform(wire, wire_loop))

        self.wait()

        resistance_value = ValueTracker(3)
        resistance_value.set_value(3)
        tracking_current = False

        dot = Dot(color=BLUE).move_to(wire_loop.get_center() + wire_loop.radius * UP)

        self.play(Create(dot))

        self.wait()


        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 3, 0.5], x_length=5, y_length=3, axis_config={"include_tip": False}
        ) 

        ax.shift(1.5 * UP)
        labels = ax.get_axis_labels(Text("Temprature").scale(0.4), Text("Resistivity").scale(0.4))

        def func(x):
            return 1.5 + (0.4 * x)**3 # Sketchy Plot

        nonlinear_graph_section = ax.plot(func, color=GOLD, x_range=[0.5, 3])

        t_label = ax.get_T_label(x_val=0.5, graph=nonlinear_graph_section, line_color=GOLD, label=Tex("$T_{C}$"))

        linear_graph_section = ax.plot(lambda x: 0.001, color=GOLD, x_range=[0, 0.5])

        initial_point = [ax.coords_to_point(resistance_value.get_value(), func(resistance_value.get_value()))]
        dot = Dot(point=initial_point)
        dot.add_updater(lambda x: x.move_to(ax.c2p(resistance_value.get_value(), func(resistance_value.get_value()))))

        self.play(Create(ax))
        self.play(Write(labels))
        self.play(Create(nonlinear_graph_section))
        self.play(Create(t_label))
        self.play(Create(linear_graph_section))
        self.play(Create(dot))

        self.wait()
