
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

def export_mean_div_pm_10(sensor_list):
    export_file = open("pm10_mean_div","w")
    for i in sensor_list:
        print("id="+str(i.id),file=export_file)
        print(i.mean_div_pm10,file=export_file)
    export_file.close()
def import_mean_div_pm_10(sensor_list,dir = "pm10_mean_div"):
    for i in sensor_list:
        i.import_mean_div_pm_10(dir=dir)

def export_coords_to_excel(sensor_list):
    import xlsxwriter

    lat_list = []
    long_list = []
    for i in sensor_list:
        if i.mean_div_pm10 > 200:
            print(i.id)
            lat_list.append(i.latitude)
            long_list.append(i.longitude)
    workbook = xlsxwriter.Workbook('myplaces.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    worksheet.write(row,col,"latitude")
    worksheet.write(row,col+1,"longitude")
    row+=1
    iteratorek = 0
    for i in range(len(lat_list)):
        worksheet.write(row,col,lat_list[iteratorek])
        worksheet.write(row,col+1,long_list[iteratorek])
        row+=1
        iteratorek+=1

    workbook.close()
