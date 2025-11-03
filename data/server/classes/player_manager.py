from data.classes.player import Player

class PlayerManager:
    def __init__(self):
        self.scene_list = {}
        self.player_list = {}
    
    def get_player(self,session_id):
        if session_id in self.player_list:
            return self.player_list[session_id]
        else:
            return False

    def get_players_in_scene(self,scene:str) -> list[Player]:
        if scene in self.scene_list:
            return self.scene_list[scene]
        else:
            return []
        
    def get_active_scenes_list(self) -> list[str]:
        return self.scene_list.keys()

    def player_change_scene(self,player,from_scene,to_scene):
        if from_scene in self.scene_list and player in self.scene_list[from_scene]:
            self.scene_list[from_scene].remove(player)
            if len(self.scene_list[from_scene]) == 0:
                del self.scene_list[from_scene]

        if to_scene not in self.scene_list:
            self.scene_list[to_scene] = []

        self.scene_list[to_scene].append(player)

    def register_player(self,player):
        self.player_list[player.id] = player

    def unregister_player(self,player):
        if player.id in self.player_list:
            del self.player_list[player.id]

        for scene in self.scene_list.copy():
            if player in self.scene_list[scene]:
                self.scene_list[scene].remove(player)
