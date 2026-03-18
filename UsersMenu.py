from Repositories.Profile_repository import ProfileRepository
import pygame
import sys
from Button import Button

repo = ProfileRepository()
repo.save_profile("player1", "Nataly", 200, 1200)
repo.save_profile("player2", "Mario", 150, 800)
print(repo.get_profile("player1"))


def runUsersMenu(screen, events, bg):
    WIDTH, HEIGH = screen.get_size()
    
    