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

        # Fuentes
        title_size = int(HEIGHT * 0.08)
        button_size = int(HEIGHT * 0.04)
        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", title_size)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", button_size)

        # Tamaños de botones del menú principal (centrados)
        menu_button_width = int(WIDTH * 0.15)
        menu_button_height = int(HEIGHT * 0.08)
        spacing = int(WIDTH * 0.02)
        center_x = WIDTH // 2

        runSettingsMenu.menu_buttons = [
            Button("Día", menu_button_width, menu_button_height, (center_x - (menu_button_width*2 + spacing*1), int(HEIGHT*0.3)), runSettingsMenu.button_font),
            Button("Hora", menu_button_width, menu_button_height, (center_x - (menu_button_width + spacing//2), int(HEIGHT*0.3)), runSettingsMenu.button_font),
            Button("Configuración", menu_button_width, menu_button_height, (center_x + spacing//2, int(HEIGHT*0.3)), runSettingsMenu.button_font),
            Button("Otro", menu_button_width, menu_button_height, (center_x + menu_button_width + spacing, int(HEIGHT*0.3)), runSettingsMenu.button_font),
        ]

        # Botones de opciones
        button_width = int(WIDTH * 0.15)
        button_height = int(HEIGHT * 0.07)
        runSettingsMenu.saveButton = Button("Guardar", button_width, button_height, (center_x - button_width - spacing//2, int(HEIGHT*0.85)), runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", button_width, button_height, (center_x + spacing//2, int(HEIGHT*0.85)), runSettingsMenu.button_font)

        # Slider
        runSettingsMenu.slider_x = int(WIDTH * 0.45)
        runSettingsMenu.slider_y = int(HEIGHT * 0.4)
        runSettingsMenu.slider_width = int(WIDTH * 0.25)

        # Botones de dificultad
        runSettingsMenu.easy_rect = pygame.Rect(int(WIDTH * 0.45), int(HEIGHT * 0.5), int(WIDTH * 0.12), int(HEIGHT * 0.07))
        runSettingsMenu.hard_rect = pygame.Rect(int(WIDTH * 0.6), int(HEIGHT * 0.5), int(WIDTH * 0.12), int(HEIGHT * 0.07))

        # Botones de fullscreen
        runSettingsMenu.fs_on_rect = pygame.Rect(int(WIDTH * 0.45), int(HEIGHT * 0.65), int(WIDTH * 0.12), int(HEIGHT * 0.07))
        runSettingsMenu.fs_off_rect = pygame.Rect(int(WIDTH * 0.6), int(HEIGHT * 0.65), int(WIDTH * 0.12), int(HEIGHT * 0.07))

        runSettingsMenu.action = None

        # Cargar configuración
        data = repo.get_settings("game_settings")
        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
            runSettingsMenu.fullscreen = data["data"].get("fullscreen", False)
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"
            runSettingsMenu.fullscreen = False
        runSettingsMenu.original_volume = runSettingsMenu.volume
        runSettingsMenu.original_difficulty = runSettingsMenu.difficulty
        runSettingsMenu.original_fullscreen = runSettingsMenu.fullscreen

    mouse_pos = pygame.mouse.get_pos()

    # Dibujo de fondo
    screen.blit(bg, (0, 0))

    # Panel transparente de opciones (más pequeño en Full Screen y ventana)
    panel_width = int(WIDTH * 0.55)
    panel_height = int(HEIGHT * 0.55)
    panel = pygame.Surface((panel_width, panel_height))
    panel.set_alpha(120)
    panel.fill((10, 10, 30))
    screen.blit(panel, panel.get_rect(center=(WIDTH//2, HEIGHT//2)))

    font = runSettingsMenu.button_font

    # Título
    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title, title.get_rect(center=(WIDTH//2, int(HEIGHT*0.15))))

    # Botones del menú principal
    for btn in runSettingsMenu.menu_buttons:
        btn.update(mouse_pos)
        btn.draw(screen)

    # Botones de opciones
    runSettingsMenu.saveButton.update(mouse_pos)
    runSettingsMenu.backButton.update(mouse_pos)
    runSettingsMenu.saveButton.draw(screen)
    runSettingsMenu.backButton.draw(screen)

    # Slider
    pygame.draw.rect(screen, (100,100,120), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, runSettingsMenu.slider_width, 10), border_radius=5)
    progress = (runSettingsMenu.volume / 100) * runSettingsMenu.slider_width
    pygame.draw.rect(screen, (0,255,200), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, progress, 10), border_radius=5)
    handle_x = runSettingsMenu.slider_x + progress
    pygame.draw.circle(screen, (200,255,255), (int(handle_x), runSettingsMenu.slider_y + 5), 8)
    vol_text = font.render(f"Volumen: {runSettingsMenu.volume}", True, (255,255,255))
    screen.blit(vol_text, (int(WIDTH*0.2), runSettingsMenu.slider_y - 20))

    # Dificultad
    diff_title = font.render("Dificultad:", True, (255,255,255))
    screen.blit(diff_title, (int(WIDTH*0.2), int(HEIGHT*0.5)))
    easy_color = (0,200,100) if runSettingsMenu.difficulty=="Easy" else (80,80,80)
    hard_color = (200,50,50) if runSettingsMenu.difficulty=="Hard" else (80,80,80)
    pygame.draw.rect(screen, easy_color, runSettingsMenu.easy_rect, border_radius=10)
    pygame.draw.rect(screen, hard_color, runSettingsMenu.hard_rect, border_radius=10)
    screen.blit(font.render("Easy", True, (255,255,255)), runSettingsMenu.easy_rect.move(20,10))
    screen.blit(font.render("Hard", True, (255,255,255)), runSettingsMenu.hard_rect.move(20,10))

    # Fullscreen
    fs_title = font.render("Pantalla:", True, (255,255,255))
    screen.blit(fs_title, (int(WIDTH*0.2), int(HEIGHT*0.65)))
    on_color = (0,200,100) if runSettingsMenu.fullscreen else (80,80,80)
    off_color = (200,50,50) if not runSettingsMenu.fullscreen else (80,80,80)
    pygame.draw.rect(screen, on_color, runSettingsMenu.fs_on_rect, border_radius=10)
    pygame.draw.rect(screen, off_color, runSettingsMenu.fs_off_rect, border_radius=10)
    screen.blit(font.render("ON", True, (255,255,255)), runSettingsMenu.fs_on_rect.move(30,10))
    screen.blit(font.render("OFF", True, (255,255,255)), runSettingsMenu.fs_off_rect.move(25,10))

    # Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Slider
            if runSettingsMenu.slider_x <= mx <= runSettingsMenu.slider_x + runSettingsMenu.slider_width and runSettingsMenu.slider_y - 10 <= my <= runSettingsMenu.slider_y + 20:
                porcentaje = (mx - runSettingsMenu.slider_x) / runSettingsMenu.slider_width
                runSettingsMenu.volume = int(porcentaje * 100)
            # Dificultad
            if runSettingsMenu.easy_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Easy"
            if runSettingsMenu.hard_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Hard"
            # Fullscreen
            if runSettingsMenu.fs_on_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = True
            if runSettingsMenu.fs_off_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = False

        if runSettingsMenu.saveButton.handle_event(event):
            runSettingsMenu.action = "save"
        if runSettingsMenu.backButton.handle_event(event):
            runSettingsMenu.action = "back"
        for btn in runSettingsMenu.menu_buttons:
            if btn.handle_event(event):
                runSettingsMenu.action = btn.text.lower()  # si quieres guardar cuál menú se presionó

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

    # Volver
    if runSettingsMenu.action == "back" and runSettingsMenu.backButton.is_ready():
        runSettingsMenu.action = None
        return 1

    pygame.display.flip()
    return 2