import pygame
from Enemy import Enemy
from Obstacle import Obstacle

def runGame(screen, events, bg, player):
    
    WIDTH, HEIGHT = screen.get_size()

    # 🔹 Inicialización segura
    if not hasattr(runGame, "initialized"):
        runGame.obstacles = []
        runGame.spawn_timer = pygame.time.get_ticks()

        try:
            runGame.obstacle_image = pygame.image.load(
                "assets/images/obstacle/obstaculo1.png"
            ).convert_alpha()
        except:
            print("❌ ERROR: No se encontró la imagen del obstáculo")
            return 0

        runGame.initialized = True

    obstacles = runGame.obstacles

    # 🎨 Fondo
    screen.blit(bg, (0, 0))

    # 🔹 Eventos (CORRECTO)
    for event in events:
        if event.type == pygame.QUIT:
            return 0

    # 🔥 SPAWN CONTROLADO
    current_time = pygame.time.get_ticks()

    if current_time - runGame.spawn_timer > 1500:
        obstacle = Obstacle(
            x=WIDTH,
            ground_y=HEIGHT - 100,
            image=runGame.obstacle_image,
            speed=8
        )
        obstacles.append(obstacle)
        runGame.spawn_timer = current_time

    # 🔄 Update
    for o in obstacles:
        o.update()

    # 🧹 Limpiar
    runGame.obstacles = [o for o in obstacles if not o.is_off_screen()]
    obstacles = runGame.obstacles

    # 🎯 Colisión
    for o in obstacles:
        if o.collide(player):
            print("💥 Colisión detectada")
            return 1

    # 🖌 Dibujar
    for o in obstacles:
        o.draw(screen)

    return 6
