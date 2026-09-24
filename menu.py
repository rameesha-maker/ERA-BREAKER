import pygame
from game_modes import GameMode

class Menu:
    def __init__(self,width,height):
        self.width = width 
        self.height = height
        self.title_font = pygame.fontFont(None,72)
        self.subtitle_font = pygame.font.Font(None,32)
        self.small_font = pygame.font.Font(None,24)
    def draw_text(self,screen,text,font,y):
        surface = font.render(text,True,(255,255,255))
        rect = surface.get_rect(center = (self.width//2,y))
        screen.blit(surface,rect)
    def draw(self,screen):
        screen.fill((12,18,40))
        self.draw_text(screen,"ERA BREAKER",self.title_font,180)
        self.draw_text(screen,"A journey through time",self.subtitle_font,260)
        self.draw_text(screen,"PRESS ENTER TO START",self.subtitle_font,360)
        self.draw_text(screen,"WASD / ARROWS = Move",self.small_font,430)
        self.draw_text(screen,"SPACE = JUMP    T = TIME MACHINE",self.small_font,465)
        pygame.display.flip()