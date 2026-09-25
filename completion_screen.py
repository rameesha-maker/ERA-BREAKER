import pygame
class CompletionScreen:
    def __init__(self,width,height):
        self.width =width
        self.height = height
        self.title_font = pygame.font.Font(None,60)
        self.font = pygame.font.Font(None,30)
    def draw(self,screen):
        screen.fill((15,25,56))
        title = self.title_font.render("TIME RESTORED!",True,(255,255,255))
        title_rect = title.get_rect(center = (self.width//2,200))
        screen.blit(title,title_rect)
        text = self.font.render("you completed ERA BREAKER. ",True,(220,220,220))
        text_rect = text.get_rect(center = (self.width//2,300))
        instruction = self.font.render("Press ENTER to return to menu",True,(220,220,220))
        instruction_rect = instruction.get_rect(center=(self.width//2,380))
        screen.blit(instruction,instruction_rect)
        pygame.display.flip()