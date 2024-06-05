import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fast Paced Action Game")

# Font settings
font = pygame.font.Font(None, 36)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_COLOR = WHITE
player_speed = 7

# Obstacle settings
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 30
obstacle_speed = 5
obstacle_frequency = 25  # Higher value means less frequent

# Power-up settings
POWERUP_SIZE = 20
powerup_speed = 3
powerup_frequency = 100  # Higher value means less frequent

# Projectile settings
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 5
PROJECTILE_COLOR = YELLOW
projectile_speed = 10
projectile_cooldown = 0.25  # Cooldown time in seconds


# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.last_shot_time = 0

    def move(self, dy):c
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def can_shoot(self):
        current_time = time.time()
        return current_time - self.last_shot_time >= projectile_cooldown

    def shoot(self):
        self.last_shot_time = time.time()

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)


# Obstacle class
class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.color = random.choice(COLORS)

    def move(self):
        self.rect.x -= obstacle_speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# Power-up class
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWERUP_SIZE, POWERUP_SIZE)
        self.color = random.choice(COLORS)

    def move(self):
        self.rect.x -= powerup_speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# Projectile class
class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)

    def move(self):
        self.rect.x += projectile_speed

    def draw(self, screen):
        pygame.draw.rect(screen, PROJECTILE_COLOR, self.rect)


# Main game loop
def game_loop():
    player = Player()
    obstacles = []
    powerups = []
    projectiles = []
    score = 0
    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(-player_speed)
        if keys[pygame.K_DOWN]:
            player.move(player_speed)
        if keys[pygame.K_SPACE] and player.can_shoot():
            player.shoot()
            projectile = Projectile(player.rect.right, player.rect.centery - PROJECTILE_HEIGHT // 2)
            projectiles.append(projectile)

        # Spawn obstacles
        if frame_count % obstacle_frequency == 0:
            obstacle_y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_HEIGHT)
            obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_y))

        # Spawn power-ups
        if frame_count % powerup_frequency == 0:
            powerup_y = random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE)
            powerups.append(PowerUp(SCREEN_WIDTH, powerup_y))

        # Move and draw projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.rect.left > SCREEN_WIDTH:
                projectiles.remove(projectile)
            projectile.draw(screen)

        # Move and draw obstacles
        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
            obstacle.draw(screen)

        # Move and draw power-ups
        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.right < 0:
                powerups.remove(powerup)
            powerup.draw(screen)

        # Check collisions
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                running = False  # End game on collision

        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                score += 1
                powerups.remove(powerup)

        for projectile in projectiles[:]:
            for obstacle in obstacles[:]:
                if projectile.rect.colliderect(obstacle.rect):
                    obstacles.remove(obstacle)
                    projectiles.remove(projectile)
                    break

        # Draw player
        player.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1


game_loop()
pygame.quit()
sys.exit()
