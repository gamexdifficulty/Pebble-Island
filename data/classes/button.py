from frostlight_engine import *
from typing import TYPE_CHECKING
from utils.load_shader import load_shader
if TYPE_CHECKING:
    from main import Game

class Button:
    def __init__(self,game:"Game",sprite_path:str=None,pos:list=[0,0],size:list=None,callback=None,shader=None):
        self.game = game
        self.sprite = Sprite(sprite_path)
        if shader != None:
            self.sprite.set_custom_shader(load_shader(shader))
        
        self.pos = pos
        self.size = [0,0]
        if size == None:
            self.size = self.sprite.size
        else:
            self.size = size

        self.selected = True

        self.callback = callback
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self):
        self.sprite.alpha = 1.0
        if self.rect.collidepoint(self.game.input.mouse.get_pos()) or self.selected:
            self.sprite.alpha = 0.5
            if self.game.input.get("accept"):
                self.callback()

    def draw(self):
        self.game.window.render(self.sprite,self.pos)