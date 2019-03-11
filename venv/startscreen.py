import pygame
from pygame.sprite import Sprite
import spritesheet
import time


class MenuPacMan(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.turnedaround = False

        self.screen = screen



        # The Sprite for Pacman
        self.pacman_sprite_up = spritesheet.spritesheet("img/PacManUp.png")
        self.pacman_sprite_down = spritesheet.spritesheet("img/PacManDown.png")
        self.pacman_sprite_left = spritesheet.spritesheet("img/PacManLeft.png")
        self.pacman_sprite_right = spritesheet.spritesheet("img/PacManRight.png")
        self.up_images = self.pacman_sprite_up.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.down_images = self.pacman_sprite_down.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.left_images = self.pacman_sprite_left.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))
        self.right_images = self.pacman_sprite_right.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24), (0, 192, 24, 24), (0, 216, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.up_images[0]
        self.rect = self.image.get_rect()

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 5

        # The coordinates on the grid for pacman
        self.x = 12
        self.y = 20

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

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 6 and self.xbuffer <= 7:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)

        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 9:
                self.image_index += 1
            else:
                self.image_index = 0
                
        # Determine movement path for menu pac man
        if self.x == 32 and self.turnedaround == False:
            self.turnedaround = True

        if self.x == 12 and self.turnedaround == True:
            self.turnedaround = False

        if not self.turnedaround:
            self.image = self.right_images[self.image_index]
            self.rect.x += 1

        if self.turnedaround:
            self.rect.x -= 1
            self.image = self.left_images[self.image_index]


        # print(str(self.x) + " , " + str(self.y))

    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)


class MenuInky(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 10
        self.y = 20

        # The Sprite for Inky
        self.blinky_sprite = spritesheet.spritesheet("img/inky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")

        self.images = self.blinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.turnedaround = False

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 5

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self):
        """Update Pacman's position and image"""

        # Test if in intersection, then recompute self.x and self.y
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 0 and self.xbuffer <= 1:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)


        if self.x == 30 and self.turnedaround == False:
            self.turnedaround = True

        if self.x == 10 and self.turnedaround == True:
            self.turnedaround = False

        # Animation and movement
        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 1:
                self.image_index += 1
            else:
                self.image_index = 0

        if not self.turnedaround:
            self.image = self.images[self.image_index + 2]
            self.rect.x += 1

        if self.turnedaround:
            self.image = self.blue_images[self.image_index]
            self.rect.x -= 1


    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)
        
class MenuBlinky(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 8
        self.y = 20

        # The Sprite for Inky
        self.blinky_sprite = spritesheet.spritesheet("img/blinky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")

        self.images = self.blinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.turnedaround = False

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 5

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self):
        """Update Pacman's position and image"""

        # Test if in intersection, then recompute self.x and self.y
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 0 and self.xbuffer <= 1:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)


        if self.x == 28 and self.turnedaround == False:
            self.turnedaround = True

        if self.x == 8 and self.turnedaround == True:
            self.turnedaround = False

        # Animation and movement
        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 1:
                self.image_index += 1
            else:
                self.image_index = 0

        if not self.turnedaround:
            self.image = self.images[self.image_index + 2]
            self.rect.x += 1

        if self.turnedaround:
            self.image = self.blue_images[self.image_index]
            self.rect.x -= 1


    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)

class MenuPinky(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 6
        self.y = 20

        # The Sprite for Inky
        self.pinky_sprite = spritesheet.spritesheet("img/pinky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")

        self.images = self.pinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.turnedaround = False

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 5

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self):
        """Update Pacman's position and image"""

        # Test if in intersection, then recompute self.x and self.y
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 0 and self.xbuffer <= 1:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)


        if self.x == 26 and self.turnedaround == False:
            self.turnedaround = True

        if self.x == 6 and self.turnedaround == True:
            self.turnedaround = False

        # Animation and movement
        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 1:
                self.image_index += 1
            else:
                self.image_index = 0

        if not self.turnedaround:
            self.image = self.images[self.image_index + 2]
            self.rect.x += 1

        if self.turnedaround:
            self.image = self.blue_images[self.image_index]
            self.rect.x -= 1


    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)
        
class MenuClyde(Sprite):

    def __init__(self, ai_settings, screen):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 4
        self.y = 20

        # The Sprite for Inky
        self.clyde_sprite = spritesheet.spritesheet("img/clyde.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")

        self.images = self.clyde_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.turnedaround = False

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 5

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self):
        """Update Pacman's position and image"""

        # Test if in intersection, then recompute self.x and self.y
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        if self.ybuffer >= 0 and self.ybuffer <= 6 and self.xbuffer >= 0 and self.xbuffer <= 1:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)


        if self.x == 24 and self.turnedaround == False:
            self.turnedaround = True

        if self.x == 4 and self.turnedaround == True:
            self.turnedaround = False

        # Animation and movement
        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 1:
                self.image_index += 1
            else:
                self.image_index = 0

        if not self.turnedaround:
            self.image = self.images[self.image_index + 2]
            self.rect.x += 1

        if self.turnedaround:
            self.image = self.blue_images[self.image_index]
            self.rect.x -= 1


    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)