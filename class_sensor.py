class sensor:
    id = 0
    connections = []
    def __init__(self, id):
        self.id = id
    def import_connections(self,dir="local",start_index="id=",end_index="id="):
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


from geopy.distance import great_circle

def export_connections_to_file(id_coordinates_list,max_dist):
    N = len(id_coordinates_list)
    id_connections = []
    connections = []
    for ij in range(N):#jak zrobic zeby latwo przyporzadkowac id czujnika do id czujnikow w poblizu
        id_connections = [id_coordinates_list[ij][0],connections]
    for i in range (N-1):
        for j in range (i,N):
            if (i!=j):
                first_sensor = (id_coordinates_list[i][1], id_coordinates_list[i][2])
                second_sensor = (id_coordinates_list[j][1], id_coordinates_list[j][2])

                distance = great_circle(first_sensor, second_sensor).kilometers
                if distance < max_dist:
                    id_connections[i][1].append(id_coordinates_list[j][0])
                    print("czujnik "+str(id_coordinates_list[j][0])+" jest w pobliżu "+str(id_coordinates_list[i][0]))
                    id_connections[j][1].append(id_coordinates_list[i][0])

#dodac eksport danych do pliku
#commit test