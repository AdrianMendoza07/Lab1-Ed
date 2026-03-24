from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore
import time
import random
import string
import os


class ProfileRepository:

    def __init__(self):
        self.table = HashTable(capacity=5000)  # Ajuste para 5000 registros
        self.store = RecordStore()

    def save_profile(self, player_id, name, score, max_score):
        record = player_id + "," + name + "," + str(score) + "," + str(max_score)
        position = self.store.add_record(record)  # Guardar registro y obtener posición
        self.table.insert(player_id, position)   # Guardar ID y posición en hash

    def get_profile(self, player_id):
        position = self.table.search(player_id)

        if position is None or position == -1:
            return None
        with open(self.store.filename, "r", encoding="utf-8") as file:
            file.seek(position)
            return file.readline().strip()

    def get_next_id(self):
        try:
            with open(self.store.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if not lines:
                    return "player1"
                last_line = lines[-1].strip()
                last_id = last_line.split(",")[0]  # "playerX"
                number = int(last_id.replace("player", ""))
                return f"player{number + 1}"
        except FileNotFoundError:
            return "player1"

    def get_all_profiles(self):
        profiles = []
        try:
            with open(self.store.filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) < 4:
                        print(f"Skipping invalid line: {line}")
                        continue
                    profile = {
                        "id": parts[0],
                        "name": parts[1],
                        "score": int(parts[2]),
                        "max_score": int(parts[3])
                    }
                    profiles.append(profile)
        except FileNotFoundError:
            pass
        return profiles


def random_name(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))


def run_benchmark():
    repo = ProfileRepository()

    
    open(repo.store.filename, "w").close()

    
    start_insert = time.perf_counter()
    for _ in range(5000):
        player_id = repo.get_next_id()
        name = random_name()
        score = random.randint(0, 1000)
        max_score = score + random.randint(0, 1000)
        repo.save_profile(player_id, name, score, max_score)
    end_insert = time.perf_counter()
    insertion_time = end_insert - start_insert

   
    search_ids = [f"player{random.randint(1, 5000)}" for _ in range(1000)]
    start_search = time.perf_counter()
    for pid in search_ids:
        _ = repo.get_profile(pid)
    end_search = time.perf_counter()
    search_time_avg = (end_search - start_search) / len(search_ids)

    
    collisions = repo.table.collisions if hasattr(repo.table, "collisions") else "No implementado"
    load_factor = (repo.table.count / repo.table.capacity) if hasattr(repo.table, "count") else "No implementado"

   
    print(f"Tiempo total de inserción (5000 registros): {insertion_time:.4f} s")
    print(f"Tiempo promedio de búsqueda (1000 consultas): {search_time_avg:.6f} s")
    print(f"Número de colisiones: {collisions}")
    print(f"Factor de carga: {load_factor:.4f}")


if __name__ == "__main__":
    run_benchmark()