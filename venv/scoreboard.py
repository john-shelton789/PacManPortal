import pygame.font
from pygame.sprite import Group
from PacMan import PacMan

class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        #self.images = images

        # Font settings for scoring information
        self.text_color = (255, 255, 25)
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.smallerfont = pygame.font.SysFont("Comic Sans MS", 14)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives(screen)

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: " + "{:,}".format(high_score)

       # high_scores = open("images/high_scores.txt", "a")
       # high_scores.write(high_score_str)
       # high_scores.write("\n")
       # high_scores.close()


        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.x = 900
        self.high_score_rect.y = 415


    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render("Level " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self, screen):
        """Show how many ships are left"""
        #useless, delete this fcn
        pass

    def show_score(self):
        """Draw scores and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        for life_number in range(self.stats.lives_left):
            life = pygame.image.load("img/Life.png")
            self.screen.blit(life, ((1100 + life_number * 30), 150))
        
        fruitimg = pygame.image.load("img/fruit.png")
        self.screen.blit(fruitimg, (1150, 200))

        help_str1 = "Press W for Orange Portal"
        self.help_str1_image = self.smallerfont.render(help_str1, True, self.text_color, self.ai_settings.bg_color)
        self.help_str1_rect = self.help_str1_image.get_rect()
        self.help_str1_rect.x = 930
        self.help_str1_rect.y = 615
        self.screen.blit(self.help_str1_image, self.help_str1_rect)

        help_str2 = "Press E for Blue Portal"
        self.help_str2_image = self.smallerfont.render(help_str2, True, self.text_color, self.ai_settings.bg_color)
        self.help_str2_rect = self.help_str2_image.get_rect()
        self.help_str2_rect.x = 930
        self.help_str2_rect.y = 645
        self.screen.blit(self.help_str2_image, self.help_str2_rect)

