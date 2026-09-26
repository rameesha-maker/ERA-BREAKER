import pygame
from settings import(SCREEN_WIDTH,SCREEN_HEIGHT)
class PauseScreen:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial",55,bold = True)
        self.font = pygame.font.SysFont("arial",28)
    def draw(self,screen):
        overlay = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        overlay.fill((0,0,0,170))
        screen.blit(overlay,(0,0))
        title=self.title_font.render("GAME PAUSED",True,(255,255,255))
        screen.blit(title,title.get_rect(center = (SCREEN_WIDTH//2,230)))
        text =self.font.render("Press ESC to continue",True,(220,220,220))
        screen.blit(text,text.get_rect(center = (SCREEN_WIDTH//2,320)))
        
        pygame.display.flip()
