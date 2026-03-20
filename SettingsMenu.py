import pygame
import sys
from Button import Button



def runSettingsMenu(screen, events, bg):
    WIDTH, HEIGHT = screen.get_size()

    # Variables creadas solo al inicio
    if not hasattr(runSettingsMenu, "initialized"):
        runSettingsMenu.initialized = True

        # Fuentes 
        runSettingsMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runSettingsMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        # Botones
        runSettingsMenu.backButton = Button("Atras", 200, 60, (WIDTH-200 , HEIGHT-150), runSettingsMenu.button_font)
        

        
        # Estado
        runSettingsMenu.action = None
    
    backButton = runSettingsMenu.backButton
    
    title_font = runSettingsMenu.title_font
    
    #Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0
        if backButton.handle_event(event):
            runSettingsMenu.action = "back"    
            
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.blit(bg, (0, 0))

    # Title
    title = title_font.render("Opciones", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    for i in range(6, 0, -1):
        glow = title_font.render("Opciones", True, (255, 20, 147))
        screen.blit(glow, title_rect)
    
    backButton.update(mouse_pos)       
    
    backButton.draw(screen)
    
    if runSettingsMenu.action == "back" and backButton.is_ready():
        runSettingsMenu.action = None
        return 1
    
    # Actualizar 
    pygame.display.flip()
    
    return 2 
