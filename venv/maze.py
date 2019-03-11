import pygame
from pygame.sprite import Sprite

class MazeBlock(Sprite):
    """Draw the maze"""
    def __init__(self, screen, pos_x, pos_y):
        super(MazeBlock, self).__init__()
        # load the wall image
        self.screen = screen
        self.image = pygame.image.load("img/Wall.png")
        self.rect = self.image.get_rect()
        self.x, self.y = pos_x, pos_y
        
        # position the wall        
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class powerPoint(Sprite):
    def __init__(self, screen, pos_x, pos_y):
        super(powerPoint, self).__init__()
        # load the point image
        self.screen = screen
        self.image = pygame.image.load("img/powerpoint.png")
        self.rect = self.image.get_rect()
        self.x, self.y = pos_x, pos_y

        # position the wall
        self.rect.x = self.x * 32 + 12
        self.rect.y = self.y * 32 + 12

    def eaten(self):
        self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class powerPill(Sprite):
    def __init__(self, screen, pos_x, pos_y):
        super(powerPill, self).__init__()
        # load the point image
        self.screen = screen
        self.image = pygame.image.load("img/powerpill.png")
        self.rect = self.image.get_rect()
        self.x, self.y = pos_x, pos_y

        # position the wall
        self.rect.x = self.x * 32 + 8
        self.rect.y = self.y * 32 + 8

    def eaten(self):
        self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Fruit(Sprite):
    """Draw the maze"""

    def __init__(self, screen, pos_x, pos_y):
        super(Fruit, self).__init__()
        # load the wall image
        self.screen = screen
        self.image = pygame.image.load("img/fruit.png")
        self.rect = self.image.get_rect()
        self.x, self.y = pos_x, pos_y
        
        self.lifespan = 0

        # position the fruit
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4
        
    def update(self):
        self.lifespan += 1
        if self.lifespan > 500:
            self.kill()
            
    def eaten(self):
        self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)