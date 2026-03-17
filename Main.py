from Repositories.Profile_repository import ProfileRepository

repo = ProfileRepository()
repo.save_profile("player1", "Nataly", 200, 1200)
repo.save_profile("player2", "Mario", 150, 800)
print(repo.get_profile("player1"))