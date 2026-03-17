import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu

pygame.init()

screen = pygame.display.set_mode((0, 0))

clock = pygame.time.Clock()



running = True
state  = 1

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or state == 0:
            running = False
    if state == 1:
        state = runStartMenu(screen, events)        
    if state == 2:
        state = runSettingsMenu(screen, events)   
        
    clock.tick(60)    
        

pygame.quit()
from Repositories.Profile_repository import ProfileRepository

repo = ProfileRepository()
repo.save_profile("player1", "Nataly", 200, 1200)
repo.save_profile("player2", "Mario", 150, 800)
print(repo.get_profile("player1"))
