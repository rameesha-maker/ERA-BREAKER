import pygame

class HUD:
    def __init__(self,screen_width):
        self.screen_width = screen_width

        self.small_font = pygame.font.Font(None,24)
        self.medium_font = pygame.font.Font(None,30)
        self.large_font = pygame.font.Font(None,42)
    def draw_panel(self,screen):
        #will draw the transparent - looking background
        panel = pygame.Surface((self.screen_width,90),pygame.SRCALPHA)
        panel.fill((10,15,30,190))
        screen.blit(panel,(0,0))
    def draw_text(self,screen,text,x,y,font = None):
        if font is None:
            font = self.small_font
        surface = font.render(str(text),True,(255,255,255))
        screen.blit(surface,(x,y))

    def draw_fuel_bar(self,screen,x,y,current,maximum,width=160,height=16):
        pygame.draw.rect(screen,(50,50,60),(x,y,width,height))
        if maximum >0:
            percentage = max(0,min(1,current/maximum))
            fuel_width = int (width*percentage)
            pygame.draw.rect(screen,(40,200,120),(x,y,fuel_width,height))
        pygame.draw.rect(screen,(220,220,220),(x,y,width,height),2)
    def draw(self,screen,era,gadgets,challenges = None):
        self.draw_panel(screen)
        self.draw_text(screen,f"ERA:{era}",20,15,self.medium_font)
        copter = getattr(gadgets,"has_copter",False)
        time_machine = getattr(gadgets,"has_time_machine",False)
        copter_active = getattr(gadgets,"copter_active",False)
        self.draw_text(screen,"Bamboo copter:"+("READY" if copter else "LOCKED"),180,10)
        self.draw_text(screen,"Tme Machine: "+("READY" if time_machine else "LOCKED",180,35))
        if copter_active:
            fuel = getattr(gadgets,"copter_fuel",0)
            max_fuel = getattr(gadgets,"max_copter_fuel",1)
            self.draw_text(screen,"COPTER FUEL",
                           430,10)
            self.draw_fuel_bar(screen,430,35,fuel,max_fuel)
        if challenges is not None:
            completed = getattr(challenges,"completed_count",0)
            total = getattr(challenges,"total_challenges",0)
            self.draw_text(screen,f"CHALLENGES:{completed}/{total}",620,15)
        self.draw_text(screen,"WASD/ARROWS = Move",20,65)
        self.draw_text(screen,"SPACE=Jump",220,65)
        self.draw_text(screen,"T = Time Machine",400,65)
        
                               
                               
                               
    
    