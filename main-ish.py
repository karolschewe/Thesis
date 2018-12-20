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
init.calc_coef_pm10(sensor_list)

init.calc_div(sensor_list)
for i in sensor_list.values():
    i.calc_cor_coefs_pm10_div(sensor_list)
init.calc_mean_maxes(sensor_list)
exports.max_pm_10_hist(sensor_list)
exports.max_pm_10_div_hist(sensor_list)


exports.corr_coef_hist(sensor_list)
exports.corr_coef_hist(sensor_list,log=True)
exports.corr_coef_hist(sensor_list,div=True)
exports.corr_coef_hist(sensor_list,log=True,div=True)
print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")