import pygame
from pygame.sprite import Sprite

class ObjectPool:
    """对象池管理类"""
    
    def __init__(self, object_class, initial_size=20):
        """
        初始化对象池
        
        Args:
            object_class: 要管理的对象类
            initial_size: 初始池大小
        """
        self.object_class = object_class
        self.pool = []
        self.active_objects = []
        
        # 预创建一些对象
        for _ in range(initial_size):
            try:
                # 尝试创建对象实例
                obj = object_class(None)  # 传递None作为临时参数
                self.pool.append(obj)
            except:
                # 如果创建失败，添加None
                self.pool.append(None)
    
    def get(self, *args, **kwargs):
        """
        从对象池获取一个对象
        
        Args:
            *args: 传递给对象构造函数的位置参数
            **kwargs: 传递给对象构造函数的关键字参数
        
        Returns:
            一个对象实例
        """
        # 尝试从池中获取空闲对象
        if self.pool:
            obj = self.pool.pop()
            if obj is not None:
                # 重置对象状态
                self._reset_object(obj, *args, **kwargs)
                self.active_objects.append(obj)
                return obj
        
        # 如果池中没有空闲对象，创建新对象
        obj = self.object_class(*args, **kwargs)
        self.active_objects.append(obj)
        return obj
    
    def _reset_object(self, obj, *args, **kwargs):
        """
        重置对象状态
        
        Args:
            obj: 要重置的对象
            *args: 传递给对象构造函数的位置参数
            **kwargs: 传递给对象构造函数的关键字参数
        """
        if hasattr(obj, 'reset'):
            obj.reset(*args, **kwargs)
        else:
            # 如果对象没有reset方法，重新初始化
            obj.__init__(*args, **kwargs)
    
    def recycle(self, obj):
        """
        回收对象到池中
        
        Args:
            obj: 要回收的对象
        """
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            # 确保池的大小不超过最大值
            if len(self.pool) < 100:  # 最大池大小
                self.pool.append(obj)
    
    def recycle_all(self):
        """
        回收所有活动对象
        """
        for obj in self.active_objects[:]:
            self.recycle(obj)
    
    def get_active(self):
        """
        获取所有活动对象
        
        Returns:
            活动对象列表
        """
        return self.active_objects
    
    def clear(self):
        """
        清空对象池
        """
        self.pool.clear()
        self.active_objects.clear()

class BulletPool(ObjectPool):
    """子弹对象池"""
    
    def __init__(self, initial_size=50):
        """
        初始化子弹对象池
        
        Args:
            initial_size: 初始池大小
        """
        from bullet import Bullet
        super().__init__(Bullet, initial_size)

class AlienPool(ObjectPool):
    """外星人对象池"""
    
    def __init__(self, initial_size=30):
        """
        初始化外星人对象池
        
        Args:
            initial_size: 初始池大小
        """
        from alien import Alien
        super().__init__(Alien, initial_size)

class AlienBulletPool(ObjectPool):
    """外星人子弹对象池"""
    
    def __init__(self, initial_size=50):
        """
        初始化外星人子弹对象池
        
        Args:
            initial_size: 初始池大小
        """
        from alien_bullet import AlienBullet
        super().__init__(AlienBullet, initial_size)