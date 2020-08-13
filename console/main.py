from time import sleep

from lib.lib import Game
import json
json_images = json.load(open("images.json","r"))
game = Game()
game.CreateObject(
    name="grass",
    x= 2,
    y=4,
    up=False,
    img=json_images["grass_image"])
game.CreateObject(
    name="villager",
    x=-10,
    y=-4,
    up=False,
    img=json_images["villager_image"])
game.CreateObject(
    name="home",
    x=20,
    y=4,
    up=True,
    rigid=True,
    img=json_images["home_image"])

game.run()
