import pygame
import json
import os
from datetime import datetime

class GameReport:
    """游戏报告类，用于显示每局游戏的详细统计"""
    
    def __init__(self, ai_game):
        """初始化游戏报告"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.show_report = False
        self.current_page = 0
        self.total_pages = 3  # 总共3页：概览、道具统计、热力图
        
        # 按钮区域
        self.button_width = 120
        self.button_height = 40
        self.button_margin = 20
        
        # 页面导航按钮
        self.prev_button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 150,
            self.settings.screen_height - 80,
            self.button_width,
            self.button_height
        )
        self.next_button_rect = pygame.Rect(
            self.settings.screen_width // 2 + 30,
            self.settings.screen_height - 80,
            self.button_width,
            self.button_height
        )
        self.close_button_rect = pygame.Rect(
            self.settings.screen_width - 150,
            20,
            self.button_width,
            self.button_height
        )
        
        # 缓存字体
        self._cache_fonts()
    
    def _cache_fonts(self):
        """缓存字体"""
        try:
            self.title_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 48)
            self.header_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 28)
            self.normal_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 20)
            self.small_font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 16)
        except:
            try:
                self.title_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 48)
                self.header_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 28)
                self.normal_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 20)
                self.small_font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 16)
            except:
                self.title_font = pygame.font.Font(None, 48)
                self.header_font = pygame.font.Font(None, 28)
                self.normal_font = pygame.font.Font(None, 20)
                self.small_font = pygame.font.Font(None, 16)
    
    def show(self):
        """显示游戏报告"""
        self.show_report = True
        self.current_page = 0
        pygame.mouse.set_visible(True)
    
    def hide(self):
        """隐藏游戏报告"""
        self.show_report = False
        pygame.mouse.set_visible(False)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # 检查关闭按钮
            if self.close_button_rect.collidepoint(mouse_pos):
                self.hide()
                self.ai_game.sound_manager.play_sound('button_click')
                return True
            
            # 检查上一页按钮
            if self.prev_button_rect.collidepoint(mouse_pos) and self.current_page > 0:
                self.current_page -= 1
                self.ai_game.sound_manager.play_sound('button_click')
                return True
            
            # 检查下一页按钮
            if self.next_button_rect.collidepoint(mouse_pos) and self.current_page < self.total_pages - 1:
                self.current_page += 1
                self.ai_game.sound_manager.play_sound('button_click')
                return True
        
        return False
    
    def draw(self):
        """绘制游戏报告"""
        if not self.show_report:
            return
        
        # 绘制半透明背景
        self._draw_background()
        
        # 根据当前页面绘制内容
        if self.current_page == 0:
            self._draw_overview_page()
        elif self.current_page == 1:
            self._draw_powerup_page()
        elif self.current_page == 2:
            self._draw_heatmap_page()
        
        # 绘制页面导航
        self._draw_navigation()
    
    def _draw_background(self):
        """绘制半透明背景"""
        # 创建半透明表面
        background = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        background.fill((0, 0, 0))
        background.set_alpha(200)
        self.screen.blit(background, (0, 0))
        
        # 绘制报告边框
        border_rect = pygame.Rect(50, 50, self.settings.screen_width - 100, self.settings.screen_height - 150)
        pygame.draw.rect(self.screen, (100, 100, 150), border_rect, 3)
    
    def _draw_overview_page(self):
        """绘制概览页面"""
        # 标题
        title = self.title_font.render("游戏报告 - 概览", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=self.settings.screen_width // 2, top=80)
        self.screen.blit(title, title_rect)
        
        # 游戏模式
        mode_names = {
            'normal': '普通模式',
            'powerups': '道具模式',
            'unlimited': '无限火力',
            'boss': 'Boss模式',
            'sniper': '狙击模式'
        }
        mode_text = self.header_font.render(f"游戏模式: {mode_names.get(self.settings.game_mode, '未知')}", True, (255, 200, 100))
        self.screen.blit(mode_text, (100, 150))
        
        # 基本统计
        stats = [
            f"最终得分: {self.stats.score}",
            f"游戏时长: {self.stats.get_game_duration():.1f} 秒",
            f"最高关卡: {self.stats.level}",
            f"击杀外星人: {self.stats.aliens_killed}",
            f"击败Boss: {self.stats.bosses_defeated}",
            f"最大连击: {self.stats.max_combo}",
            f"命中率: {self.stats.get_accuracy():.1f}%",
            f"损失生命: {self.stats.total_lives_lost}"
        ]
        
        y_offset = 200
        for stat in stats:
            text = self.normal_font.render(stat, True, (255, 255, 255))
            self.screen.blit(text, (100, y_offset))
            y_offset += 35
        
        # 子弹统计
        bullet_stats = [
            f"发射子弹: {self.stats.bullet_stats['total_fired']}",
            f"命中子弹: {self.stats.bullet_stats['total_hits']}",
            f"未命中: {self.stats.bullet_stats['total_missed']}"
        ]
        
        y_offset += 20
        for stat in bullet_stats:
            text = self.normal_font.render(stat, True, (200, 200, 255))
            self.screen.blit(text, (100, y_offset))
            y_offset += 35
        
        # 关卡统计
        if self.stats.level_stats:
            y_offset += 20
            level_text = self.header_font.render(f"通关关卡: {len(self.stats.level_stats)}", True, (255, 200, 100))
            self.screen.blit(level_text, (100, y_offset))
            
            # 显示最近3关的统计
            recent_levels = self.stats.level_stats[-3:]
            y_offset += 40
            for level_stat in recent_levels:
                level_info = f"第{level_stat['level']}关: 击杀{level_stat['aliens_killed']}个, 用时{level_stat['duration']/1000:.1f}秒"
                text = self.small_font.render(level_info, True, (200, 255, 200))
                self.screen.blit(text, (120, y_offset))
                y_offset += 25
    
    def _draw_powerup_page(self):
        """绘制道具统计页面"""
        # 标题
        title = self.title_font.render("游戏报告 - 道具统计", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=self.settings.screen_width // 2, top=80)
        self.screen.blit(title, title_rect)
        
        # 道具名称映射
        powerup_names = {
            'shield': '护盾',
            'freeze': '时间冻结',
            'lightning': '闪电链',
            'laser': '激光束',
            'magnet': '磁力场',
            'teleport': '瞬移',
            'nuke': '核弹',
            'heal': '生命恢复',
            'slow_mo': '缓慢时间',
            'clone': '分身',
            'reflect': '护盾反射',
            'summon': '召唤支援',
            'spread_shot': '扫射'
        }
        
        # 统计使用的道具
        used_powerups = {k: v for k, v in self.stats.powerup_stats.items() if v['uses'] > 0}
        
        if not used_powerups:
            no_powerup_text = self.header_font.render("本局游戏未使用任何道具", True, (200, 200, 200))
            text_rect = no_powerup_text.get_rect(centerx=self.settings.screen_width // 2, centery=self.settings.screen_height // 2)
            self.screen.blit(no_powerup_text, text_rect)
            return
        
        # 显示道具统计
        y_offset = 150
        x_offset = 100
        
        for powerup_type, stats in used_powerups.items():
            powerup_name = powerup_names.get(powerup_type, powerup_type)
            
            # 道具名称和使用次数
            name_text = self.header_font.render(f"{powerup_name}: 使用{stats['uses']}次", True, (255, 200, 100))
            self.screen.blit(name_text, (x_offset, y_offset))
            
            # 道具详细统计
            y_offset += 35
            for key, value in stats.items():
                if key != 'uses' and value > 0:
                    # 格式化统计信息
                    if key == 'total_duration':
                        stat_text = f"  总时长: {value/1000:.1f}秒"
                    elif key == 'distance_traveled':
                        stat_text = f"  移动距离: {value:.0f}像素"
                    else:
                        stat_text = f"  {key}: {value}"
                    
                    text = self.normal_font.render(stat_text, True, (200, 200, 255))
                    self.screen.blit(text, (x_offset + 20, y_offset))
                    y_offset += 25
            
            # 计算并显示效率
            efficiency = self.stats.get_powerup_efficiency(powerup_type)
            efficiency_text = f"  效率: {efficiency:.2f}"
            eff_text = self.normal_font.render(efficiency_text, True, (100, 255, 100))
            self.screen.blit(eff_text, (x_offset + 20, y_offset))
            
            y_offset += 40
            
            # 换行显示
            if y_offset > self.settings.screen_height - 200:
                y_offset = 150
                x_offset += 400
    
    def _draw_heatmap_page(self):
        """绘制击杀热力图页面"""
        # 标题
        title = self.title_font.render("游戏报告 - 击杀热力图", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=self.settings.screen_width // 2, top=80)
        self.screen.blit(title, title_rect)
        
        # 获取热力图数据
        heatmap_data = self.stats.get_kill_heatmap_data()
        
        if not heatmap_data:
            no_data_text = self.header_font.render("本局游戏无击杀记录", True, (200, 200, 200))
            text_rect = no_data_text.get_rect(centerx=self.settings.screen_width // 2, centery=self.settings.screen_height // 2)
            self.screen.blit(no_data_text, text_rect)
            return
        
        # 计算最大值用于归一化
        max_kills = max(heatmap_data.values())
        
        # 绘制热力图
        heatmap_rect = pygame.Rect(100, 150, self.settings.screen_width - 200, self.settings.screen_height - 300)
        
        # 绘制背景
        pygame.draw.rect(self.screen, (30, 30, 30), heatmap_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), heatmap_rect, 2)
        
        # 绘制热力图网格
        grid_size = 50
        for (grid_x, grid_y), kills in heatmap_data.items():
            # 计算颜色强度（从蓝色到红色）
            intensity = kills / max_kills
            color = self._get_heatmap_color(intensity)
            
            # 计算在屏幕上的位置
            x = heatmap_rect.x + grid_x * grid_size
            y = heatmap_rect.y + grid_y * grid_size
            
            # 绘制热力图单元格
            cell_rect = pygame.Rect(x, y, grid_size, grid_size)
            
            # 创建带透明度的表面
            cell_surface = pygame.Surface((grid_size, grid_size))
            cell_surface.fill(color)
            cell_surface.set_alpha(int(100 + intensity * 155))
            self.screen.blit(cell_surface, cell_rect)
            
            # 绘制击杀数量
            if kills > 0:
                kill_text = self.small_font.render(str(kills), True, (255, 255, 255))
                text_rect = kill_text.get_rect(center=cell_rect.center)
                self.screen.blit(kill_text, text_rect)
        
        # 绘制图例
        self._draw_heatmap_legend(heatmap_rect)
        
        # 显示统计信息
        total_kills = self.stats.aliens_killed
        unique_positions = len(heatmap_data)
        avg_kills_per_position = total_kills / unique_positions if unique_positions > 0 else 0
        
        stats_text = [
            f"总击杀数: {total_kills}",
            f"击杀位置数: {unique_positions}",
            f"平均每位置击杀: {avg_kills_per_position:.1f}"
        ]
        
        y_offset = self.settings.screen_height - 130
        for stat in stats_text:
            text = self.normal_font.render(stat, True, (200, 200, 255))
            self.screen.blit(text, (100, y_offset))
            y_offset += 25
    
    def _get_heatmap_color(self, intensity):
        """根据强度获取热力图颜色"""
        # 从蓝色（低强度）到红色（高强度）的渐变
        if intensity < 0.25:
            # 蓝色到青色
            ratio = intensity / 0.25
            return (int(0 * (1 - ratio) + 0 * ratio), 
                    int(0 * (1 - ratio) + 255 * ratio), 
                    int(255 * (1 - ratio) + 255 * ratio))
        elif intensity < 0.5:
            # 青色到绿色
            ratio = (intensity - 0.25) / 0.25
            return (int(0 * (1 - ratio) + 0 * ratio), 
                    int(255 * (1 - ratio) + 255 * ratio), 
                    int(255 * (1 - ratio) + 0 * ratio))
        elif intensity < 0.75:
            # 绿色到黄色
            ratio = (intensity - 0.5) / 0.25
            return (int(0 * (1 - ratio) + 255 * ratio), 
                    int(255 * (1 - ratio) + 255 * ratio), 
                    int(0 * (1 - ratio) + 0 * ratio))
        else:
            # 黄色到红色
            ratio = (intensity - 0.75) / 0.25
            return (int(255 * (1 - ratio) + 255 * ratio), 
                    int(255 * (1 - ratio) + 0 * ratio), 
                    int(0 * (1 - ratio) + 0 * ratio))
    
    def _draw_heatmap_legend(self, heatmap_rect):
        """绘制热力图图例"""
        legend_x = heatmap_rect.right + 20
        legend_y = heatmap_rect.top
        legend_width = 20
        legend_height = 200
        
        # 绘制图例背景
        legend_rect = pygame.Rect(legend_x - 5, legend_y - 5, legend_width + 10, legend_height + 10)
        pygame.draw.rect(self.screen, (50, 50, 50), legend_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), legend_rect, 1)
        
        # 绘制颜色渐变
        for i in range(legend_height):
            intensity = 1 - (i / legend_height)
            color = self._get_heatmap_color(intensity)
            pygame.draw.line(self.screen, color, 
                           (legend_x, legend_y + i), 
                           (legend_x + legend_width, legend_y + i))
        
        # 绘制标签
        high_text = self.small_font.render("高", True, (255, 255, 255))
        self.screen.blit(high_text, (legend_x + legend_width + 5, legend_y))
        
        low_text = self.small_font.render("低", True, (255, 255, 255))
        self.screen.blit(low_text, (legend_x + legend_width + 5, legend_y + legend_height - 15))
    
    def _draw_navigation(self):
        """绘制页面导航按钮"""
        # 绘制关闭按钮
        self._draw_button(self.close_button_rect, "关闭", (200, 50, 50))
        
        # 绘制上一页按钮
        if self.current_page > 0:
            self._draw_button(self.prev_button_rect, "上一页", (100, 100, 200))
        
        # 绘制下一页按钮
        if self.current_page < self.total_pages - 1:
            self._draw_button(self.next_button_rect, "下一页", (100, 200, 100))
        
        # 绘制页码指示器
        page_text = self.normal_font.render(f"第 {self.current_page + 1} / {self.total_pages} 页", True, (255, 255, 255))
        page_rect = page_text.get_rect(centerx=self.settings.screen_width // 2, 
                                       bottom=self.settings.screen_height - 90)
        self.screen.blit(page_text, page_rect)
    
    def _draw_button(self, rect, text, color):
        """绘制按钮"""
        # 绘制按钮背景
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2, border_radius=5)
        
        # 绘制按钮文字
        text_surface = self.normal_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)