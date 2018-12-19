# -----funkcje inicjalizacji -----
def import_data(path = None):
    import os
    import json
    all_files_in_dir = os.listdir()
    # wyciaganie plikow z danymi -- zalozenie: koncza sie na .txt
    datafiles = []
    for i in all_files_in_dir:
        if i.endswith("txt"):
            datafiles.append(i)
            print(i)
    # wczytywanie danych ze wszystkich plikow konczacych sie na txt
    # poprawne dane sa od 9 pazdziernika 2018
    json_list = []
    for i in datafiles:
        with open(i) as json_file:
            json_list.append(json.load(json_file))
    return json_list


def init_sensor_list(json_list,import_all = False):
    from class_sensor import Sensor
    sensor_list = []
    file = open('lista_czujnikow', 'r')
    iteratorek = 0
    sensor_id = 0
    lat = 0
    long = 0
    for line in file:
        if iteratorek == 0:
            sensor_id = int(line.strip())
            iteratorek += 1
        elif iteratorek == 1:
            lat = float(line.strip())
            iteratorek+=1
        elif iteratorek == 2:
            long = float(line.strip())
            sensor_list.append(Sensor(sensor_id, lat, long))
            iteratorek += 1
        else:
            line.strip()
            iteratorek=0


    # wyliczenie polaczen
    # init.init_connections(sensor_list)

    for i in sensor_list:
        i.import_connections()
        i.measurements = i.json_to_observations(json_list)
        if import_all is True:
            i.import_mean_pm_10()
            i.import_mean_div_pm_10()
            i.import_mean_div_wei_pm_10()
            i.import_pm10_maxes()
            i.import_pm10_div_maxes()

    print("zakonczono import polaczen i pomiarow")
    return sensor_list


def init_control_group():
    from class_sensor import Sensor
    from class_observations import Observations

    sensor_list = []
    file = open('lista_czujnikow', 'r')
    iteratorek = 0
    sensor_id = 0
    lat = 0
    long = 0
    for line in file:
        if iteratorek == 0:
            sensor_id = int(line.strip())
            iteratorek += 1
        elif iteratorek == 1:
            lat = float(line.strip())
            iteratorek += 1
        elif iteratorek == 2:
            long = float(line.strip())
            sensor_list.append(Sensor(sensor_id, lat, long))
            iteratorek += 1
        else:
            line.strip()
            iteratorek = 0
    from datetime import datetime
    from datetime import timedelta
    from numpy import random
    czas = datetime.now()
    for i in sensor_list:
        for j in range(240):
            czas += timedelta(hours=1)
            i.measurements.append(Observations(datetime_string=str(czas),pm10=random.uniform(10,110)))

        i.import_connections()


    return sensor_list


# woronoj w google: voronoi diagrsm python implrmrnysyion
#jest w scipy
def init_connections(sensor_list):
    from class_id_connections import id_connections
    connections = []
    plik = open("siec_polaczen", "w")
    for i in sensor_list:
        connections.append(id_connections(i, sensor_list, 5))

    for i in connections:
        plik.write("id=" + str(i.id))
        plik.write("\n")
        for j in i.connections:
            plik.write(str(j))
            plik.write("\n")
    plik.close()


# ----- funkcje liczace -----
def calc_div(sensor_list):
    iteratorek = 0
    print("liczenie dywergencji")
    for i in sensor_list:
        i.calc_div_pm10(sensor_list)
        i.calc_mean_div_pm10()
        iteratorek += 1
        if iteratorek % 200 == 0:
            print(str(iteratorek / 20) + "%")


def calc_div_weighted(sensor_list):
    iteratorek = 0
    print("liczenie dywergencji wazonej")
    for i in sensor_list:
        i.calc_div_pm10_weighted(sensor_list)
        i.calc_mean_div_pm10_weighted()
        iteratorek += 1
        if iteratorek % 200 == 0:
            print(str(iteratorek / 20) + "%")


def calc_mean_pm10(sensor_list):
    iteratorek = 0
    print("liczenie sredniego pm10")
    for i in sensor_list:
        i.calc_mean_pm10()
        iteratorek+=1
        if iteratorek % 200 == 0:
            print(str(iteratorek/20)+"%")

def calc_coef_pm10(sensor_list):
    for i in sensor_list:
        i.calc_cor_coefs_pm10(sensor_list)


def calc_mean_maxes(sensor_list):
    for i in sensor_list:
        i.calc_mean_maxes_pm10()
        i.calc_mean_maxes_div()
