from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore


class ProfileRepository:

    def __init__(self):
        self.table = HashTable()
        self.store = RecordStore()

    def save_profile(self, player_id, name, score, max_score):
        record = player_id + "," + name + "," + str(score) + "," + str(max_score)
        position = self.store.add_record(record)
        self.table.insert(player_id, position)
    
    def set_max_score(self, value):
        self.max_score = value

    def get_profile(self, player_id):
        position = self.table.search(player_id)
        if position == -1:
            return None
        file = open("data.log", "r")
        file.seek(position)
        line = file.readline()
        file.close()
        return line
    
    def get_next_id(self):
        try:
            with open("data.log", "r") as file:
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
            with open("data.log", "r") as file:
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
        
    