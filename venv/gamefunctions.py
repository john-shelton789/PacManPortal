import pygame
import random
from time import sleep
import time
import sys
from PacMan import PacMan
from maze import MazeBlock, powerPoint, powerPill, Fruit
from game_stats import GameStats
from high_scores import HighScores
from scoreboard import Scoreboard
from portalgun import RedPortalBullet, BluePortalBullet
from death import DeathAnimation


def check_events(ai_settings, screen, stats, sb, player, blinky, inky, pinky, clyde, maze, walls, points, pills, redportalbullets, blueportalbullets, redportal, blueportal, play_button, back_button, high_scores_button):

    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event = event, ai_settings = ai_settings, screen = screen, player = player, redportalbullets = redportalbullets, blueportalbullets = blueportalbullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_play_button(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, play_button = play_button, player = player, maze = maze, walls = walls,
                              points = points, pills = pills, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal, mouse_x = mouse_x, mouse_y = mouse_y)
            check_high_scores_button(ai_settings=ai_settings, screen=screen, stats=stats, high_scores_button=high_scores_button, mouse_x=mouse_x, mouse_y=mouse_y)
            check_back_button(ai_settings=ai_settings, back_button=back_button, stats=stats, mouse_x=mouse_x, mouse_y=mouse_y)

def check_keydown_events(event, ai_settings, screen, player, redportalbullets, blueportalbullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        player.movingRight = True
        player.movingLeft = False
        player.movingUp = False
        player.movingDown = False
    if event.key == pygame.K_LEFT:
        player.movingRight = False
        player.movingLeft = True
        player.movingUp = False
        player.movingDown = False
    if event.key == pygame.K_UP:
        player.movingRight = False
        player.movingLeft = False
        player.movingUp = True
        player.movingDown = False
    if event.key == pygame.K_DOWN:
        player.movingRight = False
        player.movingLeft = False
        player.movingUp = False
        player.movingDown = True
    if event.key == pygame.K_w:
        fire_red_portal(ai_settings = ai_settings, screen = screen, player = player, redportalbullets = redportalbullets)
    if event.key == pygame.K_e:
        fire_blue_portal(ai_settings=ai_settings, screen=screen, player = player, blueportalbullets = blueportalbullets)
        
    if event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ai_settings, screen, player):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        player.movingRight = False
    if event.key == pygame.K_LEFT:
        player.movingLeft = False
    if event.key == pygame.K_UP:
        player.movingUp = False
    if event.key == pygame.K_DOWN:
        player.movingDown = False

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_pacman_wall_collisions(player, walls):
    collisions = pygame.sprite.spritecollideany(player, walls)

    if collisions:
        if player.movingDown:
            player.movingDown = False
            player.rect.y -= 4
        if player.movingUp:
            player.movingUp = False
            player.rect.y += 4
        if player.movingLeft:
            player.movingLeft = False
            player.rect.x += 4
        if player.movingRight:
            player.movingRight = False
            player.rect.x -= 4


def check_pacman_point_collisions(ai_settings, screen, stats, sb, walls, points, pills, player, maze, blinky, inky, pinky, clyde, redportal, blueportal, fruits):
    collisions = pygame.sprite.spritecollideany(player, points)
    if collisions:
        stats.score += 10
        sb.prep_score()
        check_high_score(stats=stats, sb=sb)
        collisions.eaten()

        # Play death sound
        chomp_sound = pygame.mixer.Sound("sound/pacman_chomp.wav")
        chomp_sound.set_volume(0.5)
        chomp_sound.play()

    # Test for collisions with power pills
    pillcollisions = pygame.sprite.spritecollideany(player, pills)
    if pillcollisions:
        pillcollisions.eaten()
        stats.score += 50
        sb.prep_score()
        check_high_score(stats=stats, sb=sb)

        if blinky.mode != "returning":
            blinky.mode = "running"
            blinky.rect.x = blinky.x * 32 + 4
            blinky.rect.y = blinky.y * 32 + 4
        if inky.mode != "returning":
            inky.mode = "running"
            inky.rect.x = inky.x * 32 + 4
            inky.rect.y = inky.y * 32 + 4
        if pinky.mode != "Returning":
            pinky.mode = "running"
            pinky.rect.x = pinky.x * 32 + 4
            pinky.rect.y = pinky.y * 32 + 4
        if clyde.mode != "Returning":
            clyde.mode = "running"
            clyde.rect.x = clyde.x * 32 + 4
            clyde.rect.y = clyde.y * 32 + 4
            
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/runningsiren.mp3")
        pygame.mixer.music.play(-1)

    fruitcollisions = pygame.sprite.spritecollideany(player, fruits)
    if fruitcollisions:
        fruitcollisions.eaten()
        stats.score += 100
        sb.prep_score()
        check_high_score(stats = stats, sb = sb)

        # Play death sound
        fruit_sound = pygame.mixer.Sound("sound/pacman_eatfruit.wav")
        fruit_sound.set_volume(0.5)
        fruit_sound.play()

    if len(points) == 0 and len(pills) == 0:
        # If all points are eaten, start a new level
        stats.level += 1
        sb.prep_level()
        draw_maze(ai_settings=ai_settings, screen=screen, walls=walls, points=points, pills = pills, player=player, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal)






def check_pacman_portal_collisions(ai_settings, screen, player, redportal, blueportal, inky, pinky, blinky, clyde):
    redcollide = pygame.sprite.collide_rect(player, redportal)
    if redcollide and redportal.activated == True and blueportal.activated == True and blueportal.rect.centerx < 900 and blueportal.rect.centery < 900:
        player.rect.centerx = blueportal.rect.centerx
        player.rect.centery = blueportal.rect.centery
        redportal.activated = False
        blueportal.activated = False

        inky.rect.x = inky.x * 32 + 4
        inky.rect.y = inky.y * 32 + 4
        pinky.rect.x = pinky.x * 32 + 4
        pinky.rect.y = pinky.y * 32 + 4
        blinky.rect.x = blinky.x * 32 + 4
        blinky.rect.y = blinky.y * 32 + 4
        clyde.rect.x = clyde.x * 32 + 4
        clyde.rect.y = clyde.y * 32 + 4
        
    if not redcollide:
        redportal.activated = True

    bluecollide = pygame.sprite.collide_rect(player, blueportal)
    if bluecollide and redportal.activated == True and blueportal.activated == True and redportal.rect.centerx < 900 and redportal.rect.centery < 900:
        player.rect.centerx = redportal.rect.centerx
        player.rect.centery = redportal.rect.centery
        blueportal.activated = False
        redportal.activated = False
        inky.rect.x = inky.x * 32 + 4
        inky.rect.y = inky.y * 32 + 4
        pinky.rect.x = pinky.x * 32 + 4
        pinky.rect.y = pinky.y * 32 + 4
        blinky.rect.x = blinky.x * 32 + 4
        blinky.rect.y = blinky.y * 32 + 4
        clyde.rect.x = clyde.x * 32 + 4
        clyde.rect.y = clyde.y * 32 + 4
    if not bluecollide:
        blueportal.activated = True

def check_pacman_ghost_collisions(ai_settings, screen, stats, sb, walls, points, pills, deathanimations, player, blinky, inky, pinky, clyde):
    blinkycollide = pygame.sprite.collide_rect(player, blinky)
    inkycollide = pygame.sprite.collide_rect(player, inky)
    pinkycollide = pygame.sprite.collide_rect(player, pinky)
    clydecollide = pygame.sprite.collide_rect(player, clyde)

    if blinkycollide:
        if blinky.mode == "chasing" or blinky.mode == "scatter":
            pacman_hit(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, walls = walls, points = points,
                       pills = pills, deathanimations = deathanimations, player = player, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde)
        if blinky.mode == "running":
            blinky.mode = "returning"
            blinky.rect.x = blinky.x * 32 + 4
            blinky.rect.y = blinky.y * 32 + 4
            # if ghost is running, give points
            ai_settings.ghosts_eaten += 1
            stats.score += 100 * (2 **  ai_settings.ghosts_eaten)
            sb.prep_score()

            #if all ghosts have been eaten, reset the counter
            if ai_settings.ghosts_eaten == 4:
                ai_settings.ghosts_eaten = 0

            # set blinky mode to returning and give points to player
    if inkycollide:
        if inky.mode == "chasing" or inky.mode == "scatter":
            pacman_hit(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, walls = walls, points = points,
                       pills = pills, deathanimations = deathanimations, player = player, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde)
        if inky.mode == "running":
            inky.mode = "returning"
            inky.rect.x = inky.x * 32 + 4
            inky.rect.y = inky.y * 32 + 4
            # if ghost is running, give points
            ai_settings.ghosts_eaten += 1
            stats.score += 100 * (2 ** ai_settings.ghosts_eaten)
            sb.prep_score()

            # if all ghosts have been eaten, reset the counter
            if ai_settings.ghosts_eaten == 4:
                ai_settings.ghosts_eaten = 0

            # set inky mode to returning and give points to player

    if pinkycollide:
        if pinky.mode == "chasing" or pinky.mode == "scatter":
            pacman_hit(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, walls = walls, points = points,
                       pills = pills, deathanimations = deathanimations, player = player, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde)
        if pinky.mode == "running":
            pinky.mode = "returning"
            pinky.rect.x = pinky.x * 32 + 4
            pinky.rect.y = pinky.y * 32 + 4
            # if ghost is running, give points
            ai_settings.ghosts_eaten += 1
            stats.score += 100 * (2 ** ai_settings.ghosts_eaten)
            sb.prep_score()

            # if all ghosts have been eaten, reset the counter
            if ai_settings.ghosts_eaten == 4:
                ai_settings.ghosts_eaten = 0

            # set pinky mode to returning and give points to player

    if clydecollide:
        if clyde.mode == "chasing" or clyde.mode == "scatter":
            pacman_hit(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, walls=walls, points=points,
                       pills=pills, deathanimations=deathanimations, player=player, blinky=blinky, inky=inky, pinky = pinky, clyde = clyde)
        if clyde.mode == "running":
            clyde.mode = "returning"
            clyde.rect.x = clyde.x * 32 + 4
            clyde.rect.y = clyde.y * 32 + 4
            # if ghost is running, give points
            ai_settings.ghosts_eaten += 1
            stats.score += 100 * (2 ** ai_settings.ghosts_eaten)
            sb.prep_score()

            # if all ghosts have been eaten, reset the counter
            if ai_settings.ghosts_eaten == 4:
                ai_settings.ghosts_eaten = 0

            # set clyde mode to returning and give points to player


def initialize_game(ai_settings, screen, walls, points, pills, player, stats, sb, maze, blinky, inky, pinky, clyde, redportal, blueportal):
    draw_maze(ai_settings = ai_settings, screen = screen, walls = walls, points = points, pills = pills, player = player, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal)
    stats.reset_stats()



def fire_red_portal(ai_settings, screen, player, redportalbullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group
    if len(redportalbullets) < 1:
        new_bullet = RedPortalBullet(ai_settings = ai_settings, screen = screen, player = player)
        redportalbullets.add(new_bullet)

def fire_blue_portal(ai_settings, screen, player, blueportalbullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group
    if len(blueportalbullets) < 1:
        new_bullet = BluePortalBullet(ai_settings = ai_settings, screen = screen, player = player)
        blueportalbullets.add(new_bullet)

def check_play_button(ai_settings, screen, stats, sb, play_button, player, maze, walls, points, pills, blinky, inky, pinky, clyde, redportal, blueportal, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active and not stats.scores_visible:
        # Reset the game settings
        # ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        newgamemusic = pygame.mixer.music.load("sound/pacman_beginning.wav")
        pygame.mixer.music.play(0)
        sleep(5)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        # Initialize the map
        initialize_game(ai_settings = ai_settings, screen = screen, walls = walls, points = points, pills = pills, stats = stats, sb = sb, player = player, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal)

def check_high_scores_button(ai_settings, screen, stats, high_scores_button, mouse_x, mouse_y):
    button_clicked = high_scores_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.scores_visible = True

def check_back_button(ai_settings, back_button, stats, mouse_x, mouse_y):
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.scores_visible = False


def pacman_hit(ai_settings, screen, stats, sb, walls, points, pills, deathanimations, player, blinky, inky, pinky, clyde):

    pygame.mixer.music.stop()
    deathanim = DeathAnimation(screen, player.rect.centerx, player.rect.centery)
    deathanimations.add(deathanim)
    
    if stats.lives_left > 0:
        # lose a life
        stats.lives_left -= 1
        
        # Update scoreboard
        # sb.prep_lives()
        
        # Reset Pac Man's location as well as the ghosts
        player.x = 13
        player.y = 21
        player.reset_position()
        blinky.x = 13
        blinky.y = 10
        blinky.reset_position()
        inky.x = 11
        inky.y = 13
        inky.reset_position()
        pinky.x = 13
        pinky.y = 13
        pinky.reset_position()
        clyde.x = 15
        clyde.y = 13
        clyde.reset_position()
        # Pause.
        sleep(2)
        pygame.mixer.music.load("sound/normalsiren.mp3")
        pygame.mixer.music.play(-1)
        
    else:
        print(stats.score)
        # Add score to high scores list.  formerly stats.high_score
        high_score_int = int(round(stats.score, -1))
        high_score_str = str(high_score_int)
        high_scores = open("high_scores.txt", "a")
        #pygame.mixer.quit()
        
        high_scores.write(high_score_str)
        high_scores.write("\n")
        high_scores.close()

        stats.game_active = False
        pygame.mouse.set_visible(True)



def generate_fruits(ai_settings, screen, maze, fruits):

        fruitrng = random.randint(1, 100)
        fruitx = random.randint(1, 25)
        fruity = random.randint(1, 25)

        if fruitrng == 1 and maze[fruity][fruitx] != "X":
            # print str(fruitx) + " , " + str(fruity) + " = "  + maze[fruitx][fruity]
            fruit = Fruit(screen = screen, pos_x = fruitx, pos_y = fruity )
            fruits.add(fruit)


def check_ghosts_running(inky, blinky, pinky, clyde):
    if inky.mode == "running" or blinky.mode == "running" or pinky.mode == "running" or clyde.mode == "running":
        return True
    else:
        return False




def draw_maze(ai_settings, screen, walls, points, pills, player, maze, blinky, inky, pinky, clyde, redportal, blueportal):
    maze = maze

    siren = pygame.mixer.music.load("sound/normalsiren.mp3")
    pygame.mixer.music.play(-1)

    y = 0
    for line in maze:
        x = 0
        for char in line:
            if char == 'X':
                block = MazeBlock(screen, pos_x = x, pos_y = y)
                walls.add(block)
            if char == "M":
                player.x = x
                player.y = y
                player.reset_position()
            if char == "B":
                blinky.x = x
                blinky.y = y
                blinky.reset_position()
            if char == "I":
                inky.x = x
                inky.y = y
                inky.reset_position()
            if char == "P":
                pinky.x = x
                pinky.y = y
                pinky.reset_position()
            if char == "C":
                clyde.x = x
                clyde.y = y
                clyde.reset_position()
            if char == ".":
                point = powerPoint(screen, pos_x = x, pos_y = y)
                points.add(point)
            if char == "o":
                pill = powerPill(screen, pos_x = x, pos_y = y)
                pills.add(pill)

            x += 1
        y += 1

    # initialize the red and blue portals
    redportal.rect.centerx = 5000
    redportal.rect.centery = 5000
    blueportal.rect.centerx = 5000
    blueportal.rect.centery = 5000

    inky.startupcounter = 0
    pinky.startupcounter = 0
    clyde.startupcounter = 0
    """
    blinky.mode = "chasing"
    inky.mode = "chasing"
    pinky.mode = "chasing"
    clyde.mode = "chasing"
    """

def update_screen(ai_settings, screen, player, walls, points, pills, fruits, stats, sb, maze, ghosts, blinky, inky, pinky, clyde, redportalbullets, blueportalbullets, redportal, blueportal, deathanimations, play_button, back_button, high_scores_button, menupacman, menupowerpill, menuinky, menublinky, menupinky, menuclyde, timer, timer_started, clock_ticker, normalsiren, runningsiren):
    """Draw objects to the screen"""

    # If the game is active
    if stats.game_active:
        timeractive = True
        timer.tick(60)

        check_pacman_wall_collisions(player = player, walls = walls)
        check_pacman_point_collisions(ai_settings = ai_settings, screen = screen, walls = walls, player = player, points = points, pills = pills, fruits = fruits, stats = stats, sb = sb, maze = maze, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde, redportal = redportal, blueportal = blueportal)
        check_pacman_portal_collisions(ai_settings = ai_settings, screen = screen, player = player, redportal = redportal, blueportal = blueportal, inky = inky, pinky = pinky, blinky = blinky, clyde = clyde)
        check_pacman_ghost_collisions(ai_settings = ai_settings, screen = screen, stats = stats, sb = sb, walls = walls, points = points, pills = pills, deathanimations = deathanimations, player = player, blinky = blinky, inky = inky, pinky = pinky, clyde = clyde)

        generate_fruits(ai_settings = ai_settings, screen = screen, maze = maze, fruits = fruits)

        screen.fill(ai_settings.bg_color)
        walls.draw(screen)
        points.draw(screen)
        pills.draw(screen)
        fruits.update()
        fruits.draw(screen)
        deathanimations.update()
        deathanimations.draw(screen)


        redportalbullets.update(walls, redportal)
        for redportalbullet in redportalbullets.sprites():
            redportalbullet.draw_bullet()
    
        blueportalbullets.update(walls, blueportal)
        for blueportalbullet in blueportalbullets.sprites():
            blueportalbullet.draw_bullet()
            
        redportal.blitme()
        blueportal.blitme()
        player.update()
        player.blitme()
        blinky.update(maze = maze, screen = screen, player = player)
        blinky.blitme()
        inky.update(maze = maze, screen = screen, player = player)
        inky.blitme()
        pinky.update(maze=maze, screen=screen, player=player)
        pinky.blitme()
        clyde.update(maze=maze, screen=screen, player=player)
        clyde.blitme()
        sb.show_score()
        
    # if game has not been started yet:
    if not stats.game_active:

        if not stats.scores_visible:
            # Fill the background
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1200, 864))
            # Draw the buttons
            play_button.draw_button()
            high_scores_button.draw_button()
            # Set up the startup animation timer
            timeractive = True
            timer.tick(120)
            current_ticks = pygame.time.get_ticks()
            # if not current_ticks >= (clock_ticker + 1000):

            ghostsbanner = pygame.image.load("img/ghostsbanner.png")
            screen.blit(ghostsbanner, (405, 510))

            titletext = pygame.image.load("img/pacmantitletext.png")
            screen.blit(titletext, (200, 50))
            smallerfont = pygame.font.SysFont("Comic Sans MS", 14)
            authorstring = "John Shelton Edition"
            authorstring_image = smallerfont.render(authorstring, True, (255, 255, 25), ai_settings.bg_color)
            authorstring_rect = authorstring_image.get_rect()
            screen_rect = screen.get_rect()
            authorstring_rect.centerx = screen_rect.centerx
            authorstring_rect.y = 700
            screen.blit(authorstring_image, authorstring_rect)

            menupacman.update()
            menupacman.blitme()
            menuinky.update()
            menuinky.blitme()
            menublinky.update()
            menublinky.blitme()
            menupinky.update()
            menupinky.blitme()
            menuclyde.update()
            menuclyde.blitme()
            if menupacman.turnedaround == False:
                menupowerpill.blitme()
           # else:
           #    clock_ticker += 100

        # if high scores menu is up
        if stats.scores_visible:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1200, 864))
            high_scores1 = HighScores(screen)
            high_scores1.show_score()
            back_button.draw_button()
        
    

    pygame.display.flip()

