import pygame
import subprocess


class StartWindow:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()

        # Создание окна
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Запуск игры")

        # Создание кнопки "Играть"
        self.play_button = pygame.Rect(200, 200, 200, 50)
        self.play_button_text = pygame.font.SysFont("Arial", 36).render("Играть", True, (0, 0, 0))

        # Создание поля для ввода имени
        self.input_box = pygame.Rect(200, 100, 200, 50)
        self.input_text = ''
        self.active = False

        # Флаг, указывающий, что окно должно быть закрыто
        self.close_window = False

        # Флаг, указывающий, что кнопка "Играть" была нажата
        self.play_button_clicked = False

        # Загрузка изображения фона
        self.background_image = pygame.image.load('fon.jpg')
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (640, 480))  # Масштабирование изображения под размер окна

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка, был ли клик в поле ввода имени
                if self.input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
                # Проверка, была ли нажата кнопка "Играть"
                if self.play_button.collidepoint(event.pos):
                    # Установка флага, что кнопка "Играть" была нажата
                    self.play_button_clicked = True
            elif event.type == pygame.KEYDOWN:
                # Проверка, была ли нажата клавиша Enter
                if event.key == pygame.K_RETURN:
                    # Если нажата клавиша Enter, начать игру
                    game_state = 'dealing'
                # Проверка, была ли нажата клавиша Backspace
                elif event.key == pygame.K_BACKSPACE:
                    # Если нажата клавиша Backspace, удалить последний символ из введенного текста
                    self.input_text = self.input_text[:-1]
                # Проверка, была ли нажата любая другая клавиша
                else:
                    # Если нажата любая другая клавиша, добавить ее к введенному тексту
                    self.input_text += event.unicode

    def draw(self):
        # Отрисовка фона
        self.window.blit(self.background_image, (0, 0))

        # Отрисовка кнопки "Играть"
        pygame.draw.rect(self.window, (0, 179, 0), self.play_button)
        self.window.blit(self.play_button_text, (self.play_button.x + 50, self.play_button.y + 10))

        # Отрисовка поля для ввода имени
        pygame.draw.rect(self.window, (0, 0, 0), self.input_box)
        pygame.draw.rect(self.window, (128, 128, 128), self.input_box.inflate(-4, -4))  # Добавление затемнения

        # Создание и обновление текстовой поверхности с текущим введенным текстом
        self.text_surface = pygame.font.Font('freesansbold.ttf', 20).render(self.input_text.encode('utf-8'), True,
                                                                            (0, 0, 0))

        # Отображение текстовой поверхности в окне
        self.window.blit(self.text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Отображение окна
        pygame.display.update()

    def run(self):
        while not self.close_window:
            self.handle_events()
            self.draw()

            # Проверка, была ли нажата кнопка "Играть"
            if self.play_button_clicked:
                # Запись имени пользователя в файл `player_name.txt` в кодировке UTF-8
                with open('player_name.txt', 'w', encoding='utf-8') as f:
                    f.write(self.input_text)

                # Запуск файла main.py
                subprocess.call(["python", "main.py"])

                # Закрытие окна запуска
                self.close_window = True

                # Вызов функции close() для завершения работы PyGame
                close()


class ResultWindow:  # Поздравление, победа
    def __init__(self):
        # Инициализация PyGame
        pygame.init()

        # Создание окна
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Результат игры")

        # Получение имени победителя из файла `player_name.txt`
        with open('player_name.txt', 'r', encoding='utf-8') as f:
            winner_name = f.read()

        # Загрузка изображения фона
        self.background_image = pygame.image.load('fon.jpg')
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (640, 480))  # Масштабирование изображения под размер окна

        # Отрисовка фона
        self.window.blit(self.background_image, (0, 0))

        # Создание текстовой поверхности с сообщением о победителе
        self.winner_text = pygame.font.SysFont("Arial", 36).render(f"Поздравляю, {winner_name}, вы победили!", True,
                                                                   (0, 0, 0))

        # Отрисовка фона
        self.window.blit(self.background_image, (0, 0))

        # Отрисовка текстовой поверхности с сообщением о победителе
        self.window.blit(self.winner_text, (10, 40))

        # Отображение окна
        pygame.display.update()
        pygame.time.wait(5000)
        close()


class nobodyWindow:  # Ничья
    def __init__(self):
        # Инициализация PyGame
        pygame.init()

        # Создание окна
        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Результат игры")

        # Получение имени победителя из файла `player_name.txt`
        with open('player_name.txt', 'r', encoding='utf-8') as f:
            winner_name = f.read()

        # Загрузка изображения фона
        self.background_image = pygame.image.load('fon.jpg')
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (640, 480))  # Масштабирование изображения под размер окна

        # Отрисовка фона
        self.window.blit(self.background_image, (0, 0))

        # Создание текстовой поверхности с сообщением о ничьей
        self.x3 = pygame.Rect(200, 200, 200, 50)
        self.draw_text = pygame.font.SysFont("Arial", 36).render(f"{winner_name}, ничья!", True, (0, 0, 0))

        # Отрисовка фона
        self.window.blit(self.background_image, (0, 0))

        # Отрисовка текстовой поверхности с сообщением о ничьей
        self.window.blit(self.draw_text, (10, 40))

        # Отображение окна
        pygame.display.update()

        pygame.time.wait(5000)

        close()


def close():
    pygame.quit()


def main(self):
    # Создание окна запуска игры
    start_window = StartWindow()
    start_window.run()


if __name__ == '__main__':
    window = StartWindow()
    window.run()
