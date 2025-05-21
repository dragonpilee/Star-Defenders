
# Star Defenders

**Star Defenders** is a retro-style 2D space shooter built using **Python**, **Pygame**, and **OpenGL**. Inspired by the arcade classic Galaxian, this game adds modern enhancements like procedural starfields, stereo sound effects, and smooth animations—all in crisp 720p.

---

## 🚀 Features

- 🔫 Player ship with WASD movement and mouse-based shooting
- 👾 Multiple enemy waves with increasing difficulty
- 🌌 Dynamic starfield background
- 💥 Procedural sound effects using NumPy
- 🎯 Bullet collisions and enemy dive-bomb behavior
- 🎮 Game states: Start, Playing, Game Over, and Win
- 📈 Score, wave, and life tracking
- 🖥️ OpenGL-accelerated rendering

---

## 🛠 Requirements

- Python 3.7+
- `pygame`
- `PyOpenGL`
- `numpy`

Install dependencies using pip:

```bash
pip install pygame PyOpenGL numpy
```

---

## 🕹 Controls

| Action         | Key/Mouse          |
|----------------|--------------------|
| Move Left      | A                  |
| Move Right     | D                  |
| Move Up        | W                  |
| Move Down      | S                  |
| Shoot Bullet   | Left Mouse Button  |
| Start Game     | ENTER              |
| Restart        | R (after Game Over or Win) |
| Quit Game      | ESC / Close Window |

---

## 📸 Screenshots

*(Add your own screenshots here if you'd like!)*

---

## 📦 How to Run

```bash
python star_defenders.py
```

> Rename your script to `star_defenders.py` for consistency, or adjust this line accordingly.

---

## 🧠 How It Works

The game loop is asynchronous using `asyncio`, which works with both desktop and WebAssembly (Emscripten) environments. Graphics are rendered using OpenGL with 2D orthographic projection. Sound effects are generated dynamically using NumPy arrays.

---

## ❤️ Credits

- Created by **Alan Cyril Sunny**
- Inspired by classic arcade space shooters
- Uses free & open-source Python libraries

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, or distribute it!

---

## 🌟 Star Defenders — Defend the galaxy, one wave at a time!
