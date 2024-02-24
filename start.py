import os
import sys

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
        self.name_input = pygame.Rect(200, 100, 200, 50)
        self.name_input_text = pygame.font.SysFont("Arial", 36).render("", True, (0, 0, 0))

        # Флаг, указывающий, что окно должно быть закрыто
        self.close_window = False

        # Флаг, указывающий, что кнопка "Играть" была нажата
        self.play_button_clicked = False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.collidepoint(event.pos):
                    # Установка флага, что кнопка "Играть" была нажата
                    self.play_button_clicked = True

    def draw(self):
        # Заполнение окна белым цветом
        self.window.fill((255, 255, 255))

        # Отрисовка кнопки "Играть"
        pygame.draw.rect(self.window, (0, 179, 0), self.play_button)
        self.window.blit(self.play_button_text, (self.play_button.x + 50, self.play_button.y + 10))

        # Отрисовка поля для ввода имени
        pygame.draw.rect(self.window, (0, 0, 0), self.name_input)
        self.window.blit(self.name_input_text, (self.name_input.x + 50, self.name_input.y + 10))

        # Отображение окна
        pygame.display.update()

    def run(self):
        while not self.close_window:
            self.handle_events()
            self.draw()

            # Проверка, была ли нажата кнопка "Играть"
            if self.play_button_clicked:
                # Преобразование объекта pygame.Surface в строку
                name_input_text_string = pygame.image.tostring(self.name_input_text, "RGB")

                # Запуск файла main.py
                subprocess.call(["python", "main.py"])

                # Закрытие окна запуска
                self.close_window = True

                close()

def close():
    pygame.quit()




if __name__ == '__main__':
    window = StartWindow()
    window.run()
