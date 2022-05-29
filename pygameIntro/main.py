import pygame, sys

# lo primero siempre será llamar a pygame.init como primera instrucción
pygame.init()
# doy un title a la ventana con pygame.display.set_caption(string)
pygame.display.set_caption("Runner")
# para fijar el framerrate máximo necesito instanciar la clase Clock
clock = pygame.time.Clock()

# para crear una ventana se usa pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 600))
# sin embargo falta mantener el script indefinidamente
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  # en este bucle hay que llamar a display.update para que actualice todo
  pygame.display.update()
  clock.tick(60) # con la instancia de Clock fijo el framerrate máximo



