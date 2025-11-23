# FOCUS GAME 2, 10 LEVELS, *STROBE SLOW TO FAST
import pygame
import random
import sys
import time
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Focus Game")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
NEON_RED = (255, 20, 20)
NEON_RED_HOVER = (255, 60, 60)
RAINBOW = [(255, 0, 0), (255, 127, 0), (255, 255, 0),
           (0, 255, 0), (0, 0, 255), (75, 0, 130), (139, 0, 255)]

# Font
FONT = pygame.font.SysFont("Arial", 40)

# Game settings
levels = 10
level = 1
running = True
game_state = "main"  # main, play, level_complete, game_over

# Ball settings
ball_radius_start = 40  # level 1 large
ball_radius_end = 10    # level 10 small
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_color_index = 0

# Level durations: +10s per level
level_durations = [10 + i * 10 for i in range(levels)]  # Level 1=10s, Level 10=100s

# Level speed: steadily increase so movement is faster every level
level_speeds = [3 + i * 3 for i in range(levels)]  # Level 1=3, Level 10=30

# Ball size progression
ball_radii = [int(ball_radius_start - (ball_radius_start - ball_radius_end) * (i / (levels - 1)))
              for i in range(levels)]

# Strobe intervals: reversed so level 1 is slower, level 10 is fastest
strobe_intervals = [2 - (i / (levels - 1)) for i in range(levels)]  # Level 1=2, Level10=1

# Button
button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2, 160, 60)

def draw_button(rect, text, hover=False):
    color = NEON_RED_HOVER if hover else NEON_RED
    pygame.draw.rect(screen, color, rect)
    txt_surf = FONT.render(text, True, BLACK)
    screen.blit(txt_surf, (rect.centerx - txt_surf.get_width() // 2,
                           rect.centery - txt_surf.get_height() // 2))

def draw_main_screen():
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    draw_button(button_rect, "Start", hover)
    level_text = FONT.render(f"Level {level}", True, NEON_RED)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 100))
    pygame.display.flip()

def draw_level_complete():
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    draw_button(button_rect, "Start", hover)
    level_text = FONT.render(f"Level {level}", True, NEON_RED)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 100))
    pygame.display.flip()

def draw_game_over():
    screen.fill(BLACK)
    restart_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2, 160, 60)
    quit_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 100, 160, 60)
    mouse_pos = pygame.mouse.get_pos()
    draw_button(restart_rect, "Restart", restart_rect.collidepoint(mouse_pos))
    draw_button(quit_rect, "Quit", quit_rect.collidepoint(mouse_pos))
    pygame.display.flip()
    return restart_rect, quit_rect

def play_level():
    global ball_x, ball_y, ball_color_index, level, game_state

    start_time = time.time()
    duration = level_durations[level - 1]
    speed = level_speeds[level - 1]
    radius = ball_radii[level - 1]
    strobe_speed = strobe_intervals[level - 1]

    # Initialize ball in center
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2

    # Random initial direction
    angle = random.uniform(0, 2 * math.pi)
    ball_dx = math.cos(angle) * speed
    ball_dy = math.sin(angle) * speed

    frame_count = 0

    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        frame_count += 1

        # Ghost-like erratic movement
        if random.random() < 0.1:
            ball_dx += random.uniform(-speed*1.5, speed*1.5)
            ball_dy += random.uniform(-speed*1.5, speed*1.5)
        else:
            ball_dx += random.uniform(-0.5, 0.5)
            ball_dy += random.uniform(-0.5, 0.5)

        # Limit speed
        mag = math.sqrt(ball_dx ** 2 + ball_dy ** 2)
        if mag > speed:
            ball_dx = (ball_dx / mag) * speed
            ball_dy = (ball_dy / mag) * speed

        # Update position
        ball_x += ball_dx
        ball_y += ball_dy

        # Steer away from edges
        margin = radius + 5
        if ball_x < margin:
            ball_dx += random.uniform(0.5, 1.0)
        if ball_x > WIDTH - margin:
            ball_dx -= random.uniform(0.5, 1.0)
        if ball_y < margin:
            ball_dy += random.uniform(0.5, 1.0)
        if ball_y > HEIGHT - margin:
            ball_dy -= random.uniform(0.5, 1.0)

        # Clamp inside screen
        ball_x = max(radius, min(WIDTH - radius, ball_x))
        ball_y = max(radius, min(HEIGHT - radius, ball_y))

        # Rainbow strobe
        if frame_count % max(1, int(strobe_speed)) == 0:
            ball_color_index = (ball_color_index + 1) % len(RAINBOW)

        # Draw
        screen.fill(BLACK)
        pygame.draw.circle(screen, RAINBOW[ball_color_index], (int(ball_x), int(ball_y)), radius)
        pygame.display.flip()
        clock.tick(60)

    # Level complete
    level += 1
    if level > levels:
        game_state = "game_over"
    else:
        game_state = "level_complete"

# Main loop
while running:
    if game_state == "main":
        draw_main_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = "play"

    elif game_state == "level_complete":
        draw_level_complete()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_state = "play"

    elif game_state == "play":
        play_level()

    elif game_state == "game_over":
        restart_rect, quit_rect = draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    level = 1
                    game_state = "main"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

pygame.quit()
