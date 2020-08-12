import json
import os
from time import sleep

from keyboard import is_pressed as key


class Game():
    def __init__(self,
                 dir_images: str = "images.json",
                 background: str = "",
                 objects: list = [],
                 ):
        self.DIR_IMAGES = dir_images
        self.BACKGROUND = background
        self.OBJECTS = objects
        self.OUTPUT_IMAGE = self.BACKGROUND
        self.OPTIONS_SHOW = True
        self.OPTIONS_VIEW = "------\n|000|\n------"
        self.OPTIONS_IMAGE = "------\n|000|\n------"
        self.JSON_IMAGES = json.load(open(self.DIR_IMAGES,"r"))
        self.WALK_LEFT_PLAYER = False
        self.WALK_RIGHT_PLAYER = False
        self.WALK_UP_PLAYER = False
        self.WALK_DOWN_PLAYER = False
        self.PLAYER = {"img": self.JSON_IMAGES["player_images"]["normal"],
                       "x": 15,
                       "y": 8,
                       "walk_left_sprites":self.JSON_IMAGES["player_images"]["walk_left"],
                       "walk_right_sprites":self.JSON_IMAGES["player_images"]["walk_right"],
                       "hungry":100,
                       "h":self.GetSizeObject(self.JSON_IMAGES["player_images"]["normal"])["h"],
                       "w":self.GetSizeObject(self.JSON_IMAGES["player_images"]["normal"])["w"],
                       "sprite_now": {"side": "img", "index":0, "max":1}
                       }

    def CreateObject(self,x: int, y: int, img: str, name: str = None, up: bool = False, rigid: bool = False):
        self.OBJECTS.append(
            {"name": name,
             "x": x,
             "y": y,
             "up": up,
             "rigid": rigid,
             "img": self.JSON_IMAGES[img]}
        )
    def SetImage(self,x: int, y: int, image: str):
        x_start = x
        x = x
        y = y
        for word in image:
            if word == "\n":
                x = x_start
                y += 1
            else:
                x += 1
                try:
                    if not word == " ":  # this is to see object in background
                        self.OUTPUT_IMAGE[y][x] = word
                except IndexError:
                    break
    def GetSizeObject(self,img: str):
        w = 0
        weights = []
        h = [word for word in img if word == "\n"]

        for word in img:
            if word == "\n":
                weights.append(w)
                w = 0
            else:
                w += 1
        try:
            return {"w": max(weights), "h":len(h)}
        except ValueError:
            return {"w": 0, "h":0}

    # X = 15,
    # Y  = 8,

    # X2 = 15,
    # Y2 = 7

    # w = 3,
    # h = 3,

    # w2 = 3,
    # h2 = 6
    def IsClash(self,x: int, y: int, h: int, w: int,x2: int, y2: int, h2: int, w2: int):
        if (y >= y2 - h2 + h and y - h <= y2 + h2 - h) or (y2 >= y - h + h2 and y2 - h2 <= y + h - h2):
            if (x >= x2 - w2 + w and x - w <= x2 + w2 - w) or (x2 >= x - w + w2 and x2 - w2 <= x + w - w2):
                return True

        return False
#
    def CheckKeysObjects(self):
        self.WALK_LEFT_PLAYER = False
        self.WALK_RIGHT_PLAYER = False
        self.WALK_UP_PLAYER = False
        self.WALK_DOWN_PLAYER = False
        if key("a"):
            self.WALK_LEFT_PLAYER = True
        elif key("d"):
            self.WALK_RIGHT_PLAYER = True
        if key("w"):
            self.WALK_UP_PLAYER = True
        elif key("s"):
            self.WALK_DOWN_PLAYER = True
        if key("f3"):
            self.OPTIONS_SHOW = not self.OPTIONS_SHOW

    def DrawAll(self):
        os.system("cls||clear")
        for line_words in self.OUTPUT_IMAGE:
            for word in line_words:
                print(word, end="")
            print("\n", end="")
        self.OUTPUT_IMAGE = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],]
        """[
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
             ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],] """
    def CheckAll(self):


        self.CheckKeysObjects()  # check moves
        up_of_payer_objects = []

        for object_now in self.OBJECTS:#for in object don't up of player
            if self.WALK_LEFT_PLAYER:
                object_now["x"] += 1

                if self.PLAYER["sprite_now"]["side"] != "walk_left":
                    self.PLAYER["sprite_now"]["index"] = 0
                    self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]
                else:
                    if self.PLAYER["sprite_now"]["index"] >= self.PLAYER["sprite_now"]["max"]:
                        self.PLAYER["sprite_now"]["index"] = 0
                    else:
                        self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]
                        self.PLAYER["sprite_now"]["index"] += 1
                self.PLAYER["sprite_now"]["side"] = "walk_left"
                self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]

            elif self.WALK_RIGHT_PLAYER:
                object_now["x"] -= 1
                if self.PLAYER["sprite_now"]["side"] != "walk_right":
                    self.PLAYER["sprite_now"]["index"] = 0
                    self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]
                else:
                    if self.PLAYER["sprite_now"]["index"] >= self.PLAYER["sprite_now"]["max"]:
                        self.PLAYER["sprite_now"]["index"] = 0
                    else:
                        self.PLAYER["img"] = self.PLAYER["walk_right_sprites"][self.PLAYER["sprite_now"]["index"]]
                        self.PLAYER["sprite_now"]["index"] += 1
                self.PLAYER["sprite_now"]["side"] = "walk_right"
                self.PLAYER["img"] = self.PLAYER["walk_right_sprites"][self.PLAYER["sprite_now"]["index"]]
            if self.WALK_UP_PLAYER:
                object_now["y"] += 1
            elif self.WALK_DOWN_PLAYER:
                object_now["y"] -= 1


            if object_now["up"] == True:
                if not object_now["x"] < 0 and not object_now["y"] < 0:
                    up_of_payer_objects.append(object_now)
                continue
            else:
                if not object_now["x"] < 0 and not object_now["y"] < 0:
                    self.SetImage(x=object_now["x"],y=object_now["y"],image=object_now["img"])
                continue
        self.SetImage(x=self.PLAYER["x"], y=self.PLAYER["y"], image=self.PLAYER["img"]) #"""SET IMAGE OF PLAYER"""

        for object_now in up_of_payer_objects:
            self.SetImage(x=object_now["x"], y=object_now["y"], image=object_now["img"])



        if self.OPTIONS_SHOW:
            self.OPTIONS_VIEW = self.OPTIONS_IMAGE.replace("000",str(self.PLAYER["hungry"]))
            self.SetImage(x=0, y=0, image=self.OPTIONS_VIEW)




    def run(self):
        for object_now in range(len(self.OBJECTS)):
            sizes = self.GetSizeObject(self.OBJECTS[object_now]["img"])
            self.OBJECTS[object_now].update(sizes)
        while True:  # global
            self.CheckAll()
            self.DrawAll()
            sleep(0.1)




#background X: 40
#background Y: 17
















