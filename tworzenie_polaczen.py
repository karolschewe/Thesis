import os
import json
from datetime import datetime
from geopy.distance import great_circle

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

id_coordintates = []
for i in json_list[0]:
    id_coordintates.append([i['id'],i['latitude'],i['longitude']])
from class_sensor import export_connections_to_file
export_connections_to_file(id_coordintates,5)



#print(json_list[0][0]['latitude'])

print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")