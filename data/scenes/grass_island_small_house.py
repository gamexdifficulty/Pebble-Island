import os
import time
from frostlight_engine import *
from typing import TYPE_CHECKING

from frostlight_engine import *
from data.classes.sky import Sky
from data.classes.animation import Animation

if TYPE_CHECKING:
    from main import Game

# Mili Palette

class SceneHome:
    def __init__(self,game:"Game"):
        self.game = game

        self.island_sprite = Sprite(os.path.join("scenes","grass_island_small_house","island.png"))
        self.grass_sprite = Sprite(os.path.join("scenes","grass_island_small_house","grass.png"))
        self.house_sprite = Sprite(os.path.join("scenes","grass_island_small_house","house.png"))
        self.water_fg_sprite = Sprite(os.path.join("scenes","grass_island_small_house","water.png"))
        self.water_bg_sprite = Sprite(os.path.join("scenes","grass_island_small_house","water.png"))
        self.cloud_sprite = Sprite(os.path.join("scenes","grass_island_small_house","clouds.png"))

        self.sky = Sky(self.game)

        self.grass_animation = Animation(self.game)
        grass_sprites = []
        for i in range(18):
            grass_sprites.append(Sprite(os.path.join("scenes","grass_island_small_house",f"grass{i+1}.png")))
        
        self.grass_animation.register("windy",5,grass_sprites)

        self.water_fg_sprite.set_custom_shader("water_wave_fg.frag")
        self.water_bg_sprite.set_custom_shader("water_wave_bg.frag")

    def update(self):
        self.game.player_manager.update()
        self.grass_sprite.set_custom_uniforms("uTime",time.time() % 1000)
        self.water_fg_sprite.set_custom_uniforms("uTime",time.time() % 1000)
        self.water_bg_sprite.set_custom_uniforms("uTime",time.time() % 1000)

    def draw(self):
        self.sky.draw()
        self.game.window.render(self.water_bg_sprite,[0,132])
        self.game.window.render(self.island_sprite,[0,0])
        self.game.window.render(self.water_fg_sprite,[0,145])
        self.game.window.render(self.house_sprite,[0,0])
        self.game.player_manager.draw()
        self.game.window.render(self.grass_animation.get("windy"),[121,121])
        self.game.window.render(self.cloud_sprite,[0,0])