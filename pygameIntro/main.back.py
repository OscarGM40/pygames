import pygame, sys

# lo primero siempre será llamar a pygame.init como primera instrucción
pygame.init()
# para crear una ventana se usa pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 400))
# doy un title a la ventana con pygame.display.set_caption(string)
pygame.display.set_caption("Runner")
# para fijar el framerrate máximo necesito instanciar la clase Clock
clock = pygame.time.Clock()
game_active = True

# SUPERFICES: creo una regular surface con pygame.Surface((width, height))
# test_surface = pygame.Surface((100,200))
# test_surface.fill(pygame.Color('Red')) # fill pinta una superficie con un color

# IMAGENES: para importar una imagen se usa pygame.image.load(ruta):
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# RECTANGLES: se crean con pygame.Rect((left,top,width,height))
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600,300))
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()

player_rect = player_surf.get_rect(midbottom = (80,300)) 
player_gravity = 0
player_is_jumping = False

# TEXTOS: hay que crear una fuente con la clase pygame.font.Font(family,size as Integer)
# text_font = pygame.font.Font(None,50) # None será la fuente por defecto
text_font = pygame.font.Font('font/Pixeltype.ttf',50) # pero puedo meter una ruta de una fuente
lives_font = pygame.font.Font('font/Pixeltype.ttf',40) 
lives_surf = lives_font.render("Lives:",False,pygame.Color('Black'))
lives_rect = lives_surf.get_rect(topleft = (10,10))

score_surf = text_font.render("Score",False,(64,64,64))
score_rect = score_surf.get_rect(center = (400,50))

# sin embargo falta mantener el script indefinidamente
while True:
  #por si sóla no sabe cerrarse la ventana,hay que capturar el evento QUIT
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if game_active:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if player_rect.collidepoint(event.pos): 
          if not player_is_jumping:
            player_is_jumping = True
            player_gravity = -20
      # if event.type == pygame.KEYDOWN:
      #   if event.key == pygame.K_ESCAPE: print("jump")
    else:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.key == pygame.K_SPACE:
          game_active = True
          player_is_jumping = False
          player_gravity = 0
          player_rect.bottom = 300
          snail_rect.right = 800
  if game_active:
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen,'#c0e8ec',score_rect)
    pygame.draw.rect(screen,'#c0e8ec',score_rect,6)
    # pygame.draw.line(screen,'Pink',(0,0),(800,400),6)
    pygame.draw.ellipse(screen,(255,222,89),pygame.Rect(50,60,70,70))
    screen.blit(score_surf,score_rect)
    screen.blit(lives_surf,lives_rect)

    screen.blit(snail_surf,snail_rect)
    snail_rect.x -= 3
    if snail_rect.right <= 0: snail_rect.left = 800

    player_gravity += 1
    player_rect.bottom += player_gravity
    if player_rect.bottom >= 300:
      player_is_jumping = False
      player_rect.bottom = 300
    screen.blit(player_surf,player_rect)

    # si toca el snail se acaba el juego
    if player_rect.colliderect(snail_rect):
      game_active = False
  
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #   print(pygame.mouse.get_pressed())
    # pygame.key.get_pressed() devuelve un array de 0 y 1 con todas las teclas
    keys = pygame.key.get_pressed() # lo mejor es usarlo como un diccionario
    if not player_is_jumping:
      if keys[pygame.K_SPACE]: # tengo una constante definida para cada tecla
        player_is_jumping = True
        player_gravity = -20
    # en este bucle hay que llamar a display.update para que actualice todo
  else:
    screen.fill('yellow')
  pygame.display.update()
  clock.tick(60) # con la instancia de Clock fijo el framerrate máximo,y este bucle while True se ejecutará máximo 60 veces por segundo



