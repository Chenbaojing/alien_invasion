import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game, angle=0, start_pos=None):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.angle = angle
        
        # 在(0,0)处创建一个表示子弹的矩形,再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        
        # 如果指定了起始位置（狙击模式），使用该位置
        if start_pos:
            self.rect.center = start_pos
        else:
            self.rect.midtop = ai_game.ship.rect.midtop
        
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    def update(self):
        """向上移动子弹"""
        # 根据角度计算子弹的移动方向
        import math
        rad = math.radians(self.angle)
        dx = math.sin(rad) * self.settings.bullet_speed
        dy = -math.cos(rad) * self.settings.bullet_speed
        
        # 更新子弹的精确位置
        self.x += dx
        self.y += dy
        
        # 更新表示子弹位置的rect的位置
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
    
    def reset(self, ai_game, angle=0, start_pos=None):
        """
        重置子弹状态
        
        Args:
            ai_game: 游戏实例
            angle: 子弹角度
            start_pos: 起始位置
        """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.angle = angle
        
        # 重置矩形
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        
        # 设置位置
        if start_pos:
            self.rect.center = start_pos
        else:
            self.rect.midtop = ai_game.ship.rect.midtop
        
        # 重置位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)