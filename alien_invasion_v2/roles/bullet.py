import pygame

from roles.role import Role

class Bullet( Role ):
    
    def __init__(self, screen, ai_settings, ship):
        
        super().__init__(screen, ai_settings)
        
        self.color = ai_settings.bullet_color
        self.rect = pygame.Rect(0 , 0, ai_settings.bullet_width, ai_settings.bullet_height)
        
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top   
        
        '''子弹移动设置'''
        # 步长浮点精细化控制
        self.y = float(self.rect.y)
         
        
    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    
    def update(self):
        
        self.y -= float(self.ai_settings.bullet_speed)
        self.rect.y = self.y
        
        
        
        