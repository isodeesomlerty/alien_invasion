class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initilize the game's static settings."""
        # Screen settings
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.5
        # How quickly the alien point values increase
        self.score_scale = 1.5

    
    def initialize_dynamic_settings(self, difficulty_level=''):
        """
        Initialize settings that change throughout the game.
        The starting speed of the alien and the ship
         depends on the selected difficulty level.
        """
        self.difficulty_level = difficulty_level
        
        self.bullet_speed = 2.5
        
        if difficulty_level == 'easy':
            self.ship_speed = 2
            self.alien_speed = 0.75
        elif difficulty_level == 'hard':
            self.ship_speed = 1.5
            self.alien_speed = 1.25
        else:
            self.ship_speed = 1.5
            self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings.
        self.alien_points = 50

    
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)