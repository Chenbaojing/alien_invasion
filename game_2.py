import pygame
import random
import sys

# 初始化
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("太空射击练习")
clock = pygame.time.Clock()

# 颜色
WHITE = (255,255,255)
BLUE  = (0,150,255)
RED   = (255,50,50)
GREEN = (0,255,0)
BLACK = (0,0,0)

# 飞船
player_image = pygame.image.load("ship.bmp")
player_size = player_image.get_rect().size
player_x = 400//2 - player_size[0]//2
player_y = 600 - player_size[1] - 20
player_speed = 8

# 子弹
bullets = []
bullet_speed = 10
bullet_width = 5
bullet_height = 15

# 目标
targets = []
target_size = 40
target_speed = 3
target_spawn_rate = 0.03

# 分数
score = 0
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]

font = None
for font_path in font_paths:
    try:
        font = pygame.font.Font(font_path, 30)
        break
    except:
        continue
if not font:
    font = pygame.font.Font(None, 30)

def spawn_target():
    x = random.randint(0, 400 - target_size)
    y = -target_size
    targets.append([x, y])

def update_bullets(bullets):
    for bullet in bullets:
        bullet[1] -= bullet_speed
    return [bullet for bullet in bullets if bullet[1] > 0]

def update_targets(targets):
    for target in targets:
        target[1] += target_speed
    return [target for target in targets if target[1] < 600]

def check_collisions(bullets, targets):
    global score
    new_bullets = []
    new_targets = []
    
    for bullet in bullets:
        hit = False
        for target in targets:
            if (bullet[0] > target[0] and 
                bullet[0] < target[0] + target_size and 
                bullet[1] > target[1] and 
                bullet[1] < target[1] + target_size):
                hit = True
                score += 1
                break
        if not hit:
            new_bullets.append(bullet)
    
    for target in targets:
        safe = True
        for bullet in bullets:
            if (bullet[0] > target[0] and 
                bullet[0] < target[0] + target_size and 
                bullet[1] > target[1] and 
                bullet[1] < target[1] + target_size):
                safe = False
                break
        if safe:
            new_targets.append(target)
    
    return new_bullets, new_targets

# 主循环
running = True
while running:
    screen.fill((0, 0, 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 发射子弹
                bullet_x = player_x + player_size[0] // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])
    
    # 控制飞船
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 400 - player_size[0]:
        player_x += player_speed
    
    # 生成目标
    if random.random() < target_spawn_rate:
        spawn_target()
    
    # 更新子弹和目标
    bullets = update_bullets(bullets)
    targets = update_targets(targets)
    
    # 检查碰撞
    bullets, targets = check_collisions(bullets, targets)
    
    # 绘制飞船
    screen.blit(player_image, (player_x, player_y))
    
    # 绘制子弹
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, (bullet[0], bullet[1], bullet_width, bullet_height))
    
    # 绘制目标
    for target in targets:
        pygame.draw.rect(screen, RED, (target[0], target[1], target_size, target_size))
    
    # 绘制分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 绘制操作说明
    help_text = font.render("空格: 发射", True, WHITE)
    screen.blit(help_text, (10, 40))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()