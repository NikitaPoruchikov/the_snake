from random import randint

import pygame

# Привет Ревьювер!
# Инициализация PyGame:
pygame.init()

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
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка из Слизарина")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский class GameObject."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Метод опысывает центр поля и цвет фона"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Дэфолтный pass."""
        pass

    def draw_cell(self, position, surface, color=None):
        """
        TODO: Новый метод
        Метод отрисовок ячейек.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))

        if color is None:
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        else:
            pygame.draw.rect(surface, color, rect)


class Snake(GameObject):
    """Класс для объекта змейка"""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        # TODO: Я не могу убрать аргументы в reset() pytest не пропустит.
        # TODO: Мой косяк! Теперь всё работает.
        super().__init__(body_color)
        self.reset()
        self.last = None

    def draw(self, surface):
        """
        Метод который рисует змейку
        использовал метод 'draw_cell'.
        """
        # TODO: Тут я убрал копирования кода.
        self.draw_cell(self.positions[0], surface)
        if self.last:
            self.draw_cell(
                (self.last[0], self.last[1]
                 ), surface, color=BOARD_BACKGROUND_COLOR
            )

    def move(self):
        """Метод обновляет позицию змейки."""
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction

        position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, position)
        if len(self.positions) > (self.length):
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, direction):
        """Метод обновляет направление движения змейки"""
        # TODO: Переделал метод и использую для handle_keys()
        if direction:
            self.direction = direction
            self.next_direction = None

    def get_head_position(self):
        """Метод вызывается в случаи столкновения из reset"""
        # TODO: Убрал условия проверки.
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние"""
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс Яблока"""

    def __init__(self, snake_position=[], body_color=APPLE_COLOR) -> None:
        # TODO: Передаем координаты змейки.
        super().__init__(body_color)
        self.snake_position = snake_position
        self.position = self.randomize_position()

    def draw(self, surface):
        """Метод рисует яблоко"""
        # TODO: Убрал лишний код использую draw_cell.
        self.draw_cell((self.position[0], self.position[1]), surface)

    def randomize_position(self):
        """
        Метод создает рандомные координаты спавна яблока.
        А так же не допускает спавна яблока в змейке.
        """
        # TODO: Использую цикл для бесконечной проверки.
        while True:
            self.position = (randint(0, 31) * GRID_SIZE,
                             randint(0, 23) * GRID_SIZE)
            if self.position not in self.snake_position:
                return self.position


def handle_keys(game_object):
    """Функция позволяет нам передвигатся змейкой"""
    # TODO: Сделал словарь, сделал условия применил update_direction().
    som_dict = {
        (pygame.K_UP, LEFT): UP,
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_LEFT, DOWN): LEFT,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_RIGHT, UP): RIGHT,
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            direction = som_dict.get(
                (event.key, game_object.direction)
            )
            game_object.update_direction(direction)


def main():
    """Функция создания объектов"""
    # TODO: Тут передал в объект яблоко координаты змея.
    snake = Snake()
    snake_position = snake.positions
    apple = Apple(snake_position)
    screen.fill(BOARD_BACKGROUND_COLOR)
    print("Start Game...")

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        apple.draw(screen)
        snake.draw(screen)
        # Условия проверяющий что наша змейка кушает яблоко!
        if snake.positions[0] == apple.position:
            apple.randomize_position()
            snake.length += 1
        # TODO: Изменил условия проверки и перенес из Reset() сюда.
        for position in snake.positions[4:]:
            if position == snake.get_head_position():
                snake.reset()

        pygame.display.update()


if __name__ == "__main__":
    main()
