from dateutil import parser

class Observations:
    time_of_obs = parser.parse("1996-01-23T21:00:00Z") #format: 2018-10-13T21:00:00Z
    pm1 = -1.0
    pm2_5 = -1.0
    pm10 = -1.0 #micrograms for cubic meter
    div_pm10 = 0 #dywergencja wzgledna (ile procent wzgledem sasiadow)
    div_pm10_weighted = 0
    div_pm2_5 = 0
    div_pm2_5_weighted = 0

    def __init__(self, datetime_string=None, pm1=None, pm2_5=None, pm10=None):
        if datetime_string:
            self.time_of_obs = parser.parse(datetime_string)
        self.pm1 = pm1
        self.pm2_5 = pm2_5
        self.pm10 = pm10

    def set_time(self,time_string):
        self.time_of_obs = parser.parse(time_string)

    def set_pm1(self, pm1):
        self.pm1 = pm1

    def set_pm2_5(self, pm2_5):
        self.pm2_5 = pm2_5

    def set_pm10(self, pm10):
        self.pm10 = pm10

    def set_div_pm10(self,div):
        self.div_pm10 = div

    def set_div_pm10_weighted(self,div_w):
        self.div_pm10_weighted = div_w

    def set_div_pm2_5(self,div):
        self.div_pm2_5 = div

    def set_div_pm2_5_weighted(self,div_w):
        self.div_pm2_5_weighted = div_w
