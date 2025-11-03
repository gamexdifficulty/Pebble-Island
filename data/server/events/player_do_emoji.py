from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.classes.player import Player
    from data.server.classes.client import Client

class EventPlayerDoEmoji():
    def __init__(self, client:"Client", player:"Player"):
        self.client = client
        self.player = player