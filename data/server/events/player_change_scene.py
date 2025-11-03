from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.classes.player import Player
    from data.server.classes.client import Client

class EventPlayerChangeScene():
    def __init__(self, client:"Client",player:"Player",old_scene,new_scene):
        self.client = client
        self.player = player
        self.old_scene = old_scene
        self.new_scene = new_scene