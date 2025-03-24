import pygame

from roles.role import Role

class Alien(Role):
    
    def __init__(self, screen, ai_settings):
        
        super().__init__(screen, ai_settings)
        
        self.content = pygame.image.load(ai_settings.alien_img)
        self.rect = self.content.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
                
    def blitme(self):
        self.screen.blit(self.content, self.rect)
        
    def update(self):
        self.rect.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
               
    def speedup(self):
        self.ai_settings.alien_speed += 1 
        
    def check_edges(self):
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0 
    
    def check_bottom(self):
        return self.rect.bottom >= self.screen_rect.bottom
    
