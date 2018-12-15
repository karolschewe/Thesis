def export_mean_div_pm_10_file(sensor_list, dir = "pm10_mean_div"):
    export_file = open(dir,"w")
    for i in sensor_list:
        print("id="+str(i.id),file=export_file)
        print(i.mean_div_pm10,file=export_file)
    export_file.close()

def export_mean_div_wei_pm_10_file(sensor_list, dir = "pm10_mean_wei_div"):
    export_file = open(dir,"w")
    for i in sensor_list:
        print("id="+str(i.id),file=export_file)
        print(i.mean_div_pm10_weighted,file=export_file)
    export_file.close()

def export_mean_pm10_file(sensor_list, dir = "pm10_mean"):
    export_file = open(dir, "w")
    for i in sensor_list:
        print("id=" + str(i.id), file=export_file)
        print(i.mean_pm10, file=export_file)
    export_file.close()


def export_daily_pm10_maxes_file(sensor_list, dir = "pm10_daily_maxes"):
    export_file = open(dir, "w")
    for i in sensor_list:
        print("id=" + str(i.id), file=export_file)
        for j in i.daily_pm10_maxes:
            print(j, file=export_file)
    export_file.close()


def export_daily_div_maxes_file(sensor_list, dir = "div_daily_maxes"):
    export_file = open(dir, "w")
    for i in sensor_list:
        print("id=" + str(i.id), file=export_file)
        for j in i.daily_div_maxes:
            print(j, file=export_file)
    export_file.close()



# ----------excel-----------
def export_time_series_excel(sensor, dir="sensor.xlsx"):
    import xlsxwriter
    time_list = []
    div_wei_list = []
    pm10_list = []
    for i in sensor.measurements:
        time_list.append(str(i.time_of_obs))
        div_wei_list.append(i.div_pm10_weighted)
        pm10_list.append(i.pm10)
    workbook = xlsxwriter.Workbook(dir)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    worksheet.write(row,col,"time")
    worksheet.write(row,col+1,"div")
    worksheet.write(row, col + 2, "pm10")
    row+=1
    iteratorek = 0
    for i in range(len(pm10_list)):
        worksheet.write(row,col,time_list[iteratorek])
        worksheet.write(row,col+1,div_wei_list[iteratorek])
        worksheet.write(row, col + 2, pm10_list[iteratorek])

        row+=1
        iteratorek+=1

    workbook.close()

def export_coords_excel(sensor_list):
    import xlsxwriter

    lat_list = []
    long_list = []
    mean_div_list = []
    mean_pm10_list = []
    percentage_list = []
    sasiedzi = []
    for i in sensor_list:
        if i.mean_div_pm10 < -0.001:
            print(i.id)
            lat_list.append(i.latitude)
            long_list.append(i.longitude)
            mean_div_list.append(i.mean_div_pm10)
            mean_pm10_list.append(i.mean_pm10)
            percentage_list.append(i.mean_pm10/50.0)
            sasiedzi.append(len(i.connections))
    workbook = xlsxwriter.Workbook('ujemna.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    worksheet.write(row,col,"latitude")
    worksheet.write(row,col+1,"longitude")
    worksheet.write(row, col + 2, "mean_div_value")
    worksheet.write(row, col + 3, "mean_pm10")
    worksheet.write(row, col + 4, "pm10_%normy")
    worksheet.write(row, col + 5, "n_sasiadow")
    worksheet.write(row, col + 6, "address")
    row+=1
    iteratorek = 0
    for i in range(len(lat_list)):
        worksheet.write(row,col,lat_list[iteratorek])
        worksheet.write(row,col+1,long_list[iteratorek])
        worksheet.write(row, col + 2, mean_div_list[iteratorek])
        worksheet.write(row, col + 3, mean_pm10_list[iteratorek])
        worksheet.write(row, col + 4, percentage_list[iteratorek])
        worksheet.write(row, col + 5, sasiedzi[iteratorek])
        row+=1
        iteratorek+=1

    workbook.close()
