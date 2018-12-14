import class_sensor

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


def init_sensor_list(json_list):
    from class_sensor import Sensor
    sensor_list = []
    for i in json_list[0]:
        sensor_list.append(Sensor(i['id'], i['latitude'], i['longitude']))
    print("liczba sensorow")
    print(len(sensor_list))
    print("liczba sensorow")
    # sprawdzenie czy nie ma wiecej sensorow w reszcie
    for i in json_list:
        for j in i:
            temp_id = j['id']
            boolean = False
            for k in sensor_list:
                if k.id == temp_id:
                    boolean = True
            if boolean is False:
                sensor_list.append(Sensor(j['id'], j['latitude'], j['longitude']))
    print("liczba sensorow po sprawdzeniu 4 plikow")
    print(len(sensor_list))

    # wyliczenie polaczen
    # init.init_connections(sensor_list)

    for i in sensor_list:
        i.import_connections()
        i.measurements = i.json_to_observations(json_list)
    print("zakonczono import polaczen i pomiarow")
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
