import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,groups,obstacle_sprites):
    #le paso los groups al padre
    super().__init__(groups)
    self.image = pygame.image.load('./zelda-graphics/5 - level graphics/graphics/test/player.png').convert_alpha()
    self.rect = self.image.get_rect(topleft= pos)
    self.hitbox = self.rect.inflate(0,-26)
    
    # graphics initial setup
    self.import_player_assets()
    self.status = 'down'
    self.frame_index = 0
    self.animation_speed = 0.15

    # Movement: Vector2 da el movimiento.por defecto será x=0 e y=0,puede moverse en x=1 o sea a la derecha o en x=-1 a la izquierda y ademas con cierta speed(x=5 será una velocidad de 5)
    self.direction = pygame.math.Vector2()
    self.speed = 5
    self.attacking = False
    self.attack_cooldown = 400
    self.attack_time = None
    self.obstacle_sprites = obstacle_sprites
    
  def import_player_assets(self):
    character_path = './zelda-graphics/1 - level/graphics/player/'
    self.animations = {
      'up':[],'down':[],'left':[],'right':[],
      'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
      'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]
      }
    for animation in self.animations.keys():
      full_path = character_path +animation
      self.animations[animation] = import_folder(full_path)
      
      
  def input(self):
    if not self.attacking:
      keys = pygame.key.get_pressed() # capturo las teclas

      # movement input
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
      # magic input
      if keys[pygame.K_LCTRL]:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks() 
  
      
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
    
    
  def move(self,speed):
    #si se mueve en diagonal hay que normalizar speed
    if self.direction.magnitude() != 0:
      self.direction = self.direction.normalize()
    # no uso self.speed ya que valdrá para mover cualquier cosa
    self.hitbox.x += self.direction.x * speed
    self.collision('horizontal')
    self.hitbox.y += self.direction.y * speed
    self.collision('vertical')
    self.rect.center = self.hitbox.center
  
  def collision(self,direction):
    if direction == 'horizontal':
      for sprite in self.obstacle_sprites:
        #si colisiona con un sprite en el eje X
        if sprite.hitbox.colliderect(self.hitbox):
          # si colisiona yendo hacia la derecha
          if self.direction.x > 0: # moving right
            self.hitbox.right = sprite.hitbox.left # stop on left side of sprite
          if self.direction.x < 0: # moving left
            self.hitbox.left = sprite.hitbox.right # choca contra el right

    if direction == 'vertical':
      for sprite in self.obstacle_sprites:
        # si colisiona con un sprite en el eje Y
        if sprite.hitbox.colliderect(self.hitbox):
          if self.direction.y > 0: # moving down
            self.hitbox.bottom = sprite.hitbox.top
          if self.direction.y < 0: # moving up
            self.hitbox.top = sprite.hitbox.bottom
  
  def cooldowns(self):
    current_time = pygame.time.get_ticks() # este se llama multiples veces
    if self.attacking:
      if current_time - self.attack_time > self.attack_cooldown:
        self.attacking = False
        self.attack_time = None
    
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
    