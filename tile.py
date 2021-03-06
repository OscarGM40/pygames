import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
  def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
    #le paso los groups al padre
    super().__init__(groups)
    # self.image = pygame.image.load('./zelda-graphics/5 - level graphics/graphics/test/rock.png').convert_alpha()
    self.sprite_type = sprite_type
    self.image = surface
    if sprite_type == 'object':
      #do an offset
      self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE))
    else:
      self.rect = self.image.get_rect(topleft = pos)
      # inflate(x,y) toma un rectangulo y cambia su size segun sus args
    self.hitbox = self.rect.inflate(0,-10) 

