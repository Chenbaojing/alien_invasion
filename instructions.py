import pygame.font
import os

class Instructions:
    """显示游戏使用说明的类"""
    def __init__(self, ai_game):
        """初始化使用说明的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.ai_game = ai_game

        # 设置面板的尺寸和颜色
        self.panel_width = 600  # 面板宽度
        self.panel_height = 450  # 面板高度
        self.panel_color = (50, 50, 50)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)

        # 创建面板的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.panel_width, self.panel_height)
        self.rect.center = self.screen_rect.center

        # 设置支持中文的字体
        self._load_fonts()

        # 创建关闭按钮（叉号）
        self.close_button_size = 30
        self.close_button_rect = pygame.Rect(
            self.rect.right - self.close_button_size - 10,
            self.rect.top + 10,
            self.close_button_size,
            self.close_button_size
        )
        self.close_button_color = (200, 50, 50)

        # 翻页相关
        self.current_page = 0
        self.total_pages = 9
        
        # 创建翻页按钮
        self.prev_button_rect = pygame.Rect(
            self.rect.left + 20,
            self.rect.bottom - 40,
            80,
            30
        )
        self.next_button_rect = pygame.Rect(
            self.rect.right - 100,
            self.rect.bottom - 40,
            80,
            30
        )
        self.button_color = (100, 150, 200)
        self.button_text_color = (255, 255, 255)

        # 准备页面文本
        self._prep_pages()

    def _load_fonts(self):
        """加载支持中文的字体"""
        # Windows系统中的中文字体路径
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
            "C:/Windows/Fonts/msyhl.ttc",  # 微软雅黑Light
        ]
        
        # 尝试加载中文字体
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.title_font = pygame.font.Font(font_path, 56)
                    self.text_font = pygame.font.Font(font_path, 32)
                    self.small_font = pygame.font.Font(font_path, 26)
                    font_loaded = True
                    break
                except Exception as e:
                    continue
        
        # 如果加载失败，使用默认字体
        if not font_loaded:
            self.title_font = pygame.font.Font(None, 56)
            self.text_font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 26)

    def _prep_pages(self):
        """准备多页文本内容"""
        # 页面内容
        self.pages = [
            # 第1页：基本操作
            {
                "title": "基本操作",
                "content": [
                    "← → : 移动飞船",
                    "空格键 : 发射子弹",
                ]
            },
            # 第2页：道具操作（基础）
            {
                "title": "道具操作(1/3)",
                "content": [
                    "Shift键 : 扫射(5发,冷却10秒)",
                    "1键 : 激活护盾(5秒,冷却15秒)",
                    "2键 : 时间冻结(3秒,冷却20秒)",
                    "",
                    "注: 仅在道具和无限火力模式可用"
                ]
            },
            # 第3页：道具操作（攻击类）
            {
                "title": "道具操作(2/3)",
                "content": [
                    "3键 : 闪电链(跳跃5次,冷却25秒)",
                    "4键 : 激光束(贯穿屏幕,冷却30秒)",
                    "5键 : 磁力场(吸引外星人,冷却20秒)",
                    "6键 : 瞬移(随机移动,冷却15秒)",
                    "7键 : 核弹(清除所有外星人,冷却60秒)"
                ]
            },
            # 第4页：道具操作（辅助类）
            {
                "title": "道具操作(3/3)",
                "content": [
                    "8键 : 生命恢复(加1条命,冷却45秒)",
                    "9键 : 缓慢时间(减速30%,冷却25秒)",
                    "0键 : 分身(复制飞船,冷却35秒)",
                    "",
                    "注: 仅在道具和无限火力模式可用"
                ]
            },
            # 第5页：游戏模式和玩法
            {
                "title": "游戏模式",
                "content": [
                    "普通模式: 无道具",
                    "道具模式: 有护盾、冻结、扫射",
                    "无限火力: 子弹不限量",
                    "",
                    "游戏玩法:",
                    "1. 选择模式,点击Play开始",
                    "2. 移动飞船,发射子弹",
                    "3. 消灭所有外星人过关",
                    "4. 外星人到达底部则失败"
                ]
            },
            # 第6页：特殊外星人(1/2)
            {
                "title": "特殊外星人(1/2)",
                "content": [
                    "快速型(黄色): 移动速度快",
                    "坦克型(紫色): 需多次攻击,会发射子弹",
                    "治疗型(青色): 每20秒治疗坦克型",
                    "分裂型(橙色): 每30秒分裂普通外星人",
                    "隐形型(灰色): 每5秒切换隐形状态",
                    "传送型(紫色): 每8秒传送到新位置",
                    "",
                    "解锁等级:",
                    "快速型: 3级",
                    "坦克型: 5级",
                    "治疗型: 7级",
                ]
            },
            # 第7页：特殊外星人（2/2）
            {
                "title": "特殊外星人(2/2)",
                "content": [
                    "分裂型: 10级",
                    "隐形型: 12级",
                    "传送型: 15级"
                ]
            },

            # 第7页：Boss模式（基本规则）
            {
                "title": "Boss模式(1/2)",
                "content": [
                    "五关Boss战,每关一个Boss",
                    "Boss每10秒发射子弹攻击",
                    "Boss每10秒生成随机外星人",
                    "Boss原地停10分钟后前进",
                    "",
                    "Boss储备系统:",
                    "第1关: 200子弹,50外星人",
                    "每关子弹+50,外星人+20",
                    "储备用尽后不再生成"
                ]
            },
            # 第8页：Boss模式（模式特性）
            {
                "title": "Boss模式(2/2)",
                "content": [
                    "难度递增:",
                    "第1关: 200血,速度0.09",
                    "每关血量*1.5,速度+0.01",
                    "",
                    "模式特性:",
                    "可使用所有道具",
                    "子弹无限量",
                    "核弹对Boss造成100点伤害",
                    "",
                    "通关条件:",
                    "击败当前Boss进入下一关",
                    "击败第5关Boss通关"
                ]
            },
            # 第9页：娱乐模式
            {
                "title": "娱乐模式",
                "content": [
                    "猜字母: 经典的猜单词游戏",
                    "颠球: 控制 paddle 反弹球",
                    "飞船着陆: 控制飞船安全着陆",
                    "",
                    "注: 点击娱乐模式按钮进入"
                ]
            }
        ]
        
        self.total_pages = len(self.pages)

    def check_close_button(self, mouse_pos):
        """检查是否点击了关闭按钮"""
        if self.close_button_rect.collidepoint(mouse_pos):
            self.ai_game.sound_manager.play_sound('button_click')
            return True
        return False

    def check_page_buttons(self, mouse_pos):
        """检查是否点击了翻页按钮"""
        if self.prev_button_rect.collidepoint(mouse_pos) and self.current_page > 0:
            self.ai_game.sound_manager.play_sound('button_click')
            self.current_page -= 1
        elif self.next_button_rect.collidepoint(mouse_pos) and self.current_page < self.total_pages - 1:
            self.ai_game.sound_manager.play_sound('button_click')
            self.current_page += 1

    def draw_instructions(self):
        """绘制使用说明面板"""
        # 绘制面板背景
        self.screen.fill(self.panel_color, self.rect)
        # 绘制边框
        pygame.draw.rect(self.screen, self.border_color, self.rect, 3)

        # 获取当前页面内容
        current_page_data = self.pages[self.current_page]
        
        # 绘制页面标题
        title_surface = self.title_font.render(current_page_data["title"], True, self.text_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.top = self.rect.top + 20
        self.screen.blit(title_surface, title_rect)

        # 绘制页面内容
        text_start_y = title_rect.bottom + 25  # 标题下方25像素
        current_y = text_start_y
        
        for line in current_page_data["content"]:
            if line:
                # 普通文本行
                text_surface = self.small_font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect()
                text_rect.left = self.rect.left + 40
                text_rect.top = current_y
                self.screen.blit(text_surface, text_rect)
                current_y += 28
            else:
                # 空行
                current_y += 15

        # 绘制关闭按钮（叉号）
        self.screen.fill(self.close_button_color, self.close_button_rect)
        
        # 绘制叉号
        line_width = 2
        center_x = self.close_button_rect.centerx
        center_y = self.close_button_rect.centery
        radius = 8
        
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (center_x - radius, center_y - radius), 
                        (center_x + radius, center_y + radius), line_width)
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (center_x + radius, center_y - radius), 
                        (center_x - radius, center_y + radius), line_width)

        # 绘制翻页按钮
        
        # 上一页按钮
        if self.current_page > 0:
            pygame.draw.rect(self.screen, self.button_color, self.prev_button_rect)
            prev_text = self.small_font.render("上一页", True, self.button_text_color)
            prev_text_rect = prev_text.get_rect()
            prev_text_rect.center = self.prev_button_rect.center
            self.screen.blit(prev_text, prev_text_rect)
        
        # 下一页按钮
        if self.current_page < self.total_pages - 1:
            pygame.draw.rect(self.screen, self.button_color, self.next_button_rect)
            next_text = self.small_font.render("下一页", True, self.button_text_color)
            next_text_rect = next_text.get_rect()
            next_text_rect.center = self.next_button_rect.center
            self.screen.blit(next_text, next_text_rect)
        
        # 绘制页码指示器
        page_info = f"第 {self.current_page + 1} / {self.total_pages} 页"
        page_info_surface = self.small_font.render(page_info, True, self.text_color)
        page_info_rect = page_info_surface.get_rect()
        page_info_rect.centerx = self.rect.centerx
        page_info_rect.top = self.rect.bottom - 35
        self.screen.blit(page_info_surface, page_info_rect)
