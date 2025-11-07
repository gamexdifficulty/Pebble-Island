from frostlight_engine import *
from typing import TYPE_CHECKING

from data.packets import *

from data.classes.animation import Animation

if TYPE_CHECKING:
    from main import Game

class Player:
    def __init__(self, game:"Game", can_be_controlled=False):
        self.game = game
        self.x = 160
        self.y = 120
        self.target_x = self.x
        self.target_y = self.y
        self.id = None
        self.name = "Test"
        self.can_be_controlled = can_be_controlled
        self.flipped = False
        self.alpha = 0.0
        self.hat = 0
        self.body = 0

        self.animation_state = "idle"
        self.animation = Animation(self.game)
        self.animation.register("idle",1,[Sprite(os.path.join("player","player_idle_1.png"))])
        self.animation.register("sit",1,[Sprite(os.path.join("player","player_sit_1.png"))])
        self.animation.register("quack",1,[Sprite(os.path.join("player","player_quack_1.png"))])
        self.animation.register("sit_quack",1,[Sprite(os.path.join("player","player_sit_quack_1.png"))])
        self.animation.register("walk",0.15,[Sprite(os.path.join("player","player_walk_1.png")),
                                          Sprite(os.path.join("player","player_walk_2.png"))])
        
        self.emoji_timer = 0
        self.emoji = None
        self.emoji_sprites = [
            Sprite(os.path.join("player","emojis","star.png")),
            Sprite(os.path.join("player","emojis","heart.png")),
            Sprite(os.path.join("player","emojis","happy.png")),
            Sprite(os.path.join("player","emojis","sad.png")),
            Sprite(os.path.join("player","emojis","talking.png")),
            Sprite(os.path.join("player","emojis","left.png")),
            Sprite(os.path.join("player","emojis","right.png")),
            Sprite(os.path.join("player","emojis","up.png")),
            Sprite(os.path.join("player","emojis","down.png"))
        ]

    def update(self):

        if self.emoji_timer > 0:
            self.emoji_timer = max(self.emoji_timer-self.game.delta_time,0)
            if self.emoji_timer == 0:
                self.emoji = None

        if self.alpha != 1.0:
            self.alpha = min(1,self.alpha+self.game.delta_time*0.75)
      
        if self.can_be_controlled:
            direction = self.game.input.get("right")-self.game.input.get("left")
            sit = self.game.input.get("down")
            quack = self.game.input.get("up")
            if self.game.input.get("emoji1") and self.emoji == None: self.do_emoji(0)
            if self.game.input.get("emoji2") and self.emoji == None: self.do_emoji(1)
            if self.game.input.get("emoji3") and self.emoji == None: self.do_emoji(2)
            if self.game.input.get("emoji4") and self.emoji == None: self.do_emoji(3)
            if self.game.input.get("emoji5") and self.emoji == None: self.do_emoji(4)
            if self.game.input.get("emoji6") and self.emoji == None: self.do_emoji(5)
            if self.game.input.get("emoji7") and self.emoji == None: self.do_emoji(6)
            if self.game.input.get("emoji8") and self.emoji == None: self.do_emoji(7)
            if self.game.input.get("emoji9") and self.emoji == None: self.do_emoji(8)

            self.x = min(209,max(121,self.x + direction*self.game.delta_time*25))
            if direction == 1:
                self.flipped = False
                self.animation_state = "walk"
            elif direction == -1:
                self.flipped = True
                self.animation_state = "walk"
            else:

                if self.animation_state == "sit_quack" and not quack:
                    self.animation_state = "sit"

                elif (self.animation_state != "sit") and not quack:
                    self.animation_state = "idle"

                if sit:
                    self.animation_state = "sit"
                elif quack:
                    if self.animation_state == "sit" or self.animation_state == "sit_quack":
                        self.animation_state = "sit_quack"
                    else:
                        self.animation_state = "quack"

        else:
            # Network movement
            smoothing = 20
            self.x += (self.target_x - self.x) * min(smoothing * self.game.delta_time, 1)
            self.y += (self.target_y - self.y) * min(smoothing * self.game.delta_time, 1)

    def do_emoji(self,emoji:int):
        self.emoji = emoji
        self.emoji_timer = 3
        if self.can_be_controlled:
            self.game.network_manager.send(PacketDoEmoji(self.id,self.emoji))

    def draw(self):
        sprite = self.animation.get(self.animation_state)
        sprite.flipped = self.flipped
        sprite.alpha = self.alpha
        self.game.window.render(sprite, [int(self.x),int(self.y)])

        if self.emoji != None:
            self.game.window.render(self.emoji_sprites[self.emoji], [self.x-1,self.y - 9])
            