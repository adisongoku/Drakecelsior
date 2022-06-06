from csv import reader
from os import walk #walk lets you to go through file system
import os, shutil
import pygame
import re
from glob import glob
from settings import TILESIZE

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
            if 'cat_boss' in path:
                image_surf = pygame.transform.scale(image_surf,(image_surf.get_width() * 3,image_surf.get_height() *3))
            else:
                image_surf = pygame.transform.scale(image_surf,(TILESIZE,TILESIZE))
            surface_list.append(image_surf)

    return surface_list

def clean_files():
    folder = "../saves"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


CAT_DIAL1 = "Who dares to interrupt my slumber!?"
DIALOGUE1 = "Uh, me. Hello!"
DIALOGUE2 = "My slumber got interrupted as well."
DIALOGUE3 = "Do you know maybe where could I find that band of thieves that stole my pile of gold, and left coins everywhere?"
CAT_DIAL2 = "I don't care, nor I Know!"
CAT_DIAL3 = "Now DIE!"
DIALOGUE4 = "Wait WHY!?"
CAT_DIAL4 = "Because I'm THE BOSS, those are the rules here!"




            



