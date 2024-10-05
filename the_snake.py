from random import choice, randint
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов.
    """

    def __init__(self) -> None:
        self.position: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: Optional[tuple] = None

    def draw(self, surface, position, color, bg_color):
        """Метод draw предназначен для отрисовки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, bg_color, rect, 1)


class Apple(GameObject):
    """Класс Apple описывает яблоко и действия с ним,
    является дочерним классом родительского класса GameObject.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод, который описывает случайное появление яблоко
        на игровом поле.
        """
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Класс Snake описывает змейку, ее поведение на игровом поле,
    позволяет управлять ее движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions: list = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Позволяет обновлять направление движения нашей змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface, color, bg_color):
        """Метод, благодаря которому отрисовывается змейка на игровом поле,
        также отрисовывает голову и затирает последний элемент змейки.
        """
        for position in self.positions[:-1]:
            super().draw(surface, position, color, bg_color)
        super().draw(surface, self.positions[0], color, bg_color)
        if self.last:
            super().draw(surface, self.last, BOARD_BACKGROUND_COLOR,
                         BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Этот метод возвращает голову змейки(первый элемент списка)."""
        return self.positions[0]

    def reset(self):
        """Данный метод позволяет сбросить змейку в исходное состояние."""
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = None

    def move(self) -> None:
        """Этот метод позволяет передвигаться змейке,
        в начало списка добавляются новые координаты,
        а последний элемент удаляется.
        """
        head_position = self.get_head_position()
        new_position_head = (head_position[0] + self.direction[0] * GRID_SIZE,
                             head_position[1] + self.direction[1] * GRID_SIZE)
        if new_position_head[0] > SCREEN_WIDTH:
            new_position_head = (new_position_head[0] - SCREEN_WIDTH - 20,
                                 new_position_head[1])
        elif new_position_head[0] < 0:
            new_position_head = (new_position_head[0] + SCREEN_WIDTH,
                                 new_position_head[1])
        elif new_position_head[1] < 0:
            new_position_head = (new_position_head[0],
                                 new_position_head[1] + SCREEN_HEIGHT + 20)
        elif (new_position_head[1] > SCREEN_HEIGHT and new_position_head[1]
              % SCREEN_HEIGHT != 0):
            new_position_head = (new_position_head[0], new_position_head[1] %
                                 SCREEN_HEIGHT)
        self.positions.insert(0, new_position_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Функция, которая обрабатывает действия пользователя."""
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
    """Основной цикл игры, перед бесконечным циклом создаются экземпляры
    классов Apple и Snake, инициализируется PyGame.
    """
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw(screen, apple.position, APPLE_COLOR, BORDER_COLOR)
        snake.draw(screen, SNAKE_COLOR, BORDER_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            """Следующую строку я добавил по приколу (можно удалить).
            """
            print(f'Вы проиграли, длина змейки: {snake.length}')
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw(screen, SNAKE_COLOR, BORDER_COLOR)
            apple.draw(screen, apple.position, APPLE_COLOR, BORDER_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
