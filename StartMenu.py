import pygame
from Button import Button


def runStartMenu(screen, events, bg):
    
    WIDTH, HEIGHT = screen.get_size()

    # Variables creadas solo al inicio
    if not hasattr(runStartMenu, "initialized"):
        runStartMenu.initialized = True

        # Fuentes 
        runStartMenu.title_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 80)
        runStartMenu.button_font = pygame.font.Font("assets/fonts/Orbitron-Regular.ttf", 40)

        # Botones
        runStartMenu.startButton = Button("Nuevo Juego", 500, 60, (WIDTH//2 , 350), runStartMenu.button_font)
        runStartMenu.leaderboardButton = Button("Leaderboard", 500, 60, (WIDTH//2, 430), runStartMenu.button_font)
        runStartMenu.settingsButton = Button("Opciones", 500, 60, (WIDTH//2, 510), runStartMenu.button_font)
        runStartMenu.quitButton = Button("Salir", 500, 60, (WIDTH//2, 590), runStartMenu.button_font)

        # Estado
        runStartMenu.action = None

    # Para acceder a los botones mas rapido
    startButton = runStartMenu.startButton
    leaderboardButton = runStartMenu.leaderboardButton
    settingsButton = runStartMenu.settingsButton
    quitButton = runStartMenu.quitButton

    title_font = runStartMenu.title_font

    # Manejo de eventos
    for event in events:
        if event.type == pygame.QUIT:
            return 0

        if settingsButton.handle_event(event):
            runStartMenu.action = "settings"

        if quitButton.handle_event(event):
            runStartMenu.action = "quit"
        
        if startButton.handle_event(event):
            runStartMenu.action = "users"    

    # Actualizar posicion y botones
    mouse_pos = pygame.mouse.get_pos()

    startButton.update(mouse_pos)
    leaderboardButton.update(mouse_pos)
    settingsButton.update(mouse_pos)
    quitButton.update(mouse_pos)

    # Seccion de draw
    # Limpiar pantalla
    screen.blit(bg, (0, 0))

    # Titulo
    title = title_font.render("Neon Runners", True, (255, 60, 200))
    title_rect = title.get_rect(center=(WIDTH//2, 150))
    for i in range(6, 0, -1):
        glow = title_font.render("Neon Runners", True, (255, 20, 147))
        screen.blit(glow, title_rect)

    # Botones
    startButton.draw(screen)
    leaderboardButton.draw(screen)
    settingsButton.draw(screen)
    quitButton.draw(screen)

    # Cambio de estado (para delay entre click y cambio)
    if runStartMenu.action == "settings" and settingsButton.is_ready():
        runStartMenu.action = None
        return 2
    
    if runStartMenu.action == "users" and startButton.is_ready():
        runStartMenu.action = None
        return 3

    if runStartMenu.action == "quit" and quitButton.is_ready():
        return 0

    pygame.display.flip()

    return 1

