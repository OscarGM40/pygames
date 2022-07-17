import pygame

class Weapon(pygame.sprite.Sprite):
  def __init__(self,player,groups):
    super().__init__(groups) # parece un requerimiento cuando heredan?
    self.sprite_type = 'weapon'
    direction = player.status.split('_')[0]
    
    # graphic
    full_path = f'./zelda-graphics/1 - level/graphics/weapons/{player.weapon}/{direction}.png'
    self.image = pygame.image.load(full_path).convert_alpha() # convert_alpha para que no se vea transparente

    # placement
    if direction == 'right':
      self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0,16)) # 16px relativos 
    elif direction == 'left':
      self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0,16))
    elif direction == 'up':
      self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10,0))
    elif direction == 'down':
      self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10,0))