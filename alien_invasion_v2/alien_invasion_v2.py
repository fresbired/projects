"""屏幕使用"""

import pygame

from settings import Settings
from game_stats import GameStats
from roles.ship import Ship
from roles.bullet import Bullet
from roles.button import Button
from roles.scoreboard import ScoreBoard
from pygame.sprite import Group

import game_functions as gf

def run_game():
    
    # 生成游戏初始设置
    ai_settings = Settings()
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 每秒帧数限制
    clock = pygame.time.Clock()
    
    """生成屏幕"""
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption(ai_settings.screen_caption)
    
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    ships_sign = Group()
    play_button = Button(screen, ai_settings, 'play')
    scb = ScoreBoard(screen, ai_settings, stats)
    
    gf.create_fleet(ai_settings, screen, aliens)
    gf.create_signs(ai_settings, screen, ships_sign)
    
    """监听输入事件，变更屏幕"""
    while True:
        
        gf.check_events(ai_settings, screen, ship, bullets, play_button,ships_sign, scb, stats)
        
        if stats.game_active:
            # 变更数据
            ship.update()
            gf.update_bullets(ai_settings, screen,  bullets, aliens, scb, stats)        
            gf.update_aliens(ai_settings, screen, ship, bullets, aliens, ships_sign, stats)
        
        # 重绘屏幕
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, scb, ships_sign, stats)
          
        # 限制每秒帧数
        clock.tick(ai_settings.screen_frame)

run_game()