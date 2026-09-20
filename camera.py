from settings import (SCREEN_WIDTH,CAMERA_SMOOTHING)


class Camera:
    def __init__(self):

        #camera horizonal position
        self.x =0.0
        # maximum world position
        self.world_width = SCREEN_WIDTH

    def set_world_width(self,width):
        self.world_width = max(width,SCREEN_WIDTH)    

    def update(self,player): 
        #keeping player centered
        target_x = (player.rect.centerx-SCREEN_WIDTH /2 )

        #CAMERA CANNOT GOI BEFORE BEGGINING
        target_x =max(0,target_x)

        #camera caanot go beyond level
        max_camera_x = (self.world_width - SCREEN_WIDTH)
        target_x = min(target_x,max_camera_x)

        #smooth movement
        self.x += (target_x -self.x) * CAMERA_SMOOTHING

    def apply(self,rect):
        return rect.move(-round(self.x),0)       