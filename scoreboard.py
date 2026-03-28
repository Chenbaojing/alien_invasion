import pygame.font
from pygame.sprite import Sprite, Group

from ship import Ship

class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0, 150)
        self.font = pygame.font.Font(None, 48)
        
        # 加载货币图像
        try:
            self.money_image = pygame.image.load('money.png').convert_alpha()
            # 缩放货币图像到合适大小
            self.money_image = pygame.transform.scale(self.money_image, (30, 30))
        except:
            self.money_image = None
        
        # 得分动画效果
        self.score_animation = 0
        self.score_animation_duration = 30
        self.score_animation_active = False
        
        # 关卡完成动画
        self.level_up_animation = 0
        self.level_up_animation_duration = 60
        self.level_up_animation_active = False
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()
        self.prep_currency()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
        self.score_shadow = self.font.render(score_str, True, self.shadow_color)
        self.score_shadow_rect = self.score_shadow.get_rect()
        self.score_shadow_rect.center = (self.score_rect.centerx + 2, self.score_rect.centery + 2)

    def show_score(self):
        # 绘制得分
        if self.score_animation_active:
            # 得分动画效果
            scale = 1 + (self.score_animation / self.score_animation_duration) * 0.3
            scaled_score = pygame.transform.scale(self.score_image, 
                (int(self.score_image.get_width() * scale), 
                 int(self.score_image.get_height() * scale)))
            scaled_rect = scaled_score.get_rect(center=self.score_rect.center)
            self.screen.blit(self.score_shadow, self.score_shadow_rect)
            self.screen.blit(scaled_score, scaled_rect)
            self.score_animation += 1
            if self.score_animation >= self.score_animation_duration:
                self.score_animation_active = False
                self.score_animation = 0
        else:
            self.screen.blit(self.score_shadow, self.score_shadow_rect)
            self.screen.blit(self.score_image, self.score_rect)
        
        # 绘制最高分
        self.screen.blit(self.high_score_shadow, self.high_score_shadow_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        # 绘制关卡
        if self.level_up_animation_active:
            # 关卡升级动画效果
            scale = 1 + (self.level_up_animation / self.level_up_animation_duration) * 0.5
            scaled_level = pygame.transform.scale(self.level_image, 
                (int(self.level_image.get_width() * scale), 
                 int(self.level_image.get_height() * scale)))
            scaled_rect = scaled_level.get_rect(center=self.level_rect.center)
            # 颜色渐变效果
            alpha = 255 - int((self.level_up_animation / self.level_up_animation_duration) * 100)
            temp_surface = scaled_level.copy()
            temp_surface.set_alpha(alpha)
            self.screen.blit(self.level_shadow, self.level_shadow_rect)
            self.screen.blit(temp_surface, scaled_rect)
            self.level_up_animation += 1
            if self.level_up_animation >= self.level_up_animation_duration:
                self.level_up_animation_active = False
                self.level_up_animation = 0
        else:
            self.screen.blit(self.level_shadow, self.level_shadow_rect)
            self.screen.blit(self.level_image, self.level_rect)
        
        # 绘制货币阴影和文本
        self.screen.blit(self.currency_shadow, self.currency_shadow_rect)
        if self.money_image:
            self.screen.blit(self.money_image, self.money_rect)
        self.screen.blit(self.currency_image, self.currency_rect)
        
        # 只在游戏活动状态时绘制飞船
        if self.ai_game.game_active:
            self.ships.draw(self.screen)
    
    def start_score_animation(self):
        """开始得分动画"""
        self.score_animation_active = True
        self.score_animation = 0
    
    def start_level_up_animation(self):
        """开始关卡升级动画"""
        self.level_up_animation_active = True
        self.level_up_animation = 0

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
        self.high_score_shadow = self.font.render(high_score_str, True, self.shadow_color)
        self.high_score_shadow_rect = self.high_score_shadow.get_rect()
        self.high_score_shadow_rect.center = (self.high_score_rect.centerx + 2, self.high_score_rect.centery + 2)
    
    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        # 先保存当前的最高分
        current_high_score = self.stats.high_score
        # 更新最高分
        self.stats.update_high_score()
        # 如果最高分发生了变化，重新渲染
        if self.stats.high_score > current_high_score:
            self.prep_high_score()
    
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
        self.level_shadow = self.font.render(level_str, True, self.shadow_color)
        self.level_shadow_rect = self.level_shadow.get_rect()
        self.level_shadow_rect.center = (self.level_rect.centerx + 2, self.level_rect.centery + 2)
        
    def prep_ship(self):
        """显示还剩下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.update_skin()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
    def prep_currency(self):
        """准备游戏货币显示"""
        # 渲染货币数量文本
        currency_str = str(self.stats.currency)
        self.currency_image = self.font.render(currency_str, True, (255, 215, 0))
        
        # 设置货币文本位置
        self.currency_rect = self.currency_image.get_rect()
        self.currency_rect.right = self.score_rect.right
        self.currency_rect.top = self.level_rect.bottom + 10
        
        # 渲染货币阴影
        self.currency_shadow = self.font.render(currency_str, True, self.shadow_color)
        self.currency_shadow_rect = self.currency_shadow.get_rect()
        self.currency_shadow_rect.center = (self.currency_rect.centerx + 2, self.currency_rect.centery + 2)
        
        # 设置货币图像位置（在文本左侧）
        if self.money_image:
            self.money_rect = self.money_image.get_rect()
            self.money_rect.right = self.currency_rect.left - 5
            self.money_rect.centery = self.currency_rect.centery
