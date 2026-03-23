from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:

    def __init__(self):
        self.table = HashTable()
        self.store = RecordStore()

        self._rebuild_index()

    def save_settings(self, key, volume, difficulty, fullscreen):
        volume = max(0, min(100, volume))

        # Formato CSV
        record = f"settings,{key},{volume},{difficulty},{fullscreen}\n"

        position = self.store.append(record)
        self.table.insert(key, position)

    def get_settings(self, key):
        position = self.table.search(key)

        if position == -1:
            return None

        with open("data.log", "r") as file:
            file.seek(position)
            line = file.readline().strip()

        # Convertir CSV → diccionario
        parts = line.split(",")

        return {
            "type": parts[0],
            "key": parts[1],
            "data": {
                "volume": int(parts[2]),
                "difficulty": parts[3],
                "fullscreen": parts[4] == "True"
            }
        }

    def _rebuild_index(self):
        try:
            with open("data.log", "r") as file:
                while True:
                    offset = file.tell()

                    line = file.readline()
                    if not line:
                        break

                    parts = line.strip().split(",")
                    key = parts[1]

                    self.table.insert(key, offset)

        except FileNotFoundError:
            pass


def get_settings_data():
    repo = SettingsRepository()
    data = repo.get_settings("game_settings")

    if data:
        return data["data"]

    return {
        "volume": 50,
        "difficulty": "Easy",
        "fullscreen": False
    }