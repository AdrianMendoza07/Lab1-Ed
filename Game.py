import pygame
from Enemy import Enemy

def runGame(screen, event, bg, player):
    
    WIDTH, HEIGHT = screen.get_size()
    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN

    # Re-inicializar si cambia tamaño
    if not hasattr(runGame, "last_size") or runGame.last_size != (WIDTH, HEIGHT):
        runGame.initialized = False
        runGame.last_size = (WIDTH, HEIGHT)

    if not hasattr(runGame, "initialized") or runGame.initialized == False:
        runGame.initialized = True

        center_x = WIDTH // 2

        
        
        runGame.enemy = Enemy()
        
    screen.blit(bg, (0, 0))
    
    enemy=runGame.enemy
    
    dead = enemy.update(player.rect, obstacles)
    
    if dead:
        print("GAME OVER")
        player.save
        
    
    for event in events:
        if event.type == pygame.QUIT:
            return 0
    
    return 6    
    
