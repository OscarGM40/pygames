import pygame

class Entity(pygame.sprite.Sprite):
  def __init__(self,groups):
    super().__init__(groups)
    self.frame_index = 0
    self.animation_speed = 0.15
    self.direction = pygame.math.Vector2()
    
  def move(self,speed):
    #si se mueve en diagonal hay que normalizar speed.Fijate que magnitude() y normalize() vienen de la libreria
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