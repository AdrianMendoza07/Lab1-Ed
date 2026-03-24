from UsersMenu import runUsersMenu
from newUsersMenu import runNewUsersMenu
import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from Repositories.settings_repository import get_settings_data
from Repositories.Profile_repository import ProfileRepository
from LeaderboardMenu import runLeaderboardMenu

import sys
import random
import string
import time

pygame.init()

def random_name(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

def run_benchmark_for_size(num_records):
    print(f"\n--- Probando con {num_records} registros ---")
    repo = ProfileRepository()
    repo.table = repo.table.__class__(capacity=num_records)

    # Limpiar archivo antes de insertar
    open(repo.store.filename, "w").close()

    # Inserción
    start_insert = time.perf_counter()
    for _ in range(num_records):
        player_id = repo.get_next_id()
        name = random_name()
        score = random.randint(0,1000)
        max_score = score + random.randint(0,1000)
        repo.save_profile(player_id, name, score, max_score)
    end_insert = time.perf_counter()
    insertion_time = end_insert - start_insert

    # Búsqueda
    search_ids = [f"player{random.randint(1, num_records)}" for _ in range(num_records)]
    start_search = time.perf_counter()
    for pid in search_ids:
        _ = repo.get_profile(pid)
    end_search = time.perf_counter()
    search_time_avg = (end_search - start_search) / len(search_ids)

    # Métricas HashTable
    collisions = getattr(repo.table, "collisions", "No implementado")
    load_factor = getattr(repo.table, "count", 0) / getattr(repo.table, "capacity", num_records)

    # Resultados
    print(f"Tiempo total de inserción: {insertion_time:.4f} s")
    print(f"Tiempo promedio de búsqueda: {search_time_avg:.6f} s")
    print(f"Número de colisiones: {collisions}")
    print(f"Factor de carga: {load_factor:.4f}")


if "--benchmark" in sys.argv:
    for size in [1000, 5000, 20000]:
        run_benchmark_for_size(size)
    sys.exit(0)


# Juego
settings = get_settings_data()

if settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((800, 600))

# Reloj para controlar la velocidad de actualización (FPS)
clock = pygame.time.Clock()

bg_original = pygame.image.load("assets/images/background.jpeg").convert()
bg = pygame.transform.scale(bg_original, screen.get_size())

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
