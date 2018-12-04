from dateutil import parser

class Observations:
    time_of_obs = parser.parse("966-10-13T21:00:00Z") #format: 2018-10-13T21:00:00Z
    pm1 = -1.0
    pm2_5 = -1.0
    pm10 = -1.0 #micrograms for cubic meter
    humidity = -1.0#percent as float
    atm_pressure = -1.0  # Pa
    temperature = -1.0#in celsius
    pollution_stage = -1 #1,2,3,4,5,6,7 the smaller the better, where 3 is average quality(about 100% of EU norms)
    airly_quality_index = -1.0#no one knows the formula
    div_pm10 = -1.0 #dywergencja wzgledna (ile procent wzgledem sasiadow)

    def __init__(self,datetime_string=None,pm1=None,pm2_5=None,pm10=None,humidity=None,pressure=None,temperature=None,pollution_stage=None,airly_quality_index=None):
        if datetime_string:
            self.time_of_obs = parser.parse(datetime_string)
        self.pm1 = pm1
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.humidity = humidity
        self.atm_pressure = pressure
        self.temperature = temperature
        self.pollution_stage =pollution_stage
        self.airly_quality_index = airly_quality_index

    def set_time(self,time_string):
        self.time_of_obs = time_string

    def set_pm1(self, pm1):
        self.pm1 = pm1

    def set_pm2_5(self, pm2_5):
        self.pm2_5 = pm2_5

    def set_pm10(self, pm10):
        self.pm10 = pm10

    def set_humidity(self, humidity):
        self.humidity = humidity

    def set_pressure (self, pressure):
        self.atm_pressure = pressure

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_pollution_stage(self, pollution_level):
        self.pollution_stage = pollution_level

    def set_quality_index(self, quality_index):
        self.airly_quality_index = quality_index

    def set_div_pm10(self,div):
        self.div_pm10 = div








