from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:
    def __init__(self):
        self.store = RecordStore()
        self.table = {}
        self._rebuild_index()

    def _rebuild_index(self):
        """Reconstruye el índice de settings desde el store"""
        self.table.clear()
        records = self.store.get_all_records() if hasattr(self.store, "get_all_records") else []

        for record in records:
            if not record.strip():
                continue
            parts = record.split(",")
            if len(parts) < 9:
                print(f"WARNING: registro inválido ignorado -> {record}")
                continue
            key = parts[5].strip()  
            self.table[key] = record

    def get_settings(self, key):
        record = self.table.get(key)
        if not record:
            return None
        parts = record.split(",")
        try:
            return {
                "data": {
                    "volume": int(parts[6]),
                    "difficulty": parts[7],
                    "fullscreen": parts[8].lower() == "true"
                }
            }
        except IndexError:
            print(f"WARNING: datos incompletos en registro -> {record}")
            return None

    def save_settings(self, key, volume, difficulty, fullscreen):
        existing = self.table.get(key)
        if existing:
            parts = existing.split(",")
            parts[6] = str(volume)
            parts[7] = difficulty
            parts[8] = str(fullscreen)
            record = ",".join(parts)
            if hasattr(self.store, "update_record"):
                self.store.update_record(record)
            else:
                print("WARNING: RecordStore no tiene update_record")
        else:
            record = f"player1,Nataly,200,1200,settings,{key},{volume},{difficulty},{fullscreen}"
            if hasattr(self.store, "add_record"):
                self.store.add_record(record)
            else:
                print("WARNING: RecordStore no tiene add_record")

        self._rebuild_index()


def get_settings_data():
    """Retorna la configuración 'game_settings'"""
    repo = SettingsRepository()
    data = repo.get_settings("game_settings")
    if data is None:
        return {"volume": 50, "difficulty": "Easy", "fullscreen": False}
    return {
        "volume": data["data"]["volume"],
        "difficulty": data["data"]["difficulty"],
        "fullscreen": data["data"]["fullscreen"]
    }