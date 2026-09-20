import time 
class GameState:
    def __init__(self):
        self.era = 1

        self.player_x = 0
        self.player_y = 0

        self.player_vx = 0
        self.player_vy = 0

        self.copter_unlocked = False
        self.copter_active = False
        self.copter_fuel = 0
        self.time_machine_unlocked = False
        self.rewinding = False
        self.challenge = {}
        self.timestamp = 0

    def update_from_game(self,current_era,player,gadgets,challenges=None):
        self.era = current_era
        self.player_x = round(player.position.x)
        self.player_y = round(player.position.y)
        self.player_vx = round(player.velocity.x)
        self.player_vy = round(player.velocity.y)
        self.copter_unlocked = (gadgets.has_copter)
        self.copter_fuel =(gadgets.copter_fuel)
        self.copter_active = (gadgets.copter_active)
        self.time_machine_unlocked = gadgets.has_time_machine 
        self.rewinding= gadgets.rewinding
        if challenges is not None :
            self.challenge = challenges.get_state()
            self.timestamp = time.time()

    def to_dict(self):
        return{
            "era": self.era,
            "player":{
                "x": self.player_x,
                "y": self.player_y,
                "vx": self.player_vx,
                "vy": self.player_vy},

            "gadgets": {
                "copter_unlocked":(self.copter_unlocked),
                "time_machine_unlocked":self.time_machine_unlocked,
                "copter_active": (self.copter_active),
                "copter_fuel":(self.copter_fuel),
                "rewinding":(self.rewinding),
                } ,
                "challenge": self.challenge,
                "timestamp":self.timestamp
        }