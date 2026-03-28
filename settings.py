class Settings:
    MODE_NORMAL = "normal"
    MODE_POWERUPS = "powerups"
    MODE_UNLIMITED = "unlimited"
    MODE_BOSS = "boss"
    MODE_SNIPER = "sniper"
    
    DIFFICULTY_EASY = "easy"
    DIFFICULTY_NORMAL = "normal"
    DIFFICULTY_HARD = "hard"
    DIFFICULTY_EXPERT = "expert"

    def __init__(self, game=None):
        self.game = game
        self.game_mode = self.MODE_NORMAL
        self.game_difficulty = self.DIFFICULTY_NORMAL
        
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # 飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.ship_image = "ship.bmp"  # 默认飞船图像
        
        # 子弹设置
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10
        self.bullet_damage = 1  # 子弹伤害
        self.bullet_cooldown = 300  # 子弹冷却时间(毫秒)

        # 扫射设置
        self.spread_shot_cooldown = 10000  # 扫射冷却时间(毫秒)
        self.spread_shot_count = 5  # 扫射子弹数量
        self.spread_shot_angle = 15  # 扫射子弹间隔角度

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 3
        # fleet_direction为1表示向右移动,为-1表示向左移动
        self.fleet_direction = 1

        # 爆炸型外星人设置
        self.explosive_aliens_per_fleet = 2  # 每个舰队中爆炸型外星人的数量
        self.explosion_radius = 150  # 爆炸半径（像素），覆盖3x3到5x5区域

        # 护盾设置
        self.shield_duration = 5000  # 护盾持续时间(毫秒)
        self.shield_cooldown = 15000  # 护盾冷却时间(毫秒)

        # 时间冻结设置
        self.freeze_duration = 3000  # 冻结持续时间(毫秒)
        self.freeze_cooldown = 20000  # 冻结冷却时间(毫秒)

        # 闪电链设置（按键3）
        self.lightning_cooldown = 25000  # 闪电链冷却时间(毫秒)
        self.lightning_chain_count = 5  # 闪电链跳跃次数
        self.lightning_damage = 100  # 闪电链伤害

        # 激光束设置（按键4）
        self.laser_cooldown = 30000  # 激光束冷却时间(毫秒)
        self.laser_duration = 500  # 激光束持续时间(毫秒)

        # 磁力场设置（按键5）
        self.magnet_cooldown = 20000  # 磁力场冷却时间(毫秒)
        self.magnet_duration = 4000  # 磁力场持续时间(毫秒)
        self.magnet_radius = 200  # 磁力场半径

        # 瞬移设置（按键6）
        self.teleport_cooldown = 15000  # 瞬移冷却时间(毫秒)

        # 核弹设置（按键7）
        self.nuke_cooldown = 60000  # 核弹冷却时间(毫秒)

        # 生命恢复设置（按键8）
        self.heal_cooldown = 45000  # 生命恢复冷却时间(毫秒)

        # 缓慢时间设置（按键9）
        self.slow_mo_cooldown = 25000  # 缓慢时间冷却时间(毫秒)
        self.slow_mo_duration = 5000  # 缓慢时间持续时间(毫秒)
        self.slow_mo_factor = 0.3  # 缓慢时间速度因子

        # 分身设置（按键0）
        self.clone_cooldown = 35000  # 分身冷却时间(毫秒)
        self.clone_duration = 8000  # 分身持续时间(毫秒)

        # 护盾反射设置（按键-）
        self.reflect_cooldown = 40000  # 护盾反射冷却时间(毫秒)
        self.reflect_duration = 5000  # 护盾反射持续时间(毫秒)

        # 召唤支援设置（按键=）
        self.summon_cooldown = 50000  # 召唤支援冷却时间(毫秒)
        self.summon_duration = 10000  # 召唤支援持续时间(毫秒)

        # Boss模式设置
        self.boss_total_levels = 5  # Boss模式总关卡数
        self.boss_base_health = 200  # Boss基础血量
        self.boss_health_multiplier = 1.5  # 每关血量增长倍数
        self.boss_base_size = 80  # Boss基础大小
        self.boss_size_increment = 20  # 每关Boss大小增量
        self.boss_base_speed = 0.09  # Boss基础移动速度
        self.boss_speed_increment = 0.01  # 每关Boss速度增量
        self.boss_base_fire_cooldown = 2000  # Boss基础攻击冷却(毫秒)
        self.boss_fire_cooldown_decrease = 200  # 每关攻击冷却减少量(毫秒)
        self.boss_spawn_cooldown = 10000  # Boss生成外星人间隔(毫秒)
        self.boss_move_delay = 600000  # Boss移动延迟(毫秒，10分钟)
        
        # 帧率设置
        self.frame_rate_limit = 60  # 帧率锁定值
        self.enable_frame_rate_limit = True  # 是否启用帧率锁定

        # 难度增长设置
        self.cooldown_increase = 500  # 每关增加的冷却时间(毫秒)

        #以什么速度加快游戏节奏
        self.speedup_scale = 1.03
        #外星人分数的提高速度
        self.score_scale = 1.5
        # 速度上限（防止后期过于困难）
        self.max_alien_speed = 50.0

        self.initialize_dynamic_settings()
        

    def initialize_dynamic_settings(self):
        # 保存当前皮肤设置
        current_ship_image = getattr(self, 'ship_image', 'ship.bmp')
        
        self.ship_speed = 1.5
        self.alien_speed = 1.0
        
        difficulty_multiplier = self._get_difficulty_multiplier()
        
        if self.game_mode == self.MODE_SNIPER:
            self.bullet_speed = 10.0
            self.bullet_width = 2
            self.bullet_height = 30
            self.bullet_color = (255, 100, 0)
        else:
            self.bullet_speed = 2.5 * difficulty_multiplier['bullet_speed']
            self.bullet_width = 3
            self.bullet_height = 15
            self.bullet_color = (60, 60, 60)
        
        self.ship_speed *= difficulty_multiplier['ship_speed']
        self.alien_speed *= difficulty_multiplier['alien_speed']
        self.fleet_direction = 1
        self.alien_points = int(50 * difficulty_multiplier['score'])
        
        # 恢复皮肤设置
        self.ship_image = current_ship_image
    
    def _get_difficulty_multiplier(self):
        if self.game_difficulty == self.DIFFICULTY_EASY:
            return {
                'ship_speed': 1.2,
                'alien_speed': 0.7,
                'bullet_speed': 1.0,
                'score': 0.8
            }
        elif self.game_difficulty == self.DIFFICULTY_HARD:
            return {
                'ship_speed': 0.9,
                'alien_speed': 1.3,
                'bullet_speed': 1.0,
                'score': 1.2
            }
        elif self.game_difficulty == self.DIFFICULTY_EXPERT:
            return {
                'ship_speed': 0.8,
                'alien_speed': 1.5,
                'bullet_speed': 0.9,
                'score': 1.5
            }
        else:
            return {
                'ship_speed': 1.0,
                'alien_speed': 1.0,
                'bullet_speed': 1.0,
                'score': 1.0
            }
    
    def increase_speed(self):
        """提高速度设置的值和外星人分数"""
        self.ship_speed *= self.speedup_scale
        
        # 非狙击模式下才提高子弹速度
        if self.game_mode != self.MODE_SNIPER:
            self.bullet_speed *= self.speedup_scale
            
        self.alien_speed *= self.speedup_scale
        
        # 限制速度上限
        self.alien_speed = min(self.alien_speed, self.max_alien_speed)

# 外星人分数固定为50分，不随关卡提升
# self.alien_points = int(self.alien_points * self.score_scale)
