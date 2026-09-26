import pygame
from settings import (SCREEN_WIDTH,SCREEN_HEIGHT)
class CompletionScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("times new roman",60,bold = True)
        self.font = pygame.font.SysFont("times new roman",28)
    def draw(self,screen):
        screen.fill((15,25,56))
        title = self.title_font.render("ERA BREAKER Complete!",True,(255,215,70))
        title_rect = title.get_rect(center = (SCREEN_WIDTH//2,220))
        screen.blit(title,title_rect)
        text = self.font.render("You succcessfully surpassed time. ",True,(255,255,255))
        text_rect = text.get_rect(center = (SCREEN_WIDTH//2,310))
        screen.blit(text,text_rect)
        instruction = self.font.render("Press ENTER to return to menu",True,(200,200,200))
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2,400))
        screen.blit(instruction,instruction_rect)
        pygame.display.flip()