from class_observations import Observations
from geopy.distance import great_circle
class Sensor:
    id = -1
    latitude = -1.0
    longitude = -1.0
    connections = []
    measurements = []
    daily_pm10_maxes = []
    daily_div_maxes = []
    mean_div_pm10 = 0
    mean_div_pm10_weighted = 0
    mean_pm10 = 0

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
                        iteratorek += 1
                        is_present = True
                elif is_present == False and j == i[-1]:
                    for jj in range(24):
                        tab.append(Observations())
        return tab

    def calc_div_pm10(self,sensor_list):
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
            if denominator > 0 and i.pm10 != None and suma != 0:
                mean = (suma/denominator)
                i.set_div_pm10((((i.pm10-mean)/(mean))))
            if denominator == 0 or i.pm10 == None:
                i.set_div_pm10(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1


    def calc_mean_div_pm10(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum+=i.div_pm10
        self.mean_div_pm10 = temp_sum/len(self.measurements)

    def calc_div_pm10_weighted(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            suma_wag = 0
            denominator = len(self.connections)
            min_dist = 0.5 # uwaga!!!!!!
            for j in self.connections:
                for k in sensor_list:
                    if j == k.id:
                        if k.measurements[iteratorek].pm10 != None:
                            me = (self.latitude, self.longitude)
                            it = (k.latitude, k.longitude)
                            dist = great_circle(me, it).kilometers
                            if dist < min_dist:
                                waga = 1.0 / (min_dist * min_dist)
                                suma_wag += waga
                                suma += (k.measurements[iteratorek].pm10) * waga
                            if dist > min_dist:
                                waga = 1.0/(dist*dist)
                                suma_wag+=waga
                                suma += (k.measurements[iteratorek].pm10)*waga
                        if k.measurements[iteratorek].pm10 == None:
                            denominator -= 1
            if denominator > 0 and i.pm10 != None and suma != 0:
                mean = (suma/suma_wag)
                i.set_div_pm10_weighted((((i.pm10-mean)/(mean))))
            if denominator == 0 or i.pm10 == None:
                i.set_div_pm10(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1


    def calc_mean_div_pm10_weighted(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum += i.div_pm10_weighted
        self.mean_div_pm10_weighted = temp_sum/len(self.measurements)


    def import_mean_div_pm_10(self, dir="pm10_mean_div",start_index="id=", end_index="id="):
        data_file = open(dir, 'r')
        found = False
        find = start_index + str(self.id)
        for line in data_file:
            if found is True:
                block = line.strip()
                break
            if line.strip() == find:
                found = True


        data_file.close()
        self.mean_div_pm10 = float(block)

    def calc_mean_pm10(self):
        temp_sum = 0
        denominator = 0
        for i in self.measurements:
            if i.pm10 != None:
                if i.pm10 > 0.01:
                    temp_sum += i.pm10
                    denominator+=1
        if denominator != 0:
            self.mean_pm10 = temp_sum/denominator

    def calc_daily_maxes_pm10(self):
        from dateutil import parser
        day_list = []
        maxes_list = []
        check = parser.parse("1996-01-22T21:00:00Z")
        max = 0
        for i in self.measurements:
            dzien = (i.time_of_obs-check).days
            if dzien < 3:
                continue
            elif dzien not in day_list:
                day_list.append(dzien)
                if max == 0 and i.pm10 not in [None, 0]:
                    max = i.pm10
                elif max != 0:
                    maxes_list.append(max)
                    max = 0
            elif dzien in day_list:
                if i.pm10 != None:
                    if i.pm10 > max:
                        max = i.pm10
        self.daily_pm10_maxes = maxes_list

    def calc_daily_maxes_div(self):
        from dateutil import parser
        day_list = []
        maxes_list = []
        check = parser.parse("1996-01-22T21:00:00Z")
        max = 0
        for i in self.measurements:
            dzien = (i.time_of_obs-check).days
            if dzien < 3:
                continue
            elif dzien not in day_list:
                day_list.append(dzien)
                if max == 0 and i.div_pm10 not in [None, 0]:
                    max = i.div_pm10
                elif max != 0:
                    maxes_list.append(max)
                    max = 0
            elif dzien in day_list:
                if i.div_pm10 != None:
                    if i.div_pm10 > max:
                        max = i.div_pm10
        self.daily_div_maxes = maxes_list

