import pygame
import sys
from settings import *
from player import Player
from level import Level
from camera import Camera
from gadgets import GadgetManager
from game_state import GameState
from communication import CommunicationServer
from challenges import ChallengeManager 

class Game:
 def __init__(self):

      pygame.init()
      self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
      pygame.display.set_caption(WINDOW_TITLE)
      self.clock=pygame.time.Clock()
      self.running =True
      self.current_era = 1
      self.level=Level(self.current_era)
      self.player=Player(100,100)
      self.camera= Camera()
      self.camera.set_world_width(self.level.width)
      self.gadgets = GadgetManager(self.player)
      self.gadgets.unlock_all()
      self.challenges = ChallengeManager(self.player,self.level,self.gadgets)

      #shared game state
      self.game_state = GameState()

      #websocket
      self.communication = (CommunicationServer())
      self.communication.start()
      #sprites
      self.all_sprites=pygame.sprite.Group()
      self.all_sprites.add(self.player)

def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE,pygame.K_w,pygame.K_UP): 
                if not self.gadgets.copter_active:
                 self.player.jump()  

            elif event.key == pygame.K_c:
                self.gadgets.activate_copter()

               #time machine
            elif event.key == pygame.K_t:
                self.gadgets.start_rewind()
        elif event.type == pygame.KEYUP:
                if event.key == pygame.K_c:
                    self.gadgets.deactivate_copter()
                if event.key == pygame.K_t:
                    self.gadgets.stop_rewind()
def process_web_commands(self):
    commands = (self.communication.get_commands())
    for command in commands:
        if command == "left":
            self.player.velocity.x = (-self.player.speed)
        elif command == "right":
            self.player.velocity.x = self.player.speed
        elif command == "stop":
            self.player.velocity.x = 0
        elif command == "jump":
            self.player.jump()
        elif command == "copter":
            self.gadgets.activate_copter()
        elif command == "copter_stop":
            self.gadgets.deactivate_copter()
        elif command == "rewind":
            self.gadgets.start_rewind()
        elif command == "rewind_stop":
            self.gadgets.stop_rewind()    
def update(self):
 
    #receive commands
    self.process_web_commands()
    self.gadgets.update()
    if not self.gadgets.rewinding:
        if not self.gadgets.copter_active:
            self.player.update(self.level.platforms)
    if not self.gadgets.rewinding:
        self.challenges.update()
    self.camera.update(self.player)
        #era transition
    if self.level.exit_desk:
        if pygame.sprite.collide_rect(self.player,self.level.exit_desk):
            self.next_era()
    if self.player.rect.top > (self.level.height+200) :
           self.reset_player()
 
def send_network_state(self,dt):
 #update shared status
    self.game_state.update_from_game(self.current_era,self.player,self.gadgets,self.challenges)
     #send JSON TO BROWSER
    self.communication.broadcast_state(self.game_state.to_dict())      
def next_era(self):
    #already at final era
    if self.current_era >= 3:
       return
    #move to next era
    self.current_era +=1
    #build new level
    self.level.change_era(self.current_era)
    self.challenges.reset_for_new_level(self.level)
    self.reset_player()
    self.camera.set_world_width(self.level.width)
    self.camera.x = 0
def reset_player(self):
    self.player.position.x =100
    self.player.position.y =100
    self.player.velocity.x = 0
    self.player.velocity.y =0
    self.player.rect.topleft =(100,100)  
    self.player.on_ground = False
    self.camera.x =0
def draw_background(self):
    if self.current_era == 1:
        self.screen.fill(FEUDAL_SKY)
    elif self.current_era ==2:
        self.screen.fill(MODERN_SKY)
    elif self.current_era==3:
        self.screen.fill(FUTURE_SKY)

def draw(self):
    self.draw_background()
    self.level.draw(self.screen,self.camera)
    player_screen_rect = (self.camera.apply(self.player.rect))
    self.screen.blit(self.player.image,player_screen_rect)

    pygame.display.flip()

def run(self):
    while self.running:
        dt= self.clock.tick(FPS)/1000.0
        self.handle_events()
        self.update()
        self.send_network_state(dt)
        self.draw()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
   game = Game()
   game.run()       

