import pygame
import sys
from Button import Button
from Repositories.settings_repository import SettingsRepository

repo = SettingsRepository()

def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    # Variables creadas solo al inicio
    if not hasattr(runSettingsMenu, "initialized"):
        runSettingsMenu.initialized = True

        # Fuentes 
        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        # Botones
        runSettingsMenu.saveButton = Button("Guardar", 200, 60, (WIDTH//2 - 110, HEIGHT - 100), runSettingsMenu.button_font)
        runSettingsMenu.backButton = Button("Atras", 200, 60, (WIDTH//2 + 110, HEIGHT - 100), runSettingsMenu.button_font)

        # valores iniciales
        runSettingsMenu.volume = 50
        runSettingsMenu.difficulty = "Normal"
        runSettingsMenu.fullscreen = False

        # slider config
        runSettingsMenu.slider_x = WIDTH//2 + 20
        runSettingsMenu.slider_y = HEIGHT//2 - 50
        runSettingsMenu.slider_width = 200
        runSettingsMenu.slider_height = 10

        # checkbox config (alineado mejor)
        runSettingsMenu.checkbox_x = WIDTH//2 + 200
        runSettingsMenu.checkbox_y = HEIGHT//2 + 70
        runSettingsMenu.box_size = 25

        # Estado
        runSettingsMenu.action = None
    
    backButton = runSettingsMenu.backButton
    saveButton = runSettingsMenu.saveButton

    slider_x = runSettingsMenu.slider_x
    slider_y = runSettingsMenu.slider_y
    slider_width = runSettingsMenu.slider_width
    slider_height = runSettingsMenu.slider_height

    checkbox_x = runSettingsMenu.checkbox_x
    checkbox_y = runSettingsMenu.checkbox_y
    box_size = runSettingsMenu.box_size
    
    # Eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                runSettingsMenu.volume = min(100, runSettingsMenu.volume + 5)
            if event.key == pygame.K_DOWN:
                runSettingsMenu.volume = max(0, runSettingsMenu.volume - 5)

            if event.key == pygame.K_RIGHT:
                runSettingsMenu.difficulty = "Hard"
            if event.key == pygame.K_LEFT:
                runSettingsMenu.difficulty = "Easy"

            if event.key == pygame.K_f:
                runSettingsMenu.fullscreen = not runSettingsMenu.fullscreen

        # Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # slider
            if slider_x <= mx <= slider_x + slider_width and slider_y - 10 <= my <= slider_y + 20:
                porcentaje = (mx - slider_x) / slider_width
                runSettingsMenu.volume = int(porcentaje * 100)

            # checkbox
            if checkbox_x <= mx <= checkbox_x + box_size and checkbox_y <= my <= checkbox_y + box_size:
                runSettingsMenu.fullscreen = not runSettingsMenu.fullscreen

                if runSettingsMenu.fullscreen:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode((1280, 720))

        if backButton.handle_event(event):
            runSettingsMenu.action = "back" 
        if saveButton.handle_event(event):
            runSettingsMenu.action = "save"   
            
    mouse_pos = pygame.mouse.get_pos()

    # Fondo
    screen.blit(bg, (0, 0))

    # Panel
    panel = pygame.Surface((600, 350))
    panel.set_alpha(120) 
    panel.fill((10, 10, 30)) 
    panel_rect = panel.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(panel, panel_rect)

    # Title
    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

    font = runSettingsMenu.button_font
    color_txt = (0, 255, 200)

    # Volumen
    vol_surf = font.render("Volumen:", True, (255,255,255))
    screen.blit(vol_surf, (WIDTH//2 - 250, HEIGHT//2 - 60))

    pygame.draw.rect(screen, (100, 100, 120), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    progress = (runSettingsMenu.volume / 100) * slider_width
    pygame.draw.rect(screen, (0, 255, 200), (slider_x, slider_y, progress, slider_height), border_radius=5)

    handle_x = slider_x + progress
    pygame.draw.circle(screen, (200, 255, 255), (int(handle_x), slider_y + slider_height//2), 8)

    volume_value = font.render(str(runSettingsMenu.volume), True, (255,255,255))
    screen.blit(volume_value, (slider_x + slider_width + 20, slider_y - 10))

    # Dificultad centrada
    diff_surf = font.render(f"Dificultad: {runSettingsMenu.difficulty}", True, color_txt)
    screen.blit(diff_surf, diff_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

    # Pantalla completa centrada
    full_surf = font.render("Pantalla Completa:", True, color_txt)
    screen.blit(full_surf, full_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 80)))

    # Checkbox visible
    pygame.draw.rect(screen, (255, 255, 255), (checkbox_x, checkbox_y, box_size, box_size), 3)

    if runSettingsMenu.fullscreen:
        pygame.draw.line(screen, (0, 255, 200), (checkbox_x, checkbox_y),
                         (checkbox_x + box_size, checkbox_y + box_size), 3)
        pygame.draw.line(screen, (0, 255, 200), (checkbox_x + box_size, checkbox_y),
                         (checkbox_x, checkbox_y + box_size), 3)

    backButton.update(mouse_pos)
    saveButton.update(mouse_pos)       
    
    backButton.draw(screen)
    saveButton.draw(screen)

    if runSettingsMenu.action == "save" and saveButton.is_ready():
        repo.save_settings(
            "game_settings",
            runSettingsMenu.volume,
            runSettingsMenu.difficulty,
            runSettingsMenu.fullscreen
        )
        print("Configuración guardada")
        runSettingsMenu.action = None
    
    if runSettingsMenu.action == "back" and backButton.is_ready():
        runSettingsMenu.action = None
        return 1
    
    pygame.display.flip()
    
    return 2