from UsersMenu import runUsersMenu
from newUsersMenu import runNewUsersMenu
import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from Repositories.Profile_repository import ProfileRepository
from LeaderboardMenu import runLeaderboardMenu

# Instancia del repositorio de perfiles (gestión de datos de usuarios)
repo = ProfileRepository()

# Inicialización de todos los módulos de pygame
pygame.init()

# Creación de la ventana en modo pantalla completa (0,0 usa la resolución del sistema)
screen = pygame.display.set_mode((0, 0))

# Reloj para controlar la velocidad de actualización (FPS)
clock = pygame.time.Clock()

# Carga de la imagen de fondo
bg = pygame.image.load("assets/images/background.jpeg").convert()

# Ajuste del tamaño del fondo al tamaño de la ventana
bg = pygame.transform.scale(bg, screen.get_size())

# Variable de control del ciclo principal del juego
running = True

# Variable de estado que controla el menú 
state = 1

# Bucle principal del programa
while running:
    
    # Captura de todos los eventos del sistema (teclado, mouse, etc.)
    events = pygame.event.get()
    
    # Procesamiento de eventos globales
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
        state = runSettingsMenu(screen, events, bg)   

    # Menú de leaderboard
    if state == 3:
        state = runLeaderboardMenu(screen, events, bg)
        
    if state == 4:
        state = runUsersMenu(screen, events, bg)  

    if state == 5:
        state = runNewUsersMenu(screen, events, bg)    
        if state == 4:  # coming back to users menu
            if hasattr(runUsersMenu, "initialized"):
                del runUsersMenu.initialized
    
    clock.tick(60)    
        
# Finalización de pygame y liberación de recursos
pygame.quit()