import pygame
from pygame.sprite import Sprite
import random

class Boss(Sprite):
    """Boss敌人的类"""
    
    def __init__(self, ai_game, boss_level=1):
        """初始化Boss"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        
        # Boss等级
        self.boss_level = boss_level
        
        # 根据等级设置Boss属性
        self._setup_boss_attributes()
        
        # 创建Boss图像
        self._create_boss_image()
        
        self.rect = self.image.get_rect()
        
        # Boss初始位置：屏幕顶部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = 50
        
        # 存储Boss的精确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Boss当前生命值
        self.health = self.max_health
        
        # 计时器
        self.spawn_start_time = pygame.time.get_ticks()
        self.move_start_time = pygame.time.get_ticks()
        self.last_fire_time = pygame.time.get_ticks()
        
        # Boss是否开始移动
        self.is_moving = False
        
        # 躲避子弹相关属性
        self.dodge_points = self._calculate_dodge_points()  # 计算5个躲避点
        self.last_dodge_time = pygame.time.get_ticks()
        self.dodge_cooldown = 500  # 躲避冷却时间（毫秒）
        self.attack_count = 0  # 当前位置受到的攻击次数
        self.max_attacks_before_dodge = 10  # 连续受到10次攻击后躲避
        
        # 血条属性
        self.health_bar_width = 200
        self.health_bar_height = 15
        self.health_bar_color = (255, 0, 0)
        self.health_bar_bg_color = (100, 100, 100)
    
    def _setup_boss_attributes(self):
        """根据Boss等级设置属性"""
        # 每关Boss的血量递增
        base_health = 200
        health_multiplier = 1.5
        
        self.max_health = int(base_health * (health_multiplier ** (self.boss_level - 1)))
        
        # Boss大小固定为第一关大小
        self.width = 80
        self.height = 80
        
        # Boss移动速度
        self.move_speed = 0.09 + (self.boss_level - 1) * 0.01
        
        # Boss攻击频率（毫秒）- 调整为更合理的频率
        self.fire_cooldown = max(3000 - (self.boss_level - 1) * 200, 1500)
        
        # Boss生成外星人的间隔（毫秒）
        self.spawn_cooldown = 10000
        
        # Boss子弹储备（每关递增）
        base_bullets = 200
        bullet_increment = 50
        self.bullet_reserve = base_bullets + (self.boss_level - 1) * bullet_increment
        self.max_bullet_reserve = self.bullet_reserve  # 记录初始最大值
        
        # Boss外星人储备（每关递增）
        base_aliens = 50
        alien_increment = 20
        self.alien_reserve = base_aliens + (self.boss_level - 1) * alien_increment
        self.max_alien_reserve = self.alien_reserve  # 记录初始最大值
        
        # Boss颜色
        colors = [
            (255, 0, 0),      # 第1关：红色
            (255, 128, 0),    # 第2关：橙色
            (255, 255, 0),    # 第3关：黄色
            (0, 255, 0),      # 第4关：绿色
            (0, 0, 255)       # 第5关：蓝色
        ]
        self.color = colors[min(self.boss_level - 1, len(colors) - 1)]
    
    def _calculate_dodge_points(self):
        """计算Boss水平线上的3个等距躲避点（去掉边缘的两个）"""
        screen_width = self.screen_rect.width
        boss_width = self.width
        
        # 计算5个点的x坐标，确保Boss不会超出屏幕边界
        margin = boss_width // 2 + 10  # 左右边距
        available_width = screen_width - 2 * margin
        
        points = []
        for i in range(5):
            x = margin + (available_width * i) // 4
            points.append(x)
        
        # 只返回中间的3个点，去掉边缘的两个
        return points[1:4]
    
    def _create_boss_image(self):
        """创建Boss图像"""
        try:
            self.image = pygame.image.load('images/alien_boss.bmp')
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            # 如果加载失败，使用默认图像
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)
            
            # 在Boss上绘制一些装饰
            border_color = (255, 255, 255)
            border_width = 3
            pygame.draw.rect(self.image, border_color, 
                            (0, 0, self.width, self.height), border_width)
            
            # 绘制Boss等级
            font = pygame.font.Font(None, 36)
            level_text = font.render(f"Lv.{self.boss_level}", True, (255, 255, 255))
            text_rect = level_text.get_rect()
            text_rect.center = (self.width // 2, self.height // 2)
            self.image.blit(level_text, text_rect)
    
    def update(self):
        """更新Boss状态"""
        current_time = pygame.time.get_ticks()
        
        # 检查是否开始移动（10分钟后）
        if not self.is_moving:
            if current_time - self.move_start_time >= 600000:  # 10分钟 = 600000毫秒
                self.is_moving = True
        else:
            # 向下移动
            self.y += self.move_speed
            self.rect.y = int(self.y)
    
    def draw_health_bar(self):
        """绘制Boss血条"""
        if self.health <= 0:
            return
        
        # 重新计算血条位置，确保有足够的空间
        bar_x = 10  # 与飞船图标对齐
        bar_y = 80  # 进一步降低位置，避免与上方元素重叠
        line_spacing = 30  # 进一步增加行间距
        
        # 尝试加载中文字体
        try:
            font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 16)  # 进一步减小字体大小
        except:
            try:
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 16)  # 进一步减小字体大小
            except:
                font = pygame.font.Font(None, 16)  # 进一步减小字体大小
        
        # 绘制血量信息
        self._draw_stat_line(bar_x, bar_y, "HP:", (255, 255, 255), self.health, self.max_health, (255, 0, 0))
        
        # 绘制子弹储备信息
        self._draw_stat_line(bar_x, bar_y + line_spacing, "子弹:", (255, 255, 0), self.bullet_reserve, self.max_bullet_reserve, (255, 255, 0))
        
        # 绘制外星人储备信息
        self._draw_stat_line(bar_x, bar_y + line_spacing * 2, "外星人:", (0, 255, 255), self.alien_reserve, self.max_alien_reserve, (0, 255, 255))
    
    def _draw_stat_line(self, x, y, label, label_color, current, max_value, bar_color):
        """绘制单行统计信息"""
        # 尝试加载中文字体
        try:
            font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 16)
        except:
            try:
                font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 16)
            except:
                font = pygame.font.Font(None, 16)
        
        # 绘制标签
        label_surface = font.render(label, True, label_color)
        label_rect = label_surface.get_rect()
        label_rect.x = x + 10
        label_rect.y = y + 2
        self.screen.blit(label_surface, label_rect)
        
        # 绘制进度条
        bar_width = 180  # 减小进度条宽度，增加数值显示空间
        bar_height = 10  # 进一步减小进度条高度
        bar_rect = pygame.Rect(x + 60, y + 1, bar_width, bar_height)
        
        # 绘制背景
        pygame.draw.rect(self.screen, (100, 100, 100), bar_rect)
        
        # 绘制当前值
        ratio = max(0, current / max_value)
        current_width = int(bar_width * ratio)
        if current_width > 0:
            pygame.draw.rect(self.screen, bar_color, (x + 60, y + 1, current_width, bar_height))
        
        # 绘制边框
        pygame.draw.rect(self.screen, (255, 255, 255), bar_rect, 1)
        
        # 绘制数值
        value_text = font.render(f"{current}/{max_value}", True, label_color)
        value_rect = value_text.get_rect()
        value_rect.x = x + 60 + bar_width + 20  # 增加与进度条的间距
        value_rect.y = y + 2
        self.screen.blit(value_text, value_rect)
    
    def take_damage(self, damage=1):
        """Boss受到伤害，返回是否被消灭"""
        self.health -= damage
        self.attack_count += 1  # 增加攻击计数
        return self.health <= 0
    
    def check_fire(self, current_time):
        """检查是否可以发射子弹"""
        return current_time - self.last_fire_time >= self.fire_cooldown
    
    def fire(self):
        """发射子弹，重置发射计时器"""
        self.last_fire_time = pygame.time.get_ticks()
    
    def check_spawn_alien(self, current_time):
        """检查是否应该生成外星人"""
        return current_time - self.spawn_start_time >= self.spawn_cooldown
    
    def spawn_alien(self):
        """生成外星人，重置生成计时器"""
        self.spawn_start_time = pygame.time.get_ticks()
    
    def dodge_bullet(self):
        """瞬移到另一个躲避点"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dodge_time < self.dodge_cooldown:
            return  # 冷却中，不能躲避
        
        # 找到当前最接近的点
        current_center = self.rect.centerx
        closest_index = 0
        min_distance = abs(self.dodge_points[0] - current_center)
        
        for i, point in enumerate(self.dodge_points):
            distance = abs(point - current_center)
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        
        # 随机选择一个不同的点
        available_indices = [i for i in range(len(self.dodge_points)) if i != closest_index]
        if not available_indices:
            return
        
        new_index = random.choice(available_indices)
        new_x = self.dodge_points[new_index]
        
        # 瞬移到新位置
        self.rect.centerx = new_x
        self.x = float(self.rect.x)
        self.last_dodge_time = current_time
        self.attack_count = 0  # 重置攻击计数
