import os

class RecordStore:
    def __init__(self, filename="data.log"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                pass

    def get_all_records(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def add_record(self, record):
        """Agrega un registro y devuelve su posición en bytes"""
        with open(self.filename, "a+", encoding="utf-8") as f:
            f.seek(0, 2)  # Ir al final del archivo
            position = f.tell()
            f.write(record + "\n")
            return position

    def update_record(self, record):
        """Actualiza un registro existente según la clave"""
        key = record.split(",")[0].strip()  # Suponemos key es player_id
        updated = False
        all_records = self.get_all_records()
        new_records = []

        for r in all_records:
            parts = r.split(",")
            if parts[0].strip() == key:
                new_records.append(record)
                updated = True
            else:
                new_records.append(r)

        if not updated:
            new_records.append(record)

        with open(self.filename, "w", encoding="utf-8") as f:
            for r in new_records:
                f.write(r + "\n")
