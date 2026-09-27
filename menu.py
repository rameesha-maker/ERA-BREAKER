import pygame
from settings import (SCREEN_WIDTH,SCREEN_HEIGHT)


class Menu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial",64,bold = True)
        self.button_font = pygame.font.SysFont("arial",30)
        self.buttons = [
            ("START GAME",pygame.Rect(SCREEN_WIDTH//2-150,250,300,60)),
            ("HOW TO PLAY",pygame.Rect(SCREEN_WIDTH//2-150,330,300,60)),
            ("SETTINGS",pygame.Rect(SCREEN_WIDTH//2-150,410,300,60))
        ]
        
    def draw(self,screen):
        screen.fill((15,20,45))
        title = self.title_font.render("ERA BREAKER",True,(255,255,255))
        title_rect = title.get_rect(center = (SCREEN_WIDTH//2,140))
        screen.blit(title,title_rect)
        for text,rect in self.buttons:
            pygame.draw.rect(screen,(35,100,180),rect,border_radius=10)
            label = self.button_font.render(text,True,(255,255,255))
            label_rect = label.get_rect(center = rect.center)
            screen.blit(label,label_rect)
    
    def handle_click(self,position):
        for text , rect in self.buttons:
            if rect.collidepoint(position):
                return text
                '''if text == "START GAME":
                 return "start"
                if text == "HOW TO PLAY":
                    return "how_to_play"
                if text == "SETTINGS":
                    return "settings"'''
        return None        
       
       
       
       