# Из модуля random импортируем функции choice и randint
from random import choice, randint
# Из модуля typing импортируем функцию Optional
from typing import Optional

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты.

    Он содержит общие атрибуты игровых объектов.
    """

    def __init__(self) -> None:
        """Инициализатор класса GameObject, определяем два атрибута объекта."""
        self.position: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: Optional[tuple] = None

    def draw_cell(self, surface, position, color, bg_color):
        """Метод draw_cell предназначен для отрисовки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, bg_color, rect, 1)

    def draw(self, surface, position, color, bg_color):
        """Метод draw с выбросом ошибки о том что метод не реализован."""
        raise NotImplementedError('Метод не реализован.')


class Apple(GameObject):
    """Класс Apple описывает яблоко и действия с ним.

    Является дочерним классом родительского класса GameObject.
    """

    def __init__(self, occupied_cells=None) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """Метод, описывающий случайное появление яблоко на игровом поле."""
        while True:
            position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if not occupied_cells or position not in occupied_cells:
                break
        self.position = position

    def draw(self, surface, position, color, bg_color):
        """Метод draw для дочернего класса Apple."""
        super().draw_cell(surface, position, color, bg_color)


class Snake(GameObject):
    """Класс Snake описывает змейку, ее поведение на игровом поле.

    Позволяет управлять ее движением, отрисовкой.
    Также обрабатывает действия пользователя.
    """

    def __init__(self) -> None:
        """Инициализатор дочернего класса Snake.

        Определяем необходимые атрибуты объекта.
        """
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
        """Метод, благодаря которому отрисовывается змейка на игровом поле.

        Также отрисовывает голову и затирает последний элемент змейки.
        """
        for position in self.positions[:-1]:
            super().draw_cell(surface, position, color, bg_color)
        super().draw_cell(surface, self.get_head_position(), color, bg_color)
        if self.last:
            super().draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR,
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
        """Этот метод позволяет передвигаться змейке.

        В начало списка добавляются новые координаты.
        Последний элемент удаляется.
        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_position_head = (head_x + direction_x * GRID_SIZE,
                             head_y + direction_y * GRID_SIZE)
        new_pos_x, new_pos_y = new_position_head
        if new_pos_x > SCREEN_WIDTH:
            new_position_head = (new_pos_x - SCREEN_WIDTH
                                 - GRID_SIZE, new_pos_y)
        elif new_pos_x < 0:
            new_position_head = (new_pos_x + SCREEN_WIDTH,
                                 new_pos_y)
        elif new_pos_y < 0:
            new_position_head = (new_pos_x,
                                 new_pos_y + SCREEN_HEIGHT
                                 + GRID_SIZE)
        elif (new_pos_y > SCREEN_HEIGHT and new_pos_y
              % SCREEN_HEIGHT != 0):
            new_position_head = (new_pos_x, new_pos_y %
                                 SCREEN_HEIGHT)
        self.positions.insert(0, new_position_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None


def handle_keys(game_object):
    """Функция, которая обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры.

    Перед бесконечным циклом создаются экземпляры классов Apple и Snake.
    Инициализируется PyGame.
    """
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        apple.draw(screen, apple.position, APPLE_COLOR, BORDER_COLOR)
        snake.draw(screen, SNAKE_COLOR, BORDER_COLOR)
        pg.display.update()


if __name__ == '__main__':
    main()
