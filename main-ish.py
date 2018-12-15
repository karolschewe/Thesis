import init
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor

startTime = datetime.now() #mierzenie czasu wykonywania programu



# TODO:
#robic rozklad srednich dywergencji
#wykres z tego
# w ogole dzielic sobie program na segmenty
#korelacje serii czasowych sasiadow
#korelacje dywergencji sasiadow
#zrobic model zerowy -- wrzucic jako dane z czujników rozklad jednostajny i policzyc to samo
#zrobic tak, aby dalsi sąsiedzi mieli mniejszy wpływ na gradient



#lista zawierajaca wczytane dane z kazdego pliku w folderze ( 1 plik = 1 zmienna w liscie)
json_list = init.import_data()


# inicjalizacja klasy sensor
sensor_list = init.init_sensor_list(json_list)


print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")