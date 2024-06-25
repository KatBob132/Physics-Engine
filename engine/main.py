from scripts.functions import *
from scripts.objects import *
from scripts.utils import *

from pygame.locals import *
import pygame as pg

from time import time
from sys import exit

color = import_data("engine/data/color.json").get_data()
screen = {}

screen["size"] = (328, 256)
screen["pixel-size"] = 3

screen["surface"] = pg.Surface(screen["size"])

screen["window"] = None
screen["window-back"] = None

size = (screen["size"][0] * screen["pixel-size"], screen["size"][1] * screen["pixel-size"])
tick = 0
text = text_master("engine/data/font.json", screen["surface"])

time_cal = {}
delta = {}

time_cal["elapsed-time"] = 1
time_cal["past-time"] = time()

time_cal["frame-count"] = 0
time_cal["fps"] = 0

delta["delta"] = 0
delta["past-time"] = time()

world = {}

world["camera"] = camera(screen["size"], 0.2)
world["blocks"] = blocks(screen["surface"], color["black"], world["camera"])

world["blocks"].add((56, 56), (24, 24))
world["blocks"].add((256, 56), (24, 24))

world["objects"] = objects(screen["surface"], world["blocks"], world["camera"])

world["objects"].add_object("player", (126, 126), (12, 12), color["red"])
world["objects"].add_data("player", {"move": [False, False, False, False], "speed": 75})

for a in range(10):
    world["objects"].add_object("bot-" + str(a + 1), (0, 24 * a), (12, 12), color["green"])
    world["objects"].add_data("bot-" + str(a + 1), {"angle": 0, "speed" : 50})

pg.init()
flags = DOUBLEBUF
display = pg.display.set_mode(size, flags)
pg.display.set_caption("Game")
fps = pg.time.Clock()

mouse_data = {"xy": [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]}
mouse_data["world-xy"] = [int(mouse_data["xy"][0] / screen["pixel-size"]), int(mouse_data["xy"][1] / screen["pixel-size"])]
mouse_data["buttons"] = [False, False, False]

while True:
    display.fill(color["white"])
    screen["surface"].fill(color["white"])

    pg.mouse.set_visible(False)

    mouse_data["xy"] = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
    mouse_data["world-xy"] = [int(mouse_data["xy"][0] / screen["pixel-size"]), int(mouse_data["xy"][1] / screen["pixel-size"])]

    time_cal["frame-count"] += 1
    time_cal["elapsed-time"] = time() - time_cal["past-time"]

    if time_cal["elapsed-time"] > 1:
        time_cal["fps"] = round(time_cal["frame-count"] / time_cal["elapsed-time"])
        time_cal["frame-count"] = 0
        time_cal["past-time"] = time()

    delta["delta"] = (pg.time.get_ticks() - delta["past-time"]) / 1000
    delta["past-time"] = pg.time.get_ticks()
    
    world["blocks"].draw()
    world["objects"].update(delta["delta"])

    text.draw_text(time_cal["fps"], (1, 1), 1, color["red"], 1)

    pg.draw.rect(screen["surface"], color["red"], pg.Rect(mouse_data["world-xy"][0], mouse_data["world-xy"][1], 1, 1))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            
            if event.key == pg.K_w:
                world["objects"].change_data("player", "move/0", True)
            if event.key == pg.K_s:
                world["objects"].change_data("player", "move/1", True)
            if event.key == pg.K_d:
                world["objects"].change_data("player", "move/2", True)
            if event.key == pg.K_a:
                world["objects"].change_data("player", "move/3", True)
        
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                world["objects"].change_data("player", "move/0", False)
            if event.key == pg.K_s:
                world["objects"].change_data("player", "move/1", False)
            if event.key == pg.K_d:
                world["objects"].change_data("player", "move/2", False)
            if event.key == pg.K_a:
                world["objects"].change_data("player", "move/3", False)

        if event.type == pg.MOUSEBUTTONDOWN:
            for a in range(3):
                if event.button == a + 1:
                    mouse_data["buttons"][a] = True

        if event.type == pg.MOUSEBUTTONUP:
            for a in range(3):
                if event.button == a + 1:
                    mouse_data["buttons"][a] = False
    
    if world["objects"].get_data("player", "move/0"):
        world["objects"].add_velocity("player", (0, -world["objects"].get_data("player", "speed")))
    if world["objects"].get_data("player", "move/1"):
        world["objects"].add_velocity("player", (0, world["objects"].get_data("player", "speed")))
    if world["objects"].get_data("player", "move/2"):
        world["objects"].add_velocity("player", (world["objects"].get_data("player", "speed"), 0))
    if world["objects"].get_data("player", "move/3"):
        world["objects"].add_velocity("player", (-world["objects"].get_data("player", "speed"), 0))

    for a in range(10):
        world["objects"].change_data("bot-" + str(a + 1), "angle", get_angle(world["objects"].objects_data["bot-" + str(a + 1)]["box"].loc(), world["objects"].objects_data["player"]["box"].loc()))
        world["objects"].add_velocity("bot-" + str(a + 1), (si(world["objects"].get_data("bot-" + str(a + 1), "angle")) * world["objects"].get_data("bot-" + str(a + 1), "speed"), ci(world["objects"].get_data("bot-" + str(a + 1), "angle")) * world["objects"].get_data("bot-" + str(a + 1), "speed")))

    screen["window"] = pg.transform.scale(screen["surface"], size)
    screen["window-back"] = pg.transform.scale(screen["surface"], size)

    screen["window-back"].set_alpha(51)

    display.blit(screen["window"], (0, 0))
    display.blit(screen["window-back"], (screen["pixel-size"], screen["pixel-size"]))

    pg.display.update()
    pg.display.flip()
    fps.tick(tick)
