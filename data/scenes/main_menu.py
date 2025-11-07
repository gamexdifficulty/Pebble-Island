import os
import time
from frostlight_engine import *

class SceneMainMenu:
    def __init__(self,game):
        self.game = game

    def update(self):
        pass

    def draw(self):
        self.game.window.fill(76,139,216)