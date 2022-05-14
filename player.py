import pygame
from settings import *

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,groups,obstacle_sprites):
    #le paso los groups al padre
    super().__init__(groups)
    self.image = pygame.image.load('./zelda-graphics/5 - level graphics/graphics/test/player.png').convert_alpha()
    self.rect = self.image.get_rect(topleft= pos)
    self.hitbox = self.rect.inflate(0,-26)
    # Vector2 da el movimiento.por defecto será x=0 e y=0,puede moverse en x=1 o sea a la derecha o en x=-1 a la izquierda y ademas con cierta speed(x=5 será una velocidad de 5)
    self.direction = pygame.math.Vector2()
    self.speed = 5
    self.obstacle_sprites = obstacle_sprites
    
    
  def input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      self.direction.y = -1
    elif keys[pygame.K_DOWN]:
      self.direction.y = 1
    else:
      self.direction.y = 0
    
    if keys[pygame.K_LEFT]:
      self.direction.x = -1
    elif keys[pygame.K_RIGHT]:
      self.direction.x = 1
    else:
      self.direction.x = 0

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
  
  def update(self):
    self.input()
    self.move(self.speed)
    