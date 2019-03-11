class Settings():
    """Class to code settings"""
    def __init__(self):
        """initialize settings"""
        self.screen_width = 1200
        self.screen_height = 864
        self.bg_color = (0, 0, 0)

        #set the number of lives
        self.number_lives = 3
        
        self.ghosts_eaten = 0

        #Set power point size
        self.power_point_size = 3
        self.power_pill_size = 15
        self.power_point_color = (255, 255, 255)

    