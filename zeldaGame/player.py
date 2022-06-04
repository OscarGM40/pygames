import pygame
from entity import Entity
from settings import *
from support import import_folder

class Player(Entity):
  def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
    #le paso los groups al padre
    super().__init__(groups)
    self.image = pygame.image.load('./zelda-graphics/5 - level graphics/graphics/test/player.png').convert_alpha()
    self.rect = self.image.get_rect(topleft= pos)
    self.hitbox = self.rect.inflate(0,-26)
    
    # graphics initial setup
    self.import_player_assets()
    self.status = 'down'

    # Movement: Vector2 da el movimiento.por defecto será x=0 e y=0,puede moverse en x=1 o sea a la derecha o en x=-1 a la izquierda y ademas con cierta speed(x=5 será una velocidad de 5)
    # self.direction = pygame.math.Vector2() viene del padre Entity
    self.attacking = False
    self.attack_cooldown = 400
    self.attack_time = None
    self.obstacle_sprites = obstacle_sprites

    #weapon setup
    self.create_attack = create_attack # funcion que crea el ataque,la recibe por args y la asigna a la propiedad self.create_attack
    self.destroy_attack = destroy_attack # funcion que destruye el ataque
    self.weapon_index = 0 # selector de arma
    self.weapon = list(weapon_data.keys())[self.weapon_index]
    self.can_switch_weapon = True
    self.weapon_switch_time = None
    self.switch_duration_cooldown = 200

    # magic setup
    self.create_magic = create_magic # funcion que recibo en el __init__
    self.magic_index = 0
    self.magic = list(magic_data.keys())[self.magic_index]
    self.can_switch_magic = True
    self.magic_switch_time = None

    #stats
    self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 6}
    self.health = self.stats['health']
    self.energy = self.stats['energy']
    self.exp = 123
    self.speed = self.stats['speed']
    
  def import_player_assets(self):
    character_path = './zelda-graphics/1 - level/graphics/player/'
    self.animations = {
      'up':[],'down':[],'left':[],'right':[],
      'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
      'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]
      }
    for animation in self.animations.keys():
      full_path = character_path + animation
      self.animations[animation] = import_folder(full_path)
      
      
  def input(self):
    if not self.attacking:
      # movement input
      keys = pygame.key.get_pressed() # capturo las teclas y switcheo por las constantes
      if keys[pygame.K_UP]:
        self.direction.y = -1
        self.status = 'up'
      elif keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = 'down'
      else:
        self.direction.y = 0
      
      if keys[pygame.K_LEFT]:
        self.direction.x = -1
        self.status = 'left'
      elif keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = 'right'
      else:
        self.direction.x = 0
        
      # attack input
      if keys[pygame.K_SPACE]:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks() # este get_ticks solo se llama una vez
        self.create_attack()

      # magic input
      if keys[pygame.K_LCTRL]:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks() 
        style = self.magic
        strength = magic_data[style]['strength'] + self.stats['magic']
        cost = magic_data[style]['cost']
        self.create_magic(style,strength,cost)

      # change weapons
      if keys[pygame.K_q] and self.can_switch_weapon:
        self.can_switch_weapon = False
        self.weapon_switch_time = pygame.time.get_ticks() # unique
        self.weapon_index += 1
        if self.weapon_index > len(list(weapon_data.keys())) -  1:
          self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        
      # change magic (fijate que a and le pasa lo mismo que a not)
      if keys[pygame.K_e] and self.can_switch_magic:
        self.can_switch_magic = False
        self.magic_switch_time = pygame.time.get_ticks()
        self.magic_index += 1
        if self.magic_index > len(list(magic_data.keys())) -  1:
          self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
      
  def get_status(self):
   # idle status <- de donde venia antes de pararse?
    if self.direction.x == 0 and self.direction.y == 0:
      if not 'idle' in self.status and not 'attack' in self.status:
        self.status = self.status + '_idle'
  # attack status    
    if self.attacking:
      self.direction.x = 0
      self.direction.y = 0
      if not 'attack' in self.status:
        if 'idle' in self.status:
          self.status = self.status.replace('_idle','')
        else:
          self.status = self.status + '_attack'
    else:
      if 'attack' in self.status:
        self.status = self.status.replace('_attack','')
  
  def cooldowns(self):
    current_time = pygame.time.get_ticks() # este se llama multiples veces
    if self.attacking:
      if current_time - self.attack_time >= self.attack_cooldown:
        self.attacking = False
        self.destroy_attack()
        self.attack_time = None
    if not self.can_switch_weapon:
      if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
        self.can_switch_weapon = True
        self.weapon_switch_time = None
    if not self.can_switch_magic:
      if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
        self.can_switch_magic = True
        self.magic_switch_time = None
        
  def animate(self):
    animation = self.animations[self.status] # esto me da una lista o array
    # loop over the frame indexes
    self.frame_index += self.animation_speed
    if self.frame_index >= len(animation): # volver a empezar la animation
      self.frame_index = 0
    #set the image
    self.image = animation[int(self.frame_index)]
    self.rect = self.image.get_rect(center = self.hitbox.center) # hay que actualizar el cento por la diferencia de tamaño de las images
  
  def update(self):
    self.input()
    self.cooldowns()
    self.get_status()
    self.animate()
    self.move(self.speed)
    