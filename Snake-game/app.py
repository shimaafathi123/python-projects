import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
GRID_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 255, 0)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, GRID_COLOR, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
        return True

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, GRID_COLOR, r, 1)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    WINNING_SCORE = 10
    game_over = False

    while not game_over:
        screen.fill(BG_COLOR)
        if not snake.handle_keys():
            break
        if not snake.move():
            game_over = True

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        snake.draw(screen)
        food.draw(screen)

        font = pygame.font.SysFont(None, 40)
        score_text = font.render("Score: " + str(snake.score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if snake.score >= WINNING_SCORE:
            font = pygame.font.SysFont(None, 60)
            win_text = font.render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))
            pygame.display.update()
            time.sleep(2)
            break

        pygame.display.update()

        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
