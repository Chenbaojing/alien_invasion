import pygame
import json
import os

class Achievement:
    """成就类，定义单个成就"""
    def __init__(self, achievement_id, name, description, condition, reward=0):
        self.achievement_id = achievement_id
        self.name = name
        self.description = description
        self.condition = condition  # 成就条件函数
        self.reward = reward  # 成就奖励（分数）
        self.unlocked = False  # 是否已解锁
        self.unlock_time = None  # 解锁时间

class AchievementSystem:
    """成就系统类"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.achievements = []
        self.achievement_data = {}
        self._initialize_achievements()
        self._load_achievements()
    
    def _initialize_achievements(self):
        """初始化所有成就"""
        # 游戏进度成就
        self.achievements.append(Achievement(
            "first_blood",
            "初露锋芒",
            "消灭第1个外星人",
            lambda: self.ai_game.stats.score >= 50,
            100
        ))
        
        self.achievements.append(Achievement(
            "hundred_kills",
            "百战百胜",
            "累计消灭100个外星人",
            lambda: self.ai_game.stats.aliens_killed >= 100,
            500
        ))
        
        self.achievements.append(Achievement(
            "thousand_kills",
            "千军万马",
            "累计消灭1000个外星人",
            lambda: self.ai_game.stats.aliens_killed >= 1000,
            2000
        ))
        
        self.achievements.append(Achievement(
            "ten_thousand_kills",
            "一将功成万骨枯",
            "累计消灭10000个外星人",
            lambda: self.ai_game.stats.aliens_killed >= 10000,
            10000
        ))
        
        self.achievements.append(Achievement(
            "level_5",
            "初入江湖",
            "达到第5关",
            lambda: self.ai_game.stats.max_level_reached >= 5,
            300
        ))
        
        self.achievements.append(Achievement(
            "level_10",
            "身经百战",
            "达到第10关",
            lambda: self.ai_game.stats.max_level_reached >= 10,
            800
        ))
        
        self.achievements.append(Achievement(
            "level_20",
            "登峰造极",
            "达到第20关",
            lambda: self.ai_game.stats.max_level_reached >= 20,
            2000
        ))
        
        # 分数成就
        self.achievements.append(Achievement(
            "score_1000",
            "小试牛刀",
            "单局得分达到1000分",
            lambda: self.ai_game.stats.score >= 1000,
            200
        ))
        
        self.achievements.append(Achievement(
            "score_10000",
            "炉火纯青",
            "单局得分达到10000分",
            lambda: self.ai_game.stats.score >= 10000,
            1000
        ))
        
        self.achievements.append(Achievement(
            "score_100000",
            "独孤求败",
            "单局得分达到100000分",
            lambda: self.ai_game.stats.score >= 100000,
            5000
        ))
        
        # 道具使用成就
        self.achievements.append(Achievement(
            "shield_master",
            "护盾大师",
            "使用护盾10次",
            lambda: self.ai_game.stats.shield_uses >= 10,
            300
        ))
        
        self.achievements.append(Achievement(
            "freeze_master",
            "冰封千里",
            "使用时间冻结10次",
            lambda: self.ai_game.stats.freeze_uses >= 10,
            300
        ))
        
        self.achievements.append(Achievement(
            "nuke_master",
            "核弹专家",
            "使用核弹5次",
            lambda: self.ai_game.stats.nuke_uses >= 5,
            500
        ))
        
        # Boss模式成就
        self.achievements.append(Achievement(
            "boss_killer",
            "Boss杀手",
            "击败第1关Boss",
            lambda: self.ai_game.stats.bosses_defeated >= 1,
            500
        ))
        
        self.achievements.append(Achievement(
            "boss_master",
            "Boss终结者",
            "击败第5关Boss",
            lambda: self.ai_game.stats.bosses_defeated >= 5,
            3000
        ))
        
        # 狙击模式成就
        self.achievements.append(Achievement(
            "sniper_rookie",
            "狙击新手",
            "狙击模式发射100发子弹",
            lambda: self.ai_game.stats.sniper_shots_fired >= 100,
            200
        ))
        
        self.achievements.append(Achievement(
            "sniper_expert",
            "狙击专家",
            "狙击模式命中率达到80%且发射至少50发",
            lambda: (self.ai_game.stats.sniper_shots_fired >= 50 and 
                     self.ai_game.stats.sniper_shots_fired > 0 and
                     self.ai_game.stats.sniper_shots_hit / self.ai_game.stats.sniper_shots_fired >= 0.8),
            500
        ))
        
        self.achievements.append(Achievement(
            "sniper_master",
            "狙击大师",
            "狙击模式完成10个关卡",
            lambda: self.ai_game.stats.sniper_levels_completed >= 10,
            800
        ))
        
        self.achievements.append(Achievement(
            "sniper_perfect",
            "完美狙击",
            "狙击模式完成5个完美回合（无失误）",
            lambda: self.ai_game.stats.sniper_perfect_rounds >= 5,
            1000
        ))
        
        self.achievements.append(Achievement(
            "sniper_legend",
            "狙击传说",
            "狙击模式命中率达到90%且发射至少100发",
            lambda: (self.ai_game.stats.sniper_shots_fired >= 100 and 
                     self.ai_game.stats.sniper_shots_fired > 0 and
                     self.ai_game.stats.sniper_shots_hit / self.ai_game.stats.sniper_shots_fired >= 0.9),
            2000
        ))
        
        # 特殊成就
        self.achievements.append(Achievement(
            "perfect_level",
            "完美通关",
            "在不损失生命的情况下通关一关",
            lambda: self.ai_game.stats.lives_lost_this_level == 0 and self.ai_game.stats.max_level_reached > 1,
            500
        ))
        
        self.achievements.append(Achievement(
            "combo_master",
            "连击大师",
            "单次连击消灭10个外星人",
            lambda: self.ai_game.stats.max_combo >= 10,
            400
        ))
        
        self.achievements.append(Achievement(
            "survivor",
            "生存专家",
            "累计损失生命不超过10次",
            lambda: self.ai_game.stats.total_lives_lost <= 10 and self.ai_game.stats.max_level_reached >= 5,
            600
        ))
    
    def check_achievements(self):
        """检查并解锁成就"""
        newly_unlocked = []
        for achievement in self.achievements:
            if not achievement.unlocked:
                try:
                    if achievement.condition():
                        achievement.unlocked = True
                        achievement.unlock_time = pygame.time.get_ticks()
                        newly_unlocked.append(achievement)
                        self.ai_game.stats.score += achievement.reward
                except Exception as e:
                    pass
        
        # 如果有新解锁的成就，保存成就数据
        if newly_unlocked:
            self.save_achievements()
            
        return newly_unlocked
    
    def get_unlocked_achievements(self):
        """获取已解锁的成就列表"""
        return [a for a in self.achievements if a.unlocked]
    
    def get_locked_achievements(self):
        """获取未解锁的成就列表"""
        return [a for a in self.achievements if not a.unlocked]
    
    def get_achievement_progress(self, achievement_id):
        """获取特定成就的进度"""
        achievement = next((a for a in self.achievements if a.achievement_id == achievement_id), None)
        if achievement:
            return achievement.unlocked
        return False
    
    def _load_achievements(self):
        """从文件加载成就数据"""
        try:
            if os.path.exists('personal information/achievements.json'):
                with open('personal information/achievements.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for achievement in self.achievements:
                        if achievement.achievement_id in data:
                            achievement.unlocked = data[achievement.achievement_id].get('unlocked', False)
        except Exception as e:
            pass
    
    def save_achievements(self):
        """保存成就数据到文件"""
        try:
            data = {}
            for achievement in self.achievements:
                data[achievement.achievement_id] = {
                    'unlocked': achievement.unlocked,
                    'unlock_time': achievement.unlock_time
                }
            with open('personal information/achievements.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass
    
    def reset_achievements(self):
        """重置所有成就"""
        for achievement in self.achievements:
            achievement.unlocked = False
            achievement.unlock_time = None
        self.save_achievements()
    
    def draw_achievement_notification(self, screen, achievement, duration=3000, y_offset=0):
        font = self._load_chinese_font(24)
        title_font = self._load_chinese_font(36)
        
        notification_width = 450
        notification_height = 110
        notification_x = (screen.get_width() - notification_width) // 2
        notification_y = 50 + y_offset
        
        progress = min(1.0, (3000 - duration) / 500)
        if progress < 1.0:
            offset_y = int((1.0 - progress) * 50)
            notification_y -= offset_y
            alpha = int(progress * 255)
        else:
            alpha = 255
        
        bg_surface = pygame.Surface((notification_width, notification_height), pygame.SRCALPHA)
        
        for i in range(notification_height):
            factor = i / notification_height
            base_alpha = int(alpha * (230 - factor * 50))
            r = int(255 * (1 - factor * 0.2))
            g = int(200 * (1 - factor * 0.3))
            b = int(50 * (1 - factor * 0.5))
            line_surface = pygame.Surface((notification_width, 1), pygame.SRCALPHA)
            line_surface.fill((r, g, b))
            line_surface.set_alpha(base_alpha)
            bg_surface.blit(line_surface, (0, i))
        
        screen.blit(bg_surface, (notification_x, notification_y))
        
        border_surface = pygame.Surface((notification_width, notification_height), pygame.SRCALPHA)
        border_surface.fill((255, 215, 0))
        border_surface.set_alpha(int(alpha * 0.8))
        pygame.draw.rect(border_surface, (255, 215, 0), 
                        (0, 0, notification_width, notification_height), 3)
        screen.blit(border_surface, (notification_x, notification_y))
        
        glow_surface = pygame.Surface((notification_width + 20, notification_height + 20), pygame.SRCALPHA)
        for i in range(15, 0, -1):
            glow_alpha = int(alpha * (8 - i * 0.5))
            glow_rect = glow_surface.get_rect().inflate(-i * 2, -i * 2)
            pygame.draw.rect(glow_surface, (255, 215, 0), glow_rect, border_radius=12)
            temp_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            temp_surface.fill((255, 215, 0))
            temp_surface.set_alpha(glow_alpha)
            glow_surface.blit(temp_surface, glow_rect.topleft)
        screen.blit(glow_surface, (notification_x - 10, notification_y - 10))
        
        trophy_x = notification_x + 35
        trophy_y = notification_y + 30
        
        pulse = 1.0 + 0.1 * (1 + (pygame.time.get_ticks() % 1000) / 500)
        trophy_size = int(40 * pulse)
        
        pygame.draw.circle(screen, (255, 215, 0), (trophy_x + 25, trophy_y + 10), int(12 * pulse))
        pygame.draw.circle(screen, (255, 235, 50), (trophy_x + 25, trophy_y + 10), int(8 * pulse))
        
        cup_points = [
            (trophy_x, trophy_y + 45),
            (trophy_x + 50, trophy_y + 45),
            (trophy_x + 40, trophy_y + 20),
            (trophy_x + 10, trophy_y + 20)
        ]
        pygame.draw.polygon(screen, (255, 215, 0), cup_points)
        pygame.draw.polygon(screen, (255, 235, 50), [
            (trophy_x + 5, trophy_y + 40),
            (trophy_x + 45, trophy_y + 40),
            (trophy_x + 38, trophy_y + 25),
            (trophy_x + 12, trophy_y + 25)
        ])
        
        pygame.draw.rect(screen, (200, 170, 0), (trophy_x + 15, trophy_y + 45, 20, 15))
        pygame.draw.rect(screen, (220, 190, 0), (trophy_x + 18, trophy_y + 45, 14, 12))
        
        title_text = title_font.render("成就解锁!", True, (255, 255, 255))
        title_shadow = title_font.render("成就解锁!", True, (0, 0, 0, 150))
        title_rect = title_text.get_rect()
        title_rect.left = trophy_x + 60
        title_rect.top = notification_y + 15
        title_shadow_rect = title_shadow.get_rect()
        title_shadow_rect.center = (title_rect.centerx + 2, title_rect.centery + 2)
        screen.blit(title_shadow, title_shadow_rect)
        screen.blit(title_text, title_rect)
        
        name_text = font.render(achievement.name, True, (255, 255, 255))
        name_shadow = font.render(achievement.name, True, (0, 0, 0, 150))
        name_rect = name_text.get_rect()
        name_rect.left = trophy_x + 60
        name_rect.top = notification_y + 55
        name_shadow_rect = name_shadow.get_rect()
        name_shadow_rect.center = (name_rect.centerx + 2, name_rect.centery + 2)
        screen.blit(name_shadow, name_shadow_rect)
        screen.blit(name_text, name_rect)
        
        if achievement.reward > 0:
            reward_text = font.render(f"+{achievement.reward}分", True, (255, 255, 0))
            reward_shadow = font.render(f"+{achievement.reward}分", True, (0, 0, 0, 150))
            reward_rect = reward_text.get_rect()
            reward_rect.right = notification_x + notification_width - 25
            reward_rect.top = notification_y + 25
            reward_shadow_rect = reward_shadow.get_rect()
            reward_shadow_rect.center = (reward_rect.centerx + 2, reward_rect.centery + 2)
            screen.blit(reward_shadow, reward_shadow_rect)
            screen.blit(reward_text, reward_rect)
        
        progress_bar_width = notification_width - 20
        progress_bar_x = notification_x + 10
        progress_bar_y = notification_y + notification_height - 8
        progress_bar_height = 4
        remaining_ratio = duration / 3000
        remaining_width = int(progress_bar_width * remaining_ratio)
        
        pygame.draw.rect(screen, (0, 0, 0, 100), 
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), border_radius=2)
        pygame.draw.rect(screen, (255, 215, 0), 
                        (progress_bar_x, progress_bar_y, remaining_width, progress_bar_height), border_radius=2)
    
    def _load_chinese_font(self, size=36):
        """加载支持中文的字体"""
        import os
        # Windows系统中的中文字体路径
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
        ]
        
        # 尝试加载中文字体
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
        
        # 如果加载失败，使用默认字体
        return pygame.font.Font(None, size)
