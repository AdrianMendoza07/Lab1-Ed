class RecordStore:
    def __init__(self, filename="data.log"):
        self.filename = filename

    def append(self, record):
        file = open(self.filename, "a")
        position = file.tell()
        file.write(record + "\n")
        file.close()
        return position