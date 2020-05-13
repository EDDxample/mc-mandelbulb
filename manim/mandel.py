#!/usr/bin/env python
from manimlib.imports import *

# Manim: https://github.com/3b1b/manim/
# py -m manim mandel.py ComplexPlane -pl

class ComplexPlane(Scene):
    CONFIG = {
        "config" : {
                "background_line_style": {
                "stroke_color": "#333333"
            }
        }
    }

    def construct(self):
        v = Vector(np.array([2, 1]),color=YELLOW)

        real = DecimalNumber(0, num_decimal_places=2, include_sign=True,color=RED)
        comp = DecimalNumber(0, num_decimal_places=2, include_sign=True,color=GREEN)
        i = TexMobject("i",color="#FFFF00")

        real.add_updater(lambda d: d.next_to(v.get_end(), RIGHT + 0.5 * UP))
        real.add_updater(lambda d: d.set_value(v.get_end()[0]))
        
        comp.add_updater(lambda d: d.next_to(real, 0.5 * RIGHT))
        comp.add_updater(lambda d: d.set_value(v.get_end()[1]))

        i.add_updater(lambda d: d.next_to(comp, 0.5 * RIGHT))

        # my_plane.add(my_plane.get_axis_labels())
        self.play(FadeIn(NumberPlane(**self.config)))
        self.play(Write(v), Write(real), Write(comp), Write(i))
        self.play(Transform(v,Vector(np.array([2, -1]),color=YELLOW)))
        self.wait(0.5)
        self.play(Transform(v,Vector(np.array([-2, 1]),color=YELLOW)))
        self.wait(0.5)
        self.play(Transform(v,Vector(np.array([1, 0.3]),color=YELLOW)))
        self.play(WiggleOutThenIn(v))
        self.wait()

class MandelBrot(Scene):
    CONFIG = {
        "config" : {
                "background_line_style": {
                "stroke_color": "#333333"
            }
        }
    }

    def step(self, x, y, color, dots, arrows):
        scale = 7
        v = np.array([x, y, 0.])
        dot = Dot(v, color=color)
        dots.add(dot)

        v /= scale

        c = complex(v[0], v[1])
        z = complex(0, 0)

        flag = False

        for _ in range(20):
            v = np.array((z.real, z.imag, 0.))
            z = z*z + c
            vec = Vector((np.array((z.real, z.imag, 0.)) - v) * scale, color=color)

            if flag:
                vec.shift(v * scale)
                arrows.add(vec)
            else: flag = True
        
        return dots, arrows

    def colorize(self, field):
        scale = 4

        for dot in field:
            v = dot.get_center() / scale

            c = complex(v[0],v[1])
            z = complex(0,0)
            n = 0

            while abs(z) <= 2 and n < 30:
                z = z*z + c
                n += 1
            
            if abs(z) <= 2:
                dot.set_color(BLACK)
            else:
                dot.set_color("#FF0000")
            
        self.play(VFadeIn(field))

    def construct(self):
        
        self.play(FadeIn(NumberPlane(**self.config)))
        
        dots = VGroup()

        dots, A = self.step( 2, 1,   RED, dots, VGroup())
        dots, C = self.step(3, 1,    ORANGE, dots, VGroup())
        dots, B = self.step(-4, -3,  BLUE, dots, VGroup())
        dots, D = self.step(-3.4, 2, GREEN, dots, VGroup())
        dots, E = self.step(3, -2,   PURPLE, dots, VGroup())

        self.play(GrowFromCenter(dots))
        self.wait(0.2)
        for group in [A,B,C,D,E]:
            self.play(VFadeIn(group,run_time=0.5))
        self.wait(4)

        self.play(VFadeOut(dots),VFadeOut(A),VFadeOut(B),VFadeOut(C),VFadeOut(D),VFadeOut(E))
        self.remove(dots, A,B,C,D,E)

        self.wait()
        points = [x*RIGHT+y*UP
            for x in np.arange(-6,6,0.20)
            for y in np.arange(-3.5,3.5,0.20)
        ]

        dots = []
        for point in points:
            dots.append(Dot(point, radius=0.05))
        
        draw_field = VGroup(*dots)

        self.play(ShowCreation(draw_field))
        self.wait()

        self.colorize(draw_field)

        self.wait(2)

