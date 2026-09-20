from collections import deque
import pygame
from settings import *

class GadgetManager:
  def __init__(self,player):
    self.player = player

        #inventory flags
    self.has_copter = False
    self.has_time_machine = False

        #bamboo copter
    self.copter_active = False
    self.max_copter_fuel = (GADGET_FUEL_FRAMES)
    self.copter_fuel = (self.max_copter_fuel)

        #time machine
    self.history = deque(maxlen = HISTORY_FRAMES)
    self.rewinding = False
    self.rewind_index = -1


  def update(self):
    if self.rewinding:
      self.update_rewind()
      return
    
    self.record_history()
    if self.copter_active:
      self.update_copter()

  def record_history(self):
      state= {
        "x": self.player.position.x,
        "y": self.player.position.y,
        "vx": self.player.velocity.x,
        "vy": self.player.velocity.y,
        "on_ground": self.player.on_ground

      }
      self.history.append(state)
  

  def activate_copter(self):
    if not self.has_copter:
      return False
    if self.copter_fuel <= 0:
      return False
    self.copter_active = True
    return True
  def deactivate_copter(self): 
    self.copter_active= False
    
  def update_copter(self):
  
    if self.copter_fuel <= 0:
      self.copter_fuel = 0
      self.copter_active = False
      return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
      self.player.velocity.y = -6
    else:
      self.player.velocity.y = 2
    self.player.position.y += (self.player.velocity.y)
    self.player.rect.y = round(self.player.position.y)
    self.copter_fuel -= 1
    if self.copter_fuel <= 0:
      self.copter_fuel = 0
      self.copter_active = False
  
    #TIME MACHINE...................
  
  def start_rewind(self):
    if not self.has_time_machine:
      return False 
    if len(self.history)<2:
        return False
    self.rewinding = True
    self.rewind_index = (len(self.history)-1)
    self.player.velocity.x = 0
    self.player.velocity.y = 0
    return True
  
  
  def stop_rewind(self):
    self.rewinding = False
    self.rewind_index = -1
  

  def update_rewind(self):
    if not self.history:
      self.stop_rewind()
      return
    if self.rewind_index< 0 :
      self.stop_rewind()
      return
    state = self.history[self.rewind_index]
    self.player.position.x = state["x"]
    self.player.position.y = state["y"]
    self.player.rect.x = round(self.player.position.x)
    self.player.rect.y = round(self.player.position.y)
    self.player.velocity.x = state["vx"]
    self.player.velocity.y = state["vy"]
    self.player.on_ground = state["on_ground"]
    self.rewind_index -=1
    if self.rewind_index < 0:
      self.stop_rewind()

  def unlock_all(self):
    self.has_copter = True
    self.has_time_machine = True
  def reset_copter_fuel(self):
    self.copter_fuel = self.max_copter_fuel
  def get_state(self):
    return{
      "has_copter":self.has_copter,
      "has_time_machine": self.has_time_machine,
      "copter_actice":self.copter_active,
      "copter_fuel":self.copter_fuel,
      "rewinding":self.rewinding,
      "history_size": len(self.history)
    }


  
    



