"""
game.py - Game Controller Class
The main game engine. Manages game state, game loop, event handling,
and coordinates Snake, Food, Scoreboard, and Wall objects.
"""

import turtle
import time
import random
from snake import Snake
from food import Food, BonusFood, PoisonFood
from scoreboard import Scoreboard
from wall import Wall


class Game:
    """
    Main Game Controller using OOP design.

    States:
        MENU     → Waiting to start
        PLAYING  → Game in progress
        PAUSED   → Game paused
        GAME_OVER → Snake died, show score

    Attributes:
        screen (turtle.Screen): The game window.
        snake (Snake): The player's snake.
        food (Food): Regular food.
        bonus_food (BonusFood): Bonus gold food.
        poison_food (PoisonFood): Purple shrink food.
        scoreboard (Scoreboard): Score display.
        wall (Wall): Boundary/collision handler.
        state (str): Current game state.
    """

    # Game States
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"

    # Window settings
    WINDOW_TITLE = "🐍 Advanced Snake Game — OOP Python"
    BG_COLOR = "#000000"
    WINDOW_SIZE = 620

    # Gameplay settings
    BONUS_SPAWN_INTERVAL = 5   # Every N foods eaten, spawn bonus
    POISON_SPAWN_CHANCE = 0.25  # 25% chance after each food eaten

    def __init__(self):
        self.state = self.MENU
        self.foods_eaten = 0
        self._setup_screen()
        self._create_objects()
        self._bind_keys()
        self._show_menu()

    # ─── Setup ────────────────────────────────────────────────────────────────

    def _setup_screen(self):
        """Configure the game window."""
        self.screen = turtle.Screen()
        self.screen.title(self.WINDOW_TITLE)
        self.screen.bgcolor(self.BG_COLOR)
        self.screen.setup(width=self.WINDOW_SIZE, height=self.WINDOW_SIZE)
        self.screen.tracer(0)  # Turn off auto-refresh (manual control)

    def _create_objects(self):
        """Instantiate all game objects."""
        self.wall = Wall(width=560, height=560, wrap_mode=False)
        self.snake = Snake()
        self.food = Food()
        self.bonus_food = BonusFood()
        self.poison_food = PoisonFood()
        self.scoreboard = Scoreboard()

    def _bind_keys(self):
        """Register keyboard event listeners."""
        self.screen.listen()

        # Snake movement
        self.screen.onkey(self.snake.go_up, "Up")
        self.screen.onkey(self.snake.go_down, "Down")
        self.screen.onkey(self.snake.go_left, "Left")
        self.screen.onkey(self.snake.go_right, "Right")

        # WASD alternative controls
        self.screen.onkey(self.snake.go_up, "w")
        self.screen.onkey(self.snake.go_down, "s")
        self.screen.onkey(self.snake.go_left, "a")
        self.screen.onkey(self.snake.go_right, "d")

        # Game controls
        self.screen.onkey(self._toggle_pause, "p")
        self.screen.onkey(self._restart_game, "space")
        self.screen.onkey(self._quit_game, "q")
        self.screen.onkey(self._toggle_wrap, "t")

    # ─── Menu ─────────────────────────────────────────────────────────────────

    def _show_menu(self):
        """Display the start screen."""
        menu = turtle.Turtle()
        menu.speed(0)
        menu.color("#00FF41")
        menu.penup()
        menu.hideturtle()

        menu.goto(0, 120)
        menu.write("🐍 SNAKE GAME", align="center", font=("Courier", 26, "bold"))

        menu.color("white")
        menu.goto(0, 60)
        menu.write("Advanced OOP Edition", align="center", font=("Courier", 14, "normal"))

        menu.color("#FFD700")
        menu.goto(0, 10)
        menu.write("Controls:", align="center", font=("Courier", 12, "bold"))

        menu.color("white")
        controls = [
            "↑ ↓ ← → or W A S D : Move",
            "P : Pause / Resume",
            "T : Toggle Wall Wrap Mode",
            "SPACE : Restart  |  Q : Quit",
        ]
        for i, line in enumerate(controls):
            menu.goto(0, -20 - i * 22)
            menu.write(line, align="center", font=("Courier", 11, "normal"))

        menu.color("#FF4444")
        menu.goto(0, -120)
        menu.write("🍎 Red = +10pts  🌟 Gold = +50pts  💀 Purple = -20pts",
                   align="center", font=("Courier", 10, "normal"))

        menu.color("#00FF41")
        menu.goto(0, -160)
        menu.write("Press SPACE to Start!", align="center", font=("Courier", 14, "bold"))

        self.screen.update()
        self._menu_turtle = menu

    # ─── Game Loop ────────────────────────────────────────────────────────────

    def run(self):
        """Start the main game loop (waits for SPACE key to begin)."""
        # Wait for space to start
        self.screen.onkey(self._start_game, "space")
        turtle.mainloop()

    def _start_game(self):
        """Begin gameplay from menu or restart."""
        if self.state in (self.MENU, self.GAME_OVER):
            if hasattr(self, "_menu_turtle"):
                self._menu_turtle.clear()
            self.state = self.PLAYING
            self._game_loop()

    def _restart_game(self):
        """Full restart: reset all objects and restart loop."""
        if self.state == self.GAME_OVER:
            self.foods_eaten = 0
            self.snake.reset()
            self.food.refresh()
            self.bonus_food.deactivate()
            self.poison_food.deactivate()
            self.scoreboard.reset()
            self.scoreboard.clear_center()
            self.state = self.PLAYING
            self._game_loop()

    def _game_loop(self):
        """Core game loop — runs while state is PLAYING."""
        while self.state == self.PLAYING:
            self.screen.update()
            time.sleep(self.scoreboard.get_delay())

            self.snake.move()

            # Handle wrap or wall collision
            hx, hy = self.snake.get_head_position()
            if self.wall.wrap_mode:
                wx, wy = self.wall.wrap_position(hx, hy)
                if (wx, wy) != (hx, hy):
                    self.snake.head.goto(wx, wy)
            elif self.wall.check_collision(hx, hy):
                self._handle_death()
                break

            # Check self collision
            if self.snake.check_self_collision():
                self._handle_death()
                break

            # Check food eaten
            self._check_food_eaten()

            # Check bonus food
            self._check_bonus_food()

            # Check poison food
            self._check_poison_food()

    def _check_food_eaten(self):
        """Check if snake head touches regular food."""
        if self.food.distance_to(self.snake.head) < 15:
            self.food.refresh()
            self.snake.grow()
            self.foods_eaten += 1

            leveled_up = self.scoreboard.add_points(self.food.points)
            if leveled_up:
                self.scoreboard.show_level_up()
                time.sleep(0.5)
                self.scoreboard.clear_center()

            # Spawn bonus food periodically
            if self.foods_eaten % self.BONUS_SPAWN_INTERVAL == 0:
                self.bonus_food.spawn()

            # Randomly spawn poison food
            if random.random() < self.POISON_SPAWN_CHANCE and not self.poison_food.is_active:
                self.poison_food.activate()

    def _check_bonus_food(self):
        """Check bonus food expiry and collection."""
        if self.bonus_food.is_active:
            if self.bonus_food.check_expired():
                self.bonus_food.deactivate()
            elif self.bonus_food.distance_to(self.snake.head) < 15:
                self.bonus_food.deactivate()
                self.snake.grow()
                self.snake.grow()  # Extra growth for bonus
                leveled_up = self.scoreboard.add_points(self.bonus_food.points)
                if leveled_up:
                    self.scoreboard.show_level_up()
                    time.sleep(0.5)
                    self.scoreboard.clear_center()

    def _check_poison_food(self):
        """Check if snake eats poison food."""
        if self.poison_food.is_active:
            if self.poison_food.distance_to(self.snake.head) < 15:
                self.poison_food.deactivate()
                self.scoreboard.add_points(self.poison_food.points)

                # Shrink the snake (remove last 2 segments)
                for _ in range(min(2, len(self.snake.segments) - 3)):
                    seg = self.snake.segments.pop()
                    seg.goto(1000, 1000)
                    seg.hideturtle()

    def _handle_death(self):
        """Handle snake death — lose life or end game."""
        game_over = self.scoreboard.lose_life()
        if game_over:
            self.state = self.GAME_OVER
            self.scoreboard.show_game_over()
            self.screen.update()
            self.screen.onkey(self._restart_game, "space")
        else:
            # Still has lives — reset snake position only
            self.snake.reset()
            self.food.refresh()
            self.bonus_food.deactivate()
            self.poison_food.deactivate()
            time.sleep(0.5)
            self._game_loop()

    # ─── Controls ─────────────────────────────────────────────────────────────

    def _toggle_pause(self):
        """Toggle pause state."""
        if self.state == self.PLAYING:
            self.state = self.PAUSED
            self.scoreboard.show_paused()
            self.screen.update()
        elif self.state == self.PAUSED:
            self.state = self.PLAYING
            self.scoreboard.clear_center()
            self._game_loop()

    def _toggle_wrap(self):
        """Toggle wrap-around wall mode."""
        mode = self.wall.toggle_wrap_mode()
        # Brief on-screen notification via scoreboard
        self.scoreboard._display.goto(0, -10)
        mode_text = "WRAP ON" if mode else "WRAP OFF"
        self.scoreboard._display.write(
            f"Wall Mode: {mode_text}", align="center",
            font=("Courier", 12, "bold")
        )
        self.screen.update()
        time.sleep(0.8)
        self.scoreboard.clear_center()

    def _quit_game(self):
        """Exit the game cleanly."""
        self.state = self.GAME_OVER
        turtle.bye()

    def __str__(self):
        return f"Game(state={self.state}, foods_eaten={self.foods_eaten})"
