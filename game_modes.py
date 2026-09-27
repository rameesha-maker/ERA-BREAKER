from enum import Enum

class GameMode(Enum):
    MENU ="menu" or 1
    PLAYING = "playing" or 2
    PAUSED = "paused" or 3
    COMPLETED = "completed" or 4
    HOW_TO_PLAY ="how_to_play" or 5
    SETTINGS ="settings" or 6