import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import asyncio
import platform

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720  # 720p resolution
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Star Defenders")
clock = pygame.time.Clock()
FPS = 60

# Font for text rendering
font = pygame.font.SysFont("arial", 48)

# Game states
STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_WIN = 3
game_state = STATE_START

# Player properties
player_pos = np.array([WIDTH / 2, 60], dtype=float)
player_speed = 6.0
player_size = (48, 48)
player_alive = True
lives = 3

# Bullet properties
bullets = []  # List of [x, y, is_player_bullet]
bullet_speed = 15.0
bullet_size = (12, 24)
bullet_cooldown = 0.2
last_shot = 0

# Enemy properties
enemy_rows, enemy_cols = 4, 8
enemy_size = (48, 48)
enemy_speed = 3.0
enemy_direction = 1
enemies = []
wave = 1

# Score and high score
score = 0
high_score = 0

# Starfield properties
stars = []  # List of [x, y, size, speed]
for _ in range(50):
    x = np.random.uniform(0, WIDTH)
    y = np.random.uniform(0, HEIGHT)
    size = np.random.uniform(2, 6)
    speed = np.random.uniform(0.5, 2.0)
    stars.append([x, y, size, speed])

# Diving enemy logic
dive_interval = 2.0
last_dive = 0
enemy_shoot_interval = 1.0
last_enemy_shot = 0

# Sound effects
def create_shoot_sound():
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound_data = (np.sin(440 * 2 * np.pi * t) * 32767).astype(np.int16)
    sound_data = np.column_stack((sound_data, sound_data))  # Stereo
    return pygame.sndarray.make_sound(sound_data)

def create_hit_sound():
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound_data = (np.random.normal(0, 0.5, int(sample_rate * duration)) * 32767).astype(np.int16)
    sound_data = np.column_stack((sound_data, sound_data))  # Stereo
    return pygame.sndarray.make_sound(sound_data)

def create_game_over_sound():
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = np.linspace(440, 220, int(sample_rate * duration))
    sound_data = (np.sin(freq * 2 * np.pi * t) * 32767).astype(np.int16)
    sound_data = np.column_stack((sound_data, sound_data))  # Stereo
    return pygame.sndarray.make_sound(sound_data)

shoot_sound = create_shoot_sound()
hit_sound = create_hit_sound()
game_over_sound = create_game_over_sound()

def reset_game():
    global player_pos, player_alive, bullets, enemies, last_shot, last_dive, last_enemy_shot, enemy_direction, game_state, score, lives, enemy_speed, wave
    player_pos = np.array([WIDTH / 2, 60], dtype=float)
    player_alive = True
    lives = 3
    bullets = []
    enemies = []
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = 150 + col * 60
            y = HEIGHT - 150 - row * 60
            enemies.append([x, y, False])
    last_shot = 0
    last_dive = 0
    last_enemy_shot = 0
    enemy_direction = 1
    score = 0
    enemy_speed = 3.0
    wave = 1
    game_state = STATE_PLAYING

def spawn_new_wave():
    global enemies, enemy_speed, wave
    enemies = []
    enemy_speed *= 1.1  # Increase speed by 10% per wave
    wave += 1
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = 150 + col * 60
            y = HEIGHT - 150 - row * 60
            enemies.append([x, y, False])

def init_opengl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)

def draw_quad(x, y, w, h, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def draw_sprite(x, y, w, h, main_color, accent_color):
    draw_quad(x, y, w, h, main_color)
    accent_size = w * 0.4
    draw_quad(x + w * 0.3, y + h * 0.3, accent_size, accent_size, accent_color)

def draw_text(text, x, y, color=(1, 1, 1)):
    text_surface = font.render(text, True, (int(color[0]*255), int(color[1]*255), int(color[2]*255)))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    w, h = text_surface.get_size()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glColor3f(*color)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x, y + h)
    glEnd()
    
    glDeleteTextures([texture_id])
    return w, h

def update_game(dt):
    global player_pos, bullets, enemies, last_shot, last_dive, last_enemy_shot, enemy_direction, player_alive, game_state, score, high_score, lives

    if game_state != STATE_PLAYING:
        return

    if not player_alive:
        lives -= 1
        if lives > 0:
            player_alive = True
            player_pos = np.array([WIDTH / 2, 60], dtype=float)
        else:
            game_over_sound.play()
            game_state = STATE_GAME_OVER
            if score > high_score:
                high_score = score
        return

    if not enemies:
        spawn_new_wave()
        return

    # Update starfield
    for star in stars:
        star[1] -= star[3] * dt  # Move stars down
        if star[1] < 0:
            star[1] += HEIGHT  # Wrap to top
            star[0] = np.random.uniform(0, WIDTH)  # Random x-position

    # Handle input (WASD for movement, left mouse for shooting)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size[0]:
        player_pos[0] += player_speed
    if keys[pygame.K_w] and player_pos[1] < HEIGHT - player_size[1]:
        player_pos[1] += player_speed
    if keys[pygame.K_s] and player_pos[1] > 0:
        player_pos[1] -= player_speed

    mouse_buttons = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks() / 1000.0
    if mouse_buttons[0] and (current_time - last_shot) > bullet_cooldown:
        bullets.append([player_pos[0] + player_size[0] / 2 - bullet_size[0] / 2, player_pos[1] + player_size[1], True])
        shoot_sound.play()
        last_shot = current_time

    # Update bullets
    for bullet in bullets[:]:
        if bullet[2]:
            bullet[1] += bullet_speed
            if bullet[1] > HEIGHT:
                bullets.remove(bullet)
        else:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

    # Update enemies
    max_x = max(enemy[0] for enemy in enemies if not enemy[2]) if enemies else 0
    min_x = min(enemy[0] for enemy in enemies if not enemy[2]) if enemies else 0
    if max_x > WIDTH - enemy_size[0] or min_x < 0:
        enemy_direction *= -1
        for enemy in enemies:
            if not enemy[2]:
                enemy[1] -= 30
    for enemy in enemies:
        if not enemy[2]:
            enemy[0] += enemy_speed * enemy_direction
        else:
            enemy[1] -= 6.0
            if enemy[1] < 0:
                enemy[2] = False
                enemy[0] = 150 + (enemies.index(enemy) % enemy_cols) * 60
                enemy[1] = HEIGHT - 150 - (enemies.index(enemy) // enemy_cols) * 60

    # Trigger enemy dive
    if current_time - last_dive > dive_interval:
        for enemy in enemies:
            if not enemy[2] and np.random.random() < 0.1:
                enemy[2] = True
        last_dive = current_time

    # Enemy shooting
    if current_time - last_enemy_shot > enemy_shoot_interval:
        for enemy in enemies:
            if np.random.random() < 0.05:
                bullets.append([enemy[0] + enemy_size[0] / 2 - bullet_size[0] / 2, enemy[1], False])
                shoot_sound.play()
        last_enemy_shot = current_time

    # Collision detection (bullet vs enemy)
    for bullet in bullets[:]:
        if bullet[2]:
            for enemy in enemies[:]:
                if (abs(bullet[0] - enemy[0]) < enemy_size[0] and
                    abs(bullet[1] - enemy[1]) < enemy_size[1]):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 100
                    hit_sound.play()
                    break
        else:
            if (abs(bullet[0] - player_pos[0]) < player_size[0] and
                abs(bullet[1] - player_pos[1]) < player_size[1]):
                player_alive = False
                bullets.remove(bullet)

    # Collision detection (enemy vs player)
    for enemy in enemies:
        if (abs(enemy[0] - player_pos[0]) < player_size[0] and
            abs(enemy[1] - player_pos[1]) < player_size[1]):
            player_alive = False
            break

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw starfield
    for star in stars:
        draw_quad(star[0], star[1], star[2], star[2], (1, 1, 1))

    if game_state == STATE_START:
        text = "Press ENTER to Start"
        w, _ = draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2, (1, 1, 0))
        text = f"High Score: {high_score}"
        draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 - 120, (1, 1, 1))
    elif game_state == STATE_PLAYING:
        if player_alive:
            draw_sprite(player_pos[0], player_pos[1], player_size[0], player_size[1], (0, 1, 0), (1, 1, 1))
        for bullet in bullets:
            color = (1, 1, 1) if bullet[2] else (1, 0.5, 0)
            draw_quad(bullet[0], bullet[1], bullet_size[0], bullet_size[1], color)
        for enemy in enemies:
            draw_sprite(enemy[0], enemy[1], enemy_size[0], enemy_size[1], (1, 0, 0), (1, 1, 0))
        text = f"Score: {score}"
        draw_text(text, 30, HEIGHT - 90, (1, 1, 1))
        text = f"Lives: {lives}"
        draw_text(text, 30, HEIGHT - 150, (1, 1, 1))
        text = f"Wave: {wave}"
        draw_text(text, 30, HEIGHT - 210, (1, 1, 1))
    elif game_state == STATE_GAME_OVER:
        text = "Game Over"
        w, _ = draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 + 60, (1, 0, 0))
        text = "Press R to Restart"
        draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 - 60, (1, 1, 0))
        text = f"High Score: {high_score}"
        draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 - 180, (1, 1, 1))
    elif game_state == STATE_WIN:
        text = "You Win!"
        w, _ = draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 + 60, (0, 1, 0))
        text = "Press R to Restart"
        draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 - 60, (1, 1, 0))
        text = f"High Score: {high_score}"
        draw_text(text, WIDTH/2 - font.size(text)[0]/2, HEIGHT/2 - 180, (1, 1, 1))
    
    pygame.display.flip()

async def main():
    init_opengl()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == STATE_START and event.key == pygame.K_RETURN:
                    reset_game()
                elif (game_state == STATE_GAME_OVER or game_state == STATE_WIN) and event.key == pygame.K_r:
                    reset_game()
        
        dt = clock.tick(FPS) / 1000.0
        update_game(dt)
        render()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())