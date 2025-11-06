import os
from frostlight_engine import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import *

LETTER_MAP = {
    "questionmark":"?",
    "slash":"/",
    "minus":"-",
    "smaller_than":"<",
    "greater_than":">",
    "backslash":r"\\",
    "pipe":"|",
    "star":"*",
    "quote":'"',
    "doubledot":":"
    }
SPACE_SIZE = 3

class Font:
    def __init__(self,game:"Game",scale:int):
        self.game = game
        self.scale = scale
        self.sprite_config = {}
        
        for file in os.listdir(os.path.join("data","sprites","font")):
            letter_name = file.lower().replace(".png","")
            if letter_name in LETTER_MAP:
                letter_name = LETTER_MAP[letter_name]
            sprite = Sprite(os.path.join("font",file))
            self.sprite_config[letter_name] = {"size":sprite.size,"sprite":sprite}

    def set_shader(self,shader):
        for sprite in self.sprite_config:
            self.sprite_config[sprite][sprite].set_custom_shader(shader)

    def draw(self,text:str="",pos:list=[0,0],centered:bool=False):
        w = pos[0]
        if centered:
            width = 0
            for letter in text:
                letter = letter.lower()
                if letter == " ":
                    width += SPACE_SIZE
                else:
                    if letter not in self.sprite_config:
                        letter = "error"
                    width += self.sprite_config[letter]["size"][0]+1

            w = int(pos[0]-width/2)
            for letter in text:
                letter = letter.lower()
                if letter == " ":
                    w += SPACE_SIZE
                else:
                    if letter not in self.sprite_config:
                        letter = "error"
                    self.game.window.render(self.sprite_config[letter]["sprite"],[w,pos[1]])
                    w += self.sprite_config[letter]["size"][0]+1
        else:
            for letter in text:
                letter = letter.lower()
                if letter == " ":
                    w += SPACE_SIZE
                else:
                    if letter not in self.sprite_config:
                        letter = "error"
                    self.game.window.render(self.sprite_config[letter]["sprite"],[w,pos[1]])
                    w += self.sprite_config[letter]["size"][0]+1