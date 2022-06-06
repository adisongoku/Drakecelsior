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


DIALOGUE1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse aliquam sodales odio, et scelerisque mi ullamcorper sed. Ut non nulla congue, malesuada felis a, suscipit est. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis sed eros hendrerit nisl iaculis semper. Duis lacinia urna augue, nec elementum felis tincidunt id. Aliquam ut consequat enim. Vestibulum vel aliquam orci. Aenean euismod nisl vitae orci rhoncus efficitur. Phasellus gravida felis lectus, eu varius libero rutrum vitae. Phasellus tristique ante sed fermentum lacinia. Curabitur ullamcorper libero eget arcu feugiat, quis facilisis augue dapibus. Donec ut molestie neque. Praesent tempor, metus vel varius maximus, turpis nibh mollis nisi, sit amet varius odio augue ut odio. Fusce mauris magna, aliquam elementum iaculis ut, fringilla vel elit. Nunc egestas lacus nunc, id placerat massa ornare eget"

            




