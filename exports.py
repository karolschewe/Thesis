def mean_pm_10_div_wei_hist(sensor_list):
    mean_values = []
    for i in sensor_list.values():
        mean_values.append(i.mean_div_pm10_weighted)

    biny = []
    var = -2.0
    for i in range(100):
        biny.append(var)
        var += 0.04
    from matplotlib import pyplot
    import statistics
    (n, bins, patches) = pyplot.hist(mean_values, bins=biny)
    mean = statistics.mean(mean_values)
    median = statistics.median(mean_values)
    stdev = statistics.stdev(mean_values)
    maxvalue = max(mean_values)
    stats_string = ("średnia: " + str(round(mean, 3)) + "\n" + "mediana: " + str(
        round(median, 3)) + "\n" + "odch. std: " + str(
        round(stdev, 3)) + "\n" + "max: " + str(round(maxvalue, 3)) + "\n" + "N: " + str(len(mean_values)))
    pyplot.figtext(0.15, 0.7, stats_string)
    pyplot.title("Rozkład średnich dziennych dywergencji względnych \n dla grafu z wagami")
    pyplot.xlabel('dywergencja względna pm10')
    pyplot.ylabel('liczba zliczen')
    pyplot.legend()
    pyplot.show()

def export_mean_div_pm_10_file(sensor_list, dir = "pm10_mean_div"):
    export_file = open(dir,"w")
    for i in sensor_list.values():
        print("id="+str(i.id),file=export_file)
        print(i.mean_div_pm10,file=export_file)
    export_file.close()

def export_mean_div_wei_pm_10_file(sensor_list, dir = "pm10_mean_wei_div"):
    export_file = open(dir,"w")
    for i in sensor_list.values():
        print("id="+str(i.id),file=export_file)
        print(i.mean_div_pm10_weighted,file=export_file)
    export_file.close()

def export_mean_pm10_file(sensor_list, dir = "pm10_mean"):
    export_file = open(dir, "w")
    for i in sensor_list.values():
        print("id=" + str(i.id), file=export_file)
        print(i.mean_pm10, file=export_file)
    export_file.close()


def export_daily_pm10_maxes_file(sensor_list, dir = "pm10_daily_maxes"):
    export_file = open(dir, "w")
    for i in sensor_list.values():
        print("id=" + str(i.id), file=export_file)
        for j in i.daily_pm10_maxes:
            print(j, file=export_file)
    export_file.close()


def export_daily_div_maxes_file(sensor_list, dir = "div_daily_maxes"):
    export_file = open(dir, "w")
    for i in sensor_list.values():
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

def export_sources_excel(sensor_list,directory,weighted = False,min_val = 0.5):
    import xlsxwriter

    lat_list = []
    long_list = []
    mean_div_list = []
    mean_pm10_list = []
    percentage_list = []
    sasiedzi = []
    adresy = []
    if weighted is False:
        for i in sensor_list.values():
            if i.mean_div_pm10 > min_val:
                print(i.id)
                lat_list.append(i.latitude)
                long_list.append(i.longitude)
                mean_div_list.append(i.mean_div_pm10)
                mean_pm10_list.append(i.mean_pm10)
                percentage_list.append(i.mean_pm10 / 50.0)
                sasiedzi.append(len(i.connections))
                adresy.append(i.address)
    else:
        for i in sensor_list.values():
            if i.mean_div_pm10_weighted > min_val:
                print(i.id)
                lat_list.append(i.latitude)
                long_list.append(i.longitude)
                mean_div_list.append(i.mean_div_pm10_weighted)
                mean_pm10_list.append(i.mean_pm10)
                percentage_list.append(i.mean_pm10 / 50.0)
                sasiedzi.append(len(i.connections))
                adresy.append(i.address)
    workbook = xlsxwriter.Workbook(directory)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    worksheet.write(row,col,"sz. geograficzna")
    worksheet.write(row,col+1,"dł. geograficzna")
    worksheet.write(row, col + 2, "śr.dzienna dywergencja względna")
    worksheet.write(row, col + 3, "śr. stężenie PM10")
    worksheet.write(row, col + 4, "% normy PM10")
    worksheet.write(row, col + 5, "n_sasiadow")
    worksheet.write(row, col + 6, "lokalizacja")
    row+=1
    iteratorek = 0
    for i in range(len(lat_list)):
        worksheet.write(row,col,lat_list[iteratorek])
        worksheet.write(row,col+1,long_list[iteratorek])
        worksheet.write(row, col + 2, mean_div_list[iteratorek])
        worksheet.write(row, col + 3, mean_pm10_list[iteratorek])
        worksheet.write(row, col + 4, percentage_list[iteratorek])
        worksheet.write(row, col + 5, sasiedzi[iteratorek])
        worksheet.write(row, col + 6, adresy[iteratorek])
        row+=1
        iteratorek+=1

    workbook.close()
# -----wykresy-----

def mean_pm_10_hist(sensor_list):
    mean_values = []
    for i in sensor_list.values():
        mean_values.append(i.mean_pm10)

    from matplotlib import pyplot
    import statistics
    biny = range(0,300,5)
    (n, bins, patches) = pyplot.hist(mean_values,bins=biny)
    mean = statistics.mean(mean_values)
    median = statistics.median(mean_values)
    stdev= statistics.stdev(mean_values)
    maxvalue = max(mean_values)
    stats_string = ("średnia: " + str(round(mean,3)) + "\n" + "mediana: " + str(round(median,3)) + "\n" + "odch. std: " + str(
        round(stdev,3)) + "\n" + "max: " + str(round(maxvalue,3))+"\n"+"N: "+str(len(mean_values)))
    pyplot.xlabel('pm10[$\mu g/m^3$]')
    pyplot.ylabel('liczba zliczen')
    pyplot.figtext(0.6, 0.7, stats_string)
    pyplot.title("Rozkład średnich dziennych zanieczyszczeń")
    pyplot.show()



def mean_pm_10_div_hist(sensor_list):
    mean_values = []
    for i in sensor_list.values():
        mean_values.append(i.mean_div_pm10)

    biny = []
    var = -2.0
    for i in range(100):
        biny.append(var)
        var += 0.04
    from matplotlib import pyplot
    import statistics
    (n, bins, patches) = pyplot.hist(mean_values, bins=biny)
    mean = statistics.mean(mean_values)
    median = statistics.median(mean_values)
    stdev = statistics.stdev(mean_values)
    maxvalue = max(mean_values)
    stats_string = ("średnia: " + str(round(mean,3)) + "\n" + "mediana: " + str(round(median,3)) + "\n" + "odch. std: " + str(
        round(stdev,3)) + "\n" + "max: " + str(round(maxvalue,3))+"\n"+"N: "+str(len(mean_values)))
    pyplot.figtext(0.15, 0.7, stats_string)
    pyplot.title("Rozkład średnich dziennych dywergencji względnych")
    pyplot.xlabel('dywergencja względna pm10')
    pyplot.ylabel('liczba zliczen')
    pyplot.legend()
    pyplot.show()



def max_pm_10_hist(sensor_list):
    mean_values = []
    for i in sensor_list.values():
        mean_values.append(i.mean_daily_pm10_maxes)

    from matplotlib import pyplot
    import statistics
    biny = range(0,500,5)
    (n, bins, patches) = pyplot.hist(mean_values,bins=biny)
    mean = statistics.mean(mean_values)
    median = statistics.median(mean_values)
    stdev= statistics.stdev(mean_values)
    maxvalue = max(mean_values)
    stats_string = ("średnia: " + str(round(mean,3)) + "\n" + "mediana: " + str(round(median,3)) + "\n" + "odch. std: " + str(
        round(stdev,3)) + "\n" + "max: " + str(round(maxvalue,3))+"\n"+"N: "+str(len(mean_values)))
    pyplot.xlabel('pm10[$\mu g/m^3$]')
    pyplot.ylabel('liczba zliczen')
    pyplot.figtext(0.6, 0.7, stats_string)
    pyplot.title("Rozkład średnich maksymalnych dziennych zanieczyszczeń")
    pyplot.show()


def max_pm_10_div_hist(sensor_list):
    mean_values = []
    for i in sensor_list.values():
        mean_values.append(i.mean_daily_div_maxes)

    biny = []
    var = -1.5
    for i in range(125):
        biny.append(var)
        var += 0.05
    from matplotlib import pyplot
    import statistics
    (n, bins, patches) = pyplot.hist(mean_values, bins=biny)
    mean = statistics.mean(mean_values)
    median = statistics.median(mean_values)
    stdev = statistics.stdev(mean_values)
    maxvalue = max(mean_values)
    stats_string = ("średnia: " + str(round(mean,3)) + "\n" + "mediana: " + str(round(median,3)) + "\n" + "odch. std: " + str(
        round(stdev,3)) + "\n" + "max: " + str(round(maxvalue,3))+"\n"+"N: "+str(len(mean_values)))
    pyplot.figtext(0.7, 0.7, stats_string)
    pyplot.title("Rozkład średnich maksymalnych dziennych dywergencji względnych")
    pyplot.xlabel('Dywergencja względna pm10')
    pyplot.ylabel('liczba zliczen')
    pyplot.show()

def corr_coef_hist(sensor_list,div=False,log=False):
    print("----prosze sprawdzic czy wyliczono wspolczynniki korelacji----")
    values = []
    title = ""
    label = ''
    if div == False:
        for i in sensor_list.values():
            for j in i.cor_coefs_pm10:
                values.append(j[1])
        title = "Histogram współczynników korelacji dla przebiegów pm10"
        label = 'Współczynnik korelacji'
    else:
        for i in sensor_list.values():
            for j in i.cor_coefs_pm10_div:
                values.append(j[1])
        title = "Histogram współczynników korelacji dla przebiegów \n dywergencji względnej pm10"
        label = 'Współczynnik korelacji'

    biny = []
    var = -1.0
    while(var <= 1):
        biny.append(var)
        var += 0.02

    from matplotlib import pyplot
    import statistics
    (n, bins, patches) = pyplot.hist(values, bins=biny)
    mean = statistics.mean(values)
    median = statistics.median(values)
    stdev = statistics.stdev(values)
    maxvalue = max(values)
    stats_string = ("średnia: " + str(round(mean, 3)) + "\n" + "mediana: " + str(
        round(median, 3)) + "\n" + "odch. std: " + str(
        round(stdev, 3)) + "\n" + "max: " + str(round(maxvalue, 3)) + "\n" + "N: " + str(len(values)))
    pyplot.figtext(0.7, 0.7, stats_string)
    pyplot.title(title)
    pyplot.xlabel(label)
    pyplot.ylabel('liczba zliczen')
    if log is True:
        pyplot.yscale("log")
    pyplot.show()


def FFT_plot(sensor,gdzie = "", type_of_data="pm10"):
    from numpy import fft, absolute,log2,argmax
    from math import ceil
    data_list = []
    if type_of_data == "pm10":
        for i in sensor.measurements:
            data_list.append(i.pm10)
            print(i.pm10)

        print(data_list)
        print(len(data_list))
        powerof2 = (ceil(log2(len(data_list))))-1
        print("number of points:"+str(2**powerof2))
        transformed_data = fft.fft(data_list,2**powerof2-1)
        from matplotlib import pyplot
        modules = []
        for i in transformed_data:
            modules.append(absolute(i))
        biny = []
        for i in range(300):
            biny.append(i*3)
        print(modules)
        n, bins, patches = pyplot.hist(modules, bins=biny)
        elem = argmax(n)
        print(elem)
        print(biny[elem])
        stats_string = "max: "+ str(biny[elem])
        pyplot.figtext(0.8, 0.8, stats_string)
        pyplot.title("Analiza fourierowska sensora w "+gdzie)
        pyplot.xlabel("moduł")
        pyplot.ylabel("liczba zliczeń")
        pyplot.show()
        print("transformata:")
        print (transformed_data)
    else:
        print("types other than pm10 not implemented")

