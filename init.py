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
    json_list_dict = []
    for ii in json_list:
        temp_dict = {}
        for jj in ii:
            temp_dict[jj['id']] = jj
        json_list_dict.append(temp_dict)

    return json_list_dict


def init_sensor_list(json_list,import_all = False,random=False,custom_list = False,custom_conn=False):
    from class_sensor import Sensor
    sensor_list = {}
    # ---tworzenie lsity czujnikow na podstawie pliku z listą id---
    if custom_list is False:
        file = open('lista_czujnikow', 'r')
    else:
        file = open('ciekawe_id')
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
            sensor_list[sensor_id] = Sensor(sensor_id,lat,long)
            iteratorek += 1
        else:
            line.strip()
            iteratorek=0



    # wczytanie polaczen z pliku
    zmienna = 0
    lista_id = []
    print("import połączeń i pomiarów")
    for i in sensor_list.values():
        if zmienna % 200 == 0:
            print(str(zmienna / 20) + "%")
        if random == False and custom_conn == True:
            i.import_connections(dir="custom_connections")
        elif random == False and custom_conn == False:
            i.import_connections()
        else:
            from random import sample
            i.connections = (sample(sensor_list.keys(),10))

        i.measurements = i.json_to_observations(json_list)
        zmienna += 1
        if import_all is True:
            #i.import_mean_pm_10()
            #i.import_mean_div_pm_10()
            #i.import_mean_div_wei_pm_10()
            #i.import_pm10_maxes()
            #i.import_pm10_div_maxes()
            i.import_address(json_list)

    print("zakonczono import polaczen i pomiarow")
    return sensor_list


# woronoj w google: voronoi diagrsm python implrmrnysyion
#jest w scipy
def init_connections(sensor_list,custom=False):#wyliczanie i export polaczen do pliku
    from class_id_connections import id_connections
    connections = []
    if custom is False:
        plik = open("siec_polaczen", "w")
    else:
        plik = open("custom_connections", "w")
    for i in sensor_list.values():
        connections.append(id_connections(i, sensor_list, 5))

    for i in connections:
        plik.write("id=" + str(i.id))
        plik.write("\n")
        for j in i.connections:
            plik.write(str(j))
            plik.write("\n")
    plik.close()


# ----- funkcje liczace -----
def calc_div(sensor_list, PM = "pm10"):
    iteratorek = 0
    if PM == "pm10":
        print("---liczenie dywergencji pm10---")
        for i in sensor_list.values():
            i.calc_div_pm10(sensor_list)
            i.calc_mean_div_pm10()
            iteratorek += 1
            if iteratorek % 200 == 0:
                print(str(iteratorek / 20) + "%")
    else:
        print("---liczenie dywergencji pm2,5---")
        for i in sensor_list.values():
            i.calc_div_pm2_5(sensor_list)
            i.calc_mean_div_pm2_5()
            iteratorek += 1
            if iteratorek % 200 == 0:
                print(str(iteratorek / 20) + "%")

def calc_div_weighted(sensor_list, PM = "pm10"):
    iteratorek = 0
    if PM == "pm10":
        print("--PM10--liczenie dywergencji wazonej--PM10--")
    else:
        print("--PM2,5--liczenie dywergencji wazonej--PM2,5--")
    for i in sensor_list.values():
        if PM == "pm10":
            i.calc_div_pm10_weighted(sensor_list)
            i.calc_mean_div_pm10_weighted()
        else:
            i.calc_div_pm2_5_weighted(sensor_list)
            i.calc_mean_div_pm2_5_weighted()
        iteratorek += 1
        if iteratorek % 200 == 0:
            print(str(iteratorek / 20) + "%")


def calc_mean_pm(sensor_list,PM="pm10"):
    iteratorek = 0
    if PM == "pm10":
        print("liczenie sredniego pm10")
        for i in sensor_list.values():
            i.calc_mean_pm10()
            iteratorek += 1
            if iteratorek % 200 == 0:
                print(str(iteratorek / 20) + "%")
    else:
        print("liczenie sredniego pm2.5")
        for i in sensor_list.values():
            i.calc_mean_pm2_5()
            iteratorek += 1
            if iteratorek % 200 == 0:
                print(str(iteratorek / 20) + "%")


def calc_coef_pm(sensor_list,PM="pm10"):
    if PM == "pm10":
        print("---liczenie korelacji pm10---")
        for i in sensor_list.values():
            i.calc_cor_coefs_pm10(sensor_list)
    else:
        print("---liczenie korelacji pm2,5---")
        for i in sensor_list.values():
            i.calc_cor_coefs_pm2_5(sensor_list)


def calc_coef_div(sensor_list, PM ="pm10"):
    print("-----prosze sprawdzic czy policzono dywergencje-----")
    if PM == "pm10":
        print("---liczenie korelacji dywergencji pm10---")
        for i in sensor_list.values():
            i.calc_cor_coefs_pm10_div(sensor_list)
    else:
        print("---liczenie korelacji dywergencji pm2,5---")
        for i in sensor_list.values():
            i.calc_cor_coefs_pm2_5_div(sensor_list)
def calc_means(sensor_list):
    for i in sensor_list.values():
        # ---wyliczam maksima---
        i.calc_daily_maxes_pm10()
        i.calc_daily_maxes_pm2_5()
        i.calc_daily_maxes_div()
        i.calc_daily_maxes_div_pm2_5()
        #---wyliczam srednie---
        i.calc_mean_pm10()
        i.calc_mean_pm2_5()
        i.calc_mean_div_pm10_weighted()
        i.calc_mean_div_pm2_5_weighted()
        #---wyliczam mean maxes---
        i.calc_mean_maxes_pm10()
        i.calc_mean_maxes_pm2_5()
        i.calc_mean_maxes_div()
        i.calc_mean_maxes_div_pm2_5()

def find_closest_sensors(sensor_list,latitude,longitude,inner_radius=0,outer_radius=5):
    from geopy.distance import great_circle
    id_list = []
    lat_list = []
    long_list = []
    for i in sensor_list.values():
        centre = (latitude, longitude)
        me = (i.latitude, i.longitude)
        dist = great_circle(me, centre).kilometers
        if dist > inner_radius and dist < outer_radius:
            id_list.append(i.id)
            lat_list.append(i.latitude)
            long_list.append(i.longitude)
    file = open("ciekawe_id","w")
    for j in range(len(id_list)):
        print(id_list[j],file=file)
        print(lat_list[j],file=file)
        print(long_list[j],file=file)
        print(" ",file=file)
    file.close()


