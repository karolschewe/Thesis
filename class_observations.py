from dateutil import parser

class Observations:
    time_of_obs = parser.parse("966-10-13T21:00:00Z") #format: 2018-10-13T21:00:00Z
    pm1 = -1.0
    pm2_5 = -1.0
    pm10 = -1.0 #micrograms for cubic meter
    humidity = -1.0#percent as float
    atm_pressure = -1.0  # kPa
    temperature = -1.0#in celsius
    polution_stage = -1 #1,2,3,4,5,6,7 the smaller the better, where 3 is average quality(about 100% of EU norms)
    airly_quality_index = -1.0#no one knows the formula
    variance = -1.0

    def __init__(self,datetime_string=None,pm1=None,pm2_5=None,pm10=None,humidity=None,pressure=None,temperature=None,pollution_stage=None,airly_quality_index=None):
        self.time_of_obs = parser.parse(datetime_string)
        self.pm1 = pm1
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.humidity = humidity
        self.atm_pressure = pressure
        self.temperature = temperature
        self.polution_stage =pollution_stage
        self.airly_quality_index = airly_quality_index
    def set_variance(self,variance):
        self.variance = variance








