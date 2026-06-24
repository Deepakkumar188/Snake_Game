"""
scoreboard.py - Scoreboard Class
Manages score display, high score tracking, lives, and level system.
Saves high score to a file so it persists between sessions.
"""

import turtle
import os


class Scoreboard:
    """
    Displays and manages the game scoreboard.

    Attributes:
        score (int): Current score.
        high_score (int): All-time high score (loaded from file).
        level (int): Current game level.
        lives (int): Remaining lives.
    """

    HIGH_SCORE_FILE = "high_score.txt"
    FONT_MAIN = ("Courier", 14, "bold")
    FONT_LARGE = ("Courier", 22, "bold")
    FONT_SMALL = ("Courier", 11, "normal")

    def __init__(self):
        self.score = 0
        self.level = 1
        self.lives = 3
        self.high_score = self._load_high_score()

        self._display = turtle.Turtle()
        self._display.speed(0)
        self._display.color("white")
        self._display.penup()
        self._display.hideturtle()
        self.update()

    def _load_high_score(self):
        """Load high score from file. Returns 0 if file doesn't exist."""
        if os.path.exists(self.HIGH_SCORE_FILE):
            try:
                with open(self.HIGH_SCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                return 0
        return 0

    def _save_high_score(self):
        """Save the current high score to file."""
        try:
            with open(self.HIGH_SCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except IOError:
            pass  # Fail silently if file write fails

    def update(self):
        """Redraw the scoreboard with current values."""
        self._display.clear()

        # Top bar
        self._display.goto(0, 290)
        self._display.write(
            f"Score: {self.score}   High Score: {self.high_score}   Level: {self.level}   Lives: {'❤ ' * self.lives}",
            align="center",
            font=self.FONT_MAIN
        )

    def add_points(self, points):
        """Add points to the score and check for level up."""
        self.score += points
        if self.score < 0:
            self.score = 0

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()

        # Level up every 100 points
        new_level = max(1, self.score // 100 + 1)
        leveled_up = new_level > self.level
        self.level = new_level

        self.update()
        return leveled_up

    def lose_life(self):
        """Decrease lives by 1. Returns True if no lives left."""
        self.lives -= 1
        self.update()
        return self.lives <= 0

    def reset(self):
        """Reset score and lives for a new game, keep high score."""
        self.score = 0
        self.level = 1
        self.lives = 3
        self.update()

    def show_game_over(self):
        """Display the Game Over message in the center."""
        self._display.goto(0, 50)
        self._display.write("GAME OVER", align="center", font=self.FONT_LARGE)
        self._display.goto(0, 10)
        self._display.write(f"Final Score: {self.score}", align="center", font=self.FONT_MAIN)
        self._display.goto(0, -30)
        self._display.write("Press SPACE to Play Again | Q to Quit", align="center", font=self.FONT_SMALL)

    def show_paused(self):
        """Display paused message."""
        self._display.goto(0, 10)
        self._display.write("⏸ PAUSED — Press P to Resume", align="center", font=self.FONT_MAIN)

    def show_level_up(self):
        """Briefly show level up notification."""
        self._display.goto(0, -20)
        self._display.color("#FFD700")
        self._display.write(f"🎉 LEVEL UP! Level {self.level}", align="center", font=self.FONT_MAIN)
        self._display.color("white")

    def clear_center(self):
        """Clear center messages and redraw scoreboard."""
        self._display.clear()
        self._display.color("white")
        self.update()

    def get_delay(self):
        """Return game loop delay based on level (faster at higher levels)."""
        base_delay = 0.12
        reduction = (self.level - 1) * 0.008
        return max(0.04, base_delay - reduction)

    def __str__(self):
        return f"Scoreboard(score={self.score}, level={self.level}, lives={self.lives})"
