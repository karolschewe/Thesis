import os
import json
from datetime import datetime


startTime = datetime.now() #mierzenie czasu wykonywania programu




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
print(json_list[0][123]['history'][0])
print(json_list[0][123]['history'][0]['measurements'])
print(json_list[0][123]['history'][0]['measurements']['pm1'])
from class_id_connections import id_connections


#tworzenie sieci polaczen i eksport do pliku

#connections = []
#plik = open("siec_polaczen","w")
#for i in json_list[0]:
#     connections.append(id_connections(i['id'],i['latitude'],i['longitude'],json_list[0],5))
#
# for i in connections:
#     plik.write("id="+str(i.id))
#     plik.write("\n")
#     for j in i.connections:
#         plik.write(str(j))
#         plik.write("\n")
# plik.close()
#
#

# inicjalizacja klasy sensor
#import polaczen sensorow z pliku
from class_sensor import Sensor
sensor_list = []
for i in json_list[0]:
    sensor_list.append(Sensor(i['id'],i['latitude'],i['longitude']))
for i in sensor_list:
    i.import_connections(start_index=("id="+str(i.id)))
    i.measurements = i.json_to_observations(json_list)

print(sensor_list[0].connections)
# for i in sensor_list[7].measurements:
#     print(i.time_of_obs)
print(len(sensor_list[7].measurements))
print(sensor_list[7].id)
print(len(sensor_list[8].measurements))
print(sensor_list[8].id)
for gowno in sensor_list[156].measurements:
    print(gowno.time_of_obs)
    print(gowno.pm1)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")