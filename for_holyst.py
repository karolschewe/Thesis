import init
from datetime import datetime
import exports

startTime = datetime.now() #mierzenie czasu wykonywania programu
json_list = init.import_data()



sensor_list = init.init_sensor_list(json_list)

for i in sensor_list:
    i.calc_daily_maxes()
exports.export_daily_pm10_maxes_file(sensor_list)



print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")
#sprawdz czy do initu nie trzeba wprowadzic zmian (tworzenie_polaczen.py)