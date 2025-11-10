from frostlight_engine import *

from data.classes.network import NetworkManager
from data.classes.player_manager import PlayerManager
from data.classes.scene_manager import SceneManager
from data.classes.player import Player

from data.scenes.grass_island_small_house import SceneHome
from data.scenes.main_menu import SceneMainMenu

from data.classes.font import Font
from data.classes.time import Time

class Game(FrostlightEngine):
    def __init__(self):
        super().__init__(canvas_size=[320,180],fps_limit=165)
        self.running = True
        self.debug = True

        self.state = "main_menu"

        self.input.new("emoji1",KEY_1,CLICKED)
        self.input.new("emoji2",KEY_2,CLICKED)
        self.input.new("emoji3",KEY_3,CLICKED)
        self.input.new("emoji4",KEY_4,CLICKED)
        self.input.new("emoji5",KEY_5,CLICKED)
        self.input.new("emoji6",KEY_6,CLICKED)
        self.input.new("emoji7",KEY_7,CLICKED)
        self.input.new("emoji8",KEY_8,CLICKED)
        self.input.new("emoji9",KEY_9,CLICKED)

        self.network_manager = NetworkManager(self)
        self.scene_manager = SceneManager(self)
        self.player_manager = PlayerManager(self)

        self.player = Player(self,True)
        self.player_manager.register_player(self.player)

        self.scene_manager.register_scene("grass_island_small_house", SceneHome(self))
        self.scene_manager.register_scene("main_menu", SceneMainMenu(self))

        self.scene_manager.load_scene("grass_island_small_house")

        self.font = Font(self,1)
        self.time = Time(self)

        self.network_manager.run()
    
    def event_quit(self):
        self.running = False
        self.network_manager.close()
    
    def update(self):
        self.time.update()
        self.scene_manager.update()

    def draw(self):
        self.scene_manager.draw()

game = Game()
game.run()