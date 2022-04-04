import os
import time
import random
import pygame
from plyer import notification
from .ship import Ship

pygame.init()
pygame.font.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
LIME = 0, 255, 0
MATTE_GRAY = 123, 123, 124

cwd = os.path.dirname(os.path.abspath(__file__))
fonts_dir = os.path.join(cwd, "fonts")

def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

class Game:
    def __init__(self, window):
        self.window = window

        self.isRunning = True
        self.bg_color = BLACK

        self.player_color = get_random_color()
        self.player_ship = Ship(MATTE_GRAY, self.player_color, 10, 0)
        self.player_sprite = self.player_ship.get_sprite()
        self.player_x = (self.window.WIDTH / 2) - (self.player_sprite.get_width() / 2)
        self.player_y = self.window.HEIGHT - self.player_sprite.get_height() - 25
        self.player_health = 100

        self.projectile_width = 10
        self.projectile_height = 25
        self.projectiles = [] # [[(x, y), color, team=0,1],]
        self.projectile_cooldown = 0.5
        self.last_projectile_time = time.time() - self.projectile_cooldown
        self.enemy_projectile_cooldown = 2

        self.enemy_ships = [] # [[ship, sprite, (x, y), color],]
        self.enemy_projectile_times = [] # [last_projectile_time,]

        self.lives = 5
        self.wave_length = 5
        self.level = 0

        self.create_enemy_ships()

    def run(self):
        while self.window.isRunning and self.isRunning:
            self.window.clock.tick(self.window.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window.isRunning = False

            self.handle_keys()
            self.handle_enemy_ships_and_projectiles()

            if len(self.enemy_ships) == 0:
                self.level += 1
                self.wave_length += 5
                self.create_enemy_ships()

            if self.player_health <= 0:
                self.player_health = 0
                self.draw()
                self.isRunning = False

            if self.lives <= 0:
                self.lives = 0
                self.draw()
                self.isRunning = False

        pygame.time.wait(3000)
        pygame.quit()

    def handle_keys(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (self.player_y > 0):
            self.player_y -= 5
            self.draw()

        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (self.player_y < (self.window.HEIGHT - self.player_sprite.get_height() - 25)):
            self.player_y += 5
            self.draw()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (self.player_x > 0):
            self.player_x -= 5
            self.draw()

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (self.player_x < (self.window.WIDTH - self.player_sprite.get_width())):
            self.player_x += 5
            self.draw()

        if keys[pygame.K_SPACE] and ((time.time() - self.last_projectile_time) >= self.projectile_cooldown):
            self.last_projectile_time = time.time()
            self.create_player_projectile()
            self.draw()

        self.draw()

    def draw(self):
        self.window.win.fill(self.bg_color)

        # Player
        self.window.win.blit(self.player_sprite, (self.player_x, self.player_y))
        x = self.player_x
        y = self.player_y + self.player_sprite.get_height() + 3
        pygame.draw.rect(self.window.win, RED, (x, y, self.player_sprite.get_width(), 22))
        pygame.draw.rect(self.window.win, LIME, (x, y, (self.player_health / 100 * self.player_sprite.get_width()), 22))

        # Projectiles
        for (x, y), color, team in self.projectiles:
            pygame.draw.rect(self.window.win, color, (x, y, self.projectile_width, self.projectile_height))

        # Enemy Ships
        for ship, sprite, (x, y), color in self.enemy_ships:
            self.window.win.blit(sprite, (x, y))

        # Top Bars
        font = pygame.font.SysFont(os.path.join(fonts_dir, "helvetica"), 40)

        render = font.render(f"Lives: {self.lives}", True, WHITE)
        self.window.win.blit(render, (10, 10))

        render = font.render(f"Level: {self.level}", True, WHITE)
        x = self.window.WIDTH - render.get_width() - 10
        self.window.win.blit(render, (x, 10))

        pygame.display.update()

    def create_player_projectile(self):
        color = self.player_color
        x = (self.player_x + (self.player_ship.square_length * 3)) + (self.player_ship.square_length - (self.projectile_width / 2))
        y = (self.player_y - self.projectile_height - 10)
        projectile = [(x, y), color, 0]
        self.projectiles.append(projectile)

    def handle_enemy_ships_and_projectiles(self):
        ## Projectile Movement and Removal, Ship Removal

        projectiles = {i:p for i,p in enumerate(self.projectiles)}

        for i, ((x, y), color, team) in enumerate(self.projectiles):
            if team == 0:
                # Moving the projectile
                y -= 5
                projectile = [(x, y), color, team]
                projectiles[i] = projectile

                # Removing the projectile
                if (y + self.projectile_height) < 0:
                    projectiles.pop(i)
                    continue

                # Checking for projectile collision
                enemy_ships = self.enemy_ships[:]

                for sI, (ship, sprite, (ship_x, ship_y), color) in enumerate(self.enemy_ships):
                    if self.check_rect_collision(x, y, self.projectile_width, self.projectile_height, ship_x, ship_y, *sprite.get_size()):
                        enemy_ships.pop(sI)
                        self.enemy_projectile_times.pop(sI)
                        projectiles.pop(i)
                        break

                self.enemy_ships = enemy_ships[:]

            elif team == 1:
                # Moving the projectile
                y += 5
                projectile = [(x, y), color, team]
                projectiles[i] = projectile

                # Removing the projectile
                if y >= (self.window.HEIGHT + self.projectile_height):
                    projectiles.pop(i)
                    continue

                # Checking for projectile collision
                if self.check_rect_collision(x, y, self.projectile_width, self.projectile_height, self.player_x, self.player_y, *self.player_sprite.get_size()):
                    self.player_health -= 10
                    projectiles.pop(i)

        self.projectiles = list(projectiles.values())

        ## Ship Movement and Removal

        enemy_ships = {i:s for i,s in enumerate(self.enemy_ships)}

        for i, (ship, sprite, (x, y), color) in enumerate(self.enemy_ships):
            y += 1
            ship_arr = [ship, sprite, (x, y), color]
            enemy_ships[i] = ship_arr

            if y >= (self.window.HEIGHT + sprite.get_height()):
                enemy_ships.pop(i)
                self.enemy_projectile_times.pop(i)
                self.lives -= 1

            if self.check_rect_collision(self.player_x, self.player_y, *self.player_sprite.get_size(), x, y, *sprite.get_size()):
                self.player_health -= 10
                enemy_ships.pop(i)
                self.enemy_projectile_times.pop(i)

        self.enemy_ships = list(enemy_ships.values())

        ## Ship Firing

        for i, (ship, sprite, (x, y), color) in enumerate(self.enemy_ships):
            if (y >= 0) and (i < len(self.enemy_projectile_times)) and ((time.time() - self.enemy_projectile_times[i]) >= self.enemy_projectile_cooldown):
                self.create_enemy_projectile(ship, x, y, color)
                self.enemy_projectile_times[i] = time.time()

    def create_enemy_ships(self):
        for i in range(self.wave_length):
            color = get_random_color()
            type = random.choice([1, 2])

            ship = Ship(MATTE_GRAY, color, 10, type)
            sprite = ship.get_sprite()
            sprite = pygame.transform.rotate(sprite, 180)
            x = random.randint(10, (self.window.WIDTH - sprite.get_width() - 10))
            y = random.randint(-1500, -100)

            self.enemy_ships.append([ship, sprite, (x, y), color])
            self.enemy_projectile_times.append(time.time() - self.enemy_projectile_cooldown)

    def create_enemy_projectile(self, ship, x, y, color):
        if ship.type == 1:
            x += (ship.square_length * 2)
            y += (ship.square_length * 2)
        elif ship.type == 2:
            x += ship.square_length
            y += (ship.square_length * 3)

        y += 10
        projectile = [(x, y), color, 1]
        self.projectiles.append(projectile)

    def check_rect_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        x_diff = x1 - x2
        y_diff = y1 - y2
        return (x_diff > -w1) and (x_diff < w2) and (y_diff > -h1) and (y_diff < h2)
