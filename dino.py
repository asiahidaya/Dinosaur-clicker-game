import pygame
import random
import time
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Clicker Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

# Load assets
dino = pygame.image.load("dino.png")
dino_rect = dino.get_rect()

click_sound = pygame.mixer.Sound("click_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

clock = pygame.time.Clock()

# High score
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

# ================= START SCREEN =================
def start_screen():
    while True:
        screen.fill(WHITE)

        title = big_font.render("Dino Clicker", True, BLACK)
        msg = font.render("Press 1-Easy  2-Medium  3-Hard", True, BLACK)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 3   # slow
                if event.key == pygame.K_2:
                    return 6   # medium
                if event.key == pygame.K_3:
                    return 10  # fast

# ================= GAME =================
def game(speed):
    global high_score

    score = 0
    combo = 0
    last_click_time = 0

    start_time = time.time()
    duration = 30

    dino_rect.topleft = (random.randint(50, WIDTH-100), random.randint(50, HEIGHT-100))

    dx = random.choice([-speed, speed])
    dy = random.choice([-speed, speed])

    while True:
        screen.fill(WHITE)

        elapsed = int(time.time() - start_time)
        remaining = max(0, duration - elapsed)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if dino_rect.collidepoint(event.pos):
                    current_time = time.time()

                    # Combo logic
                    if current_time - last_click_time < 0.7:
                        combo += 1
                    else:
                        combo = 1

                    score += combo
                    last_click_time = current_time

                    click_sound.play()

                    # Move dino randomly
                    dino_rect.topleft = (
                        random.randint(50, WIDTH-100),
                        random.randint(50, HEIGHT-100)
                    )

        # MOVE DINO
        dino_rect.x += dx
        dino_rect.y += dy

        # Bounce
        if dino_rect.left <= 0 or dino_rect.right >= WIDTH:
            dx *= -1
        if dino_rect.top <= 0 or dino_rect.bottom >= HEIGHT:
            dy *= -1

        # TIME UP
        if remaining == 0:
            game_over_sound.play()
            return score

        # DRAW
        screen.blit(dino, dino_rect)

        score_text = font.render(f"Score: {score}", True, BLACK)
        combo_text = font.render(f"Combo: x{combo}", True, BLACK)
        time_text = font.render(f"Time: {remaining}", True, BLACK)
        high_text = font.render(f"High: {high_score}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 40))
        screen.blit(time_text, (WIDTH//2 - 50, 10))
        screen.blit(high_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

# ================= GAME OVER =================
def game_over(score):
    global high_score

    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

    while True:
        screen.fill(WHITE)

        title = big_font.render("Game Over", True, BLACK)
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_text = font.render(f"High Score: {high_score}", True, BLACK)
        msg = font.render("Press R to Restart or Q to Quit", True, BLACK)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(high_text, (WIDTH//2 - high_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ================= MAIN =================
while True:
    speed = start_screen()
    final_score = game(speed)
    restart = game_over(final_score)
    if not restart:
        break
