import pygame
from pygame.sprite import Sprite
import spritesheet
import time
from warnings import warn
"""Credit for Astar algorithm implementation and related Node class goes to Nicholas Swift's online tutorial. spoiler alert: it doesn't work right even when i mess around with it a ton"""

# Credit for this: Nicholas Swift
# as found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement=False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 2
    #max_iterations = max_iterations ** 2
    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))


    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])



            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[1]][node_position[0]] == "X":
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)



class Blinky(Sprite):

    def __init__(self, ai_settings, screen, maze, player, ghosts):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0
        self.chasingcounter = 0
        self.scattercounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 15
        self.y = 15

        # The Sprite for Pacman
        self.blinky_sprite = spritesheet.spritesheet("img/blinky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")
        self.eyes_sprite = spritesheet.spritesheet("img/eyesghost.png")

        self.images = self.blinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.eyes_images = self.eyes_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.mode = "chasing"

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 1

        # The coordinates on the grid for pacman
        self.x = 13
        self.y = 10

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)


    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self, screen, maze, player):
        """Update Pacman's position and image"""

        # Test if in intersection, then recompute self.x and self.y
        self.xbuffer = self.rect.x % 32
        self.ybuffer = self.rect.y % 32

        # If ghost loses itself and goes out of bounds, reset its position
        if self.rect.x > 26 * 32 or self.rect.x < 0 or self.rect.y > 26 * 32 or self.rect.y < 0:
            self.rect.x = self.x * 32 + 4
            self.rect.y = self.y * 32 + 4

        if self.ybuffer >= 2 and self.ybuffer <= 6 and self.xbuffer >= 2 and self.xbuffer <= 6:
            self.x = int(self.rect.x / 32)
            self.y = int(self.rect.y / 32)


        if self.xbuffer > 6 and self.ybuffer > 6:
            self.rect.x = self.x * 32 + 4
            self.rect.y = self.y * 32 + 4




        self.up = (self.x, self.y - 1)
        self.down = (self.x, self.y + 1)
        self.left = (self.x - 1, self.y)
        self.right = (self.x + 1, self.y)

        self.start = (self.x, self.y)
        if self.mode == "chasing":
            self.end = (player.x, player.y)
        if self.mode == "returning":
            self.end = (13, 13)
        if self.mode == "running" or self.mode == "scatter":
            self.end = (1, 1)

        # Debugging print statements
        # print("start = " + str(self.start))
        # print("end = " + str(self.end))
        # Find the path
        path = astar(maze, self.start, self.end)

        # Draw path on screen for debugging purposes
        # for node in path:
        #    circle = pygame.draw.circle(screen, (255, 0, 0), (node[0] * 32 + 16, node[1] * 32 + 16), 16)
        
        # print(path)
        if path != None:
            if len(path) > 1:
                if path[1] == self.up:
                    self.movingUp = True
                    self.movingDown = False
                    self.movingLeft = False
                    self.movingRight = False
                if path[1] == self.down:
                    self.movingUp = False
                    self.movingDown = True
                    self.movingLeft = False
                    self.movingRight = False
                if path[1] == self.left:
                    self.movingUp = False
                    self.movingDown = False
                    self.movingLeft = True
                    self.movingRight = False
                if path[1] == self.right:
                    self.movingUp = False
                    self.movingDown = False
                    self.movingLeft = False
                    self.movingRight = True
            else:
                self.movingUp = False
                self.movingDown = False
                self.movingLeft = False
                self.movingRight = False

        # Animation and movement
        self.framecounter += 1
        if self.framecounter > self.framelimit:
            self.framecounter = 0
            if self.image_index < 1:
                self.image_index += 1
            else:
                self.image_index = 0

        if self.mode == "chasing" or self.mode == "scatter":
            if self.mode == "chasing":
                self.chasingcounter += 1
            if self.mode == "scatter":
                self.scattercounter += 1

            if self.chasingcounter >= 1000:
                self.mode = "scatter"
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4
                self.chasingcounter = 0
            if self.scattercounter >= 200:
                self.mode = "chasing"
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4
                self.scattercounter = 0

            self.image = self.images[self.image_index]
            if self.movingLeft:
                self.image = self.images[self.image_index]
                self.rect.x -= 1
            if self.movingRight:
                self.rect.x += 1
                self.image = self.images[self.image_index + 2]
            if self.movingUp:
                self.rect.y -= 1
                self.image = self.images[self.image_index + 4]
            if self.movingDown:
                self.rect.y += 1
                self.image = self.images[self.image_index + 6]
                
        if self.mode == "running":
            self.runningcounter += 1
            self.image = self.blue_images[self.image_index]
            if self.movingLeft:
                self.image = self.blue_images[self.image_index]
                self.rect.x -= 1
            if self.movingRight:
                self.rect.x += 1
                self.image = self.blue_images[self.image_index + 2]
            if self.movingUp:
                self.rect.y -= 1
                self.image = self.blue_images[self.image_index + 4]
            if self.movingDown:
                self.rect.y += 1
                self.image = self.blue_images[self.image_index + 6]
            if self.runningcounter > 750:
                self.runningcounter = 0
                self.mode = "chasing"
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sound/normalsiren.mp3")
                pygame.mixer.music.play(-1)
        
        if self.mode == "returning":
            self.runningcounter += 1
            self.image = self.eyes_images[self.image_index]
            if self.movingLeft:
                self.image = self.eyes_images[self.image_index]
                self.rect.x -= 1
            if self.movingRight:
                self.rect.x += 1
                self.image = self.eyes_images[self.image_index + 2]
            if self.movingUp:
                self.rect.y -= 1
                self.image = self.eyes_images[self.image_index + 4]
            if self.movingDown:
                self.rect.y += 1
                self.image = self.eyes_images[self.image_index + 6]
            #if self.runningcounter > 1000:
            #    self.runningcounter = 0
            #    self.mode = "chasing"
            if self.x == 13 and self.y == 13:
                self.mode = "chasing"
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)


class Inky(Sprite):

    def __init__(self, ai_settings, screen, maze, player, ghosts):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0
        self.chasingcounter = 0
        self.scattercounter = 0
        self.startupcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 15
        self.y = 15

        # The Sprite for Pacman
        self.blinky_sprite = spritesheet.spritesheet("img/inky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")
        self.eyes_sprite = spritesheet.spritesheet("img/eyesghost.png")

        self.images = self.blinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.eyes_images = self.eyes_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.mode = "chasing"

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 1

        # The coordinates on the grid for pacman
        self.x = 11
        self.y = 13

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self, screen, maze, player):
        """Update Pacman's position and image"""
        self.startupcounter += 1

        if self.startupcounter > 300:
            # Test if in intersection, then recompute self.x and self.y
            self.xbuffer = self.rect.x % 32
            self.ybuffer = self.rect.y % 32

            # If ghost loses itself and goes out of bounds, reset its position
            if self.rect.x > 26 * 32 or self.rect.x < 0 or self.rect.y > 26 * 32 or self.rect.y < 0:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            if self.ybuffer >= 2 and self.ybuffer <= 6 and self.xbuffer >= 2 and self.xbuffer <= 6:
                self.x = int(self.rect.x / 32)
                self.y = int(self.rect.y / 32)

            if self.xbuffer > 6 and self.ybuffer > 6:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            self.up = (self.x, self.y - 1)
            self.down = (self.x, self.y + 1)
            self.left = (self.x - 1, self.y)
            self.right = (self.x + 1, self.y)




            # slightly less garbage Pathfinding
            self.start = (self.x, self.y)
            if self.mode == "chasing":
                self.end = (player.x, player.y)
            if self.mode == "returning":
                self.end = (13, 13)
            if self.mode == "running" or self.mode == "scatter":
                self.end = (1, 25)


            # Debugging print statements
            #  print("start = " + str(self.start))
            # print("end = " + str(self.end))
            # Find the path
            path = astar(maze, self.start, self.end)

            # Draw path on screen for debugging purposes
            #for node in path:
            #    circle = pygame.draw.circle(screen, (255, 0, 0), (node[0] * 32 + 16, node[1] * 32 + 16), 16)

            # print(path)
            if path != None:
                if len(path) > 1:
                    if path[1] == self.up:
                        self.movingUp = True
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.down:
                        self.movingUp = False
                        self.movingDown = True
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.left:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = True
                        self.movingRight = False
                    if path[1] == self.right:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = True
                else:
                    self.movingUp = False
                    self.movingDown = False
                    self.movingLeft = False
                    self.movingRight = False

            # Animation and movement
            self.framecounter += 1
            if self.framecounter > self.framelimit:
                self.framecounter = 0
                if self.image_index < 1:
                    self.image_index += 1
                else:
                    self.image_index = 0

            if self.mode == "chasing" or self.mode == "scatter":
                if self.mode == "chasing":
                    self.chasingcounter += 1
                if self.mode == "scatter":
                    self.scattercounter += 1

                if self.chasingcounter >= 1000:
                    self.mode = "scatter"
                    self.chasingcounter = 0
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                if self.scattercounter >= 200:
                    self.mode = "chasing"
                    self.scattercounter = 0
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                self.image = self.images[self.image_index]
                if self.movingLeft:
                    self.image = self.images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.images[self.image_index + 6]

            if self.mode == "running":
                self.runningcounter += 1
                self.image = self.blue_images[self.image_index]
                if self.movingLeft:
                    self.image = self.blue_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.blue_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.blue_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.blue_images[self.image_index + 6]
                if self.runningcounter > 750:
                    self.runningcounter = 0
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sound/normalsiren.mp3")
                    pygame.mixer.music.play(-1)

            if self.mode == "returning":
                self.runningcounter += 1
                self.image = self.eyes_images[self.image_index]
                if self.movingLeft:
                    self.image = self.eyes_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.eyes_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.eyes_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.eyes_images[self.image_index + 6]
                #if self.runningcounter > 1000:
                #    self.runningcounter = 0
                #    self.mode = "chasing"
                if self.x == 13 and self.y == 13:
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4

    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)

class Pinky(Sprite):

    def __init__(self, ai_settings, screen, maze, player, ghosts):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0
        self.chasingcounter = 0
        self.scattercounter = 0
        self.startupcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 15
        self.y = 15

        # The Sprite for Pacman
        self.pinky_sprite = spritesheet.spritesheet("img/pinky.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")
        self.eyes_sprite = spritesheet.spritesheet("img/eyesghost.png")

        self.images = self.pinky_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.eyes_images = self.eyes_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.mode = "chasing"

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 1

        # The coordinates on the grid for pacman
        self.x = 13
        self.y = 13

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self, screen, maze, player):
        """Update Pacman's position and image"""
        self.startupcounter += 1
        if self.startupcounter > 500:
            # Test if in intersection, then recompute self.x and self.y
            self.xbuffer = self.rect.x % 32
            self.ybuffer = self.rect.y % 32

            # If ghost loses itself and goes out of bounds, reset its position
            if self.rect.x > 26 * 32 or self.rect.x < 0 or self.rect.y > 26 * 32 or self.rect.y < 0:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            if self.ybuffer >= 2 and self.ybuffer <= 6 and self.xbuffer >= 2 and self.xbuffer <= 6:
                self.x = int(self.rect.x / 32)
                self.y = int(self.rect.y / 32)

            if self.xbuffer > 6 and self.ybuffer > 6:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            self.up = (self.x, self.y - 1)
            self.down = (self.x, self.y + 1)
            self.left = (self.x - 1, self.y)
            self.right = (self.x + 1, self.y)

            # slightly less garbage Pathfinding
            self.start = (self.x, self.y)
            if self.mode == "chasing":
                self.end = (player.x, player.y)
                if player.movingRight:
                    self.end = (player.x + 4, player.y)
                if player.movingLeft:
                    self.end = (player.x - 4, player.y)
                if player.movingUp:
                   self.end = (player.x, player.y - 4)
                if player.movingDown:
                    self.end = (player.x, player.y + 4)


            if self.mode == "returning":
                self.end = (13, 13)
            if self.mode == "running" or self.mode == "scatter":
                self.end = (25, 1)

            # Debugging print statements
            #  print("start = " + str(self.start))
            # print("end = " + str(self.end))
            # Find the path
            path = astar(maze, self.start, self.end)

            # Draw path on screen for debugging purposes
            #for node in path:
            #    circle = pygame.draw.circle(screen, (255, 0, 0), (node[0] * 32 + 16, node[1] * 32 + 16), 16)

            # print(path)
            if path != None:
                if len(path) > 1:
                    if path[1] == self.up:
                        self.movingUp = True
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.down:
                        self.movingUp = False
                        self.movingDown = True
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.left:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = True
                        self.movingRight = False
                    if path[1] == self.right:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = True
                else:
                    self.movingUp = False
                    self.movingDown = False
                    self.movingLeft = False
                    self.movingRight = False

            # Animation and movement
            self.framecounter += 1
            if self.framecounter > self.framelimit:
                self.framecounter = 0
                if self.image_index < 1:
                    self.image_index += 1
                else:
                    self.image_index = 0

            if self.mode == "chasing" or self.mode == "scatter":
                if self.mode == "chasing":
                    self.chasingcounter += 1
                if self.mode == "scatter":
                    self.scattercounter += 1

                if self.chasingcounter >= 1000:
                    self.mode = "scatter"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    self.chasingcounter = 0
                if self.scattercounter >= 200:
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    self.scattercounter = 0

                self.image = self.images[self.image_index]
                if self.movingLeft:
                    self.image = self.images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.images[self.image_index + 6]

            if self.mode == "running":
                self.runningcounter += 1
                self.image = self.blue_images[self.image_index]
                if self.movingLeft:
                    self.image = self.blue_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.blue_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.blue_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.blue_images[self.image_index + 6]
                if self.runningcounter > 750:
                    self.runningcounter = 0
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sound/normalsiren.mp3")
                    pygame.mixer.music.play(-1)

            if self.mode == "returning":
                self.runningcounter += 1
                self.image = self.eyes_images[self.image_index]
                if self.movingLeft:
                    self.image = self.eyes_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.eyes_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.eyes_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.eyes_images[self.image_index + 6]
               # if self.runningcounter > 1000:
               #     self.runningcounter = 0
               #     self.mode = "chasing"
                if self.x == 13 and self.y == 13:
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4

    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)

class Clyde(Sprite):

    def __init__(self, ai_settings, screen, maze, player, ghosts):

        # Movement Flags
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.runningcounter = 0
        self.chasingcounter = 0
        self.scattercounter = 0
        self.startupcounter = 0

        self.screen = screen

        # The coordinates within the screen for pacman
        self.x = 15
        self.y = 15

        # The Sprite for Pacman
        self.clyde_sprite = spritesheet.spritesheet("img/clyde.png")
        self.blue_sprite = spritesheet.spritesheet("img/blueghost.png")
        self.eyes_sprite = spritesheet.spritesheet("img/eyesghost.png")

        self.images = self.clyde_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.blue_images = self.blue_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.eyes_images = self.eyes_sprite.images_at(
            [(0, 0, 24, 24), (0, 24, 24, 24), (0, 48, 24, 24), (0, 72, 24, 24), (0, 96, 24, 24), (0, 120, 24, 24),
             (0, 144, 24, 24), (0, 168, 24, 24)], colorkey=(0, 0, 0))

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # ai mode options are "chasing", "running", and "returning"
        self.mode = "chasing"

        # Initialize frame counter
        self.framecounter = 0
        self.image_index = 0
        self.framelimit = 1

        # The coordinates on the grid for pacman
        self.x = 15
        self.y = 13

        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

        self.screen_rect = screen.get_rect()
        self.center = (self.rect.centerx, self.rect.centery)

    def reset_position(self):
        self.rect.x = self.x * 32 + 4
        self.rect.y = self.y * 32 + 4

    def update(self, screen, maze, player):
        """Update Pacman's position and image"""
        self.startupcounter += 1
        if self.startupcounter > 800:
            # Test if in intersection, then recompute self.x and self.y
            self.xbuffer = self.rect.x % 32
            self.ybuffer = self.rect.y % 32

            # If ghost loses itself and goes out of bounds, reset its position
            if self.rect.x > 26 * 32 or self.rect.x < 0 or self.rect.y > 26 * 32 or self.rect.y < 0:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            if self.ybuffer >= 2 and self.ybuffer <= 6 and self.xbuffer >= 2 and self.xbuffer <= 6:
                self.x = int(self.rect.x / 32)
                self.y = int(self.rect.y / 32)

            if self.xbuffer > 6 and self.ybuffer > 6:
                self.rect.x = self.x * 32 + 4
                self.rect.y = self.y * 32 + 4

            self.up = (self.x, self.y - 1)
            self.down = (self.x, self.y + 1)
            self.left = (self.x - 1, self.y)
            self.right = (self.x + 1, self.y)

            # slightly less garbage Pathfinding
            self.start = (self.x, self.y)
            if self.mode == "chasing":

                dist = int(((abs(player.x - self.x) ** 2 + (abs(player.y - self.y)) ** 2) // 2))

                if dist > 8:
                    self.end = (player.x, player.y)
                else:
                    self.end = (25, 1)

            if self.mode == "returning":
                self.end = (13, 13)
            if self.mode == "running" or self.mode == "scatter":
                self.end = (25, 25)

            # Debugging print statements
            #  print("start = " + str(self.start))
            # print("end = " + str(self.end))
            # Find the path
            path = astar(maze, self.start, self.end)

            # Draw path on screen for debugging purposes
            #for node in path:
            #    circle = pygame.draw.circle(screen, (255, 0, 0), (node[0] * 32 + 16, node[1] * 32 + 16), 16)

            # print(path)
            if path != None:
                if len(path) > 1:
                    if path[1] == self.up:
                        self.movingUp = True
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.down:
                        self.movingUp = False
                        self.movingDown = True
                        self.movingLeft = False
                        self.movingRight = False
                    if path[1] == self.left:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = True
                        self.movingRight = False
                    if path[1] == self.right:
                        self.movingUp = False
                        self.movingDown = False
                        self.movingLeft = False
                        self.movingRight = True
                else:
                    self.movingUp = False
                    self.movingDown = False
                    self.movingLeft = False
                    self.movingRight = False

            # Animation and movement
            self.framecounter += 1
            if self.framecounter > self.framelimit:
                self.framecounter = 0
                if self.image_index < 1:
                    self.image_index += 1
                else:
                    self.image_index = 0

            if self.mode == "chasing" or self.mode == "scatter":
                if self.mode == "chasing":
                    self.chasingcounter += 1
                if self.mode == "scatter":
                    self.scattercounter += 1

                if self.chasingcounter >= 1000:
                    self.mode = "scatter"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    self.chasingcounter = 0
                if self.scattercounter >= 200:
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    self.scattercounter = 0

                self.image = self.images[self.image_index]
                if self.movingLeft:
                    self.image = self.images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.images[self.image_index + 6]

            if self.mode == "running":
                self.runningcounter += 1
                self.image = self.blue_images[self.image_index]
                if self.movingLeft:
                    self.image = self.blue_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.blue_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.blue_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.blue_images[self.image_index + 6]
                if self.runningcounter > 750:
                    self.runningcounter = 0
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sound/normalsiren.mp3")
                    pygame.mixer.music.play(-1)

            if self.mode == "returning":
                self.runningcounter += 1
                self.image = self.eyes_images[self.image_index]
                if self.movingLeft:
                    self.image = self.eyes_images[self.image_index]
                    self.rect.x -= 1
                if self.movingRight:
                    self.rect.x += 1
                    self.image = self.eyes_images[self.image_index + 2]
                if self.movingUp:
                    self.rect.y -= 1
                    self.image = self.eyes_images[self.image_index + 4]
                if self.movingDown:
                    self.rect.y += 1
                    self.image = self.eyes_images[self.image_index + 6]
                #if self.runningcounter > 1000:
                #    self.runningcounter = 0
                #    self.mode = "chasing"
                if self.x == 13 and self.y == 13:
                    self.mode = "chasing"
                    self.rect.x = self.x * 32 + 4
                    self.rect.y = self.y * 32 + 4

    def blitme(self):
        """Draw pacman at his current location"""
        self.screen.blit(self.image, self.rect)