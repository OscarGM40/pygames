import pygame

class Level():
  def __init__(self):
    # SUPERFICES: creo una regular surface con pygame.Surface((width, height))
    # test_surface = pygame.Surface((100,200))
    # fill pinta una superficie con un color
    # test_surface.fill(pygame.Color('Red')) 
    self.create_map()
    self.create_player()
    self.create_enemy()
    self.create_UI()
    self.player_gravity = 0
    self.player_is_jumping = False

  def create_map(self):
    # IMAGENES: para importar una imagen se usa pygame.image.load(ruta):
    self.sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
    self.ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
    
  def create_player(self):
    self.player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
    self.player_rect = self.player_surf.get_rect(midbottom = (80,300)) 
    
  def create_enemy(self):
    self.snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
    self.snail_rect = self.snail_surf.get_rect(bottomright = (600,300))
    
  def create_UI(self):
    # TEXTOS: hay que crear una fuente con la clase pygame.font.Font(family,size as Integer)
    # text_font = pygame.font.Font(None,50) # None será la fuente por defecto
    # también puedo meter una ruta de una fuente
    self.text_font = pygame.font.Font('font/Pixeltype.ttf',50) 
    self.lives_font = pygame.font.Font('font/Pixeltype.ttf',40) 
    self.lives_surf = self.lives_font.render("Lives:",False,pygame.Color('Black'))
    self.lives_rect = self.lives_surf.get_rect(topleft = (10,10))
    self.score_surf = self.text_font.render("Score",False,(64,64,64))
    self.score_rect = self.score_surf.get_rect(center = (400,50))

    