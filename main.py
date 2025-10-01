# main.py
import sys

from engine import GameEngine
from scenes.menu_scene import MenuScene
from scenes.battle_scene import BattleScene
from pets import Dog

if __name__ == "__main__":
    game = GameEngine()
    print("Args:", sys.argv)
    if "--test" in sys.argv:
        test_pet = Dog("TestDog", "Labrador")
        image_path = "assets/images/dog.png"
        scene = BattleScene(game, test_pet, image_path)

        # ✅ Setup for opponent turn test
        scene.stamina = 0
        scene.player_power = 4
        scene.start_opponent_turn()

        game.set_scene(scene)

    else:
        game.set_scene(MenuScene(game))

    game.run()
