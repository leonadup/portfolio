import pygame
import sys
import os
import math
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Watch out")

clock = pygame.time.Clock()
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "fonts", "Cinzel-VariableFont_wght.ttf")

pygame.mixer.music.load(os.path.join(BASE_DIR, "music", "Serge Quadrado - Scary Forest.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

scene1 = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "images", "image_chemin_foret.bmp")),
    (WIDTH, HEIGHT)
)
scene2 = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "images", "image_foret_chemin.bmp")),
    (WIDTH, HEIGHT)
)
scene3 = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "images", "image_haunted_house.bmp")),
    (WIDTH, HEIGHT)
)

monster = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "images", "pixel_horror_face.png")).convert_alpha(),
    (WIDTH, HEIGHT)
)

ghost_image_orig = pygame.image.load(
    os.path.join(BASE_DIR, "images", "ghost.png")
).convert_alpha()
ghost_image_orig = pygame.transform.scale(ghost_image_orig, (50, 50))
ghost_image_orig.set_alpha(50)

apparition_image_orig = pygame.image.load(
    os.path.join(BASE_DIR, "images", "apparition_horror_pixel.png")
).convert_alpha()
apparition_image_orig = pygame.transform.scale(apparition_image_orig, (60, 60))
apparition_image_orig.set_alpha(128)
apparition_visible = False
apparition_timer = 0
APPARITION_INTERVAL = 3500

zones = [
    {"scene": scene1, "rect": pygame.Rect(370, 300, 80, 20), "next": scene2},
    {"scene": scene2, "rect": pygame.Rect(335, 410, 100, 50), "next": scene3},
    {"scene": scene2, "rect": pygame.Rect(250, 550, 200, 70), "next": scene1},
    {"scene": scene3, "rect": pygame.Rect(230, 558, 200, 70), "next": scene2},
    {"scene": scene3, "rect": pygame.Rect(488, 326, 20, 50), "next": None},
]

hidden_numbers = [
    {"scene": scene1, "pos": (116, 127), "digit": "6"},
    {"scene": scene2, "pos": (650, 390), "digit": "1"},
    {"scene": scene3, "pos": (132, 449), "digit": "4"},
]

darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
current_scene = scene1
timer_started = False
timer_start = 0
TIMER_LIMIT = 20000

ghosts = []
corners = [(0,0), (WIDTH-50,0), (0,HEIGHT-50), (WIDTH-50, HEIGHT-50)]
for i in range(8):
    start_corner = random.choice(corners)
    start_x, start_y = start_corner
    ghosts.append({
        "x": start_x,
        "y": start_y,
        "target": (370 + 40, 300 + 10),
        "appeared": False,
        "start_time": 2000 + i*2500,
        "arrived": False
    })

def show_intro():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(font_path, 26)
    text = (
        "Tu t'es aventuré trop loin dans la forêt.\n"
        "La nuit est tombée. Quelque chose rôde.\n\n"
        "Observe bien ton environnement.\n"
        "Un code te permettra peut-être de survivre."
    )
    y = 120
    for line in text.split("\n"):
        screen.blit(font.render(line, True, (220, 200, 150)), (60, y))
        y += 40
    small_font = pygame.font.Font(font_path, 20)
    screen.blit(
        small_font.render("Appuie sur une touche pour commencer", True, (160, 150, 110)),
        (60, y + 20)
    )
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                return

def show_victory():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    font = pygame.font.Font(font_path, 30)
    text = (
        "La porte s'ouvre lentement.\n\n"
        "À l'intérieur, la chaleur.\n\n"
        "Tu es enfin en sécurité.\n"
        "Repose-toi, brave aventurier."
    )
    y = 150
    for line in text.split("\n"):
        screen.blit(font.render(line, True, (200, 220, 180)), (80, y))
        y += 40
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def draw_timer():
    if not timer_started:
        return
    remaining = max(0, (TIMER_LIMIT - (pygame.time.get_ticks() - timer_start)) // 1000)
    font = pygame.font.Font(font_path, 20)
    screen.blit(font.render(f"{remaining}s", True, (200, 50, 50)), (WIDTH - 260, 20))

def check_timer():
    if timer_started and pygame.time.get_ticks() - timer_start >= TIMER_LIMIT:
        show_game_over()

def draw_hidden_numbers():
    font = pygame.font.Font(font_path, 18)
    mx, my = pygame.mouse.get_pos()
    for h in hidden_numbers:
        if h["scene"] == current_scene:
            if math.dist((mx, my), h["pos"]) < 80:
                screen.blit(font.render(h["digit"], True, (160, 150, 120)), h["pos"])

def show_game_over():
    font = pygame.font.Font(font_path, 36)
    alpha = 0
    while True:
        screen.fill((0, 0, 0))
        if alpha < 255:
            monster.set_alpha(alpha)
            screen.blit(monster, (0, 0))
            alpha += 3
        else:
            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.fill((random.randint(150,255), random.randint(0,80), random.randint(0,80)))
            flash.set_alpha(90)
            screen.blit(flash, (0, 0))
            text = random.choice(["TU AS PERDU", "TROP TARD", "IL ÉTAIT LÀ"])
            t = font.render(text, True, (255, 0, 0))
            screen.blit(t, (random.randint(50, WIDTH-400), random.randint(50, HEIGHT-50)))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def show_code_screen(correct="614"):
    global timer_started, timer_start
    font = pygame.font.Font(font_path, 28)
    if not timer_started:
        timer_started = True
        timer_start = pygame.time.get_ticks()
    entered = ""
    display = ["_", "_", "_"]
    cross_rect = pygame.Rect(WIDTH - 50, 20, 30, 30)
    while True:
        check_timer()
        screen.fill((0, 0, 0))
        screen.blit(font.render("X", True, (150,0,0)), (cross_rect.x+7, cross_rect.y))
        screen.blit(font.render("As tu bien observé ? Entre le code trouvé", True, (220, 200, 150)), (60, 180))
        screen.blit(font.render(" ".join(display), True, (255, 230, 150)), (60, 230))
        draw_timer()
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if cross_rect.collidepoint(e.pos):
                    return
            if e.type == pygame.KEYDOWN:
                if e.unicode.isdigit() and len(entered) < 3:
                    entered += e.unicode
                    display[len(entered)-1] = e.unicode
                elif e.key == pygame.K_BACKSPACE and entered:
                    display[len(entered)-1] = "_"
                    entered = entered[:-1]
                elif e.key == pygame.K_RETURN and len(entered) == 3:
                    if entered == correct:
                        show_victory()
                    else:
                        entered = ""
                        display = ["_", "_", "_"]

def update_ghosts():
    if current_scene != scene1:
        return
    current_time = pygame.time.get_ticks()
    for g in ghosts:
        if g["arrived"]:
            continue
        if not g["appeared"] and current_time >= g["start_time"]:
            g["appeared"] = True
        if g["appeared"]:
            x, y = g["x"], g["y"]
            tx, ty = g["target"]
            dx, dy = tx - x, ty - y
            dist = math.hypot(dx, dy)
            if dist > 1:
                step = 2
                g["x"] += dx/dist * step
                g["y"] += dy/dist * step
            else:
                g["arrived"] = True

def draw_ghosts():
    if current_scene != scene1:
        return
    for g in ghosts:
        if g["appeared"] and not g["arrived"]:
            screen.blit(ghost_image_orig, (g["x"] - 25, g["y"] - 25))

def update_apparition():
    global apparition_visible, apparition_timer
    if current_scene != scene2:
        return
    current_time = pygame.time.get_ticks()
    if current_time - apparition_timer >= APPARITION_INTERVAL:
        apparition_visible = not apparition_visible
        apparition_timer = current_time

def draw_apparition():
    if current_scene == scene2 and apparition_visible:
        for z in zones:
            if z["scene"] == scene2 and z["rect"].collidepoint(z["rect"].center):
                x, y = z["rect"].center
                screen.blit(apparition_image_orig, (x - 30, y - 30))

show_intro()

running = True
while running:
    check_timer()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            for z in zones:
                if z["scene"] == current_scene and z["rect"].collidepoint(e.pos):
                    if z["next"]:
                        current_scene = z["next"]
                    else:
                        show_code_screen()

    screen.blit(current_scene, (0, 0))
    draw_hidden_numbers()
    update_ghosts()
    draw_ghosts()
    update_apparition()
    draw_apparition()
    draw_timer()

    darkness.fill((0, 0, 0, 240))
    pygame.draw.circle(darkness, (0, 0, 0, 0), pygame.mouse.get_pos(), 80)
    screen.blit(darkness, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
