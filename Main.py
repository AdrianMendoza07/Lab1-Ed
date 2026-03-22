import pygame
from StartMenu import runStartMenu
from SettingsMenu import runSettingsMenu
from Repositories.settings_repository import get_settings_data

pygame.init()

settings = get_settings_data()

if settings["fullscreen"]:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((800, 600))

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

    elif state == 2:
        result = runSettingsMenu(screen, events, bg)

        if isinstance(result, tuple):
            state, screen, bg = result
        else:
            state = result

    clock.tick(60)

pygame.quit()


