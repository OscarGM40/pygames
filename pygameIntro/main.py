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
    self.score = 0
    self.text_font = pygame.font.Font('font/Pixeltype.ttf',50) 
    # siempre hay que sumar 1 más a USERVENT por cada timer que cree 
    self.obstacle_timer = pygame.USEREVENT  + 1
    # pygame.time.set_timer(functionToExecute, milliseconds)
    pygame.time.set_timer(self.obstacle_timer, 1300)
    # más timers para animar los enemies
    self.snail_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(self.snail_animation_timer, 300)
    self.fly_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(self.fly_animation_timer, 200)

  def collisions(self,player,obstacles):
    if obstacles:
      for obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
          return False
    return True

  def player_animation(self):
    global player_surf,player_index
    # si no toca el suelo cambio el sprite
    if self.level.player_rect.bottom < 300:
      self.level.player_surf = self.level.player_jump
    else:
      self.level.player_index += 0.1
      self.level.player_surf = self.level.player_walk[int(self.level.player_index) % len(self.level.player_walk)]
    
  def create_enemies(self):
    # for enemy_rect in self.level.enemies_list:
    if(self.level.enemies):
      for enemy_rect in self.level.enemies['rects']:
        enemy_rect.x -= 5
        if enemy_rect.bottom == 300:
          self.screen.blit(self.level.snail_surf, enemy_rect)
        else:
          self.screen.blit(self.level.fly_surf, enemy_rect)
          # list comprehension(x for x in list if ...):  
      self.level.enemies_list = [enemy_rect for enemy_rect in self.level.enemies_list if enemy_rect.x > -100]
      
    return self.level.enemies_list
  
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
              self.level.start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == self.obstacle_timer and self.game_active:
          newEnemy = self.level.create_enemy()
          self.level.enemies['surfs'].append(newEnemy[0])
          self.level.enemies['rects'].append(newEnemy[1])
          self.level.enemies['types'].append(newEnemy[2])
          self.level.enemies_surf.append(newEnemy[0])
          self.level.enemies_list.append(newEnemy[1])
          self.level.types.append(newEnemy[2])
        if event.type == self.snail_animation_timer and self.game_active:
          snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
          snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
          snail_frames = [snail_frame_1, snail_frame_2]
          self.level.snail_surf = snail_frames[0]
          if self.level.snail_frame_index == 0:
            self.level.snail_frame_index = 1
          else:
            self.level.snail_frame_index = 0
          self.level.snail_surf = snail_frames[self.level.snail_frame_index]
        if event.type == self.fly_animation_timer and self.game_active:
          fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
          fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
          fly_frames = [fly_frame_1,fly_frame_2]
          self.level.fly_surf = fly_frames[0]
          if self.level.fly_frame_index == 0:
            self.level.fly_frame_index = 1
          else:
            self.level.fly_frame_index = 0
          self.level.fly_surf = fly_frames[self.level.fly_frame_index]
  
                   
          
              
      if self.game_active:
        self.screen.blit(self.level.sky_surface,(0,0))
        self.screen.blit(self.level.ground_surface,(0,300))
        pygame.draw.rect(self.screen,'#c0e8ec',self.level.score_rect)
        pygame.draw.rect(self.screen,'#c0e8ec',self.level.score_rect,6)
        # pygame.draw.line(self.screen,'Pink',(0,0),(800,400),6)
        pygame.draw.ellipse(self.screen,(255,222,89),pygame.Rect(50,60,70,70))
        self.score = self.level.display_score()
        self.level.enemies_list = self.create_enemies()
        # collisions
        self.game_active = self.collisions(self.level.player_rect,self.level.enemies_list)
        self.player_animation()
        self.screen.blit(self.level.score_surf,self.level.score_rect)
        self.screen.blit(self.level.lives_surf,self.level.lives_rect)
    
        # self.screen.blit(self.level.snail_surf,self.level.snail_rect)
    
        self.level.player_gravity += 1
        self.level.player_rect.bottom += self.level.player_gravity
        if self.level.player_rect.bottom >= 300:
          self.level.player_is_jumping = False
          self.level.player_rect.bottom = 300
        self.screen.blit(self.level.player_surf,self.level.player_rect)

        
        # si toca el snail se acaba el juego
        # if self.level.player_rect.colliderect(self.level.snail_rect):
        #   self.game_active = False
  
        # pygame.key.get_pressed() devuelve un array de 0 y 1 con todas las teclas
        keys = pygame.key.get_pressed() # lo mejor es usarlo como un diccionario
        if not self.level.player_is_jumping:
          if keys[pygame.K_SPACE]: # constante definida para cada tecla
            self.level.player_is_jumping = True
            self.level.player_gravity = -20
      else:
        self.screen.fill((94,129,162))
        self.level.enemies_list.clear() 
        self.level.player_rect.midbottom = (80,300)
        self.level.player_gravity = 0
        self.screen.blit(self.level.create_standing_player()[0], self.level.create_standing_player()[1])
        score_message = self.text_font.render(f'Your score: {self.score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        self.screen.blit(self.level.create_game_over_UI()[0], self.level.create_game_over_UI()[1])
        
        if self.score == 0:
          self.screen.blit(self.level.create_game_over_UI()[2], self.level.create_game_over_UI()[3])
        else:
          self.screen.blit(score_message, score_message_rect)

      # en este bucle hay que llamar a display.update para que actualice todo
      pygame.display.update()
      self.clock.tick(60) # con la instancia de Clock fijo el framerrate máximo,y este bucle while True se ejecutará máximo 60 veces por segundo

if __name__ == "__main__":
  game = Game()
  game.run()

