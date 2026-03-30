from PIL import Image
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'images')

# 定义文件路径
ship_bmp_path = os.path.join(images_dir, 'ship.bmp')
ship_1_path = os.path.join(images_dir, 'ship_1.bmp')
ship_2_path = os.path.join(images_dir, 'ship_2.bmp')

try:
    # 打开 ship.bmp 并获取其大小
    with Image.open(ship_bmp_path) as ship_img:
        ship_size = ship_img.size
        print(f"ship.bmp 的大小: {ship_size}")
    
    # 调整 ship_1.bmp 的大小
    with Image.open(ship_1_path) as ship_1_img:
        resized_ship_1 = ship_1_img.resize(ship_size)
        resized_ship_1.save(ship_1_path)
        print(f"已将 ship_1.bmp 调整为大小: {ship_size}")
    
    # 调整 ship_2.bmp 的大小
    with Image.open(ship_2_path) as ship_2_img:
        resized_ship_2 = ship_2_img.resize(ship_size)
        resized_ship_2.save(ship_2_path)
        print(f"已将 ship_2.bmp 调整为大小: {ship_size}")
    
    print("调整完成！")
except Exception as e:
    print(f"调整过程中出现错误: {e}")
