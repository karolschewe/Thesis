from geopy.distance import great_circle

class id_connections:
    id = 0
    latitude = 0.0
    longitude = 0.0
    connections = []

    def __init__(self,sensorek,sensor_list,max_dist):
        self.id = sensorek.id
        self.latitude = sensorek.latitude
        self.longitude = sensorek.longitude
        temp_id_list = []
        for i in sensor_list:
            me = (sensorek.latitude, sensorek.longitude)
            it = (i.latitude, i.longitude)
            dist = great_circle(me, it).kilometers
            if dist < max_dist:
                if self.id != i.id:
                    temp_id_list.append(i.id)




        self.connections = temp_id_list











