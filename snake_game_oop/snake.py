"""
snake.py - Snake Class
Handles all snake-related logic: body segments, movement, direction, growth.
"""

import turtle


class Snake:
    """
    Represents the Snake in the game.

    Attributes:
        segments (list): List of turtle segments forming the snake body.
        head (turtle.Turtle): The head of the snake.
        direction (str): Current direction of movement.
        speed (int): Movement step size.
        colors (list): Colors for head and body gradient.
    """

    SEGMENT_SIZE = 20
    MOVE_DISTANCE = 20

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def __init__(self):
        self.segments = []
        self.direction = self.RIGHT
        self.speed = self.MOVE_DISTANCE
        self.colors = ["#00FF41", "#00CC33", "#009922"]  # Matrix green gradient
        self._create_snake()

    def _create_snake(self):
        """Initialize the snake with 3 starting segments."""
        starting_positions = [(0, 0), (-20, 0), (-40, 0)]
        for i, pos in enumerate(starting_positions):
            self._add_segment(pos, i)

        self.head = self.segments[0]
        self.head.shape("square")

    def _add_segment(self, position, index=None):
        """Add a new segment to the snake body."""
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.penup()
        segment.goto(position)

        # Color: head is bright green, body fades
        if index == 0:
            segment.color("#00FF41")  # Head: bright green
            segment.shapesize(stretch_wid=1.1, stretch_len=1.1)
        else:
            color_idx = min(index, len(self.colors) - 1)
            segment.color(self.colors[color_idx])
            segment.shapesize(stretch_wid=0.9, stretch_len=0.9)

        self.segments.append(segment)

    def grow(self):
        """Add a new segment at the tail of the snake."""
        tail_pos = self.segments[-1].pos()
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(self.colors[-1])
        new_segment.shapesize(stretch_wid=0.9, stretch_len=0.9)
        new_segment.penup()
        new_segment.goto(tail_pos)
        self.segments.append(new_segment)

    def move(self):
        """Move all segments: body follows head, head moves in current direction."""
        # Move body segments backward
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        # Move head in current direction
        if self.direction == self.UP:
            self.head.sety(self.head.ycor() + self.speed)
        elif self.direction == self.DOWN:
            self.head.sety(self.head.ycor() - self.speed)
        elif self.direction == self.LEFT:
            self.head.setx(self.head.xcor() - self.speed)
        elif self.direction == self.RIGHT:
            self.head.setx(self.head.xcor() + self.speed)

    def go_up(self):
        """Change direction to UP (prevents reversing)."""
        if self.direction != self.DOWN:
            self.direction = self.UP

    def go_down(self):
        """Change direction to DOWN (prevents reversing)."""
        if self.direction != self.UP:
            self.direction = self.DOWN

    def go_left(self):
        """Change direction to LEFT (prevents reversing)."""
        if self.direction != self.RIGHT:
            self.direction = self.LEFT

    def go_right(self):
        """Change direction to RIGHT (prevents reversing)."""
        if self.direction != self.LEFT:
            self.direction = self.RIGHT

    def reset(self):
        """Remove all segments and reset the snake."""
        for seg in self.segments:
            seg.goto(1000, 1000)  # Move off-screen
            seg.hideturtle()
        self.segments.clear()
        self.direction = self.RIGHT
        self._create_snake()

    def get_head_position(self):
        """Return the current (x, y) position of the snake head."""
        return (self.head.xcor(), self.head.ycor())

    def check_self_collision(self):
        """Return True if the head collides with any body segment."""
        for segment in self.segments[1:]:
            if self.head.distance(segment) < 15:
                return True
        return False

    def increase_speed(self):
        """Increase snake movement speed slightly."""
        pass  # Speed is managed by game loop delay in main

    @property
    def length(self):
        """Return the number of segments."""
        return len(self.segments)
