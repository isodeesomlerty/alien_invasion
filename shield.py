import pygame

class Shield:
    """A class to manage the shield."""

    def __init__(self, ai_game):
        """Create a shield object above the ship's current position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.color = self.settings.shield_color
        self.width = self.settings.shield_width
        self.height = self.settings.shield_height
        self.health = self.settings.shield_health
        self.ship = ai_game.ship
        self.sb = ai_game.sb
        self.sound_effects = ai_game.sound_effects

        # Initialize the shield's availability and active status.
        self.shield_available = True
        self.shield_active = False

        # Create a shield rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.set_position()
        self._destroy()

    
    def _check_edges(self):
        """Move the shield to within the screen boundaries."""
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.screen_rect.right:
            self.rect.right = self.screen_rect.right


    def set_position(self):
        """Set the shield's position to be above the ship's position."""
        self.rect.centerx = self.ship.rect.centerx
        self.rect.bottom = self.ship.rect.top - 50
        self._check_edges()


    def hit(self):
        """Decrement the health of the shield and check if it's destroyed."""
        self.health -= 1

        if self.health <= 0:
            self.sound_effects.play_shield_explosion_sound()
            self.shield_active = False
            self._destroy()


    def _destroy(self):
        """Destroy the shield."""
        self.rect.right = -10


    def reset_shield(self):
        """Reset the shield's health and availability."""
        self._destroy()
        self.health = self.settings.shield_health
        self.shield_available = True


    def deploy_shield(self):
        """Deploy the shield."""
        if self.shield_available:
            self.shield_active = True
            self.shield_available = False
            self.set_position()


    def draw_availability_status(self):
        """Draw the shield's availability status to the screen."""
        self.availability_image = self.sb.font.render("SHIELD AVAILABLE", 
                                                      True,
                                                      self.sb.text_color,
                                                      self.settings.bg_color)
        self.availability_rect = self.availability_image.get_rect()
        self.availability_rect.top = self.sb.score_rect.top
        self.availability_rect.right = self.sb.high_score_rect.left - 250
        self.screen.blit(self.availability_image,
                         self.availability_rect)


    def draw(self):
        """Draw the shield to the screen."""
        if self.shield_active:
            pygame.draw.rect(self.screen, self.color, self.rect)