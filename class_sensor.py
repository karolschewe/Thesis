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
            data_file = open(dir,'r')
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
        iteratorek = 0
        for i in json_all_days_list:
            is_present = False
            for j in i:
                key_list = j.keys()
                if self.id == j['id'] and 'history' not in key_list:
                    for ii in range(24):
                        tab.append(Observations())
                        iteratorek+=1
                        is_present = True
                elif self.id == j['id'] and 'history' in key_list:
                    for every_hour in j['history']:
                        meas_key_list = every_hour['measurements'].keys()#musi się sprawdzac niestety co godz bo sa takie czujniki w ktorych zmienia sie z godziny na godzine
                        tab.append(Observations())
                        tab[iteratorek].set_time(every_hour['fromDateTime'])
                        if 'pm1' in meas_key_list:
                            tab[iteratorek].set_pm1(every_hour['measurements']['pm1'])
                        if 'pm25' in meas_key_list:
                            tab[iteratorek].set_pm2_5(every_hour['measurements']['pm25'])
                        if 'pm10' in meas_key_list:
                            tab[iteratorek].set_pm10(every_hour['measurements']['pm10'])
                        if 'humidity' in meas_key_list:
                            tab[iteratorek].set_humidity(every_hour['measurements']['humidity'])
                        if 'pressure' in meas_key_list:
                            tab[iteratorek].set_pressure(every_hour['measurements']['pressure'])
                        if 'pollutionLevel' in meas_key_list:
                            tab[iteratorek].set_pollution_stage(every_hour['measurements']['pollutionLevel'])
                        if 'airQualityIndex' in meas_key_list:
                            tab[iteratorek].set_quality_index(every_hour['measurements']['airQualityIndex'])
                        if 'temperature' in meas_key_list:
                            tab[iteratorek].set_temperature(every_hour['measurements']['temperature'])
                        iteratorek += 1
                        is_present = True
                elif is_present == False and j == i[-1]:
                    for jj in range(24):
                        tab.append(Observations())






        return tab

    def calc_var_pm10(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            denominator = len(self.connections)
            for j in self.connections:
                for k in sensor_list:
                    if j == k.id:
                        if k.measurements[iteratorek].pm10 != None:
                            suma += k.measurements[iteratorek].pm10
                        if k.measurements[iteratorek].pm10 == None:
                            denominator -= 1
            if denominator > 0 and i.pm10 != None:
                i.set_variance((suma/denominator)-i.pm10)
            if denominator == 0 or i.pm10 == None:
                i.set_variance(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1


#dodac przypadki reszte na seterach z ifami

