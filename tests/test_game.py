import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import Settings
from game_stats import GameStats

class TestGame(unittest.TestCase):
    """测试游戏核心功能"""
    
    def test_settings_initialization(self):
        """测试设置初始化"""
        settings = Settings()
        self.assertIsInstance(settings, Settings)
        self.assertGreater(settings.screen_width, 0)
        self.assertGreater(settings.screen_height, 0)
    
    def test_game_stats_initialization(self):
        """测试游戏统计信息初始化"""
        settings = Settings()
        stats = GameStats(None)
        self.assertIsInstance(stats, GameStats)
        self.assertTrue(stats.game_active)
        self.assertEqual(stats.score, 0)

if __name__ == '__main__':
    unittest.main()
