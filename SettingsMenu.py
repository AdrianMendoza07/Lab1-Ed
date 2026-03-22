import pygame
from Button import Button
from Repositories.settings_repository import SettingsRepository

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    if not hasattr(runSettingsMenu, "initialized"):
        runSettingsMenu.initialized = True

        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        runSettingsMenu.saveButton = Button("Guardar", 200, 60, (WIDTH//2 - 110, HEIGHT - 100), runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", 200, 60, (WIDTH//2 + 110, HEIGHT - 100), runSettingsMenu.button_font)

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

        runSettingsMenu.slider_x = WIDTH//2 - 40
        runSettingsMenu.slider_y = HEIGHT//2 - 50
        runSettingsMenu.slider_width = 200
        runSettingsMenu.slider_height = 10

        # BOTONES DIFICULTAD
        runSettingsMenu.easy_rect = pygame.Rect(WIDTH//2 - 20, HEIGHT//2 + 20, 120, 50)
        runSettingsMenu.hard_rect = pygame.Rect(WIDTH//2 + 140, HEIGHT//2 + 20, 120, 50)

        # BOTONES FULLSCREEN
        runSettingsMenu.fs_on_rect = pygame.Rect(WIDTH//2 - 20, HEIGHT//2 + 100, 120, 50)
        runSettingsMenu.fs_off_rect = pygame.Rect(WIDTH//2 + 140, HEIGHT//2 + 100, 120, 50)

        runSettingsMenu.action = None

    backButton = runSettingsMenu.backButton
    saveButton = runSettingsMenu.saveButton

    slider_x = runSettingsMenu.slider_x
    slider_y = runSettingsMenu.slider_y
    slider_width = runSettingsMenu.slider_width

    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                runSettingsMenu.volume = min(100, runSettingsMenu.volume + 5)
            if event.key == pygame.K_DOWN:
                runSettingsMenu.volume = max(0, runSettingsMenu.volume - 5)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # SLIDER
            if slider_x <= mx <= slider_x + slider_width:
                porcentaje = (mx - slider_x) / slider_width
                runSettingsMenu.volume = int(porcentaje * 100)

            # DIFICULTAD
            if runSettingsMenu.easy_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Easy"

            if runSettingsMenu.hard_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Hard"

            # FULLSCREEN
            if runSettingsMenu.fs_on_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = True

            if runSettingsMenu.fs_off_rect.collidepoint(mx, my):
                runSettingsMenu.fullscreen = False

        if backButton.handle_event(event):
            runSettingsMenu.action = "back"

        if saveButton.handle_event(event):
            runSettingsMenu.action = "save"

    mouse_pos = pygame.mouse.get_pos()

    screen.blit(bg, (0, 0))

    panel = pygame.Surface((600, 350))
    panel.set_alpha(120)
    panel.fill((10, 10, 30))
    screen.blit(panel, panel.get_rect(center=(WIDTH//2, HEIGHT//2)))

    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    font = runSettingsMenu.button_font

    # VOLUMEN
    vol_text = font.render("Volumen:", True, (255,255,255))
    screen.blit(vol_text, (WIDTH//2 - 300, HEIGHT//2 - 60))

    pygame.draw.rect(screen, (100, 100, 120), (slider_x, runSettingsMenu.slider_y, 200, 10))
    progress = (runSettingsMenu.volume / 100) * 200
    pygame.draw.rect(screen, (0, 255, 200), (slider_x, runSettingsMenu.slider_y, progress, 10))

    # DIFICULTAD
    diff_title = font.render("Dificultad:", True, (255,255,255))
    screen.blit(diff_title, (WIDTH//2 - 300, HEIGHT//2 + 20))

    easy_color = (0,200,100) if runSettingsMenu.difficulty == "Easy" else (80,80,80)
    hard_color = (200,50,50) if runSettingsMenu.difficulty == "Hard" else (80,80,80)

    pygame.draw.rect(screen, easy_color, runSettingsMenu.easy_rect, border_radius=10)
    pygame.draw.rect(screen, hard_color, runSettingsMenu.hard_rect, border_radius=10)

    screen.blit(font.render("Easy", True, (255,255,255)), runSettingsMenu.easy_rect.move(20,10))
    screen.blit(font.render("Hard", True, (255,255,255)), runSettingsMenu.hard_rect.move(20,10))

    # FULLSCREEN
    fs_title = font.render("Pantalla:", True, (255,255,255))
    screen.blit(fs_title, (WIDTH//2 - 300, HEIGHT//2 + 100))

    on_color = (0,200,100) if runSettingsMenu.fullscreen else (80,80,80)
    off_color = (200,50,50) if not runSettingsMenu.fullscreen else (80,80,80)

    pygame.draw.rect(screen, on_color, runSettingsMenu.fs_on_rect, border_radius=10)
    pygame.draw.rect(screen, off_color, runSettingsMenu.fs_off_rect, border_radius=10)

    screen.blit(font.render("ON", True, (255,255,255)), runSettingsMenu.fs_on_rect.move(35,10))
    screen.blit(font.render("OFF", True, (255,255,255)), runSettingsMenu.fs_off_rect.move(30,10))

    backButton.update(mouse_pos)
    saveButton.update(mouse_pos)

    backButton.draw(screen)
    saveButton.draw(screen)

    # GUARDAR
    if runSettingsMenu.action == "save" and saveButton.is_ready():
        repo.save_settings(
            "game_settings",
            runSettingsMenu.volume,
            runSettingsMenu.difficulty,
            runSettingsMenu.fullscreen
        )

        runSettingsMenu.original_volume = runSettingsMenu.volume
        runSettingsMenu.original_difficulty = runSettingsMenu.difficulty
        runSettingsMenu.original_fullscreen = runSettingsMenu.fullscreen

        runSettingsMenu.action = None

    # VOLVER
    if runSettingsMenu.action == "back" and backButton.is_ready():
        runSettingsMenu.volume = runSettingsMenu.original_volume
        runSettingsMenu.difficulty = runSettingsMenu.original_difficulty
        runSettingsMenu.fullscreen = runSettingsMenu.original_fullscreen

        runSettingsMenu.action = None
        return 1

    pygame.display.flip()
    return 2