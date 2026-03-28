import sys
from time import sleep

import pygame
import random
"""
--------------------
|     __      __    |
|    |__| __ |__|   |
|      __|  |__     |
|     |   __   |    |
|     |__|  |__|    |
|___________________|
"""
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_bullet import AlienBullet
from button import Button
from scoreboard import Scoreboard
from instructions import Instructions
from boss import Boss
from sound_manager import SoundManager
from achievement import AchievementSystem
from achievement_display import AchievementDisplay
from sniper_scope import SniperScope
from shop import Shop


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化统计信息"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # 设置游戏引用
        self.settings.game = self

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion(外星人入侵)")

        #创建存储游戏统计信息的实例,并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #创建音效管理器
        self.sound_manager = SoundManager()

        #创建成就系统
        self.achievement_system = AchievementSystem(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()  # Boss精灵组

        #让游戏开始时处于非活动状态
        self.game_active = False
        #创建Play按钮
        self.play_button = Button(self, "Play")
        #创建模式选择按钮
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 2

        # 创建模式选择按钮
        self.normal_mode_button = Button(self, "普通模式", 150, 40, (100, 100, 100), (screen_center_x, screen_center_y + 50))
        self.powerups_mode_button = Button(self, "道具模式", 150, 40, (0, 150, 255), (screen_center_x, screen_center_y + 100))
        self.unlimited_mode_button = Button(self, "无限火力", 150, 40, (255, 100, 0), (screen_center_x, screen_center_y + 150))
        self.boss_mode_button = Button(self, "Boss模式", 150, 40, (255, 0, 100), (screen_center_x, screen_center_y + 200))
        self.entertainment_mode_button = Button(self, "娱乐模式", 150, 40, (255, 165, 0), (screen_center_x, screen_center_y + 250))

        self.easy_difficulty_button = Button(self, "简单", 100, 35, (100, 200, 100), (screen_center_x - 150, screen_center_y + 320))
        self.normal_difficulty_button = Button(self, "普通", 100, 35, (150, 150, 150), (screen_center_x - 50, screen_center_y + 320))
        self.hard_difficulty_button = Button(self, "困难", 100, 35, (255, 100, 100), (screen_center_x + 50, screen_center_y + 320))
        self.expert_difficulty_button = Button(self, "专家", 100, 35, (200, 50, 50), (screen_center_x + 150, screen_center_y + 320))

        self.instructions = Instructions(self)
        self.show_instructions = True

        self.achievement_display = AchievementDisplay(self)
        self.achievement_button = Button(self, "成就", 120, 40, (255, 215, 0), (80, 30))

        # 创建商店系统
        self.shop = Shop(self)
        self.shop_button = Button(self, "商店", 120, 40, (100, 200, 100), (220, 30))

        # 创建设置系统
        from settings_ui import SettingsUI
        self.settings_ui = SettingsUI(self)
        self.settings_button = Button(self, "设置", 120, 40, (0, 135, 0), (360, 30))
        self.show_settings = False
        
        # 创建统计信息按钮
        self.stats_button = Button(self, "统计", 120, 40, (0, 0, 255), (500, 30))
        self.show_stats = False

        # 显示娱乐模式标志
        self.show_entertainment = False

        # 创建娱乐模式按钮
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 2
        start_y = screen_center_y - 210

        self.sniper_button = Button(self, "狙击模式", 200, 60, (75, 0, 130), (screen_center_x, start_y))
        self.dodge_button = Button(self, "太空躲避陨石", 200, 60, (0, 150, 255), (screen_center_x, start_y + 70))
        self.shoot_button = Button(self, "太空射击练习", 200, 60, (0, 255, 0), (screen_center_x, start_y + 140))
        self.hangman_button = Button(self, "猜字母", 200, 60, (128, 0, 128), (screen_center_x, start_y + 210))
        self.pong_button = Button(self, "颠球", 200, 60, (255, 105, 180), (screen_center_x, start_y + 280))
        self.lander_button = Button(self, "飞船着陆", 200, 60, (0, 255, 255), (screen_center_x, start_y + 350))
        self.entertainment_back_button = Button(self, "返回", 120, 45, (200, 0, 0), (screen_center_x, start_y + 420))

        # 创建狙击模式瞄准镜
        self.sniper_scope = SniperScope(self)

        # 导入对象池
        from object_pool import BulletPool, AlienPool, AlienBulletPool

        # 创建对象池
        self.bullet_pool = BulletPool()
        self.alien_pool = AlienPool()
        self.alien_bullet_pool = AlienBulletPool()

        # 初始化图像缓存
        self._initialize_image_cache()

        # 缓存常用Surface，避免重复创建
        self._cache_surfaces()

        # 缓存字体，避免重复加载
        self._cache_fonts()

        # 创建外星舰队
        self._create_fleet()

        #扫射冷却计时器
        self.last_spread_shot_time = 0
        #护盾系统
        self.shield_active = False
        self.shield_end_time = 0
        self.last_shield_time = 0
        #时间冻结系统
        self.time_frozen = False
        self.freeze_end_time = 0
        self.last_freeze_time = 0
        #子弹冷却系统
        self.last_bullet_time = 0
        #关卡选择系统
        self.show_level_select = False
        self.selected_level = 1
        self.max_level = 10
        # 从游戏统计中获取最后关卡
        self.last_played_level = self.stats.last_level
        self.selected_level = self.last_played_level
        #闪电链系统
        self.last_lightning_time = 0
        #激光束系统
        self.last_laser_time = 0
        self.laser_active = False
        self.laser_end_time = 0
        #磁力场系统
        self.last_magnet_time = 0
        self.magnet_active = False
        self.magnet_end_time = 0
        #瞬移系统
        self.last_teleport_time = 0
        #核弹系统
        self.last_nuke_time = 0
        #生命恢复系统
        self.last_heal_time = 0
        self.heal_effect_active = False
        self.heal_effect_end_time = 0
        #加载不死图腾图片
        try:
            self.totem_image = pygame.image.load('nodind_modified.png')
            self.totem_image = pygame.transform.scale(self.totem_image, (60, 80))
        except:
            self.totem_image = None
        #缓慢时间系统
        self.last_slow_mo_time = 0
        self.slow_mo_active = False
        self.slow_mo_end_time = 0
        #分身系统
        self.last_clone_time = 0
        self.clone_active = False
        self.clone_end_time = 0
        self.clone_ship = None
        #护盾反射系统
        self.last_reflect_time = 0
        self.reflect_active = False
        self.reflect_end_time = 0
        #召唤支援系统
        self.last_summon_time = 0
        self.summon_active = False
        self.summon_end_time = 0
        self.summon_ships = []
        #成就通知系统
        self.achievement_notifications = []
        #得分通知系统
        self.score_notifications = []

    def run_game(self):
        """开始游戏的主循环"""
        # 预计算一些常用值
        frame_rate_limit = self.settings.frame_rate_limit
        enable_frame_limit = self.settings.enable_frame_rate_limit
        
        while True:
            # 处理事件
            self._check_events()

            if self.game_active:
                # 更新飞船位置
                self.ship.update()
                
                # 更新分身（如果激活）
                if self.clone_active and self.clone_ship:
                    self._update_clone()
                
                # 更新子弹
                self._update_bullets()
                
                # 更新外星人子弹
                self._update_alien_bullets()
                
                # 更新外星人
                self._update_aliens()

                # 每2帧检查一次成就，减少计算
                current_time = pygame.time.get_ticks()
                if current_time % 2 == 0:
                    newly_unlocked = self.achievement_system.check_achievements()
                    if newly_unlocked:
                        for achievement in newly_unlocked:
                            if self.achievement_notifications:
                                last_notif = self.achievement_notifications[-1]
                                delay_start = last_notif['start_time'] + last_notif['duration']
                            else:
                                delay_start = current_time

                            self.achievement_notifications.append({
                                'achievement': achievement,
                                'start_time': delay_start,
                                'duration': 3000
                            })
                            self.sound_manager.play_sound('powerup')
            
            # 渲染屏幕
            self._update_screen()
            
            # 更新游戏计时器
            if self.game_active:
                self.stats.update_game_timer()
            
            # 根据设置应用帧率锁定
            if enable_frame_limit:
                self.clock.tick(frame_rate_limit)
            else:
                self.clock.tick()  # 不限制帧率

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEMOTION:
                # 狙击模式下更新瞄准镜位置
                if self.game_active and self.settings.game_mode == self.settings.MODE_SNIPER:
                    mouse_pos = pygame.mouse.get_pos()
                    self.sniper_scope.update_position(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.show_level_select:
                    self._check_level_select(mouse_pos)
                elif self.show_instructions:
                    self.instructions.check_page_buttons(mouse_pos)
                    self._check_instructions_close(mouse_pos)
                elif self.achievement_display.show_achievements:
                    self.achievement_display.check_page_buttons(mouse_pos)
                    self.achievement_display.check_close_button(mouse_pos)
                elif self.shop.shop_active:
                    self.shop.handle_event(event)
                elif self.show_settings:
                    result = self.settings_ui.handle_event(event)
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
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.play_button.trigger_click()
            self.sound_manager.play_sound('button_click')
            self.show_level_select = True
            pygame.mouse.set_visible(True)

    def _check_mode_buttons(self, mouse_pos):
        if not self.game_active:
            if self.normal_mode_button.rect.collidepoint(mouse_pos):
                self.normal_mode_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_NORMAL
                self._apply_mode_settings()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.last_played_level = self.stats.last_level
                self.selected_level = self.last_played_level
            elif self.powerups_mode_button.rect.collidepoint(mouse_pos):
                self.powerups_mode_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_POWERUPS
                self._apply_mode_settings()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.last_played_level = self.stats.last_level
                self.selected_level = self.last_played_level
            elif self.unlimited_mode_button.rect.collidepoint(mouse_pos):
                self.unlimited_mode_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_UNLIMITED
                self._apply_mode_settings()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.last_played_level = self.stats.last_level
                self.selected_level = self.last_played_level
            elif self.boss_mode_button.rect.collidepoint(mouse_pos):
                self.boss_mode_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_mode = self.settings.MODE_BOSS
                self._apply_mode_settings()
                self.stats.reset_stats()
                self.sb.prep_score()
                self.sb.prep_high_score()
                self.selected_level = 1
            elif self.entertainment_mode_button.rect.collidepoint(mouse_pos):
                self.entertainment_mode_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.show_entertainment = True

    def _check_achievement_button(self, mouse_pos):
        if not self.game_active and self.achievement_button.rect.collidepoint(mouse_pos):
            self.achievement_button.trigger_click()
            self.sound_manager.play_sound('button_click')
            self.achievement_display.show_achievements = True
            self.achievement_display.current_page = 0

    def _check_shop_button(self, mouse_pos):
        if not self.game_active and self.shop_button.rect.collidepoint(mouse_pos):
            self.shop_button.trigger_click()
            self.sound_manager.play_sound('button_click')
            self.shop.shop_active = True

    def _check_settings_button(self, mouse_pos):
        if not self.game_active and self.settings_button.rect.collidepoint(mouse_pos):
            self.settings_button.trigger_click()
            self.sound_manager.play_sound('button_click')
            self.show_settings = True

    def _check_stats_button(self, mouse_pos):
        if not self.game_active and self.stats_button.rect.collidepoint(mouse_pos):
            self.stats_button.trigger_click()
            self.sound_manager.play_sound('button_click')
            self.show_stats = True

    def _check_difficulty_buttons(self, mouse_pos):
        if not self.game_active:
            if self.easy_difficulty_button.rect.collidepoint(mouse_pos):
                self.easy_difficulty_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_EASY
            elif self.normal_difficulty_button.rect.collidepoint(mouse_pos):
                self.normal_difficulty_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_NORMAL
            elif self.hard_difficulty_button.rect.collidepoint(mouse_pos):
                self.hard_difficulty_button.trigger_click()
                self.sound_manager.play_sound('button_click')
                self.settings.game_difficulty = self.settings.DIFFICULTY_HARD
            elif self.expert_difficulty_button.rect.collidepoint(mouse_pos):
                self.expert_difficulty_button.trigger_click()
                self.sound_manager.play_sound('button_click')
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
        if self.show_level_select:
            button_width = 70
            button_height = 70
            buttons_per_row = 5
            start_x = (self.settings.screen_width - (buttons_per_row * button_width + (buttons_per_row - 1) * 20)) // 2
            start_y = (self.settings.screen_height - (2 * button_height + 20)) // 2

            for level in range(1, self.max_level + 1):
                row = (level - 1) // buttons_per_row
                col = (level - 1) % buttons_per_row
                button_x = start_x + col * (button_width + 20)
                button_y = start_y + row * (button_height + 20)

                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                if button_rect.collidepoint(mouse_pos):
                    self.sound_manager.play_sound('button_click')
                    self.selected_level = level
                    self.show_level_select = False
                    self._start_game_with_level()
                    return

            continue_button_rect = pygame.Rect(
                self.settings.screen_width // 2 - 130,
                start_y + 2 * (button_height + 20) + 20,
                260,
                45
            )
            if continue_button_rect.collidepoint(mouse_pos):
                self.sound_manager.play_sound('button_click')
                self.selected_level = self.last_played_level + 1
                self.show_level_select = False
                self._start_game_with_level()
                return

            back_button_rect = pygame.Rect(
                self.settings.screen_width // 2 - 60,
                start_y + 2 * (button_height + 20) + 75,
                120,
                45
            )
            if back_button_rect.collidepoint(mouse_pos):
                self.sound_manager.play_sound('button_click')
                self.show_level_select = False
                return

    def _check_entertainment_options(self, mouse_pos):
        """检查娱乐模式选项的点击"""
        import subprocess

        if self.sniper_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            self.show_entertainment = False
            # 切换到狙击模式
            self.settings.game_mode = self.settings.MODE_SNIPER
            self._apply_mode_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.last_played_level = self.stats.last_level
            self.selected_level = self.last_played_level
        elif self.dodge_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            # 启动太空躲避陨石游戏
            subprocess.Popen(['python', 'game_1.py'])
        elif self.shoot_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            # 启动太空射击练习游戏
            subprocess.Popen(['python', 'game_2.py'])
        elif self.pong_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            # 启动颠球游戏
            subprocess.Popen(['python', 'PyPong.py'])
        elif self.lander_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            # 启动飞船着陆游戏
            subprocess.Popen(['python', 'LunarLander.py'])
        elif self.entertainment_back_button.rect.collidepoint(mouse_pos):
            self.sound_manager.play_sound('button_click')
            self.show_entertainment = False

    def _start_game_with_level(self):
        """开始指定关卡的游戏"""
        #开始游戏
        self.game_active = True

        # 先应用商店购买的皮肤（在重置设置之前）
        self.shop._apply_skin()

        #还原游戏设置
        self.settings.initialize_dynamic_settings()

        # 更新飞船皮肤
        self.ship.update_skin()

        #重置游戏的统计信息
        self.stats.reset_stats()
        self.stats.level = self.selected_level
        # 根据关卡调整游戏速度
        for _ in range(self.selected_level - 1):
            self.settings.increase_speed()
        
        # 启动游戏计时器
        self.stats.start_game_timer()

        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()

        #清空外星人列表和子弹列表
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.bosses.empty()
        self.clone_active = False
        self.clone_ship = None
        self.summon_active = False
        self.summon_ships = []

        #创建一个新的外星舰队,并将飞船放到屏幕底端的中央
        self._create_fleet()
        self.ship.center_ship()
        #隐藏光标
        pygame.mouse.set_visible(False)

        # 狙击模式显示瞄准镜
        if self.settings.game_mode == self.settings.MODE_SNIPER:
            self.sniper_scope.set_visible(True)

        # 播放背景音乐
        self.sound_manager.play_background_music()


    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._fire_spread_shot()
        elif event.key == pygame.K_1:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._activate_shield()
        elif event.key == pygame.K_2:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._freeze_time()
        elif event.key == pygame.K_3:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._lightning_chain()
        elif event.key == pygame.K_4:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._laser_beam()
        elif event.key == pygame.K_5:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._magnet_field()
        elif event.key == pygame.K_6:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._teleport()
        elif event.key == pygame.K_7:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._nuke()
        elif event.key == pygame.K_8:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._heal()
        elif event.key == pygame.K_9:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._slow_mo()
        elif event.key == pygame.K_0:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._clone()
        elif event.key == pygame.K_MINUS:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._activate_reflect()
        elif event.key == pygame.K_EQUALS:
            if self.game_active and self.settings.game_mode in [self.settings.MODE_POWERUPS, self.settings.MODE_UNLIMITED, self.settings.MODE_BOSS]:
                self._summon_support()


    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:

            # 狙击模式：子弹从飞船发射到准星位置
            if self.settings.game_mode == self.settings.MODE_SNIPER:
                scope_pos = self.sniper_scope.get_position()

                # 计算从飞船到准星的角度
                import math
                dx = scope_pos[0] - self.ship.rect.centerx
                dy = scope_pos[1] - self.ship.rect.centery
                angle = math.degrees(math.atan2(dx, -dy))

                # 从飞船位置创建子弹，指向准星
                new_bullet = self.bullet_pool.get(self, angle)
                self.bullets.add(new_bullet)
                self.sound_manager.play_sound('shoot')
                self.stats.record_sniper_shot()
                self.stats.record_shot_fired()
            else:
                # 其他模式：从飞船位置垂直向上发射子弹
                new_bullet = self.bullet_pool.get(self)
                self.bullets.add(new_bullet)
                self.sound_manager.play_sound('shoot')
                self.stats.record_shot_fired()

        # 如果分身激活，分身也发射子弹（狙击模式不使用分身）
        if self.clone_active and self.clone_ship and len(self.bullets) < self.settings.bullets_allowed and self.settings.game_mode != self.settings.MODE_SNIPER:
            # 创建分身的子弹
            clone_bullet = self.bullet_pool.get(self)
            # 修改子弹位置到分身飞船
            clone_bullet.rect.midtop = self.clone_ship.rect.midtop
            clone_bullet.y = float(clone_bullet.rect.y)
            clone_bullet.x = float(clone_bullet.rect.x)
            self.bullets.add(clone_bullet)
            self.stats.record_shot_fired()

        # 如果支援激活，支援飞船也发射子弹（狙击模式不使用支援）
        if self.summon_active and self.summon_ships and self.settings.game_mode != self.settings.MODE_SNIPER:
            for support_ship in self.summon_ships:
                if len(self.bullets) < self.settings.bullets_allowed:
                    support_bullet = self.bullet_pool.get(self)
                    support_bullet.rect.midtop = support_ship.rect.midtop
                    support_bullet.y = float(support_bullet.rect.y)
                    support_bullet.x = float(support_bullet.rect.x)
                    self.bullets.add(support_bullet)
                    self.stats.record_shot_fired()

    def _fire_spread_shot(self):
        """发射扫射（多方向子弹）"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spread_shot_time >= self.settings.spread_shot_cooldown:
            self.last_spread_shot_time = current_time

            # 计算起始角度（向左偏转）
            start_angle = -(self.settings.spread_shot_count - 1) * self.settings.spread_shot_angle / 2

            # 发射多颗子弹
            for i in range(self.settings.spread_shot_count):
                angle = start_angle + i * self.settings.spread_shot_angle
                new_bullet = self.bullet_pool.get(self, angle)
                self.bullets.add(new_bullet)

    def _activate_shield(self):
        """激活护盾"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shield_time >= self.settings.shield_cooldown:
            self.last_shield_time = current_time
            self.stats.shield_uses += 1
            self.shield_active = True
            self.shield_end_time = current_time + self.settings.shield_duration

    def _freeze_time(self):
        """冻结时间"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_freeze_time >= self.settings.freeze_cooldown:
            self.last_freeze_time = current_time
            self.stats.freeze_uses += 1
            self.time_frozen = True
            self.freeze_end_time = current_time + self.settings.freeze_duration

    def _lightning_chain(self):
        """闪电链 - 在多个外星人之间跳跃"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_lightning_time >= self.settings.lightning_cooldown and len(self.aliens) > 0:
            self.last_lightning_time = current_time

            # 找到离飞船最近的外星人作为起点
            closest_alien = None
            min_distance = float('inf')
            for alien in self.aliens:
                distance = ((alien.rect.centerx - self.ship.rect.centerx) ** 2 +
                           (alien.rect.centery - self.ship.rect.centery) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_alien = alien

            if closest_alien:
                # 闪电链跳跃
                current_alien = closest_alien
                for _ in range(self.settings.lightning_chain_count):
                    if current_alien in self.aliens:
                        self.stats.score += self.settings.alien_points
                        self.aliens.remove(current_alien)
                        self.alien_pool.recycle(current_alien)

                        # 找到下一个最近的外星人
                        next_alien = None
                        min_dist = float('inf')
                        for alien in self.aliens:
                            dist = ((alien.rect.centerx - current_alien.rect.centerx) ** 2 +
                                   (alien.rect.centery - current_alien.rect.centery) ** 2) ** 0.5
                            if dist < min_dist:
                                min_dist = dist
                                next_alien = alien
                        current_alien = next_alien
                    else:
                        break

                self.sb.prep_score()
                self.sb.check_high_score()

    def _laser_beam(self):
        """激光束 - 发射一道贯穿屏幕的激光"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_laser_time >= self.settings.laser_cooldown:
            self.last_laser_time = current_time
            self.laser_active = True
            self.laser_end_time = current_time + self.settings.laser_duration

            # 删除激光路径上的所有外星人
            laser_width = 20
            laser_rect = pygame.Rect(0, 0, laser_width, self.settings.screen_height)
            laser_rect.centerx = self.ship.rect.centerx

            aliens_hit = []
            for alien in self.aliens:
                if laser_rect.colliderect(alien.rect):
                    aliens_hit.append(alien)

            for alien in aliens_hit:
                self.stats.score += self.settings.alien_points
                self.aliens.remove(alien)
                self.alien_pool.recycle(alien)

            if aliens_hit:
                self.sb.prep_score()
                self.sb.check_high_score()

    def _magnet_field(self):
        """磁力场 - 吸引附近的外星人"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_magnet_time >= self.settings.magnet_cooldown:
            self.last_magnet_time = current_time
            self.magnet_active = True
            self.magnet_end_time = current_time + self.settings.magnet_duration

    def _teleport(self):
        """瞬移 - 随机移动到屏幕底部安全位置"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_teleport_time >= self.settings.teleport_cooldown:
            self.last_teleport_time = current_time

            # 随机选择一个新的x位置
            # 尝试最多10次找到安全位置
            for _ in range(10):
                new_x = random.randint(50, self.settings.screen_width - 50)
                # 检查新位置是否安全（没有外星人）
                safe = True
                for alien in self.aliens:
                    distance = abs(new_x - alien.rect.centerx)
                    if distance < 100:  # 100像素的安全距离
                        safe = False
                        break
                if safe:
                    break
            else:
                # 如果找不到安全位置，就使用屏幕中央
                new_x = self.settings.screen_width // 2

            self.ship.rect.centerx = new_x
            self.ship.rect.bottom = self.settings.screen_height - 10
            # 更新飞船的x属性
            self.ship.x = float(self.ship.rect.x)

    def _nuke(self):
        """核弹 - 清除屏幕上所有外星人,对Boss造成100点伤害"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_nuke_time >= self.settings.nuke_cooldown:
            self.last_nuke_time = current_time
            self.stats.nuke_uses += 1

            # 清除所有外星人并计算分数
            alien_count = len(self.aliens)
            self.stats.score += self.settings.alien_points * alien_count

            # 回收所有外星人为对象池
            for alien in self.aliens.copy():
                self.aliens.remove(alien)
                self.alien_pool.recycle(alien)

            # 对所有Boss造成100点伤害
            bosses_to_remove = []
            for boss in self.bosses:
                # 对Boss造成100点伤害
                if boss.take_damage(100):
                    # Boss被消灭
                    bosses_to_remove.append(boss)
                    self.stats.score += self.settings.alien_points * 10

            # 移除被消灭的Boss
            for boss in bosses_to_remove:
                boss.kill()

            self.sb.prep_score()
            self.sb.check_high_score()

            # 如果是Boss模式且所有Boss都被清除，完成关卡
            if self.settings.game_mode == self.settings.MODE_BOSS and not self.bosses:
                self._boss_level_complete()

    def _heal(self):
        """生命恢复 - 恢复一条生命"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_heal_time >= self.settings.heal_cooldown:
            self.last_heal_time = current_time

            if self.stats.ships_left < self.settings.ship_limit:
                self.stats.ships_left += 1
                self.sb.prep_ship()
                # 激活不死图腾效果
                self.heal_effect_active = True
                self.heal_effect_end_time = current_time + 2000  # 效果持续2秒

    def _slow_mo(self):
        """缓慢时间 - 减慢外星人移动速度"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_slow_mo_time >= self.settings.slow_mo_cooldown:
            self.last_slow_mo_time = current_time
            self.slow_mo_active = True
            self.slow_mo_end_time = current_time + self.settings.slow_mo_duration

    def _clone(self):
        """分身 - 创建一个飞船分身"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_clone_time >= self.settings.clone_cooldown:
            self.last_clone_time = current_time
            self.clone_active = True
            self.clone_end_time = current_time + self.settings.clone_duration
            # 创建分身飞船
            self.clone_ship = Ship(self)
            self.clone_ship.rect.centerx = self.ship.rect.centerx - 100
            if self.clone_ship.rect.left < 0:
                self.clone_ship.rect.left = 0
            self.clone_ship.x = float(self.clone_ship.rect.x)

    def _update_clone(self):
        """更新分身飞船的位置"""
        if self.clone_ship:
            # 计算目标位置，保持固定距离
            target_x = self.ship.rect.centerx - 100

            # 边界检查
            if target_x < 50:
                target_x = 50
            elif target_x > self.settings.screen_width - 50:
                target_x = self.settings.screen_width - 50

            # 平滑移动：使用缓动效果
            current_x = self.clone_ship.rect.centerx
            # 缓动因子，值越小移动越平滑
            easing_factor = 0.1

            # 计算新位置
            new_x = current_x + (target_x - current_x) * easing_factor

            # 更新分身飞船位置
            self.clone_ship.rect.centerx = new_x
            self.clone_ship.x = float(self.clone_ship.rect.x)

    def _activate_reflect(self):
        """激活护盾反射"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_reflect_time >= self.settings.reflect_cooldown:
            self.last_reflect_time = current_time
            self.reflect_active = True
            self.reflect_end_time = current_time + self.settings.reflect_duration

    def _summon_support(self):
        """召唤支援飞船"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_summon_time >= self.settings.summon_cooldown:
            self.last_summon_time = current_time
            self.summon_active = True
            self.summon_end_time = current_time + self.settings.summon_duration
            # 创建两艘支援飞船
            self.summon_ships = []
            for i in range(2):
                support_ship = Ship(self)
                support_ship.rect.centerx = self.settings.screen_width // 4 * (i + 1)
                support_ship.rect.bottom = self.settings.screen_height - 50
                support_ship.x = float(support_ship.rect.x)
                self.summon_ships.append(support_ship)

    def _add_score_notification(self, position, score):
        """添加得分通知"""
        self.score_notifications.append({
            'position': position,
            'score': score,
            'start_time': pygame.time.get_ticks(),
            'duration': 1500,
            'y_offset': 0
        })

    def _draw_score_notifications(self, current_time):
        """绘制得分通知"""
        # 更新并绘制得分通知
        updated_notifications = []
        for notification in self.score_notifications:
            # 计算通知的生命周期
            elapsed_time = current_time - notification['start_time']
            if elapsed_time < notification['duration']:
                # 更新y偏移量（向上浮动）
                notification['y_offset'] = -elapsed_time * 0.15

                # 计算透明度（逐渐消失）
                alpha = 255 - int((elapsed_time / notification['duration']) * 255)

                # 创建得分文本
                # 直接使用默认字体，因为得分通知中只有数字
                font = pygame.font.Font(None, 24)
                score_text = font.render(f"+{notification['score']}", True, (255, 255, 0))

                # 计算通知位置
                x = notification['position'][0] - score_text.get_width() // 2
                y = notification['position'][1] + notification['y_offset'] - score_text.get_height() // 2

                # 绘制发光效果
                glow_surface = pygame.Surface((score_text.get_width() + 10, score_text.get_height() + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 255, 0, alpha // 4), glow_surface.get_rect())
                glow_rect = glow_surface.get_rect(center=(x + score_text.get_width() // 2, y + score_text.get_height() // 2))
                self.screen.blit(glow_surface, glow_rect)

                # 绘制得分文本
                text_surface = score_text.copy()
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, (x, y))

                # 保留未过期的通知
                updated_notifications.append(notification)

        # 更新通知列表
        self.score_notifications = updated_notifications



    def _update_bullets(self):
        """更新子弹的位置"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除已消失的子弹（超出屏幕边界）
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom <= 0 or
                bullet.rect.top >= self.settings.screen_height or
                bullet.rect.right <= 0 or
                bullet.rect.left >= self.settings.screen_width):
                self.bullets.remove(bullet)
                self.bullet_pool.recycle(bullet)

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        """更新外星人子弹的位置"""
        # 更新外星人子弹的位置
        if self.time_frozen:
            # 时间冻结时，外星人子弹不移动
            pass
        elif self.slow_mo_active:
            # 缓慢时间时，外星人子弹速度减慢
            for bullet in self.alien_bullets:
                bullet.y += bullet.speed * self.settings.slow_mo_factor
                bullet.rect.y = bullet.y
        else:
            # 正常时间
            self.alien_bullets.update()

        # 删除已消失的外星人子弹
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.settings.screen_height:
                self.alien_bullets.remove(bullet)
                # 回收子弹到对象池
                self.alien_bullet_pool.recycle(bullet)

        # 检查外星人子弹和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            # 如果护盾反射激活，反射子弹
            if self.reflect_active:
                for bullet in self.alien_bullets.copy():
                    bullet.speed = -bullet.speed
                    bullet.rect.y = self.ship.rect.top - bullet.rect.height
            # 如果护盾未激活，飞船受损
            elif not self.shield_active:
                self._ship_hit()
            # 删除所有外星人子弹
            for bullet in self.alien_bullets:
                bullet.kill()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 检查子弹和Boss的碰撞
        if self.settings.game_mode == self.settings.MODE_BOSS:
            for boss in self.bosses:
                # 使用 False 不自动删除子弹，以便我们手动回收
                collisions = pygame.sprite.spritecollide(boss, self.bullets, False)
                if collisions:
                    # 记录子弹命中Boss
                    for _ in collisions:
                        self.stats.record_shot_hit()
                    # Boss受到伤害
                    for bullet in collisions:
                        if boss.take_damage():
                            # Boss被消灭
                            boss.kill()
                            self.stats.score += self.settings.alien_points * 10
                            self.stats.record_boss_defeat()
                            self.sb.prep_score()
                            self.sb.check_high_score()

                            # 检查是否通关
                            if not self.bosses:
                                self._boss_level_complete()
                            break
                        else:
                            # Boss受到伤害后检查是否需要躲避
                            if not boss.is_moving and boss.attack_count >= boss.max_attacks_before_dodge:
                                boss.dodge_bullet()

                    # 移除并回收子弹
                    for bullet in collisions:
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                            self.bullet_pool.recycle(bullet)

        # 检查子弹和外星人的碰撞
        # 使用 False 不自动删除子弹，以便我们手动回收
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, False)

        if collisions:
            aliens_to_remove = []
            bullets_to_remove = []

            for bullet, aliens in collisions.items():
                bullets_to_remove.append(bullet)
                # 记录子弹命中
                self.stats.record_shot_hit()
                for alien in aliens:
                    # 检查是否为爆炸型外星人
                    if alien.is_explosive:
                        self._trigger_explosion(alien)
                        aliens_to_remove.append(alien)
                    else:
                        # 检查外星人类型
                        if alien.alien_type == 'tank':
                            # 坦克型外星人需要多次攻击
                            if alien.take_damage(self.settings.bullet_damage):
                                aliens_to_remove.append(alien)
                                self.stats.score += self.settings.alien_points
                        else:
                            # 其他外星人一次攻击消灭
                            aliens_to_remove.append(alien)
                            self.stats.score += self.settings.alien_points

            # 移除并回收子弹
            for bullet in bullets_to_remove:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                    self.bullet_pool.recycle(bullet)

            # 移除被消灭的外星人
            for alien in aliens_to_remove:
                if alien in self.aliens:
                    self.aliens.remove(alien)
                    self.alien_pool.recycle(alien)
                    self.stats.record_kill()

                    # 狙击模式记录命中
                    if self.settings.game_mode == self.settings.MODE_SNIPER:
                        self.stats.record_sniper_hit()

                    # 添加得分通知
                    self._add_score_notification(alien.rect.center, self.settings.alien_points)

            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_level()
            self.sb.prep_currency()

        if not self.aliens and self.settings.game_mode != self.settings.MODE_BOSS:
            self.stats.save_last_level(self.stats.level)

            if self.settings.game_mode == self.settings.MODE_SNIPER:
                self.stats.record_sniper_level_complete()

            self.bullets.empty()
            self.clone_active = False
            self.clone_ship = None
            self.summon_active = False
            self.summon_ships = []
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.stats.update_max_level_reached(self.stats.level)
            self.stats.reset_level_stats()
            self.sb.prep_level()

    def _trigger_explosion(self, explosive_alien):
        """触发爆炸，清除范围内的外星人和飞船"""
        self.sound_manager.play_sound('explosion')
        explosion_center = explosive_alien.rect.center
        explosion_radius = self.settings.explosion_radius

        # 获取爆炸范围内的所有外星人
        aliens_in_range = []
        for alien in self.aliens:
            distance = ((alien.rect.centerx - explosion_center[0]) ** 2 +
                       (alien.rect.centery - explosion_center[1]) ** 2) ** 0.5
            if distance <= explosion_radius:
                aliens_in_range.append(alien)

        # 删除范围内的外星人
        for alien in aliens_in_range:
            if alien in self.aliens:
                self.stats.score += self.settings.alien_points
                self.aliens.remove(alien)
                self.alien_pool.recycle(alien)

        # 检查飞船是否在爆炸范围内
        ship_distance = ((self.ship.rect.centerx - explosion_center[0]) ** 2 +
                        (self.ship.rect.centery - explosion_center[1]) ** 2) ** 0.5
        if ship_distance <= explosion_radius:
            # 如果护盾未激活，飞船受损
            if not self.shield_active:
                self._ship_hit()

    def _update_aliens(self):
        """检查是否有外星人到达屏幕边缘,并更新外星舰队中所有外星人的位置"""
        current_time = pygame.time.get_ticks()

        # 统一检查所有时间状态
        self._check_time_based_states(current_time)

        # 如果时间冻结，外星人不移动
        if not self.time_frozen:
            # 应用磁力场效果
            if self.magnet_active:
                self._apply_magnet_effect()

            # 应用缓慢时间效果
            if self.slow_mo_active:
                self.check_fleet_edges()
                alien_speed = self.settings.alien_speed * self.settings.fleet_direction * self.settings.slow_mo_factor
                for alien in self.aliens:
                    alien.x += alien_speed
                    alien.rect.x = alien.x
            else:
                self.check_fleet_edges()
                self.aliens.update()

            # 处理特殊外星人的行为
            self._handle_special_alien_actions(current_time)

        # Boss模式的特殊处理
        if self.settings.game_mode == self.settings.MODE_BOSS:
            self._update_bosses(current_time)

        #检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # 如果护盾激活，则忽略碰撞
            if not self.shield_active:
                self._ship_hit()

        #检查是否有外星人到达屏幕的下边缘
        self._check_aliens_bottom()

    def _check_time_based_states(self, current_time):
        """统一检查所有基于时间的状态"""
        # 检查时间冻结状态
        if self.time_frozen and current_time >= self.freeze_end_time:
            self.time_frozen = False

        # 检查护盾状态
        if self.shield_active and current_time >= self.shield_end_time:
            self.shield_active = False

        # 检查激光束状态
        if self.laser_active and current_time >= self.laser_end_time:
            self.laser_active = False

        # 检查磁力场状态
        if self.magnet_active and current_time >= self.magnet_end_time:
            self.magnet_active = False

        # 检查缓慢时间状态
        if self.slow_mo_active and current_time >= self.slow_mo_end_time:
            self.slow_mo_active = False

        # 检查生命恢复效果状态
        if self.heal_effect_active and current_time >= self.heal_effect_end_time:
            self.heal_effect_active = False

        # 检查分身状态
        if self.clone_active and current_time >= self.clone_end_time:
            self.clone_active = False
            self.clone_ship = None

        # 检查护盾反射状态
        if self.reflect_active and current_time >= self.reflect_end_time:
            self.reflect_active = False

        # 检查召唤支援状态
        if self.summon_active and current_time >= self.summon_end_time:
            self.summon_active = False
            self.summon_ships = []

    def _apply_magnet_effect(self):
        """应用磁力场效果，优化距离计算"""
        aliens_to_remove = []
        ship_centerx = self.ship.rect.centerx
        ship_centery = self.ship.rect.centery
        magnet_radius_sq = self.settings.magnet_radius ** 2
        magnet_radius_2_sq = (self.settings.magnet_radius * 2) ** 2

        for alien in self.aliens:
            dx = ship_centerx - alien.rect.centerx
            dy = ship_centery - alien.rect.centery
            distance_sq = dx * dx + dy * dy

            # 使用平方比较替代平方根计算
            if distance_sq < magnet_radius_sq:
                # 进入磁力圈的外星人被杀死
                aliens_to_remove.append(alien)
            elif distance_sq < magnet_radius_2_sq and distance_sq > 0:
                # 吸引外圈的外星人
                distance = distance_sq ** 0.5  # 只在需要时计算平方根
                alien.rect.x += int(dx / distance * 3)
                alien.rect.y += int(dy / distance * 3)

        # 移除被磁力场杀死的外星人
        if aliens_to_remove:
            for alien in aliens_to_remove:
                if alien in self.aliens:
                    self.stats.score += self.settings.alien_points
                    self.aliens.remove(alien)
                    self.alien_pool.recycle(alien)

            self.sb.prep_score()
            self.sb.check_high_score()

    def _handle_special_alien_actions(self, current_time):
        """处理特殊外星人的特殊行为"""

        # 时间冻结时，外星人不执行任何行为
        if self.time_frozen:
            return

        # 预先计算缓慢时间因子
        slow_mo_factor = self.settings.slow_mo_factor if self.slow_mo_active else 1

        # 为每种外星人类型创建处理函数映射
        alien_action_map = {
            'splitter': self._split_alien,
            'tank': self._tank_fire,
            'healer': self._healer_heal,
            'stealth': self._stealth_toggle,
            'teleporter': self._teleporter_teleport
        }

        for alien in self.aliens:
            alien_type = alien.alien_type
            if alien_type in alien_action_map:
                # 计算实际冷却时间
                cooldown = int(alien.action_cooldown / slow_mo_factor)
                if current_time - alien.last_action_time >= cooldown:
                    alien.last_action_time = current_time
                    # 执行对应行为
                    alien_action_map[alien_type](alien)

    def _split_alien(self, splitter_alien):
        """分裂型外星人分裂出3个普通外星人"""
        # 限制最大外星人数目，避免游戏崩溃
        if len(self.aliens) >= 100:
            return

        # 获取当前外星人位置
        alien_width, alien_height = splitter_alien.rect.size

        # 计算可能的分裂位置（在分裂型外星人附近）
        possible_positions = []
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx == 0 and dy == 0:
                    continue
                new_x = splitter_alien.rect.x + dx * alien_width
                new_y = splitter_alien.rect.y + dy * alien_height

                # 检查位置是否在屏幕内且不与其他外星人重叠
                if (0 <= new_x <= self.settings.screen_width - alien_width and
                    0 <= new_y <= self.settings.screen_height - alien_height):
                    new_rect = pygame.Rect(new_x, new_y, alien_width, alien_height)
                    overlap = False
                    for other_alien in self.aliens:
                        if new_rect.colliderect(other_alien.rect):
                            overlap = True
                            break
                    if not overlap:
                        possible_positions.append((new_x, new_y))

        # 随机选择最多3个位置
        num_to_create = min(3, len(possible_positions))
        if num_to_create > 0:
            selected_positions = random.sample(possible_positions, num_to_create)
            for x, y in selected_positions:
                self._create_alien(x, y, False, 'normal')

    def _tank_fire(self, tank_alien):
        """坦克型外星人发射子弹攻击飞船"""
        # 限制外星人子弹数目，避免游戏卡顿
        if len(self.alien_bullets) >= 20:
            return

        # 从对象池获取外星人子弹
        alien_bullet = self.alien_bullet_pool.get(self, tank_alien)
        self.alien_bullets.add(alien_bullet)

    def _healer_heal(self, healer_alien):
        """治疗型外星人治疗坦克型外星人"""
        # 找到所有坦克型外星人
        tank_aliens = [alien for alien in self.aliens if alien.alien_type == 'tank']

        # 治疗所有坦克型外星人（恢复1点生命）
        for tank in tank_aliens:
            if tank.health < tank.max_health:
                tank.health = min(tank.health + 1, tank.max_health)

    def _stealth_toggle(self, stealth_alien):
        """隐形型外星人切换隐形状态"""
        stealth_alien.is_invisible = not stealth_alien.is_invisible
        # 隐形时设置透明度
        if stealth_alien.is_invisible:
            stealth_alien.image.set_alpha(50)
        else:
            stealth_alien.image.set_alpha(255)

    def _teleporter_teleport(self, teleporter_alien):
        """传送型外星人传送到新位置"""
        # 尝试最多10次找到新位置
        for _ in range(10):
            new_x = random.randint(0, self.settings.screen_width - 50)
            new_y = random.randint(0, self.settings.screen_height - 300)

            # 检查新位置是否安全（没有其他外星人）
            safe = True
            new_rect = pygame.Rect(new_x, new_y, 50, 50)
            for alien in self.aliens:
                if alien != teleporter_alien and new_rect.colliderect(alien.rect):
                    safe = False
                    break

            if safe:
                teleporter_alien.rect.x = new_x
                teleporter_alien.rect.y = new_y
                teleporter_alien.x = float(teleporter_alien.rect.x)
                return

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)

        # 如果显示关卡选择界面
        if self.show_level_select:
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
            title_font = self._load_chinese_font(size=64)
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
            title_font = self._load_chinese_font(size=64)
            title_text = title_font.render("游戏统计", True, (0, 0, 0))
            title_rect = title_text.get_rect()
            title_rect.centerx = self.settings.screen_width // 2
            title_rect.y = 50
            self.screen.blit(title_text, title_rect)

            # 关闭按钮
            close_font = self._load_chinese_font(size=24)
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
            stats_font = self._load_chinese_font(size=24)
            stats_texts = [
                f"总游戏时长: {self.stats.get_play_time_formatted()}",
                f"总击杀外星人: {self.stats.aliens_killed}",
                f"总击败Boss: {self.stats.bosses_defeated}",
                f"总发射子弹: {self.stats.total_shots_fired}",
                f"总命中子弹: {self.stats.total_shots_hit}",
                f"总命中率: {self.stats.get_hit_rate_formatted()}",
                f"总护盾使用: {self.stats.shield_uses}",
                f"总时间冻结使用: {self.stats.freeze_uses}",
                f"总核弹使用: {self.stats.nuke_uses}",
                f"总损失生命: {self.stats.total_lives_lost}",
                f"最高连击: {self.stats.max_combo}",
                f"最高关卡: {self.stats.max_level_reached}"
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
            # 如果时间冻结，绘制冻结效果
            if self.time_frozen:
                self.screen.blit(self._freeze_overlay, (0, 0))

            # 如果缓慢时间，绘制缓慢效果
            if self.slow_mo_active:
                self.screen.blit(self._slow_overlay, (0, 0))

            # 如果磁力场激活，绘制磁力场效果
            if self.magnet_active:
                magnet_rect = pygame.Rect(0, 0, self.settings.magnet_radius * 2, self.settings.magnet_radius * 2)
                magnet_rect.center = self.ship.rect.center
                pygame.draw.circle(self.screen, (150, 100, 255), magnet_rect.center, self.settings.magnet_radius, 2)
                pygame.draw.circle(self.screen, (150, 100, 255), magnet_rect.center, self.settings.magnet_radius - 20, 1)

            # 如果激光束激活，绘制激光束
            if self.laser_active:
                laser_rect = pygame.Rect(0, 0, 20, self.settings.screen_height)
                laser_rect.centerx = self.ship.rect.centerx
                pygame.draw.rect(self.screen, (255, 0, 0), laser_rect)
                pygame.draw.rect(self.screen, (255, 255, 0), laser_rect, 2)

            # 显示得分
            self.sb.show_score()

            #如果游戏处于非活动状态,就绘制Play按钮
            if not self.game_active:
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
                mode_font = self._load_chinese_font(size=36)
                mode_image = mode_font.render(mode_text, True, (0, 0, 0))
                mode_rect = mode_image.get_rect()
                mode_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 100)
                self.screen.blit(mode_image, mode_rect)

                difficulty_text = f"当前难度: {self._get_difficulty_name()}"
                difficulty_font = self._load_chinese_font(size=28)
                difficulty_image = difficulty_font.render(difficulty_text, True, (0, 0, 0))
                difficulty_rect = difficulty_image.get_rect()
                difficulty_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 60)
                self.screen.blit(difficulty_image, difficulty_rect)

                self._draw_menu_background()
            else:
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()

                # 绘制外星人子弹
                for bullet in self.alien_bullets.sprites():
                    self.screen.blit(bullet.image, bullet.rect)

                # 绘制飞船
                self.ship.blitme()

                # 狙击模式绘制瞄准镜
                if self.settings.game_mode == self.settings.MODE_SNIPER:
                    self.sniper_scope.draw()

                # 如果生命恢复效果激活，绘制不死图腾效果
                if self.heal_effect_active:
                    # 绘制金色光芒
                    glow_rect = pygame.Rect(0, 0, 120, 120)
                    glow_rect.center = self.ship.rect.center
                    # 创建渐变效果
                    for i in range(5):
                        radius = 60 - i * 10
                        alpha = 100 - i * 20
                        glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(glow_surface, (255, 215, 0, alpha), (radius, radius), radius)
                        glow_surface_rect = glow_surface.get_rect()
                        glow_surface_rect.center = self.ship.rect.center
                        self.screen.blit(glow_surface, glow_surface_rect)
                    # 绘制不死图腾图片
                    if self.totem_image:
                        totem_rect = self.totem_image.get_rect()
                        totem_rect.center = self.ship.rect.center
                        totem_rect.y -= 10
                        self.screen.blit(self.totem_image, totem_rect)
                    else:
                        # 绘制不死图腾符号（备用）
                        pygame.draw.polygon(self.screen, (255, 215, 0), [
                            (self.ship.rect.centerx, self.ship.rect.centery - 20),
                            (self.ship.rect.centerx + 15, self.ship.rect.centery + 10),
                            (self.ship.rect.centerx, self.ship.rect.centery + 5),
                            (self.ship.rect.centerx - 15, self.ship.rect.centery + 10)
                        ])
                        pygame.draw.circle(self.screen, (255, 215, 0),
                                         (self.ship.rect.centerx, self.ship.rect.centery), 8, 2)

                # 如果分身激活，绘制分身飞船
                if self.clone_active and self.clone_ship:
                    self.clone_ship.blitme()

                # 如果召唤支援激活，绘制支援飞船
                if self.summon_active and self.summon_ships:
                    for support_ship in self.summon_ships:
                        support_ship.blitme()

                # 如果护盾激活，绘制护盾效果
                if self.shield_active:
                    shield_rect = pygame.Rect(0, 0, 80, 80)
                    shield_rect.center = self.ship.rect.center
                    pygame.draw.circle(self.screen, (0, 200, 255), shield_rect.center, 40, 3)
                    pygame.draw.circle(self.screen, (0, 200, 255), shield_rect.center, 35, 2)

                # 如果护盾反射激活，绘制反射效果
                if self.reflect_active:
                    reflect_rect = pygame.Rect(0, 0, 100, 100)
                    reflect_rect.center = self.ship.rect.center
                    pygame.draw.circle(self.screen, (255, 255, 0), reflect_rect.center, 50, 3)
                    pygame.draw.circle(self.screen, (255, 200, 0), reflect_rect.center, 45, 2)
                    # 绘制反射箭头
                    for angle in range(0, 360, 45):
                        import math
                        rad = math.radians(angle)
                        start_x = reflect_rect.centerx + math.cos(rad) * 35
                        start_y = reflect_rect.centery + math.sin(rad) * 35
                        end_x = reflect_rect.centerx + math.cos(rad) * 50
                        end_y = reflect_rect.centery + math.sin(rad) * 50
                        pygame.draw.line(self.screen, (255, 255, 0), (start_x, start_y), (end_x, end_y), 2)

                # 绘制Boss
                for boss in self.bosses:
                    self.screen.blit(boss.image, boss.rect)
                    # 绘制Boss血条
                    boss.draw_health_bar()

                self.aliens.draw(self.screen)

            # 绘制版本和作者信息
            # 使用支持中文的字体，大小24
            version_font = self._load_chinese_font(size=24)
            version_text = version_font.render("版本:3.4.9", True, (0, 0, 0))
            author_text = version_font.render("作者:Systen32-mc | flb5   联合出品", True, (0, 0, 0))

            # 绘制到屏幕左下角，调整位置避免重叠
            version_rect = version_text.get_rect()
            version_rect.bottomleft = (20, self.settings.screen_height - 35)
            author_rect = author_text.get_rect()
            author_rect.bottomleft = (20, self.settings.screen_height - 10)

            self.screen.blit(version_text, version_rect)
            self.screen.blit(author_text, author_rect)

        # 绘制成就通知
        current_time = pygame.time.get_ticks()
        # 移除已过期的通知
        self.achievement_notifications = [
            notif for notif in self.achievement_notifications
            if current_time - notif['start_time'] < notif['duration']
        ]
        # 绘制剩余的通知
        for i, notif in enumerate(self.achievement_notifications):
            y_offset = i * 120
            self.achievement_system.draw_achievement_notification(
                self.screen,
                notif['achievement'],
                notif['duration'] - (current_time - notif['start_time']),
                y_offset
            )

        # 绘制得分通知
        self._draw_score_notifications(current_time)

        pygame.display.flip()

    def _get_mode_name(self):
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

    def _cache_surfaces(self):
        """缓存常用Surface，提高性能"""
        self._freeze_overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self._freeze_overlay.set_alpha(30)
        self._freeze_overlay.fill((0, 100, 255))

        self._slow_overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self._slow_overlay.set_alpha(20)
        self._slow_overlay.fill((100, 255, 100))

    def _initialize_image_cache(self):
        """初始化图像缓存，预加载所有游戏图像"""
        self.image_cache = {}

        # 预加载外星人图像
        alien_images = {
            'alien': 'alien.bmp',
            'alien_2': 'alien_2.bmp',  # 爆炸型
            'alien_3': 'alien_3.bmp',  # 快速型
            'alien_4': 'alien_4.bmp',  # 坦克型
            'alien_5': 'alien_5.bmp',  # 治疗型
            'alien_6': 'alien_6.bmp',  # 分裂型
            'alien_7': 'alien_7.bmp',  # 隐形型
            'alien_8': 'alien_8.bmp',  # 传送型
        }

        for name, path in alien_images.items():
            try:
                image = pygame.image.load(path)
                self.image_cache[name] = image
            except:
                # 如果加载失败，创建默认图像
                self.image_cache[name] = self._create_default_image(50, 50, (0, 255, 0))

        # 预加载飞船图像
        ship_images = {
            'ship': 'ship.bmp',
        }

        # 预加载飞船皮肤
        for i in range(1, 21):
            ship_images[f'ship_{i}'] = f'ship_{i}.bmp'

        for name, path in ship_images.items():
            try:
                image = pygame.image.load(path)
                self.image_cache[name] = image
            except:
                # 如果加载失败，使用默认飞船图像
                if name == 'ship':
                    self.image_cache[name] = self._create_default_image(60, 48, (255, 0, 0))
                else:
                    self.image_cache[name] = self.image_cache.get('ship', self._create_default_image(60, 48, (255, 0, 0)))

        # 预加载其他图像
        other_images = {
            'money': 'money.png',
            'nodind_modified': 'nodind_modified.png',
        }

        for name, path in other_images.items():
            try:
                image = pygame.image.load(path)
                self.image_cache[name] = image
            except:
                pass

        # 缓存缩放后的图像
        self._cache_scaled_images()

    def _create_default_image(self, width, height, color):
        """创建默认图像"""
        image = pygame.Surface((width, height))
        image.fill(color)
        return image

    def _cache_scaled_images(self):
        """缓存缩放后的图像"""
        # 缓存图腾图像
        if 'nodind_modified' in self.image_cache:
            self.totem_image = pygame.transform.scale(self.image_cache['nodind_modified'], (60, 80))
        else:
            self.totem_image = None

    def get_image(self, name, width=None, height=None):
        """
        从缓存获取图像，如果需要则缩放

        Args:
            name: 图像名称
            width: 目标宽度
            height: 目标高度

        Returns:
            图像Surface
        """
        if name not in self.image_cache:
            # 尝试加载图像
            try:
                path = f'{name}.bmp'
                image = pygame.image.load(path)
                self.image_cache[name] = image
            except:
                return self._create_default_image(50, 50, (255, 0, 255))

        image = self.image_cache[name]

        # 如果需要缩放
        if width and height:
            scaled_name = f'{name}_{width}x{height}'
            if scaled_name not in self.image_cache:
                scaled_image = pygame.transform.scale(image, (width, height))
                self.image_cache[scaled_name] = scaled_image
            return self.image_cache[scaled_name]

        return image

    def _cache_fonts(self):
        """缓存常用字体，提高性能"""
        self._font_cache = {}
        common_sizes = [24, 36]
        for size in common_sizes:
            self._font_cache[size] = self._load_chinese_font(size)

    def _load_chinese_font(self, size=36):
        """加载支持中文的字体（优先使用缓存）"""
        # 如果字体已缓存，直接返回
        if hasattr(self, '_font_cache') and size in self._font_cache:
            return self._font_cache[size]

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

    def _draw_menu_background(self):
        bg_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)

        for i in range(0, self.settings.screen_height, 4):
            alpha = int(5 * (1 - i / self.settings.screen_height))
            color = (100, 150, 255, alpha)
            pygame.draw.line(bg_surface, color, (0, i), (self.settings.screen_width, i))

        self.screen.blit(bg_surface, (0, 0))

        title_font = self._load_chinese_font(size=72)
        title_text = title_font.render("外星人入侵", True, (30, 30, 30))
        title_rect = title_text.get_rect()
        title_rect.center = (self.settings.screen_width // 2, 100)

        shadow_offset = 3
        shadow_surface = title_font.render("外星人入侵", True, (200, 200, 200))
        shadow_rect = shadow_surface.get_rect()
        shadow_rect.center = (title_rect.centerx + shadow_offset, title_rect.centery + shadow_offset)
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_text, title_rect)

        pygame.draw.line(self.screen, (100, 100, 100), (100, 160), (self.settings.screen_width - 100, 160), 2)

    def _create_fleet(self):
        """创建外星人舰队"""
        # Boss模式：创建Boss（如果不存在）
        if self.settings.game_mode == self.settings.MODE_BOSS:
            if len(self.bosses) == 0:
                self._create_boss(self.stats.level)
            return

        # 普通模式：创建外星人舰队
        # 创建一个外星人,再不断添加,直到没有空间容纳外星人为止
        # 外星人的间距为外星人的宽度和高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 记录所有外星人的位置
        alien_positions = []

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                alien_positions.append((current_x, current_y))
                current_x += 2 * alien_width

            # 添加一行外星人后,重置x值,并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

        # 根据关卡确定外星人类型分布
        level = self.stats.level

        # 定义不同关卡的外星人类型分布
        alien_types = ['normal']
        if level >= 3:
            alien_types.append('fast')
        if level >= 5:
            alien_types.append('tank')
        if level >= 7:
            alien_types.append('healer')
        if level >= 10:
            alien_types.append('splitter')
        if level >= 12:
            alien_types.append('stealth')
        if level >= 15:
            alien_types.append('teleporter')

        # 随机选择一些位置作为爆炸型外星人（1-3个）
        # 狙击模式下不创建爆炸外星人
        if self.settings.game_mode != self.settings.MODE_SNIPER:
            num_explosive = random.randint(1, min(3, len(alien_positions)))
            explosive_positions = random.sample(alien_positions, num_explosive)
            explosive_set = set(explosive_positions)
        else:
            explosive_set = set()

        # 为特殊类型外星人选择位置（每种1-3个）
        special_positions = {}
        remaining_positions = [pos for pos in alien_positions if pos not in explosive_set]

        if level >= 3:
            num_fast = random.randint(1, min(3, len(remaining_positions)))
            fast_positions = random.sample(remaining_positions, num_fast)
            special_positions['fast'] = set(fast_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in fast_positions]

        if level >= 5 and remaining_positions:
            num_tank = random.randint(1, min(3, len(remaining_positions)))
            tank_positions = random.sample(remaining_positions, num_tank)
            special_positions['tank'] = set(tank_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in tank_positions]

        if level >= 7 and remaining_positions:
            num_healer = random.randint(1, min(3, len(remaining_positions)))
            healer_positions = random.sample(remaining_positions, num_healer)
            special_positions['healer'] = set(healer_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in healer_positions]

        if level >= 10 and remaining_positions:
            num_splitter = random.randint(1, min(3, len(remaining_positions)))
            splitter_positions = random.sample(remaining_positions, num_splitter)
            special_positions['splitter'] = set(splitter_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in splitter_positions]

        if level >= 12 and remaining_positions:
            num_stealth = random.randint(1, min(2, len(remaining_positions)))
            stealth_positions = random.sample(remaining_positions, num_stealth)
            special_positions['stealth'] = set(stealth_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in stealth_positions]

        if level >= 15 and remaining_positions:
            num_teleporter = random.randint(1, min(2, len(remaining_positions)))
            teleporter_positions = random.sample(remaining_positions, num_teleporter)
            special_positions['teleporter'] = set(teleporter_positions)
            remaining_positions = [pos for pos in remaining_positions if pos not in teleporter_positions]

        # 创建所有外星人
        for x_position, y_position in alien_positions:
            is_explosive = (x_position, y_position) in explosive_set

            # 确定外星人类型
            alien_type = 'normal'
            if (x_position, y_position) in special_positions.get('fast', set()):
                alien_type = 'fast'
            elif (x_position, y_position) in special_positions.get('tank', set()):
                alien_type = 'tank'
            elif (x_position, y_position) in special_positions.get('healer', set()):
                alien_type = 'healer'
            elif (x_position, y_position) in special_positions.get('splitter', set()):
                alien_type = 'splitter'
            elif (x_position, y_position) in special_positions.get('stealth', set()):
                alien_type = 'stealth'
            elif (x_position, y_position) in special_positions.get('teleporter', set()):
                alien_type = 'teleporter'

            self._create_alien(x_position, y_position, is_explosive, alien_type)

    def _create_alien(self, x_position, y_position, is_explosive=False, alien_type='normal'):
        """创建一行外星人,并将其加入外星舰队"""
        new_alien = self.alien_pool.get(self, is_explosive, alien_type)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将外星舰队向下移动,并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        self.sound_manager.play_sound('ship_hit')
        #将ships_left减1并更新记分牌
        self.stats.ships_left -= 1
        self.stats.record_life_lost()
        self.sb.prep_ship()

        if self.stats.ships_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.clone_active = False
            self.clone_ship = None
            self.summon_active = False
            self.summon_ships = []

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.sound_manager.play_sound('game_over')
            self.game_active = False
            pygame.mouse.set_visible(True)
            if self.settings.game_mode == self.settings.MODE_SNIPER:
                self.sniper_scope.set_visible(False)
            self.clone_active = False
            self.clone_ship = None
            self.summon_active = False
            self.summon_ships = []
            self.achievement_system.save_achievements()


    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #像飞船被撞到一样处理
                self._ship_hit()
                break

    def _draw_level_select_screen(self):
        bg_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        for i in range(0, self.settings.screen_height, 6):
            alpha = int(8 * (1 - i / self.settings.screen_height))
            color = (150, 200, 255, alpha)
            pygame.draw.line(bg_surface, color, (0, i), (self.settings.screen_width, i))
        self.screen.blit(bg_surface, (0, 0))

        title_font = self._load_chinese_font(size=60)
        title_text = "选择关卡"
        title_surface = title_font.render(title_text, True, (30, 30, 30))
        title_rect = title_surface.get_rect()
        title_rect.center = (self.settings.screen_width // 2, 100)

        title_shadow = title_font.render(title_text, True, (200, 200, 200))
        title_shadow_rect = title_shadow.get_rect()
        title_shadow_rect.center = (title_rect.centerx + 3, title_rect.centery + 3)
        self.screen.blit(title_shadow, title_shadow_rect)
        self.screen.blit(title_surface, title_rect)

        pygame.draw.line(self.screen, (100, 100, 100), (150, 150), (self.settings.screen_width - 150, 150), 2)

        button_width = 70
        button_height = 70
        buttons_per_row = 5
        start_x = (self.settings.screen_width - (buttons_per_row * button_width + (buttons_per_row - 1) * 20)) // 2
        start_y = (self.settings.screen_height - (2 * button_height + 20)) // 2

        mouse_pos = pygame.mouse.get_pos()

        for level in range(1, self.max_level + 1):
            row = (level - 1) // buttons_per_row
            col = (level - 1) % buttons_per_row
            button_x = start_x + col * (button_width + 20)
            button_y = start_y + row * (button_height + 20)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            is_hovered = button_rect.collidepoint(mouse_pos)
            is_selected = (level == self.selected_level)

            if is_selected:
                bg_color = (0, 200, 255)
            elif is_hovered:
                bg_color = (100, 220, 255)
            else:
                bg_color = (220, 220, 220)

            shadow_rect = button_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(self.screen, (0, 0, 0, 80), shadow_rect, border_radius=10)

            pygame.draw.rect(self.screen, bg_color, button_rect, border_radius=10)

            border_color = (0, 150, 200) if is_selected else (150, 150, 150)
            border_width = 3 if is_selected else 2
            pygame.draw.rect(self.screen, border_color, button_rect, border_radius=10, width=border_width)

            level_font = self._load_chinese_font(size=32)
            text_color = (255, 255, 255) if is_selected else (30, 30, 30)
            level_surface = level_font.render(str(level), True, text_color)
            level_rect = level_surface.get_rect()
            level_rect.center = button_rect.center
            self.screen.blit(level_surface, level_rect)

        continue_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 130,
            start_y + 2 * (button_height + 20) + 20,
            260,
            45
        )
        continue_hovered = continue_button_rect.collidepoint(mouse_pos)

        continue_shadow = continue_button_rect.copy()
        continue_shadow.x += 3
        continue_shadow.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 80), continue_shadow, border_radius=8)

        continue_bg_color = (60, 180, 60) if continue_hovered else (50, 150, 50)
        pygame.draw.rect(self.screen, continue_bg_color, continue_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (40, 130, 40), continue_button_rect, border_radius=8, width=2)

        continue_font = self._load_chinese_font(size=28)
        continue_surface = continue_font.render("继续以前的关卡", True, (0, 0, 0))
        continue_rect = continue_surface.get_rect()
        continue_rect.center = continue_button_rect.center
        self.screen.blit(continue_surface, continue_rect)

        back_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 60,
            start_y + 2 * (button_height + 20) + 75,
            120,
            45
        )
        back_hovered = back_button_rect.collidepoint(mouse_pos)

        back_shadow = back_button_rect.copy()
        back_shadow.x += 3
        back_shadow.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 80), back_shadow, border_radius=8)

        back_bg_color = (220, 60, 60) if back_hovered else (200, 50, 50)
        pygame.draw.rect(self.screen, back_bg_color, back_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (180, 40, 40), back_button_rect, border_radius=8, width=2)

        back_font = self._load_chinese_font(size=28)
        back_surface = back_font.render("返回", True, (0, 0, 0))
        back_rect = back_surface.get_rect()
        back_rect.center = back_button_rect.center
        self.screen.blit(back_surface, back_rect)

        pygame.display.flip()

    def _create_boss(self, boss_level):
        """创建指定等级的Boss"""
        boss = Boss(self, boss_level)
        self.bosses.add(boss)

    def _update_bosses(self, current_time):
        """更新Boss状态和行为"""
        for boss in self.bosses:
            # 更新Boss位置（时间冻结时不移动）
            if not self.time_frozen:
                boss.update()

            # Boss发射子弹（时间冻结时不发射，有储备才发射）
            if not self.time_frozen and boss.bullet_reserve > 0 and boss.check_fire(current_time):
                self._boss_fire(boss)
                boss.fire()
                boss.bullet_reserve -= 1

            # Boss生成外星人（时间冻结时不生成，有储备才生成）
            if not self.time_frozen and boss.alien_reserve > 0 and boss.check_spawn_alien(current_time):
                self._boss_spawn_alien(boss)
                boss.spawn_alien()
                boss.alien_reserve -= 1

            # 检查Boss是否到达底部
            if boss.rect.bottom >= self.settings.screen_height:
                self._ship_hit()

    def _boss_fire(self, boss):
        """Boss发射子弹"""
        # 创建Boss子弹
        boss_bullet = AlienBullet(self, boss)
        self.alien_bullets.add(boss_bullet)

    def _boss_spawn_alien(self, boss):
        """Boss在面前生成随机类型的外星人"""
        # 限制外星人数量
        if len(self.aliens) >= 20:
            return

        # 在Boss前方生成外星人
        alien_width, alien_height = 50, 50

        # 随机选择外星人类型
        alien_types = ['normal', 'fast', 'tank', 'healer', 'splitter']
        alien_type = random.choice(alien_types)

        # 在Boss前方随机位置生成
        spawn_x = random.randint(max(0, boss.rect.centerx - 100),
                                  min(self.settings.screen_width - alien_width, boss.rect.centerx + 100))
        spawn_y = boss.rect.bottom + 10

        self._create_alien(spawn_x, spawn_y, False, alien_type)

    def _boss_level_complete(self):
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.clone_active = False
        self.clone_ship = None
        self.summon_active = False
        self.summon_ships = []

        if self.stats.level >= self.settings.boss_total_levels:
            self.game_active = False
        else:
            self.stats.level += 1
            # 更新实际通关的最高关卡（用于成就系统）
            self.stats.update_max_level_reached(self.stats.level)
            self.sb.prep_level()
            # 创建下一关的Boss
            self._create_boss(self.stats.level)

if __name__ == "__main__":
    """创建游戏实例并运行游戏"""
    ai = AlienInvasion()
    ai.run_game()