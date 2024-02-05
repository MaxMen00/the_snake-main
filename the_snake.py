import sys
import pygame
from random import randrange

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SPEED = 10

SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)
BOARD_BACKGROUND_COLOR = (0, 255, 204)
COLOR_NUMBER_1 = (255, 255, 255)
COLOR_NUMBER_2 = (204, 255, 255)

GAME_ICON = 'snaking.png'
GAME_TITLE = 'Snake'

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(GAME_ICON)
pygame.display.set_icon(icon)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects"""

    def __init__(self, position=(0, 0), color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.color = color
        self.body_color = color

    def draw(self, surface):
        """Draw the object on the surface"""
        pygame.draw.rect(surface, self.color, (
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Class for the snake object"""

    def __init__(self, position=(0, 0), color=BOARD_BACKGROUND_COLOR):
        super().__init__(position=position, color=color)
        self.positions = [position]
        self.direction = DOWN
        self.next_direction = None
        self.length = 3
        self.last = None
        self.body_color = SNAKE_COLOR
        self.rip = False

    def draw(self, surface):
        """Draw the snake on the surface"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Draw snake head
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Erase last segment
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get the position of the snake's head"""
        return self.positions[0]

    def calculate_new_head_position(self):
        """Calculate the new position of the snake's head"""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)
        return new_head

    def check_collision(self):
        """Check if the snake has collided with itself"""
        new_head = self.calculate_new_head_position()
        if new_head in self.positions[1:]:
            self.reset()

    def update_positions(self):
        """Update the positions of the snake's body segments"""
        new_head = self.calculate_new_head_position()
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Reset the snake's attributes"""
        self.rip = True

    def update_direction(self):
        """Update the direction of the snake"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the snake"""
        self.update_direction()
        self.update_positions()
        self.check_collision()


class Apple(GameObject):
    """A class for representing an apple"""

    def __init__(self, position=(0, 0), color=BOARD_BACKGROUND_COLOR):
        super().__init__(position, color)
        self.body_color = (255, 0, 0)

    def draw(self, surface):
        """Draw the apple on the surface"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Randomize the position of the apple"""
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))


def handle_keys(game_object):
    """Handle keyboard input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main game function"""
    # Create objects
    snake = Snake(position=(randrange(0, GRID_WIDTH, GRID_SIZE),
                  randrange(0, GRID_HEIGHT, GRID_SIZE)), color=SNAKE_COLOR)
    apple = Apple((randrange(0, GRID_WIDTH, GRID_SIZE),
                  randrange(0, GRID_HEIGHT, GRID_SIZE)), APPLE_COLOR)

    screen.fill(BOARD_BACKGROUND_COLOR)
    # Game loop
    game_over = False
    while not game_over:
        # Handle keys
        handle_keys(snake)

        # Move snake
        snake.move()

        # Check if snake ate apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Draw objects
        snake.draw(screen)
        apple.draw(screen)

        # Check if game over
        if snake.rip or game_over:
            game_over = True
            font = pygame.font.SysFont(None, 36)
            text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(1000)
            pygame.quit()
            sys.exit()
        # Update screen
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
