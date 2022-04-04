import pygame

class Window:
    def __init__(self):
        self.isRunning = True
        self.WIDTH = 600
        self.HEIGHT = 600
        self.FPS = 60

        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()