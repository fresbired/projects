import sys

import pygame

from roles.bullet import Bullet
from roles.alien import Alien
from roles.ship import Ship

from time import sleep 

'''角色初始化'''

def create_fleet(ai_settings, screen, aliens):
    """创建一阵列外星人"""
    col_num = (ai_settings.screen_width - 2 * ai_settings.alien_width) / ai_settings.alien_width 
    row_num = ai_settings.screen_height / ( 2 * ai_settings.alien_height )
    
    for i in range(int(row_num)):
        for j in range(int(col_num)):
            
            new_alien = Alien( screen, ai_settings )
            new_alien.rect.x += j * new_alien.rect.width
            new_alien.rect.y += i * new_alien.rect.height
            aliens.add( new_alien )
    
def create_signs(ai_settings, screen, ships_sign):
    """创建飞艇剩余数目图标"""
    for i in range(ai_settings.ship_limit):
        new_sign = Ship(screen, ai_settings)
        new_sign.rect.y = 0
        new_sign.rect.x = i*new_sign.rect.width
        ships_sign.add(new_sign)
        
'''监听输入'''

def check_play_button(ai_settings, screen, play_button, mouse_x, mouse_y, ships_sign, scb, stats):
    if play_button.rect.collidepoint(mouse_x, mouse_y): 
        if stats.ships_left <= 0 : 
            stats.reset_stats()
            scb.prep_score()
            create_signs(ai_settings, screen, ships_sign)

def check_mouse_events(event, ai_settings, screen, play_button, ships_sign, scb, stats):
    if event.type == pygame.MOUSEBUTTONDOWN :
        mouse_x, mouse_y = pygame.mouse.get_pos()
        check_play_button(ai_settings, screen, play_button, mouse_x, mouse_y, ships_sign, scb, stats)


def fire_bullets(ai_settings, screen, ship, bullets):
    """填装子弹"""
    if len(bullets) < ai_settings.bullets_allowed: 
        new_bullet = Bullet(screen, ai_settings, ship) 
        bullets.add(new_bullet) 


def check_key_events(event, ai_settings, screen, ship, bullets):
    """处理按键事件"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_SPACE: 
            fire_bullets(ai_settings, screen, ship, bullets)
            
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            ship.moving_right = False


def check_quit_events(event):
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type in (pygame.TEXTEDITING, pygame.TEXTINPUT):
        if 'q' in event.text or 'Q' in event.text:
            sys.exit()



def check_events(ai_settings, screen, ship, bullets, play_button,ships_sign, scb, stats):
    """监听输入事件，安排数据变更"""
    for event in pygame.event.get():
        check_quit_events(event)
        check_key_events(event, ai_settings, screen, ship, bullets)
        if not stats.game_active:
            check_mouse_events(event, ai_settings, screen, play_button, ships_sign, scb, stats)


'''数据变更'''

def ship_hit(ai_settings, screen, ship, aliens, bullets, ships_sign, stats): 
    """响应被外星人撞到的飞船""" 
    
    '''将所剩飞船数减1'''
    # 将本局所剩飞船数减1并去除一个飞艇标志。
    stats.ships_left -= 1 
    sprites_list = ships_sign.sprites()
    if sprites_list:
        ships_sign.remove(sprites_list[-1])
    
    '''重置，开启新一轮''' 
    # 清空子弹列表，清空外星人列表并创建一群新的外星人，
    bullets.empty() 
    aliens.empty() 
    create_fleet(ai_settings, screen, aliens) 
    # 将飞船放到屏幕底端中央（初始位置）
    ship.center() 
    
    '''判定本局是否结束'''
    # # 当飞船剩余数目为零时，
    if stats.ships_left > 0:
        # 暂停
        sleep(0.5)  
    else:
        stats.game_active = False

def check_ship_crashed(ai_settings, screen, ship, bullets, aliens, ships_sign, stats):
    """检查飞船是否因外星人达到底部或撞击而毁坏""" 
    # 检测外星人是否达到底部
    for alien in aliens.sprites():
        if alien.check_bottom(): 
            # 像飞船被撞到一样进行处理 
            ship_hit(ai_settings, screen, ship, bullets, aliens, ships_sign, stats)            
            return
    # 检测外星人是否与飞艇碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, aliens, bullets, ships_sign, stats)

def update_scores(ai_settings, collisions, aliens, scb, stats):
    if collisions:
        for aliens in collisions.values(): 
            stats.score += ai_settings.alien_points * len(aliens) 
            scb.prep_score() 
    # 检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, bullets, aliens, scb, stats): 
    """响应子弹和外星人的碰撞""" 
    # 删除发生碰撞的子弹和外星人 
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    # 根据碰撞情况，更新分值
    update_scores(ai_settings, collisions, aliens, scb, stats)
    
    if len(aliens) == 0: 
    # 删除现有的所有子弹，并创建一个新的外星人群 
        bullets.empty() 
        create_fleet(ai_settings, screen, aliens)
        for alien in aliens.sprites():
                alien.speedup()


def update_bullets(ai_settings, screen, bullets, aliens, scb, stats):
    
    # 更新子弹的位置 
    bullets.update() 
    # 删除已消失的子弹 
    for bullet in bullets.copy(): 
        if bullet.rect.bottom <= 0: 
            bullets.remove(bullet) 
    # 检测是否射中外星人
    check_bullet_alien_collisions(ai_settings, screen, bullets, aliens, scb, stats)


def check_fleet_edges(ai_settings, aliens): 
    """有外星人到达边缘时采取相应的措施""" 
    for alien in aliens.copy(): 
        if alien.check_edges(): 
            # 将整群外星人下移，并改变它们的方向
            for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed 
            ai_settings.fleet_direction *= -1 
            break          
           
def update_aliens(ai_settings, screen, ship, bullets, aliens, ships_sign, stats):
    """ 
    检测外星人是否达到边缘并更新整群外星人移动模式；
    检测外星人是否撞毁飞艇。
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_ship_crashed(ai_settings, screen, ship, bullets, aliens, ships_sign, stats)
    
    

'''重绘屏幕'''
def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, scb, ships_sign, stats):
    
    pygame.mouse.set_visible(False)
    
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    for bullet in bullets.sprites():
        bullet.blitme()
    for alien in aliens.sprites():
        alien.blitme()
    for sign in ships_sign.sprites():
        sign.blitme()
    scb.blitme()
    if not stats.game_active:
        play_button.blitme()
        pygame.mouse.set_visible(True)
        
    pygame.display.flip()
