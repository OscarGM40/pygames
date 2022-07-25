import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:
  def __init__(self):
    # general setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Zelda 1.0.0')
    self.clock = pygame.time.Clock()
    self.level = Level()
    # sound
    main_sound = pygame.mixer.Sound('./zelda-graphics/15 - fixes audio/audio/main.ogg')
    main_sound.set_volume(0.5)
    main_sound.play(loops = -1)    

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: # cierra el juego con la X
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE: # cierra con el ESCAPE
            pygame.quit()
            sys.exit()
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m: # entra al menu con la m
              self.level.toggle_menu()
      self.screen.fill(WATER_COLOR)
      # llamo al Level.run
      self.level.run()
      pygame.display.update()
      self.clock.tick(FPS) # vino de settings.py y es 60

# si el name del file es main.py, se ejecuta el programa.No quiero otro punto de arranque
if __name__ == '__main__':
  game = Game()
  game.run()