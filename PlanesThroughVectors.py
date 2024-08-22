from manim import *
import numpy as np


class MySpaceScene(ThreeDScene):
    def construct(self):
        def z_updater(mob: Mobject):
            mob.set_z(axes.c2p(0, 0, z_var.get_value())[-1])

        def end_z_updater(mob: Arrow3D):
            mob.become(
                Arrow3D(
                    axes.c2p(0, 0, 0), axes.c2p(-2, 2, z_var.get_value()), color=YELLOW
                )
            )

        def pos_label_updater(mob: Mobject):
            mob.next_to(pos_vec.get_end(), 1.5 * OUT)

        def pos_new_label_updater(mob: Mobject):
            mob.move_to(axes.c2p(-2, 2, z_var.get_value() + 0.5))

        def p1_label_updater(mob: Mobject):
            mob.next_to(p1, IN)

        def p1_new_label_updater(mob: Mobject):
            mob.next_to(p1_new, IN)

        # Axes
        axes = ThreeDAxes()
        labels = axes.get_axis_labels()

        # Plane
        plane = axes.plot_surface(
            lambda x, y: -(2 * x + -1 * y) / 3, (-3, 3), (-3, 3), resolution=(1, 1)
        )
        plane.set_style(fill_opacity=0.75, fill_color=BLUE)

        # Normal Vector
        normal_vec = Arrow3D(
            axes.c2p(0, 0, 0), axes.c2p(2 / 2, -1 / 2, 3 / 2), color=RED
        )
        vector_label = MathTex(
            r"\mathbf{n}", font_size=0.6 * DEFAULT_FONT_SIZE
        ).next_to(normal_vec.get_end(), 1.5 * OUT)

        # Point
        t = ValueTracker(-PI)

        def parametric_pos(t):
            return (np.sin(PI - t) - 2, np.cos(t) + 3, t / 2 + 2 - PI / 2)

        p1 = always_redraw(
            lambda: Dot3D(
                point=axes.c2p(*parametric_pos(t.get_value())), radius=0.04, color=GREEN
            )
        )

        p1_label = always_redraw(
            lambda: MathTex(
                f"({', '.join(f'{i:.1f}' for i in p1.get_center())})",
                font_size=0.55 * DEFAULT_FONT_SIZE,
            ).next_to(p1, IN)
        )

        # Position Vector
        pos_vec = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(-2, 2, 2), color=YELLOW)
        pos_label = MathTex(r"\mathbf{x}", font_size=0.6 * DEFAULT_FONT_SIZE).next_to(
            pos_vec.get_end(), 1.5 * OUT
        )

        # Angle
        angle = Arc3D(
            normal_vec.get_center(),
            pos_vec.get_center(),
            normal_vec.get_start(),
            0.5,
        )
        angle_label = always_redraw(
            lambda: MathTex(r"\theta", font_size=0.6 * DEFAULT_FONT_SIZE).next_to(
                angle, 1.25 * OUT
            )
        )

        # Graph VGroup
        graph = VGroup(
            axes,
            labels,
            plane,
            normal_vec,
            vector_label,
            p1,
            pos_vec,
            pos_label,
            angle,
            angle_label,
        )

        self.set_camera_orientation(75 * DEGREES, -60 * DEGREES)

        self.play(DrawBorderThenFill(axes))
        self.play(Write(labels))
        self.wait(1)

        self.play(GrowFromCenter(plane))

        self.play(
            GrowFromPoint(normal_vec, axes.c2p(0, 0, 0)),
            axes.animate.set_opacity(0.5),
            labels.animate.set_opacity(0.5),
        )
        self.add_fixed_orientation_mobjects(vector_label)
        self.play(Write(vector_label))
        self.wait()

        self.begin_ambient_camera_rotation(rate=0.28)
        self.wait(2)
        self.play(Create(p1))
        self.add_fixed_orientation_mobjects(p1_label)
        self.play(Write(p1_label))
        self.play(t.animate.set_value(PI), run_time=4)
        p1_label_prime = MathTex(
            f"(x, y, z)",
            font_size=0.55 * DEFAULT_FONT_SIZE,
        ).next_to(p1, IN)

        graph.add(p1_label_prime)
        self.remove(p1_label)
        self.add_fixed_orientation_mobjects(p1_label_prime)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.move_camera(75 * DEGREES, 50 * DEGREES, run_time=2)
        self.play(GrowFromPoint(pos_vec, axes.c2p(0, 0, 0)))
        self.add_fixed_orientation_mobjects(pos_label)
        self.wait(2)
        self.play(Create(angle))
        self.add_fixed_orientation_mobjects(angle_label)
        self.play(Write(angle_label))
        self.wait(2)
        self.play(graph.animate.scale(0.8), graph.animate.shift(1.2 * (RIGHT + DOWN)))

        ## Part 2: LaTeX
        condition = Tex(
            r"$(x,y,z)$ lies on the \\plane $\iff$ $\theta = 90^\circ$",
            r"\\[1em]since $\mathbf{x} \cdot \mathbf{n} \propto \cos\theta$",
            r"\\[1em]$\mathbf{x} \cdot \mathbf{n} = 0$",
            r"\\[-1em] \[\begin{bmatrix}x \\ y \\ z\end{bmatrix} \cdot \begin{bmatrix}a \\ b \\ c\end{bmatrix} = 0\]",
            r"\\[-1em] \[ax+by+cz=0\]",
            font_size=0.8 * DEFAULT_FONT_SIZE,
        ).to_edge(RIGHT, buff=1.2 * MED_LARGE_BUFF)

        self.add_fixed_in_frame_mobjects(condition[0])
        self.play(Write(condition[0]))
        self.play(Indicate(angle), Indicate(angle_label))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(condition[1])
        self.play(Write(condition[1]))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(condition[2])
        self.play(Write(condition[2]))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(condition[3])
        self.play(Write(condition[3]))
        self.wait(2)
        self.add_fixed_in_frame_mobjects(condition[4])
        self.play(Write(condition[4]))
        self.wait(2)
        self.play(Indicate(condition[4]))
        self.wait(4)

        z_var = ValueTracker(p1.get_z())
        p1_new = p1.copy().add_updater(z_updater)
        self.replace(p1, p1_new)
        p1_label_prime.add_updater(p1_new_label_updater)
        pos_vec_new = pos_vec.copy().add_updater(end_z_updater)
        self.replace(pos_vec, pos_vec_new)
        pos_label.remove_updater(pos_label_updater)
        pos_label.add_updater(pos_new_label_updater)
        angle_new = always_redraw(
            lambda: Arc3D(
                axes.c2p(2 / 2, -1 / 2, 3 / 2),
                axes.c2p(-2, 2, z_var.get_value()),
                axes.c2p(0, 0, 0),
                0.5,
            )
        )
        self.replace(angle, angle_new)

        l_than = MathTex(
            r"\theta > 90^\circ \implies \cos\theta < 0",
            r"\\ \implies \mathbf{x} \cdot \mathbf{n} < 0",
            r"\\ \implies ax+by+cz<0",
            font_size=0.8 * DEFAULT_FONT_SIZE,
        ).to_edge(RIGHT, buff=1.2 * MED_LARGE_BUFF)

        g_than = MathTex(
            r"\theta < 90^\circ \implies \cos\theta > 0",
            r"\\ \implies \mathbf{x} \cdot \mathbf{n} > 0",
            r"\\ \implies ax+by+cz>0",
            font_size=0.8 * DEFAULT_FONT_SIZE,
        ).to_edge(RIGHT, buff=1.2 * MED_LARGE_BUFF)

        self.play(z_var.animate.set_value(0))
        self.wait()

        self.play(FadeOut(condition))
        self.wait(3)
        self.add_fixed_in_frame_mobjects(l_than[0])
        self.play(Write(l_than[0]))
        self.wait()
        self.add_fixed_in_frame_mobjects(l_than[1])
        self.play(Write(l_than[1]))
        self.wait()
        self.add_fixed_in_frame_mobjects(l_than[2])
        self.play(Write(l_than[2]))
        self.wait(3)

        self.play(z_var.animate.set_value(3))
        self.wait(3)
        # self.add_fixed_in_frame_mobjects(g_than)
        self.play(l_than.animate.become(g_than))
        self.wait(4)

        self.play(Unwrite(l_than), Uncreate(angle_new), Uncreate(angle_label))

        self.wait(2)
        self.play(
            plane.animate.shift(OUT),
            normal_vec.animate.become(
                Arrow3D(axes.c2p(0, 0, 1), axes.c2p(2 / 2, -1 / 2, 5 / 2), color=RED)
            ),
            vector_label.animate.move_to(axes.c2p(2 / 4, -3 / 4, 5 / 4)),
        )

        p2 = Dot3D(axes.c2p(0, 0, 1), radius=0.04, color=PURPLE)
        p_vector = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(0, 0, 1), color=GREEN)
        p_vector_label = (
            MathTex(r"\mathbf{p}", font_size=0.6 * DEFAULT_FONT_SIZE)
            .move_to(p_vector.get_end())
            .shift(3.1 * LEFT, 1.7 * UP)
        )

        diff_vector = Arrow3D(axes.c2p(0, 0, 1), axes.c2p(-2, 2, 3), color=PURPLE)
        diff_vector_label = (
            MathTex(r"\mathbf{x}-\mathbf{p}", font_size=0.6 * DEFAULT_FONT_SIZE)
            .next_to(diff_vector.get_end(), 1.5 * OUT)
            .shift(1.1 * UP, 0.4 * LEFT)
        )

        final_angle = angle = Arc3D(
            axes.c2p(2 / 2, -1 / 2, 5 / 2),
            axes.c2p(-2, 2, 3),
            axes.c2p(0, 0, 1),
            0.5,
        )
        final_anlge_label = (
            MathTex(r"\theta", font_size=0.6 * DEFAULT_FONT_SIZE)
            .move_to(normal_vec.get_start())
            .shift(1.6 * UP, 1.55 * LEFT)
        )

        self.play(GrowFromCenter(p2))
        self.wait(2)
        self.play(Indicate(p2))
        self.wait(1.5)
        self.play(GrowFromPoint(diff_vector, axes.c2p(0, 0, 1)))
        self.wait(3)
        self.add_fixed_in_frame_mobjects(final_anlge_label)
        self.play(Create(final_angle), Write(final_anlge_label))
        self.wait(4)
        self.add_fixed_in_frame_mobjects(p_vector_label)
        self.play(GrowFromPoint(p_vector, axes.c2p(0, 0, 0)), Write(p_vector_label))
        self.wait(3.5)
        self.add_fixed_in_frame_mobjects(diff_vector_label)
        self.play(Write(diff_vector_label))
        self.wait(3)

        final_expl = Tex(
            r"$(x,y,z)$ lies on the \\plane $\iff$ $\theta = 90^\circ$",
            r"\\[-1.3em] \[(\mathbf{x}-\mathbf{p}) \cdot \mathbf{n} = 0\]",
            r"\\[-2em] \[\mathbf{x}\cdot \mathbf{n}-\mathbf{p} \cdot \mathbf{n} = 0\]",
            r"\\[-2em] \[ \mathbf{x} \cdot \mathbf{n} = \mathbf{p} \cdot \mathbf{n} \]",
            r"\\[-1.5em] \[\begin{bmatrix}x \\ y \\ z\end{bmatrix} \cdot \begin{bmatrix}a \\ b \\ c\end{bmatrix} = \begin{bmatrix}p_x \\ p_y \\ p_z\end{bmatrix} \cdot \begin{bmatrix}a \\ b \\ c\end{bmatrix}\]",
            r"\\[-1.5em] \[ax+by+cz=ap_x+bp_y+cp_z\]",
            font_size=0.8 * DEFAULT_FONT_SIZE,
        ).to_edge(RIGHT, buff=1.2 * MED_LARGE_BUFF)

        for tex in final_expl:
            self.add_fixed_in_frame_mobjects(tex)
            self.play(Write(tex))
            self.wait(2)

        self.wait(2)
        self.play(Indicate(final_expl[-1]))

        self.wait(5)
        self.play(FadeOut(i) for i in self.mobjects + [diff_vector])
        self.wait(0.5)


class Arc3D(VMobject):
    def __init__(self, A=None, B=None, center=None, radius=1, segments=40, **kwargs):
        super().__init__(**kwargs)
        start = center + (A - center) * radius / np.linalg.norm(A - center)
        end = center + (B - center) * radius / np.linalg.norm(B - center)
        self.set_points([start])
        for i in np.linspace(0, 1, segments, endpoint=True):
            dotonline = start + i * (end - start)
            radline = dotonline - center
            dotonarc = center + radline / np.linalg.norm(radline) * radius
            self.add_smooth_curve_to(dotonarc)
