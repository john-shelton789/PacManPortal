import pygame
from pygame.sprite import Sprite

class RedPortalBullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, player):
        """Create a bullet object at the ship's current position"""
        super(RedPortalBullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0,0, 5, 5)
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery


        self.color = (255, 128, 10)
        self.speed_factor = 10
        self.direction = "up"

        if player.movingRight:
            self.direction = "right"
        elif player.movingLeft:
            self.direction = "left"
        elif player.movingUp:
            self.direction = "up"
        elif player.movingDown:
            self.direction = "down"



        # Play laser sound effect
        # self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        # self.bullet_sound.set_volume(0.1)
        # self.bullet_sound.play()

    def update(self, walls, redportal):
        """Move the bullet up the screen"""
        if self.direction == "up":
            self.rect.y -= self.speed_factor
        elif self.direction == "down":
            self.rect.y += self.speed_factor
        elif self.direction == "left":
            self.rect.x -= self.speed_factor
        elif self.direction == "right":
            self.rect.x += self.speed_factor

        # If red portal bullet touches a wall, spawn the red portal
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            redportal.activated = True
            if self.direction == "up":
                redportal.rect.centerx = collision.rect.centerx
                redportal.rect.centery = collision.rect.centery + 32
                self.kill()
            if self.direction == "down":
                redportal.rect.centerx = collision.rect.centerx
                redportal.rect.centery = collision.rect.centery - 32
                self.kill()
            if self.direction == "left":
                redportal.rect.centerx = collision.rect.centerx + 32
                redportal.rect.centery = collision.rect.centery
                self.kill()
            if self.direction == "right":
                redportal.rect.centerx = collision.rect.centerx - 32
                redportal.rect.centery = collision.rect.centery
                self.kill()


    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

class BluePortalBullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, player):
        """Create a bullet object at the ship's current position"""
        super(BluePortalBullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0,0, 5, 5)
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery


        self.color = (0, 242, 255)
        self.speed_factor = 10
        self.direction = "up"

        if player.movingRight:
            self.direction = "right"
        elif player.movingLeft:
            self.direction = "left"
        elif player.movingUp:
            self.direction = "up"
        elif player.movingDown:
            self.direction = "down"



        # Play laser sound effect
        # self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        # self.bullet_sound.set_volume(0.1)
        # self.bullet_sound.play()

    def update(self, walls, blueportal):
        """Move the bullet up the screen"""
        if self.direction == "up":
            self.rect.y -= self.speed_factor
        elif self.direction == "down":
            self.rect.y += self.speed_factor
        elif self.direction == "left":
            self.rect.x -= self.speed_factor
        elif self.direction == "right":
            self.rect.x += self.speed_factor


        # If red portal bullet touches a wall, spawn the red portal
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            blueportal.activated = True
            if self.direction == "up":
                blueportal.rect.centerx = collision.rect.centerx
                blueportal.rect.centery = collision.rect.centery + 32
                self.kill()
            if self.direction == "down":
                blueportal.rect.centerx = collision.rect.centerx
                blueportal.rect.centery = collision.rect.centery - 32
                self.kill()
            if self.direction == "left":
                blueportal.rect.centerx = collision.rect.centerx + 32
                blueportal.rect.centery = collision.rect.centery
                self.kill()
            if self.direction == "right":
                blueportal.rect.centerx = collision.rect.centerx - 32
                blueportal.rect.centery = collision.rect.centery
                self.kill()


    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class RedPortal(Sprite):
    """A class to show the red portal"""

    def __init__(self, ai_settings, screen):
        """Create a bullet object at the ship's current position"""
        super(RedPortal, self).__init__()
        self.screen = screen

        # Create a portal rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0,0, 35, 35)
        self.rect.centerx = 5000
        self.rect.centery = 5000


        self.color = (255, 128, 10)
        self.activated = False


        # Play laser sound effect
        # self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        # self.bullet_sound.set_volume(0.1)
        # self.bullet_sound.play()

    def update(self, walls):

        pass



    def blitme(self):
        """Draw the portal to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

class BluePortal(Sprite):
    """A class to show the blue portal"""

    def __init__(self, ai_settings, screen):
        """initialize the portal off screen and make it inactive"""
        super(BluePortal, self).__init__()
        self.screen = screen

        # Create a portal rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0,0, 35, 35)
        self.rect.centerx = 5000
        self.rect.centery = 5000


        self.color = (0, 242, 255)
        self.activated = False


        # Play laser sound effect
        # self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        # self.bullet_sound.set_volume(0.1)
        # self.bullet_sound.play()

    def update(self, walls):

        pass



    def blitme(self):
        """Draw the portal to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)