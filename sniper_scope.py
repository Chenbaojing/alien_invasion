import pygame

class SniperScope:
    """狙击模式瞄准镜类"""
    
    def __init__(self, ai_game):
        """初始化瞄准镜"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # 瞄准镜位置（初始在屏幕中心）
        self.x = self.settings.screen_width // 2
        self.y = self.settings.screen_height // 2
        
        # 瞄准镜颜色和大小
        self.color = (255, 0, 0)  # 红色
        self.crosshair_size = 20  # 准星大小
        self.circle_radius = 15  # 圆圈半径
        self.line_length = 30  # 线条长度
        self.line_width = 2  # 线条宽度
        
        # 是否显示瞄准镜
        self.visible = False
    
    def update_position(self, mouse_pos):
        """更新瞄准镜位置到鼠标位置"""
        self.x, self.y = mouse_pos
    
    def draw(self):
        """绘制瞄准镜"""
        if not self.visible:
            return
        
        # 绘制准星圆圈
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.circle_radius, self.line_width)
        
        # 绘制十字准星
        # 水平线
        pygame.draw.line(self.screen, self.color, 
                        (self.x - self.line_length, self.y), 
                        (self.x + self.line_length, self.y), 
                        self.line_width)
        # 垂直线
        pygame.draw.line(self.screen, self.color, 
                        (self.x, self.y - self.line_length), 
                        (self.x, self.y + self.line_length), 
                        self.line_width)
        
        # 绘制中心点
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 2)
        
        # 绘制四个角落的辅助线（可选，增加狙击感）
        corner_offset = 5
        corner_length = 10
        # 左上
        pygame.draw.line(self.screen, self.color,
                        (self.x - corner_offset, self.y - corner_offset - corner_length),
                        (self.x - corner_offset, self.y - corner_offset),
                        self.line_width)
        pygame.draw.line(self.screen, self.color,
                        (self.x - corner_offset - corner_length, self.y - corner_offset),
                        (self.x - corner_offset, self.y - corner_offset),
                        self.line_width)
        # 右上
        pygame.draw.line(self.screen, self.color,
                        (self.x + corner_offset, self.y - corner_offset - corner_length),
                        (self.x + corner_offset, self.y - corner_offset),
                        self.line_width)
        pygame.draw.line(self.screen, self.color,
                        (self.x + corner_offset + corner_length, self.y - corner_offset),
                        (self.x + corner_offset, self.y - corner_offset),
                        self.line_width)
        # 左下
        pygame.draw.line(self.screen, self.color,
                        (self.x - corner_offset, self.y + corner_offset + corner_length),
                        (self.x - corner_offset, self.y + corner_offset),
                        self.line_width)
        pygame.draw.line(self.screen, self.color,
                        (self.x - corner_offset - corner_length, self.y + corner_offset),
                        (self.x - corner_offset, self.y + corner_offset),
                        self.line_width)
        # 右下
        pygame.draw.line(self.screen, self.color,
                        (self.x + corner_offset, self.y + corner_offset + corner_length),
                        (self.x + corner_offset, self.y + corner_offset),
                        self.line_width)
        pygame.draw.line(self.screen, self.color,
                        (self.x + corner_offset + corner_length, self.y + corner_offset),
                        (self.x + corner_offset, self.y + corner_offset),
                        self.line_width)
    
    def get_position(self):
        """获取瞄准镜当前位置"""
        return (self.x, self.y)
    
    def set_visible(self, visible):
        """设置瞄准镜是否可见"""
        self.visible = visible