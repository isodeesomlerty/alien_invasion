import sys
from time import sleep

import pygame

from settings import Settings
from sound_effects import SoundEffects
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from ship_bullet import ShipBullet
from alien import Alien
from shield import Shield

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.sound_effects = SoundEffects()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.shield = Shield(self)
        self.ship_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state. 
        # Initialize the selecting_difficulty attribute to False as the player
        #  needs to click the Play button before selecting the difficulty level.
        self.game_active = False
        self.selecting_difficulty = False

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make the difficulty buttons.
        self.easy_button = Button(self, 'Easy', -2)
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, 'Hard', 2)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_ship_bullets()
                self._update_aliens()
                self._update_alien_bullets()
            
            self._update_screen()
            self.clock.tick(60)

    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_active and not self.selecting_difficulty:
                    self._check_play_button(mouse_pos)
                elif self.selecting_difficulty:
                    self._check_difficulty_button(mouse_pos)


    def _quit_game(self):
        """Exit the game."""
        self.stats.write_high_score()
        sys.exit()

    
    def _check_play_button(self, mouse_pos):
        """
        Check whether the player clicks on the Play button.
        Take the player to select the difficulty level once they have clicked
         on the Play button.
        """
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.game_active:
            self.selecting_difficulty = True


    def _check_difficulty_button(self, mouse_pos):
        """
        Check which difficulty level the player selects.
        Reset the selecting_difficulty attribute to False once a choice is made.
        """
        if self.selecting_difficulty:

            if self.easy_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings('easy')
                self._start_game()

            if self.medium_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings()
                self._start_game()

            if self.hard_button.rect.collidepoint(mouse_pos):
                self.settings.initialize_dynamic_settings('hard')
                self._start_game()
            
            self.selecting_difficulty = False


    def _start_game(self):
        """Start a new game if the game is currently inactive."""
        if not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_images()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.ship_bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_ship_bullet()
        elif event.key == pygame.K_s:
            if self.game_active:
                self.shield.deploy_shield()
        elif event.key == pygame.K_p:
            self._start_game()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _fire_ship_bullet(self):
        """Create a new bullet and add it the bullets group."""
        if len(self.ship_bullets) < self.settings.ship_bullets_allowed:
            new_ship_bullet = ShipBullet(self)
            self.ship_bullets.add(new_ship_bullet)
            self.sound_effects.play_shooting_sound()


    def _update_ship_bullets(self):
        """
        Update position of bullets from the ship.
        Get rid of old bullets.
        """
        # Update bullet positions.
        self.ship_bullets.update()

        # Get rid of bullets that have disappeared.
        for ship_bullet in self.ship_bullets.copy():
            if ship_bullet.rect.bottom <= 0:
                self.ship_bullets.remove(ship_bullet)

        self._check_bullet_alien_collisions()
        
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.ship_bullets, self.aliens,
                                                True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sound_effects.play_alien_explosion_sound()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.ship_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self._new_level()


    def _new_level(self):
        """Start a new level."""
        self.stats.level += 1
        self.sb.prep_level()
        self.shield.reset_shield()

    
    def _update_aliens(self):
        """Update the fleet of aliens."""
        self._check_fleet_edges()
        self.aliens.update()

        self._check_shield_alien_collisions()

        # Get the time passed since last call (frame).
        time_passed = self.clock.get_time() / 1000.0

        # Allow for the aliens to shoot.
        for alien in self.aliens.sprites():
            alien.shoot_cooldown -= time_passed
            alien.shoot()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _check_shield_alien_collisions(self):
        # Remove any bullets that have collided with the shield.
        # The shield is hit if an alien collides with it.
        collisions = pygame.sprite.spritecollide(self.shield, self.aliens, True)
        
        if collisions:
            for collision in collisions:
                self.shield.hit()
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sound_effects.play_alien_explosion_sound()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.ship_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self._new_level()


    def _update_alien_bullets(self):
        """Update position of bullets from the aliens."""
        # Update bullet positions.
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared.
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

        self._check_bullet_shield_collision()
        self._check_bullet_ship_collision()


    def _check_bullet_shield_collision(self):
        """Respond to bullet-shield collisions."""
        collisions = pygame.sprite.spritecollide(self.shield, 
                                                 self.alien_bullets, True)
        for collision in collisions:
            self.shield.hit()


    def _check_bullet_ship_collision(self):
        """Respond to bullet-ship collisions."""
        # Remove any bullets and ships that have collided.
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
        
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        self.sound_effects.play_ship_explosion_sound()

        # Reset the shield.
        self.shield.reset_shield()
        
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.ship_bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(2)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for ship_bullet in self.ship_bullets.sprites():
            ship_bullet.draw_bullet()
        self.ship.blitme()

        # Draw the shield if it's active.
        self.shield.draw()

        # Draw the shield availability status.
        if self.shield.shield_available:
            self.shield.draw_availability_status()

        self.aliens.draw(self.screen)
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        # Draw the score information.
        self.sb.show_score()


        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            if self.selecting_difficulty:
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()