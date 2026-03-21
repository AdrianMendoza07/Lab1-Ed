import json
from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:

    def __init__(self):
        self.table = HashTable()
        self.store = RecordStore()

    def save_settings(self, key, volume, difficulty, fullscreen):
        data = {
            "volume": volume,
            "difficulty": difficulty,
            "fullscreen": fullscreen
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

