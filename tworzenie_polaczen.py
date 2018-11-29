import os
import json
from datetime import datetime
import matplotlib.pyplot as plt


startTime = datetime.now() #mierzenie czasu wykonywania programu


#dodac procentowo ile jest wiecej
#czyli dywergencja/srednia w otoczeniu
#obliczyc średnią dywergencję dla czujnika
#i znaleźć czujniki ze średnią powyżej średniej
#robic rozklad srednich dywergencji
#wykres z tego
#zrobic mapę z srednich dywergencji (np wykres: x szerokość y długość)
#pomyslec zeby wyliczone wariancje dla sensora wyrzucac do pliku i potem tylko to wczytywac i na tym liczyc zamiast zawsze od nowa
# w ogole dzielic sobie program na segmenty
#korelacje serii czasowych sasiadow
#korelacje dywergencji sasiadow
#zrobic model zerowy -- wrzucic jako dane z czujników rozklad jednostajny i policzyc to samo


#test importu danych do airly
test = []
plik_test = open("airly_sensor_list",'r')
for line in plik_test:
    test.append(line.strip())
print("lista czujnikow do airly")
print(test)

all_files_in_dir = os.listdir()
#wyciaganie plikow z danymi -- zalozenie: koncza sie na .txt
datafiles = []
for i in all_files_in_dir:
    if i.endswith("txt"):
        datafiles.append(i)
        print(i)

#lista zawierajaca wczytane dane z kazdego pliku w folderze ( 1 plik = 1 zmienna w liscie)
json_list = []

#wczytywanie danych ze wszystkich plikow konczacych sie na txt
#poprawne dane sa od 9 pazdziernika 2018
for i in datafiles:
    with open(i) as json_file:
        json_list.append(json.load(json_file))
#odwolywanie sie do konkretnego czujnika z konkretnego dnia
#print (json_list[0][123]['history'][0].keys())
#print (json_list[0][123].keys())
#print(json_list[0][123]['currentMeasurements'])
print(json_list[0][123]['history'])
print(json_list[0][123].keys())
print(json_list[0][123]['history'][0])
print(json_list[0][123]['history'][0]['measurements'])
print(json_list[0][123]['history'][0]['measurements']['pm1'])

from class_id_connections import id_connections




# inicjalizacja klasy sensor
#import polaczen sensorow z pliku
from class_sensor import Sensor
sensor_list = []
for i in json_list[0]:
    sensor_list.append(Sensor(i['id'],i['latitude'],i['longitude']))
print("liczba sensorow")
print(len(sensor_list))
print("liczba sensorow")
#sprawdzenie czy nie ma wiecej sensorow w reszcie
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
#wyliczenie polaczen

connections = []
plik = open("siec_polaczen","w")
for i in sensor_list:
    connections.append(id_connections(i,sensor_list,5))

for i in connections:
    plik.write("id="+str(i.id))
    plik.write("\n")
    for j in i.connections:
        plik.write(str(j))
        plik.write("\n")
plik.close()



for i in sensor_list:
    i.import_connections()
    i.measurements = i.json_to_observations(json_list)
print("zakonczono tworzenie polaczen")
# for i in sensor_list:
#     i.calc_var_pm10(sensor_list)
print(sensor_list[0].connections)
# for i in sensor_list[7].measurements:
#     print(i.time_of_obs)
print(len(sensor_list[7].measurements))
print(sensor_list[7].id)
print(len(sensor_list[8].measurements))
print(sensor_list[8].id)

sensor_list[44].calc_var_pm10(sensor_list)
wykres_y = []
for jj in sensor_list[44].measurements:
    print(jj.variance)
    wykres_y.append(jj.variance)
plt.plot(wykres_y)
plt.ylabel('wariancja licznika w krakowie')
plt.show()
print("lat:")
print (sensor_list[44].latitude)
print("long:")
print(sensor_list[44].longitude)
print(sensor_list[44].connections)
puste = 0
lista_do_airly = []
plik_sensory = open("airly_sensor_list",'a')
for i in sensor_list:
    if len(i.connections) == 0:
        print(i.id)
        puste+=1
    else:
        print(i.id, file=plik_sensory)
        lista_do_airly.append(i.id)

print("liczba pustych sensorow")
print(puste)
print ("liczba niepustych sensorow")
print(len(lista_do_airly))
print()
print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")