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

        self.wait(duration=10)

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

        self.wait(duration=2)


        func = get_force_field_func(
            (1 * LEFT, -1), (3 * LEFT, +1),
            (1 * RIGHT, -1), (3 * RIGHT, +1)
        )

        flip_bar_magnet = AnimationGroup(
            Rotate(bar_magnet_two, PI),
            vector_field.animate.become(ArrowVectorField(func))
        )

        self.play(flip_bar_magnet)

        self.wait()

        func = get_force_field_func(
            (3 * LEFT, -1), (5 * LEFT, +1),
            (3 * RIGHT, -1), (5 * RIGHT, +1)
        )

        unstick_bar_magnet = AnimationGroup(
            bar_magnet_one.animate.shift(2 * LEFT),
            bar_magnet_two.animate.shift(2 * RIGHT),
            vector_field.animate.become(ArrowVectorField(func))
        )

        self.play(unstick_bar_magnet)

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
                return (0.2 * func(0.1)) / func(temprature_value.get_value()) # I = V / R

        represent_current(get_current, self, wire, left_end, right_end)

        wire_label = MathTex("I = \\frac{V}{R}").next_to(wire, LEFT)

        self.play(Write(wire_label))

        self.wait()

        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 3, 0.5], x_length=5, y_length=3, axis_config={"include_tip": False}
        )        
        ax.shift(1.5 * UP)
        labels = ax.get_axis_labels(Text("Temperature").scale(0.4), Text("Resistivity").scale(0.4))

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

        temprature_value = ValueTracker(3)
        temprature_value.set_value(3)
        tracking_current = False

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
        
        current_dot = Circle(color=BLUE, radius=0.08, fill_opacity=1).move_to(wire_loop.get_center() + wire_loop.radius * UP)
        current_dot.save_state()

        self.play(Create(current_dot))

        self.wait()

        wire_label = MathTex("I = \\frac{V}{R}").next_to(wire, 1.5 * LEFT)

        self.play(Write(wire_label))

        self.wait()

        def current_dot_position(dot: Dot):
            if temprature_value.get_value() <= 0.5:
                    dot.become(Circle(radius=0.7, color=BLUE, fill_opacity=0).move_to(wire_loop.get_center()))
            else:
                if dot.get_center()[0] == wire_loop.get_center()[0]:
                    dot.become(Circle(color=BLUE, radius=0.08, fill_opacity=1)).move_to(wire_loop.get_center() + wire_loop.radius * UP)

                if tracking_current:
                    dot.rotate(1.0 / func(temprature_value.get_value()), about_point=wire_loop.get_center())

        current_dot.add_updater(current_dot_position)

        self.wait()

        initial_point = [ax.coords_to_point(temprature_value.get_value(), func(temprature_value.get_value()))]
        dot = Dot(point=initial_point)
        def tracker_dot_position(x: Dot):
            if ax.p2c(x.get_center())[0] >= 0.5:
                x.move_to(ax.c2p(temprature_value.get_value(), func(temprature_value.get_value())))
            else:
                x.move_to(ax.c2p(temprature_value.get_value(), 0.001))

        dot.add_updater(tracker_dot_position)

        self.play(Create(ax))
        self.play(Write(labels))
        self.play(Create(nonlinear_graph_section))
        self.play(Create(t_label))
        self.play(Create(linear_graph_section))
        self.play(Create(dot))

        self.wait()

        tracking_current = True
        self.play(temprature_value.animate.set_value(0.1), run_time=5)
        self.play(temprature_value.animate.set_value(3), run_time=5)

        self.wait()

def make_proton():
    proton = Circle(radius=0.3, color=RED, fill_opacity=0.5)
    proton_label = Text("+")

    proton_animation_group = AnimationGroup(
        Create(proton),
        Write(proton_label)
    )

    return VGroup(proton, proton_label), proton_animation_group

def make_electron():
    electron = Circle(radius=0.2, color=GOLD, fill_opacity=0.5)
    electron_label = Text("-")

    electron_animation_group = AnimationGroup(
        Create(electron),
        Write(electron_label)
    )
    
    return VGroup(electron, electron_label), electron_animation_group

class ProtonLattice(Scene):
    def construct(self):
        scene_label = Text("Super Conductor Proton Lattice").shift(3.25 * UP)

        self.play(Write(scene_label))

        self.wait()

        proton_lattice_width = 8
        proton_lattice_height = 4

        proton_lattice_spacing = 1.5

        protons = np.empty((proton_lattice_width, proton_lattice_height), dtype=VGroup)
        proton_group = VGroup()
        for i in range(proton_lattice_height):
            for j in range(proton_lattice_width):
                proton, proton_animation_group = make_proton()
                proton.move_to(    
                    ((-(proton_lattice_width-1) * proton_lattice_spacing/2.0) + proton_lattice_spacing * j) * RIGHT + 
                    ((-(proton_lattice_height-1) * proton_lattice_spacing/2.0) + proton_lattice_spacing * i) * UP
                )
                proton_group.add(proton)
                protons[j, i] = proton

        proton_group.shift(0.5 * DOWN)

        self.play(FadeIn(proton_group))

        self.wait()

        first_electron, first_electron_animation_group = make_electron()
        first_electron.move_to(((proton_lattice_width-1)/2.0 * proton_lattice_spacing + 1.25) * LEFT + 0.5 * DOWN)
        
        self.play(first_electron_animation_group)

        self.wait()

        self.play(first_electron.animate.shift(8.0 * RIGHT), run_time=2)

        self.wait()

        # Move all 4 protons in
        # 42, 52
        # 41, 51
        proton_shift_spacing = 0.15

        proton_influence_circle = Circle(radius=1.5, color=RED, fill_opacity=0.1).move_to(first_electron.get_center())

        proton_move_in = AnimationGroup(
            protons[4, 1].animate.shift(proton_shift_spacing * RIGHT + proton_shift_spacing * UP),
            protons[4, 2].animate.shift(proton_shift_spacing * RIGHT + proton_shift_spacing * DOWN),
            protons[5, 1].animate.shift(proton_shift_spacing * LEFT + proton_shift_spacing * UP),
            protons[5, 2].animate.shift(proton_shift_spacing * LEFT + proton_shift_spacing * DOWN),
            Create(Arrow(protons[4, 1].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[4, 2].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[5, 1].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[5, 2].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(proton_influence_circle),
        )

        self.play(proton_move_in)

        self.wait()
        
        second_electron, second_electron_animation_group = make_electron()
        second_electron.move_to(((proton_lattice_width-1)/2.0 * proton_lattice_spacing + 1.25) * LEFT + 0.5 * DOWN)

        self.play(second_electron_animation_group)

        self.wait()

        self.play(second_electron.animate.shift(6.0 * RIGHT))

        self.wait()

        self.play(Create(Line(first_electron.get_center(), second_electron.get_center(), color=BLUE).set_z_index(first_electron.z_index - 1)))

        self.play(Write(Text("Cooper Pair", color=BLUE).scale(0.5).next_to(second_electron, 0.75 * LEFT)))

        self.wait()

class ElectronPairs(Scene):
    def construct(self):
        scene_label = Text("Net Spin in Electron Pairs").shift(3.25 * UP)

        self.play(Write(scene_label))

        self.wait()

        first_electron = Circle(radius=1, color=GOLD, fill_opacity=0.5).move_to(2 * LEFT + 0.5 * DOWN)
        first_electron_label = MathTex("\\pm \\frac{1}{2}").move_to(first_electron.get_center())

        second_electron = Circle(radius=1, color=GOLD, fill_opacity=0.5).move_to(2 * RIGHT + 0.5 * DOWN)
        second_electron_label = MathTex("\\pm \\frac{1}{2}").move_to(second_electron.get_center())

        electron_creation_animation_group = AnimationGroup(
            Create(first_electron),
            Create(second_electron),
            Write(first_electron_label),
            Write(second_electron_label)
        )

        self.play(electron_creation_animation_group)

        self.wait()

        spin_rectangle = Rectangle(color=BLUE, fill_opacity=0).surround(VGroup(first_electron, second_electron))
        spin_label = Tex("Net Spin: +0", color=BLUE).next_to(spin_rectangle, LEFT)

        electron_zero_spin_animation_group = AnimationGroup(
            first_electron_label.animate.become(MathTex("-\\frac{1}{2}").shift(1.5 * LEFT + 0.5 * DOWN)),
            second_electron_label.animate.become(MathTex("+\\frac{1}{2}").shift(1.5 * RIGHT + 0.5 * DOWN)),
            first_electron.animate.shift(0.5 * RIGHT),
            second_electron.animate.shift(0.5 * LEFT),
            Create(spin_rectangle),
            Write(spin_label)
        )

        self.play(electron_zero_spin_animation_group)

        self.wait()

        electron_zero_arrow_spin_animation_group = AnimationGroup(
            first_electron_label.animate.become(MathTex("\\uparrow").shift(first_electron.get_center())),
            second_electron_label.animate.become(MathTex("\\downarrow").shift(second_electron.get_center())),
        )

        self.play(electron_zero_arrow_spin_animation_group)

        self.wait()

        electron_one_spin_animation_group = AnimationGroup(
            first_electron_label.animate.become(MathTex("\\uparrow").move_to(first_electron.get_center())),
            second_electron_label.animate.become(MathTex("\\uparrow").move_to(second_electron.get_center())),
            spin_label.animate.become(Tex("Net Spin: +1", color=BLUE).move_to(spin_label.get_center()))
        )

        self.play(electron_one_spin_animation_group)

        self.wait()

        electron_neg_one_arrow_spin_animation_group = AnimationGroup(
            first_electron_label.animate.become(MathTex("\\downarrow").move_to(first_electron.get_center())),
            second_electron_label.animate.become(MathTex("\\downarrow").move_to(second_electron.get_center())),
            spin_label.animate.become(Tex("Net Spin: -1", color=BLUE).move_to(spin_label.get_center()))
        )

        self.play(electron_neg_one_arrow_spin_animation_group)

        self.wait()


class ProtonLatticeCooperPair(Scene):
    def construct(self):
        scene_label = Text("Cooper Pairs").shift(3.25 * UP)

        self.play(Write(scene_label))

        self.wait()

        proton_lattice_width = 8
        proton_lattice_height = 4

        proton_lattice_spacing = 1.5

        protons = np.empty((proton_lattice_width, proton_lattice_height), dtype=VGroup)
        proton_group = VGroup()
        for i in range(proton_lattice_height):
            for j in range(proton_lattice_width):
                proton, proton_animation_group = make_proton()
                proton.move_to(    
                    ((-(proton_lattice_width-1) * proton_lattice_spacing/2.0) + proton_lattice_spacing * j) * RIGHT + 
                    ((-(proton_lattice_height-1) * proton_lattice_spacing/2.0) + proton_lattice_spacing * i) * UP
                )
                proton.set_z_index(0)
                proton_group.add(proton)
                protons[j, i] = proton

        proton_group.shift(0.5 * DOWN)

        self.play(FadeIn(proton_group))

        self.wait()

        first_electron, first_electron_animation_group = make_electron()
        first_electron.move_to(((proton_lattice_width-1)/2.0 * proton_lattice_spacing + 1.25) * LEFT + 0.5 * DOWN)
        first_electron.shift(8.0 * RIGHT)
        first_electron.set_z_index(500)
        
        self.play(first_electron_animation_group)

        # Move all 4 protons in
        # 42, 52
        # 41, 51
        proton_shift_spacing = 0.15

        proton_influence_circle = Circle(radius=1.5, color=RED, fill_opacity=0.1).move_to(first_electron.get_center())

        proton_move_in = AnimationGroup(
            protons[4, 1].animate.shift(proton_shift_spacing * RIGHT + proton_shift_spacing * UP),
            protons[4, 2].animate.shift(proton_shift_spacing * RIGHT + proton_shift_spacing * DOWN),
            protons[5, 1].animate.shift(proton_shift_spacing * LEFT + proton_shift_spacing * UP),
            protons[5, 2].animate.shift(proton_shift_spacing * LEFT + proton_shift_spacing * DOWN),
            Create(Arrow(protons[4, 1].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[4, 2].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[5, 1].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(Arrow(protons[5, 2].get_center(), proton_influence_circle.get_center(), color=RED)),
            Create(proton_influence_circle),
        )

        self.play(proton_move_in)

        self.wait()
        
        second_electron, second_electron_animation_group = make_electron()
        second_electron.move_to(((proton_lattice_width-1)/2.0 * proton_lattice_spacing + 1.25) * LEFT + 0.5 * DOWN)
        first_electron.set_z_index(500)

        self.play(second_electron_animation_group)

        self.wait()

        self.play(second_electron.animate.shift(6.0 * RIGHT))

        self.wait()

        cooper_pair_line = Line(first_electron.get_center(), second_electron.get_center(), color=BLUE).set_z_index(first_electron.z_index - 1)
        
        self.play(Create(cooper_pair_line))

        cooper_pair_label = Text("Cooper Pair", color=BLUE).scale(0.5).next_to(second_electron, 0.75 * LEFT)

        self.play(Write(cooper_pair_label))

        self.wait()

        electron_charge_label_to_spin = AnimationGroup(
            first_electron[1].animate.become(MathTex("\\uparrow").scale(0.5).move_to(first_electron.get_center())),
            second_electron[1].animate.become(MathTex("\\downarrow").scale(0.5).move_to(second_electron.get_center())),
        )

        self.play(electron_charge_label_to_spin)

        self.wait()

        second_electron.save_state()
        cooper_pair_line.save_state()
        cooper_pair_label.save_state()
        

        relative_move_position = 2.0 * RIGHT + 0.4 * UP
        move_cooper_pair = AnimationGroup(
            second_electron.animate.move_to(second_electron.get_center() + relative_move_position),
            cooper_pair_line.animate.become(Line(first_electron.get_center(), second_electron.get_center() + relative_move_position, color=BLUE).set_z_index(first_electron.z_index - 1)),
            cooper_pair_label.animate.become(Text("Cooper Pair", color=BLUE).scale(0.5).move_to(cooper_pair_label.get_center() + relative_move_position))
        )

        self.play(move_cooper_pair)

        self.wait()

        relative_move_position = 1.3 * RIGHT + 1.3 * UP
        move_cooper_pair = AnimationGroup(
            second_electron.animate.move_to(second_electron.get_center() + relative_move_position),
            cooper_pair_line.animate.become(Line(first_electron.get_center(), second_electron.get_center() + relative_move_position, color=BLUE).set_z_index(first_electron.z_index - 1)),
            cooper_pair_label.animate.become(Text("Cooper Pair", color=BLUE).scale(0.5).move_to(cooper_pair_label.get_center() + relative_move_position))
        )

        self.play(move_cooper_pair)

        self.wait()
            
        move_cooper_pair = AnimationGroup(
            second_electron.animate.restore(),
            cooper_pair_line.animate.restore(),
            cooper_pair_label.animate.restore()
        )

        self.play(move_cooper_pair)

        self.wait()

def construct_flow_line_arrow(start, stop, endpoint_value, deviation_point, deviation_value, color=BLUE):
    first_section = CubicBezier(start, start + endpoint_value * UP, deviation_point + deviation_value * DOWN, deviation_point, color=color)
    second_section = CubicBezier(deviation_point, deviation_point + deviation_value * UP, stop + endpoint_value * DOWN, stop, color=color)

    arrow_tip = RegularPolygon(n=3, start_angle=PI/2, fill_opacity=1, color=color).scale_to_fit_width(0.1).move_to(stop)

    return VGroup(first_section, second_section, arrow_tip)

class MagneticFieldsThroughSuperconductor(Scene):
    def construct(self):
        scene_label = Text("Meissner Effect").shift(3.25 * UP)

        self.play(Write(scene_label))

        self.wait()

        self.play(FadeOut(scene_label))

        self.wait()

        magnet_width = 4.0
        magnet_height = 1.0

        magnet_position = -2.0

        magnet = Rectangle(height=magnet_height - 0.25, width=magnet_width + 0.5, color=GREY, fill_opacity=0.7).move_to(magnet_position * UP).set_z_index(1)

        self.play(Create(magnet))

        self.wait()

        superconductor = Rectangle(height=0.5, width=1.5, color=GOLD, fill_opacity=0.8).move_to((magnet_position + 2) * UP).set_z_index(10)

        self.play(Create(superconductor))

        self.wait()

        magnet_label = Text("Magnet", color=GREY).scale(0.5).next_to(magnet, 0.75 * LEFT)
        superconductor_label = Text("Superconductor", color=GOLD).scale(0.5).next_to(superconductor, 0.75 * LEFT)

        label_group = AnimationGroup(
            Write(magnet_label),
            Write(superconductor_label)
        )

        self.play(label_group)

        self.wait()

        label_group = AnimationGroup(
            FadeOut(magnet_label),
            FadeOut(superconductor_label)
        )

        self.play(label_group)

        self.wait()

        func = get_force_field_func(
            (magnet_position * UP + (magnet_height / 2) * UP, +2), (magnet_position * UP + (magnet_height / 2) * DOWN, -2)
        )

        magnet_vector_field = ArrowVectorField(func).set_z_index(0)

        self.play(FadeIn(magnet_vector_field))

        self.wait()

        flow_line_arrows = VGroup()

        num_of_flow_line_arrows = 9
        line_spacing = magnet_width / num_of_flow_line_arrows
        line_length = 3

        def make_straight_arrow(arrow_number):
            flow_line_arrows.add(
                construct_flow_line_arrow(
                    start=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2) * UP,
                    stop=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + line_length) * UP,
                    endpoint_value=0.5,
                    deviation_point=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + (line_length / 2)) * UP,
                    deviation_value=0.5
                )
            )

        for i in range(num_of_flow_line_arrows + 1):
            make_straight_arrow(i)

    
        self.play(Transform(magnet_vector_field, flow_line_arrows))

        self.wait()

        flow_line_curvy_arrows = VGroup()

        def make_curvy_arrow(arrow_number, blocker_ammount, endpoint_value, deviation_value):
            flow_line_curvy_arrows.add(
                construct_flow_line_arrow(
                    start=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2) * UP,
                    stop=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + line_length) * UP,
                    endpoint_value=endpoint_value,
                    deviation_point=(magnet_width/2 - (line_spacing * arrow_number) - blocker_ammount) * LEFT + (magnet_position + magnet_height/2 + (line_length / 2)) * UP,
                    deviation_value=deviation_value
                )
            )

        make_curvy_arrow(0, 0, 0.5, 0.5)
        make_curvy_arrow(1, 0, 0.5, 0.5)
        make_curvy_arrow(2, 0, 0.5, 0.5)

        make_curvy_arrow(3, -0.3, 0.5, 0.5)
        make_curvy_arrow(4, -0.65, 0.5, 0.7)
        make_curvy_arrow(5, 0.65, 0.5, 0.7)
        make_curvy_arrow(6, 0.3, 0.5, 0.5)

        make_curvy_arrow(7, 0, 0.5, 0.5)
        make_curvy_arrow(8, 0, 0.5, 0.5)
        make_curvy_arrow(9, 0, 0.5, 0.5)


        temprature_value = ValueTracker(3)
        temprature_value.set_value(3)

        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 3, 0.5], x_length=3, y_length=2, axis_config={"include_tip": False}
        ) 

        ax.shift(2 * UP + 4.5 * RIGHT)
        labels = ax.get_axis_labels(Text("Temperature").scale(0.4), Text("Resistivity").scale(0.4))

        def func(x):
            return 1.5 + (0.4 * x)**3 # Sketchy Plot

        nonlinear_graph_section = ax.plot(func, color=GOLD, x_range=[0.5, 3])
        t_label = ax.get_T_label(x_val=0.5, graph=nonlinear_graph_section, line_color=GOLD, label=Tex("$T_{C}$").scale(0.75))
        linear_graph_section = ax.plot(lambda x: 0.001, color=GOLD, x_range=[0, 0.5])

        initial_point = [ax.coords_to_point(temprature_value.get_value(), func(temprature_value.get_value()))]
        dot = Dot(point=initial_point)
        def tracker_dot_position(x: Dot):
            if ax.p2c(x.get_center())[0] > 0.5:
                x.move_to(ax.c2p(temprature_value.get_value(), func(temprature_value.get_value())))
            else:
                x.move_to(ax.c2p(temprature_value.get_value(), 0.001))

        dot.add_updater(tracker_dot_position)

        self.play(Create(ax))
        self.play(Write(labels))
        self.play(Create(nonlinear_graph_section))
        self.play(Create(t_label))
        self.play(Create(linear_graph_section))
        self.play(Create(dot))

        self.wait()

        self.play(temprature_value.animate.set_value(0.5 - 1e-6), run_time=5)
        self.play(Transform(magnet_vector_field, flow_line_curvy_arrows))

        self.play(temprature_value.animate.set_value(0.1), run_time=2)

        self.play(temprature_value.animate.set_value(0.5 + 1e-6), run_time=2)
        
        self.play(Transform(magnet_vector_field, flow_line_arrows))
        self.play(temprature_value.animate.set_value(3), run_time=5)

        self.wait()

class SuperconductorFluxPinning(Scene):
    def construct(self):
        scene_label = Text("Flux Pinning").shift(3.25 * UP)

        self.play(Write(scene_label))

        self.wait()

        self.play(FadeOut(scene_label))

        self.wait()

        magnet_width = 4.0
        magnet_height = 1.0

        magnet_position = -2.0

        magnet = Rectangle(height=magnet_height - 0.25, width=magnet_width + 0.5, color=GREY, fill_opacity=0.7).move_to(magnet_position * UP).set_z_index(1)

        self.play(Create(magnet))

        self.wait()

        superconductor = Rectangle(height=0.5, width=1.5, color=GOLD, fill_opacity=0.8).move_to((magnet_position + 2) * UP).set_z_index(10)

        self.play(Create(superconductor))

        self.wait()

        magnet_label = Text("Magnet", color=GREY).scale(0.5).next_to(magnet, 0.75 * LEFT)
        superconductor_label = Text("Superconductor", color=GOLD).scale(0.5).next_to(superconductor, 0.75 * LEFT)

        label_group = AnimationGroup(
            Write(magnet_label),
            Write(superconductor_label)
        )

        self.play(label_group)

        self.wait()

        label_group = AnimationGroup(
            FadeOut(magnet_label),
            FadeOut(superconductor_label)
        )

        self.play(label_group)

        self.wait()

        func = get_force_field_func(
            (magnet_position * UP + (magnet_height / 2) * UP, +2), (magnet_position * UP + (magnet_height / 2) * DOWN, -2)
        )

        magnet_vector_field = ArrowVectorField(func).set_z_index(0)

        self.play(FadeIn(magnet_vector_field))

        self.wait()

        flow_line_arrows = VGroup()

        num_of_flow_line_arrows = 9
        line_spacing = magnet_width / num_of_flow_line_arrows
        line_length = 3

        def make_straight_arrow(arrow_number):
            flow_line_arrows.add(
                construct_flow_line_arrow(
                    start=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2) * UP,
                    stop=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + line_length) * UP,
                    endpoint_value=0.5,
                    deviation_point=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + (line_length / 2)) * UP,
                    deviation_value=0.5
                )
            )

        for i in range(num_of_flow_line_arrows + 1):
            make_straight_arrow(i)

    
        self.play(Transform(magnet_vector_field, flow_line_arrows))

        self.wait()

        flow_line_curvy_arrows = VGroup()

        def make_curvy_arrow(arrow_number, blocker_ammount, endpoint_value, deviation_value):
            flow_line_curvy_arrows.add(
                construct_flow_line_arrow(
                    start=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2) * UP,
                    stop=(magnet_width/2 - (line_spacing * arrow_number)) * LEFT + (magnet_position + magnet_height/2 + line_length) * UP,
                    endpoint_value=endpoint_value,
                    deviation_point=(magnet_width/2 - (line_spacing * arrow_number) - blocker_ammount) * LEFT + (magnet_position + magnet_height/2 + (line_length / 2)) * UP,
                    deviation_value=deviation_value
                )
            )

        make_curvy_arrow(0, 0, 0.5, 0.5)
        make_curvy_arrow(1, 0, 0.5, 0.5)
        make_curvy_arrow(2, 0, 0.5, 0.5)

        make_curvy_arrow(3, line_spacing/2, 0.5, 0.5)
        make_curvy_arrow(4, -line_spacing/2, 0.5, 0.5)
        make_curvy_arrow(5, line_spacing/2, 0.5, 0.5)
        make_curvy_arrow(6, -line_spacing/2, 0.5, 0.5)

        make_curvy_arrow(7, 0, 0.5, 0.5)
        make_curvy_arrow(8, 0, 0.5, 0.5)
        make_curvy_arrow(9, 0, 0.5, 0.5)

        temprature_value = ValueTracker(3)
        temprature_value.set_value(3)

        ax = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 3, 0.5], x_length=3, y_length=2, axis_config={"include_tip": False}
        ) 

        ax.shift(2 * UP + 4.5 * RIGHT)
        labels = ax.get_axis_labels(Text("Temperature").scale(0.4), Text("Resistivity").scale(0.4))

        def func(x):
            return 1.5 + (0.4 * x)**3 # Sketchy Plot

        nonlinear_graph_section = ax.plot(func, color=GOLD, x_range=[0.5, 3])
        t_label = ax.get_T_label(x_val=0.5, graph=nonlinear_graph_section, line_color=GOLD, label=Tex("$T_{C}$").scale(0.75))
        linear_graph_section = ax.plot(lambda x: 0.001, color=GOLD, x_range=[0, 0.5])

        initial_point = [ax.coords_to_point(temprature_value.get_value(), func(temprature_value.get_value()))]
        dot = Dot(point=initial_point)
        def tracker_dot_position(x: Dot):
            if ax.p2c(x.get_center())[0] > 0.5:
                x.move_to(ax.c2p(temprature_value.get_value(), func(temprature_value.get_value())))
            else:
                x.move_to(ax.c2p(temprature_value.get_value(), 0.001))

        dot.add_updater(tracker_dot_position)

        self.play(Create(ax))
        self.play(Write(labels))
        self.play(Create(nonlinear_graph_section))
        self.play(Create(t_label))
        self.play(Create(linear_graph_section))
        self.play(Create(dot))

        self.wait()

        self.play(temprature_value.animate.set_value(0.5 - 1e-6), run_time=5)
        self.play(Transform(magnet_vector_field, flow_line_curvy_arrows))

        self.play(temprature_value.animate.set_value(0.1), run_time=2)

        self.wait()

        first_flux_tube = Rectangle(height=0.5, width=0.2, color=RED, fill_opacity=0.5).move_to((magnet_width/2 - (line_spacing * 3) - line_spacing/2) * LEFT + (magnet_position + 2) * UP).set_z_index(15)
        second_flux_tube = Rectangle(height=0.5, width=0.2, color=RED, fill_opacity=0.5).move_to((magnet_width/2 - (line_spacing * 5) - line_spacing/2) * LEFT + (magnet_position + 2) * UP).set_z_index(15)
        
        create_flux_tubes = AnimationGroup(
            Create(first_flux_tube),
            Create(second_flux_tube)
        )

        self.play(create_flux_tubes)

        flux_tube_label = Text("Flux Tubes", color=RED).scale(0.5).next_to(first_flux_tube, 1.25 * LEFT)

        self.play(Write(flux_tube_label))

        self.wait()

        flux_tube_fade_out = AnimationGroup(
            FadeOut(first_flux_tube),
            FadeOut(second_flux_tube),
            FadeOut(flux_tube_label),
        )

        self.play(flux_tube_fade_out)

        self.wait()

        self.play(temprature_value.animate.set_value(0.5 + 1e-6), run_time=2)
        
        self.play(Transform(magnet_vector_field, flow_line_arrows))
        self.play(temprature_value.animate.set_value(3), run_time=5)

        self.wait()
