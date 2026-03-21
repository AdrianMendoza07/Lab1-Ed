import pygame
import sys
from Button import Button
from Repositories.Settings_repository import SettingsRepository

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
        runSettingsMenu.slider_x = WIDTH//2 + 50
        runSettingsMenu.slider_y = HEIGHT//2 - 60
        runSettingsMenu.slider_width = 200
        runSettingsMenu.slider_height = 10

        # checkbox config
        runSettingsMenu.checkbox_x = WIDTH//2 + 120
        runSettingsMenu.checkbox_y = HEIGHT//2 + 80
        runSettingsMenu.box_size = 25

        # Estado
        runSettingsMenu.action = None
    
    backButton = runSettingsMenu.backButton
    saveButton = runSettingsMenu.saveButton

    # variables locales
    slider_x = runSettingsMenu.slider_x
    slider_y = runSettingsMenu.slider_y
    slider_width = runSettingsMenu.slider_width
    slider_height = runSettingsMenu.slider_height

    checkbox_x = runSettingsMenu.checkbox_x
    checkbox_y = runSettingsMenu.checkbox_y
    box_size = runSettingsMenu.box_size
    
    #Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        # controles de teclado
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

        # slider con mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if slider_x <= mx <= slider_x + slider_width and slider_y - 10 <= my <= slider_y + 20:
                porcentaje = (mx - slider_x) / slider_width
                runSettingsMenu.volume = int(porcentaje * 100)

            # checkbox click
            if checkbox_x <= mx <= checkbox_x + box_size and checkbox_y <= my <= checkbox_y + box_size:
                runSettingsMenu.fullscreen = not runSettingsMenu.fullscreen


        if backButton.handle_event(event):
            runSettingsMenu.action = "back" 
        if saveButton.handle_event(event):
            runSettingsMenu.action = "save"   
            
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.blit(bg, (0, 0))

    # panel
    panel = pygame.Surface((600, 350))
    panel.set_alpha(120) 
    panel.fill((10, 10, 30)) 
    panel_rect = panel.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(panel, panel_rect)

    # Title
    title = runSettingsMenu.title_font.render("Opciones", True, (210, 15, 240))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    screen.blit(title, title_rect)

    # mostrar valores
    font = runSettingsMenu.button_font
    color_txt = (0, 255, 200)

    vol_surf = font.render(f"Volumen: {runSettingsMenu.volume}", True, (255,255,255))
    diff_surf = font.render(f"Dificultad: {runSettingsMenu.difficulty}", True, color_txt)
    full_surf = font.render("Pantalla Completa:", True, color_txt)

    screen.blit(vol_surf, (WIDTH//2 - 200, HEIGHT//2 - 80))
    screen.blit(diff_surf, (WIDTH//2 - 200, HEIGHT//2))
    screen.blit(full_surf, (WIDTH//2 - 200, HEIGHT//2 + 80))


    #  SLIDER
    pygame.draw.rect(screen, (100, 100, 120), (slider_x, slider_y, slider_width, slider_height), border_radius=5)

    progress = (runSettingsMenu.volume / 100) * slider_width
    pygame.draw.rect(screen, (0, 255, 200), (slider_x, slider_y, progress, slider_height), border_radius=5)

    handle_x = slider_x + progress
    pygame.draw.circle(screen, (200, 255, 255), (int(handle_x), slider_y + slider_height//2), 8)


    # CHECKBOX
    pygame.draw.rect(screen, (200, 200, 200), (checkbox_x, checkbox_y, box_size, box_size), 2)

    if runSettingsMenu.fullscreen:
        pygame.draw.line(screen, (255, 100, 200), (checkbox_x, checkbox_y), (checkbox_x + box_size, checkbox_y + box_size), 3)
        pygame.draw.line(screen, (255, 100, 200), (checkbox_x + box_size, checkbox_y), (checkbox_x, checkbox_y + box_size), 3)
    
    
    backButton.update(mouse_pos)
    saveButton.update(mouse_pos)       
    
    backButton.draw(screen)
    saveButton.draw(screen)

    # guardar en persistencia
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
    
    # Actualizar 
    pygame.display.flip()
    
    return 2