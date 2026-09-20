import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        #CREATING PLAYER(A SOLID RECTANGULAR BOX)
        self.image=pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        self.image.fill(DORAEMON_BLUE)

        #DEFINING ITS PHYSICAL POSITION
        self.rect=self.image.get_rect(topleft=(x,y))

        self.position = pygame.math.Vector2(x,y)
        self.velocity = pygame.math.Vector2(0,0)

        self.speed=PLAYER_SPEED
        self.on_ground = False

        self.copter_active = False
        self.rewinding = False

    
    def handle_input(self): 
        self.velocity.x = 0
        
        #CHECK KEYS CURRENTLY HELD DOWN
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        #jumping(only if on ground)
    def jump(self):
        if self.on_ground:
            self.velocity.y= JUMP_FORCE

            self.on_ground = False

    def apply_gravity(self):
        #continually pulls the player down
        self.velocity.y += GRAVITY
        if self.velocity.y  > TERMINAL_VELOCITY:
            self.velocity.y = TERMINAL_VELOCITY

    def apply_copter_physics(self):
        keys=pygame.key.get_pressed()

        #small amount of downward force
        self.velocity.y += COPTER_GRAVITY
         #holding W/UP produces lift
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity.y += COPTER_UP_FORCE
        if self.velocity.y<COPTER_MAX_UP_SPEED:
            self.velocity.y = (COPTER_MAX_UP_SPEED)
        if self.velocity.y> COPTER_MAX_DOWN_SPEED:
            self.velocity.y = (COPTER_MAX_DOWN_SPEED)



    def move_horizontal(self,platforms):
        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)

        # CHECK IF HITTING LEFT OR RIGHT SIDE OF PLATFORM
        collisions = pygame.sprite.spritecollide(self,platforms,False)
        for tile in collisions:
            if self.velocity.x>0 : #moving right
                self.rect.right = tile.rect.left
                self.position.x = self.rect.x
            elif self.velocity.x<0: #moving left
                self.rect.left = tile.rect.right
                self.position.x =self.rect.x

    def move_vertical(self,platforms):
        self.position.y += self.velocity.y
        self.rect.y = round(self.position.y)
        self.on_ground = False          
        #check if landing on top or hitting the ceiling
        collisions= pygame.sprite.spritecollide(self,platforms,False)  
        for tile in collisions:
            if self.velocity.y >0: #falling downward
                self.rect.bottom = tile.rect.top
                self.position.y =self.rect.y
                self.velocity.y =0
                self.on_ground =True

            elif self.velocity.y<0: #hitting the ceiling
                self.rect.top = tile.rect.bottom
                self.position.y = self.rect.y
                self.velocity.y =0    

    def update(self,platforms):
        if self.rewinding:
            return
        
        self.handle_input()
        if self.copter_active:
            self.apply_copter_physics()
        else:
            self.apply_gravity()
        # processing collisions one by one to avoid clipping though walls
        self.move_horizontal(platforms)
        self.move_vertical(platforms)

    def get_snapshot(self):
        return {
            "x":float(self.position.x),
            "y": float(self.position.y),
            "vx": float(self.velocity.x),
            "vy": float(self.velocity.y)
        }

    def restore_snapshot(self,snapshot):
        self.position.x = snapshot ["x"]
        self.position.y = snapshot ["y"]
        self.velocity.x = snapshot ["vx"]
        self.velocity.y = snapshot ["vy"]
        self.rect.x = round (self.position.x)
        self.rect.y = round(self.position.y)
        