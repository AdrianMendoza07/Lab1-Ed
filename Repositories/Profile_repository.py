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
    
    def update_max_score(self, player_id, new_score):
        try:
            with open("data.log", "r") as file:
                lines = file.readlines()

            updated_lines = []

            for line in lines:
                parts = line.strip().split(",")

                if len(parts) < 4:
                    updated_lines.append(line)
                    continue

                if parts[0] == player_id:
                    try:
                        current_max = int(parts[3])
                    except:
                        current_max = 0

                    if new_score > current_max:
                        print(f"Actualizando {player_id}: {current_max} -> {new_score}")
                        parts[3] = str(new_score)

                    line = ",".join(parts) + "\n"

                updated_lines.append(line)

            with open("data.log", "w") as file:
                file.writelines(updated_lines)

        except Exception as e:
            print("Error actualizando score:", e)

    def get_profile(self, player_id):
        position = self.table.search(player_id)

        if position is None or position == -1:
            return None

        with open("data.log", "r") as file:
            file.seek(position)
            line = file.readline()

        parts = line.strip().split(",")

        return {
            "id": parts[0],
            "name": parts[1],
            "score": int(parts[2]),
            "max_score": int(parts[3])
        }
    
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
        
    