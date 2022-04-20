from csv import reader
from os import walk #walk lets you to go through file system
import pygame
import re

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

#print(import_csv_layout("../map/map_FloorBlocks.csv"))

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in sorted(img_files, key=natural_keys):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf,(128,128))
            surface_list.append(image_surf)

    return surface_list


