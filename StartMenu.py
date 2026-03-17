import pygame
import sys
from Button import Button


def runStartMenu(screen, events):
    
    WIDTH, HEIGHT = screen.get_size()

    clock = pygame.time.Clock()

    # Fuentes
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 40)

    # Botones rects
    startButton = Button("Nuevo Juego", 200, 60, (WIDTH//2 , 220), button_font)
    leaderboardButton = Button("Leaderboard", 200, 60, (WIDTH//2, 300), button_font)
    settingsButton = Button("Opcion", 200, 60, (WIDTH//2, 380), button_font)
    quitButton = Button("Salir", 200, 60, (WIDTH//2, 460), button_font)

    # Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0
        if settingsButton.isClicked(event):
            return 2     
        if quitButton.isClicked(event):
            return 0


    # Posicion mouse
    mouse_pos = pygame.mouse.get_pos()

    # Limpa 
    screen.fill((30, 30, 40))

    # Title
    title = title_font.render("Neon Runners", True, (210, 15, 240))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    screen.blit(title, title_rect)
    
    
    
    startButton.update(mouse_pos)
    leaderboardButton.update(mouse_pos)
    settingsButton.update(mouse_pos)
    quitButton.update(mouse_pos)
    
    startButton.draw(screen)
    leaderboardButton.draw(screen)
    settingsButton.draw(screen)
    quitButton.draw(screen)


    # Actualizar 
    pygame.display.flip()

    clock.tick(60)
    
    return 1

