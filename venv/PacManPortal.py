import pygame
from pygame.sprite import Group
import spritesheet
from PacMan import PacMan
import gamefunctions as gf
from settings import Settings
from maze import MazeBlock, powerPill
from game_stats import GameStats
from high_scores import HighScores
from scoreboard import Scoreboard
import ghost
from ghost import Blinky, Inky, Pinky, Clyde
from portalgun import RedPortal, BluePortal
from button import Button
from startscreen import MenuPacMan, MenuInky, MenuBlinky, MenuPinky, MenuClyde

def run_game():
    pygame.init()
    pygame.mixer.init()

    normalsiren = pygame.mixer.music.load("sound/normalsiren.mp3")
    runningsiren = pygame.mixer.music.load("sound/runningsiren.mp3")

    normalsirenplaying = False
    runningsirenplaying = False
    
    #load the settings
    ai_settings = Settings()
    
    # Set up the screen
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Pacman Portal")
    screen_rect = screen.get_rect()
    
    # Timer for ghosts to run away
    timer = pygame.time.Clock()
    timer_started = True
    clock_ticker = 0


    menuRect = pygame.Rect(0, 0, ai_settings.screen_width, ai_settings.screen_height)

    # Show buttons
    play_button = Button(ai_settings, screen, "Play", (600, 400))
    high_scores_button = Button(ai_settings, screen, "High Scores", (screen_rect.centerx, 460))
    back_button = Button(ai_settings, screen, "Back", (screen_rect.centerx, 700))
    # Open the high scores list
    high_scoresfile = open("high_scores.txt", "r")
    high_scores = HighScores(screen)

    # Set up the maze
    maze = [["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X"],
            ["X", ".", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", ".", "X"],
            ["X", "o", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", "o", "X"],
            ["X", ".", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", ".", "X"],
            ["X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X"],
            ["X", ".", "X", "X", "X", "X", ".", "X", "X", ".", "X", "X", "X", "X", "X", "X", "X", ".", "X", "X", ".", "X", "X", "X", "X", ".", "X"],
            ["X", ".", "X", "X", "X", "X", ".", "X", "X", ".", "X", "X", "X", "X", "X", "X", "X", ".", "X", "X", ".", "X", "X", "X", "X", ".", "X"],
            ["X", ".", ".", ".", ".", ".", ".", "X", "X", ".", ".", ".", ".", "X", ".", ".", ".", ".", "X", "X", ".", ".", ".", ".", ".", ".", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", "_", "X", "_", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "_", "_", "_", "_", "B", "_", "_", "_", "_", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "X", "X", "X", "X", "_", "X", "X", "X", "X", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "X", "_", "_", "_", "_", "_", "_", "_", "X", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "_", "_", "_", "_", "_", ".", "_", "_", "X", "_", "I", "_", "_", "_", "P", "_", "X", "_", "_", ".", "_", "_", "_", "_", "_", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "X", "_", "_", "_", "C", "_", "_", "_", "X", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "X", "X", "X", "X", "X", "X", "X", "X", "X", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", ".", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", ".", "X", "_", "X", "X", "X", "X", "X", "X", "X", "X", "X", "_", "X", ".", "X", "X", "X", "X", "X", "X"],
            ["X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X"],
            ["X", ".", "X", "X", "X", "X", ".", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", ".", "X", "X", "X", "X", ".", "X"],
            ["X", "o", ".", ".", "X", "X", ".", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", ".", "X", "X", ".", ".", "o", "X"],
            ["X", "X", "X", ".", "X", "X", ".", ".", ".", ".", ".", ".", ".", "M", ".", ".", ".", ".", ".", ".", ".", "X", "X", ".", "X", "X", "X"],
            ["X", "X", "X", ".", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", ".", "X", "X", "X"],
            ["X", ".", ".", ".", ".", ".", ".", "X", ".", ".", ".", ".", ".", "X", ".", ".", ".", ".", ".", "X", ".", ".", ".", ".", ".", ".", "X"],
            ["X", ".", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", ".", "X", ".", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", ".", "X"],
            ["X", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ]
    
    # Set up the stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings = ai_settings, screen = screen, stats = stats)
    
    walls = Group()
    points = Group()
    pills = Group()
    ghosts = Group()
    redportalbullets = Group()
    blueportalbullets = Group()
    redportals = Group()
    blueportals = Group()
    deathanimations = Group()
    fruits = Group()
    
    # Initialize menu objects
    menupacman = MenuPacMan(ai_settings=ai_settings, screen=screen)
    menupacman.reset_position()
    menupowerpill = powerPill(screen = screen, pos_x = 32, pos_y = 20)
    menuinky = MenuInky(ai_settings = ai_settings, screen = screen)
    menublinky = MenuBlinky(ai_settings = ai_settings, screen = screen)
    menupinky = MenuPinky(ai_settings = ai_settings, screen = screen)
    menuclyde = MenuClyde(ai_settings = ai_settings, screen = screen)
    

    # Initialize Pacman
    
    player = PacMan(ai_settings = ai_settings, screen = screen)
    player.reset_position()
    
    # Initialize Ghosts

    blinky = Blinky(ai_settings=ai_settings, screen=screen, maze=maze, player=player, ghosts = ghosts)
    blinky.reset_position()

    inky = Inky(ai_settings=ai_settings, screen=screen, maze=maze, player=player, ghosts=ghosts)
    inky.reset_position()

    pinky = Pinky(ai_settings=ai_settings, screen=screen, maze=maze, player=player, ghosts=ghosts)
    inky.reset_position()

    clyde = Clyde(ai_settings=ai_settings, screen=screen, maze=maze, player=player, ghosts=ghosts)
    clyde.reset_position()
    
    # Initialize Portals
    redportal = RedPortal(ai_settings = ai_settings, screen = screen)
    blueportal = BluePortal(ai_settings=ai_settings, screen=screen)
    
    # Initialize the game
    # gf.initialize_game(ai_settings = ai_settings, screen = screen, walls = walls, points = points, pills = pills, stats = stats, sb = sb, player = player, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal)


    # Game Loop
    while(True):
        
        
        
        gf.check_events(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, player = player, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, maze = maze, walls = walls, points = points, pills = pills,
                        redportalbullets = redportalbullets, blueportalbullets = blueportalbullets, redportal = redportal, blueportal = blueportal, play_button = play_button, back_button = back_button, high_scores_button = high_scores_button)

        gf.update_screen(ai_settings = ai_settings, screen = screen, player = player, walls = walls , points = points, pills = pills, fruits = fruits, stats = stats, sb = sb, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, ghosts = ghosts,
                         redportalbullets = redportalbullets, blueportalbullets = blueportalbullets, redportal = redportal, blueportal = blueportal, deathanimations = deathanimations, play_button = play_button, back_button = back_button, high_scores_button = high_scores_button, menupacman = menupacman, menupowerpill = menupowerpill, menuinky = menuinky, menublinky = menublinky, menupinky = menupinky, menuclyde = menuclyde, timer = timer, timer_started = timer_started, clock_ticker = clock_ticker, normalsiren = normalsiren, runningsiren = runningsiren)


run_game()
