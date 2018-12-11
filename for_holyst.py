import init
from datetime import datetime

startTime = datetime.now() #mierzenie czasu wykonywania programu
json_list = init.import_data()

# prezentacja
# cel pracy
# podzial czasteczek co to znaczy pm10
# wplyw zapylenia na zdrowie
#python - dlaczego, wady zalety
# metoda łączenia w siatkę powiedziec o mozliwym woronoju
# jak liczenie gradient
#ewentualne pole skalarne
# wyszukane zrodla mapa
#tabelka od hołysta
# co jeszcze zostalo

sensor_list = init.init_sensor_list(json_list)
#init.import_mean_div_pm_10(sensor_list)
#init.export_coords_to_excel(sensor_list)

# init.calc_mean_pm10(sensor_list)
# init.export_mean_pm10(sensor_list)

# file = open("interesujące punkty(lista id)","r")
# ajdi = []
# for line in file:
#     ajdi.append(int(line.strip()))
# file.close()
# # file = open('my_places_pm10', "w")
# for i in sensor_list:
#     if i.id in ajdi:
#         print("id="+str(i.id))
#         print(len(i.connections))
#         if i.id == 3365:
#             for j in i.measurements:
#                 print(j.time_of_obs)
#                 print(j.pm10)




for i in sensor_list:
    if i.id == 739:
        print (len(i.connections))

print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")
#sprawdz czy do initu nie trzeba wprowadzic zmian (tworzenie_polaczen.py)