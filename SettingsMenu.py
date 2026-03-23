import pygame
from Button import Button
from Repositories.settings_repository import SettingsRepository

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    # Detectar cambio de resolución
    if not hasattr(runSettingsMenu, "last_size") or runSettingsMenu.last_size != (WIDTH, HEIGHT):
        runSettingsMenu.initialized = False
        runSettingsMenu.last_size = (WIDTH, HEIGHT)

    if not hasattr(runSettingsMenu, "initialized") or runSettingsMenu.initialized == False:
        runSettingsMenu.initialized = True

        is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        scale = 1 if is_fullscreen else 0.75

        # Fuentes
        title_size = int(HEIGHT * 0.08 * scale)
        button_size = int(HEIGHT * 0.035 * scale)

        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", title_size)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", button_size)


        spacing = int(90 * scale)

        start_y = center_y - spacing * 2

        slider_y = start_y
        diff_y = start_y + spacing
        fs_y = start_y + spacing * 2
        buttons_y = start_y + spacing * 3

        # Slider
        runSettingsMenu.slider_width = int(WIDTH * 0.35)
        runSettingsMenu.slider_x = center_x - runSettingsMenu.slider_width // 2
        runSettingsMenu.slider_y = slider_y

        # Botones
        btn_w = int(140 * scale)
        btn_h = int(50 * scale)

        runSettingsMenu.easy_rect = pygame.Rect(center_x - btn_w - 20, diff_y, btn_w, btn_h)
        runSettingsMenu.hard_rect = pygame.Rect(center_x + 20, diff_y, btn_w, btn_h)

        runSettingsMenu.fs_on_rect = pygame.Rect(center_x - btn_w - 20, fs_y, btn_w, btn_h)
        runSettingsMenu.fs_off_rect = pygame.Rect(center_x + 20, fs_y, btn_w, btn_h)

        runSettingsMenu.saveButton = Button("Guardar", btn_w, btn_h,
                                            (center_x - btn_w - 10, buttons_y),
                                            runSettingsMenu.button_font)

        runSettingsMenu.backButton = Button("Atras", btn_w, btn_h,
                                            (center_x + 10, buttons_y),
                                            runSettingsMenu.button_font)

        # Panel
        panel_width = int(WIDTH * (0.45 if is_fullscreen else 0.55))
        panel_height = int(spacing * 5)
        runSettingsMenu.panel_size = (panel_width, panel_height)

        runSettingsMenu.action = None

        # Configuración
        data = repo.get_settings("game_settings")
        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
            runSettingsMenu.fullscreen = data["data"].get("fullscreen", False)
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"
            runSettingsMenu.fullscreen = False

    mouse_pos = pygame.mouse.get_pos()
    screen.blit(bg, (0, 0))

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Panel centrado correcto
    panel = pygame.Surface(runSettingsMenu.panel_size)
    panel.set_alpha(120)
    panel.fill((10, 10, 30))
    screen.blit(panel, panel.get_rect(center=(center_x, center_y)))

    font = runSettingsMenu.button_font

    # Título
    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title, title.get_rect(center=(center_x, center_y - runSettingsMenu.panel_size[1]//2 + 40)))

    # Slider
    pygame.draw.rect(screen, (100,100,120),
                     (runSettingsMenu.slider_x, runSettingsMenu.slider_y,
                      runSettingsMenu.slider_width, 10), border_radius=5)

    progress = (runSettingsMenu.volume / 100) * runSettingsMenu.slider_width

    pygame.draw.rect(screen, (0,255,200),
                     (runSettingsMenu.slider_x, runSettingsMenu.slider_y,
                      progress, 10), border_radius=5)

    handle_x = runSettingsMenu.slider_x + progress
    pygame.draw.circle(screen, (200,255,255),
                       (int(handle_x), runSettingsMenu.slider_y + 5), 8)

    # Texto volumen
    screen.blit(font.render(f"Volumen: {runSettingsMenu.volume}", True, (255,255,255)),
                (runSettingsMenu.slider_x, runSettingsMenu.slider_y - 25))

    # Dificultad
    screen.blit(font.render("Dificultad:", True, (255,255,255)),
                (runSettingsMenu.slider_x, runSettingsMenu.easy_rect.y))

    easy_color = (0,200,100) if runSettingsMenu.difficulty=="Easy" else (80,80,80)
    hard_color = (200,50,50) if runSettingsMenu.difficulty=="Hard" else (80,80,80)

    pygame.draw.rect(screen, easy_color, runSettingsMenu.easy_rect, border_radius=10)
    pygame.draw.rect(screen, hard_color, runSettingsMenu.hard_rect, border_radius=10)

    screen.blit(font.render("Easy", True, (255,255,255)), runSettingsMenu.easy_rect.move(25,10))
    screen.blit(font.render("Hard", True, (255,255,255)), runSettingsMenu.hard_rect.move(25,10))

    # Fullscreen
    screen.blit(font.render("Pantalla:", True, (255,255,255)),
                (runSettingsMenu.slider_x, runSettingsMenu.fs_on_rect.y))

    on_color = (0,200,100) if runSettingsMenu.fullscreen else (80,80,80)
    off_color = (200,50,50) if not runSettingsMenu.fullscreen else (80,80,80)

    pygame.draw.rect(screen, on_color, runSettingsMenu.fs_on_rect, border_radius=10)
    pygame.draw.rect(screen, off_color, runSettingsMenu.fs_off_rect, border_radius=10)

    screen.blit(font.render("ON", True, (255,255,255)), runSettingsMenu.fs_on_rect.move(35,10))
    screen.blit(font.render("OFF", True, (255,255,255)), runSettingsMenu.fs_off_rect.move(30,10))

    # Botones
    runSettingsMenu.saveButton.update(mouse_pos)
    runSettingsMenu.backButton.update(mouse_pos)
    runSettingsMenu.saveButton.draw(screen)
    runSettingsMenu.backButton.draw(screen)

    # Eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if runSettingsMenu.slider_x <= mx <= runSettingsMenu.slider_x + runSettingsMenu.slider_width:
                porcentaje = (mx - runSettingsMenu.slider_x) / runSettingsMenu.slider_width
                runSettingsMenu.volume = int(porcentaje * 100)

            if runSettingsMenu.easy_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Easy"

            if runSettingsMenu.hard_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Hard"

            if runSettingsMenu.fs_on_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = True

            if runSettingsMenu.fs_off_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = False

        if runSettingsMenu.saveButton.handle_event(event):
            runSettingsMenu.action = "save"

        if runSettingsMenu.backButton.handle_event(event):
            runSettingsMenu.action = "back"

    # Guardar
    if runSettingsMenu.action == "save" and runSettingsMenu.saveButton.is_ready():
        repo.save_settings("game_settings", runSettingsMenu.volume, runSettingsMenu.difficulty, runSettingsMenu.fullscreen)

        if runSettingsMenu.fullscreen:
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((800,600))

        bg = pygame.transform.scale(bg, screen.get_size())
        runSettingsMenu.initialized = False
        runSettingsMenu.action = None
        return 2, screen, bg

    if runSettingsMenu.action == "back" and runSettingsMenu.backButton.is_ready():
        runSettingsMenu.action = None
        return 1

    pygame.display.flip()
    return 2