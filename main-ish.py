import init
import exports
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor

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


startTime = datetime.now() #mierzenie czasu wykonywania programu


json_list = init.import_data()
sensor_list = init.init_sensor_list(json_list)
init.calc_coef_pm(sensor_list)
exports.corr_coef_hist(sensor_list,min=0)
exports.corr_coef_hist(sensor_list,min=4)


print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")