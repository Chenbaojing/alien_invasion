import json

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        
        # 先加载数据
        #从文件中加载最高分
        self.high_scores = self._load_high_scores()
        # 从文件中加载最后关卡
        self.last_levels = self._load_last_levels()
        # 从文件加载最高通关关卡
        max_level_data = self._load_max_level_reached()
        self.max_level_reached = max_level_data.get(self.settings.game_mode, 1)
        
        # 然后重置统计信息
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.high_score = self.high_scores.get(self.settings.game_mode, 0)
        self.last_level = self.last_levels.get(self.settings.game_mode, 1)
        
        self.aliens_killed = 0
        self.bosses_defeated = 0
        self.shield_uses = 0
        self.freeze_uses = 0
        self.nuke_uses = 0
        self.lives_lost_this_level = 0
        self.total_lives_lost = 0
        self.max_combo = 0
        self.current_combo = 0
        self.last_kill_time = 0
        self.sniper_shots_fired = 0
        self.sniper_shots_hit = 0
        self.sniper_perfect_rounds = 0
        self.sniper_levels_completed = 0
        self.current_level_perfect = True
        self.currency = self._load_currency()
        
        # 新增统计指标
        self.game_start_time = 0  # 游戏开始时间
        self.total_play_time = self._load_total_play_time()  # 总游戏时长（毫秒）
        self.total_shots_fired = 0  # 总发射子弹数
        self.total_shots_hit = 0  # 总命中子弹数
        self.session_shots_fired = 0  # 当前局发射子弹数
        self.session_shots_hit = 0  # 当前局命中子弹数
        self.bullets_used = 0  # 消耗子弹数
        self.damage_dealt = 0  # 造成伤害总量
        
    def _load_high_scores(self):
        """从文件中加载最高分"""
        try:
            with open('personal information/high_score.json', 'r') as f:
                data = json.load(f)
                # 确保返回的是字典格式
                result = {
                    self.settings.MODE_NORMAL: 0,
                    self.settings.MODE_POWERUPS: 0,
                    self.settings.MODE_UNLIMITED: 0,
                    self.settings.MODE_BOSS: 0
                }
                
                if isinstance(data, dict):
                    # 处理字符串键
                    for key, value in data.items():
                        if key in result:
                            result[key] = value
                        elif isinstance(key, str):
                            # 尝试转换字符串键
                            key_lower = key.lower()
                            if key_lower == '0' or key_lower == 'normal':
                                result[self.settings.MODE_NORMAL] = value
                            elif key_lower == '1' or key_lower == 'powerups':
                                result[self.settings.MODE_POWERUPS] = value
                            elif key_lower == '2' or key_lower == 'unlimited':
                                result[self.settings.MODE_UNLIMITED] = value
                elif isinstance(data, (int, float)):
                    # 如果是旧格式（单个值），转换为新格式
                    result[self.settings.MODE_NORMAL] = data
                
                return result
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                self.settings.MODE_NORMAL: 0,
                self.settings.MODE_POWERUPS: 0,
                self.settings.MODE_UNLIMITED: 0,
                self.settings.MODE_BOSS: 0
            }
            
    def save_high_score(self):
        """将最高分保存到文件中"""
        # 更新当前模式的最高分
        if self.score > self.high_scores.get(self.settings.game_mode, 0):
            self.high_scores[self.settings.game_mode] = self.score
            self.high_score = self.score
        
        with open('personal information/high_score.json', 'w') as f:
            json.dump(self.high_scores, f)
            
    def update_high_score(self):
        """更新最高分"""
        if self.score > self.high_scores.get(self.settings.game_mode, 0):
            self.high_scores[self.settings.game_mode] = self.score
            self.high_score = self.score
            self.save_high_score()
    
    def _load_last_levels(self):
        """从文件中加载最后玩的关卡"""
        try:
            with open('personal information/last_level.json', 'r') as f:
                data = json.load(f)
                # 确保返回的是字典格式，并处理各种类型的键
                result = {
                    self.settings.MODE_NORMAL: 1,
                    self.settings.MODE_POWERUPS: 1,
                    self.settings.MODE_UNLIMITED: 1,
                    self.settings.MODE_BOSS: 1
                }
                
                if isinstance(data, dict):
                    # 处理字符串键
                    for key, value in data.items():
                        if key in result:
                            result[key] = value
                        elif isinstance(key, str):
                            # 尝试转换字符串键
                            key_lower = key.lower()
                            if key_lower == 'normal' or key_lower == '0':
                                result[self.settings.MODE_NORMAL] = value
                            elif key_lower == 'powerups' or key_lower == '1':
                                result[self.settings.MODE_POWERUPS] = value
                            elif key_lower == 'unlimited' or key_lower == '2':
                                result[self.settings.MODE_UNLIMITED] = value
                elif isinstance(data, (int, float)):
                    # 如果是旧格式（单个值），转换为新格式
                    result[self.settings.MODE_NORMAL] = int(data)
                
                return result
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                self.settings.MODE_NORMAL: 1,
                self.settings.MODE_POWERUPS: 1,
                self.settings.MODE_UNLIMITED: 1,
                self.settings.MODE_BOSS: 1
            }
            
    def save_last_level(self, level):
        """将最后玩的关卡保存到文件中"""
        # 更新当前模式的最后关卡
        self.last_levels[self.settings.game_mode] = level
        self.last_level = level
        
        with open('personal information/last_level.json', 'w') as f:
            json.dump(self.last_levels, f)
    
    def update_max_level_reached(self, level):
        """更新实际通关的最高关卡（用于成就系统）"""
        if level > self.max_level_reached:
            self.max_level_reached = level
            self._save_max_level_reached()
    
    def _save_max_level_reached(self):
        """保存最高通关关卡到文件"""
        try:
            data = {
                'normal': self.max_level_reached if self.settings.game_mode == self.settings.MODE_NORMAL else self._load_max_level_reached().get('normal', 1),
                'powerups': self.max_level_reached if self.settings.game_mode == self.settings.MODE_POWERUPS else self._load_max_level_reached().get('powerups', 1),
                'unlimited': self.max_level_reached if self.settings.game_mode == self.settings.MODE_UNLIMITED else self._load_max_level_reached().get('unlimited', 1),
                'boss': self.max_level_reached if self.settings.game_mode == self.settings.MODE_BOSS else self._load_max_level_reached().get('boss', 1)
            }
            with open('personal information/max_level_reached.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            pass
    
    def _load_max_level_reached(self):
        """从文件加载最高通关关卡"""
        try:
            with open('personal information/max_level_reached.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def record_kill(self):
        """记录击杀，更新连击"""
        import pygame
        current_time = pygame.time.get_ticks()
        
        # 如果距离上次击杀不超过2秒，增加连击
        if current_time - self.last_kill_time <= 2000:
            self.current_combo += 1
        else:
            self.current_combo = 1
        
        # 更新最大连击
        if self.current_combo > self.max_combo:
            self.max_combo = self.current_combo
        
        self.last_kill_time = current_time
        self.aliens_killed += 1
        
        # 每击杀10个外星人获得1个货币
        if self.aliens_killed % 10 == 0:
            self.add_currency(1)
    
    def record_boss_defeat(self):
        """记录Boss击败"""
        self.bosses_defeated += 1
    
    def record_sniper_shot(self):
        """记录狙击模式发射子弹"""
        self.sniper_shots_fired += 1
    
    def record_sniper_hit(self):
        """记录狙击模式命中"""
        self.sniper_shots_hit += 1
    
    def record_sniper_level_complete(self):
        """记录狙击模式关卡完成"""
        self.sniper_levels_completed += 1
        if self.current_level_perfect:
            self.sniper_perfect_rounds += 1
    
    def record_life_lost(self):
        """记录生命损失"""
        self.lives_lost_this_level += 1
        self.total_lives_lost += 1
        self.current_level_perfect = False  # 损失生命后不再完美
    
    def reset_level_stats(self):
        """重置关卡统计"""
        self.lives_lost_this_level = 0
        self.current_level_perfect = True  # 标记当前关卡是否完美
    
    def _load_currency(self):
        """从文件中加载游戏货币"""
        try:
            with open('personal information/currency.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, int) else 0
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
    
    def save_currency(self):
        """保存游戏货币到文件"""
        with open('personal information/currency.json', 'w') as f:
            json.dump(self.currency, f)
    
    def add_currency(self, amount):
        """添加游戏货币"""
        self.currency += amount
        self.save_currency()
    
    def spend_currency(self, amount):
        """消费游戏货币，返回是否成功"""
        if self.currency >= amount:
            self.currency -= amount
            self.save_currency()
            return True
        return False
    
    def _load_total_play_time(self):
        """从文件中加载总游戏时长"""
        try:
            with open('personal information/total_play_time.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, int) else 0
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
    
    def save_total_play_time(self):
        """保存总游戏时长到文件"""
        with open('personal information/total_play_time.json', 'w') as f:
            json.dump(self.total_play_time, f)
    
    def start_game_timer(self):
        """开始游戏计时"""
        import pygame
        self.game_start_time = pygame.time.get_ticks()
    
    def update_game_timer(self):
        """更新游戏时长"""
        import pygame
        if self.game_start_time > 0:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.game_start_time
            self.total_play_time += elapsed
            self.game_start_time = current_time
            self.save_total_play_time()
    
    def get_play_time_formatted(self):
        """获取格式化的游戏时长"""
        total_seconds = self.total_play_time // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def record_shot_fired(self):
        """记录发射子弹"""
        self.total_shots_fired += 1
        self.session_shots_fired += 1
        self.bullets_used += 1
    
    def record_shot_hit(self):
        """记录子弹命中"""
        self.total_shots_hit += 1
        self.session_shots_hit += 1
    
    def record_damage(self, damage):
        """记录造成伤害"""
        self.damage_dealt += damage
    
    def get_hit_rate(self, session_only=False):
        """获取命中率"""
        if session_only:
            shots_fired = self.session_shots_fired
            shots_hit = self.session_shots_hit
        else:
            shots_fired = self.total_shots_fired
            shots_hit = self.total_shots_hit
        
        if shots_fired == 0:
            return 0.0
        return shots_hit / shots_fired * 100
    
    def get_hit_rate_formatted(self, session_only=False):
        """获取格式化的命中率"""
        return f"{self.get_hit_rate(session_only):.1f}%"
