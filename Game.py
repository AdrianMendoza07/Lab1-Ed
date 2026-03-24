from Repositories.Profile_repository import ProfileRepository
import pygame
import random
from Enemy import Enemy
from Player import Player
from Obstacle import Obstacle

def runGame(screen, events, bg, player_data):

    clock = pygame.time.Clock()
    WIDTH, HEIGHT = screen.get_size()

    ground_y = HEIGHT - 300
    player = Player(100, ground_y)    
    enemy = Enemy()
    obstacles = []

    obstacle_images = []
    for i in range(1, 4):
        img = pygame.image.load(f"assets/images/obstacle/obstaculo{i}.png").convert_alpha()
        obstacle_images.append(img)

    spawn_timer = 0
    spawn_delay = random.randint(800, 1800)
    running = True
    
    score = 0
    score_timer = 0
    font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 40)
    
    paused = False
    pause_font = pygame.font.Font("assets/fonts/Orbitron-Bold.ttf", 55)

    
    while running:

        dt = clock.tick(60)
        score_timer += dt

        if score_timer >= 500:  # cada 0.5 segundos
            score += 10
            score_timer = 0 

        # -------- EVENTS --------
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.jump()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  
                    
        if paused:
            pause_text = pause_font.render(
                "Juego pausado - ESC continuar | Q salir",
                True,
                (255, 255, 255)
            )

            rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            screen.blit(bg, (0, 0))
            screen.blit(pause_text, rect)
            pygame.display.flip()

            # detectar salida con Q
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return 1

            continue      

        # -------- SPAWN --------
        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            spawn_timer = 0

            spawn_delay = random.randint(800, 1800)  # 🔥 nuevo delay cada vez

            img = random.choice(obstacle_images)
            obstacle = Obstacle(WIDTH, ground_y, img, speed=6)
            obstacles.append(obstacle)

        # -------- UPDATE --------
        player.update(obstacles, [enemy])

        dead = enemy.update(player.rect, obstacles)
        if dead:
            player.alive = False

        for obs in obstacles:
            obs.update()

        obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

        # -------- GAME OVER --------
        if not player.alive:
            repo = ProfileRepository()
            print("Guardando score:", player_data["id"], score)  # DEBUG
            repo.update_max_score(player_data["id"], score)
            return 1

        # -------- DRAW --------
        screen.blit(bg, (0, 0))

        score_text = font.render(f"Puntos: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 300, 20))

        player.draw(screen)
        enemy.draw(screen)

        for obs in obstacles:
            obs.draw(screen)

        pygame.display.flip()