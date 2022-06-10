import pygame
from random import randint

class Level():
  start_time = 0
  snail_frame_index = 0
  snail_frames = []
  fly_frame_index = 0
  fly_frames = []
  def __init__(self):
    # SUPERFICES: creo una regular surface con pygame.Surface((width, height))
    # test_surface = pygame.Surface((100,200))
    # fill pinta una superficie con un color
    # test_surface.fill(pygame.Color('Red')) 
    self.create_map()
    self.create_player()
    self.create_enemy()
    self.create_UI()
    self.display_score()
    self.player_gravity = 0
    self.player_is_jumping = False
    self.enemies_list = []
    self.enemies_surf = []
    
    self.types = []
    self.enemies = {
      'rects': self.enemies_list,
      'surfs': self.enemies_surf,
      'types': self.types
    }

  def create_map(self):
    # IMAGENES: para importar una imagen se usa pygame.image.load(ruta):
    self.sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
    self.ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
    
  def create_player(self):
    player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2]
    self.player_index = 0
    self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
    self.player_surf = self.player_walk[self.player_index]
    self.player_rect = self.player_surf.get_rect(midbottom = (80,300)) 


  
  def create_standing_player(self):
    self.player_standing_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    # self.player_standing_surf = pygame.transform.scale(self.player_standing_surf,(150,150))
    self.player_standing_surf = pygame.transform.rotozoom(self.player_standing_surf,0,2)
    self.player_standing_rect = self.player_standing_surf.get_rect(center = (400,200))
    return (self.player_standing_surf, self.player_standing_rect)
  
  def create_game_over_UI(self):
    self.text_font = pygame.font.Font('font/Pixeltype.ttf',50) 
    self.game_title_surf = self.text_font.render("Pixel Runner",False,(111,196,169))
    self.game_title_rect = self.game_title_surf.get_rect(center = (410,80))
    self.game_message = self.text_font.render("Press space to run",False,(111,196,169))
    self.game_message_rect = self.game_message.get_rect(center = (410,340))
    return(self.game_title_surf, self.game_title_rect, self.game_message, self.game_message_rect)
    
  
  def create_enemy(self):
    condition = randint(0,2)
    if condition == 0:
      self.snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
      self.snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
      self.snail_frames = [self.snail_frame_1, self.snail_frame_2]
      self.snail_frame_index = 0
      self.snail_surf = self.snail_frames[0]
      self.snail_rect = self.snail_surf.get_rect(bottomright = (randint(900,1100),300))
      self.type = "snail"
      return (self.snail_surf,self.snail_rect, self.type)
    else:
      self.fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
      self.fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
      self.fly_frames = [self.fly_frame_1, self.fly_frame_2]
      self.fly_frame_index = 0
      self.fly_surf = self.fly_frames[0]
      self.fly_rect = self.fly_surf.get_rect(bottomright = (randint(900,1100),200))
      self.type = "fly"
      return (self.fly_surf,self.fly_rect,self.type)
  
  def create_UI(self):
    # TEXTOS: hay que crear una fuente con la clase pygame.font.Font(family,size as Integer)
    # text_font = pygame.font.Font(None,50) # None será la fuente por defecto
    # también puedo meter una ruta de una fuente
    self.text_font = pygame.font.Font('font/Pixeltype.ttf',50) 
    self.lives_font = pygame.font.Font('font/Pixeltype.ttf',40) 
    self.lives_surf = self.lives_font.render("Lives:",False,pygame.Color('Black'))
    self.lives_rect = self.lives_surf.get_rect(topleft = (10,10))
    # self.score_surf = self.text_font.render("Score",False,(64,64,64))
    # self.score_rect = self.score_surf.get_rect(center = (400,50))

  def display_score(self):
    # global current_time <- forma uno de hacer una variable global
    current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
    self.score_surf = self.text_font.render(f'Score {current_time}',False,(64,64,64))    
    self.score_rect = self.score_surf.get_rect(center = (400,50))
    return current_time 
  
        