import pygame
from settings import(TRIAL_TIME_FRAMES)
class ChallengeManager:
    def __init__(self,player,level,gadgets):
        self.player = player
        self.level = level
        self.gadgets = gadgets
        self.blueprints_collected = 0
        self.trial_active = False
        self.trial_complete = False
        self.trial_failed = False
        self.current_checkpoint = 0
        self.trial_timer = 0
        self.total_checkpoints = (len(self.level.trial_checkpoints))
    def update(self):
        self.check_blueprints()
        self.update_trial()
    def check_blueprints(self):
        collected = pygame.sprite.spritecollide(self.player,self.level.blueprints,True)
        for blueprint in collected:
            self.blueprints_collected += 1
            self.unlock_era_gadget()
    def unlock_era_gadget(self):
        era = self.level.current_era
        if era == 1:
            self.gadgets.has_copter = True
        elif era == 2 :
            self.gadgets.has_copter = True
        elif era == 3 :
            self.gadgets.has_copter = True
        self.gadgets.has_time_machine = True
    def update_trial(self):
        if not self.trial_active:
            if self.level.trial_start:
                if pygame.sprite.collide_rect(self.player,self.level.trial_start):
                    self.start_trial()
                    return
        self.trial_timer -= 1
        if self.trial_timer <=0:
            self.fail_trial()
            return
        if (self.current_checkpoint>= self.total_checkpoints):
            self.comnplete_trial()
            return
        checkpoint = (self.level.trial_checkpoints[self.current_checkpoint])
        if pygame.sprite.collide_rect(self.player,checkpoint):
            self.current_checkpoint += 1
            if (self.current_checkpoint>= self.total_checkpoints):
                self.complete_trial()
    def start_trial(self):
        self.trial_active = True
        self.trial_complete = False
        self.trial_failed = False
        self.current_checkpoint = 0
        self.trial_timer = (TRIAL_TIME_FRAMES)
    def complete_trial(self):
        self.trial_active = False
        self.trial_complete = True
        self.trial_failed = False
        self.trial_timer = 0
        #reward: restore bamboo copter fuel
        self.gadgets.reset_copter_fuel()
    def fail_trial(self):
        self.trial_active = False
        self.trial_complete = False
        self.trial_failed = True
        self.current_checkpoint = 0
        self.trial_timer = 0
    def reset_for_new_level(self,level):
        self.level = level
        self.trial_active = False
        self.trial_complete = False
        self.trial_failed = False
        self.current_checkpoint = 0
        self.trial_timer = 0
        self.total_checkpoints = len(self.level.trial_checkpoints)
    def get_state(self):
        seconds_left = (self.trial_timer/60)
        return{
            "blueprints_collected":self.blueprints_collected,
            "trial_active":self.trial_active,
            "trial_complete":self.trial_complete,
            "trial_failed": self.trial_failed,
            "checkpoint":self.current_checkpoint,
            "total_checkpoints":self.total_checkpoints,
            "trial_time_left":round(max(0,seconds_left),1)
        }


