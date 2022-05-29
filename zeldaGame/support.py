from csv import reader
from os import walk # walk me permite recorrer un directorio y sus subdirectorios(caminar por el file system,de ahi su nombre)
import pygame

def import_csv_layout(path):
  terrain_map = []
  with open(path) as level_map:
    layout = reader(level_map,delimiter = ',')
    for row in layout:
      terrain_map.append(list(row))
  return terrain_map

def import_folder(path): 
  surface_list = []
  for _,__,files in walk(path):
    for file in files:
      full_path = path + '/' + file
      image_surf = pygame.image.load(full_path).convert_alpha()
      surface_list.append(image_surf) 
  return surface_list


    