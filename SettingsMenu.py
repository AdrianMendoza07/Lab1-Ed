import pygame
from Button import Button
from Repositories.settings_repository import SettingsRepository

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    # Detectar cambio de resolución para reinicializar posiciones
    if not hasattr(runSettingsMenu, "last_size") or runSettingsMenu.last_size != (WIDTH, HEIGHT):
        runSettingsMenu.initialized = False
        runSettingsMenu.last_size = (WIDTH, HEIGHT)

    if not hasattr(runSettingsMenu, "initialized") or runSettingsMenu.initialized == False:
        runSettingsMenu.initialized = True
        is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        scale = 1 if is_fullscreen else 0.8

        # Fuentes
        title_size = int(HEIGHT * 0.07 * scale)
        button_font_size = int(HEIGHT * 0.03 * scale)
        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", title_size)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", button_font_size)

        # Configuración de Layout 
        row_height = int(75 * scale)
        start_y = center_y - (row_height * 1.5)

        # Posición Slider
        runSettingsMenu.slider_width = int(WIDTH * 0.3)
        runSettingsMenu.slider_x = center_x - runSettingsMenu.slider_width // 2
        runSettingsMenu.slider_y = start_y + 20
        # Rectángulo invisible para detectar clics precisos en el volumen
        runSettingsMenu.slider_hitbox = pygame.Rect(runSettingsMenu.slider_x, runSettingsMenu.slider_y - 15, 
                                                   runSettingsMenu.slider_width, 40)

        # Posición Dificultad
        diff_y = start_y + row_height + 10
        btn_w = int(120 * scale)
        btn_h = int(45 * scale)
        runSettingsMenu.easy_rect = pygame.Rect(center_x - btn_w - 10, diff_y, btn_w, btn_h)
        runSettingsMenu.hard_rect = pygame.Rect(center_x + 10, diff_y, btn_w, btn_h)

        # Posición Fullscreen
        fs_y = diff_y + row_height
        runSettingsMenu.fs_on_rect = pygame.Rect(center_x - btn_w - 10, fs_y, btn_w, btn_h)
        runSettingsMenu.fs_off_rect = pygame.Rect(center_x + 10, fs_y, btn_w, btn_h)

        # Botones de Acción (Guardar / Atrás)
        action_y = fs_y + row_height + 20
        runSettingsMenu.saveButton = Button("Guardar", btn_w + 20, btn_h,
                                            (center_x - btn_w - 20, action_y),
                                            runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", btn_w + 20, btn_h,
                                            (center_x + 20, action_y),
                                            runSettingsMenu.button_font)

        # Tamaño del Panel de fondo
        panel_w = int(WIDTH * 0.5)
        panel_h = int(HEIGHT * 0.6)
        runSettingsMenu.panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        runSettingsMenu.panel_rect.center = (center_x, center_y)

        runSettingsMenu.action = None

        # Cargar datos del Repo
        data = repo.get_settings("game_settings")
        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
            runSettingsMenu.fullscreen = data["data"].get("fullscreen", False)
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"
            runSettingsMenu.fullscreen = False

    # RENDERIZADO
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(bg, (0, 0))
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Panel
    panel_surf = pygame.Surface((runSettingsMenu.panel_rect.width, runSettingsMenu.panel_rect.height))
    panel_surf.set_alpha(160)
    panel_surf.fill((20, 10, 40))
    screen.blit(panel_surf, runSettingsMenu.panel_rect)

    # Título
    title_text = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title_text, title_text.get_rect(center=(center_x, runSettingsMenu.panel_rect.top + 50)))

    # Dibujar Slider de Volumen
    pygame.draw.rect(screen, (60, 60, 80), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, runSettingsMenu.slider_width, 8), border_radius=4)
    vol_w = (runSettingsMenu.volume / 100) * runSettingsMenu.slider_width
    pygame.draw.rect(screen, (0, 255, 200), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, vol_w, 8), border_radius=4)
    pygame.draw.circle(screen, (255, 255, 255), (int(runSettingsMenu.slider_x + vol_w), runSettingsMenu.slider_y + 4), 10)
    
    vol_lbl = runSettingsMenu.button_font.render(f"Volumen: {runSettingsMenu.volume}", True, (255, 255, 255))
    screen.blit(vol_lbl, (runSettingsMenu.slider_x, runSettingsMenu.slider_y - 30))

    # Dibujar Dificultad
    diff_lbl = runSettingsMenu.button_font.render("Dificultad", True, (255, 255, 255))
    screen.blit(diff_lbl, (runSettingsMenu.easy_rect.x, runSettingsMenu.easy_rect.y - 25))
    
    e_col = (0, 200, 100) if runSettingsMenu.difficulty == "Easy" else (60, 60, 60)
    h_col = (200, 50, 50) if runSettingsMenu.difficulty == "Hard" else (60, 60, 60)
    pygame.draw.rect(screen, e_col, runSettingsMenu.easy_rect, border_radius=8)
    pygame.draw.rect(screen, h_col, runSettingsMenu.hard_rect, border_radius=8)
    
    screen.blit(runSettingsMenu.button_font.render("Easy", True, (255,255,255)), runSettingsMenu.easy_rect.move(20, 8))
    screen.blit(runSettingsMenu.button_font.render("Hard", True, (255,255,255)), runSettingsMenu.hard_rect.move(20, 8))

    # Dibujar Pantalla
    fs_lbl = runSettingsMenu.button_font.render("Pantalla Fullscreen", True, (255, 255, 255))
    screen.blit(fs_lbl, (runSettingsMenu.fs_on_rect.x, runSettingsMenu.fs_on_rect.y - 25))

    on_col = (0, 200, 100) if runSettingsMenu.fullscreen else (60, 60, 60)
    off_col = (200, 50, 50) if not runSettingsMenu.fullscreen else (60, 60, 60)
    pygame.draw.rect(screen, on_col, runSettingsMenu.fs_on_rect, border_radius=8)
    pygame.draw.rect(screen, off_col, runSettingsMenu.fs_off_rect, border_radius=8)
    
    screen.blit(runSettingsMenu.button_font.render("ON", True, (255,255,255)), runSettingsMenu.fs_on_rect.move(30, 8))
    screen.blit(runSettingsMenu.button_font.render("OFF", True, (255,255,255)), runSettingsMenu.fs_off_rect.move(25, 8))

    # Actualizar y dibujar botones Guardar/Atras
    runSettingsMenu.saveButton.update(mouse_pos)
    runSettingsMenu.backButton.update(mouse_pos)
    runSettingsMenu.saveButton.draw(screen)
    runSettingsMenu.backButton.draw(screen)

    # LÓGICA DE EVENTOS 
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Ajustar volumen 
            if runSettingsMenu.slider_hitbox.collidepoint(mx, my):
                rel_x = mx - runSettingsMenu.slider_x
                runSettingsMenu.volume = int((rel_x / runSettingsMenu.slider_width) * 100)
                runSettingsMenu.volume = max(0, min(100, runSettingsMenu.volume))

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

    # Acciones de botones
    if runSettingsMenu.action == "save" and runSettingsMenu.saveButton.is_ready():
        repo.save_settings("game_settings", runSettingsMenu.volume, runSettingsMenu.difficulty, runSettingsMenu.fullscreen)
        if runSettingsMenu.fullscreen:
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((800, 600))
        
        bg = pygame.transform.scale(bg, screen.get_size())
        runSettingsMenu.initialized = False
        runSettingsMenu.action = None
        return 2, screen, bg

    if runSettingsMenu.action == "back" and runSettingsMenu.backButton.is_ready():
        runSettingsMenu.action = None
        return 1

    pygame.display.flip()
    return 2