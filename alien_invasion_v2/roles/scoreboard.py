import pygame.font

from roles.role import Role

class ScoreBoard(Role):
    
    def __init__(self, screen, ai_settings, stats):
        
        super().__init__(screen, ai_settings)
        
        self.stats = stats

        self.font = pygame.font.SysFont(None, 48)
        self.color = ai_settings.text_color
        self.bg_color = ai_settings.bg_color
        
        self.prep_score()
        self.prep_high_score()
        
        
    def prep_score(self):
        
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score) 
        self.score_img = self.font.render(score_str, True, self.color, self.bg_color)
        
        # 将得分放在屏幕右上角 
        self.score_rect = self.score_img.get_rect() 
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 
        
    def prep_high_score(self): 
        """将最高得分转换为渲染的图像""" 
        rounded_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(rounded_score)
        self.high_score_img = self.font.render(high_score_str, True, self.color, self.bg_color)
                    
        #将最高得分放在屏幕顶部中央 
        self.high_score_rect = self.high_score_img.get_rect() 
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top 
        
    def blitme(self):
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect) 
