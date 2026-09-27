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
from hud import HUD
from menu import Menu
from pause_screen import PauseScreen
from completion_screen import CompletionScreen
from game_modes import GameMode
from how_to_play import HowToPlay
from settings_screen import SettingsScreen
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

      self.game_mode = GameMode.MENU
      self.hud = HUD(SCREEN_WIDTH)
      self.menu = Menu()
      self.how_to_play = HowToPlay()
      self.pause_screen = PauseScreen()
      self.completion_screen = CompletionScreen()
      self.settings_screen = SettingsScreen()
      #sprites
      self.all_sprites=pygame.sprite.Group()
      self.all_sprites.add(self.player)

 def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.game_mode == GameMode.MENU:
                    clicked = self.menu.handle_click(event.pos)
                    if clicked =="START GAME":
                        continue
                    elif clicked == "HOW TO PLAY":
                        self.game_mode = GameMode.HOW_TO_PLAY
                        self.how_to_play.draw(self.screen)
                    elif clicked == "SETTINGS":
                        self.game_mode = GameMode.SETTINGS
                        continue
                    
        
        if event.type != pygame.KEYDOWN:
            continue
        if self.game_mode == GameMode.MENU:
            if event.key ==pygame.K_RETURN:
                self.game_mode = (GameMode.PLAYING)
            elif event.key == pygame.K_h:
                self.game_mode = GameMode.HOW_TO_PLAY
        elif self.game_mode == GameMode.PLAYING:        
            if event.key == pygame.K_ESCAPE:
                self.game_mode = (GameMode.PAUSED)
            elif event.key in (pygame.K_SPACE,pygame.K_w,pygame.K_UP):
                self.player.jump()
            elif event.key == pygame.K_c:
                self.gadgets.activate_copter()
            elif event.key == pygame.K_t:
                self.gadgets.start_rewind()
            #playing
        elif self.game_mode == GameMode.PAUSED:
                if event.key == pygame.K_ESCAPE:
                    self.game_mode = (GameMode.PLAYING)
        elif self.game_mode == GameMode.HOW_TO_PLAY:
            if event.key == pygame.K_ESCAPE:
                self.game_mode = GameMode.COMPLETED
            #comleted
        elif self.game_mode == GameMode.COMPLETED:
            if event.key == pygame.K_RETURN:
                self.game_mode = (GameMode.MENU)


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
 
    if self.game_mode != GameMode.PLAYING:
        return
    self.player.update(self.level.platforms)
    self.camera.update(self.player)
    self.gadgets.update()
    self.challenges.update(self.player)
    if self.level.exit_desk is not None:
        if pygame.sprite.collide_rect(self.player,self.level.exit_desk):
            self.next_era()
    for blueprint in self.level.blueprints:
        if pygame.sprite.collide_rect(self.player,blueprint):
            self.gadgets.has_copter = True
    if self.level.trial_start is not None:
        if pygame.sprite.collide_rect(self.player,self.level.trial_start):
            self.challenges.start_trial()
    if self.player.rect.right> self.level.width:
        self.player.rect.right = self.level.width
        self.player.position.x = self.player.rect.x
    if self.player.rect.left<0:
        self.player.rect.left = 0
        self.player.position.x = self.player.rect.x
 
 def send_network_state(self,dt):
 #update shared status
    self.game_state.update_from_game(self.current_era,self.player,self.gadgets,self.challenges)
     #send JSON TO BROWSER
    self.communication.broadcast_state(self.game_state.to_dict())      
 def next_era(self):
    #already at final era
    if self.current_era >= 3:
       self.game_mode = GameMode.COMPLETED
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
    if self.game_mode == GameMode.MENU:
        self.menu.draw(self.screen)
    elif self.game_mode == GameMode.HOW_TO_PLAY:
        self.how_to_play.draw(self.screen)

    elif self.game_mode == GameMode.PLAYING:

        self.draw_background()
        self.level.draw(self.screen,self.camera)
        player_rect = (self.camera.apply(self.player.rect))
        self.screen.blit(self.player.image,player_rect)
        self.hud.draw(self.screen,self.current_era,self.gadgets,self.challenges)
    elif self.game_mode == GameMode.PAUSED:
        self.draw_background()
        self.level.draw(self.screen,self.camera)
        player_rect = self.camera.apply(self.player.rect)
        self.screen.blit(self.player.image,player_rect)
        self.pause_screen.draw(self.screen)
    elif self.game_mode == GameMode.COMPLETED:
        self.completion_screen.draw(self.screen)

    pygame.display.flip()

 def run(self):
    while self.running:
        dt= self.clock.tick(FPS)/1000.0
        self.handle_events()
        self.process_web_commands()
        self.update()
        self.send_network_state(dt)
        self.draw()
        if self.communication:
            self.communication.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
   game = Game()
   game.run()       

