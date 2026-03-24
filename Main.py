from UsersMenu import runUsersMenu
from newUsersMenu import runNewUsersMenu
import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from Repositories.settings_repository import get_settings_data
from Repositories.Profile_repository import ProfileRepository
from LeaderboardMenu import runLeaderboardMenu
from Game import runGame

pygame.init()

settings = get_settings_data()
selected_user = None

if settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((800, 600))

# Reloj para controlar la velocidad de actualización (FPS)
clock = pygame.time.Clock()

bg_original = pygame.image.load("assets/images/background.jpeg").convert()
bg = pygame.transform.scale(bg_original, screen.get_size())

bg_original2 = pygame.image.load("assets/images/background2.png").convert()
bg2 = pygame.transform.scale(bg_original2, screen.get_size())


running = True

# Variable de estado que controla el menú 
state = 1

# Bucle principal del programa
while running:
    
    # Captura de todos los eventos del sistema (teclado, mouse, etc.)
    events = pygame.event.get()

    for event in events:
        # Si el usuario cierra la ventana o el estado indica salida
        if event.type == pygame.QUIT or state == 0:
            running = False

    # Control de navegación entre menús según el estado actual
    # Menú principal
    if state == 1:
        state = runStartMenu(screen, events, bg)   
    
    #Menu de Configuracion
    if state == 2:
        result = runSettingsMenu(screen, events, bg, bg_original)
        if isinstance(result, tuple):
            state, screen, bg = result
        else:
            state = result

    # Menú de leaderboard
    if state == 3:
        state = runLeaderboardMenu(screen, events, bg)
        
    #Menu de creacion de perfil
    if state == 5:
        state = runNewUsersMenu(screen, events, bg)    
        if state == 4:  # coming back to users menu
            if hasattr(runUsersMenu, "initialized"):
                del runUsersMenu.initialized
    
    #Menu de seleccion de usuarion antes del juego
    if state == 4:
        result = runUsersMenu(screen, events, bg)

        if isinstance(result, tuple):
            state, selected_user = result
        else:
            state = result
        
    #Juego            
    if state == 6:
        if selected_user is None:
            print("ERROR: no hay usuario seleccionado")
            state = 4
        else:
            state = runGame(screen, events, bg2, selected_user)    
    
    clock.tick(60)    
        
# Finalización de pygame y liberación de recursos
pygame.quit()
