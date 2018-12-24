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
sensor_list = init.init_sensor_list(json_list)
exports.FFT_plot(sensor_list[739],"Ładach")
exports.FFT_plot(sensor_list[3165],"Pruszkowie")
#exports.export_sources_excel(sensor_list,"źródła_base.xlsx")
#exports.export_sources_excel(sensor_list,"źródła_wagi.xlsx",weighted=True)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")