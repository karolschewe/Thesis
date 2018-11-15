class sensor:
    id = 0
    connections = []
    def __init__(self, id):
        self.id = id
    def import_connections(self,dir="siec_polaczen",start_index="id=",end_index="id="):
        if dir == "local":
            data_file = open("test.txt")
        else:
            data_file = open(dir)
        block = []
        found = False
        find = start_index+str(self.id)
        for line in data_file:
            if found:
                if line.strip().startswith(end_index): break
                block.append(line)
            else:
                if line.strip() == find:
                    found = True

        data_file.close()
        block = list(map(int, block))
        self.connections = block


#dodac eksport danych do pliku
#commit test