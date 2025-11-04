import os
import time
from frostlight_engine import *

class SceneInsideHouse:
    def __init__(self,game):
        self.game = game
        
        self.unlocked = [] #[0,1,2,3,4,5] # max permitted value is 5

        # old idea on grass island now unused
        self.house_background_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_background.png"))
        self.house_workbench_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_workbench.png"))
        self.house_wardrobe_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_wardrobe.png"))
        self.house_table_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_table.png"))
        self.house_pictures_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_pictures.png"))
        self.house_oven_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_oven.png"))
        self.house_ladder_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_ladder.png"))
        self.house_chest_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_chest.png")) 
        self.house_bookshelf_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_bookshelf.png"))
        self.house_book_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_book.png"))
        self.house_bed_sprite = Sprite(os.path.join("scenes","grass_island_inside","inside_bed.png"))

        self.unlockable_sprits = [self.house_wardrobe_sprite, self.house_pictures_sprite, self.house_ladder_sprite, 
                                  self.house_chest_sprite, self.house_bookshelf_sprite, self.house_bed_sprite]

    def update(self):
        self.game.player_manager.update()

    def draw(self):
        self.game.window.fill(51,44,58)
        self.game.window.render(self.house_background_sprite,[0,0])
        self.game.window.render(self.house_table_sprite,[0,0])
        self.game.window.render(self.house_workbench_sprite,[0,0])
        self.game.window.render(self.house_book_sprite,[0,0])
        self.game.window.render(self.house_oven_sprite,[0,0])

        for value in self.unlocked:
            self.game.window.render(self.unlockable_sprits[value],[0,0])

        self.game.player_manager.draw()
