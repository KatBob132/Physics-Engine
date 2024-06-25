from json import load
import pygame as pg

class import_data:
    def __init__(self, location):
        self.location = str(location)
        self.file = open(self.location, "r")
        self.data = load(self.file)
    
    def get_data(self):
        return self.data

class config_color:
    def __init__(self, color_value):
        self.color_value = (round(color_value[0]), round(color_value[1]), round(color_value[2]))
    
    def get(self):
        return self.color_value

class text_master:
    def __init__(self, json_file, surface):
        self.text_data = import_data(str(json_file)).get_data()
        self.surface = surface
    
    def draw_text(self, text, xy, size, color, spacing=None, shadow_place=(0, 0), shadow_color=(0, 0, 0)):
        self.text = str(text)
        self.xy = (int(xy[0]), int(xy[1]))
        self.size = int(size)
        self.color = config_color(color).get()

        self.spacing = spacing

        self.shadow_place = (int(shadow_place[0]), int(shadow_place[1]))
        self.shadow_color = config_color(shadow_color).get()

        if self.spacing == None:
            self.spacing = self.size
        else:
            self.spacing = int(self.spacing)

        self.x_place = 0

        for letter in self.text:
            for y in range(len(self.text_data[letter])):
                for x in range(len(self.text_data[letter][0])):
                    if self.text_data[letter][y][x] == 1:
                        if self.shadow_place != (0, 0):
                            pg.draw.rect(self.surface, self.shadow_color, pg.Rect(self.xy[0] + ((x + self.shadow_place[0]) * self.size) + self.x_place, self.xy[1] + ((y + self.shadow_place[1]) * self.size), self.size, self.size))

                        pg.draw.rect(self.surface, self.color, pg.Rect(self.xy[0] + (x * self.size) + self.x_place, self.xy[1] + (y * self.size), self.size, self.size))
                
            self.x_place += (len(self.text_data[letter][0]) * self.size) + self.spacing

class hit_box:
    def __init__(self, xy, size, color, surface):
        self.xy = [float(xy[0]), float(xy[1])]
        self.size = (int(size[0]), int(size[1]))
        self.weight = self.size[0] * self.size[1]

        self.color = color
        self.surface = surface
    
    def loc(self):
        return (self.xy[0] + self.size[0] / 2, self.xy[1] + self.size[1] / 2)

    def draw(self, camera):
        self.camera = (int(camera[0]), int(camera[1]))

        pg.draw.rect(self.surface, self.color, pg.Rect(self.xy[0] - self.camera[0], self.xy[1] - self.camera[1], self.size[0], self.size[1]))

    def collide(self, collide_with_box, offset=(0, 0, 0, 0)):
        self.collide_with_box = ((float(collide_with_box.xy[0]), float(collide_with_box.xy[1])), (float(collide_with_box.size[0]), float(collide_with_box.size[1])))

        self.offset = ((float(offset[0]), float(offset[1])), (float(offset[2]), float(offset[3])))

        self.collide_box = ((float(self.xy[0] + self.offset[0][0]), float(self.xy[1] + self.offset[0][1])), (float(self.size[0] + self.offset[1][0]), float(self.size[1] + self.offset[1][1])))
        self.collided = False

        self.center = (self.collide_box[0][0] + self.collide_box[1][0] / 2, self.collide_box[0][1] + self.collide_box[1][1] / 2)
        self.center_with = (self.collide_with_box[0][0] + self.collide_with_box[1][0] / 2, self.collide_with_box[0][1] + self.collide_with_box[1][1] / 2)

        self.center_diff = (abs(self.center[0] - self.center_with[0]), abs(self.center[1] - self.center_with[1]))

        if self.center_diff[0] < self.collide_with_box[1][0] / 2 + self.collide_box[1][0] / 2 and self.center_diff[1] < self.collide_with_box[1][1] / 2 + self.collide_box[1][1] / 2:
            self.collided = True

        return self.collided