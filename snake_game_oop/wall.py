"""
wall.py - Wall / Boundary Class
Draws the game boundary and checks wall collisions.
Supports both wall-death mode and wrap-around mode.
"""

import turtle


class Wall:
    """
    Represents the game boundary walls.

    Attributes:
        width (int): Width of the game area.
        height (int): Height of the game area.
        wrap_mode (bool): If True, snake wraps around; if False, wall kills snake.
    """

    def __init__(self, width=560, height=560, wrap_mode=False):
        self.width = width
        self.height = height
        self.wrap_mode = wrap_mode
        self.half_w = width // 2
        self.half_h = height // 2

        self._drawer = turtle.Turtle()
        self._draw()

    def _draw(self):
        """Draw the boundary walls."""
        self._drawer.speed(0)
        self._drawer.color("#00FF41")  # Matrix green border
        self._drawer.pensize(3)
        self._drawer.penup()
        self._drawer.goto(-self.half_w, -self.half_h)
        self._drawer.pendown()
        self._drawer.hideturtle()

        for _ in range(4):
            self._drawer.forward(self.width if _ % 2 == 0 else self.height)
            self._drawer.left(90)

        # Draw corner accents
        self._draw_corners()

    def _draw_corners(self):
        """Draw small corner accent squares."""
        corners = [
            (-self.half_w, -self.half_h),
            (self.half_w, -self.half_h),
            (self.half_w, self.half_h),
            (-self.half_w, self.half_h),
        ]
        self._drawer.penup()
        self._drawer.color("#00FF41")
        self._drawer.pensize(5)
        for cx, cy in corners:
            self._drawer.goto(cx, cy)
            self._drawer.pendown()
            self._drawer.forward(0)  # Draw dot at corner
            self._drawer.penup()

    def check_collision(self, x, y):
        """
        Check if position (x, y) is outside the boundary.
        Returns True if collision detected (wall-death mode).
        Returns False if wrap mode handles it.
        """
        if self.wrap_mode:
            return False  # No collision in wrap mode
        return (
            x > self.half_w - 10 or
            x < -self.half_w + 10 or
            y > self.half_h - 10 or
            y < -self.half_h + 10
        )

    def wrap_position(self, x, y):
        """
        If snake goes out of bounds in wrap mode, return wrapped position.
        Returns (new_x, new_y).
        """
        new_x, new_y = x, y
        if x > self.half_w - 10:
            new_x = -self.half_w + 20
        elif x < -self.half_w + 10:
            new_x = self.half_w - 20
        if y > self.half_h - 10:
            new_y = -self.half_h + 20
        elif y < -self.half_h + 10:
            new_y = self.half_h - 20
        return (new_x, new_y)

    def is_inside(self, x, y):
        """Return True if (x, y) is within the boundary."""
        return (
            -self.half_w + 10 <= x <= self.half_w - 10 and
            -self.half_h + 10 <= y <= self.half_h - 10
        )

    def toggle_wrap_mode(self):
        """Toggle between wall-death and wrap-around mode."""
        self.wrap_mode = not self.wrap_mode
        return self.wrap_mode

    def __str__(self):
        return f"Wall(size={self.width}x{self.height}, wrap={self.wrap_mode})"
