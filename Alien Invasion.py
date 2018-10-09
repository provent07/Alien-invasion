import sys
import pygame
from settings import settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats

def run_game():
    pygame.init()
    ai_settings=settings()
    pygame.mouse.set_visible(0)

    screen=pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings, screen)
    alien=Alien(ai_settings,screen)
    bullets=Group()
    secondaries=Group()
    aliens=Group()
    bombs=Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
    stats=GameStats(ai_settings)
    ai_settings.soundin.play()

    while True:
        gf.check_events(ai_settings,screen,ship,bullets,secondaries,bombs)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets,secondaries,bombs)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs)
            screen.blit(ai_settings.background, [0, 0])
            gf.update_screen(ai_settings,screen,ship,bullets,secondaries,aliens,bombs)


run_game()