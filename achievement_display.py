import pygame
import os

class AchievementDisplay:
    """成就显示界面类"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.show_achievements = False
        self.current_page = 0
        self.achievements_per_page = 6
        
        # 创建关闭按钮
        self.close_button_rect = pygame.Rect(0, 0, 100, 40)
        self.close_button_rect.topright = (self.screen_rect.right - 20, 20)
        
        # 创建翻页按钮
        self.prev_button_rect = pygame.Rect(0, 0, 80, 40)
        self.prev_button_rect.bottomleft = (50, self.screen_rect.bottom - 20)
        
        self.next_button_rect = pygame.Rect(0, 0, 80, 40)
        self.next_button_rect.bottomright = (self.screen_rect.right - 50, self.screen_rect.bottom - 20)
        
        # 加载字体
        self.title_font = self._load_font(48)
        self.achievement_font = self._load_font(28)
        self.description_font = self._load_font(20)
    
    def _load_font(self, size):
        """加载支持中文的字体"""
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
        
        return pygame.font.Font(None, size)
    
    def draw_achievements(self):
        """绘制成就界面"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # 绘制标题
        title_text = self.title_font.render("成就系统", True, (255, 215, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 30
        self.screen.blit(title_text, title_rect)
        
        # 绘制已解锁成就数量
        unlocked_count = len(self.ai_game.achievement_system.get_unlocked_achievements())
        total_count = len(self.ai_game.achievement_system.achievements)
        unlocked_text = self.achievement_font.render(f"已解锁: {unlocked_count}/{total_count}", True, (255, 215, 0))
        unlocked_rect = unlocked_text.get_rect()
        unlocked_rect.topleft = (20, 20)
        self.screen.blit(unlocked_text, unlocked_rect)
        
        # 获取所有成就
        all_achievements = self.ai_game.achievement_system.achievements
        total_pages = (len(all_achievements) + self.achievements_per_page - 1) // self.achievements_per_page
        
        # 计算当前页的成就
        start_idx = self.current_page * self.achievements_per_page
        end_idx = min(start_idx + self.achievements_per_page, len(all_achievements))
        current_achievements = all_achievements[start_idx:end_idx]
        
        # 绘制成就列表
        start_y = 100
        for i, achievement in enumerate(current_achievements):
            achievement_y = start_y + i * 80
            
            # 绘制成就背景框
            bg_rect = pygame.Rect(50, achievement_y, self.screen_rect.width - 100, 70)
            if achievement.unlocked:
                bg_color = (50, 100, 50)
                border_color = (255, 215, 0)
            else:
                bg_color = (50, 50, 50)
                border_color = (100, 100, 100)
            
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((*bg_color, 150))
            self.screen.blit(bg_surface, bg_rect)
            pygame.draw.rect(self.screen, border_color, bg_rect, 2)
            
            # 绘制成就图标
            icon_rect = pygame.Rect(60, achievement_y + 10, 50, 50)
            if achievement.unlocked:
                try:
                    trophy_image = pygame.image.load('images/trophy.bmp')
                    trophy_image = pygame.transform.scale(trophy_image, (50, 50))
                    self.screen.blit(trophy_image, icon_rect)
                except:
                    # 如果图片加载失败，使用默认绘制
                    pygame.draw.polygon(self.screen, (255, 215, 0), [
                        (icon_rect.centerx, icon_rect.bottom - 5),
                        (icon_rect.left + 15, icon_rect.top + 10),
                        (icon_rect.right - 15, icon_rect.top + 10)
                    ])
                    pygame.draw.circle(self.screen, (255, 215, 0), (icon_rect.centerx, icon_rect.top + 5), 10)
            else:
                try:
                    lock_image = pygame.image.load('images/lock.bmp')
                    lock_image = pygame.transform.scale(lock_image, (50, 50))
                    self.screen.blit(lock_image, icon_rect)
                except:
                    # 如果图片加载失败，使用默认绘制
                    pygame.draw.rect(self.screen, (100, 100, 100), icon_rect)
                    pygame.draw.circle(self.screen, (150, 150, 150), icon_rect.center, 15)
                    pygame.draw.line(self.screen, (150, 150, 150), 
                                 (icon_rect.centerx - 10, icon_rect.centery),
                                 (icon_rect.centerx + 10, icon_rect.centery), 3)
                    pygame.draw.line(self.screen, (150, 150, 150),
                                 (icon_rect.centerx, icon_rect.centery - 10),
                                 (icon_rect.centerx, icon_rect.centery + 10), 3)
            
            # 绘制成就名称
            name_color = (255, 255, 255) if achievement.unlocked else (150, 150, 150)
            name_text = self.achievement_font.render(achievement.name, True, name_color)
            name_rect = name_text.get_rect()
            name_rect.left = 130
            name_rect.top = achievement_y + 8
            self.screen.blit(name_text, name_rect)
            
            # 绘制成就描述
            desc_color = (200, 200, 200) if achievement.unlocked else (100, 100, 100)
            desc_text = self.description_font.render(achievement.description, True, desc_color)
            desc_rect = desc_text.get_rect()
            desc_rect.left = 130
            desc_rect.top = achievement_y + 40
            self.screen.blit(desc_text, desc_rect)
            
            # 绘制奖励
            if achievement.reward > 0:
                reward_text = self.description_font.render(f"+{achievement.reward}分", True, (255, 215, 0))
                reward_rect = reward_text.get_rect()
                reward_rect.right = self.screen_rect.width - 70
                reward_rect.top = achievement_y + 25
                self.screen.blit(reward_text, reward_rect)
        
        # 绘制页码
        if total_pages > 1:
            page_text = self.description_font.render(f"第 {self.current_page + 1} / {total_pages} 页", True, (200, 200, 200))
            page_rect = page_text.get_rect()
            page_rect.centerx = self.screen_rect.centerx
            page_rect.bottom = self.screen_rect.bottom - 70
            self.screen.blit(page_text, page_rect)
        
        # 绘制关闭按钮
        pygame.draw.rect(self.screen, (200, 50, 50), self.close_button_rect)
        close_text = self.achievement_font.render("关闭", True, (255, 255, 255))
        close_rect = close_text.get_rect()
        close_rect.center = self.close_button_rect.center
        self.screen.blit(close_text, close_rect)
        
        # 绘制翻页按钮
        if self.current_page > 0:
            pygame.draw.rect(self.screen, (100, 100, 200), self.prev_button_rect)
            prev_text = self.achievement_font.render("上一页", True, (255, 255, 255))
            prev_rect = prev_text.get_rect()
            prev_rect.center = self.prev_button_rect.center
            self.screen.blit(prev_text, prev_rect)
        
        if self.current_page < total_pages - 1:
            pygame.draw.rect(self.screen, (100, 100, 200), self.next_button_rect)
            next_text = self.achievement_font.render("下一页", True, (255, 255, 255))
            next_rect = next_text.get_rect()
            next_rect.center = self.next_button_rect.center
            self.screen.blit(next_text, next_rect)
    
    def check_close_button(self, mouse_pos):
        """检查是否点击了关闭按钮"""
        if self.close_button_rect.collidepoint(mouse_pos):
            self.ai_game.sound_manager.play_sound('button_click')
            self.show_achievements = False
            return True
        return False
    
    def check_page_buttons(self, mouse_pos):
        """检查是否点击了翻页按钮"""
        all_achievements = self.ai_game.achievement_system.achievements
        total_pages = (len(all_achievements) + self.achievements_per_page - 1) // self.achievements_per_page
        
        if self.prev_button_rect.collidepoint(mouse_pos) and self.current_page > 0:
            self.ai_game.sound_manager.play_sound('button_click')
            self.current_page -= 1
        elif self.next_button_rect.collidepoint(mouse_pos) and self.current_page < total_pages - 1:
            self.ai_game.sound_manager.play_sound('button_click')
            self.current_page += 1
