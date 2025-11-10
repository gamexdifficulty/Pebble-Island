import os
from frostlight_engine import *

from data.classes.overlay_manager import OVERLAY_MANAGER

@OVERLAY_MANAGER.register_overlay
class TestOverlay:

    OVERLAY_NAME = "test_overlay"

    def __init__(self, game):
        self.game = game
        
        self.house_background_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_small_house.png"))
        self.house_oven_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_small_house_oven.png"))
        self.house_book_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_small_house_book.png"))
        self.house_mirror_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_small_house_mirror.png"))

    def update(self):
        self.game.overlay_manager.update()

    def draw(self):
        self.game.window.fill(51,44,58)
        self.game.window.render(self.house_background_sprite,[0,0])
        self.game.window.render(self.house_oven_sprite,[0,0])
        self.game.window.render(self.house_book_sprite,[0,0])
        self.game.window.render(self.house_mirror_sprite,[0,0])

        self.game.player_manager.draw()