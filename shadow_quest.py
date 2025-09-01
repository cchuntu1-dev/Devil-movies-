import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Game Constants ---
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0) # For danger zones (spikes)

# Player properties
PLAYER_SIZE = 40
PLAYER_COLOR = BLACK
PLAYER_SPEED = 5
JUMP_STRENGTH = -15
GRAVITY = 0.8
DOUBLE_JUMP_STRENGTH = -12

# --- Setup the Game Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Quest")

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.platforms = None  # We'll set this later to the platform group
        self.jumps = 2 # Starts with 2 jumps (single and double)

    def update(self):
        # Apply gravity
        self.change_y += GRAVITY
        
        # Move left/right
        self.rect.x += self.change_x

        # Check for horizontal collisions with platforms
        self.check_collision_x()
        
        # Move up/down
        self.rect.y += self.change_y
        
        # Keep player from falling off the bottom of the screen
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y = 0
            self.on_ground = True
            self.jumps = 2
            
        # Check for vertical collisions with platforms
        self.check_collision_y()

    def check_collision_x(self):
        if self.platforms:
            block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
            for block in block_hit_list:
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

    def check_collision_y(self):
        if self.platforms:
            block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
            for block in block_hit_list:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
                    self.on_ground = True
                    self.jumps = 2  # Reset jumps when the player lands
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    self.change_y = 0
                    
    def move_left(self):
        self.change_x = -PLAYER_SPEED

    def move_right(self):
        self.change_x = PLAYER_SPEED

    def stop(self):
        self.change_x = 0
        
    def jump(self):
        if self.jumps > 0:
            if self.jumps == 2:
                self.change_y = JUMP_STRENGTH
            else:
                self.change_y = DOUBLE_JUMP_STRENGTH
            self.jumps -= 1
            self.on_ground = False

# --- Platform Class ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Level Creation Function ---
def create_level():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    
    # Define the level layout
    level_list = [
        # Regular platforms
        [300, 20, 200, 500, BLACK],
        [150, 20, 500, 400, BLACK],
        [100, 20, 650, 250, BLACK],
        [400, 20, 50, 200, BLACK],
        
        # A small, tricky platform
        [50, 20, 100, 300, BLACK],

        # A "spike" platform (just a red block for now)
        [80, 20, 350, 300, RED],

        # The end goal platform
        [100, 20, 10, 100, BLACK]
    ]

    for platform_data in level_list:
        width, height, x, y, color = platform_data
        platform = Platform(width, height, x, y, color)
        platforms.add(platform)
        all_sprites.add(platform)

    return all_sprites, platforms

# --- Main Game Loop ---
def main():
    player = Player()
    
    # Create the level and get the sprite groups
    all_sprites, platforms = create_level()
    all_sprites.add(player)
    player.platforms = platforms # Tell the player about the platforms

    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Keyboard Input ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_SPACE:
                    player.jump()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                elif event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # --- Game Logic ---
        all_sprites.update()
        
        # --- Drawing ---
        screen.fill(YELLOW)
        all_sprites.draw(screen)

        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
