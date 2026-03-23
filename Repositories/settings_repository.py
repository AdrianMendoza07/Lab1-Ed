from Persistence.Hash_table import HashTable
from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:
    def __init__(self):
        self.store = RecordStore()
        self.table = {}  
        self._rebuild_index()

    def _rebuild_index(self):
        """Reconstruye el índice interno de los registros de manera segura."""
        self.table.clear()
        for record in self.store.records:
            if not record.strip():
                continue

            parts = record.split(",")
            if len(parts) < 2:
                print(f"WARNING: registro inválido ignorado -> {record}")
                continue

            key = parts[1].strip()
            self.table[key] = record 


    def get_settings(self, key):
        """Retorna los datos del registro para una key, en formato dict"""
        record = self.table.get(key)
        if not record:
            return None

        parts = record.split(",")
        try:
            return {
                "data": {
                    "volume": int(parts[2]),
                    "difficulty": parts[3],
                    "fullscreen": parts[4].lower() == "true"
                }
            }
        except IndexError:
            return None

    def save_settings(self, key, volume, difficulty, fullscreen):
        """Guarda o actualiza la configuración en RecordStore"""
        record = f"user,{key},{volume},{difficulty},{fullscreen}"
        self.store.add_record(record)
        self._rebuild_index()