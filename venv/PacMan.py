import pygame
from pygame.sprite import Sprite
import spritesheet
import time

class PacMan(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        
        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 500
        self.y = 500

        

        # The coordinates on a 2D grid for pacman
        self.grid_x = 13
        self.grid_y = 13

        # The Sprite for Pacman
        self.pacman_sprite_up = spritesheet.spritesheet("img/PacManUp.png")
        self.pacman_sprite_down = spritesheet.spritesheet("img/PacManDown.png")
        self.pacman_sprite_left = spritesheet.spritesheet("img/PacManLeft.png")
        self.pacman_sprite_right = spritesheet.spritesheet("img/PacManRight.png")
        self.up_images = self.pacman_sprite_up.images_at([(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24), (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.down_images = self.pacman_sprite_down.images_at([(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24), (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.left_images = self.pacman_sprite_left.images_at([(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24), (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.right_images = self.pacman_sprite_right.images_at([(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24), (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.up_images[0]
        self.rect = self.image.get_rect()

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 1



        # The coordinates on the grid for pacman
        self.x = 22
        self.y = 14

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4


        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)



    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self):
        """Update Pacman's position and image"""
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 0 and self.xbuffer <= 6:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)

        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 9:
                self.image_index += 1
            else:
                self.image_index = 0

        if self.movingLeft:
            self.image = self.left_images[self.image_index]
            self.rect.x -= 1
        if self.movingRight:
            self.rect.x += 1
            self.image = self.right_images[self.image_index]
        if self.movingUp:
            self.rect.y -= 1
            self.image = self.up_images[self.image_index]
        if self.movingDown:
            self.rect.y += 1
            self.image = self.down_images[self.image_index]

        

        # print(str(self.x) + " , " + str(self.y))


    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)
