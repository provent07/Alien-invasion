import pygame,pygame.mixer
class settings():
    def __init__(self):
        self.screen_width=800
        self.screen_height=600
        self.background=pygame.image.load('space.png')
        self.ship_speed_factor=1
        self.bullet_speed_factor=3
        self.bullet_width=2
        self.bullet_height=15
        self.bullet=(255,50,100)
        self.bullets_allowed=100
        self.bomb_width=100
        self.bomb_height=20
        self.bombs_allowed=1
        self.alien_speed_factor=5
        self.fleet_drop_speed=5
        self.fleet_direction=1
        self.ship_limit=3
        self.shot = pygame.mixer.Sound("pew.wav")
        self.soundin = pygame.mixer.Sound("background.wav")
        self.bomb = pygame.mixer.Sound("bomb.wav")



