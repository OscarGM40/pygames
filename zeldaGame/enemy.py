import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
  def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
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
    self.damage_player = damage_player
    self.trigger_death_particles = trigger_death_particles   
    self.add_exp = add_exp
    # invincibility timer(for attacks)
    self.vulnerable = True
    self.hit_time = None
    self.invincibility_duration = 300

    # sounds
    self.death_sound = pygame.mixer.Sound('./zelda-graphics/15 - fixes audio/audio/death.wav')
    self.hit_sound = pygame.mixer.Sound('./zelda-graphics/15 - fixes audio/audio/hit.wav')
    self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
    self.death_sound.set_volume(0.2)
    self.hit_sound.set_volume(0.2)
    self.attack_sound.set_volume(0.3)
  
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
      self.damage_player(self.attack_damage,self.attack_type)
      self.attack_sound.play()
    elif self.status == 'move':
      self.direction = self.get_player_distance_direction(player)[1]
    else:
      self.direction = pygame.math.Vector2(0,0)
      
  def cooldowns(self):
    current_time = pygame.time.get_ticks() 
    if not self.can_attack:
      if current_time - self.attack_time >= self.attack_cooldown:
        self.can_attack = True
        self.attack_time = pygame.time.get_ticks() 
        self.attack_time = None

    if not self.vulnerable:
      if current_time - self.hit_time >= self.invincibility_duration:
        self.vulnerable = True

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
    if not self.vulnerable:
      #flicker
      alpha = self.wave_value()
      self.image.set_alpha(alpha)
    else:
      self.image.set_alpha(255) # opacity a 1
    
  def get_damage(self,player,attack_type):
    if self.vulnerable:
      self.hit_sound.play()
      self.direction = self.get_player_distance_direction(player)[1] 
      if attack_type == 'weapon':
        self.health -= player.get_full_weapon_damage()
      else: # magic damage
        self.health -= player.get_full_magic_damage() 
      self.hit_time = pygame.time.get_ticks()
      self.vulnerable = False
  
  def check_death(self):
    if self.health <= 0:
      self.kill()
      self.trigger_death_particles(self.rect.center,self.monster_name)
      self.add_exp(self.exp)
      self.death_sound.play()
      
  def hit_reaction(self):  
    if not self.vulnerable:
      self.direction *= -self.resistance

    # update es de la libreria,no es un custom method.Aqui va todo lo
    # que quiera chequear cada frame(move,animate,etc) ya que se llama cada clock tick o frame.Creo que todo se llama cada frame
  def update(self): 
    self.hit_reaction()
    self.move(self.speed)
    self.animate()
    self.cooldowns()
    self.check_death()
    
  def enemy_update(self,player):
    self.get_status(player)
    self.actions(player)       