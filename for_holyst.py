import init
from datetime import datetime
import exports

#starac sie robic kilka operacji w jednej pętli


startTime = datetime.now() #mierzenie czasu wykonywania programu


json_list = init.import_data()
sensor_list = init.init_sensor_list(json_list)





init.calc_div(sensor_list)
init.calc_div_weighted(sensor_list)
init.calc_mean_pm10(sensor_list)
for i in sensor_list:
    i.calc_daily_maxes_div()
    i.calc_daily_maxes_pm10()

exports.export_daily_div_maxes_file(sensor_list)
exports.export_daily_pm10_maxes_file(sensor_list)
exports.export_mean_div_pm_10_file(sensor_list)
exports.export_mean_pm10_file(sensor_list)
exports.export_mean_div_wei_pm_10_file(sensor_list)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")
#sprawdz czy do initu nie trzeba wprowadzic zmian (tworzenie_polaczen.py)