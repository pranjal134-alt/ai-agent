import pygame
import random

pygame.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Shooter")

# Colors
white = (255, 255, 255)
green = (0, 150, 0)
black = (0, 0, 0)
red = (200, 0, 0)

# Player
player_x = width // 2
player_y = height - 50
player_speed = 6

# Bullet
bullet_x = 0
bullet_y = player_y
bullet_speed = 8
bullet_state = "ready"

# Zombies (multiple)
zombies = []
for i in range(5):
    zombies.append([random.randint(0, width - 40), random.randint(20, 100)])

zombie_speed = 2

# Score
score = 0
font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, green, (x, y, 40, 40))

def draw_zombies():
    for z in zombies:
        pygame.draw.rect(screen, red, (z[0], z[1], 40, 40))

def fire_bullet(x, y):
    pygame.draw.rect(screen, black, (x + 18, y, 5, 10))

def is_collision(zx, zy, bx, by):
    return abs(zx - bx) < 30 and abs(zy - by) < 30

def game_over():
    text = font.render("GAME OVER", True, red)
    screen.blit(text, (220, 180))
    pygame.display.update()
    pygame.time.delay(2000)

# Game loop
running = True
while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                bullet_y = player_y
                bullet_state = "fire"

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - 40:
        player_x += player_speed

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed

    if bullet_y < 0:
        bullet_state = "ready"

    # Zombie movement
    for z in zombies:
        z[1] += zombie_speed

        # Game over if zombie hits player
        if abs(z[0] - player_x) < 30 and abs(z[1] - player_y) < 30:
            game_over()
            running = False

        # Reset zombie if it goes down
        if z[1] > height:
            z[1] = random.randint(20, 100)
            z[0] = random.randint(0, width - 40)

        # Bullet hit zombie
        if bullet_state == "fire" and is_collision(z[0], z[1], bullet_x, bullet_y):
            score += 1
            bullet_state = "ready"
            z[0] = random.randint(0, width - 40)
            z[1] = random.randint(20, 100)

    # Draw
    draw_player(player_x, player_y)
    draw_zombies()

    # Score
    text = font.render("Score: " + str(score), True, black)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
