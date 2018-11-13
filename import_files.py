import os
import json
#poprawne dane sa od 9 pazdziernika 2018

#funkcja zwraca tablice z danymi - jedna zmienna w tej tablicy to jeden wielki json ze wszystkimi senorami z jednego pliku
def get_data(dir="local"):
    if dir == "local":
        all_files_in_dir = os.listdir()
    else:
        all_files_in_dir = os.listdir(dir)
    datafiles = []
    #funkcja zaklada ze pliki z danymi koncza sie na txt
    for i in all_files_in_dir:
        if i.endswith("txt"):
            datafiles.append(i)
    json_list = []
    for i in datafiles:
        with open(i) as json_file:
            json_list.append(json.load(json_file))
    return json_list