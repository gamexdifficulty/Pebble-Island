import socket
import threading

from typing import TYPE_CHECKING

from utils.generate_uid import generate_uid

from data.packets import *
from data.server.events import *

from data.server.classes.player import Player
from data.server.classes.network_object import NetworkObject

from data.packets.packet_registry import PACKET_REGISTRY

if TYPE_CHECKING:
    from server import GameServer

class Client(NetworkObject):
    def __init__(self,game:"GameServer",connection:socket.socket,address:list):
        super().__init__(connection, address, self.remove_player)

        self.game = game
        self.player = Player()

        game.player_client_map[self.player] = self

        self.packet_function_map = {

            # function mapping variable for incoming packets
            0:  self.player_left,
            1:  self.player_get_session_id,
            11: self.player_change_scene,
            14: self.update_player,
            15: self.player_change_cosmetic,
            16: self.player_do_emoji
        }

        threading.Thread(target=self.receive).start()

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
                self.player_left()


    def player_left(self):
        self.close()
        self.remove_player()

    def remove_player(self):
        self.game.event_queue.append(EventPlayerLeave(self, self.player))

    def player_get_session_id(self,packet:PacketRequestSessionID):
        player_session_id = generate_uid(self.game.used_uids)

        self.player.name = packet.name
        self.player.id = player_session_id
        
        self.send(PacketReturnSessionID(player_session_id))

        self.game.player_manager.register_player(self.player)

    def player_change_scene(self,packet:PacketPlayerGoToScene):
        if self.player.id == packet.session_id:
            self.game.player_manager.player_change_scene(self.player, self.player.scene, packet.scene)
            self.game.event_queue.append(EventPlayerChangeScene(self, self.player, self.player.scene ,packet.scene))

            self.player.scene = packet.scene
            self.player.name = packet.name
            self.player.hat = packet.hat
            self.player.body = packet.body

    def update_player(self,packet:PacketUpdatePlayer):
        if self.player.id == packet.session_id:
            self.player.x = packet.x
            self.player.y = packet.y
            self.player.animation = packet.animation
            self.player.flipped = packet.flipped

    def player_change_cosmetic(self,packet:PacketChangeCosmetics):
        if self.player.id == packet.session_id:
            self.player.hat = packet.hat
            self.player.body = packet.body

            self.game.event_queue.append(EventPlayerChangeCosmetic(self, self.player))

    def player_do_emoji(self,packet:PacketDoEmoji):
        if self.player.id == packet.session_id:
            self.player.emoji = packet.emoji

            self.game.event_queue.append(EventPlayerDoEmoji(self, self.player))