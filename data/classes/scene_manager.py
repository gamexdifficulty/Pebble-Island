import pkgutil
import importlib
import inspect
import data

blacklist = ["inside_house"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Game

class SceneManager:
    def __init__(self, game:"Game"):
        self.game = game
        self.scenes = {}
        self.current_scene = None

        for module_info in pkgutil.iter_modules(data.scenes.__path__):
            module = importlib.import_module(f"{data.scenes.__name__}.{module_info.name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):

                if hasattr(obj, "SCENE_NAME") and obj.SCENE_NAME not in blacklist:
                
                    print(f"obj={obj}")
                    instance = obj(self.game)
                    print(f"instance={instance}")
                    self.register_scene(instance)

    def update(self):
        if self.current_scene != None:
            self.scenes[self.current_scene].update()

    def draw(self):
        if self.current_scene != None:
            self.scenes[self.current_scene].draw()

    def register_scene(self, scene):
        scene_name = scene.SCENE_NAME
        self.scenes[scene_name] = scene

    def load_scene(self, scene_name):
        self.current_scene = scene_name
        self.game.save_manager.save("current_scene",scene_name)