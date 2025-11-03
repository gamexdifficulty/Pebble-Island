import time
import pygame
import threading

from data.packets import *
from typing import TYPE_CHECKING

from data.packets.packet_registry import PACKET_REGISTRY
from data.classes.network_object import NetworkObject

if TYPE_CHECKING:
    from main import Game

class NetworkManager(NetworkObject):
    def __init__(self,game:"Game"):
        # super().__init__(("penguin.frostlightgames.net",50450))
        super().__init__(("192.168.2.128",50450))
        self.game = game

        self.packet_function_map = {

            # function mapping variable for incoming packets
            2:  self.get_session_id,
            12: self.load_player,
            13: self.unload_player,
            14: self.player_update,
            15: self.player_change_cosmetic,
            16: self.player_do_emoji
        }

    def receive(self):
        buffer = b""
        while self.game.running and self.connected:
            try:
                chunk = self.socket.recv(512)
                if not chunk:
                    continue
                buffer += chunk

                # Process all complete packets
                while len(buffer) >= 2:
                    packet_len = int.from_bytes(buffer[:2], "big")
                    if len(buffer) < 2 + packet_len:
                        break  # wait for more data
                    packet_data = buffer[2:2+packet_len]
                    buffer = buffer[2+packet_len:]

                    data = self.unpack(packet_data)
                    pack_id = data[0]
                    args = data[1:]
                    packet_cls = PACKET_REGISTRY.get(pack_id)
                    packet = packet_cls.from_bytes(args)
                    handler = self.packet_function_map.get(pack_id)
                    handler(packet)

            except Exception as e:
                print(f"Error while receiving data: {self.address[0]}:{self.address[1]} | {e}")
                self.close()

    def get_session_id(self, packet:PacketReturnSessionID):
        print(f"Player got session id {packet.session_id}")
        self.game.player.id = packet.session_id
        player = self.game.player
        self.game.network_manager.send(
            PacketPlayerGoToScene(
                player.id,
                self.game.scene_manager.current_scene,
                player.name,
                int(player.x),
                int(player.y),
                player.hat,
                player.body
            )
        )

    def load_player(self, packet:PacketLoadPlayer):
        self.game.player_manager.create_network_player(packet.session_id,packet.name,packet.hat,packet.body)

    def unload_player(self, packet:PacketUnloadPlayer):
        self.game.player.id = packet.session_id

    def player_update(self,packet:PacketUpdatePlayer):
        player = self.game.player_manager.get(packet.session_id)
        if player:
            player.target_x = packet.x
            player.target_y = packet.y
            player.animation_state = packet.animation
            player.flipped = packet.flipped

    def player_change_cosmetic(self,packet:PacketChangeCosmetics):
        player = self.game.player_manager.get(packet.session_id)
        if player:
            player.hat = packet.hat
            player.body = packet.body

    def player_do_emoji(self,packet:PacketDoEmoji):
        player = self.game.player_manager.get(packet.session_id)
        if player:
            player.do_emoji(packet.emoji)

    def loop(self):
        while self.game.running:
            while not self.connected and self.game.running:
                try:
                    self.socket.connect(self.address)
                    self.connected = True
                    threading.Thread(target=self.receive,daemon=True).start()
                    self.send(PacketRequestSessionID(self.game.player.name))
                except Exception as e:
                    print(f"Failed to connect to server {e}")
                    time.sleep(1)

            clock = pygame.time.Clock()
            while self.connected:
                clock.tick(20)
                player = self.game.player
                if player.id != None:
                    self.send(PacketUpdatePlayer(player.id,int(player.x),int(player.y),player.animation_state,player.flipped))

            self.connected = False