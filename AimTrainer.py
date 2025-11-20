import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
TOP_BAR_HEIGHT = 50
GAME_DURATION = 20  #in seconds

LABEL_FONT = pygame.font.SysFont("comicsans", 24)
BUTTON_FONT = pygame.font.SysFont("comicsans", 50)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size


def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(win, elapsed_time, targets_pressed):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_left = max(0, GAME_DURATION - elapsed_time)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(time_left)}", 1, "black")

    speed = round(targets_pressed / (elapsed_time + 1e-5), 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))


def end_screen(win, targets_pressed, clicks, misses, high_score):
    win.fill(BG_COLOR)
    end_label = BUTTON_FONT.render("Game Over", 1, "white")
    win.blit(end_label, (get_middle(end_label), 50))

    speed = round(targets_pressed / GAME_DURATION, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / (clicks + 1e-5) * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    misses_label = LABEL_FONT.render(f"Hits Missed: {misses}", 1, "white")

    high_score_label = LABEL_FONT.render(f"High Score: {high_score}", 1, "white")

    win.blit(speed_label, (get_middle(speed_label), 150))
    win.blit(hits_label, (get_middle(hits_label), 200))
    win.blit(accuracy_label, (get_middle(accuracy_label), 250))
    win.blit(misses_label, (get_middle(misses_label), 300))
    win.blit(high_score_label, (get_middle(high_score_label), 350))

    restart_button = BUTTON_FONT.render("Restart", 1, "white")
    restart_button_rect = restart_button.get_rect(
        center=(WIDTH / 2, HEIGHT - 150))
    win.blit(restart_button, restart_button_rect)
    pygame.display.update()

    return restart_button_rect


def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def draw_start_screen(win, high_score):
    win.fill(BG_COLOR)
    start_button = BUTTON_FONT.render("Start", 1, "white")
    high_score_label = LABEL_FONT.render(f"High Score: {high_score}", 1, "white")
    win.blit(start_button, (get_middle(start_button), HEIGHT / 2 - start_button.get_height() / 2))
    win.blit(high_score_label, (get_middle(high_score_label), HEIGHT / 2 + start_button.get_height()))
    pygame.display.update()
    return start_button.get_rect(center=(WIDTH / 2, HEIGHT / 2))


def main():
    high_score = 0

    while True:
        start_game = False
        clock = pygame.time.Clock()

        while not start_game:
            start_button_rect = draw_start_screen(WIN, high_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        start_game = True

        targets = []
        targets_pressed = 0
        clicks = 0
        misses = 0
        start_time = time.time()

        pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

        game_running = True
        while game_running:
            clock.tick(60)
            click = False
            mouse_pos = pygame.mouse.get_pos()
            elapsed_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == TARGET_EVENT:
                    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                    y = random.randint(
                        TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                    target = Target(x, y)
                    targets.append(target)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                    clicks += 1

            if elapsed_time >= GAME_DURATION:
                if targets_pressed > high_score:
                    high_score = targets_pressed
                restart_button_rect = end_screen(
                    WIN, targets_pressed, clicks, misses, high_score)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if restart_button_rect.collidepoint(event.pos):
                                start_game = True
                                game_running = False
                                break
                    if not game_running:
                        break

            for target in targets:
                target.update()

                if target.size <= 0:
                    targets.remove(target)
                    misses += 1

                if click and target.collide(*mouse_pos):
                    targets.remove(target)
                    targets_pressed += 1

            draw(WIN, targets)
            draw_top_bar(WIN, elapsed_time, targets_pressed)
            pygame.display.update()


if __name__ == "__main__":
    main()