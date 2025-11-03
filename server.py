import time
import socket
import pygame
import threading

from data.packets import *
from data.server.events import *

from data.server.classes.client import Client
from data.server.classes.player import Player
from data.server.classes.player_manager import PlayerManager

TICKSPEED = 20

class GameServer:
    def __init__(self):
        self.running = True

        self.delta_time = 1
        self.last_time = 1
        self.clock = pygame.time.Clock()

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self.address = (socket.gethostbyname(socket.gethostname()),50450)
        self.socket.bind(self.address)

        self.player_manager = PlayerManager()

        self.clients: dict[str,Client] = {}
        self.player_client_map: dict[Player, Client] = {}
        self.used_uids = []
        self.event_queue = []

    def update(self):

        print(f'Started game loop')
        self.last_time = time.time()
        while self.running:
            self.clock.tick(TICKSPEED)

            self.delta_time = time.time()-self.last_time
            self.last_time = time.time()

            for event in self.event_queue.copy():
                if type(event) == EventPlayerLeave:

                    # Send every player in old scene the player unload command
                    for player in self.player_manager.get_players_in_scene(event.player.scene):
                        if player.id != event.player.id:
                            self.player_client_map[player].send(PacketUnloadPlayer(event.player.id))

                    # To Do Close client connection
                    self.player_manager.unregister_player(event.player)
                    del self.clients[event.client.address]
                    del self.player_client_map[event.player]

                elif type(event) == EventPlayerChangeScene:

                    # Send every player in old scene the player unload command
                    for player in self.player_manager.get_players_in_scene(event.old_scene):
                        if player.id != event.player.id:
                            self.player_client_map[player].send(PacketUnloadPlayer(event.player.id))

                    # Send every player in new scene the player load command
                    for player in self.player_manager.get_players_in_scene(event.new_scene):
                        if player.id != event.player.id:
                            
                            # Sending to players in scene
                            self.player_client_map[player].send(
                                PacketLoadPlayer(
                                    event.player.id,
                                    event.player.name,
                                    event.player.x,
                                    event.player.y,
                                    event.player.hat,
                                    event.player.body
                                )
                            )

                            # Sending to new player
                            self.player_client_map[event.player].send(
                                PacketLoadPlayer(
                                    player.id,
                                    player.name,
                                    player.x,
                                    player.y,
                                    player.hat,
                                    player.body
                                )
                            )

                elif type(event) == EventPlayerChangeCosmetic:

                    # Send every player in scene the player change cosmetic command
                    for player in self.player_manager.get_players_in_scene(event.player.scene):
                        if player.id != event.player.id:
                            self.player_client_map[player].send(PacketChangeCosmetics(event.player.id, event.player.hat, event.player.body))

                elif type(event) == EventPlayerDoEmoji:

                    # Send every player in scene the player do emoji command
                    if event.player.emoji != None:
                        for player in self.player_manager.get_players_in_scene(event.player.scene):
                            if player.id != event.player.id:
                                self.player_client_map[player].send(PacketDoEmoji(event.player.id, event.player.emoji))

                        event.player.emoji = None
                        
                self.event_queue.remove(event)

            # Update all player in every scene
            for scene in self.player_manager.get_active_scenes_list():
                for player in self.player_manager.get_players_in_scene(scene).copy():
                    if player.id != None:
                        for updating_player in self.player_manager.get_players_in_scene(scene).copy():
                            print("sending update")
                            self.player_client_map[updating_player].send(PacketUpdatePlayer(player.id,player.x, player.y, player.animation, player.flipped))


    def send_all(self, except_player, packet):
        for client in self.clients.copy():
            if self.clients[client].player.id != except_player.id:
                self.clients[client].send(packet)
        
    def stop(self):
        if self.running:
            print(f"[Stopping server]")
            self.running = False
            for client in self.clients:
                self.clients[client].socket.close()
            self.socket.close()
            exit(0)

    def start(self):
        # starting socket and update loop
        print(f'[Starting server]')
        threading.Thread(target=self.update,daemon=True).start()
        self.socket.listen(-1)
        print(f'Server listening on {self.address[0]}:{self.address[1]}')
        while self.running:
            try:
                # accepting new connections
                connection,address = self.socket.accept()
                print(f'New Client: {address[0]}:{address[1]}')
                player = Client(self,connection,address)
                self.clients[address] = player

            except Exception as e:
                if self.running:
                    
                    print(f"Error while listening for new connections: {e}")
                    self.stop()

if __name__ == "__main__":
    server = GameServer()
    server.start()