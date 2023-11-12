from pygame import mixer

class SoundEffects:
    """A class to manage sound effects in the game."""

    def __init__(self):
        """Initialize all of the game's sound effects."""
        # Load and play the background music.
        self._play_background_music()

        # Load the sound effects.
        self.shooting_sound = mixer.Sound('sound/hand_phaser_weapon.wav')
        self.alien_explosion_sound = (mixer.Sound
                                      ('sound/sliding_door_truncated.wav'))
        self.ship_explosion_sound = mixer.Sound('sound/severe_crash.wav')
        self.shield_explosion_sound = mixer.Sound('sound/descending_crash.wav')

        # Set the volume for the background music and sound effects.
        mixer.music.set_volume(0.1)
        self.shooting_sound.set_volume(0.1)
        self.alien_explosion_sound.set_volume(0.1)
        self.shield_explosion_sound.set_volume(0.25)
        self.ship_explosion_sound.set_volume(0.5)


    def _play_background_music(self):
        """Play the background music."""
        mixer.music.load('sound/raf_atmosphere.wav')
        mixer.music.set_volume(3)
        mixer.music.play(-1)


    def play_shooting_sound(self):
        """Play the shooting sound."""
        self.shooting_sound.play()

    
    def play_alien_explosion_sound(self):
        """Play the alien explosion sound."""
        self.alien_explosion_sound.play()


    def play_ship_explosion_sound(self):
        """Play the ship explosion sound."""
        self.ship_explosion_sound.play()


    def play_shield_explosion_sound(self):
        """Play the shield explosion sound."""
        self.shield_explosion_sound.play()   