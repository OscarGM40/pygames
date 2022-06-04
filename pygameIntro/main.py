import pygame, sys
from level import Level


class Game:
  def __init__(self):
    # lo primero siempre será llamar a pygame.init como primera instrucción,para que inicialice todo
    pygame.init()
    # para crear una ventana se usa pygame.display.set_mode((width, height))
    self.screen = pygame.display.set_mode((800, 400))
    # doy un title a la ventana con pygame.display.set_caption(string)
    pygame.display.set_caption("Runner")
    # para fijar el framerrate máximo necesito instanciar la clase Clock
    self.clock = pygame.time.Clock()
    self.game_active = True
    self.level = Level()

# sin embargo falta mantener el script indefinidamente
  def run(self):
    while True:
    # por si sóla no sabe cerrarse la ventana,hay que capturar el evento QUIT
      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if self.game_active:
          if event.type == pygame.MOUSEBUTTONDOWN:
            if self.level.player_rect.collidepoint(event.pos): 
              if not self.level.player_is_jumping:
                self.level.player_is_jumping = True
                self.level.player_gravity = -20
        else:
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              pygame.quit()
              sys.exit()
            if event.key == pygame.K_SPACE:
              self.game_active = True
              self.level.player_is_jumping = False
              self.level.player_gravity = 0
              self.level.player_rect.bottom = 300
              self.level.snail_rect.right = 800
      if self.game_active:
        self.screen.blit(self.level.sky_surface,(0,0))
        self.screen.blit(self.level.ground_surface,(0,300))
        pygame.draw.rect(self.screen,'#c0e8ec',self.level.score_rect)
        pygame.draw.rect(self.screen,'#c0e8ec',self.level.score_rect,6)
        # pygame.draw.line(self.screen,'Pink',(0,0),(800,400),6)
        pygame.draw.ellipse(self.screen,(255,222,89),pygame.Rect(50,60,70,70))
        self.screen.blit(self.level.score_surf,self.level.score_rect)
        self.screen.blit(self.level.lives_surf,self.level.lives_rect)
    
        self.screen.blit(self.level.snail_surf,self.level.snail_rect)
        self.level.snail_rect.x -= 3
        if self.level.snail_rect.right <= 0: 
          self.level.snail_rect.left = 800
    
        self.level.player_gravity += 1
        self.level.player_rect.bottom += self.level.player_gravity
        if self.level.player_rect.bottom >= 300:
          self.level.player_is_jumping = False
          self.level.player_rect.bottom = 300
        self.screen.blit(self.level.player_surf,self.level.player_rect)

        # si toca el snail se acaba el juego
        if self.level.player_rect.colliderect(self.level.snail_rect):
          self.game_active = False
  
        # pygame.key.get_pressed() devuelve un array de 0 y 1 con todas las teclas
        keys = pygame.key.get_pressed() # lo mejor es usarlo como un diccionario
        if not self.level.player_is_jumping:
          if keys[pygame.K_SPACE]: # constante definida para cada tecla
            self.level.player_is_jumping = True
            self.level.player_gravity = -20
      else:
        self.screen.fill('yellow')
      # en este bucle hay que llamar a display.update para que actualice todo
      pygame.display.update()
      self.clock.tick(60) # con la instancia de Clock fijo el framerrate máximo,y este bucle while True se ejecutará máximo 60 veces por segundo

if __name__ == "__main__":
  game = Game()
  game.run()

