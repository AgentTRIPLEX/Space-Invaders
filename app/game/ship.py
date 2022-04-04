import random
import pygame

class Ship:
    def __init__(self, color1, color2, square_length, type=0):
        self.color1 = color1
        self.color2 = color2
        self.square_length = square_length
        self.type = type

    def get_sprite(self):
        win = pygame.Surface((self.get_width(), self.get_height()), pygame.SRCALPHA, 32)

        if self.type == 0:
            # Top
            x = self.square_length * 3
            y = 0
            pygame.draw.rect(win, self.color1, (x, y, (self.square_length * 2), (self.square_length * 3)))

            # Mid-Left 3
            x = 0
            y = self.square_length * 5
            pygame.draw.rect(win, self.color2, (x, y, self.square_length, (self.square_length * 2)))

            # Mid-Left 2
            x = self.square_length
            y = self.square_length * 5
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, (self.square_length * 2)))

            # Mid-Left 1
            x = self.square_length * 2
            y = self.square_length * 3
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, (self.square_length * 4)))

            # Middle
            x = self.square_length * 3
            y = self.square_length * 3
            pygame.draw.rect(win, self.color2, (x, y, (self.square_length * 2), (self.square_length * 4)))

            # Mid-Right 1
            x = self.square_length * 5
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, (self.square_length * 4)))

            # Mid-Right 2
            x = self.square_length * 6
            y = self.square_length * 5
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, (self.square_length * 2)))

            # Mid-Right 3
            x = self.square_length * 7
            y = self.square_length * 5
            pygame.draw.rect(win, self.color2, (x, y, self.square_length, (self.square_length * 2)))

            # Bottom
            x = self.square_length * 3
            y = self.square_length * 7
            pygame.draw.rect(win, self.color1, (x, y, (self.square_length * 2), self.square_length))

        elif self.type == 1:
            # TOP
            x = self.square_length * 2
            y = 0
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

            # MID-LEFT 2
            x = 0
            y = self.square_length * 2
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

            # MID-LEFT 1
            x = self.square_length
            y = self.square_length
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

            # MIDDLE
            x = self.square_length * 2
            y = self.square_length
            pygame.draw.rect(win, self.color2, (x, y, self.square_length, self.square_length))

            # MID-RIGHT 1
            x = self.square_length * 3
            y = self.square_length
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

            # MID-RIGHT 2
            x = self.square_length * 4
            y = self.square_length * 2
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

        elif self.type == 2:
            # TOP
            x = self.square_length
            y = 0
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, (self.square_length * 2)))

            # MID-LEFT
            x = 0
            y = self.square_length * 2
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

            # MIDDLE
            x = self.square_length
            y = self.square_length * 2
            pygame.draw.rect(win, self.color2, (x, y, self.square_length, self.square_length))

            # MID-RIGHT
            x = self.square_length * 2
            y = self.square_length * 2
            pygame.draw.rect(win, self.color1, (x, y, self.square_length, self.square_length))

        if self.type in [1, 2]:
            win = pygame.transform.rotate(win, 180)

        return win

    def get_width(self):
        if self.type == 0:
            return self.square_length * 8
        elif self.type == 1:
            return self.square_length * 5
        elif self.type == 2:
            return self.square_length * 3

    def get_height(self):
        if self.type == 0:
            return self.square_length * 8
        elif self.type == 1:
            return self.square_length * 3
        elif self.type == 2:
            return self.square_length * 3
