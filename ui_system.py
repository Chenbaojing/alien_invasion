import pygame

from button import Button
from instructions import Instructions
from achievement_display import AchievementDisplay
from sniper_scope import SniperScope
from shop import Shop
from settings_ui import SettingsUI

class UISystem:
    """UI系统类，管理所有用户界面元素"""
    def __init__(self, game):
        """初始化UI系统"""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        
        # 创建UI元素
        self._create_buttons()
        self._create_ui_components()
        
        # UI状态
        self.show_instructions = True
        self.show_settings = False
        self.show_stats = False
        self.show_entertainment = False
    
    def _create_buttons(self):
        """创建所有按钮"""
        # 创建Play按钮
        self.play_button = Button(self.game, "Play")
        
        # 创建模式选择按钮
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 2

        # 创建模式选择按钮
        self.normal_mode_button = Button(self.game, "普通模式", 150, 40, (100, 100, 100), (screen_center_x, screen_center_y + 50))
        self.powerups_mode_button = Button(self.game, "道具模式", 150, 40, (0, 150, 255), (screen_center_x, screen_center_y + 100))
        self.unlimited_mode_button = Button(self.game, "无限火力", 150, 40, (255, 100, 0), (screen_center_x, screen_center_y + 150))
        self.boss_mode_button = Button(self.game, "Boss模式", 150, 40, (255, 0, 100), (screen_center_x, screen_center_y + 200))
        self.entertainment_mode_button = Button(self.game, "娱乐模式", 150, 40, (255, 165, 0), (screen_center_x, screen_center_y + 250))

        self.easy_difficulty_button = Button(self.game, "简单", 100, 35, (100, 200, 100), (screen_center_x - 150, screen_center_y + 320))
        self.normal_difficulty_button = Button(self.game, "普通", 100, 35, (150, 150, 150), (screen_center_x - 50, screen_center_y + 320))
        self.hard_difficulty_button = Button(self.game, "困难", 100, 35, (255, 100, 100), (screen_center_x + 50, screen_center_y + 320))
        self.expert_difficulty_button = Button(self.game, "专家", 100, 35, (200, 50, 50), (screen_center_x + 150, screen_center_y + 320))
        
        # 创建成就按钮
        self.achievement_button = Button(self.game, "成就", 120, 40, (255, 215, 0), (80, 30))
        
        # 创建商店按钮
        self.shop_button = Button(self.game, "商店", 120, 40, (100, 200, 100), (220, 30))
        
        # 创建设置按钮
        self.settings_button = Button(self.game, "设置", 120, 40, (0, 135, 0), (360, 30))
        
        # 创建统计信息按钮
        self.stats_button = Button(self.game, "统计", 120, 40, (0, 0, 255), (500, 30))
        
        # 创建娱乐模式按钮
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 2
        start_y = screen_center_y - 210

        self.sniper_button = Button(self.game, "狙击模式", 200, 60, (75, 0, 130), (screen_center_x, start_y))
        self.dodge_button = Button(self.game, "太空躲避陨石", 200, 60, (0, 150, 255), (screen_center_x, start_y + 70))
        self.shoot_button = Button(self.game, "太空射击练习", 200, 60, (0, 255, 0), (screen_center_x, start_y + 140))
        self.hangman_button = Button(self.game, "猜字母", 200, 60, (128, 0, 128), (screen_center_x, start_y + 210))
        self.pong_button = Button(self.game, "颠球", 200, 60, (255, 105, 180), (screen_center_x, start_y + 280))
        self.lander_button = Button(self.game, "飞船着陆", 200, 60, (0, 255, 255), (screen_center_x, start_y + 350))
        self.entertainment_back_button = Button(self.game, "返回", 120, 45, (200, 0, 0), (screen_center_x, start_y + 420))
    
    def _create_ui_components(self):
        """创建UI组件"""
        self.instructions = Instructions(self.game)
        self.achievement_display = AchievementDisplay(self.game)
        self.sniper_scope = SniperScope(self.game)
        self.shop = Shop(self.game)
        self.settings_ui = SettingsUI(self.game)
    
    def handle_mouse_click(self, mouse_pos):
        """处理鼠标点击事件"""
        if self.game.game_core.show_level_select:
            self._check_level_select(mouse_pos)
        elif self.show_instructions:
            self.instructions.check_page_buttons(mouse_pos)
            self._check_instructions_close(mouse_pos)
        elif self.achievement_display.show_achievements:
            self.achievement_display.check_page_buttons(mouse_pos)
            self.achievement_display.check_close_button(mouse_pos)
        elif self.shop.shop_active:
            self.shop.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=mouse_pos))
        elif self.show_settings:
            result = self.settings_ui.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=mouse_pos))
            if result == "close":
                self.show_settings = False
        elif self.show_stats:
            # 检查统计界面的关闭按钮
            close_button_rect = pygame.Rect(
                self.settings.screen_width - 100,
                20,
                80,
                30
            )
            if close_button_rect.collidepoint(mouse_pos):
                self.show_stats = False
        elif self.show_entertainment:
            self._check_entertainment_options(mouse_pos)
        else:
            self._check_play_button(mouse_pos)
            self._check_mode_buttons(mouse_pos)
            self._check_difficulty_buttons(mouse_pos)
            self._check_achievement_button(mouse_pos)
            self._check_shop_button(mouse_pos)
            self._check_settings_button(mouse_pos)
            self._check_stats_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """检查Play按钮点击"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game.game_core.game_active:
            self.play_button.trigger_click()
            self.game.game_core.sound_manager.play_sound('button_click')
            self.game.game_core.show_level_select = True
            pygame.mouse.set_visible(True)
    
    def _check_mode_buttons(self, mouse_pos):
        """检查模式按钮点击"""
        if not self.game.game_core.game_active:
            if self.normal_mode_button.rect.collidepoint(mouse_pos):
                self.normal_mode_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_NORMAL
                self._apply_mode_settings()
                self.game.game_core.stats.reset_stats()
                self.game.game_core.sb.prep_score()
                self.game.game_core.sb.prep_high_score()
                self.game.game_core.last_played_level = self.game.game_core.stats.last_level
                self.game.game_core.selected_level = self.game.game_core.last_played_level
            elif self.powerups_mode_button.rect.collidepoint(mouse_pos):
                self.powerups_mode_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_POWERUPS
                self._apply_mode_settings()
                self.game.game_core.stats.reset_stats()
                self.game.game_core.sb.prep_score()
                self.game.game_core.sb.prep_high_score()
                self.game.game_core.last_played_level = self.game.game_core.stats.last_level
                self.game.game_core.selected_level = self.game.game_core.last_played_level
            elif self.unlimited_mode_button.rect.collidepoint(mouse_pos):
                self.unlimited_mode_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_UNLIMITED
                self._apply_mode_settings()
                self.game.game_core.stats.reset_stats()
                self.game.game_core.sb.prep_score()
                self.game.game_core.sb.prep_high_score()
                self.game.game_core.last_played_level = self.game.game_core.stats.last_level
                self.game.game_core.selected_level = self.game.game_core.last_played_level
            elif self.boss_mode_button.rect.collidepoint(mouse_pos):
                self.boss_mode_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_BOSS
                self._apply_mode_settings()
                self.game.game_core.stats.reset_stats()
                self.game.game_core.sb.prep_score()
                self.game.game_core.sb.prep_high_score()
                self.game.game_core.selected_level = 1
            elif self.entertainment_mode_button.rect.collidepoint(mouse_pos):
                self.entertainment_mode_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.show_entertainment = True
    
    def _check_achievement_button(self, mouse_pos):
        """检查成就按钮点击"""
        if not self.game.game_core.game_active and self.achievement_button.rect.collidepoint(mouse_pos):
            self.achievement_button.trigger_click()
            self.game.game_core.sound_manager.play_sound('button_click')
            self.achievement_display.show_achievements = True
            self.achievement_display.current_page = 0
    
    def _check_shop_button(self, mouse_pos):
        """检查商店按钮点击"""
        if not self.game.game_core.game_active and self.shop_button.rect.collidepoint(mouse_pos):
            self.shop_button.trigger_click()
            self.game.game_core.sound_manager.play_sound('button_click')
            self.shop.shop_active = True
    
    def _check_settings_button(self, mouse_pos):
        """检查设置按钮点击"""
        if not self.game.game_core.game_active and self.settings_button.rect.collidepoint(mouse_pos):
            self.settings_button.trigger_click()
            self.game.game_core.sound_manager.play_sound('button_click')
            self.show_settings = True
    
    def _check_stats_button(self, mouse_pos):
        """检查统计按钮点击"""
        if not self.game.game_core.game_active and self.stats_button.rect.collidepoint(mouse_pos):
            self.stats_button.trigger_click()
            self.game.game_core.sound_manager.play_sound('button_click')
            self.show_stats = True
    
    def _check_difficulty_buttons(self, mouse_pos):
        """检查难度按钮点击"""
        if not self.game.game_core.game_active:
            if self.easy_difficulty_button.rect.collidepoint(mouse_pos):
                self.easy_difficulty_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_EASY
            elif self.normal_difficulty_button.rect.collidepoint(mouse_pos):
                self.normal_difficulty_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_NORMAL
            elif self.hard_difficulty_button.rect.collidepoint(mouse_pos):
                self.hard_difficulty_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_HARD
            elif self.expert_difficulty_button.rect.collidepoint(mouse_pos):
                self.expert_difficulty_button.trigger_click()
                self.game.game_core.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_EXPERT
    
    def _apply_mode_settings(self):
        """根据当前模式应用设置"""
        if self.settings.game_mode == self.settings.MODE_NORMAL:
            self.settings.bullets_allowed = 10
            self.settings.explosive_aliens_per_fleet = 0
        elif self.settings.game_mode == self.settings.MODE_POWERUPS:
            self.settings.bullets_allowed = 10
            self.settings.explosive_aliens_per_fleet = 2
        elif self.settings.game_mode == self.settings.MODE_UNLIMITED:
            self.settings.bullets_allowed = 999
            self.settings.explosive_aliens_per_fleet = 2
        elif self.settings.game_mode == self.settings.MODE_BOSS:
            self.settings.bullets_allowed = 999  # Boss模式子弹无限
            self.settings.explosive_aliens_per_fleet = 0
        elif self.settings.game_mode == self.settings.MODE_SNIPER:
            self.settings.bullets_allowed = 5  # 狙击模式子弹数量有限
            self.settings.explosive_aliens_per_fleet = 0  # 狙击模式没有爆炸外星人
    
    def _check_instructions_close(self, mouse_pos):
        """检查是否点击了使用说明的关闭按钮"""
        if self.show_instructions:
            if self.instructions.check_close_button(mouse_pos):
                self.show_instructions = False
    
    def _check_level_select(self, mouse_pos):
        """检查关卡选择"""
        if self.game.game_core.show_level_select:
            button_width = 70
            button_height = 70
            buttons_per_row = 5
            start_x = (self.settings.screen_width - (buttons_per_row * button_width + (buttons_per_row - 1) * 20)) // 2
            start_y = (self.settings.screen_height - (2 * button_height + 20)) // 2

            for level in range(1, self.game.game_core.max_level + 1):
                row = (level - 1) // buttons_per_row
                col = (level - 1) % buttons_per_row
                button_x = start_x + col * (button_width + 20)
                button_y = start_y + row * (button_height + 20)

                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    self.game.game_core.sound_manager.play_sound('button_click')
                    self.game.game_core.selected_level = level
                    self.game.game_core.show_level_select = False
                    self.game.game_core._start_game_with_level()
                    return

            continue_button_rect = pygame.Rect(
                self.settings.screen_width // 2 - 130,
                start_y + 2 * (button_height + 20) + 20,
                260,
                45
            )
            if continue_button_rect.collidepoint(mouse_pos):
                self.game.game_core.sound_manager.play_sound('button_click')
                self.game.game_core.selected_level = self.game.game_core.last_played_level + 1
                self.game.game_core.show_level_select = False
                self.game.game_core._start_game_with_level()
                return

            back_button_rect = pygame.Rect(
                self.settings.screen_width // 2 - 60,
                start_y + 2 * (button_height + 20) + 75,
                120,
                45
            )
            if back_button_rect.collidepoint(mouse_pos):
                self.game.game_core.sound_manager.play_sound('button_click')
                self.game.game_core.show_level_select = False
                return
    
    def _check_entertainment_options(self, mouse_pos):
        """检查娱乐模式选项的点击"""
        import subprocess

        if self.sniper_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            self.show_entertainment = False
            # 切换到狙击模式
            self.settings.game_mode = self.settings.MODE_SNIPER
            self._apply_mode_settings()
            self.game.game_core.stats.reset_stats()
            self.game.game_core.sb.prep_score()
            self.game.game_core.sb.prep_high_score()
            self.game.game_core.last_played_level = self.game.game_core.stats.last_level
            self.game.game_core.selected_level = self.game.game_core.last_played_level
        elif self.dodge_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            # 启动太空躲避陨石游戏
            subprocess.Popen(['python', 'game_1.py'])
        elif self.shoot_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            # 启动太空射击练习游戏
            subprocess.Popen(['python', 'game_2.py'])
        elif self.pong_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            # 启动颠球游戏
            subprocess.Popen(['python', 'PyPong.py'])
        elif self.lander_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            # 启动飞船着陆游戏
            subprocess.Popen(['python', 'LunarLander.py'])
        elif self.entertainment_back_button.rect.collidepoint(mouse_pos):
            self.game.game_core.sound_manager.play_sound('button_click')
            self.show_entertainment = False
    
    def draw(self):
        """绘制所有UI元素"""
        # 如果显示关卡选择界面
        if self.game.game_core.show_level_select:
            self._draw_level_select_screen()
        # 如果显示使用说明，只绘制使用说明
        elif self.show_instructions:
            self.instructions.draw_instructions()
        # 如果显示成就界面，只绘制成就界面
        elif self.achievement_display.show_achievements:
            self.achievement_display.draw_achievements()
        # 如果显示商店界面，只绘制商店界面
        elif self.shop.shop_active:
            self.shop.draw()
        # 如果显示设置界面，只绘制设置界面
        elif self.show_settings:
            self.settings_ui.draw()
        # 如果显示娱乐模式界面，只绘制娱乐模式界面
        elif self.show_entertainment:
            # 绘制娱乐模式页面
            self.screen.fill(self.settings.bg_color)

            # 标题
            title_font = self.game._load_chinese_font(size=64)
            title_text = title_font.render("娱乐模式", True, (0, 0, 0))
            title_rect = title_text.get_rect()
            title_rect.centerx = self.settings.screen_width // 2
            title_rect.y = 100
            self.screen.blit(title_text, title_rect)

            # 更新并绘制娱乐模式按钮
            self.sniper_button.update()
            self.sniper_button.draw_button()

            self.dodge_button.update()
            self.dodge_button.draw_button()

            self.shoot_button.update()
            self.shoot_button.draw_button()

            self.hangman_button.update()
            self.hangman_button.draw_button()

            self.pong_button.update()
            self.pong_button.draw_button()

            self.entertainment_back_button.update()
            self.entertainment_back_button.draw_button()
        # 如果显示统计界面，只绘制统计界面
        elif self.show_stats:
            # 绘制统计页面
            self.screen.fill(self.settings.bg_color)

            # 标题
            title_font = self.game._load_chinese_font(size=64)
            title_text = title_font.render("游戏统计", True, (0, 0, 0))
            title_rect = title_text.get_rect()
            title_rect.centerx = self.settings.screen_width // 2
            title_rect.y = 50
            self.screen.blit(title_text, title_rect)

            # 关闭按钮
            close_font = self.game._load_chinese_font(size=24)
            close_text = close_font.render("关闭", True, (0, 0, 0))
            close_rect = pygame.Rect(
                self.settings.screen_width - 100,
                20,
                80,
                30
            )
            pygame.draw.rect(self.screen, (255, 0, 0), close_rect)
            close_text_rect = close_text.get_rect(center=close_rect.center)
            self.screen.blit(close_text, close_text_rect)

            # 统计信息
            stats_font = self.game._load_chinese_font(size=24)
            stats_texts = [
                f"总游戏时长: {self.game.game_core.stats.get_play_time_formatted()}",
                f"总击杀外星人: {self.game.game_core.stats.aliens_killed}",
                f"总击败Boss: {self.game.game_core.stats.bosses_defeated}",
                f"总发射子弹: {self.game.game_core.stats.total_shots_fired}",
                f"总命中子弹: {self.game.game_core.stats.total_shots_hit}",
                f"总命中率: {self.game.game_core.stats.get_hit_rate_formatted()}",
                f"总护盾使用: {self.game.game_core.stats.shield_uses}",
                f"总时间冻结使用: {self.game.game_core.stats.freeze_uses}",
                f"总核弹使用: {self.game.game_core.stats.nuke_uses}",
                f"总损失生命: {self.game.game_core.stats.total_lives_lost}",
                f"最高连击: {self.game.game_core.stats.max_combo}",
                f"最高关卡: {self.game.game_core.stats.max_level_reached}"
            ]

            # 绘制统计信息
            y_offset = 150
            for text in stats_texts:
                stats_surface = stats_font.render(text, True, (0, 0, 0))
                stats_rect = stats_surface.get_rect()
                stats_rect.x = 100
                stats_rect.y = y_offset
                self.screen.blit(stats_surface, stats_rect)
                y_offset += 40
        else:
            # 如果游戏处于非活动状态,就绘制Play按钮和其他UI元素
            if not self.game.game_core.game_active:
                self.achievement_button.update()
                self.shop_button.update()
                self.settings_button.update()
                self.stats_button.update()
                self.play_button.update()
                self.normal_mode_button.update()
                self.powerups_mode_button.update()
                self.unlimited_mode_button.update()
                self.boss_mode_button.update()
                self.entertainment_mode_button.update()
                self.easy_difficulty_button.update()
                self.normal_difficulty_button.update()
                self.hard_difficulty_button.update()
                self.expert_difficulty_button.update()

                self.achievement_button.draw_button()
                self.shop_button.draw_button()
                self.settings_button.draw_button()
                self.stats_button.draw_button()
                self.play_button.draw_button()
                self.normal_mode_button.draw_button()
                self.powerups_mode_button.draw_button()
                self.unlimited_mode_button.draw_button()
                self.boss_mode_button.draw_button()
                self.entertainment_mode_button.draw_button()
                self.easy_difficulty_button.draw_button()
                self.normal_difficulty_button.draw_button()
                self.hard_difficulty_button.draw_button()
                self.expert_difficulty_button.draw_button()

                # 绘制当前模式和难度信息
                mode_text = f"当前模式: {self._get_mode_name()}"
                mode_font = self.game._load_chinese_font(size=36)
                mode_image = mode_font.render(mode_text, True, (0, 0, 0))
                mode_rect = mode_image.get_rect()
                mode_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 100)
                self.screen.blit(mode_image, mode_rect)

                difficulty_text = f"当前难度: {self._get_difficulty_name()}"
                difficulty_font = self.game._load_chinese_font(size=28)
                difficulty_image = difficulty_font.render(difficulty_text, True, (0, 0, 0))
                difficulty_rect = difficulty_image.get_rect()
                difficulty_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 60)
                self.screen.blit(difficulty_image, difficulty_rect)

                self._draw_menu_background()
            else:
                # 游戏活动状态下的UI绘制
                # 绘制飞船
                self.game.game_core.ship.blitme()

                # 狙击模式绘制瞄准镜
                if self.settings.game_mode == self.settings.MODE_SNIPER:
                    self.sniper_scope.draw()

                # 绘制子弹
                for bullet in self.game.game_core.bullets.sprites():
                    bullet.draw_bullet()

                # 绘制外星人子弹
                for bullet in self.game.game_core.alien_bullets.sprites():
                    self.screen.blit(bullet.image, bullet.rect)

                # 绘制外星人
                self.game.game_core.aliens.draw(self.screen)
                
                # 绘制Boss
                for boss in self.game.game_core.bosses:
                    self.screen.blit(boss.image, boss.rect)
                    # 绘制Boss血条
                    boss.draw_health_bar()
                
                # 绘制分身飞船
                if self.game.game_core.clone_active and self.game.game_core.clone_ship:
                    self.game.game_core.clone_ship.blitme()

                # 绘制支援飞船
                if self.game.game_core.summon_active and self.game.game_core.summon_ships:
                    for support_ship in self.game.game_core.summon_ships:
                        support_ship.blitme()
    
    def _draw_level_select_screen(self):
        """绘制关卡选择屏幕"""
        self.screen.fill(self.settings.bg_color)
        
        # 标题
        title_font = self.game._load_chinese_font(size=64)
        title_text = title_font.render("选择关卡", True, (0, 0, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.settings.screen_width // 2
        title_rect.y = 100
        self.screen.blit(title_text, title_rect)
        
        # 绘制关卡按钮
        button_width = 70
        button_height = 70
        buttons_per_row = 5
        start_x = (self.settings.screen_width - (buttons_per_row * button_width + (buttons_per_row - 1) * 20)) // 2
        start_y = (self.settings.screen_height - (2 * button_height + 20)) // 2
        
        for level in range(1, self.game.game_core.max_level + 1):
            row = (level - 1) // buttons_per_row
            col = (level - 1) % buttons_per_row
            button_x = start_x + col * (button_width + 20)
            button_y = start_y + row * (button_height + 20)
            
            # 绘制关卡按钮
            pygame.draw.rect(self.screen, (0, 150, 0), (button_x, button_y, button_width, button_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (button_x, button_y, button_width, button_height), 2)
            
            # 绘制关卡数字
            level_font = self.game._load_chinese_font(size=36)
            level_text = level_font.render(str(level), True, (255, 255, 255))
            level_rect = level_text.get_rect()
            level_rect.center = (button_x + button_width // 2, button_y + button_height // 2)
            self.screen.blit(level_text, level_rect)
        
        # 绘制继续按钮
        continue_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 130,
            start_y + 2 * (button_height + 20) + 20,
            260,
            45
        )
        pygame.draw.rect(self.screen, (0, 0, 255), continue_button_rect)
        pygame.draw.rect(self.screen, (0, 0, 255), continue_button_rect, 2)
        
        continue_font = self.game._load_chinese_font(size=24)
        continue_text = continue_font.render("继续游戏", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button_rect.center)
        self.screen.blit(continue_text, continue_text_rect)
        
        # 绘制返回按钮
        back_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 60,
            start_y + 2 * (button_height + 20) + 75,
            120,
            45
        )
        pygame.draw.rect(self.screen, (255, 0, 0), back_button_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), back_button_rect, 2)
        
        back_font = self.game._load_chinese_font(size=24)
        back_text = back_font.render("返回", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)
    
    def _draw_menu_background(self):
        """绘制菜单背景"""
        # 这里可以添加菜单背景的绘制代码
        pass
    
    def _get_mode_name(self):
        """获取当前模式名称"""
        if self.settings.game_mode == self.settings.MODE_NORMAL:
            return "普通模式"
        elif self.settings.game_mode == self.settings.MODE_POWERUPS:
            return "道具模式"
        elif self.settings.game_mode == self.settings.MODE_UNLIMITED:
            return "无限火力"
        elif self.settings.game_mode == self.settings.MODE_BOSS:
            return "Boss模式"
        elif self.settings.game_mode == self.settings.MODE_SNIPER:
            return "狙击模式"
        else:
            return "普通模式"
    
    def _get_difficulty_name(self):
        """获取当前难度名称"""
        if self.settings.game_difficulty == self.settings.DIFFICULTY_EASY:
            return "简单"
        elif self.settings.game_difficulty == self.settings.DIFFICULTY_NORMAL:
            return "普通"
        elif self.settings.game_difficulty == self.settings.DIFFICULTY_HARD:
            return "困难"
        elif self.settings.game_difficulty == self.settings.DIFFICULTY_EXPERT:
            return "专家"
        else:
            return "普通"