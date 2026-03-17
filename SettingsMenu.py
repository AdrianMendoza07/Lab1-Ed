import pygame
import sys
from Button import Button




def runSettingsMenu(screen, events):
    WIDTH, HEIGHT = screen.get_size()

    clock = pygame.time.Clock()

    # Fuentes
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 40)

    backButton = Button("Back", 200, 60, (WIDTH-200, HEIGHT-100), button_font)
    
    #Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0
        if backButton.isClicked(event):
            return 1    
            
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.fill((30, 30, 40))

    # Title
    title = title_font.render("Opciones", True, (210, 15, 240))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    screen.blit(title, title_rect)
    
    backButton.update(mouse_pos)       
    backButton.draw(screen)
    
    # Actualizar 
    pygame.display.flip()

    clock.tick(60)
    
    return 2 
