import init
import exports
from datetime import datetime
import matplotlib.pyplot as plt
from class_sensor import Sensor
from geopy.geocoders import Nominatim
import pandas
from time import sleep


def policz_rzeczy_inz():
    json_list = init.import_data()
    sensor_list = init.init_sensor_list(json_list, True)
    del json_list
    init.calc_div(sensor_list)
    init.calc_div(sensor_list,PM="pm25")
    init.calc_div_weighted(sensor_list)
    init.calc_div_weighted(sensor_list,PM="pm25")
    init.calc_means(sensor_list)
    init.calc_coef_pm(sensor_list)
    init.calc_coef_pm(sensor_list,PM="pm25")
    init.calc_coef_div(sensor_list)
    init.calc_coef_div(sensor_list,PM="pm25")
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
    exports.corr_coef_hist(sensor_list)
    exports.corr_coef_hist(sensor_list,PM="pm25")
    exports.corr_coef_hist(sensor_list,div=True)
    exports.corr_coef_hist(sensor_list,PM="pm25",div=True)


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

json_list = init.import_data()
sensor_list = init.init_sensor_list(json_list, True)
del json_list



geolocator = Nominatim(user_agent="g")
location = geolocator.reverse("52.387294, 22.010903")
print(location.raw)

#zbieranie pm10, i koordynatow

id = []
pm10 = []
lat = []
long = []
wojewodztwo = []
kod_pocztowy = []
powiat = []
g=0

for i in sensor_list.values():
    g = g + 1
    if g < 1500: continue
    print(g)
    id.append(i.id)
    pm10.append(i.mean_pm10)
    lat.append(i.latitude)
    long.append(i.longitude)
    location = geolocator.reverse([i.latitude,i.longitude])
    wojewodztwo.append(location.raw['address']['state'])
    if 'postcode' in location.raw['address'].keys():
        kod_pocztowy.append(location.raw['address']['postcode'])
    else:
        kod_pocztowy.append(None)
    powiat.append(location.raw['address']['county'])
    sleep(1.1)
    if g == 2500:break


df = pandas.DataFrame(list(zip(id, pm10,lat,long,wojewodztwo,kod_pocztowy,powiat)),
               columns =['id', 'pm10','lat','long','wojewodztwo','kod_pocztowy','gmina'])

print(df)

df.to_csv("gminy4.csv", index=False)





print("Program wykonywał się " + str((datetime.now() - startTime).seconds)+ " sekund")