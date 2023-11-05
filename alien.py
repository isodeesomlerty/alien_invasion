from random import random

import pygame
from pygame.sprite import Sprite
import alien_color_converter as converter

from alien_bullet import AlienBullet

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Determine if the alien can shoot.
        #  The initial cooldown period after the alien is spawned is random.
        self.can_shoot = random() < self.settings.alien_shooter_probability
        self.shoot_cooldown = random() * self.settings.cooldown_period

        # Load the alien image and set its rect attribute.
        if self.can_shoot:
            converter.convert_alien_color('images/alien.bmp',
                                          'images/shooter_alien.bmp', 
                                          self.settings.alien_color,
                                          self.settings.alien_shooter_color,
                                          self.settings.color_tolerance)
            self.image = pygame.image.load('images/shooter_alien.bmp')
        else:
            self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


    def shoot(self):
        """Allow the alien to shoot if its cooldown has elapsed."""
        if self.can_shoot and self.shoot_cooldown <= 0:
            # Create a new bullet and add it to the alien bullets group.
            new_alien_bullet = AlienBullet(self.ai_game, self)
            self.ai_game.alien_bullets.add(new_alien_bullet)
            
            # Reset the cooldown period.
            self.shoot_cooldown = self.settings.cooldown_period