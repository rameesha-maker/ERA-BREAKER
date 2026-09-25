import pygame
class PauseScreen:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.title_font = pygame.font.Font(None,64)
        self.font = pygame.font.Font(None,30)
    def draw(self,screen):
        overlay = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        overlay.fill((0,0,0,170))
        screen.blit(overlay,(0,0))
        title=self.title_font.render("PAUSED",True,(255,255,255))
        title_rect = title.get_rect(center = (self.width//2,230))
        screen.blit(title,title_rect)
        text =self.font.render("Press ESC to continue",True,(220,220,220))
        text_rect = text.get_rect(center=(self.width//2,320))
        screen.blit(text,text_rect)
        pygame.display.flip()