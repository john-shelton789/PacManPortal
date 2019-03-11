import pygame

class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Pac Man in an inactive state.
        self.game_active = False
        self.scores_visible = False
        self.high_score = 0
        self.level = 1
        self.lives_left = self.ai_settings.number_lives
        # Start the BGM
        # Set up the background music
        # self.bgm = pygame.mixer.music.load("sound/bgmusic.mp3")
        # High score should never be reset
        self.high_scores_list = open("high_scores.txt", "r")
        self.scores_list = []
        
        # Read the high scores from the file
        while True:
            self.current_score = self.high_scores_list.readline()
            self.scores_list.append(self.current_score)
            if self.current_score == "":
                break

        # Convert the high scores to ints
        index = 0
        for score in self.scores_list:
            strippedscore = score.rstrip("\r\n")
            score = ("0" + score)
            score = int(score)
            self.scores_list[index] = score
            index += 1

        self.scores_list.sort()
        self.scores_list.reverse()

        if self.scores_list[0] == "":
            self.high_score = 0
        else:
            self.high_score = int(float(self.scores_list[0]))

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.lives_left = self.ai_settings.number_lives
        self.score = 0
        self.level = 1


