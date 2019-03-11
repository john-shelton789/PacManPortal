import pygame.font
from pygame.sprite import Group

class HighScores:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.high_scores_list = open("high_scores.txt", "r")
        self.pointsfont = pygame.font.SysFont("Comic Sans MS", 64)
        self.scorefont = pygame.font.SysFont("Comic Sans MS", 48)
        self.titlesurface = self.pointsfont.render('HIGH SCORES', False, (255, 255, 25))


        self.scores_list = []

        #Read the high scores from the text file
        while True:
            self.current_score = self.high_scores_list.readline()
            self.scores_list.append(self.current_score)
            if self.current_score == "":
                break
        # Convert the scores to ints to sort them
        index = 0
        for score in self.scores_list:
            strippedscore = score.rstrip("\r\n")
            score = ("0" + score)
            score = int(score)
            self.scores_list[index] = score
            index += 1

        self.scores_list.sort()
        self.scores_list.reverse()

    # Show the scores
    def show_score(self):
        self.screen.blit(self.titlesurface, (self.screen_rect.centerx - 200, 120))
        loopindex = 0
        # display the high scores in a list
        for score in self.scores_list:
            if score == 0:
                break
            score_y = 220 + (loopindex * 40)
            scoresurface = self.scorefont.render(str(loopindex + 1) + ". " + str(score), False, (255, 255, 255))

            self.screen.blit(scoresurface, (self.screen_rect.centerx - 100, score_y))
            loopindex += 1
            # only show the top 10 scores
            if loopindex >= 10:
                break






