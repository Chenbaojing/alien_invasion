import pygame
import json
import os
from datetime import datetime, timedelta

class BattlePassReward:
    """高级通行证奖励类"""
    def __init__(self, reward_id, name, description, reward_type, value, is_premium=False):
        self.reward_id = reward_id
        self.name = name
        self.description = description
        self.reward_type = reward_type  # 'currency', 'skin', 'upgrade', 'powerup'
        self.value = value
        self.is_premium = is_premium
        self.claimed = False

class BattlePassTask:
    """高级通行证任务类"""
    def __init__(self, task_id, name, description, task_type, target, experience_reward, is_daily=False):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.task_type = task_type  # 'kill', 'score', 'level', 'boss', 'sniper'
        self.target = target
        self.current = 0
        self.experience_reward = experience_reward
        self.is_daily = is_daily
        self.completed = False
        self.claimed = False

class BattlePassLevel:
    """高级通行证等级类"""
    def __init__(self, level, required_experience):
        self.level = level
        self.required_experience = required_experience
        self.rewards = []
        self.experience_gained = 0
    
    def add_reward(self, reward):
        """添加奖励"""
        self.rewards.append(reward)
    
    def get_progress(self):
        """获取当前等级的进度"""
        return min(1.0, self.experience_gained / self.required_experience)



class BattlePass:
    """高级通行证系统主类"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.pass_active = False
        self.premium_unlocked = False
        self.current_level = 1
        self.total_experience = 0
        self.pass_season = "Season 1"
        self.season_end_date = None
        
        self.levels = []
        self.tasks = []
        self.daily_tasks = []
        
        # 动画相关属性
        self.animation_progress = 0.0
        self.animation_duration = 500  # 动画持续时间（毫秒）
        self.last_update_time = 0
        self.level_up_animation = False
        self.level_up_timer = 0
        self.level_up_duration = 2000  # 等级提升动画持续时间
        
        # 粒子特效
        self.particles = []
        
        # 按钮悬停效果
        self.hovered_button = None
        
        # 赛季主题系统
        self.season_themes = self._define_season_themes()
        self.current_theme = self.season_themes.get(self.pass_season, self.season_themes["default"])
        
        # 初始化通行证数据
        self._initialize_battle_pass()
        
        # 加载通行证数据
        self._load_battle_pass_data()
        
        # 设置赛季结束日期（示例：当前日期后30天）
        self._set_season_end_date()
    
    def _initialize_battle_pass(self):
        """初始化高级通行证"""
        # 创建通行证等级
        self._create_levels()
        
        # 创建任务
        self._create_tasks()
        
        # 创建每日任务
        self._create_daily_tasks()
    
    def _create_levels(self):
        """创建通行证等级"""
        # 定义等级所需经验值
        level_experience = [0, 1000, 2500, 4500, 7000, 10000, 13500, 17500, 22000, 27000, 32500, 38500, 45000, 52000, 59500, 67500, 76000, 85000, 94500, 104500]
        
        for i in range(20):
            level = BattlePassLevel(i + 1, level_experience[i] if i < len(level_experience) else level_experience[-1] + 10000 * (i - len(level_experience) + 1))
            
            # 添加普通奖励
            if i == 0:
                # 等级1奖励
                level.add_reward(BattlePassReward(f"reward_1_1", "初始奖励", "获得5个货币", "currency", 5))
            elif i == 2:
                # 等级3奖励
                level.add_reward(BattlePassReward(f"reward_3_1", "等级3奖励", "获得特殊头衔", "title", "新手战士", False))
            elif i == 6:
                # 等级7奖励
                level.add_reward(BattlePassReward(f"reward_7_1", "等级7奖励", "获得表情动作", "emote", "胜利欢呼", False))
            elif i == 12:
                # 等级13奖励
                level.add_reward(BattlePassReward(f"reward_13_1", "等级13奖励", "获得专属特效", "effect", "火焰轨迹", False))
            else:
                # 其他等级普通奖励
                currency_reward = 10 + i * 2
                level.add_reward(BattlePassReward(f"reward_{i+1}_1", f"等级{i+1}奖励", f"获得{currency_reward}个货币", "currency", currency_reward))
            
            # 添加高级奖励
            if i == 0:
                # 等级1高级奖励
                level.add_reward(BattlePassReward(f"reward_1_2", "高级初始奖励", "获得特殊皮肤", "skin", "ship_10", True))
            elif i == 3:
                # 等级4高级奖励
                level.add_reward(BattlePassReward(f"reward_4_2", "高级奖励", "获得特殊武器", "weapon", "激光枪", True))
            elif i == 5:
                # 等级6高级奖励
                level.add_reward(BattlePassReward(f"reward_6_2", "高级奖励", "获得专属特效", "effect", "闪电环绕", True))
            elif i == 7:
                # 等级8高级奖励
                level.add_reward(BattlePassReward(f"reward_8_2", "高级奖励", "获得特殊头衔", "title", "通行证专家", True))
            elif i == 9:
                # 等级10高级奖励
                level.add_reward(BattlePassReward(f"reward_10_2", "高级奖励", "获得特殊皮肤", "skin", "ship_15", True))
            elif i == 11:
                # 等级12高级奖励
                level.add_reward(BattlePassReward(f"reward_12_2", "高级奖励", "获得特殊武器", "weapon", "等离子炮", True))
            elif i == 13:
                # 等级14高级奖励
                level.add_reward(BattlePassReward(f"reward_14_2", "高级奖励", "获得表情动作", "emote", "庆祝胜利", True))
            elif i == 15:
                # 等级16高级奖励
                level.add_reward(BattlePassReward(f"reward_16_2", "高级奖励", "获得专属特效", "effect", "彩虹轨迹", True))
            elif i == 17:
                # 等级18高级奖励
                level.add_reward(BattlePassReward(f"reward_18_2", "高级奖励", "获得特殊头衔", "title", "赛季冠军", True))
            elif i == 19:
                # 等级20高级奖励
                level.add_reward(BattlePassReward(f"reward_20_2", "终极奖励", "获得终极武器", "weapon", "终极毁灭者", True))
            else:
                # 其他等级高级奖励
                premium_currency = 20 + i * 3
                level.add_reward(BattlePassReward(f"reward_{i+1}_2", f"高级等级{i+1}奖励", f"获得{premium_currency}个货币", "currency", premium_currency, True))
            
            self.levels.append(level)
    
    def _create_tasks(self):
        """创建通行证任务"""
        # 任务列表
        tasks = [
            {"id": "task_1", "name": "初露锋芒", "description": "消灭10个外星人", "type": "kill", "target": 10, "reward": 500},
            {"id": "task_2", "name": "百发百中", "description": "消灭100个外星人", "type": "kill", "target": 100, "reward": 1000},
            {"id": "task_3", "name": "千军万马", "description": "消灭500个外星人", "type": "kill", "target": 500, "reward": 2000},
            {"id": "task_4", "name": "得分高手", "description": "获得5000分", "type": "score", "target": 5000, "reward": 800},
            {"id": "task_5", "name": "高分达人", "description": "获得20000分", "type": "score", "target": 20000, "reward": 1500},
            {"id": "task_6", "name": "关卡大师", "description": "完成10个关卡", "type": "level", "target": 10, "reward": 1200},
            {"id": "task_7", "name": "关卡专家", "description": "完成20个关卡", "type": "level", "target": 20, "reward": 2500},
            {"id": "task_8", "name": "Boss杀手", "description": "击败5个Boss", "type": "boss", "target": 5, "reward": 1800},
            {"id": "task_9", "name": "狙击高手", "description": "在狙击模式下发射50发子弹", "type": "sniper", "target": 50, "reward": 1000},
            {"id": "task_10", "name": "道具大师", "description": "使用护盾10次", "type": "shield", "target": 10, "reward": 800},
        ]
        
        for task_data in tasks:
            task = BattlePassTask(
                task_data["id"],
                task_data["name"],
                task_data["description"],
                task_data["type"],
                task_data["target"],
                task_data["reward"]
            )
            self.tasks.append(task)
    
    def _create_daily_tasks(self):
        """创建每日任务"""
        # 每日任务模板
        daily_task_templates = [
            {"name": "每日消灭", "description": "消灭30个外星人", "type": "kill", "target": 30, "reward": 500},
            {"name": "每日得分", "description": "获得3000分", "type": "score", "target": 3000, "reward": 400},
            {"name": "每日关卡", "description": "完成2个关卡", "type": "level", "target": 2, "reward": 600},
            {"name": "每日道具", "description": "使用时间冻结3次", "type": "freeze", "target": 3, "reward": 300},
        ]
        
        # 随机选择3个每日任务
        import random
        selected_templates = random.sample(daily_task_templates, 3)
        
        for i, template in enumerate(selected_templates):
            task = BattlePassTask(
                f"daily_task_{i+1}",
                template["name"],
                template["description"],
                template["type"],
                template["target"],
                template["reward"],
                is_daily=True
            )
            self.daily_tasks.append(task)
    
    def _set_season_end_date(self):
        """设置赛季结束日期"""
        # 从存储中加载赛季结束日期
        if os.path.exists('battle_pass_season.json'):
            try:
                with open('battle_pass_season.json', 'r') as f:
                    data = json.load(f)
                    if 'season_end_date' in data:
                        self.season_end_date = datetime.fromisoformat(data['season_end_date'])
                        return
            except Exception as e:
                pass
        
        # 如果没有存储的日期，设置为当前日期后30天
        self.season_end_date = datetime.now() + timedelta(days=30)
        
        # 保存赛季结束日期
        try:
            with open('battle_pass_season.json', 'w') as f:
                json.dump({'season_end_date': self.season_end_date.isoformat()}, f)
        except Exception as e:
            pass
    
    def _load_battle_pass_data(self):
        """加载通行证数据"""
        try:
            if os.path.exists('battle_pass.json'):
                with open('battle_pass.json', 'r') as f:
                    data = json.load(f)
                    
                    # 加载基本数据
                    self.current_level = data.get('current_level', 1)
                    self.total_experience = data.get('total_experience', 0)
                    self.premium_unlocked = data.get('premium_unlocked', False)
                    self.pass_active = data.get('pass_active', False)
                    
                    # 加载等级数据
                    if 'levels' in data:
                        for level_data in data['levels']:
                            level_num = level_data.get('level')
                            if level_num and 1 <= level_num <= len(self.levels):
                                level = self.levels[level_num - 1]
                                level.experience_gained = level_data.get('experience_gained', 0)
                                
                                # 加载奖励领取状态
                                if 'rewards' in level_data:
                                    for reward_data in level_data['rewards']:
                                        reward_id = reward_data.get('reward_id')
                                        claimed = reward_data.get('claimed', False)
                                        for reward in level.rewards:
                                            if reward.reward_id == reward_id:
                                                reward.claimed = claimed
                    
                    # 加载任务数据
                    if 'tasks' in data:
                        for task_data in data['tasks']:
                            task_id = task_data.get('task_id')
                            if task_id:
                                for task in self.tasks:
                                    if task.task_id == task_id:
                                        task.current = task_data.get('current', 0)
                                        task.completed = task_data.get('completed', False)
                                        task.claimed = task_data.get('claimed', False)
                    
                    # 加载每日任务数据
                    if 'daily_tasks' in data:
                        for task_data in data['daily_tasks']:
                            task_id = task_data.get('task_id')
                            if task_id:
                                for task in self.daily_tasks:
                                    if task.task_id == task_id:
                                        task.current = task_data.get('current', 0)
                                        task.completed = task_data.get('completed', False)
                                        task.claimed = task_data.get('claimed', False)
        except Exception as e:
            print(f"加载通行证数据失败: {e}")
    
    def save_battle_pass_data(self):
        """保存通行证数据（优化性能）"""
        # 限制保存频率，避免频繁IO操作
        if not hasattr(self, '_last_save_time'):
            self._last_save_time = 0
        
        current_time = pygame.time.get_ticks()
        if current_time - self._last_save_time < 1000:  # 1秒内不重复保存
            return
        
        try:
            data = {
                'current_level': self.current_level,
                'total_experience': self.total_experience,
                'premium_unlocked': self.premium_unlocked,
                'pass_active': self.pass_active,
                'levels': [],
                'tasks': [],
                'daily_tasks': []
            }
            
            # 保存等级数据
            for level in self.levels:
                level_data = {
                    'level': level.level,
                    'experience_gained': level.experience_gained,
                    'rewards': []
                }
                
                # 保存奖励数据
                for reward in level.rewards:
                    level_data['rewards'].append({
                        'reward_id': reward.reward_id,
                        'claimed': reward.claimed
                    })
                
                data['levels'].append(level_data)
            
            # 保存任务数据
            for task in self.tasks:
                data['tasks'].append({
                    'task_id': task.task_id,
                    'current': task.current,
                    'completed': task.completed,
                    'claimed': task.claimed
                })
            
            # 保存每日任务数据
            for task in self.daily_tasks:
                data['daily_tasks'].append({
                    'task_id': task.task_id,
                    'current': task.current,
                    'completed': task.completed,
                    'claimed': task.claimed
                })
            
            with open('battle_pass.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            # 更新最后保存时间
            self._last_save_time = current_time
        except Exception as e:
            print(f"保存通行证数据失败: {e}")
    
    def update(self):
        """更新通行证状态"""
        # 检查赛季是否结束
        if datetime.now() > self.season_end_date:
            self._reset_season()
        
        # 检查每日任务是否需要刷新
        self._check_daily_tasks_refresh()
        
        # 更新任务进度
        self._update_task_progress()
        
        # 检查等级提升
        self._check_level_up()
    
    def _reset_season(self):
        """重置赛季"""
        # 重置通行证数据
        self.current_level = 1
        self.total_experience = 0
        self.premium_unlocked = False
        
        # 重置等级数据
        for level in self.levels:
            level.experience_gained = 0
            for reward in level.rewards:
                reward.claimed = False
        
        # 重置任务数据
        for task in self.tasks:
            task.current = 0
            task.completed = False
            task.claimed = False
        
        # 重置每日任务
        self.daily_tasks = []
        self._create_daily_tasks()
        
        # 设置新赛季
        self.pass_season = f"Season {int(self.pass_season.split()[1]) + 1}"
        self._set_season_end_date()
        
        # 保存数据
        self.save_battle_pass_data()
    
    def _check_daily_tasks_refresh(self):
        """检查每日任务是否需要刷新"""
        # 检查是否有存储的每日任务刷新时间
        last_refresh = None
        try:
            if os.path.exists('battle_pass_daily.json'):
                with open('battle_pass_daily.json', 'r') as f:
                    data = json.load(f)
                    last_refresh_str = data.get('last_refresh')
                    if last_refresh_str:
                        last_refresh = datetime.fromisoformat(last_refresh_str)
        except Exception as e:
            pass
        
        # 如果没有刷新时间或已过一天，刷新每日任务
        if not last_refresh or datetime.now().date() > last_refresh.date():
            self._refresh_daily_tasks()
            
            # 保存刷新时间
            try:
                with open('battle_pass_daily.json', 'w') as f:
                    json.dump({'last_refresh': datetime.now().isoformat()}, f)
            except Exception as e:
                pass
    
    def _refresh_daily_tasks(self):
        """刷新每日任务"""
        self.daily_tasks = []
        self._create_daily_tasks()
    
    def _update_task_progress(self):
        """更新任务进度"""
        # 更新普通任务进度
        for task in self.tasks:
            if not task.completed:
                if task.task_type == "kill":
                    task.current = self.stats.aliens_killed
                elif task.task_type == "score":
                    task.current = self.stats.score
                elif task.task_type == "level":
                    task.current = self.stats.max_level_reached
                elif task.task_type == "boss":
                    task.current = self.stats.bosses_defeated
                elif task.task_type == "sniper":
                    task.current = self.stats.sniper_shots_fired
                elif task.task_type == "shield":
                    task.current = self.stats.shield_uses
                
                # 检查任务是否完成
                if task.current >= task.target:
                    task.completed = True
        
        # 更新每日任务进度
        for task in self.daily_tasks:
            if not task.completed:
                if task.task_type == "kill":
                    task.current = self.stats.aliens_killed
                elif task.task_type == "score":
                    task.current = self.stats.score
                elif task.task_type == "level":
                    task.current = self.stats.max_level_reached
                elif task.task_type == "freeze":
                    task.current = self.stats.freeze_uses
                
                # 检查任务是否完成
                if task.current >= task.target:
                    task.completed = True
    
    def _check_level_up(self):
        """检查等级提升"""
        # 计算当前等级
        total_exp = self.total_experience
        new_level = 1
        
        for i, level in enumerate(self.levels):
            if i > 0 and total_exp >= level.required_experience:
                new_level = i + 1
        
        # 如果等级提升
        if new_level > self.current_level:
            self.current_level = new_level
            self.save_battle_pass_data()
    
    def add_experience(self, amount):
        """添加经验值"""
        self.total_experience += amount
        
        # 更新当前等级的经验值
        if self.current_level <= len(self.levels):
            level = self.levels[self.current_level - 1]
            
            # 计算当前等级所需经验
            if self.current_level == 1:
                level_required = self.levels[0].required_experience
            else:
                level_required = self.levels[self.current_level - 1].required_experience - self.levels[self.current_level - 2].required_experience
            
            # 添加经验到当前等级
            level.experience_gained += amount
        
        # 检查等级提升
        self._check_level_up()
        
        # 保存数据
        self.save_battle_pass_data()
    
    def claim_task_reward(self, task):
        """领取任务奖励"""
        if task.completed and not task.claimed:
            # 添加经验值
            self.add_experience(task.experience_reward)
            
            # 标记任务为已领取
            task.claimed = True
            
            # 保存数据
            self.save_battle_pass_data()
            
            return True
        return False
    
    def claim_level_reward(self, level, reward):
        """领取等级奖励（优化用户体验）"""
        # 检查奖励是否可领取
        if not reward.claimed:
            # 检查是否达到领取条件
            if level.level <= self.current_level:
                # 根据奖励类型发放奖励
                if reward.reward_type == "currency":
                    self.stats.add_currency(reward.value)
                elif reward.reward_type == "skin":
                    # 这里需要实现皮肤解锁逻辑
                    pass
                elif reward.reward_type == "upgrade":
                    # 这里需要实现升级逻辑
                    pass
                elif reward.reward_type == "weapon":
                    # 发放特殊武器
                    self._unlock_special_weapon(reward.value)
                elif reward.reward_type == "effect":
                    # 发放专属特效
                    self._unlock_special_effect(reward.value)
                elif reward.reward_type == "title":
                    # 发放专属头衔
                    self._unlock_special_title(reward.value)
                elif reward.reward_type == "emote":
                    # 发放表情动作
                    self._unlock_emote(reward.value)
                
                # 标记奖励为已领取
                reward.claimed = True
                
                # 创建奖励领取的粒子特效
                screen_width, screen_height = self.ai_game.screen.get_size()
                center_x, center_y = screen_width // 2, screen_height // 2
                self.create_particle(center_x, center_y, self.current_theme["colors"]["accent"])
                
                # 重置动画进度，使经验条动画重新播放
                self.animation_progress = 0.0
                self.last_update_time = pygame.time.get_ticks()
                
                # 保存数据
                self.save_battle_pass_data()
                
                return True
        return False
    
    def _unlock_special_weapon(self, weapon_id):
        """解锁特殊武器"""
        # 这里需要实现特殊武器解锁逻辑
        # 示例：保存武器解锁状态到游戏设置
        if not hasattr(self, 'unlocked_weapons'):
            self.unlocked_weapons = []
        if weapon_id not in self.unlocked_weapons:
            self.unlocked_weapons.append(weapon_id)
        print(f"解锁特殊武器: {weapon_id}")
    
    def _unlock_special_effect(self, effect_id):
        """解锁专属特效"""
        # 这里需要实现专属特效解锁逻辑
        # 示例：保存特效解锁状态到游戏设置
        if not hasattr(self, 'unlocked_effects'):
            self.unlocked_effects = []
        if effect_id not in self.unlocked_effects:
            self.unlocked_effects.append(effect_id)
        print(f"解锁专属特效: {effect_id}")
    
    def _unlock_special_title(self, title_id):
        """解锁专属头衔"""
        # 这里需要实现专属头衔解锁逻辑
        # 示例：保存头衔解锁状态到游戏设置
        if not hasattr(self, 'unlocked_titles'):
            self.unlocked_titles = []
        if title_id not in self.unlocked_titles:
            self.unlocked_titles.append(title_id)
        print(f"解锁专属头衔: {title_id}")
    
    def _unlock_emote(self, emote_id):
        """解锁表情动作"""
        # 这里需要实现表情动作解锁逻辑
        # 示例：保存表情解锁状态到游戏设置
        if not hasattr(self, 'unlocked_emotes'):
            self.unlocked_emotes = []
        if emote_id not in self.unlocked_emotes:
            self.unlocked_emotes.append(emote_id)
        print(f"解锁表情动作: {emote_id}")
    
    def unlock_premium(self):
        """解锁高级通行证"""
        # 检查是否有足够的货币（示例：100个货币）
        if self.stats.spend_currency(100):
            self.premium_unlocked = True
            self.pass_active = True
            self.save_battle_pass_data()
            return True
        return False
    
    def get_current_level(self):
        """获取当前等级"""
        return self.levels[self.current_level - 1] if self.current_level <= len(self.levels) else None
    
    def get_season_time_left(self):
        """获取赛季剩余时间"""
        time_left = self.season_end_date - datetime.now()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f"{days}天 {hours}小时 {minutes}分钟"
    
    def draw_battle_pass_ui(self, screen):
        """绘制通行证UI"""
        if not self.pass_active:
            return
        
        # 绘制通行证界面
        screen_width, screen_height = screen.get_size()
        pass_width = 800
        pass_height = 600
        pass_x = (screen_width - pass_width) // 2
        pass_y = (screen_height - pass_height) // 2
        
        # 绘制背景（使用当前主题颜色）
        theme_colors = self.current_theme["colors"]
        pygame.draw.rect(screen, theme_colors["primary"], (pass_x, pass_y, pass_width, pass_height), border_radius=10)
        pygame.draw.rect(screen, theme_colors["secondary"], (pass_x + 10, pass_y + 10, pass_width - 20, pass_height - 20), border_radius=8)
        
        # 绘制标题（使用当前主题颜色）
        font = self._load_chinese_font(48)
        title_text = font.render(f"高级通行证 - {self.pass_season}", True, theme_colors["highlight"])
        title_rect = title_text.get_rect(center=(pass_x + pass_width // 2, pass_y + 50))
        screen.blit(title_text, title_rect)
        
        # 绘制赛季剩余时间
        small_font = self._load_chinese_font(20)
        time_text = small_font.render(f"赛季剩余时间: {self.get_season_time_left()}", True, (200, 200, 200))
        time_rect = time_text.get_rect(center=(pass_x + pass_width // 2, pass_y + 90))
        screen.blit(time_text, time_rect)
        
        # 绘制当前等级和经验条
        current_level = self.get_current_level()
        if current_level:
            level_font = self._load_chinese_font(32)
            level_text = level_font.render(f"等级 {self.current_level}", True, (255, 255, 255))
            level_rect = level_text.get_rect(left=pass_x + 50, top=pass_y + 130)
            screen.blit(level_text, level_rect)
            
            # 绘制经验条
            exp_bar_width = pass_width - 100
            exp_bar_height = 20
            exp_bar_x = pass_x + 50
            exp_bar_y = pass_y + 170
            
            # 计算经验条进度
            if self.current_level < len(self.levels):
                next_level_exp = self.levels[self.current_level].required_experience
                prev_level_exp = self.levels[self.current_level - 1].required_experience
                current_level_exp = next_level_exp - prev_level_exp
                current_exp_in_level = self.total_experience - prev_level_exp
                progress = min(1.0, current_exp_in_level / current_level_exp)
            else:
                progress = 1.0
            
            # 绘制经验条背景
            pygame.draw.rect(screen, (30, 30, 50), (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), border_radius=10)
            
            # 绘制经验条进度（带动画效果，使用当前主题颜色）
            animated_progress = progress * self.animation_progress
            progress_width = int(exp_bar_width * animated_progress)
            pygame.draw.rect(screen, theme_colors["accent"], (exp_bar_x, exp_bar_y, progress_width, exp_bar_height), border_radius=10)
            
            # 绘制经验值文本
            exp_text = small_font.render(f"{self.total_experience} / {next_level_exp if self.current_level < len(self.levels) else 'Max'}", True, (255, 255, 255))
            exp_rect = exp_text.get_rect(center=(pass_x + pass_width // 2, exp_bar_y + exp_bar_height // 2))
            screen.blit(exp_text, exp_rect)
        
        # 绘制等级奖励
        reward_start_y = pass_y + 220
        reward_spacing = 80
        
        # 绘制当前等级和下一级的奖励
        for i in range(max(0, self.current_level - 2), min(len(self.levels), self.current_level + 2)):
            level = self.levels[i]
            level_y = reward_start_y + (i - max(0, self.current_level - 2)) * reward_spacing
            
            # 绘制等级标题
            level_title_font = self._load_chinese_font(24)
            level_title_text = level_title_font.render(f"等级 {level.level}", True, (255, 255, 255))
            level_title_rect = level_title_text.get_rect(left=pass_x + 50, top=level_y)
            screen.blit(level_title_text, level_title_rect)
            
            # 绘制奖励
            reward_x = pass_x + 150
            reward_y = level_y
            reward_spacing_x = 200
            
            for j, reward in enumerate(level.rewards):
                # 绘制奖励背景
                reward_bg_color = (100, 100, 150) if not reward.is_premium else (150, 100, 150)
                reward_bg_rect = pygame.Rect(reward_x + j * reward_spacing_x, reward_y, 180, 50)
                pygame.draw.rect(screen, reward_bg_color, reward_bg_rect, border_radius=5)
                
                # 绘制奖励名称
                reward_font = self._load_chinese_font(16)
                reward_text = reward_font.render(reward.name, True, (255, 255, 255))
                reward_rect = reward_text.get_rect(center=(reward_bg_rect.centerx, reward_bg_rect.centery - 5))
                screen.blit(reward_text, reward_rect)
                
                # 绘制奖励状态
                status_text = "已领取" if reward.claimed else "可领取" if level.level <= self.current_level else "未解锁"
                status_color = (100, 200, 100) if reward.claimed else (200, 200, 0) if level.level <= self.current_level else (100, 100, 100)
                status_surface = reward_font.render(status_text, True, status_color)
                status_rect = status_surface.get_rect(center=(reward_bg_rect.centerx, reward_bg_rect.centery + 15))
                screen.blit(status_surface, status_rect)
        
        # 绘制任务
        task_start_y = pass_y + 420
        task_font = self._load_chinese_font(20)
        
        # 绘制普通任务
        task_title_text = task_font.render("普通任务", True, (255, 255, 255))
        task_title_rect = task_title_text.get_rect(left=pass_x + 50, top=task_start_y)
        screen.blit(task_title_text, task_title_rect)
        
        task_y = task_start_y + 30
        for task in self.tasks[:3]:  # 只显示前3个任务
            # 绘制任务背景
            task_bg_color = (100, 150, 100) if task.completed else (80, 80, 120)
            task_bg_rect = pygame.Rect(pass_x + 50, task_y, pass_width - 100, 40)
            pygame.draw.rect(screen, task_bg_color, task_bg_rect, border_radius=5)
            
            # 绘制任务名称和进度
            task_text = task_font.render(f"{task.name}: {min(task.current, task.target)}/{task.target}", True, (255, 255, 255))
            task_rect = task_text.get_rect(left=pass_x + 60, top=task_y + 10)
            screen.blit(task_text, task_rect)
            
            # 绘制任务状态
            status_text = "已领取" if task.claimed else "可领取" if task.completed else "进行中"
            status_color = (100, 200, 100) if task.claimed else (200, 200, 0) if task.completed else (150, 150, 150)
            status_surface = task_font.render(status_text, True, status_color)
            status_rect = status_surface.get_rect(right=pass_x + pass_width - 60, top=task_y + 10)
            screen.blit(status_surface, status_rect)
            
            task_y += 45
        
        # 绘制每日任务
        daily_task_title_text = task_font.render("每日任务", True, (255, 215, 0))
        daily_task_title_rect = daily_task_title_text.get_rect(left=pass_x + 50, top=task_y)
        screen.blit(daily_task_title_text, daily_task_title_rect)
        
        task_y += 30
        for task in self.daily_tasks:
            # 绘制任务背景
            task_bg_color = (150, 100, 100) if task.completed else (80, 80, 120)
            task_bg_rect = pygame.Rect(pass_x + 50, task_y, pass_width - 100, 40)
            pygame.draw.rect(screen, task_bg_color, task_bg_rect, border_radius=5)
            
            # 绘制任务名称和进度
            task_text = task_font.render(f"{task.name}: {min(task.current, task.target)}/{task.target}", True, (255, 255, 255))
            task_rect = task_text.get_rect(left=pass_x + 60, top=task_y + 10)
            screen.blit(task_text, task_rect)
            
            # 绘制任务状态
            status_text = "已领取" if task.claimed else "可领取" if task.completed else "进行中"
            status_color = (100, 200, 100) if task.claimed else (200, 200, 0) if task.completed else (150, 150, 150)
            status_surface = task_font.render(status_text, True, status_color)
            status_rect = status_surface.get_rect(right=pass_x + pass_width - 60, top=task_y + 10)
            screen.blit(status_surface, status_rect)
            
            task_y += 45
        
        # 绘制解锁高级通行证按钮
        if not self.premium_unlocked:
            unlock_button_rect = pygame.Rect(pass_x + pass_width - 200, pass_y + 130, 150, 40)
            pygame.draw.rect(screen, (200, 150, 0), unlock_button_rect, border_radius=5)
            
            unlock_font = self._load_chinese_font(20)
            unlock_text = unlock_font.render("解锁高级通行证", True, (255, 255, 255))
            unlock_rect = unlock_text.get_rect(center=unlock_button_rect.center)
            screen.blit(unlock_text, unlock_rect)
        

        
        # 绘制关闭按钮
        close_button_rect = pygame.Rect(pass_x + pass_width - 120, pass_y + pass_height - 60, 100, 40)
        pygame.draw.rect(screen, (200, 50, 50), close_button_rect, border_radius=5)
        
        close_font = self._load_chinese_font(20)
        close_text = close_font.render("关闭", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=close_button_rect.center)
        screen.blit(close_text, close_rect)
        

        
        # 绘制粒子特效
        self.draw_particles(screen)
        
        # 绘制等级提升动画
        self.draw_level_up_animation(screen)
    
    def handle_event(self, event):
        """处理通行证事件"""
        if not self.pass_active:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                screen_width, screen_height = self.ai_game.screen.get_size()
                pass_width = 800
                pass_height = 600
                pass_x = (screen_width - pass_width) // 2
                pass_y = (screen_height - pass_height) // 2
                
                # 检查关闭按钮
                close_button_rect = pygame.Rect(pass_x + pass_width - 120, pass_y + pass_height - 60, 100, 40)
                if close_button_rect.collidepoint(mouse_pos):
                    self.pass_active = False
                    return True
                
                # 检查解锁高级通行证按钮
                if not self.premium_unlocked:
                    unlock_button_rect = pygame.Rect(pass_x + pass_width - 200, pass_y + 130, 150, 40)
                    if unlock_button_rect.collidepoint(mouse_pos):
                        if self.unlock_premium():
                            # 播放解锁音效
                            if hasattr(self.ai_game, 'sound_manager'):
                                self.ai_game.sound_manager.play_sound('button_click')
                        return True
                
                # 检查奖励领取
                reward_start_y = pass_y + 220
                reward_spacing = 80
                
                for i in range(max(0, self.current_level - 2), min(len(self.levels), self.current_level + 2)):
                    level = self.levels[i]
                    level_y = reward_start_y + (i - max(0, self.current_level - 2)) * reward_spacing
                    
                    reward_x = pass_x + 150
                    reward_y = level_y
                    reward_spacing_x = 200
                    
                    for j, reward in enumerate(level.rewards):
                        reward_bg_rect = pygame.Rect(reward_x + j * reward_spacing_x, reward_y, 180, 50)
                        if reward_bg_rect.collidepoint(mouse_pos):
                            # 检查是否可以领取奖励
                            if not reward.claimed and level.level <= self.current_level:
                                # 如果是高级奖励，检查是否解锁了高级通行证
                                if reward.is_premium and not self.premium_unlocked:
                                    pass
                                else:
                                    # 领取奖励
                                    if self.claim_level_reward(level, reward):
                                        # 播放领取音效
                                        if hasattr(self.ai_game, 'sound_manager'):
                                            self.ai_game.sound_manager.play_sound('button_click')
                                return True
                
                # 检查任务领取
                task_start_y = pass_y + 420
                task_y = task_start_y + 30
                
                for task in self.tasks[:3]:
                    task_bg_rect = pygame.Rect(pass_x + 50, task_y, pass_width - 100, 40)
                    if task_bg_rect.collidepoint(mouse_pos):
                        # 检查是否可以领取任务奖励
                        if task.completed and not task.claimed:
                            if self.claim_task_reward(task):
                                # 播放领取音效
                                if hasattr(self.ai_game, 'sound_manager'):
                                    self.ai_game.sound_manager.play_sound('button_click')
                            return True
                    task_y += 45
                
                # 检查每日任务领取
                task_y += 30
                for task in self.daily_tasks:
                    task_bg_rect = pygame.Rect(pass_x + 50, task_y, pass_width - 100, 40)
                    if task_bg_rect.collidepoint(mouse_pos):
                        # 检查是否可以领取任务奖励
                        if task.completed and not task.claimed:
                            if self.claim_task_reward(task):
                                # 播放领取音效
                                if hasattr(self.ai_game, 'sound_manager'):
                                    self.ai_game.sound_manager.play_sound('button_click')
                            return True
                    task_y += 45
        
        return False
    
    def update_animations(self):
        """更新动画效果"""
        current_time = pygame.time.get_ticks()
        
        # 更新经验条动画
        if self.animation_progress < 1.0:
            elapsed = current_time - self.last_update_time
            self.animation_progress += elapsed / self.animation_duration
            self.animation_progress = min(1.0, self.animation_progress)
        
        # 更新等级提升动画
        if self.level_up_animation:
            self.level_up_timer += current_time - self.last_update_time
            if self.level_up_timer > self.level_up_duration:
                self.level_up_animation = False
                self.level_up_timer = 0
        
        # 更新粒子特效
        self._update_particles()
        
        # 更新按钮悬停效果
        self._update_hover_effects()
        
        self.last_update_time = current_time
    
    def _update_particles(self):
        """更新粒子特效（优化性能）"""
        # 限制粒子数量，避免过多粒子影响性能
        max_particles = 100
        if len(self.particles) > max_particles:
            self.particles = self.particles[-max_particles:]
        
        # 更新粒子位置和生命周期
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # 移除生命值为0的粒子
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def _update_hover_effects(self):
        """更新按钮悬停效果"""
        # 这里可以添加按钮悬停的视觉效果逻辑
        pass
    
    def create_particle(self, x, y, color=None):
        """创建粒子特效"""
        import random
        
        # 如果没有指定颜色，使用当前主题的粒子颜色
        if color is None:
            color = self.current_theme["particle_color"]
        
        # 创建10个粒子
        for _ in range(10):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'color': color,
                'life': random.randint(30, 60),
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
    
    def draw_particles(self, screen):
        """绘制粒子特效"""
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_level_up_animation(self, screen):
        """绘制等级提升动画"""
        if not self.level_up_animation:
            return
        
        screen_width, screen_height = screen.get_size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # 绘制等级提升文本
        font = self._load_chinese_font(72)
        level_up_text = font.render(f"等级提升！", True, (255, 215, 0))
        level_text = font.render(f"Lv.{self.current_level}", True, (255, 215, 0))
        
        # 计算动画进度
        progress = min(1.0, self.level_up_timer / self.level_up_duration)
        
        # 绘制动画效果
        if progress < 0.5:
            # 缩放动画
            scale = 0.5 + progress * 1.0
            level_up_surface = pygame.transform.scale(level_up_text, 
                                                    (int(level_up_text.get_width() * scale), 
                                                     int(level_up_text.get_height() * scale)))
            level_surface = pygame.transform.scale(level_text, 
                                                 (int(level_text.get_width() * scale), 
                                                  int(level_text.get_height() * scale)))
        else:
            # 淡出动画
            alpha = 255 - (progress - 0.5) * 510
            level_up_surface = level_up_text.copy()
            level_surface.set_alpha(int(alpha))
            level_surface = pygame.transform.scale(level_up_surface, 
                                                  (int(level_up_text.get_width() * 1.5), 
                                                   int(level_up_text.get_height() * 1.5)))
            level_surface = level_surface.copy()
            level_surface.set_alpha(int(alpha))
            level_surface = pygame.transform.scale(level_surface, 
                                                  (int(level_text.get_width() * 1.5), 
                                                   int(level_text.get_height() * 1.5)))
        
        # 绘制文本
        level_up_rect = level_up_surface.get_rect(center=(center_x, center_y - 50))
        level_rect = level_surface.get_rect(center=(center_x, center_y + 50))
        screen.blit(level_up_surface, level_up_rect)
        screen.blit(level_surface, level_rect)
        
        # 创建粒子特效
        if progress < 0.3:
            self.create_particle(center_x, center_y)
    
    def _check_level_up(self):
        """检查等级提升"""
        # 计算当前等级
        total_exp = self.total_experience
        new_level = 1
        
        for i, level in enumerate(self.levels):
            if i > 0 and total_exp >= level.required_experience:
                new_level = i + 1
        
        # 如果等级提升
        if new_level > self.current_level:
            old_level = self.current_level
            self.current_level = new_level
            self.save_battle_pass_data()
            
            # 触发等级提升动画
            self.level_up_animation = True
            self.level_up_timer = 0
            self.last_update_time = pygame.time.get_ticks()
            
            # 创建粒子特效
            screen_width, screen_height = self.ai_game.screen.get_size()
            self.create_particle(screen_width // 2, screen_height // 2)
    
    def _define_season_themes(self):
        """定义赛季主题"""
        return {
            "default": {
                "name": "默认主题",
                "colors": {
                    "primary": (50, 50, 80),
                    "secondary": (80, 80, 120),
                    "accent": (0, 150, 255),
                    "text": (255, 255, 255),
                    "highlight": (255, 215, 0)
                },
                "particle_color": (255, 215, 0),
                "background_effect": "none"
            },
            "Season 1": {
                "name": "星际探索",
                "colors": {
                    "primary": (20, 30, 60),
                    "secondary": (40, 50, 90),
                    "accent": (0, 100, 200),
                    "text": (255, 255, 255),
                    "highlight": (255, 165, 0)
                },
                "particle_color": (0, 150, 255),
                "background_effect": "stars"
            },
            "Season 2": {
                "name": "冰雪奇缘",
                "colors": {
                    "primary": (30, 60, 80),
                    "secondary": (50, 80, 100),
                    "accent": (100, 200, 255),
                    "text": (255, 255, 255),
                    "highlight": (255, 255, 255)
                },
                "particle_color": (100, 200, 255),
                "background_effect": "snow"
            },
            "Season 3": {
                "name": "马年庆典",
                "colors": {
                    "primary": (80, 20, 20),
                    "secondary": (120, 40, 40),
                    "accent": (255, 50, 50),
                    "text": (255, 255, 255),
                    "highlight": (255, 215, 0)
                },
                "particle_color": (255, 50, 50),
                "background_effect": "fire"
            }
        }
    
    def _load_chinese_font(self, size=36):
        """加载支持中文的字体（带缓存）"""
        import os
        
        # 检查字体缓存
        if not hasattr(self, '_font_cache'):
            self._font_cache = {}
        
        # 如果字体已缓存，直接返回
        if size in self._font_cache:
            return self._font_cache[size]
        
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
                    font = pygame.font.Font(font_path, size)
                    self._font_cache[size] = font
                    return font
                except:
                    continue
        
        # 如果加载失败，使用默认字体
        font = pygame.font.Font(None, size)
        self._font_cache[size] = font
        return font