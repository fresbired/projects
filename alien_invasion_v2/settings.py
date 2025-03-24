class Settings():
    """存储《外星人入侵》的所有设置"""
    
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.screen_caption = "Alien Invasion"
        self.screen_frame = 380
        
        # 飞船设置
        self.ship_img = './images/ship.bmp'
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15 
        self.bullet_color = ( 60, 60, 60 )
        self.bullet_speed = 1 
        self.bullets_allowed = 4 
        
        # 外星人设置
        self.alien_img = './images/alien.bmp'
        self.alien_speed = 1
        self.alien_speedup_factor = 1
        self.alien_width = 81
        self.alien_height = 81
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，为-1表示向左移 
        self.fleet_direction = 1
        
        # play按钮设置
        self.button_width, self.button_height = 200, 50 
        self.button_color = (0, 255, 0) 
        self.button_text_color = (255, 255, 255)
        
        # 计分板文本设置
        self.text_color = (0, 0 , 0)

        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self): 
     
        # 记分 
        self.alien_points = 50 