from class_observations import Observations
from geopy.distance import great_circle
class Sensor:
    id = -1
    latitude = -1.0
    longitude = -1.0
    address = ""
    connections = []
    measurements = []
    # ---pm10---
    cor_coefs_pm10 = []  # first value is id for which coef was calculated, second is correlation coefficient, the last is p-value
    cor_coefs_pm10_div = []
    daily_pm10_maxes = []
    mean_daily_pm10_maxes = 0
    daily_div_maxes = []
    mean_daily_div_maxes = 0
    mean_div_pm10 = 0
    mean_div_pm10_weighted = 0
    mean_pm10 = 0
    # ---pm2,5---
    cor_coefs_pm2_5 = []  # first value is id for which coef was calculated, second is correlation coefficient, the last is p-value
    cor_coefs_pm2_5_div = []
    daily_pm2_5_maxes = []
    mean_daily_pm2_5_maxes = 0
    daily_div_maxes_pm2_5 = []
    mean_daily_div_maxes_pm2_5 = 0
    mean_div_pm2_5 = 0
    mean_div_pm2_5_weighted = 0
    mean_pm2_5 = 0


    def __init__(self, id, lat, long):
        self.id = id
        self.latitude = lat
        self.longitude = long

    # ----inits----
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
    def import_address(self,json_all_days_list):
        for i in json_all_days_list[0].values():
            if self.id == i['id']:
                if 'address' in i.keys() and 'locality' in i['address'].keys():
                    self.address = i['address']['locality']
        for i in json_all_days_list[-1].values():
            if self.id == i['id']:
                if 'address' in i.keys() and 'locality' in i['address'].keys():
                    self.address = i['address']['locality']

    def json_to_observations(self,json_all_days_list):
        tab = []
        iteratorek = 0
        for i in json_all_days_list:
            if self.id in i.keys():
                key_list = i[self.id].keys()
                if 'history' not in key_list:
                    for ii in range(24):
                        tab.append(Observations())
                        iteratorek += 1
                elif 'history' in key_list:
                    for every_hour in i[self.id]['history']:
                        meas_key_list = every_hour[
                            'measurements'].keys()  # musi się sprawdzac niestety co godz bo sa takie czujniki w ktorych zmienia sie z godziny na godzine
                        tab.append(Observations())
                        tab[iteratorek].set_time(every_hour['fromDateTime'])
                        if 'pm1' in meas_key_list:
                            tab[iteratorek].set_pm1(every_hour['measurements']['pm1'])
                        if 'pm25' in meas_key_list:
                            tab[iteratorek].set_pm2_5(every_hour['measurements']['pm25'])
                        if 'pm10' in meas_key_list:
                            tab[iteratorek].set_pm10(every_hour['measurements']['pm10'])
                        iteratorek += 1
            else:
                for jj in range(24):
                    tab.append(Observations())

        return tab

    # -----calculations-----

    def calc_div_pm10(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            denominator = len(self.connections)
            for j in self.connections:
                if sensor_list[j].measurements[iteratorek].pm10 != None:
                    suma += sensor_list[j].measurements[iteratorek].pm10
                if sensor_list[j].measurements[iteratorek].pm10 == None:
                    denominator -= 1
            if denominator > 0 and i.pm10 != None and suma != 0:
                mean = (suma/denominator)
                i.set_div_pm10((((i.pm10-mean)/(mean))))
            if denominator == 0 or i.pm10 == None:
                i.set_div_pm10(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1

    def calc_div_pm2_5(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            denominator = len(self.connections)
            for j in self.connections:
                if sensor_list[j].measurements[iteratorek].pm2_5 != None:
                    suma += sensor_list[j].measurements[iteratorek].pm2_5
                if sensor_list[j].measurements[iteratorek].pm2_5 == None:
                    denominator -= 1
            if denominator > 0 and i.pm2_5 != None and suma != 0:
                mean = (suma/denominator)
                i.set_div_pm2_5((((i.pm2_5-mean)/(mean))))
            if denominator == 0 or i.pm2_5 == None:
                i.set_div_pm2_5(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1

    def calc_mean_div_pm10(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum+=i.div_pm10
        self.mean_div_pm10 = temp_sum/len(self.measurements)

    def calc_mean_div_pm2_5(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum+=i.div_pm2_5
        self.mean_div_pm2_5 = temp_sum/len(self.measurements)

    def calc_div_pm10_weighted(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            suma_wag = 0
            denominator = len(self.connections)
            min_dist = 0.5 # uwaga!!!!!!
            for j in self.connections:
                if sensor_list[j].measurements[iteratorek].pm10 != None:
                    me = (self.latitude, self.longitude)
                    it = (sensor_list[j].latitude, sensor_list[j].longitude)
                    dist = great_circle(me, it).kilometers
                    if dist < min_dist:
                        waga = 1.0 / (min_dist * min_dist)
                        suma_wag += waga
                        suma += (sensor_list[j].measurements[iteratorek].pm10) * waga
                    if dist > min_dist:
                        waga = 1.0 / (dist * dist)
                        suma_wag += waga
                        suma += (sensor_list[j].measurements[iteratorek].pm10) * waga
                if sensor_list[j].measurements[iteratorek].pm10 == None:
                    denominator -= 1
            if denominator > 0 and i.pm10 != None and suma != 0:
                mean = (suma/suma_wag)
                i.set_div_pm10_weighted((((i.pm10-mean)/(mean))))
            if denominator == 0 or i.pm10 == None:
                i.set_div_pm10(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1

    def calc_div_pm2_5_weighted(self,sensor_list):
        iteratorek = 0
        for i in self.measurements:
            suma = 0
            suma_wag = 0
            denominator = len(self.connections)
            min_dist = 0.5 # uwaga!!!!!!
            for j in self.connections:
                if sensor_list[j].measurements[iteratorek].pm2_5 != None:
                    me = (self.latitude, self.longitude)
                    it = (sensor_list[j].latitude, sensor_list[j].longitude)
                    dist = great_circle(me, it).kilometers
                    if dist < min_dist:
                        waga = 1.0 / (min_dist * min_dist)
                        suma_wag += waga
                        suma += (sensor_list[j].measurements[iteratorek].pm2_5) * waga
                    if dist > min_dist:
                        waga = 1.0 / (dist * dist)
                        suma_wag += waga
                        suma += (sensor_list[j].measurements[iteratorek].pm2_5) * waga
                if sensor_list[j].measurements[iteratorek].pm2_5 == None:
                    denominator -= 1
            if denominator > 0 and i.pm2_5 != None and suma != 0:
                mean = (suma/suma_wag)
                i.set_div_pm2_5_weighted((((i.pm2_5-mean)/(mean))))
            if denominator == 0 or i.pm2_5 == None:
                i.set_div_pm2_5_weighted(0)
            if denominator < 0:
                print("blad w skrypcie")
            iteratorek += 1

    def calc_mean_div_pm10_weighted(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum += i.div_pm10_weighted
        self.mean_div_pm10_weighted = temp_sum/len(self.measurements)

    def calc_mean_div_pm2_5_weighted(self):
        temp_sum = 0
        for i in self.measurements:
            temp_sum += i.div_pm2_5_weighted
        self.mean_div_pm2_5_weighted = temp_sum/len(self.measurements)

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

    def calc_mean_pm2_5(self):
        temp_sum = 0
        denominator = 0
        for i in self.measurements:
            if i.pm2_5 != None:
                if i.pm2_5 > 0.01:
                    temp_sum += i.pm2_5
                    denominator+=1
        if denominator != 0:
            self.mean_pm2_5 = temp_sum/denominator

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

    def calc_daily_maxes_pm2_5(self):
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
                if max == 0 and i.pm2_5 not in [None, 0]:
                    max = i.pm2_5
                elif max != 0:
                    maxes_list.append(max)
                    max = 0
            elif dzien in day_list:
                if i.pm2_5 != None:
                    if i.pm2_5 > max:
                        max = i.pm2_5
        self.daily_pm2_5_maxes = maxes_list

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

    def calc_daily_maxes_div_pm2_5(self):
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
                if max == 0 and i.div_pm2_5 not in [None, 0]:
                    max = i.div_pm2_5
                elif max != 0:
                    maxes_list.append(max)
                    max = 0
            elif dzien in day_list:
                if i.div_pm2_5 != None:
                    if i.div_pm2_5 > max:
                        max = i.div_pm2_5
        self.daily_div_maxes_pm2_5 = maxes_list

    def calc_cor_coefs_pm10(self,sensor_list):
        from scipy.stats.stats import pearsonr
        id_coefs_to_set = []
        my_obs = []
        my_obs.append(0.1)
        const = 0
        for m in self.measurements:
            if const != 0:
                if m.pm10 == None:
                    const += 1
                    continue
                else:
                    for n in range(const):
                        my_obs.append((m.pm10+my_obs[-1])/const)
                    my_obs.append(m.pm10)
                    const = 0
            else:
                if m.pm10 == None:
                    const += 1
                    continue
                else:
                    my_obs.append(m.pm10)
        if const!= 0:
            for g in range(const):
                my_obs.append(0)
            const = 0

        sasiedzi = self.connections
        for i in sasiedzi:
            if i in sensor_list.keys():
                its_obs = []
                its_obs.append(0.1)
                for m in sensor_list[i].measurements:
                    if const != 0:
                        if m.pm10 == None:
                            const += 1
                            continue
                        else:
                            for n in range(const):
                                its_obs.append((m.pm10 + its_obs[-1]) / const)
                            its_obs.append(m.pm10)
                            const = 0
                    else:
                        if m.pm10 == None:
                            const += 1
                            continue
                        else:
                            its_obs.append(m.pm10)
                if const != 0:
                    for q in range(const):
                        its_obs.append(0)
                    const = 0

                calculated = pearsonr(my_obs, its_obs)
                coefs_to_append = [sensor_list[i].id, calculated[0], calculated[1]]
                id_coefs_to_set.append(coefs_to_append)

        self.cor_coefs_pm10 = id_coefs_to_set

    def calc_cor_coefs_pm2_5(self,sensor_list):
        from scipy.stats.stats import pearsonr
        id_coefs_to_set = []
        my_obs = []
        my_obs.append(0.1)
        const = 0
        for m in self.measurements:
            if const != 0:
                if m.pm2_5 == None:
                    const += 1
                    continue
                else:
                    for n in range(const):
                        my_obs.append((m.pm2_5+my_obs[-1])/const)
                    my_obs.append(m.pm2_5)
                    const = 0
            else:
                if m.pm2_5 == None:
                    const += 1
                    continue
                else:
                    my_obs.append(m.pm2_5)
        if const!= 0:
            for g in range(const):
                my_obs.append(0)
            const = 0

        sasiedzi = self.connections
        for i in sasiedzi:
            if i in sensor_list.keys():
                its_obs = []
                its_obs.append(0.1)
                for m in sensor_list[i].measurements:
                    if const != 0:
                        if m.pm2_5 == None:
                            const += 1
                            continue
                        else:
                            for n in range(const):
                                its_obs.append((m.pm2_5 + its_obs[-1]) / const)
                            its_obs.append(m.pm2_5)
                            const = 0
                    else:
                        if m.pm2_5 == None:
                            const += 1
                            continue
                        else:
                            its_obs.append(m.pm2_5)
                if const != 0:
                    for q in range(const):
                        its_obs.append(0)
                    const = 0

                calculated = pearsonr(my_obs, its_obs)
                coefs_to_append = [sensor_list[i].id, calculated[0], calculated[1]]
                id_coefs_to_set.append(coefs_to_append)

        self.cor_coefs_pm2_5 = id_coefs_to_set

    def calc_cor_coefs_pm10_div(self,sensor_list):
        from scipy.stats.stats import pearsonr
        id_coefs_to_set = []
        my_obs = []
        my_obs.append(0.1)
        const = 0
        for m in self.measurements:
            if const != 0:
                if m.div_pm10 == None:
                    const += 1
                    continue
                else:
                    for n in range(const):
                        my_obs.append((m.div_pm10+my_obs[-1])/const)
                    my_obs.append(m.div_pm10)
                    const = 0
            else:
                if m.div_pm10 == None:
                    const += 1
                    continue
                else:
                    my_obs.append(m.div_pm10)
        if const!= 0:
            for i in range(const):
                my_obs.append(0)
            const = 0


        for i in self.connections:
            its_obs = []
            its_obs.append(0.1)
            for m in sensor_list[i].measurements:
                if const != 0:
                    if m.div_pm10 == None:
                        const += 1
                        continue
                    else:
                        for n in range(const):
                            its_obs.append((m.div_pm10 + its_obs[-1]) / const)
                        its_obs.append(m.div_pm10)
                        const = 0
                else:
                    if m.div_pm10 == None:
                        const += 1
                        continue
                    else:
                        its_obs.append(m.div_pm10)
            if const != 0:
                for q in range(const):
                    its_obs.append(0)
                const = 0

            calculated = pearsonr(my_obs, its_obs)
            coefs_to_append = [sensor_list[i].id, calculated[0], calculated[1]]
            id_coefs_to_set.append(coefs_to_append)


        self.cor_coefs_pm10_div = id_coefs_to_set

    def calc_cor_coefs_pm2_5_div(self,sensor_list):
        from scipy.stats.stats import pearsonr
        id_coefs_to_set = []
        my_obs = []
        my_obs.append(0.1)
        const = 0
        for m in self.measurements:
            if const != 0:
                if m.div_pm2_5 == None:
                    const += 1
                    continue
                else:
                    for n in range(const):
                        my_obs.append((m.div_pm2_5+my_obs[-1])/const)
                    my_obs.append(m.div_pm2_5)
                    const = 0
            else:
                if m.div_pm2_5 == None:
                    const += 1
                    continue
                else:
                    my_obs.append(m.div_pm2_5)
        if const!= 0:
            for i in range(const):
                my_obs.append(0)
            const = 0


        for i in self.connections:
            its_obs = []
            its_obs.append(0.1)
            for m in sensor_list[i].measurements:
                if const != 0:
                    if m.div_pm2_5 == None:
                        const += 1
                        continue
                    else:
                        for n in range(const):
                            its_obs.append((m.div_pm2_5 + its_obs[-1]) / const)
                        its_obs.append(m.div_pm2_5)
                        const = 0
                else:
                    if m.div_pm2_5 == None:
                        const += 1
                        continue
                    else:
                        its_obs.append(m.div_pm2_5)
            if const != 0:
                for q in range(const):
                    its_obs.append(0)
                const = 0

            calculated = pearsonr(my_obs, its_obs)
            coefs_to_append = [sensor_list[i].id, calculated[0], calculated[1]]
            id_coefs_to_set.append(coefs_to_append)


        self.cor_coefs_pm2_5_div = id_coefs_to_set

    def calc_mean_maxes_pm10(self):
        suma = 0
        for i in self.daily_pm10_maxes:
            suma += i
        if len(self.daily_pm10_maxes) != 0:
            self.mean_daily_pm10_maxes = suma/len(self.daily_pm10_maxes)

    def calc_mean_maxes_pm2_5(self):
        suma = 0
        for i in self.daily_pm2_5_maxes:
            suma += i
        if len(self.daily_pm2_5_maxes) != 0:
            self.mean_daily_pm2_5_maxes = suma/len(self.daily_pm2_5_maxes)

    def calc_mean_maxes_div(self):
        suma = 0.0
        for i in self.daily_div_maxes:
            suma += i
        if len(self.daily_div_maxes) != 0:
            self.mean_daily_div_maxes = float(suma)/float(len(self.daily_div_maxes))

    def calc_mean_maxes_div_pm2_5(self):
        suma = 0.0
        for i in self.daily_div_maxes_pm2_5:
            suma += i
        if len(self.daily_div_maxes_pm2_5) != 0:
            self.mean_daily_div_maxes_pm2_5 = float(suma)/float(len(self.daily_div_maxes_pm2_5))




    # ----imports----
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


    def import_mean_div_wei_pm_10(self, dir="pm10_mean_wei_div",start_index="id=", end_index="id="):
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
        self.mean_div_pm10_weighted = float(block)


    def import_mean_pm_10(self, dir="pm10_mean",start_index="id=", end_index="id="):
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
        self.mean_pm10 = float(block)


    def import_pm10_maxes(self, dir="pm10_daily_maxes", start_index="id=", end_index="id="):
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
        block = list(map(float, block))
        self.daily_pm10_maxes = block


    def import_pm10_div_maxes(self, dir="div_daily_maxes", start_index="id=", end_index="id="):
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
        block = list(map(float, block))
        self.daily_div_maxes = block