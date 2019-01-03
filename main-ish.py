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
#print(json_list[3][125].keys())
sensor_list = init.init_sensor_list(json_list)
init.calc_div(sensor_list)
init.calc_div(sensor_list,"yusdgas")

exports.FFT_plot(sensor_list[739],"Ładach",type_of_data="hatsdcf")


print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")