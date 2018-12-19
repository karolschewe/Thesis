import init
import exports
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor

startTime = datetime.now() #mierzenie czasu wykonywania programu

#jakie parametry losować w próbie kontrolnej
# jak to na wykres jak to jest zespolone? -- moduł
# co jeszcze warto doliczyć -- minima
# co powinienem zawrzeć w inżynerce
# TODO:
# histogram z maksimow


#lista zawierajaca wczytane dane z kazdego pliku w folderze ( 1 plik = 1 zmienna w liscie)
json_list = init.import_data()


# inicjalizacja klasy sensor
sensor_list = init.init_sensor_list(json_list,import_all=True)
init.calc_mean_maxes(sensor_list)

exports.max_pm_10_div_hist(sensor_list)
exports.FFT_plot(sensor_list[849])
print(sensor_list[849].daily_div_maxes)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")