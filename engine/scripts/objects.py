from scripts.functions import *
from scripts.utils import *

class camera:
    def __init__(self, camera_size, camera_drag):
        self.camera_size = (int(camera_size[0]), int(camera_size[1]))
        self.camera_drag = float(camera_drag)
        self.camera_data = {}

        self.camera_data["real"] = [0, 0]
        self.camera_data["drag"] = [0, 0]
        self.camera_data["use"] = [0, 0]

    def update(self, update_target, update_delta):
        self.update_target = update_target
        self.update_delta = float(update_delta)

        self.update_target_xy = (round(self.update_target.xy[0]), round(self.update_target.xy[1]))
        self.update_target_size = (int(self.update_target.size[0]), int(self.update_target.size[1]))

        self.camera_data["real"] = [self.update_target_xy[0] + self.update_target_size[0] / 2 - self.camera_size[0] / 2, self.update_target_xy[1] + self.update_target_size[1] / 2 - self.camera_size[1] / 2]

        for a in range(2):
            self.camera_data["drag"][a] += (self.camera_data["real"][a] - self.camera_data["drag"][a]) / (self.camera_drag / self.update_delta)
            self.camera_data["use"][a] = round(self.camera_data["drag"][a])

class blocks:
    def __init__(self, block_surface, block_color, block_camera):
        self.block_surface = block_surface
        self.block_color = config_color(block_color).get()
        self.block_camera = block_camera

        self.block_list = []

    def add(self, add_xy, add_size):
        self.block_list.append(hit_box(add_xy, add_size, self.block_color, self.block_surface))
    
    def draw(self):
        for block in self.block_list:
            block.draw(self.block_camera.camera_data["use"])

class objects:
    def __init__(self, objects_surface, objects_blocks, objects_camera):
        self.objects_surface = objects_surface
        self.objects_blocks = list(objects_blocks.block_list)
        self.objects_camera = objects_camera

        self.object_inaccuracy = 0.1
        self.objects_data = {}
        
    def add_object(self, add_object_tag, add_object_xy, add_object_size, add_object_color, add_object_data={}):
        self.add_object_tag = str(add_object_tag)
        self.add_object_box = hit_box(add_object_xy, add_object_size, add_object_color, self.objects_surface)
        self.add_object_data = dict(add_object_data)

        self.objects_data[self.add_object_tag] = {}

        self.objects_data[self.add_object_tag]["box"] = self.add_object_box
        self.objects_data[self.add_object_tag]["velocity"] = [0, 0]
        self.objects_data[self.add_object_tag]["data"] = self.add_object_data
    
    def add_velocity(self, add_velocity_tag, add_velocity_amount):
        self.add_velocity_tag = str(add_velocity_tag)
        self.add_velocity_amount = (float(add_velocity_amount[0]), float(add_velocity_amount[1]))

        self.objects_data[self.add_velocity_tag]["velocity"][0] += self.add_velocity_amount[0]
        self.objects_data[self.add_velocity_tag]["velocity"][1] += self.add_velocity_amount[1]
    
    def add_data(self, add_data_tag, add_data_dict):
        self.add_data_tag = str(add_data_tag)
        self.add_data_dict = dict(add_data_dict)

        self.objects_data[self.add_data_tag]["data"].update(add_data_dict)
    
    def change_data(self, change_data_tag, change_data_address, change_data_new):
        self.change_data_tag = str(change_data_tag)
        self.change_data_address = str(change_data_address).split("/")
        self.change_data_new = change_data_new

        self.change_data_current = self.objects_data[self.change_data_tag]["data"][self.change_data_address[0]]
        
        if type(self.change_data_current) == list:
            self.objects_data[self.change_data_tag]["data"][self.change_data_address[0]][int(self.change_data_address[1])] = self.change_data_new
        elif type(self.change_data_current) == dict:
            self.objects_data[self.change_data_tag]["data"][self.change_data_address[0]][str(self.change_data_address[1])] = self.change_data_new
        else:
            self.objects_data[self.change_data_tag]["data"][self.change_data_address[0]] = self.change_data_new

    def get_data(self, get_data_tag, get_data_address):
        self.get_data_tag = str(get_data_tag)
        self.get_data_address = str(get_data_address).split("/")

        self.get_data_current = self.objects_data[self.get_data_tag]["data"][self.get_data_address[0]]

        if type(self.get_data_current) == list:
            return self.objects_data[self.get_data_tag]["data"][self.get_data_address[0]][int(self.get_data_address[1])]
        if type(self.get_data_current) == dict:
            return self.objects_data[self.get_data_tag]["data"][self.get_data_address[0]][str(self.get_data_address[1])]
        else:
            return self.objects_data[self.get_data_tag]["data"][self.get_data_address[0]]
    
    def get_collide(self, get_collide_tag):
        self.get_collide_tag = str(get_collide_tag)
        self.get_collide_d = False
        self.get_collide_list = []

        self.get_collide_list.extend(self.objects_blocks)

        for object in self.objects_data:
            self.get_collide_list.append(self.objects_data[object]["box"])
        
        for block in self.get_collide_list:
            if self.objects_data[self.get_collide_tag]["box"].collide(block):
                self.get_collide_d = True
                break
        
        return self.get_collide_d

    def get_other(self, get_other_tags=False):
        self.get_other_d = False
        self.get_other_tags = bool(get_other_tags)

        self.get_other_tag_list = None
        
        for object_1 in self.objects_data:
            for object_2 in self.objects_data:
                if object_1 != object_2 and self.objects_data[object_1]["box"].collide(self.objects_data[object_2]["box"]):    
                    self.get_other_d = True
                    self.get_other_tag_list = (object_1, object_2)

                    break
            
            if self.get_other_d:
                break
        
        if self.get_other_tags:
            return self.get_other_d, self.get_other_tag_list
        else:
            return self.get_other_d
    
    def get_block(self, get_block_box=False):
        self.get_block_d = False
        
        self.get_block_box = bool(get_block_box)        
        self.get_block_boxs = None

        for object in self.objects_data:
            for a in range(len(self.objects_blocks)):
                if self.objects_data[object]["box"].collide(self.objects_blocks[a]):
                    self.get_block_d = True
                    self.get_block_boxs = (object, a)

                    break
            
            if self.get_block_d:
                break
        
        if self.get_block_box:
            return self.get_block_d, self.get_block_boxs
        else:
            return self.get_block_d
        
    def fix_other(self, fix_other_tag_1, fix_other_tag_2):
        self.fix_other_tag_1 = str(fix_other_tag_1)
        self.fix_other_tag_2 = str(fix_other_tag_2)

        if self.objects_data[self.fix_other_tag_1]["box"].collide(self.objects_data[self.fix_other_tag_2]["box"]):
            self.fix_other_diff = [abs(self.objects_data[self.fix_other_tag_1]["box"].loc()[0] - self.objects_data[self.fix_other_tag_2]["box"].loc()[0]), abs(self.objects_data[self.fix_other_tag_1]["box"].loc()[1] - self.objects_data[self.fix_other_tag_2]["box"].loc()[1])]
            self.fix_other_raw = (abs(self.objects_data[self.fix_other_tag_1]["box"].loc()[0] - self.objects_data[self.fix_other_tag_2]["box"].loc()[0]), abs(self.objects_data[self.fix_other_tag_1]["box"].loc()[1] - self.objects_data[self.fix_other_tag_2]["box"].loc()[1]))

            for a in range(2):
                self.fix_other_diff[a] -= self.objects_data[self.fix_other_tag_1]["box"].size[a] / 2
                self.fix_other_diff[a] -= self.objects_data[self.fix_other_tag_2]["box"].size[a] / 2

                self.fix_other_diff[a] = abs(self.fix_other_diff[a]) / 2 + self.object_inaccuracy

            if self.fix_other_raw[0] > self.fix_other_raw[1]:
                if self.objects_data[self.fix_other_tag_1]["box"].loc()[0] > self.objects_data[self.fix_other_tag_2]["box"].loc()[0]:
                    self.objects_data[self.fix_other_tag_1]["box"].xy[0] += self.fix_other_diff[0]
                    self.objects_data[self.fix_other_tag_2]["box"].xy[0] -= self.fix_other_diff[0]
                else:
                    self.objects_data[self.fix_other_tag_1]["box"].xy[0] -= self.fix_other_diff[0]
                    self.objects_data[self.fix_other_tag_2]["box"].xy[0] += self.fix_other_diff[0]
                
                self.objects_data[self.fix_other_tag_1]["velocity"][0] = ((self.objects_data[self.fix_other_tag_1]["velocity"][0] * (self.objects_data[self.fix_other_tag_1]["box"].weight / self.objects_data[self.fix_other_tag_2]["box"].weight)) + (self.objects_data[self.fix_other_tag_2]["velocity"][0] * (self.objects_data[self.fix_other_tag_2]["box"].weight / self.objects_data[self.fix_other_tag_1]["box"].weight))) / 2
                self.objects_data[self.fix_other_tag_2]["velocity"][0] = self.objects_data[self.fix_other_tag_1]["velocity"][0]
            else:
                if self.objects_data[self.fix_other_tag_1]["box"].loc()[1] > self.objects_data[self.fix_other_tag_2]["box"].loc()[1]:
                    self.objects_data[self.fix_other_tag_1]["box"].xy[1] += self.fix_other_diff[1]
                    self.objects_data[self.fix_other_tag_2]["box"].xy[1] -= self.fix_other_diff[1]
                else:
                    self.objects_data[self.fix_other_tag_1]["box"].xy[1] -= self.fix_other_diff[1]
                    self.objects_data[self.fix_other_tag_2]["box"].xy[1] += self.fix_other_diff[1]

                self.objects_data[self.fix_other_tag_1]["velocity"][1] = ((self.objects_data[self.fix_other_tag_1]["velocity"][1] * (self.objects_data[self.fix_other_tag_1]["box"].weight / self.objects_data[self.fix_other_tag_2]["box"].weight)) + (self.objects_data[self.fix_other_tag_2]["velocity"][1] * (self.objects_data[self.fix_other_tag_2]["box"].weight / self.objects_data[self.fix_other_tag_1]["box"].weight))) / 2
                self.objects_data[self.fix_other_tag_2]["velocity"][1] = self.objects_data[self.fix_other_tag_1]["velocity"][1]

    def fix_block(self, fix_block_tag, fix_block_id):
        self.fix_block_tag = str(fix_block_tag)
        self.fix_block_id = int(fix_block_id)

        if self.objects_data[self.fix_block_tag]["box"].collide(self.objects_blocks[self.fix_block_id], (0, 0, 0, 0)):
            self.fix_block_diff = [abs(self.objects_data[self.fix_block_tag]["box"].loc()[0] - self.objects_blocks[self.fix_block_id].loc()[0]), abs(self.objects_data[self.fix_block_tag]["box"].loc()[1] - self.objects_blocks[self.fix_block_id].loc()[1])]
            self.fix_block_raw = [abs(self.objects_data[self.fix_block_tag]["box"].loc()[0] - self.objects_blocks[self.fix_block_id].loc()[0]), abs(self.objects_data[self.fix_block_tag]["box"].loc()[1] - self.objects_blocks[self.fix_block_id].loc()[1])]

            for a in range(2):
                self.fix_block_diff[a] -= self.objects_data[self.fix_block_tag]["box"].size[a] / 2
                self.fix_block_diff[a] -= self.objects_blocks[self.fix_block_id].size[a] / 2

                self.fix_block_diff[a] = abs(self.fix_block_diff[a]) + self.object_inaccuracy
            
            if self.fix_block_raw[0] > self.fix_block_raw[1]:
                if self.objects_data[self.fix_block_tag]["box"].loc()[0] > self.objects_blocks[self.fix_block_id].loc()[0]:
                   self.objects_data[self.fix_block_tag]["box"].xy[0] += self.fix_block_diff[0]
                else:
                   self.objects_data[self.fix_block_tag]["box"].xy[0] -= self.fix_block_diff[0]
                
                self.objects_data[self.fix_block_tag]["box"].xy[0] = round(self.objects_data[self.fix_block_tag]["box"].xy[0])
            else:
                if self.objects_data[self.fix_block_tag]["box"].loc()[1] > self.objects_blocks[self.fix_block_id].loc()[1]:
                   self.objects_data[self.fix_block_tag]["box"].xy[1] += self.fix_block_diff[1]
                else:
                   self.objects_data[self.fix_block_tag]["box"].xy[1] -= self.fix_block_diff[1]

                self.objects_data[self.fix_block_tag]["box"].xy[1] = round(self.objects_data[self.fix_block_tag]["box"].xy[1])

    def move(self, move_delta):
        self.move_delta = float(move_delta)

        for object in self.objects_data:
            self.move_velocity = (self.objects_data[object]["velocity"][0] * self.move_delta, self.objects_data[object]["velocity"][1] * self.move_delta)
            self.move_loop = [abs(round(self.move_velocity[0])), abs(round(self.move_velocity[1]))]

            if self.move_loop[0] == 0:
                self.move_loop[0] = 1
            if self.move_loop[1] == 0:
                self.move_loop[1] = 1
            
            self.move_bit = (self.move_velocity[0] / self.move_loop[0], self.move_velocity[1] / self.move_loop[1])

            for x in range(self.move_loop[0]):
                self.objects_data[object]["box"].xy[0] += self.move_bit[0]

                if self.get_collide(object):
                    break

            for y in range(self.move_loop[1]):
                self.objects_data[object]["box"].xy[1] += self.move_bit[1]

                if self.get_collide(object):
                    break
            
            self.objects_data[object]["velocity"] = [0, 0]            

    def fix(self):        
        while self.get_block() or self.get_other():
            if self.get_block():
                self.fix_all_block = self.get_block(True)[1]
                self.fix_block(self.fix_all_block[0], self.fix_all_block[1])
            else:
                self.fix_all_other = self.get_other(True)[1]
                self.fix_other(self.fix_all_other[0], self.fix_all_other[1])
                    
    def draw(self):
        for object in self.objects_data:
            self.objects_data[object]["box"].draw(self.objects_camera.camera_data["use"])
    
    def update(self, update_delta):
        self.update_delta = float(update_delta)
        self.object_inaccuracy = self.update_delta * 10

        self.fix()
        self.move(self.update_delta)
        self.draw()