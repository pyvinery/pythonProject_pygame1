import pygame
import os
import random

# Определение констант
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
CARD_WIDTH, CARD_HEIGHT = 150, 240
# Определите смещение для каждой следующей карты
CARD_OFFSET = CARD_WIDTH / 2.5

# Определение пути к папке с картами
CARD_FOLDER = 'cards'

# Инициализация pygame
pygame.init()

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Получение списка файлов в папке с картами
card_files = [f for f in os.listdir(CARD_FOLDER) if os.path.isfile(os.path.join(CARD_FOLDER, f))]

# Загрузка изображений карт
cards = {}
for filename in card_files:
    card_name = os.path.splitext(filename)[0]
    if card_name != 'back':  # Исключение изображения обратной стороны карты из списка карт
        card_path = os.path.join(CARD_FOLDER, filename)
        image = pygame.image.load(card_path)
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT)) # Масштабирование изображения
        cards[card_name] = image

# Создание списка доступных карт
available_cards = list(cards.keys())


# Функция для сравнения букв в двух строках
def common_letters(string1, string2):
    return len(set(string1) & set(string2))


# Классы Player и Bot
class Player:
    def __init__(self, hand_pos):
        self.hand = []
        self.hand_pos = hand_pos

class Bot:
    def __init__(self, hand_pos):
        self.hand = []
        self.hand_pos = hand_pos

class Card:
    def __init__(self, name, position, hand, position_in_hand):
        self.name = name
        self.position = list(position)
        self.hand = hand
        self.target = None
        self.reached_target = False
        self.position_in_hand = position_in_hand

    def move_towards(self, target, speed):
        # Обновляем цель
        self.target = target

        # Если карта достигла цели, помечаем её как достигшую цели и возвращаем True
        if abs(self.position[0] - self.target[0]) < speed and abs(self.position[1] - self.target[1]) < speed:
            self.position = self.target
            self.reached_target = True
            return True

        # Иначе, продолжаем двигаться к цели
        direction = [self.target[0] - self.position[0], self.target[1] - self.position[1]]
        length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        direction = [direction[0] / length, direction[1] / length]
        self.position[0] += direction[0] * speed
        self.position[1] += direction[1] * speed

        return False


# Создание игроков
player = Player((0, SCREEN_HEIGHT - CARD_HEIGHT))
bot = Bot((0, 0))

# Выбор козыря
trump_card = random.choice(available_cards)
available_cards.remove(trump_card)

# Список движущихся карт
moving_cards = []

# Начальная позиция колоды карт
deck_pos = (SCREEN_WIDTH - CARD_WIDTH, SCREEN_HEIGHT // 2)

# Загрузка изображения обратной стороны карты
back_card_image = pygame.image.load(os.path.join(CARD_FOLDER, 'back.png')).convert_alpha()
back_card_image = pygame.transform.scale(back_card_image, (CARD_WIDTH, CARD_HEIGHT)) # Масштабирование изображения


# Загрузка изображения фона
background_image = pygame.image.load('fon.jpg').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Масштабирование изображения под размер экрана

# Начинаем с пустых рук для игрока и бота
player.hand = []
bot.hand = []

# Состояние игры
game_state = 'dealing'

# Главный цикл игры
running = True
deal_to_player = True  # Начинаем с раздачи карт игроку
while running:
    # Очистка экрана перед каждым новым кадром
    screen.fill((0, 0, 0))

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    if game_state == 'dealing':
        # Если у игрока меньше 6 карт в руке и нет движущихся карт, раздаём ему ещё одну
        if deal_to_player and len(player.hand) < 6 and len(moving_cards) == 0:
            card_name = random.choice(available_cards)
            hand_width = len(player.hand) * CARD_OFFSET
            start_pos = (SCREEN_WIDTH - hand_width) / 2
            target = (start_pos + len(player.hand) * CARD_OFFSET, 3 * SCREEN_HEIGHT / 4)
            moving_cards.append(Card(card_name, deck_pos, player.hand, len(player.hand)))
            moving_cards[-1].target = target
            available_cards.remove(card_name)
            deal_to_player = False  # Переключаемся на раздачу боту
        # Если у бота меньше 6 карт в руке и нет движущихся карт, раздаём ему ещё одну
        elif not deal_to_player and len(bot.hand) < 6 and len(moving_cards) == 0:
            card_name = random.choice(available_cards)
            hand_width = len(bot.hand) * CARD_OFFSET
            start_pos = (SCREEN_WIDTH - hand_width) / 2
            target = (start_pos + len(bot.hand) * CARD_OFFSET, SCREEN_HEIGHT / 4 - CARD_HEIGHT)
            moving_cards.append(Card(card_name, deck_pos, bot.hand, len(bot.hand)))
            moving_cards[-1].target = target
            available_cards.remove(card_name)
            deal_to_player = True  # Переключаемся на раздачу игроку
        else:
            # Если у обоих игроков по 6 карт, переходим к следующему состоянию игры
            if len(player.hand) >= 6 and len(bot.hand) >= 6:
                game_state = 'playing'

        # Добавляем задержку между раздачей карт
        pygame.time.wait(40)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Двигаем карты и удаляем те, которые достигли цели
    for card in moving_cards:
        hand_width = len(card.hand) * CARD_OFFSET
        start_pos = (SCREEN_WIDTH - hand_width) / 2
        target = (start_pos + card.position_in_hand * CARD_OFFSET, card.target[1])
        if card.move_towards(target, 100):
            moving_cards.remove(card)
            if card.reached_target:
                card.hand.append(card.name)

    for card in moving_cards:
        card_image = cards[card.name]
        screen.blit(card_image, tuple(card.position))

    # Для отображения карт в руке игрока
    hand_width = len(player.hand) * CARD_OFFSET
    start_pos = (SCREEN_WIDTH - hand_width) / 2
    for i, card_name in enumerate(player.hand):
        card_image = cards[card_name]
        card_pos = (start_pos + i * CARD_OFFSET, 3 * SCREEN_HEIGHT / 3.407)
        screen.blit(card_image, card_pos)

    # Для отображения карт в руке бота
    hand_width = len(bot.hand) * CARD_OFFSET
    start_pos = (SCREEN_WIDTH - hand_width) / 2
    for i, card_name in enumerate(bot.hand):
        card_image = cards[card_name]
        card_pos = (start_pos + i * CARD_OFFSET, SCREEN_HEIGHT / 8.65 - CARD_HEIGHT)
        screen.blit(card_image, card_pos)

    # Отображение козыря
    trump_image = cards[trump_card]
    trump_image = pygame.transform.rotate(trump_image, 90)  # Поворот карты на 90 градусов
    # Позиция козыря
    trump_pos = (SCREEN_WIDTH - CARD_WIDTH - CARD_WIDTH / 1.7, SCREEN_HEIGHT / 2.3)
    screen.blit(trump_image, trump_pos)

    # Рисование обратной стороны карты (колоды)
    for i in range(3):  # Рисуем три карты для иллюзии
        screen.blit(back_card_image, (SCREEN_WIDTH - CARD_WIDTH - i * 5, SCREEN_HEIGHT // 2.5 - i * 5))

    pygame.display.flip()

pygame.quit()
