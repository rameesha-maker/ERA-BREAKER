import pygame
from settings import (SCREEN_WIDTH,SCREEN_HEIGHT)

class HowToPlay:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial",48,bold = True)
        self.font = pygame.font.SysFont("arial",25)
        self.instructions = [
            "ARROWS/ A D    -  Move",
            "SPACE / W      -  Jump",
            "C              -  Bamboo Copter",
            "T              -  Time Mchine",
            "ESC            -  Pause",
            "", 
            "Find Blueprints to unlock Gadgets.",
            "Complete challenges to progress.",
            "Travel through all three eras."
        ]
    def draw(self,screen):
        screen.fill((20,25,50))
        title = self.title_font.render("HOW TO PLAY",True,(255,255,255))
        screen.blit(title,title.get_rect(center = (SCREEN_WIDTH//2,90)))
        y = 170
        for line in self.instructions:
            text = self.font.render(line,True,(230,230,230))
            screen.blit(text,(100,y))
            y += 42

        back = self.font.render("Press ESC to return",True,(180,180,180))
        screen.blit(back,(100,SCREEN_HEIGHT - 60 ))