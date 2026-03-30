import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    '''初始化外星人的类'''

    def __init__(self, ai_game, is_explosive=False, alien_type='normal'):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # 外星人类型
        self.alien_type = alien_type
        self.is_explosive = is_explosive

        # 根据类型设置属性
        self._setup_alien_type()

        # 加载外星人图像并设置其rect属性
        self._load_alien_image()
        
        self.rect = self.image.get_rect()

        # 每个外星人放在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        
        # 坦克型外星人的生命值
        self.health = self.max_health
        
        # 特殊行为计时器
        self.last_action_time = pygame.time.get_ticks()
        # 不要覆盖_setup_alien_type()中设置的action_cooldown

    def _setup_alien_type(self):
        """根据外星人类型设置属性"""
        if self.alien_type == 'normal':
            self.max_health = 1
            self.speed_multiplier = 1.0
            self.color = (0, 255, 0)
            self.action_cooldown = 0
        elif self.alien_type == 'fast':
            self.max_health = 1
            self.speed_multiplier = 1.5
            self.color = (255, 255, 0)
            self.action_cooldown = 0
        elif self.alien_type == 'tank':
            self.max_health = 3
            self.speed_multiplier = 0.7
            self.color = (128, 0, 128)
            self.action_cooldown = 2000  # 坦克型外星人每2秒发射一次子弹
        elif self.alien_type == 'healer':
            self.max_health = 1
            self.speed_multiplier = 0.8
            self.color = (0, 255, 255)
            self.action_cooldown = 20000  # 治疗型外星人每20秒治疗一次
        elif self.alien_type == 'splitter':
            self.max_health = 1
            self.speed_multiplier = 1.0
            self.color = (255, 128, 0)
            self.action_cooldown = 30000  # 分裂型外星人每30秒分裂一次
        elif self.alien_type == 'stealth':
            self.max_health = 1
            self.speed_multiplier = 1.2
            self.color = (100, 100, 100)
            self.action_cooldown = 5000  # 隐形型外星人每5秒切换隐形状态
            self.is_invisible = False
        elif self.alien_type == 'teleporter':
            self.max_health = 2
            self.speed_multiplier = 0.9
            self.color = (255, 0, 255)
            self.action_cooldown = 8000  # 传送型外星人每8秒传送一次

    def _load_alien_image(self):
        """根据外星人类型加载图像"""
        # 尝试使用游戏的图像缓存
        if hasattr(self.settings, 'game') and hasattr(self.settings.game, 'image_cache'):
            cache = self.settings.game.image_cache
            if self.is_explosive:
                self.image = cache.get('alien_2', None)
            else:
                if self.alien_type == 'normal':
                    self.image = cache.get('alien', None)
                elif self.alien_type == 'fast':
                    self.image = cache.get('alien_3', None)
                elif self.alien_type == 'tank':
                    self.image = cache.get('alien_4', None)
                elif self.alien_type == 'healer':
                    self.image = cache.get('alien_5', None)
                elif self.alien_type == 'splitter':
                    self.image = cache.get('alien_6', None)
                elif self.alien_type == 'stealth':
                    self.image = cache.get('alien_7', None)
                elif self.alien_type == 'teleporter':
                    self.image = cache.get('alien_8', None)
        else:
            self.image = None
        
        # 如果缓存中没有或加载失败，使用传统方法加载
        if self.image is None:
            if self.is_explosive:
                self.image = pygame.image.load('images/alien_2.bmp')
            else:
                if self.alien_type == 'normal':
                    self.image = pygame.image.load('images/alien_2.bmp')
                elif self.alien_type == 'fast':
                    self.image = pygame.image.load('images/alien_3.bmp')
                elif self.alien_type == 'tank':
                    self.image = pygame.image.load('images/alien_4.bmp')
                elif self.alien_type == 'healer':
                    self.image = pygame.image.load('images/alien_5.bmp')
                elif self.alien_type == 'splitter':
                    self.image = pygame.image.load('images/alien_6.bmp')
                elif self.alien_type == 'stealth':
                    try:
                        self.image = pygame.image.load('images/alien_7.bmp')
                    except:
                        self.image = pygame.Surface((50, 50))
                        self.image.fill(self.color)
                        pygame.draw.circle(self.image, (200, 200, 200), (25, 25), 20, 2)
                elif self.alien_type == 'teleporter':
                    try:
                        self.image = pygame.image.load('images/alien_8.bmp')
                    except:
                        self.image = pygame.Surface((50, 50))
                        self.image.fill(self.color)
                        pygame.draw.polygon(self.image, (255, 255, 255), [(25, 5), (45, 45), (5, 45)], 2)

    def take_damage(self, damage=1):
        """受到伤害，返回是否被消灭"""
        self.health -= damage
        return self.health <= 0

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """向左或右移动外星人"""
        speed = self.settings.alien_speed * self.speed_multiplier
        self.x += speed * self.settings.fleet_direction
        self.rect.x = self.x
    
    def reset(self, ai_game, is_explosive=False, alien_type='normal'):
        """
        重置外星人状态
        
        Args:
            ai_game: 游戏实例
            is_explosive: 是否为爆炸型外星人
            alien_type: 外星人类型
        """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # 外星人类型
        self.alien_type = alien_type
        self.is_explosive = is_explosive

        # 根据类型设置属性
        self._setup_alien_type()

        # 加载外星人图像并设置其rect属性
        self._load_alien_image()
        
        self.rect = self.image.get_rect()

        # 每个外星人放在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        
        # 坦克型外星人的生命值
        self.health = self.max_health
        
        # 特殊行为计时器
        self.last_action_time = pygame.time.get_ticks()
    
    
    
    