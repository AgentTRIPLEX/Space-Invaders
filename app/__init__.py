import pygame

pygame.init()

def run_app():
    from .window import Window
    from .game import Game

    window = Window()

    game = Game(window)
    game.run()