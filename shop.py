import pygame
import json
import os

class Shop:
    """游戏商店系统，用于购买皮肤"""
    
    def __init__(self, ai_game):
        """初始化商店"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.shop_active = False
        
        # 加载已购买的物品
        self.purchased_items = self._load_purchased_items()
        self.current_skin = self._load_current_skin()
        
        # 商店物品数据
        self.skins = [
            {"id": "default", "name": "默认皮肤", "price": 0, "image": "images/ship.bmp", "owned": True},
            {"id": "ship_1", "name": "皮肤1", "price": 5, "image": "images/ship_1.bmp", "owned": False},
            {"id": "ship_2", "name": "皮肤2", "price": 5, "image": "images/ship_2.bmp", "owned": False},
            {"id": "ship_3", "name": "皮肤3", "price": 5, "image": "images/ship_3.png", "owned": False},
            {"id": "ship_4", "name": "皮肤4", "price": 5, "image": "images/ship_4.bmp", "owned": False},
            {"id": "ship_5", "name": "皮肤5", "price": 5, "image": "images/ship_5.bmp", "owned": False},
            {"id": "ship_6", "name": "皮肤6", "price": 10, "image": "images/ship_6.bmp", "owned": False},
            {"id": "ship_7", "name": "皮肤7", "price": 10, "image": "images/ship_7.bmp", "owned": False},
            {"id": "ship_8", "name": "皮肤8", "price": 10, "image": "images/ship_8.bmp", "owned": False},
            {"id": "ship_9", "name": "皮肤9", "price": 10, "image": "images/ship_9.bmp", "owned": False},
            {"id": "ship_10", "name": "皮肤10", "price": 15, "image": "images/ship_10.bmp", "owned": False},
            {"id": "ship_11", "name": "皮肤11", "price": 15, "image": "images/ship_11.bmp", "owned": False},
            {"id": "ship_12", "name": "皮肤12", "price": 15, "image": "images/ship_12.bmp", "owned": False},
            {"id": "ship_13", "name": "皮肤13", "price": 20, "image": "images/ship_13.bmp", "owned": False},
            {"id": "ship_14", "name": "皮肤14", "price": 20, "image": "images/ship_14.bmp", "owned": False},
            {"id": "ship_15", "name": "皮肤15", "price": 20, "image": "images/ship_15.bmp", "owned": False},
            {"id": "ship_16", "name": "皮肤16", "price": 25, "image": "images/ship_16.bmp", "owned": False},
            {"id": "ship_17", "name": "皮肤17", "price": 25, "image": "images/ship_17.bmp", "owned": False},
            {"id": "ship_18", "name": "皮肤18", "price": 25, "image": "images/ship_18.bmp", "owned": False},
            {"id": "ship_19", "name": "皮肤19", "price": 30, "image": "images/ship_19.bmp", "owned": False},
            {"id": "ship_20", "name": "皮肤20", "price": 30, "image": "images/ship_20.bmp", "owned": False},
        ]
        
        # 同步已购买的物品状态
        for skin in self.skins:
            if skin['id'] in self.purchased_items:
                skin['owned'] = True
        
        # 创建按钮
        self._create_buttons()
        
        # 字体
        self.title_font = self._load_font(48)
        self.item_font = self._load_font(32)
        
        # 加载货币图像
        try:
            self.money_image = pygame.image.load('images/money.png').convert_alpha()
            # 缩放货币图像到合适大小
            self.money_image = pygame.transform.scale(self.money_image, (24, 24))
        except:
            self.money_image = None
        
        # 背景遮罩
        self.overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)
        
        # 滚动偏移
        self.scroll_offset = 0
        self.max_scroll = 0
    
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
    
    def _create_buttons(self):
        """创建商店按钮"""
        screen_center_x = self.settings.screen_width // 2
        screen_center_y = self.settings.screen_height // 2
        
        # 关闭按钮
        self.close_button = self._create_button("关闭", 120, 40, (200, 50, 50), 
                                               (screen_center_x, 500))
        
        # 物品按钮
        self.item_buttons = []
        for i in range(21):
            y_pos = 180 + i * 45
            btn = self._create_button("", 500, 40, (80, 80, 80), (screen_center_x, y_pos))
            self.item_buttons.append(btn)
    
    def _create_button(self, text, width, height, color, pos):
        """创建简单的按钮"""
        from button import Button
        return Button(self.ai_game, text, width, height, color, pos)
    
    def _load_purchased_items(self):
        """加载已购买的物品"""
        try:
            with open('personal information/purchased_items.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_purchased_items(self):
        """保存已购买的物品"""
        with open('personal information/purchased_items.json', 'w') as f:
            json.dump(self.purchased_items, f)
    
    def _load_current_skin(self):
        """加载当前使用的皮肤"""
        try:
            with open('personal information/current_skin.json', 'r') as f:
                data = json.load(f)
                return data if isinstance(data, str) else "default"
        except (FileNotFoundError, json.JSONDecodeError):
            return "default"
    
    def _save_current_skin(self):
        """保存当前使用的皮肤"""
        with open('personal information/current_skin.json', 'w') as f:
            json.dump(self.current_skin, f)
    
    def update(self):
        """更新商店状态"""
        if not self.shop_active:
            return
        
        self.close_button.update()
        
        for btn in self.item_buttons:
            btn.update()
    
    def handle_event(self, event):
        """处理商店事件"""
        if not self.shop_active:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检查关闭按钮
                if self.close_button.rect.collidepoint(event.pos):
                    self.shop_active = False
                    self.close_button.trigger_click()
                    return True
                
                # 检查物品按钮
                for i, btn in enumerate(self.item_buttons):
                    # 根据滚动偏移计算实际显示位置
                    display_y = 180 + i * 45 - self.scroll_offset
                    display_rect = btn.rect.copy()
                    display_rect.y = display_y
                    
                    # 只检测可见的按钮
                    if display_y < 150 or display_y > self.settings.screen_height - 100:
                        continue
                    
                    if display_rect.collidepoint(event.pos):
                        self._handle_item_click(i)
                        btn.trigger_click()
                        return True
            
            elif event.button == 4:  # 鼠标滚轮向上
                self.scroll_offset = max(0, self.scroll_offset - 50)
            
            elif event.button == 5:  # 鼠标滚轮向下
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 50)
        
        return False
    
    def _handle_item_click(self, index):
        """处理物品点击"""
        # 皮肤
        if index < len(self.skins):
            skin = self.skins[index]
            if skin['owned']:
                self.current_skin = skin['id']
                self._save_current_skin()
                self._apply_skin()
            elif self.stats.spend_currency(skin['price']):
                skin['owned'] = True
                self.purchased_items.append(skin['id'])
                self._save_purchased_items()
                # 购买后自动应用该皮肤
                self.current_skin = skin['id']
                self._save_current_skin()
                self._apply_skin()
                # 更新主页面货币显示
                if hasattr(self.ai_game, 'sb'):
                    self.ai_game.sb.prep_currency()
    
    def _apply_skin(self):
        """应用皮肤"""
        skin = next((s for s in self.skins if s['id'] == self.current_skin), self.skins[0])
        self.settings.ship_image = skin['image']
    
    def draw(self):
        """绘制商店界面"""
        if not self.shop_active:
            return
        
        # 绘制遮罩
        self.screen.blit(self.overlay, (0, 0))
        
        # 绘制标题
        title_text = self.title_font.render("商店", True, (255, 255, 255))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = 30
        self.screen.blit(title_text, title_rect)
        
        # 绘制货币显示
        currency_str = str(self.stats.currency)
        currency_text = self.item_font.render(currency_str, True, (255, 215, 0))
        currency_rect = currency_text.get_rect()
        currency_rect.topright = (self.screen_rect.right - 20, 30)
        
        if self.money_image:
            money_rect = self.money_image.get_rect()
            money_rect.right = currency_rect.left - 5
            money_rect.centery = currency_rect.centery
            self.screen.blit(self.money_image, money_rect)
        
        self.screen.blit(currency_text, currency_rect)
        
        # 绘制物品
        self._draw_items()
        
        # 绘制关闭按钮
        self.close_button.draw_button()
    
    def _draw_items(self):
        """绘制物品列表"""
        items = self.skins
        
        # 计算最大滚动偏移
        items_height = len(items) * 45
        visible_height = self.settings.screen_height - 250
        self.max_scroll = max(0, items_height - visible_height)
        
        # 先清空所有按钮
        for btn in self.item_buttons:
            btn.msg_image = btn.font.render("", True, btn.text_color)
            btn.msg_image_rect = btn.msg_image.get_rect()
            btn.msg_image_rect.center = btn.rect.center
        
        for i, item in enumerate(items):
            if i >= len(self.item_buttons):
                break
            
            btn = self.item_buttons[i]
            
            # 根据滚动偏移调整按钮位置
            btn.rect.y = 180 + i * 45 - self.scroll_offset
            
            # 只绘制可见的按钮
            if btn.rect.y < 150 or btn.rect.y > self.settings.screen_height - 100:
                continue
            
            # 更新按钮文本
            if item['owned']:
                if item['id'] == self.current_skin:
                    btn_text = f"{item['name']} (使用中)"
                else:
                    btn_text = f"{item['name']} (已拥有)"
                btn_color = (100, 200, 100)
            else:
                btn_text = f"{item['name']} - ${item['price']}"
                btn_color = (80, 80, 80)
            
            # 重新准备按钮文本
            btn.msg_image = btn.font.render(btn_text, True, btn.text_color)
            btn.msg_image_rect = btn.msg_image.get_rect()
            btn.msg_image_rect.center = btn.rect.center
            
            btn.draw_button()