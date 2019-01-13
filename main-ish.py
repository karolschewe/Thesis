import init
import exports
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor

def policz_rzeczy_inz():
    json_list = init.import_data()
    sensor_list = init.init_sensor_list(json_list, True)
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

def custom_graph(latitude,longitude,inner_radius=0,outer_radius = 5,podpis=""):
    json_list = init.import_data()
    sensor_list = init.init_sensor_list(json_list)
    init.find_closest_sensors(sensor_list, latitude, longitude,inner_radius,outer_radius)
    sensor_list = init.init_sensor_list(json_list,True,False,True)
    init.init_connections(sensor_list,custom=True)
    sensor_list = init.init_sensor_list(json_list, True, False, True)
    init.calc_coef_pm(sensor_list)
    exports.corr_coef_hist(sensor_list,gdzie=podpis)

startTime = datetime.now() #mierzenie czasu wykonywania programu


custom_graph(52.231565,21.006170,0,12,"dla całej Warszawy")
custom_graph(52.231565,21.006170,0,6,"dla centrum Warszawy")
custom_graph(52.231565,21.006170,9,14,"dla obrzeży Warszawy")
custom_graph(50.053527,19.977138,0,4,"dla centrum Krakowa")
custom_graph(50.053527,19.977138,6,10,"dla obrzeży Krakowa")
custom_graph(50.053527,19.977138,0,10,"dla całego Krakowa")

print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")