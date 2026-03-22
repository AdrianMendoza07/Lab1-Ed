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

        # CARGAR DATOS
        data = repo.get_settings("game_settings")

        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"

        # COPIA ORIGINAL
        runSettingsMenu.original_volume = runSettingsMenu.volume
        runSettingsMenu.original_difficulty = runSettingsMenu.difficulty

        # SLIDER
        runSettingsMenu.slider_x = WIDTH//2 - 40
        runSettingsMenu.slider_y = HEIGHT//2 - 50
        runSettingsMenu.slider_width = 200
        runSettingsMenu.slider_height = 10

        # BOTONES DE DIFICULTAD
        runSettingsMenu.easy_rect = pygame.Rect(WIDTH//2 - 20, HEIGHT//2 + 20, 120, 50)
        runSettingsMenu.hard_rect = pygame.Rect(WIDTH//2 + 140, HEIGHT//2 + 20, 120, 50)

        runSettingsMenu.action = None

    backButton = runSettingsMenu.backButton
    saveButton = runSettingsMenu.saveButton

    slider_x = runSettingsMenu.slider_x
    slider_y = runSettingsMenu.slider_y
    slider_width = runSettingsMenu.slider_width
    slider_height = runSettingsMenu.slider_height

    # EVENTOS
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
            if slider_x <= mx <= slider_x + slider_width and slider_y - 10 <= my <= slider_y + 20:
                porcentaje = (mx - slider_x) / slider_width
                runSettingsMenu.volume = int(porcentaje * 100)

            # CLICK EASY
            if runSettingsMenu.easy_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Easy"

            # CLICK HARD
            if runSettingsMenu.hard_rect.collidepoint(mx, my):
                runSettingsMenu.difficulty = "Hard"

        if backButton.handle_event(event):
            runSettingsMenu.action = "back"

        if saveButton.handle_event(event):
            runSettingsMenu.action = "save"

    mouse_pos = pygame.mouse.get_pos()

    # FONDO
    screen.blit(bg, (0, 0))

    panel = pygame.Surface((600, 300))
    panel.set_alpha(120)
    panel.fill((10, 10, 30))
    screen.blit(panel, panel.get_rect(center=(WIDTH//2, HEIGHT//2)))

    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    font = runSettingsMenu.button_font

    # VOLUMEN
    vol_text = font.render("Volumen:", True, (255,255,255))
    screen.blit(vol_text, (WIDTH//2 - 300, HEIGHT//2 - 60))

    pygame.draw.rect(screen, (100, 100, 120), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    progress = (runSettingsMenu.volume / 100) * slider_width
    pygame.draw.rect(screen, (0, 255, 200), (slider_x, slider_y, progress, slider_height), border_radius=5)

    handle_x = slider_x + progress
    pygame.draw.circle(screen, (200, 255, 255), (int(handle_x), slider_y + slider_height//2), 8)

    volume_value = font.render(str(runSettingsMenu.volume), True, (255,255,255))
    screen.blit(volume_value, (slider_x + slider_width + 20, slider_y - 10))

    # DIFICULTAD (BOTONES)

    diff_title = font.render("Dificultad:", True, (255,255,255))
    screen.blit(diff_title, (WIDTH//2 - 300, HEIGHT//2 + 20))

    # COLORES
    easy_color = (0, 200, 100) if runSettingsMenu.difficulty == "Easy" else (80, 80, 80)
    hard_color = (200, 50, 50) if runSettingsMenu.difficulty == "Hard" else (80, 80, 80)

    # HOVER
    if runSettingsMenu.easy_rect.collidepoint(mouse_pos):
        easy_color = (0, 255, 150)

    if runSettingsMenu.hard_rect.collidepoint(mouse_pos):
        hard_color = (255, 80, 80)

    # DIBUJAR BOTONES
    pygame.draw.rect(screen, easy_color, runSettingsMenu.easy_rect, border_radius=10)
    pygame.draw.rect(screen, hard_color, runSettingsMenu.hard_rect, border_radius=10)

    easy_text = font.render("Easy", True, (255,255,255))
    hard_text = font.render("Hard", True, (255,255,255))

    screen.blit(easy_text, easy_text.get_rect(center=runSettingsMenu.easy_rect.center))
    screen.blit(hard_text, hard_text.get_rect(center=runSettingsMenu.hard_rect.center))

    # BOTONES GENERALES
    backButton.update(mouse_pos)
    saveButton.update(mouse_pos)

    backButton.draw(screen)
    saveButton.draw(screen)

    # GUARDAR
    if runSettingsMenu.action == "save" and saveButton.is_ready():
        repo.save_settings(
            "game_settings",
            runSettingsMenu.volume,
            runSettingsMenu.difficulty
        )

        runSettingsMenu.original_volume = runSettingsMenu.volume
        runSettingsMenu.original_difficulty = runSettingsMenu.difficulty

        runSettingsMenu.action = None

    # VOLVER
    if runSettingsMenu.action == "back" and backButton.is_ready():
        runSettingsMenu.volume = runSettingsMenu.original_volume
        runSettingsMenu.difficulty = runSettingsMenu.original_difficulty

        runSettingsMenu.action = None
        return 1

    pygame.display.flip()

    return 2