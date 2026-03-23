from Persistence.Storage.Record_store import RecordStore

class SettingsRepository:
    def __init__(self):
        self.store = RecordStore()
        self.table = {}  # índice interno
        self._rebuild_index()

    def _rebuild_index(self):
        """Reconstruye el índice interno de los registros de manera segura."""

        self.table.clear()

        # Obtener registros de manera segura
        if hasattr(self.store, "records"):
            records = self.store.records
        elif hasattr(self.store, "get_all_records"):
            records = self.store.get_all_records()
        else:
            records = []
            print("WARNING: RecordStore no tiene records ni get_all_records")

        for record in records:
            if not record.strip():
                continue
            parts = record.split(",")
            if len(parts) < 2:
                print(f"WARNING: registro inválido ignorado -> {record}")
                continue
            key = parts[1].strip()
            self.table[key] = record

    # -------------------
    # Métodos de acceso
    # -------------------
    def get_settings(self, key):
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
        record = f"user,{key},{volume},{difficulty},{fullscreen}"
        if hasattr(self.store, "add_record"):
            self.store.add_record(record)
        else:
            print("WARNING: RecordStore no tiene add_record")
        self._rebuild_index()