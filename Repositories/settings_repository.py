import json
from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:

    def __init__(self):
        self.table = HashTable()
        self.store = RecordStore()

        self._rebuild_index()

    def save_settings(self, key, volume, difficulty):
        volume = max(0, min(100, volume))
        data = {
            "volume": volume,
            "difficulty": difficulty
        }

        record = json.dumps({
            "type": "settings",
            "key": key,
            "data": data
        })

        position = self.store.append(record)
        self.table.insert(key, position)

    def get_settings(self, key):
        position = self.table.search(key)

        if position == -1:
            return None

        with open("data.log", "r") as file:
            file.seek(position)
            line = file.readline()

        return json.loads(line)

    def _rebuild_index(self):
        try:
            with open("data.log", "r") as file:
                while True:
                    offset = file.tell()   

                    line = file.readline()
                    if not line:
                        break

                    record = json.loads(line)
                    key = record["key"]

                    self.table.insert(key, offset)

        except FileNotFoundError:
            pass


def get_difficulty():
    repo = SettingsRepository()
    data = repo.get_settings("game_settings")

    if data:
        return data["data"]["difficulty"]

    return "Normal"