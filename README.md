# 🐍 Advanced Snake Game — OOPs Edition

A fully **Object-Oriented Python Snake Game** built using **Turtle Graphics**.
This project is designed to demonstrate core OOPs concepts in a fun, playable game.

---

## 📁 Project Structure

```
snake_game_oop/
│
├── main.py          # Entry point — run this to start the game
├── game.py          # Game controller (state machine, game loop)
├── snake.py         # Snake class (movement, growth, collision)
├── food.py          # Food, BonusFood, PoisonFood (inheritance)
├── scoreboard.py    # Scoreboard (score, lives, levels, file I/O)
├── wall.py          # Wall/Boundary class (wrap mode)
├── high_score.txt   # Auto-created — stores your best score
└── README.md        # This file
```

---

## 🎮 How to Run

```bash
# Make sure Python 3 is installed (turtle is built-in)
python main.py
```

No external libraries needed — uses only Python's built-in `turtle` module.

---

## 🕹️ Controls

| Key         | Action              |
|-------------|---------------------|
| ↑ ↓ ← → or WASD | Move the snake |
| `P`         | Pause / Resume      |
| `T`         | Toggle Wall Wrap Mode |
| `SPACE`     | Start / Restart     |
| `Q`         | Quit the game       |

---

## 🍎 Food Types

| Food     | Color  | Points | Effect                     |
|----------|--------|--------|----------------------------|
| Regular  | 🔴 Red | +10    | Snake grows by 1           |
| Bonus    | 🟡 Gold| +50    | Snake grows by 3 (5 sec only!) |
| Poison   | 🟣 Purple | -20 | Snake shrinks by 2 segments |

---

## 📈 Game Features

- **3 Lives** — You get 3 chances before Game Over
- **Leveling System** — Every 100 points = Level Up (faster speed!)
- **Persistent High Score** — Saved in `high_score.txt` between sessions
- **Bonus Food Timer** — Gold food disappears after 5 seconds
- **Wall Wrap Mode** — Press T to pass through walls instead of dying
- **Pause/Resume** — Press P any time during gameplay
- **Color-coded Snake** — Head is bright green, body fades

---

## 🧠 OOP Concepts Demonstrated

### 1. Classes & Objects
Every game element is a class:
```python
snake = Snake()
food = Food()
scoreboard = Scoreboard()
```

### 2. Inheritance
`BonusFood` and `PoisonFood` inherit from `Food`:
```python
class BonusFood(Food):     # Inherits Food, adds timer + spawn logic
class PoisonFood(Food):    # Inherits Food, adds shrink effect
```

### 3. Encapsulation
Private attributes (prefixed with `_`) are only modified via public methods:
```python
self._food = turtle.Turtle()   # Private
self.refresh()                 # Public interface
```

### 4. Abstraction
The Game class hides complexity — you just call `game.run()`:
```python
game = Game()
game.run()  # Entire game logic is abstracted away
```

### 5. Polymorphism
Each food subclass overrides `_setup()` to render differently:
```python
class Food:       → red circle
class BonusFood:  → large gold circle
class PoisonFood: → purple square
```

### 6. File I/O
High score is saved and loaded automatically:
```python
def _load_high_score(self):
    with open(self.HIGH_SCORE_FILE, "r") as f:
        return int(f.read().strip())
```

### 7. State Machine
The game uses a state pattern (MENU → PLAYING → PAUSED → GAME_OVER):
```python
self.state = Game.PLAYING
self.state = Game.GAME_OVER
```

---

## 🏗️ Class Diagram

```
Game (Controller)
├── Snake
│   ├── segments: list[Turtle]
│   ├── move()
│   ├── grow()
│   └── check_self_collision()
│
├── Food (Base Class)
│   ├── BonusFood (Subclass)
│   └── PoisonFood (Subclass)
│
├── Scoreboard
│   ├── score, lives, level
│   ├── add_points()
│   └── _load/_save_high_score()
│
└── Wall
    ├── check_collision()
    └── wrap_position()
```

---

## 👨‍💻 Requirements

- Python 3.x
- No external packages needed (uses built-in `turtle`)

---

## 📊 Scoring

| Action             | Points  |
|--------------------|---------|
| Eat regular food   | +10     |
| Eat bonus food     | +50     |
| Eat poison food    | -20     |
| Level up threshold | 100 pts |
