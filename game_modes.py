from enum import Enum

class GameMode(Enum):
    MENU ="menu" 
    PLAYING = "playing" 
    PAUSED = "paused" 
    COMPLETED = "completed" 
    HOW_TO_PLAY ="how_to_play" 
    SETTINGS ="settings" 