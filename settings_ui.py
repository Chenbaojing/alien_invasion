import pygame
import sys

# 尝试使用 freetype 模块
use_freetype = False
try:
    import pygame.freetype
    use_freetype = True
except ImportError:
    pass

class SettingsUI:
    """设置界面类"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.ai_game = ai_game
        
        # 界面尺寸
        self.width, self.height = 800, 600
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # 背景颜色
        self.bg_color = (200, 200, 200)
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        
        # 字体设置
        self.font = None
        self.small_font = None
        
        # 尝试使用指定的字体文件路径
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simsun.ttc"   # 宋体
        ]
        
        font_found = False
        for font_path in font_paths:
            try:
                # 尝试使用指定字体文件
                self.font = pygame.font.Font(font_path, 48)
                self.small_font = pygame.font.Font(font_path, 36)
                # 测试中文字符
                test_surface = self.font.render('游戏设置', True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    font_found = True
                    break
            except:
                continue
        
        # 如果指定字体失败，尝试使用 freetype 模块
        if not font_found and use_freetype:
            try:
                pygame.freetype.init()
                for font_path in font_paths:
                    try:
                        self.font = pygame.freetype.Font(font_path, 48)
                        self.small_font = pygame.freetype.Font(font_path, 36)
                        font_found = True
                        break
                    except:
                        continue
            except:
                pass
        
        # 如果所有方法都失败，使用默认字体
        if not font_found:
            try:
                self.font = pygame.font.Font(None, 48)
                self.small_font = pygame.font.Font(None, 36)
            except:
                pass
        
        # 滚动偏移
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # 初始化UI元素
        self._initialize_elements()
    
    def _initialize_elements(self):
        """初始化UI元素"""
        # 标题
        self.title_image = self.font.render("游戏设置", True, self.text_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.rect.centerx
        self.title_rect.y = 30
        
        # 关闭按钮
        self.close_button = pygame.Rect(0, 0, 80, 40)
        self.close_button.topright = (self.rect.right - 20, self.rect.top + 20)
        self.close_text = self.small_font.render("关闭", True, self.text_color)
        self.close_text_rect = self.close_text.get_rect()
        self.close_text_rect.center = self.close_button.center
        
        # 设置项
        self.settings_items = [
            {
                "name": "屏幕尺寸",
                "type": "dropdown",
                "options": ["800x600", "1024x768", "1200x800", "1366x768"],
                "current": f"{self.settings.screen_width}x{self.settings.screen_height}",
                "id": "screen_size"
            },
            {
                "name": "游戏难度",
                "type": "dropdown",
                "options": ["简单", "普通", "困难", "专家"],
                "current": self._get_difficulty_name(),
                "id": "difficulty"
            },
            {
                "name": "游戏模式",
                "type": "dropdown",
                "options": ["普通模式", "道具模式", "无限模式", "Boss模式", "狙击模式"],
                "current": self._get_mode_name(),
                "id": "game_mode"
            },
            {
                "name": "背景音乐",
                "type": "toggle",
                "current": True,  # 假设默认开启
                "id": "background_music"
            },
            {
                "name": "音效",
                "type": "toggle",
                "current": True,  # 假设默认开启
                "id": "sound_effects"
            },
            {
                "name": "粒子效果",
                "type": "toggle",
                "current": True,  # 假设默认开启
                "id": "particle_effects"
            },
            {
                "name": "子弹轨迹",
                "type": "toggle",
                "current": True,  # 假设默认开启
                "id": "bullet_trail"
            },
            {
                "name": "FPS显示",
                "type": "toggle",
                "current": False,  # 假设默认关闭
                "id": "show_fps"
            },
            {
                "name": "帧率锁定",
                "type": "toggle",
                "current": self.settings.enable_frame_rate_limit,  # 使用设置中的值
                "id": "frame_rate_limit"
            },
            {
                "name": "帧率值",
                "type": "dropdown",
                "options": ["30", "60", "120", "240"],
                "current": str(self.settings.frame_rate_limit),  # 使用设置中的值
                "id": "frame_rate_value"
            }
        ]
        
        # 计算最大滚动值
        self.max_scroll = max(0, len(self.settings_items) * 80 - 450)
    
    def _get_difficulty_name(self):
        """获取难度名称"""
        difficulty_map = {
            self.settings.DIFFICULTY_EASY: "简单",
            self.settings.DIFFICULTY_NORMAL: "普通",
            self.settings.DIFFICULTY_HARD: "困难",
            self.settings.DIFFICULTY_EXPERT: "专家"
        }
        return difficulty_map.get(self.settings.game_difficulty, "普通")
    
    def _get_mode_name(self):
        """获取模式名称"""
        mode_map = {
            self.settings.MODE_NORMAL: "普通模式",
            self.settings.MODE_POWERUPS: "道具模式",
            self.settings.MODE_UNLIMITED: "无限模式",
            self.settings.MODE_BOSS: "Boss模式",
            self.settings.MODE_SNIPER: "狙击模式"
        }
        return mode_map.get(self.settings.game_mode, "普通模式")
    
    def _render_text(self, font, text, color):
        """渲染文本，支持两种字体类型"""
        if hasattr(font, 'render'):
            # 传统字体方法
            return font.render(text, True, color)
        elif hasattr(font, 'SysFont') or hasattr(font, 'render_to'):
            # freetype 方法
            surface = pygame.Surface((200, 50), pygame.SRCALPHA)
            font.render_to(surface, (0, 0), text, color)
            return surface
        return None
    
    def draw(self):
        """绘制设置界面"""
        # 绘制背景
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        
        # 绘制标题
        title_surface = self._render_text(self.font, "游戏设置", self.text_color)
        if title_surface:
            self.title_rect = title_surface.get_rect()
            self.title_rect.centerx = self.rect.centerx
            self.title_rect.y = 30
            self.screen.blit(title_surface, self.title_rect)
        
        # 绘制关闭按钮
        pygame.draw.rect(self.screen, (200, 0, 0), self.close_button)
        close_surface = self._render_text(self.small_font, "关闭", self.text_color)
        if close_surface:
            self.close_text_rect = close_surface.get_rect()
            self.close_text_rect.center = self.close_button.center
            self.screen.blit(close_surface, self.close_text_rect)
        
        # 绘制设置项
        for i, item in enumerate(self.settings_items):
            # 计算位置
            item_y = 120 + i * 80 - self.scroll_offset
            
            # 只绘制可见的设置项
            if item_y < 100 or item_y > self.rect.bottom - 50:
                continue
            
            # 绘制设置项名称
            name_surface = self._render_text(self.small_font, item["name"], (0, 0, 0))
            if name_surface:
                name_rect = name_surface.get_rect()
                name_rect.x = self.rect.left + 50
                name_rect.y = item_y
                self.screen.blit(name_surface, name_rect)
            
            # 绘制设置项控件
            if item["type"] == "dropdown":
                # 下拉菜单按钮
                dropdown_rect = pygame.Rect(0, 0, 200, 40)
                dropdown_rect.x = self.rect.right - 250
                dropdown_rect.y = item_y
                pygame.draw.rect(self.screen, (255, 255, 255), dropdown_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), dropdown_rect, 2)
                
                # 下拉菜单文本
                current_surface = self._render_text(self.small_font, item["current"], (0, 0, 0))
                if current_surface:
                    current_rect = current_surface.get_rect()
                    current_rect.center = dropdown_rect.center
                    self.screen.blit(current_surface, current_rect)
            elif item["type"] == "toggle":
                # 开关按钮
                toggle_rect = pygame.Rect(0, 0, 80, 40)
                toggle_rect.x = self.rect.right - 130
                toggle_rect.y = item_y
                
                # 根据当前状态绘制开关
                if item["current"]:
                    pygame.draw.rect(self.screen, (0, 200, 0), toggle_rect)
                    toggle_text = "开启"
                else:
                    pygame.draw.rect(self.screen, (200, 0, 0), toggle_rect)
                    toggle_text = "关闭"
                
                pygame.draw.rect(self.screen, (0, 0, 0), toggle_rect, 2)
                
                # 开关文本
                toggle_surface = self._render_text(self.small_font, toggle_text, (255, 255, 255))
                if toggle_surface:
                    toggle_rect_center = toggle_surface.get_rect()
                    toggle_rect_center.center = toggle_rect.center
                    self.screen.blit(toggle_surface, toggle_rect_center)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查关闭按钮
            if self.close_button.collidepoint(event.pos):
                return "close"
            
            # 检查设置项
            for i, item in enumerate(self.settings_items):
                item_y = 120 + i * 80 - self.scroll_offset
                
                if item["type"] == "dropdown":
                    dropdown_rect = pygame.Rect(0, 0, 200, 40)
                    dropdown_rect.x = self.rect.right - 250
                    dropdown_rect.y = item_y
                    
                    if dropdown_rect.collidepoint(event.pos):
                        # 处理下拉菜单点击
                        self._handle_dropdown_click(item)
                elif item["type"] == "toggle":
                    toggle_rect = pygame.Rect(0, 0, 80, 40)
                    toggle_rect.x = self.rect.right - 130
                    toggle_rect.y = item_y
                    
                    if toggle_rect.collidepoint(event.pos):
                        # 切换开关状态
                        item["current"] = not item["current"]
                        # 应用帧率锁定设置
                        if item["id"] == "frame_rate_limit":
                            self.settings.enable_frame_rate_limit = item["current"]
        
        elif event.type == pygame.MOUSEBUTTONUP:
            # 处理鼠标滚轮
            pass
        
        elif event.type == pygame.MOUSEMOTION:
            # 处理鼠标移动
            pass
    
    def _handle_dropdown_click(self, item):
        """处理下拉菜单点击"""
        # 简单实现：循环切换选项
        current_index = item["options"].index(item["current"])
        next_index = (current_index + 1) % len(item["options"])
        item["current"] = item["options"][next_index]
        
        # 应用设置
        if item["id"] == "screen_size":
            # 更改屏幕尺寸
            size = item["current"].split("x")
            self.settings.screen_width = int(size[0])
            self.settings.screen_height = int(size[1])
            # 重新创建屏幕
            self.ai_game.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
            self.ai_game.screen_rect = self.ai_game.screen.get_rect()
            # 重新初始化UI元素
            self.rect.center = self.ai_game.screen_rect.center
            self._initialize_elements()
        elif item["id"] == "difficulty":
            # 更改游戏难度
            difficulty_map = {
                "简单": self.settings.DIFFICULTY_EASY,
                "普通": self.settings.DIFFICULTY_NORMAL,
                "困难": self.settings.DIFFICULTY_HARD,
                "专家": self.settings.DIFFICULTY_EXPERT
            }
            self.settings.game_difficulty = difficulty_map.get(item["current"], self.settings.DIFFICULTY_NORMAL)
            self.settings.initialize_dynamic_settings()
        elif item["id"] == "game_mode":
            # 更改游戏模式
            mode_map = {
                "普通模式": self.settings.MODE_NORMAL,
                "道具模式": self.settings.MODE_POWERUPS,
                "无限模式": self.settings.MODE_UNLIMITED,
                "Boss模式": self.settings.MODE_BOSS,
                "狙击模式": self.settings.MODE_SNIPER
            }
            self.settings.game_mode = mode_map.get(item["current"], self.settings.MODE_NORMAL)
            self.ai_game._apply_mode_settings()
        elif item["id"] == "frame_rate_value":
            # 更改帧率值
            self.settings.frame_rate_limit = int(item["current"])
    
    def handle_scroll(self, event):
        """处理滚动事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 向上滚动
                self.scroll_offset = max(0, self.scroll_offset - 20)
            elif event.button == 5:  # 向下滚动
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 20)
    
    def check_close_button(self, mouse_pos):
        """检查是否点击了关闭按钮"""
        return self.close_button.collidepoint(mouse_pos)