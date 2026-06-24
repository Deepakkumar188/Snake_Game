"""
food.py - Food Classes
Handles regular food and special bonus food with different point values.
Uses OOP inheritance: BonusFood extends Food.
"""

import turtle
import random
import time


class Food:
    """
    Regular Food item for the snake to eat.

    Attributes:
        _food (turtle.Turtle): The turtle object representing food.
        points (int): Points awarded when eaten.
        color (str): Display color.
    """

    BOUNDARY = 270  # Grid boundary for random placement
    GRID_SIZE = 20  # Snap to grid

    def __init__(self):
        self.points = 10
        self.color = "#FF0000"  # Red
        self._food = turtle.Turtle()
        self._setup()
        self.refresh()

    def _setup(self):
        """Configure the food turtle."""
        self._food.speed(0)
        self._food.shape("circle")
        self._food.color(self.color)
        self._food.penup()
        self._food.shapesize(stretch_wid=0.8, stretch_len=0.8)

    def refresh(self):
        """Move food to a new random grid-aligned position."""
        x = random.randint(-13, 13) * self.GRID_SIZE
        y = random.randint(-13, 13) * self.GRID_SIZE
        self._food.goto(x, y)

    def get_position(self):
        """Return (x, y) position of the food."""
        return (self._food.xcor(), self._food.ycor())

    def hide(self):
        """Hide the food (used when resetting)."""
        self._food.goto(1000, 1000)

    def show(self):
        """Show the food at its current position."""
        self._food.showturtle()

    def distance_to(self, other_turtle):
        """Return distance from food to another turtle."""
        return self._food.distance(other_turtle)

    def __str__(self):
        return f"Food(points={self.points}, pos={self.get_position()})"


class BonusFood(Food):
    """
    Special Bonus Food — appears temporarily and awards extra points.
    Inherits from Food and overrides appearance and behavior.

    Attributes:
        duration (int): How many seconds the bonus food stays visible.
        spawn_time (float): Timestamp when it was spawned.
        is_active (bool): Whether bonus food is currently on screen.
    """

    def __init__(self):
        self.points = 50
        self.color = "#FFD700"  # Gold
        self.duration = 5  # seconds
        self.spawn_time = None
        self.is_active = False
        self._food = turtle.Turtle()
        self._setup()
        self._food.goto(1000, 1000)  # Start hidden

    def _setup(self):
        """Configure the bonus food turtle — star shaped & glowing gold."""
        self._food.speed(0)
        self._food.shape("circle")
        self._food.color(self.color)
        self._food.penup()
        self._food.shapesize(stretch_wid=1.2, stretch_len=1.2)

    def spawn(self):
        """Show the bonus food at a random location and record spawn time."""
        self.refresh()
        self.spawn_time = time.time()
        self.is_active = True

    def check_expired(self):
        """Return True if the bonus food has been on screen too long."""
        if self.is_active and self.spawn_time:
            return (time.time() - self.spawn_time) >= self.duration
        return False

    def deactivate(self):
        """Remove the bonus food from screen."""
        self._food.goto(1000, 1000)
        self.is_active = False
        self.spawn_time = None

    def __str__(self):
        return f"BonusFood(points={self.points}, active={self.is_active})"


class PoisonFood(Food):
    """
    Poison Food — causes the snake to shrink if eaten.
    Inherits from Food with negative points and different color.
    """

    def __init__(self):
        self.points = -20
        self.color = "#9B59B6"  # Purple
        self.is_active = False
        self._food = turtle.Turtle()
        self._setup()
        self._food.goto(1000, 1000)  # Start hidden

    def _setup(self):
        """Configure poison food with an X shape (square with red-X style)."""
        self._food.speed(0)
        self._food.shape("square")
        self._food.color(self.color)
        self._food.penup()
        self._food.shapesize(stretch_wid=0.7, stretch_len=0.7)

    def activate(self):
        """Show poison food at a random location."""
        self.refresh()
        self.is_active = True

    def deactivate(self):
        """Hide poison food."""
        self._food.goto(1000, 1000)
        self.is_active = False

    def __str__(self):
        return f"PoisonFood(points={self.points}, active={self.is_active})"
