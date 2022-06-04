import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
  def __init__(self,monster_name,pos,groups,obstacle_sprites):
    # general setup
    super().__init__(groups)
    self.sprite_type = 'enemy'

    # graphics setup
    self.import_graphics(monster_name)
    self.status = 'idle'
    # ¿como puede acceder a un diccionario que se crea en un método?Investigar sobre el scope en Python
    self.image = self.animations[self.status][self.frame_index]
    self.import_graphics(monster_name)

    # movement
    self.rect = self.image.get_rect(topleft=pos)
    self.hitbox = self.rect.inflate(0,-10)
    self.obstacle_sprites = obstacle_sprites # funcion que

    # stats(leidos de settings.py)
    self.monster_name = monster_name
    monster_info = monster_data[self.monster_name]
    self.health = monster_info['health']
    self.exp = monster_info['exp']
    self.speed = monster_info['speed']
    self.attack_damage = monster_info['damage']
    self.resistance = monster_info['resistance']
    self.attack_radius = monster_info['attack_radius']
    self.notice_radius = monster_info['notice_radius']
    self.attack_type = monster_info['attack_type']

    # player interaction
    self.can_attack = True
    self.attack_time = None
    self.attack_cooldown = 400
    
  
  def import_graphics(self,name):
    self.animations = {'idle':[],'move':[],'attack': []}
    main_path = f'./zelda-graphics/10 - Enemies/graphics/monsters/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)

  def get_player_distance_direction(self,player):
    # puedo coger el vector de cada rect del juego
    enemy_vector = pygame.math.Vector2(self.rect.center)
    player_vector = pygame.math.Vector2(player.rect.center)
    
    # ojo que puedo sumar o restar vectores
    # y para sacar la distancia(hipotenusa) puedo usar magnitude() sobre un vector(si por ejemplo es [2,4] me devolverá raiz cuadrada de 20)
    distance = (player_vector - enemy_vector).magnitude() 
    # para conseguir la direction hay que normalizar el vector,siempre que tenga magnitud(fijate que pude haber usado la variable distance)
    if (player_vector - enemy_vector).magnitude() > 0:
      direction = (player_vector - enemy_vector).normalize()
    else:
      direction = pygame.math.Vector2(0,0) # sin args tamb es (0,0)
    return (distance,direction) # devuelvo una lista inmutable

  def get_status(self,player):
    distance = self.get_player_distance_direction(player)[0]
    if distance <= self.attack_radius and self.can_attack:
      if self.status != 'attack':
        self.frame_index = 0
      self.status = 'attack'
    elif distance <= self.notice_radius:
      self.status = 'move'
    else:
      self.status = 'idle'

  def actions(self, player):
    if self.status == 'attack':
      self.attack_time = pygame.time.get_ticks()
    elif self.status == 'move':
      self.direction = self.get_player_distance_direction(player)[1]
    else:
      self.direction = pygame.math.Vector2(0,0)
      
  def cooldown(self):
    if not self.can_attack:
      current_time = pygame.time.get_ticks() 
      if current_time - self.attack_time >= self.attack_cooldown:
        self.can_attack = True
        self.attack_time = pygame.time.get_ticks() 
        self.attack_time = None
  
  def animate(self):
    # frame_index es el index del sprite(4 hacen la animacion)
    self.frame_index += self.animation_speed

    animation = self.animations[self.status] 
    if self.frame_index >= len(animation): # volver a empezar la animation
      if self.status == 'attack':
        self.can_attack = False
      self.frame_index = 0
    # set the image
    self.image = animation[int(self.frame_index)]
    # hay que actualizar el centro del rect segun el centro del hitbox,ya que movemos el hitbox únicamente
    self.rect = self.image.get_rect(center = self.hitbox.center) 

    # update es de la libreria,no es un custom method.Aqui va todo lo
    # que quiera chequear cada frame(move,animate,etc) ya que se llama cada clock tick o frame.Creo que todo se llama cada frame
  def update(self): 
    self.move(self.speed)
    self.cooldown()
    self.animate()
    
  def enemy_update(self,player):
    self.get_status(player)
    self.actions(player)       