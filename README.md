# Star Defenders

![Python](https://img.shields.io/badge/Language-Python-blue)
![Pygame](https://img.shields.io/badge/Engine-Pygame-green)
![OpenGL](https://img.shields.io/badge/Graphics-OpenGL-orange)
![NumPy](https://img.shields.io/badge/Math-NumPy-purple)
![Game](https://img.shields.io/badge/Type-2D%20Shooter-yellow)

> **Developed by Alan Cyril Sunny**  
> If you find this project helpful, please consider ⭐ [starring the repository](https://github.com/dragonpilee/star-defenders)!

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

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, or distribute it!

---

For more information, updates, and documentation, visit the  
👉 [GitHub Repository](https://github.com/dragonpilee/star-defenders)

Feel free to fork, star ⭐, and contribute!

---

## 🌟 Star Defenders — Defend the galaxy, one wave at a time!
