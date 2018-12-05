import init
json_list = init.import_data()

sensor_list = init.init_sensor_list(json_list)
#init.import_mean_div_pm_10(sensor_list)
#init.export_coords_to_excel(sensor_list)
for i in sensor_list:
    if i.id == 3365:
        for j in i.measurements:
            print(j.pm10)