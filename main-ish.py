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

def policz_rzeczy_inz():
    json_list = init.import_data()
    sensor_list = init.init_sensor_list(json_list,True)
    init.calc_div(sensor_list)
    init.calc_div(sensor_list,PM="pm25")
    init.calc_div_weighted(sensor_list)
    init.calc_div_weighted(sensor_list,PM="pm25")
    init.calc_means(sensor_list)
    exports.mean_pm_hist(sensor_list)
    exports.mean_pm_hist(sensor_list,PM="pm25")
    exports.max_pm_hist(sensor_list)
    exports.max_pm_hist(sensor_list,PM="pm25")
    exports.mean_div_hist(sensor_list)
    exports.mean_div_hist(sensor_list,PM="pm25")
    exports.mean_pm_div_wei_hist(sensor_list)
    exports.mean_pm_div_wei_hist(sensor_list,PM="pm25")
    exports.export_sources_excel_pm10(sensor_list,"lista_pm10_zrodla_bez_wag.xlsx")
    exports.export_sources_excel_pm10(sensor_list, "lista_pm10_zrodla_wagi.xlsx",True)
    exports.export_sources_excel_pm2_5(sensor_list,"lista_pm25_zrodla_bez_wag.xlsx")
    exports.export_sources_excel_pm2_5(sensor_list,"lista_pm25_zrodla_bez_z_wagami.xlsx",True)
    exports.FFT_plot(sensor_list[739],"Ładach")
    exports.FFT_plot(sensor_list[1123],"Gliwicach")
    exports.FFT_plot(sensor_list[2880],"Pruszkowie")
    exports.FFT_plot(sensor_list[739], "Ładach","pm25")
    exports.FFT_plot(sensor_list[1123], "Gliwicach","pm25")
    exports.FFT_plot(sensor_list[2880], "Pruszkowie","pm25")

policz_rzeczy_inz()

print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")