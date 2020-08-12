from time import sleep

from lib.lib import Game


game = Game()
game.CreateObject(
    name="grass",
    x= 2,
    y=4,
    up=False,
    img="grass_image")
game.CreateObject(
    name="villager",
    x=-10,
    y=-4,
    up=False,
    img="villager_image")
game.CreateObject(
    name="home",
    x=20,
    y=4,
    up=True,
    rigid=True,
    img="home_image")

game.run()
