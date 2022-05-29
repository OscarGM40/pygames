from attr import has
import pygame
from settings import *

class UI:
  def __init__(self):
    # general
    self.display_surface = pygame.display.get_surface()
    self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE) # font,size
    # bar setup Pygame.Rect(left,right,width,height)
    self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
    self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
    
    # convert weapon dictionary
    self.weapon_graphics = []
    for weapon in weapon_data.values():
      path = weapon['graphic']
      # para cargar una imagen en pygame con pygame.image.load(path) y convertir para que no sea invisible 
      weapon = pygame.image.load(path).convert_alpha()
      self.weapon_graphics.append(weapon)

    # convert magic dictionary
    self.magic_graphics = []
    for magic in magic_data.values():
      path = magic['graphic']
      magic = pygame.image.load(path).convert_alpha()
      self.magic_graphics.append(magic)


  def show_bar(self,current,max_amount,bg_rect,color):
    # pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
    pygame.draw.rect(self.display_surface,[120,120,120],bg_rect)
    # helper to convert any stat to pixel
    ratio = current / max_amount # i.e => 100 / 200 = 0.5
    current_width = ratio * bg_rect.width # i.e => 0.5 * 200 = 100
    current_rect = bg_rect.copy()
    current_rect.width = current_width #copio el rect pero modifico el width
    # draw the bar(draw.rect(surface where paint,color,figure,border?))
    pygame.draw.rect(self.display_surface,color,current_rect)
    pygame.draw.rect(self.display_surface,[160,160,160],bg_rect,2)
    pygame.draw.rect(self.display_surface,[50,50,50],current_rect,3)

  def show_exp(self,exp):
    # pintar texto con self.font.render(que ya almacenó una referencia a una fuente)ARgs: texto,Antialiasing(bool),color 
    text_surf = self.font.render("Exp: "+str(int(exp)),False,[220,220,220])
    # en display_surface.get_size():[] están las dimensions de la surface
    x = self.display_surface.get_size()[0] - 20
    y = self.display_surface.get_size()[1] - 20
    # get-rect tiene acceso a keywords como top,right,bottomright,midright,..
    text_rect = text_surf.get_rect(bottomright = (x,y))
    pygame.draw.rect(self.display_surface,[50,50,50],text_rect.inflate(10,10))
    # blit recibio un texto y una superfice,en ese orden
    self.display_surface.blit(text_surf,text_rect)

  # cajas para mostrar el ataque actual
  def selection_box(self,left,top,has_switched):
    # para crear un rect es con pygame.Rect(l,r,w,h)
    bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
    pygame.draw.rect(self.display_surface,[60,60,60],bg_rect)
    if has_switched:
      pygame.draw.rect(self.display_surface,[200,200,0],bg_rect,3)
    else:
      pygame.draw.rect(self.display_surface,[0,0,0],bg_rect,3)
    return bg_rect

  # método para pintar el sprite del arma actual
  def weapon_overlay(self,weapon_index,has_switched):
    bg_rect = self.selection_box(10,630,has_switched) # weapon
    weapon_surf = self.weapon_graphics[weapon_index]
    weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
    # ahora blit montó una imagen sobre un rect(parece que es para fusionar)
    self.display_surface.blit(weapon_surf,weapon_rect)
  
  def magic_overlay(self,magic_index,has_switched):
    bg_rect = self.selection_box(85,635,has_switched)  
    magic_surf = self.magic_graphics[magic_index]
    magic_rect = magic_surf.get_rect(center = bg_rect.center)
    self.display_surface.blit(magic_surf,magic_rect)

  def display(self,player):
    # draw.rect(surface,color,rect)
    self.show_bar(player.health,player.stats['health'],self.health_bar_rect,[255,0,0])
    self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,[0,0,255])
    self.show_exp(player.exp)
    # para invertir en Python no es con !boolean sino con la palabra not(not isLoading sería como !isLoading)
    self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
    self.magic_overlay(player.magic_index,not player.can_switch_magic) # magic