import pygame

from roles.role import Role

class Ship(Role):
    
    def __init__(self, screen, ai_settings):
        
        super().__init__(screen, ai_settings)
        
        self.content = pygame.image.load(ai_settings.ship_img)
        self.rect = self.content.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        '''飞艇移动设置'''
        # 方向记录
        self.moving_right = False
        self.moving_left = False
        # 步长浮点精细化控制
        self.centerx = float(self.rect.centerx)
        
    def blitme(self):
        self.screen.blit(self.content, self.rect)
        
    def update(self):
        # 向左移动
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed
        # 向右移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed
        
        self.rect.centerx = self.centerx
    
    def center(self):
        self.rect.centerx = self.screen_rect.centerx