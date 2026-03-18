from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore


class ProfileRepository:

    def __init__(self):
        self.table = HashTable()
        self.store = RecordStore()

    def save_profile(self, player_id, name, score, max_score):
        record = player_id + "," + name + "," + str(score) + "," + str(max_score)
        position = self.store.append(record)
        self.table.insert(player_id, position)

    def get_profile(self, player_id):
        position = self.table.search(player_id)
        if position == -1:
            return None
        file = open("data.log", "r")
        file.seek(position)
        line = file.readline()
        file.close()
        return line
    
    