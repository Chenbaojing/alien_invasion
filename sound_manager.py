import pygame
import os

class SoundManager:
    """音效管理器类，负责加载和播放游戏音效"""
    
    def __init__(self):
        """初始化音效管理器"""
        pygame.mixer.init()
        
        # 音效音量 (0.0 - 1.0)
        self.sfx_volume = 0.7
        # 背景音乐音量 (0.0 - 1.0)
        self.music_volume = 0.5
        # 音效开关
        self.sfx_enabled = True
        # 背景音乐开关
        self.music_enabled = True
        
        # 音效字典
        self.sounds = {}
        # 背景音乐
        self.background_music = None
        
        # 加载所有音效
        self._load_sounds()
        # 加载背景音乐
        self._load_background_music()
    
    def _load_sounds(self):
        """加载所有音效文件"""
        sound_files = {
            'shoot': 'sounds/射击.mp3',
            'button_click': 'sounds/按按钮.mp3',
            'game_over': 'sounds/游戏结束.mp3',
            'explosion': 'sounds/爆炸.mp3',
            'ship_hit': 'sounds/飞船被击中.mp3'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                except Exception as e:
                    print(f"加载音效 {path} 失败: {e}")
            else:
                print(f"音效文件不存在: {path}")
    
    def _load_background_music(self):
        """加载背景音乐"""
        music_path = 'sounds/背景音乐.mp3'
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception as e:
                print(f"加载背景音乐失败: {e}")
        else:
            print(f"背景音乐文件不存在: {music_path}")
    
    def play_sound(self, sound_name):
        """播放指定音效"""
        if not self.sfx_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"播放音效 {sound_name} 失败: {e}")
    
    def play_background_music(self, loops=-1):
        """播放背景音乐
        
        Args:
            loops: 循环次数，-1表示无限循环
        """
        if not self.music_enabled:
            return
        
        try:
            pygame.mixer.music.play(loops=loops)
        except Exception as e:
            print(f"播放背景音乐失败: {e}")
    
    def stop_background_music(self):
        """停止背景音乐"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"停止背景音乐失败: {e}")
    
    def pause_background_music(self):
        """暂停背景音乐"""
        try:
            pygame.mixer.music.pause()
        except Exception as e:
            print(f"暂停背景音乐失败: {e}")
    
    def resume_background_music(self):
        """恢复背景音乐"""
        if not self.music_enabled:
            return
        
        try:
            pygame.mixer.music.unpause()
        except Exception as e:
            print(f"恢复背景音乐失败: {e}")
    
    def set_sfx_volume(self, volume):
        """设置音效音量
        
        Args:
            volume: 音量值 (0.0 - 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """设置背景音乐音量
        
        Args:
            volume: 音量值 (0.0 - 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_sfx(self):
        """切换音效开关"""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled
    
    def toggle_music(self):
        """切换背景音乐开关"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_background_music()
        else:
            self.play_background_music()
        return self.music_enabled
    
    def is_music_playing(self):
        """检查背景音乐是否正在播放"""
        return pygame.mixer.music.get_busy()
