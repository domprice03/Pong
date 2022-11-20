import pygame
import numpy as np
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 720
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 160
BALL_WIDTH, BALL_HEIGHT = 10, 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
PLAYER_VEL = 10
BALL_VEL = 5

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Player:
    def __init__(self, x, y):
        self.player = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.score = 0

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.player)

    def collide_ball(self, ball):
        if self.player.colliderect(ball):
            return True


class LeftPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)

    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_w] and self.player.y - PLAYER_VEL >= 0:  # Up
            self.player.y -= PLAYER_VEL
        if keys_pressed[pygame.K_s] and self.player.y + PLAYER_HEIGHT + PLAYER_VEL <= HEIGHT:  # Down
            self.player.y += PLAYER_VEL


class RightPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y)

    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.player.y - PLAYER_VEL >= 0:  # Up
            self.player.y -= PLAYER_VEL
        if keys_pressed[pygame.K_DOWN] and self.player.y + PLAYER_HEIGHT + PLAYER_VEL <= HEIGHT:  # Down
            self.player.y += PLAYER_VEL


class Ball:
    def __init__(self, side, vel):
        if side == 'left':
            self.ball = pygame.Rect(PLAYER_WIDTH + BALL_WIDTH, HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
            self.ball_angle = random.choice(
                [random.uniform(np.pi / 12, 5*np.pi / 12), random.uniform(19 * np.pi / 12, 23 * np.pi / 12)])
        if side == 'right':
            self.ball = pygame.Rect(WIDTH - PLAYER_WIDTH - BALL_WIDTH, HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)
            self.ball_angle = random.choice(
                [random.uniform(7*np.pi / 12, 11*np.pi / 12), random.uniform(13 * np.pi / 12, 17 * np.pi / 12)])

        self.vel = vel

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.ball)

    def move(self):
        self.ball.x += np.cos(self.ball_angle) * self.vel
        self.ball.y -= np.sin(self.ball_angle) * self.vel  # - sign due to pygame coordinate system

    def collisions(self, right_player, left_player):
        if self.ball.y + BALL_HEIGHT >= HEIGHT or self.ball.y <= 0:
            self.vel *= 1.02
            self.ball_angle = 2 * np.pi - self.ball_angle

        if right_player.collide_ball(self.ball) or left_player.collide_ball(self.ball):
            self.vel *= 1.02
            if 0 < self.ball_angle < np.pi:
                self.ball_angle = np.pi - self.ball_angle
                # Running self.move() again makes sure it only registers the collision once
                self.move()
            if np.pi < self.ball_angle < 2 * np.pi:
                self.ball_angle = 3 * np.pi - self.ball_angle
                self.move()

    def x(self):
        return self.ball.x


def main():
    run = True
    main_font = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()

    left_player = LeftPlayer(PLAYER_WIDTH // 2, HEIGHT // 2 - PLAYER_HEIGHT // 2)
    right_player = RightPlayer(WIDTH - PLAYER_WIDTH - 10, HEIGHT // 2 - PLAYER_HEIGHT // 2)
    ball = Ball(random.choice(['left', 'right']), BALL_VEL)

    def draw_window():
        pygame.draw.rect(WIN, BLACK, BACKGROUND)

        left_score = main_font.render(f"Score: {left_player.score}", 1, WHITE)
        right_score = main_font.render(f"Score: {right_player.score}", 1, WHITE)
        WIN.blit(left_score, (10, 10))
        WIN.blit(right_score, (WIDTH - right_score.get_width() - 10, 10))

        left_player.draw()
        right_player.draw()
        ball.draw()

    while run:
        clock.tick(FPS)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys_pressed = pygame.key.get_pressed()
        left_player.movement(keys_pressed)
        right_player.movement(keys_pressed)

        ball.move()
        ball.collisions(right_player, left_player)
        if ball.x() >= WIDTH:
            left_player.score += 1
            ball = Ball('right', BALL_VEL)
        if ball.x() <= 0:
            right_player.score += 1
            ball = Ball('left', BALL_VEL)

        pygame.display.update()


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        pygame.draw.rect(WIN, BLACK, BACKGROUND)
        title_label = title_font.render("Left click to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
