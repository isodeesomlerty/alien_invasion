from pathlib import Path
import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self._read_high_score()

    
    def _read_high_score(self, file_path='high_score.json'):
        """
        Read the high score from a file if it exists.
        Otherwise, initialize the high score to 0.
        """
        self.path = Path(file_path)

        if self.path.exists():
            contents = self.path.read_text()
            self.high_score = json.loads(contents)
        else:
            self.high_score = 0


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


    def write_high_score(self, file_path='high_score.json'):
        """Write the high score to a file."""
        self.path = Path(file_path)
        contents = json.dumps(self.high_score)
        self.path.write_text(contents)