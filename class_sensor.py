from class_observations import Observations
class Sensor:
    id = -1
    latitude = -1.0
    longitude = -1.0
    connections = []
    measurements = []

    def __init__(self, id, lat, long):
        self.id = id
        self.latitude = lat
        self.longitude = long


    def import_connections(self, dir="siec_polaczen", start_index="id=", end_index="id="):
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

    def json_to_observations(self,json_all_days_list):
        tab = []
        for i in json_all_days_list:
            for j in i:
                key_list = j.keys()
                if self.id == j['id'] and 'history' in key_list:
                    meas_key_list = j['history'][0]['measurements'].keys()
                    for every_hour in j['history']:
                        tab.append(Observations(datetime_string=every_hour['fromDateTime']))


        return tab


#dodac przypadki jeżeli jest tylko czesc danych
#sprobowac to zrobic seterami
