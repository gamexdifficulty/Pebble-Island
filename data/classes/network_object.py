import socket
import threading

from typing import get_type_hints

from data.packets import *

from data.packets.packet import Packet
from data.packets.packet_registry import PACKET_REGISTRY

class NetworkObject:
    def __init__(self, address:list, debug:bool):
        self.connected = False
        self.address = address
        self.debug = debug

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    def receive(self):
        ...

    def send(self,packet):
        if self.connected:
            threading.Thread(target=self.send_thread,args=(packet,)).start()

    def send_thread(self,packet):
        try:
            data = self.pack(packet)
            self.socket.send(data)
        except Exception as e:
            if self.debug:
                print(f"Error while sending package: {data}|{e}")

    def run(self):
        threading.Thread(target=self.loop,args=()).start()

    def unpack(self, data: bytes):
        try:
            pack_id = int.from_bytes(data[:1], "big")
            data = data[1:]

            packet = PACKET_REGISTRY.get(pack_id)

            type_hints = list(get_type_hints(packet).values())
            result = [pack_id]

            for dtype in type_hints:
                if dtype == bool:
                    result.append(data[:1] != b"\x00")
                    data = data[1:]
                elif dtype == int:
                    result.append(int.from_bytes(data[:1], "big"))
                    data = data[1:]
                elif dtype == str:
                    length = int.from_bytes(data[:1], "big")
                    data = data[1:]
                    result.append(data[:length].decode("utf-8"))
                    data = data[length:]
                else:
                    raise TypeError(f"Unsupported type {dtype} in packet {packet.__name__}")

            if data:
                result.append(data)

            return result

        except Exception as e:
            if self.debug:
                print(f"Error while unpacking packet {self.address[0]}:{self.address[1]} | {e}")

    def pack(self,packet:Packet) -> bytes:
        try:
            pack_id = packet.PACKET_ID
            sequence = packet.get_sequence()
            data = packet.data
            result = pack_id.to_bytes(1,"big")
            for i,chunk in enumerate(data):
                if sequence[i] == "b":
                    if chunk == True:
                        result += int(1).to_bytes(1,"big")
                    else:
                        result += int(0).to_bytes(1,"big")
                
                elif sequence[i] == "i":
                    result += chunk.to_bytes(1,"big")

                elif sequence[i] == "s":
                    package = b""
                    for letter in chunk:
                        package += ord(letter).to_bytes(1,"big")
                    result += len(chunk).to_bytes(1,"big") + package

            length = len(result)
            return length.to_bytes(2, "big") + result
        except Exception as e:
            if self.debug:
                print(f'Error while packing package: {self.address[0]}:{self.address[1]}|{pack_id}|{data}|{e}')

    def close(self):
        self.connected = False
        self.send(PacketClientLeft())
        self.socket.close()