import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from Repositories.Profile_repository import ProfileRepository



pygame.init()

screen = pygame.display.set_mode((0, 0))

clock = pygame.time.Clock()
bg = pygame.image.load("assets/images/background.jpeg").convert()
bg = pygame.transform.scale(bg, screen.get_size())



running = True
state  = 1

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or state == 0:
            running = False
    if state == 1:
        state = runStartMenu(screen, events, bg)        
    if state == 2:
        state = runSettingsMenu(screen, events, bg)   
        
    clock.tick(60)    
        

pygame.quit()

