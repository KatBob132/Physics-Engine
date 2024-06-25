from random import *
from math import *

def si(angle):
    return sin(radians(angle))

def ci(angle):
    return cos(radians(angle))

def random_number(min, max):
    return randrange(min, max + 1)

def clamp(number, min=None, max=None):
    if min != None:
        if number < min:
            number = min
    if max != None:
        if number > max:
            number = max

    return number

def normalize_angle(angle):
    while angle > 360 or angle < 0:
        if angle > 360:
            angle -= 360
        else:
            angle += 360
    
    return angle

def get_angle(point_1, point_2):
    angle = normalize_angle(-degrees(atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])) + 90)

    return angle

def get_distance(point_1, point_2):
    distance = sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)
    
    return distance