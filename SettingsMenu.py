import pygame
from Button import Button
from Repositories.settings_repository import SettingsRepository

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    if not hasattr(runSettingsMenu, "last_size") or runSettingsMenu.last_size != (WIDTH, HEIGHT):
        runSettingsMenu.initialized = False
        runSettingsMenu.last_size = (WIDTH, HEIGHT)

    if not hasattr(runSettingsMenu, "initialized") or runSettingsMenu.initialized == False:
        runSettingsMenu.initialized = True
        is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # --- NUEVA ESCALA AGRESIVA ---
        # Aumentamos considerablemente el tamaño si está en Fullscreen (1.2x)
        scale = 1.2 if is_fullscreen else 0.9

        # Fuentes (Más grandes por la nueva escala)
        title_size = int(HEIGHT * 0.09 * scale) # Subimos título
        label_size = int(HEIGHT * 0.028 * scale) # Subimos labels
        button_font_size = int(HEIGHT * 0.035 * scale) # Subimos texto botones
        
        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", title_size)
        runSettingsMenu.label_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", label_size)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", button_font_size)

        # --- SEPARACIÓN VERTICAL (Más espacio para el nuevo tamaño) ---
        row_height = int(120 * scale) # Subimos de 105 a 120
        start_y = center_y - (row_height * 1.6)

        # Botones medidas (Agrandados por escala)
        btn_w = int(155 * scale) # Subimos ancho
        btn_h = int(55 * scale) # Subimos alto
        gap = int(30 * scale) # Más espacio horizontal

        # 1. Slider de Volumen (Más ancho)
        runSettingsMenu.slider_width = int(WIDTH * 0.45)
        runSettingsMenu.slider_x = center_x - runSettingsMenu.slider_width // 2
        runSettingsMenu.slider_y = start_y + 35
        runSettingsMenu.slider_hitbox = pygame.Rect(runSettingsMenu.slider_x, runSettingsMenu.slider_y - 25, 
                                                   runSettingsMenu.slider_width, 50)

        # Base horizontal para Dificultad y Fullscreen (Ligero shift derecha)
        shift_right_general = int(20 * scale) 
        base_x_general = center_x + shift_right_general

        # 2. Dificultad
        diff_y = start_y + row_height + 25
        runSettingsMenu.easy_rect = pygame.Rect(base_x_general - btn_w - (gap//2), diff_y, btn_w, btn_h)
        runSettingsMenu.hard_rect = pygame.Rect(base_x_general + (gap//2), diff_y, btn_w, btn_h)

        # 3. Fullscreen
        fs_y = diff_y + row_height
        runSettingsMenu.fs_on_rect = pygame.Rect(base_x_general - btn_w - (gap//2), fs_y, btn_w, btn_h)
        runSettingsMenu.fs_off_rect = pygame.Rect(base_x_general + (gap//2), fs_y, btn_w, btn_h)

        # --- NUEVA POSICIÓN HORIZONTAL PARA ACCIONES (MÁS A LA DERECHA) ---
        # Desplazamos este bloque mucho más a la derecha que el resto
        shift_right_acciones = int(150 * scale) 
        base_x_acciones = center_x + shift_right_acciones

        # 4. Botones Guardar / Atrás
        action_y = fs_y + row_height + 20
        # Alineamos el par de botones con el centro en base_x_acciones
        runSettingsMenu.saveButton = Button("Guardar", btn_w, btn_h,
                                            (base_x_acciones - btn_w - (gap//2), action_y),
                                            runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", btn_w, btn_h,
                                            (base_x_acciones + (gap//2), action_y),
                                            runSettingsMenu.button_font)

        # Panel (Mucho más grande y ancho para cubrir el nuevo diseño)
        panel_w = int(runSettingsMenu.slider_width + 400 * scale)
        panel_h = int(HEIGHT * 0.85) # Más alto para despegar botones finales
        runSettingsMenu.panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        runSettingsMenu.panel_rect.center = (center_x, center_y)

        runSettingsMenu.action = None

        data = repo.get_settings("game_settings")
        if data:
            runSettingsMenu.volume = data["data"]["volume"]
            runSettingsMenu.difficulty = data["data"]["difficulty"]
            runSettingsMenu.fullscreen = data["data"].get("fullscreen", False)
        else:
            runSettingsMenu.volume = 50
            runSettingsMenu.difficulty = "Easy"
            runSettingsMenu.fullscreen = False

    # --- RENDERIZADO ---
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(bg, (0, 0))
    center_x = WIDTH // 2

    # Panel fondo (Un tono más oscuro y opaco para el nuevo tamaño)
    panel_surf = pygame.Surface((runSettingsMenu.panel_rect.width, runSettingsMenu.panel_rect.height))
    panel_surf.set_alpha(200) # Subimos opacidad
    panel_surf.fill((10, 5, 20))
    screen.blit(panel_surf, runSettingsMenu.panel_rect)

    # Título (Despegado un poco más)
    title_text = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title_text, title_text.get_rect(center=(center_x, runSettingsMenu.panel_rect.top + 70)))

    # Slider (Línea más gruesa)
    pygame.draw.rect(screen, (60, 60, 80), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, runSettingsMenu.slider_width, 10), border_radius=5)
    vol_w = (runSettingsMenu.volume / 100) * runSettingsMenu.slider_width
    pygame.draw.rect(screen, (0, 255, 200), (runSettingsMenu.slider_x, runSettingsMenu.slider_y, vol_w, 10), border_radius=5)
    pygame.draw.circle(screen, (255, 255, 255), (int(runSettingsMenu.slider_x + vol_w), runSettingsMenu.slider_y + 5), 12) # Círculo más grande
    
    vol_lbl = runSettingsMenu.label_font.render(f"Volumen: {runSettingsMenu.volume}", True, (220, 220, 220))
    screen.blit(vol_lbl, (runSettingsMenu.slider_x, runSettingsMenu.slider_y - 40)) # Más despegado

    # Dificultad (Alineado con base_x_general)
    diff_lbl = runSettingsMenu.label_font.render("Dificultad", True, (220, 220, 220))
    # Alineamos etiqueta con el primer botón de su bloque
    screen.blit(diff_lbl, (runSettingsMenu.easy_rect.x, runSettingsMenu.easy_rect.y - 35))
    
    e_col = (0, 200, 100) if runSettingsMenu.difficulty == "Easy" else (60, 60, 60)
    h_col = (200, 50, 50) if runSettingsMenu.difficulty == "Hard" else (60, 60, 60)
    pygame.draw.rect(screen, e_col, runSettingsMenu.easy_rect, border_radius=12) # Bordes más suaves
    pygame.draw.rect(screen, h_col, runSettingsMenu.hard_rect, border_radius=12)
    
    # Texto de botones centrado manualmente dentro del rect (ajustado por nuevo tamaño)
    screen.blit(runSettingsMenu.button_font.render("Easy", True, (255,255,255)), runSettingsMenu.easy_rect.move(35, 12))
    screen.blit(runSettingsMenu.button_font.render("Hard", True, (255,255,255)), runSettingsMenu.hard_rect.move(35, 12))

    # Fullscreen
    fs_lbl = runSettingsMenu.label_font.render("Pantalla Fullscreen", True, (220, 220, 220))
    screen.blit(fs_lbl, (runSettingsMenu.fs_on_rect.x, runSettingsMenu.fs_on_rect.y - 35))

    on_col = (0, 200, 100) if runSettingsMenu.fullscreen else (60, 60, 60)
    off_col = (200, 50, 50) if not runSettingsMenu.fullscreen else (60, 60, 60)
    pygame.draw.rect(screen, on_col, runSettingsMenu.fs_on_rect, border_radius=12)
    pygame.draw.rect(screen, off_col, runSettingsMenu.fs_off_rect, border_radius=12)
    
    screen.blit(runSettingsMenu.button_font.render("ON", True, (255,255,255)), runSettingsMenu.fs_on_rect.move(50, 12))
    screen.blit(runSettingsMenu.button_font.render("OFF", True, (255,255,255)), runSettingsMenu.fs_off_rect.move(45, 12))

    # Dibujar Botones de acción (Ya posicionados en base_x_acciones)
    runSettingsMenu.saveButton.update(mouse_pos)
    runSettingsMenu.backButton.update(mouse_pos)
    runSettingsMenu.saveButton.draw(screen)
    runSettingsMenu.backButton.draw(screen)

    # --- EVENTOS ---
    for event in events:
        if event.type == pygame.QUIT: return 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if runSettingsMenu.slider_hitbox.collidepoint(mx, my):
                rel_x = mx - runSettingsMenu.slider_x
                runSettingsMenu.volume = max(0, min(100, int((rel_x / runSettingsMenu.slider_width) * 100)))
            if runSettingsMenu.easy_rect.collidepoint(mx, my): runSettingsMenu.difficulty = "Easy"
            if runSettingsMenu.hard_rect.collidepoint(mx, my): runSettingsMenu.difficulty = "Hard"
            if runSettingsMenu.fs_on_rect.collidepoint(mx, my): runSettingsMenu.fullscreen = True
            if runSettingsMenu.fs_off_rect.collidepoint(mx, my): runSettingsMenu.fullscreen = False

        if runSettingsMenu.saveButton.handle_event(event): runSettingsMenu.action = "save"
        if runSettingsMenu.backButton.handle_event(event): runSettingsMenu.action = "back"

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