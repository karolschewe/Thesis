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
print (json_list[0][0].keys())

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

#inicjalizacja klasy sensor
#import polaczen sensorow z pliku
from class_sensor import sensor
sensor_list = []
for i in json_list[0]:
    sensor_list.append(sensor(i['id']))
for i in sensor_list:
    i.import_connections(start_index=("id="+str(i.id)))





print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")