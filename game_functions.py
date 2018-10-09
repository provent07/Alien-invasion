import sys
import pygame
from bullet import Bullet
from bullet import Secondary
from bullet import Bomb
from alien import Alien
from time import sleep


def check_keydown_events(event,ship,ai_settings,screen,bullets,secondaries,bombs):
    if event.key==pygame.K_d:
        ship.moving_right=True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        ai_settings.shot.play()
        fire_bullet(ai_settings,screen,ship,bullets,secondaries)
    elif event.key == pygame.K_b:
        ai_settings.bomb.play()
        fire_bomb(ai_settings,screen,ship,bombs)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key==pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_s:
        ship.moving_down = False

def check_events(ai_settings,screen,ship,bullets,secondaries,bombs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ship,ai_settings,screen,bullets,secondaries,bombs)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,bullets,secondaries,aliens,bombs):
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for secondary in secondaries.sprites():
        secondary.draw_bullet()
    for bomb in bombs.sprites():
        bomb.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets,secondaries,bombs):
    bullets.update()
    secondaries.update()
    bombs.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for secondary in secondaries.copy():
        if secondary.rect.bottom <= 0:
            secondaries.remove(secondary)
    for bomb in bombs.copy():
        if bomb.rect.bottom <= 0:
            bombs.remove(bomb)
    check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,secondaries,bombs)

def fire_bullet(ai_settings,screen,ship,bullets,secondaries):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    if len(secondaries) < ai_settings.bullets_allowed:
        new_secondary = Secondary(ai_settings, screen, ship)
        bullets.add(new_secondary)

def fire_bomb(ai_settings,screen,ship,bombs):
    if len(bombs) < ai_settings.bombs_allowed:
        new_bomb =Bomb(ai_settings, screen, ship)
        bombs.add(new_bomb)

def create_fleet(ai_settings, screen,ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(4*alien_height)-ship_height)
    number_rows=int(available_space_y/(4*alien_height))
    return number_rows

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, secondaries,bombs)
    if pygame.sprite.spritecollideany(ship,aliens):
        print("ARRRRRGGGGGHHHHH!!!!!!")
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y +=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,secondaries,bombs):
    pygame.sprite.groupcollide(bullets,aliens,True,True)
    pygame.sprite.groupcollide(secondaries,aliens,True,True)
    pygame.sprite.groupcollide(bombs,aliens,False,True)
    if len(aliens)==0:
        bullets.empty()
        secondaries.empty()

        create_fleet(ai_settings,screen,ship,aliens)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs):
    if stats.ship_left>1:
        stats.ship_left-=1
        aliens.empty()
        bullets.empty()
        secondaries.empty()
        bombs.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(1)
    else:
        stats.game_active=False

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,secondaries,bombs)
            break







