import pygame.font
import os

class Button:
    """为游戏创建按钮的类"""
    def __init__(self, ai_game, msg, width=200, height=50, button_color=(0, 255, 0), center_pos=None):
        """初始化按钮的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.ai_game = ai_game

        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if center_pos:
            self.rect.center = center_pos
        else:
            self.rect.center = self.screen_rect.center

        self.font = self._load_font()
        self._prep_msg(msg)

        self.hovered = False
        self.clicked = False
        self.click_timer = 0
        self.scale_factor = 1.0
        self.target_scale = 1.0

        self.corner_radius = min(10, min(width, height) // 4)
        self.shadow_offset = 4
        self.shadow_color = (0, 0, 0, 100)
        
        # 缓存已创建的渐变表面
        self.gradient_cache = {}

    def _load_font(self):
        """加载支持中文的字体"""
        # Windows系统中的中文字体路径
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
        ]
        
        # 根据按钮高度计算合适的字体大小
        font_size = int(self.height * 0.7)  # 字体大小为按钮高度的70%
        
        # 尝试加载中文字体
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, font_size)
                except:
                    continue
        
        # 如果加载失败，使用默认字体
        return pygame.font.Font(None, font_size)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        # 不设置背景色，让文字直接显示在渐变背景上
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _create_gradient_surface(self, color, width, height):
        """创建带圆角的渐变表面"""
        # 创建主表面
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 创建渐变
        r, g, b = color
        for y in range(height):
            factor = y / height
            new_r = int(r * (1 - factor * 0.3))
            new_g = int(g * (1 - factor * 0.3))
            new_b = int(b * (1 - factor * 0.3))
            pygame.draw.line(surface, (new_r, new_g, new_b, 255), (0, y), (width, y))
        
        # 创建带圆角的结果表面
        result = pygame.Surface((width, height), pygame.SRCALPHA)
        # 使用 pygame.draw.rect 直接绘制圆角矩形
        pygame.draw.rect(result, (255, 255, 255, 255), result.get_rect(), border_radius=self.corner_radius)
        # 使用 BLENDMODE 只保留圆角区域
        result.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        return result

    def _draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def _draw_shadow(self, surface, rect, offset, color):
        shadow_rect = rect.copy()
        shadow_rect.x += offset
        shadow_rect.y += offset
        
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, color, shadow_surface.get_rect(), border_radius=self.corner_radius)
        surface.blit(shadow_surface, shadow_rect.topleft)

    def _draw_glow(self, surface, rect, color):
        glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        glow_rect = glow_surface.get_rect()
        
        for i in range(10, 0, -1):
            alpha = 15 - i
            glow_color = (*color[:3], alpha)
            offset = 10 - i
            glow_rect_inflated = glow_rect.inflate(-offset * 2, -offset * 2)
            pygame.draw.rect(glow_surface, glow_color, glow_rect_inflated, border_radius=self.corner_radius)
        
        surface.blit(glow_surface, (rect.x - 10, rect.y - 10))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
        
        self.scale_factor += (self.target_scale - self.scale_factor) * 0.2
        
        if self.clicked:
            self.click_timer -= 1
            if self.click_timer <= 0:
                self.clicked = False

    def draw_button(self):
        scaled_width = int(self.width * self.scale_factor)
        scaled_height = int(self.height * self.scale_factor)
        scaled_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        scaled_rect.center = self.rect.center
        
        if self.clicked:
            draw_rect = scaled_rect.copy()
            draw_rect.x += 2
            draw_rect.y += 2
        else:
            draw_rect = scaled_rect
        
        self._draw_shadow(self.screen, draw_rect, self.shadow_offset, self.shadow_color)
        
        if self.hovered:
            self._draw_glow(self.screen, draw_rect, self.button_color)
        
        # 使用缓存的渐变表面
        cache_key = (scaled_width, scaled_height, self.button_color)
        if cache_key not in self.gradient_cache:
            self.gradient_cache[cache_key] = self._create_gradient_surface(self.button_color, scaled_width, scaled_height)
        
        gradient_surface = self.gradient_cache[cache_key]
        self.screen.blit(gradient_surface, draw_rect.topleft)
        
        border_color = self._brighten_color(self.button_color, 30) if self.hovered else self._darken_color(self.button_color, 20)
        pygame.draw.rect(self.screen, border_color, draw_rect, border_radius=self.corner_radius, width=2)
        
        # 缓存缩放后的消息图像
        msg_cache_key = (scaled_width, scaled_height)
        if not hasattr(self, 'msg_cache'):
            self.msg_cache = {}
        
        if msg_cache_key not in self.msg_cache:
            scaled_msg_width = int(self.msg_image.get_width() * self.scale_factor)
            scaled_msg_height = int(self.msg_image.get_height() * self.scale_factor)
            self.msg_cache[msg_cache_key] = pygame.transform.scale(self.msg_image, (scaled_msg_width, scaled_msg_height))
        
        scaled_msg = self.msg_cache[msg_cache_key]
        scaled_msg_rect = scaled_msg.get_rect()
        scaled_msg_rect.center = draw_rect.center
        
        self.screen.blit(scaled_msg, scaled_msg_rect)

    def _brighten_color(self, color, amount):
        r = min(255, color[0] + amount)
        g = min(255, color[1] + amount)
        b = min(255, color[2] + amount)
        return (r, g, b)

    def _darken_color(self, color, amount):
        r = max(0, color[0] - amount)
        g = max(0, color[1] - amount)
        b = max(0, color[2] - amount)
        return (r, g, b)

    def trigger_click(self):
        self.clicked = True
        self.click_timer = 10
