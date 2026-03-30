import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """外星人子弹的类"""
    
    def __init__(self, ai_game, alien):
        """初始化外星人子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # 创建子弹图像
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0))
        
        # 设置子弹位置
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        
        # 存储子弹的精确位置
        self.y = float(self.rect.y)
        
        # 子弹速度
        self.speed = 3.0
    
    def update(self):
        """向下移动子弹"""
        self.y += self.speed
        self.rect.y = self.y
        
        # 如果子弹超出屏幕，删除它
        if self.rect.top > self.settings.screen_height:
            self.kill()
