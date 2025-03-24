from pygame.sprite import Sprite

class Role(Sprite):
    
    def __init__(self, screen, ai_settings):
        
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        self.content = None
        self.rect = None
        self.screen_rect = self.screen.get_rect()
    
    def pre_content(self):
        pass      
    
    def blitme(self):
        pass
    
    def update(self):
        pass