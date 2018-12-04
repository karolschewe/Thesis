import init
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor

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




#lista zawierajaca wczytane dane z kazdego pliku w folderze ( 1 plik = 1 zmienna w liscie)
json_list = init.import_data()

print(json_list[0][123]['history'])
print(json_list[0][123].keys())
print(json_list[0][123]['history'][0])
print(json_list[0][123]['history'][0]['measurements'])
print(json_list[0][123]['history'][0]['measurements']['pm1'])

# inicjalizacja klasy sensor
sensor_list = init.init_sensor_list(json_list)


init.import_mean_div_pm_10(sensor_list)

init.export_coords_to_excel(sensor_list)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")