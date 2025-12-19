import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - 50) // GRID_SIZE

# Colors
BG_COLOR = (20, 30, 48)  # Dark blue background
SNAKE_COLOR = (46, 204, 113)  # Green snake
SNAKE_BORDER = (39, 174, 96)  # Darker green border
FOOD_COLOR = (231, 76, 60)  # Red food
GRID_COLOR = (30, 40, 60)  # Subtle grid
TEXT_COLOR = (255, 255, 255)  # White text
GAME_OVER_BG = (20, 30, 48)  # Dark background
HEADER_BG = (15, 25, 40)  # Header background
GOLD_COLOR = (255, 215, 0)  # Gold for high score
GLOW_COLOR = (100, 200, 255)  # Glow effect

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.pulse = 0
    
    def generate_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos
    
    def update_pulse(self):
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 30
        self.color = random.choice([(46, 204, 113), (52, 211, 123), (255, 215, 0)])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
    
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 30))
            size = max(1, int(4 * (self.life / 30)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

def draw_gradient_background(screen):
    for y in range(WINDOW_HEIGHT):
        color_val = 20 + int(15 * (y / WINDOW_HEIGHT))
        pygame.draw.line(screen, (color_val, color_val + 10, color_val + 28), (0, y), (WINDOW_WIDTH, y))

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 50), (x, WINDOW_HEIGHT), 1)
    for y in range(50, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y), 1)

def draw_snake(screen, snake):
    for i, segment in enumerate(snake.body):
        x = segment[0] * GRID_SIZE
        y = segment[1] * GRID_SIZE + 50
        
        if i == 0:  # Head
            # Glow effect
            glow_surf = pygame.Surface((GRID_SIZE + 10, GRID_SIZE + 10), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*GLOW_COLOR, 30), (GRID_SIZE // 2 + 5, GRID_SIZE // 2 + 5), GRID_SIZE)
            screen.blit(glow_surf, (x - 5, y - 5))
            
            # Draw head
            pygame.draw.rect(screen, (34, 153, 84), (x, y, GRID_SIZE, GRID_SIZE), border_radius=8)
            pygame.draw.rect(screen, SNAKE_BORDER, (x, y, GRID_SIZE, GRID_SIZE), 2, border_radius=8)
            
            # Eyes with animation
            eye_color = (255, 255, 255)
            pupil_color = (0, 0, 0)
            
            if snake.direction == RIGHT:
                pygame.draw.circle(screen, eye_color, (x + GRID_SIZE - 6, y + 6), 4)
                pygame.draw.circle(screen, eye_color, (x + GRID_SIZE - 6, y + GRID_SIZE - 6), 4)
                pygame.draw.circle(screen, pupil_color, (x + GRID_SIZE - 4, y + 6), 2)
                pygame.draw.circle(screen, pupil_color, (x + GRID_SIZE - 4, y + GRID_SIZE - 6), 2)
            elif snake.direction == LEFT:
                pygame.draw.circle(screen, eye_color, (x + 6, y + 6), 4)
                pygame.draw.circle(screen, eye_color, (x + 6, y + GRID_SIZE - 6), 4)
                pygame.draw.circle(screen, pupil_color, (x + 4, y + 6), 2)
                pygame.draw.circle(screen, pupil_color, (x + 4, y + GRID_SIZE - 6), 2)
            elif snake.direction == UP:
                pygame.draw.circle(screen, eye_color, (x + 6, y + 6), 4)
                pygame.draw.circle(screen, eye_color, (x + GRID_SIZE - 6, y + 6), 4)
                pygame.draw.circle(screen, pupil_color, (x + 6, y + 4), 2)
                pygame.draw.circle(screen, pupil_color, (x + GRID_SIZE - 6, y + 4), 2)
            elif snake.direction == DOWN:
                pygame.draw.circle(screen, eye_color, (x + 6, y + GRID_SIZE - 6), 4)
                pygame.draw.circle(screen, eye_color, (x + GRID_SIZE - 6, y + GRID_SIZE - 6), 4)
                pygame.draw.circle(screen, pupil_color, (x + 6, y + GRID_SIZE - 4), 2)
                pygame.draw.circle(screen, pupil_color, (x + GRID_SIZE - 6, y + GRID_SIZE - 4), 2)
            
            # Tongue
            tongue_color = (231, 76, 60)
            if snake.direction == RIGHT:
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE, y + GRID_SIZE // 2), (x + GRID_SIZE + 5, y + GRID_SIZE // 2 - 3), 2)
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE, y + GRID_SIZE // 2), (x + GRID_SIZE + 5, y + GRID_SIZE // 2 + 3), 2)
            elif snake.direction == LEFT:
                pygame.draw.line(screen, tongue_color, (x, y + GRID_SIZE // 2), (x - 5, y + GRID_SIZE // 2 - 3), 2)
                pygame.draw.line(screen, tongue_color, (x, y + GRID_SIZE // 2), (x - 5, y + GRID_SIZE // 2 + 3), 2)
            elif snake.direction == UP:
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE // 2, y), (x + GRID_SIZE // 2 - 3, y - 5), 2)
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE // 2, y), (x + GRID_SIZE // 2 + 3, y - 5), 2)
            elif snake.direction == DOWN:
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE // 2, y + GRID_SIZE), (x + GRID_SIZE // 2 - 3, y + GRID_SIZE + 5), 2)
                pygame.draw.line(screen, tongue_color, (x + GRID_SIZE // 2, y + GRID_SIZE), (x + GRID_SIZE // 2 + 3, y + GRID_SIZE + 5), 2)
        else:
            # Body with gradient
            if i % 2 == 0:
                body_color = SNAKE_COLOR
            else:
                body_color = (52, 211, 123)
            
            pygame.draw.rect(screen, body_color, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2), border_radius=5)
            pygame.draw.rect(screen, SNAKE_BORDER, (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2), 2, border_radius=5)
            
            # Scale pattern
            pygame.draw.circle(screen, (39, 174, 96), (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 3)

def draw_food(screen, food):
    x = food.position[0] * GRID_SIZE
    y = food.position[1] * GRID_SIZE + 50
    
    # Pulsing glow
    pulse_size = int(5 + 3 * math.sin(food.pulse))
    glow_surf = pygame.Surface((GRID_SIZE + pulse_size * 2, GRID_SIZE + pulse_size * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*FOOD_COLOR, 50), (GRID_SIZE // 2 + pulse_size, GRID_SIZE // 2 + pulse_size), GRID_SIZE + pulse_size)
    screen.blit(glow_surf, (x - pulse_size, y - pulse_size))
    
    # Food
    pygame.draw.rect(screen, FOOD_COLOR, (x, y, GRID_SIZE, GRID_SIZE), border_radius=10)
    pygame.draw.circle(screen, (192, 57, 43), (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 3)
    pygame.draw.circle(screen, (255, 100, 80), (x + GRID_SIZE // 2 - 3, y + GRID_SIZE // 2 - 3), 3)

def draw_header(screen, score, high_score, font):
    # Header background
    pygame.draw.rect(screen, HEADER_BG, (0, 0, WINDOW_WIDTH, 50))
    pygame.draw.line(screen, (100, 200, 255), (0, 49), (WINDOW_WIDTH, 49), 2)
    
    # Title
    title_font = pygame.font.Font(None, 36)
    title = title_font.render('🐍 SNAKE GAME', True, (100, 200, 255))
    screen.blit(title, (20, 10))
    
    # Score
    score_text = font.render(f'Score: {score}', True, TEXT_COLOR)
    screen.blit(score_text, (WINDOW_WIDTH - 200, 15))
    
    # High Score
    high_score_text = font.render(f'Best: {high_score}', True, GOLD_COLOR)
    screen.blit(high_score_text, (WINDOW_WIDTH - 200, 32))

def game_over_screen(screen, score, high_score, font, big_font, particles):
    draw_gradient_background(screen)
    
    # Draw particles
    for particle in particles:
        particle.draw(screen)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Game Over text with glow
    game_over_text = big_font.render('GAME OVER', True, (231, 76, 60))
    glow_text = big_font.render('GAME OVER', True, (255, 150, 150))
    screen.blit(glow_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2 + 2, WINDOW_HEIGHT // 2 - 82))
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 80))
    
    # Score box
    box_width = 300
    box_height = 120
    box_x = WINDOW_WIDTH // 2 - box_width // 2
    box_y = WINDOW_HEIGHT // 2 - 20
    
    pygame.draw.rect(screen, (30, 40, 60), (box_x, box_y, box_width, box_height), border_radius=15)
    pygame.draw.rect(screen, (100, 200, 255), (box_x, box_y, box_width, box_height), 3, border_radius=15)
    
    # Scores
    score_text = font.render(f'Your Score: {score}', True, TEXT_COLOR)
    high_score_text = font.render(f'Best Score: {high_score}', True, GOLD_COLOR)
    screen.blit(score_text, (box_x + box_width // 2 - score_text.get_width() // 2, box_y + 20))
    screen.blit(high_score_text, (box_x + box_width // 2 - high_score_text.get_width() // 2, box_y + 50))
    
    # Instructions
    restart_text = font.render('Press SPACE to restart', True, (100, 200, 255))
    quit_text = font.render('Press ESC to quit', True, (150, 150, 150))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 120))
    screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, WINDOW_HEIGHT // 2 + 145))
    
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('🐍 Snake Game - Enhanced Edition')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    big_font = pygame.font.Font(None, 64)
    
    high_score = 0
    
    while True:
        snake = Snake()
        food = Food(snake.body)
        score = 0
        game_active = True
        particles = []
        
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
            
            snake.move()
            food.update_pulse()
            
            # Check food collision
            if snake.body[0] == food.position:
                snake.grow = True
                score += 10
                if score > high_score:
                    high_score = score
                
                # Create particles
                food_x = food.position[0] * GRID_SIZE + GRID_SIZE // 2
                food_y = food.position[1] * GRID_SIZE + GRID_SIZE // 2 + 50
                for _ in range(20):
                    particles.append(Particle(food_x, food_y))
                
                food = Food(snake.body)
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for particle in particles:
                particle.update()
            
            # Check game over
            if snake.check_collision():
                game_active = False
            
            # Draw everything
            draw_gradient_background(screen)
            draw_grid(screen)
            
            # Draw particles
            for particle in particles:
                particle.draw(screen)
            
            draw_snake(screen, snake)
            draw_food(screen, food)
            draw_header(screen, score, high_score, font)
            
            pygame.display.flip()
            clock.tick(5)
        
        # Game over with particles
        game_over_particles = []
        for i in range(50):
            game_over_particles.append(Particle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        game_over_screen(screen, score, high_score, font, big_font, game_over_particles)
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

if __name__ == '__main__':
    main()