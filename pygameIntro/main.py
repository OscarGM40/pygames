import pygame, sys

# lo primero siempre será llamar a pygame.init como primera instrucción
pygame.init()
# para crear una ventana se usa pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 400))
# doy un title a la ventana con pygame.display.set_caption(string)
pygame.display.set_caption("Runner")
# para fijar el framerrate máximo necesito instanciar la clase Clock
clock = pygame.time.Clock()

# SUPERFICES: creo una regular surface con pygame.Surface((width, height))
# test_surface = pygame.Surface((100,200))
# test_surface.fill(pygame.Color('Red')) # fill pinta una superficie con un color

# IMAGENES: para importar una imagen se usa pygame.image.load(ruta):
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600,300))
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()

# RECTANGLES: se crean con pygame.Rect((left,top,width,height))
player_rect = player_surf.get_rect(midbottom = (80,300)) 

# TEXTOS: hay que crear una fuente con la clase pygame.font.Font(family,size as Integer)
# text_font = pygame.font.Font(None,50) # None será la fuente por defecto
text_font = pygame.font.Font('font/Pixeltype.ttf',50) # pero puedo meter una ruta de una fuente

text_surface = text_font.render("Hola",False,'Black')

# sin embargo falta mantener el script indefinidamente
while True:
  #por si sóla no sabe cerrarse la ventana,hay que capturar el evento QUIT
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  screen.blit(sky_surface,(0,0))
  screen.blit(ground_surface,(0,300))
  screen.blit(text_surface,(300,50))
  screen.blit(snail_surf,snail_rect)
  screen.blit(player_surf,player_rect)
  snail_rect.x -= 3
  if snail_rect.right <= 0: snail_rect.left = 800
  
  # en este bucle hay que llamar a display.update para que actualice todo
  pygame.display.update()
  clock.tick(60) # con la instancia de Clock fijo el framerrate máximo,y este bucle while True se ejecutará máximo 60 veces por segundo



