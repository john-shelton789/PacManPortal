import pygame
from pygame.sprite import Sprite
import spritesheet
from time import sleep

class DeathAnimation(Sprite):

    def __init__(self, screen, x_coord, y_coord):
        """Initialize the ship and set its starting position"""
        super(DeathAnimation, self).__init__()
        self.screen = screen

        # Load the explosion image and get its rect.
        self.death_images = spritesheet.spritesheet("img/PacManDeath.png")
        self.images = self.death_images.images_at([(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24), (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24), (0, 240, 24, 24), (0, 264, 24, 24), (0, 288, 24, 24), (0, 312, 24, 24), (0, 336, 24, 24), (0, 360, 24, 24), (0, 384, 24, 24), (0, 408, 0, 0)], colorkey=(0, 0, 0))
        self.aindex = 0
        self.framecounter = 0
        self.framelimit = 5
        self.image = self.images[0]

        # Play death sound
        self.death_sound = pygame.mixer.Sound("sound/pacman_death.wav")
        self.death_sound.set_volume(0.5)
        self.death_sound.play()


        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each explosion wherever the alien that died is
        self.rect.centerx = x_coord
        self.rect.centery = y_coord

    def update(self):
        """Move the explosion along, then delete it when it gets to the end"""
        self.framecounter = self.framecounter + 1

        if self.framecounter >= self.framelimit:
            self.framecounter = 0
            self.image = self.images[self.aindex]
            self.aindex += 1
        
            if self.aindex == 17:
                sleep(0.5)
                self.kill()

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)