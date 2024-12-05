import os
import pygame
import random

# 初始化 Pygame
pygame.init()

# ... 在 pygame.init() 之后添加字体初始化 ...
try:
    font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)  # 使用微软雅黑字体
except:
    font = pygame.font.Font(None, 36)  # 如果找不到中文字体，使用默认字体



# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCORE_PER_LINE = 100  # 每消除一行的分数
LEVEL_SPEED_FACTOR = 1.2  # 每提升一级，速度增加20%
BASE_SPEED = 5  # 基础速度（每秒帧数）
LINES_PER_LEVEL = 5  # 每消除5行提升一级
BASE_SPEED = 60  # 基础帧率
FALL_SPEED = 1   # 基础下落速度（每30帧下落一次）
LEVEL_SPEED_FACTOR = 1.2  # 每提升一级，速度增加20%


# 计算游戏区域的位置，使其居中
GAME_AREA_X = (WINDOW_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GAME_AREA_Y = (WINDOW_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# 创建游戏网格
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 在主循环前定义当前方块
current_shape = random.choice(SHAPES)
current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
current_y = 0

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

def check_collision(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = current_x + x + offset_x
                new_y = current_y + y + offset_y
                
                if (new_x < 0 or new_x >= GRID_WIDTH or
                    new_y >= GRID_HEIGHT or
                    (new_y >= 0 and grid[new_y][new_x])):
                    return True
    return False

def rotate_shape(shape):
    return list(zip(*shape[::-1]))

def reset_game():
    global grid, current_shape, next_shape, current_x, current_y, score, level, lines_cleared
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_shape = random.choice(SHAPES)
    next_shape = random.choice(SHAPES)  # 添加下一个方块
    current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
    current_y = 0
    score = 0
    level = 1
    lines_cleared = 0

# ... 添加新的函数 ...
def clear_lines():
    global grid, score, level, lines_cleared
    lines_cleared_now = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if all(grid[y]):
            lines_cleared_now += 1
            for y2 in range(y, 0, -1):
                grid[y2] = grid[y2-1][:]
            grid[0] = [0] * GRID_WIDTH
        else:
            y -= 1
    
    if lines_cleared_now > 0:
        score += SCORE_PER_LINE * lines_cleared_now
        lines_cleared += lines_cleared_now
        # 更新等级
        level = (lines_cleared // LINES_PER_LEVEL) + 1

# ... 添加获取方块投影位置的函数 ...
def get_ghost_position():
    ghost_y = current_y
    while not check_collision(current_shape, 0, ghost_y - current_y + 1):
        ghost_y += 1
    return ghost_y

# 初始化游戏状态
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_shape = random.choice(SHAPES)
next_shape = random.choice(SHAPES)  # 添加下一个方块
current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
current_y = 0
game_over = False
score = 0
level = 1
lines_cleared = 0
paused = False

# 修改主循环
running = True
clock = pygame.time.Clock()  # 添加时钟对象来控制游戏速度

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # 按P键暂停/继续
                paused = not paused
            if not game_over and not paused:  # 只在游戏进行且未暂停时响应其他按键
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_shape, -1, 0):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_shape, 1, 0):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_shape, 0, 1):
                        current_y += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(rotated_shape, 0, 0):
                        current_shape = rotated_shape



    if not game_over and not paused:
        # 自动下落
        if not check_collision(current_shape, 0, 1):
            current_y += 1
        else:
            # 将方块固定到网格中
            for y, row in enumerate(current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_y + y][current_x + x] = 1
                
                # 检查并清除完整的行
                clear_lines()
            
            # 当前方块变为下一个方块
            current_shape = next_shape
            next_shape = random.choice(SHAPES)
            current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
            current_y = 0
            
            # 检查游戏是否结束
            if check_collision(current_shape, 0, 0):
                game_over = True
        
        

    # 绘制部分
    screen.fill(BLACK)

    # 绘制下一个方块预览
    preview_x = WINDOW_WIDTH - 150
    preview_y = 100
    preview_text = font.render('下一个:', True, WHITE)
    screen.blit(preview_text, (preview_x - 20, preview_y - 40))

    
    # 绘制游戏区域边框
    pygame.draw.rect(screen, WHITE, 
                    (GAME_AREA_X - 1, GAME_AREA_Y - 1, 
                     GRID_WIDTH * BLOCK_SIZE + 2, 
                     GRID_HEIGHT * BLOCK_SIZE + 2), 1)
    
    # 绘制网格线
    for i in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, (50, 50, 50),
                        (GAME_AREA_X + i * BLOCK_SIZE, GAME_AREA_Y),
                        (GAME_AREA_X + i * BLOCK_SIZE, GAME_AREA_Y + GRID_HEIGHT * BLOCK_SIZE))
    for i in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, (50, 50, 50),
                        (GAME_AREA_X, GAME_AREA_Y + i * BLOCK_SIZE),
                        (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE, GAME_AREA_Y + i * BLOCK_SIZE))
    
    # 绘制已固定的方块
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, BLUE,
                               (GAME_AREA_X + x * BLOCK_SIZE,
                                GAME_AREA_Y + y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))
    
    # 绘制当前方块
    if not game_over:
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, RED,
                                   (GAME_AREA_X + (current_x + x) * BLOCK_SIZE,
                                    GAME_AREA_Y + (current_y + y) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    if paused:
        # 创建半透明的暂停遮罩
        pause_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        pause_surface.set_alpha(128)
        pause_surface.fill(BLACK)
        screen.blit(pause_surface, (0, 0))
        
        # 显示暂停文字
        pause_text = font.render('已暂停 - 按P继续', True, WHITE)
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        screen.blit(pause_text, text_rect)
                    
     # 绘制下一个方块预览
    preview_x = WINDOW_WIDTH - 150
    preview_y = 100
    preview_text = font.render('下一个:', True, WHITE)
    screen.blit(preview_text, (preview_x - 20, preview_y - 40))
    
    for y, row in enumerate(next_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, GREEN,
                               (preview_x + x * BLOCK_SIZE,
                                preview_y + y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))
                
     # 显示分数和等级
    score_text = font.render(f'分数: {score}', True, WHITE)
    level_text = font.render(f'等级: {level}', True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 60))

    # 如果游戏结束，显示游戏结束文字
    if game_over:
        try:
            # Windows系统默认中文字体
            font = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", 36)
        except:
            # 如果找不到中文字体，就使用默认字体
            font = pygame.font.Font(None, 36)

       
        score_text = font.render(f'分数: {score}', True, WHITE)
        screen.blit(score_text, (20, 20))
        game_over_text = font.render('游戏结束! 按R重新开始', True, WHITE)
        restart_text = font.render('按R重新开始', True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30))
        screen.blit(game_over_text, text_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(BASE_SPEED)   # 控制基础帧率

    current_speed = BASE_SPEED * (LEVEL_SPEED_FACTOR ** (level - 1))
    clock.tick(5)

pygame.quit()
