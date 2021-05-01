from lib.lib import Game
import json
from sys import exit
json_images = json.load(open("images.json","r"))
try:
    player_stats = json.load(open("player.json","r"))
except FileNotFoundError:
    player_stats = {}
    name = input("Please, input your game name: ")
    player_stats.update({"name":name})
    with open("player.json","w") as f:
        f.write(json.dumps(player_stats))

server = input("Use servers? Y - if yes, else - no: \n")
my_server = False
if server.lower() == "y":
    server = True
    my_server = input("Connect to server or create? C - connect, else - create: \n")
    if my_server.lower() == "c":
        my_server = False
    else:
        my_server = True
else:
    server = False





game = Game()
if server and my_server:
    address = input("Input new address of server: ")
    if address:
        try:
            port = address.split(":")[1]
            ip = address.split(":")[0]
        except:
            print("Incorrect address")
            input()
            exit()
        game.OpenServer(ip=ip,port=port)
    else:
        game.OpenServer()

elif server and not my_server:
    address = input("Input address of server: ")
    if address:
        try:
            port = address.split(":")[1]
            ip = address.split(":")[0]
        except:
            print("Incorrect address")
            input()
            exit()
        game.ConnectToServer(ip=ip,port=port)
    else:
        game.ConnectToServer()
game.PLAYER.update({"name":player_stats.get("name")})
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
