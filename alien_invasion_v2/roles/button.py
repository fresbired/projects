import pygame.font

from roles.role import Role

class Button(Role):
    
    def __init__(self, screen, ai_settings, text):
        
        super().__init__(screen, ai_settings)
        
        self.font = pygame.font.SysFont(None, 48)        
        self.content = self.font.render(text, True, self.ai_settings.button_text_color, self.ai_settings.button_color)
        
        self.rect = pygame.Rect(0, 0, 
                self.ai_settings.button_width, 
                self.ai_settings.button_height) 
        self.rect.center = self.screen_rect.center
        self.rect.x += 60

    def blitme(self):
        self.screen.blit(self.content, self.rect)        