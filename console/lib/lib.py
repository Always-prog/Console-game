import json
import os
import threading
from random import randint
from time import sleep
from uuid import uuid4
from keyboard import is_pressed as key, KEY_DOWN as key_down

from sys import exit

class Game():
    def __init__(self,
                 dir_images: str = "images.json",
                 background: str = "",
                 objects: list = [],
                 ):
        self.DIR_IMAGES = dir_images
        self.JSON_IMAGES = json.load(open(self.DIR_IMAGES,"r"))
        self.BACKGROUND = background
        self.BACKGROUND_X = 40
        self.BACKGROUND_Y = 17
        self.OBJECTS = objects
        self.MINIMIZE_HUNGRY_COUNT = 0.02
        self.ADD_HUNGRY_COUNT = 10.0
        self.OUTPUT_IMAGE = self.BACKGROUND
        self.OPTIONS_SHOW = True
        self.OPTIONS_VIEW = "------\n|000|\n------"
        self.OPTIONS_IMAGE = "------\n|000|\n------"
        self.INVENTORY_IMAGE = self.JSON_IMAGES["inventory_image"]
        self.WALK_LEFT_PLAYER = False
        self.WALK_RIGHT_PLAYER = False
        self.WALK_UP_PLAYER = False
        self.WALK_DOWN_PLAYER = False
        self.KEY_F = False
        self.PLAYER = {"img": self.JSON_IMAGES["player_images"]["normal"],
                       "image_normal":self.JSON_IMAGES["player_images"]["normal"],
                       "x": 15,
                       "y": 8,
                       "walk_left_sprites":self.JSON_IMAGES["player_images"]["walk_left"],
                       "walk_right_sprites":self.JSON_IMAGES["player_images"]["walk_right"],
                       "hungry":100.00,
                       "h":self.GetSizeObject(self.JSON_IMAGES["player_images"]["normal"])["h"],
                       "w":self.GetSizeObject(self.JSON_IMAGES["player_images"]["normal"])["w"],
                       "sprite_now": {"side": "img", "index":0, "max":1},
                       "inventory_must_update": True,
                       "selected_now":"0",
                       "default_inventory_item":lambda num:{"status":"space","name":"#"+str(num), "minimize_image":"#"+str(num)},
                       "inventory":{
                           "0":{"status":"space","name":"#0", "minimize_image":"#0"},
                           "1":{"status":"space","name":"#1", "minimize_image":"#1"},
                           "2":{"status":"space","name":"#2", "minimize_image":"#2"},
                           "3":{"status":"space","name":"#3", "minimize_image":"#3"},
                       }
                       }
    def CreateInventoryObject(self,object_for_paste: dict):
        for inventory_item in range(len(self.PLAYER["inventory"])):
            object_for_paste.update({"minimize_image":object_for_paste["data"]["minimize_image"]})
            if self.PLAYER["inventory"][str(inventory_item)]["status"] == "space":
                self.PLAYER["inventory"][str(inventory_item)] = object_for_paste
                self.PLAYER["inventory"][str(inventory_item)]["status"] = object_for_paste["name"]
                self.PLAYER["inventory_must_update"] = True
                return True
            else:
                self.PLAYER["inventory_must_update"] = False
    def InventoryView(self):
        if self.PLAYER["inventory_must_update"]:
            list_image = list(self.INVENTORY_IMAGE)
            list_image[15] = list(self.PLAYER["inventory"]["0"]["minimize_image"])[0]
            list_image[16] = list(self.PLAYER["inventory"]["0"]["minimize_image"])[1]

            list_image[18] = list(self.PLAYER["inventory"]["1"]["minimize_image"])[0]
            list_image[19] = list(self.PLAYER["inventory"]["1"]["minimize_image"])[1]

            list_image[21] = list(self.PLAYER["inventory"]["2"]["minimize_image"])[0]
            list_image[22] = list(self.PLAYER["inventory"]["2"]["minimize_image"])[1]

            list_image[24] = list(self.PLAYER["inventory"]["3"]["minimize_image"])[0]
            list_image[25] = list(self.PLAYER["inventory"]["3"]["minimize_image"])[1]
            self.INVENTORY_IMAGE = "".join(list_image)
        self.SetImage(x=0,y=15,image=self.INVENTORY_IMAGE)
    def CreateObject(self,x: int, y: int, img: str, name: str = None, up: bool = False, rigid: bool = False, data: dict = {}):
        size_object = self.GetSizeObject(img=img)
        self.OBJECTS.append(
            {"name": name,
             "x": x,
             "y": y,
             "up": up,
             "rigid": rigid,
             "h":size_object["h"],
             "w":size_object["w"],
             "id":uuid4().hex,
             "data":data,
             "img": img}
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
    def QuitItem(self):
        for inventory_item in range(len(self.PLAYER["inventory"])):
            if self.PLAYER["inventory"][str(inventory_item)]["status"] != "space":
                self.CreateObject(
                    img=self.PLAYER["inventory"][str(inventory_item)]["img"],
                    x=self.PLAYER["x"],
                    y=self.PLAYER["y"],
                    name=self.PLAYER["inventory"][str(inventory_item)]["name"],
                    data=self.PLAYER["inventory"][str(inventory_item)]["data"],
                )
                self.DestroyItem(index_item=str(inventory_item))
                break
    def DestroyItem(self,index_item: str):
        item = self.PLAYER["inventory"][index_item]
        self.PLAYER["inventory"][index_item] = self.PLAYER["default_inventory_item"](index_item)
        self.PLAYER["inventory_must_update"] = True
        return item
    def SpawnEat(self):
        for meat in range(4):
            self.CreateObject(
                x=randint(0,self.BACKGROUND_X),
                y=randint(0,self.BACKGROUND_Y),
                data={"minimize_image":self.JSON_IMAGES["eat"]["meat"]["minimize_image"]},
                img=self.JSON_IMAGES["eat"]["meat"]["default_image"],
                name="meat"
            )

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
        if key("f"):
            self.KEY_F = True
        else:
            self.KEY_F= False
        if key("x"):
            self.QuitItem()
        if key("e"):
            self.UseEat()
        if key("esc"):
            exit()

    def InventoryIsSpace(self):
        for inventory_item in range(len(self.PLAYER["inventory"])):
            if self.PLAYER["inventory"][str(inventory_item)]["status"] == "space":
                return True
        return False
    def UseEat(self):
        for inventory_item in range(len(self.PLAYER["inventory"])):
            if self.PLAYER["inventory"][str(inventory_item)]["name"] == "meat":
                if self.PLAYER["hungry"] + self.ADD_HUNGRY_COUNT < 100.0:
                    self.PLAYER["hungry"] += self.ADD_HUNGRY_COUNT
                    self.DestroyItem(index_item=str(inventory_item))
    def MinimizeHungry(self):
        self.PLAYER["hungry"] -= 2
    def DrawAll(self):
        os.system("cls||clear")
        for line_words in self.OUTPUT_IMAGE:
            for word in line_words:
                print(word, end="")
            print("\n", end="")
        self.OUTPUT_IMAGE = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "," ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],]


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
        items_objects = []
        if self.PLAYER["hungry"] <= 0.0:
            print(self.JSON_IMAGES["dead_image"])
            exit()
        for object_now in range(len(self.OBJECTS)):#for in object don't up of player
            try:
                self.OBJECTS[object_now]
            except IndexError:
                continue
            self.PLAYER["img"] = self.PLAYER["image_normal"]
            if self.WALK_LEFT_PLAYER:
                self.OBJECTS[object_now]["x"] += 1
                if self.PLAYER["sprite_now"]["side"] != "walk_left":
                    self.PLAYER["sprite_now"]["index"] = 0
                    self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]

                else:
                    if self.PLAYER["sprite_now"]["index"] >= self.PLAYER["sprite_now"]["max"]:
                        self.PLAYER["sprite_now"]["index"] = 0
                    else:

                        self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]
                        self.PLAYER["sprite_now"]["index"] += 1
                self.PLAYER["hungry"] -= self.MINIMIZE_HUNGRY_COUNT  # minimize hungry because player is walk
                self.PLAYER["sprite_now"]["side"] = "walk_left"
                self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]

            elif self.WALK_RIGHT_PLAYER:
                self.OBJECTS[object_now]["x"] -= 1
                if self.PLAYER["sprite_now"]["side"] != "walk_right":
                    self.PLAYER["sprite_now"]["index"] = 0
                    self.PLAYER["img"] = self.PLAYER["walk_left_sprites"][self.PLAYER["sprite_now"]["index"]]
                else:
                    if self.PLAYER["sprite_now"]["index"] >= self.PLAYER["sprite_now"]["max"]:
                        self.PLAYER["sprite_now"]["index"] = 0
                    else:
                        self.PLAYER["img"] = self.PLAYER["walk_right_sprites"][self.PLAYER["sprite_now"]["index"]]
                        self.PLAYER["sprite_now"]["index"] += 1
                self.PLAYER["hungry"] -= self.MINIMIZE_HUNGRY_COUNT  # minimize hungry because player is walk
                self.PLAYER["sprite_now"]["side"] = "walk_right"
                self.PLAYER["img"] = self.PLAYER["walk_right_sprites"][self.PLAYER["sprite_now"]["index"]]
            if self.WALK_UP_PLAYER:
                self.PLAYER["hungry"] -= self.MINIMIZE_HUNGRY_COUNT  # minimize hungry because player is walk
                self.OBJECTS[object_now]["y"] += 1
            elif self.WALK_DOWN_PLAYER:
                self.PLAYER["hungry"] -= self.MINIMIZE_HUNGRY_COUNT  # minimize hungry because player is walk
                self.OBJECTS[object_now]["y"] -= 1

            if self.OBJECTS[object_now]["name"] == "meat":
                items_objects.append(object_now)
                is_clash = self.IsClash(
                    x=self.OBJECTS[object_now]["x"],
                    y=self.OBJECTS[object_now]["y"],
                    h=self.OBJECTS[object_now]["h"],
                    w=self.OBJECTS[object_now]["w"],
                    x2=self.PLAYER["x"],
                    y2=self.PLAYER["y"],
                    h2=self.PLAYER["h"],
                    w2=self.PLAYER["w"],
                )

                if is_clash:
                    self.SetImage(x=7, y=0, image=self.JSON_IMAGES["message_up"])
                    if self.InventoryIsSpace():
                        if self.KEY_F:
                            try:
                                if self.PLAYER["hungry"] + self.ADD_HUNGRY_COUNT < 100.0:#if hungry is not more on 100
                                    self.CreateInventoryObject(object_for_paste=self.OBJECTS[object_now])
                                    del self.OBJECTS[object_now]
                                    break
                                else:
                                    pass#player don't can to eat more

                            except IndexError:
                                pass
                    else:
                        self.SetImage(x=7, y=0, image=self.JSON_IMAGES["message_cant_up"])



            if self.OBJECTS[object_now]["up"] == True:
                if not self.OBJECTS[object_now]["x"] < 0 and not self.OBJECTS[object_now]["y"] < 0:
                    up_of_payer_objects.append(self.OBJECTS[object_now])
                continue
            else:
                if not self.OBJECTS[object_now]["x"] < 0 and not self.OBJECTS[object_now]["y"] < 0:
                    self.SetImage(x=self.OBJECTS[object_now]["x"],y=self.OBJECTS[object_now]["y"],image=self.OBJECTS[object_now]["img"])
                continue

        self.SetImage(x=self.PLAYER["x"], y=self.PLAYER["y"], image=self.PLAYER["img"]) #"""SET IMAGE OF PLAYER"""

        for object_now in up_of_payer_objects:
            try:
                self.SetImage(x=object_now["x"], y=object_now["y"], image=object_now["img"])
            except IndexError:
                continue

        #default checks
        self.InventoryView()
        if self.OPTIONS_SHOW:
            self.OPTIONS_VIEW = self.OPTIONS_IMAGE.replace("000",str(self.PLAYER["hungry"]))
            self.SetImage(x=32, y=0, image=self.OPTIONS_VIEW)

    def Eat(self):
        # scheduler to start spawn eat, and start minimize hungry
        while True:
            sleep(4)
            if len([i for i in self.OBJECTS if i["name"] == "meat"]) < 10:
                self.SpawnEat()
            sleep(1)
            self.MinimizeHungry()


    def Start(self):
        while True:  # global
            self.CheckAll()
            self.DrawAll()
            sleep(0.01)
    def run(self):
        proc1 = threading.Thread(target=self.Start)
        proc1.start()
        proc2 = threading.Thread(target=self.Eat)
        proc2.start()















