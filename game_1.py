import pygame
import random
import sys

# 初始化
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("躲避陨石")
clock = pygame.time.Clock()

# 颜色
WHITE = (255,255,255)
BLUE  = (0,150,255)
RED   = (255,50,50)
BLACK = (0,0,0)

# 飞船
player_image = pygame.image.load("ship.bmp")
player_size = player_image.get_rect().size
player_x = 400//2 - player_size[0]//2
player_y = 600 - player_size[1] - 20
speed = 8

# 陨石
enemy_size = 30
enemy_list = []
enemy_speed = 5

# 分数
score = 0
font = pygame.font.Font(None, 40)

def drop_enemy(enemy_list):
    delay = random.random()
    if len(enemy_list) < 6 and delay < 0.08:
        x = random.randint(0, 400-enemy_size)
        y = 0
        enemy_list.append([x, y])

def draw_enemy(enemy_list):
    for x,y in enemy_list:
        pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))

def update_enemy_pos(enemy_list, score):
    for idx, enemy in enumerate(enemy_list):
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemy_list.pop(idx)
            return score + 1
    return score

def collision(player_x, player_y, player_width, player_height, enemy_list):
    for ex, ey in enemy_list:
        if (player_x < ex + enemy_size and
            player_x + player_width > ex and
            player_y < ey + enemy_size and
            player_y + player_height > ey):
            return True
    return False

# 主循环
running = True
game_over = False

while running:
    screen.fill((230, 230, 230))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= speed
        if keys[pygame.K_RIGHT] and player_x < 400 - player_size[0]:
            player_x += speed

        # 生成陨石
        drop_enemy(enemy_list)
        score = update_enemy_pos(enemy_list, score)

        # 碰撞
        if collision(player_x, player_y, player_size[0], player_size[1], enemy_list):
            game_over = True

        # 画飞船
        screen.blit(player_image, (player_x, player_y))
        draw_enemy(enemy_list)

        # 分数
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10,10))

    else:
        # 结束
        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, (130, 250))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (150, 300))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()