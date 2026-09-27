import pygame
from settings import (SCREEN_WIDTH,SCREEN_HEIGHT)
class SettingsScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None,48)
        self.text_font = pygame.font.Font(None,28)
        self.back_button = pygame.Rect(250,450,300,60)
    def draw(self,screen):
        screen.fill((15,20,47))
        title = self.title_font.render("SETTINGS",True,(255,255,255))
        title_rect = title.get_rect(center = (SCREEN_WIDTH//2,120))
        screen.blit(title,title_rect)
        text = self.text_font.render("CONTROLS:",True,(255,255,255))
        screen.blit(text,(100,220))
        controls = self.text_font.render("Move : A/D or Arrow Keys",True,(220,220,220))
        screen.blit(controls,(120,270))
        jump = self.text_font.render("Jump: SPACE",True,(220,220,220))
        copter = self.text_font.render("Bamboo Copter: C ",True,(220,220,220))
        screen.blit(copter,(120,350))
        time_machine = self.text_font.render("Time Machine: T ",True,(220,220,220))
        screen.blit(time_machine,(120,390))
        pygame.draw.rect(screen,(35,100,180),self.back_button,border_radius = 10)
        back = self.text_font.render("BACK",True,(255,255,255))
        back_rect = back.get_rect(center = self.back_button.center)
        screen.blit(back,back_rect)
    def handle_click(self,position):
        if self.back_button.collidepoint(position):
            return "BACK"
        return None