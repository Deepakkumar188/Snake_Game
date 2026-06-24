"""
main.py - Entry Point
Advanced Snake Game using Object-Oriented Programming (OOP)
Built with Python Turtle Graphics

Project Structure:
    main.py        → Entry point
    game.py        → Game controller (main engine)
    snake.py       → Snake class (movement, growth, collision)
    food.py        → Food, BonusFood, PoisonFood classes (inheritance)
    scoreboard.py  → Scoreboard class (score, lives, levels, file I/O)
    wall.py        → Wall class (boundary, wrap mode)

OOP Concepts Used:
    ✔ Classes & Objects
    ✔ Inheritance (BonusFood, PoisonFood extend Food)
    ✔ Encapsulation (private _attributes, public methods)
    ✔ Abstraction (game logic hidden inside classes)
    ✔ Polymorphism (each food type overrides _setup/refresh)
    ✔ File I/O (high score persisted in high_score.txt)
    ✔ State Machine (MENU → PLAYING → PAUSED → GAME_OVER)
"""

from game import Game


def main():
    """Launch the Advanced Snake Game."""
    print("=" * 50)
    print("  🐍 Advanced Snake Game — OOP Edition")
    print("=" * 50)
    print("Controls:")
    print("  Arrow Keys / WASD  → Move snake")
    print("  P                  → Pause / Resume")
    print("  T                  → Toggle wall wrap mode")
    print("  SPACE              → Start / Restart")
    print("  Q                  → Quit")
    print("=" * 50)
    print("Food Types:")
    print("  🔴 Red    → +10 points (regular)")
    print("  🟡 Gold   → +50 points (bonus, limited time!)")
    print("  🟣 Purple → -20 points + shrink (poison!)")
    print("=" * 50)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
