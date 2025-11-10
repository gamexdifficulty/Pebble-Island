from utils.lerp import lerp
from frostlight_engine import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t))
    )

class Sky:
    def __init__(self, game: "Game"):
        self.game = game
        self.sprite = Sprite(size=[320,180])
        self.keyframes = [
            (0.0, (10, 15, 30)),      # Midnight
            (4.0, (30, 40, 80)),      # Pre-dawn (NEW)
            (6.0, (255, 160, 100)),   # Dawn
            (9.0, (135, 206, 235)),   # Morning
            (12.0, (100, 180, 255)),  # Noon
            (16.0, (255, 200, 120)),  # Afternoon
            (19.0, (255, 120, 150)),  # Sunset
            (22.0, (20, 30, 60)),     # Night
            (24.0, (10, 15, 30))      # Loop back
        ]

        self.sprite.set_custom_shader("sky.frag")

    def get_sky_color(self):
        for i in range(len(self.keyframes) - 1):
            t1, c1 = self.keyframes[i]
            t2, c2 = self.keyframes[i + 1]
            if t1 <= self.game.time.get_time() < t2:
                t = (self.game.time.get_time() - t1) / (t2 - t1)
                return lerp_color(c1, c2, t)
        return self.keyframes[-1][1]

    def draw(self):
        color = self.get_sky_color()
        self.sprite.set_custom_uniforms("color2",[*color,255])
        self.sprite.set_custom_uniforms("color1",[color[0]/2,color[1]/2,color[2]/2,255])
        self.game.window.render(self.sprite)
