import time
from w1thermsensor import W1ThermSensor
import http.client
import urllib
import thingspeak

##while True:
##    for sensor in W1ThermSensor.get_available_sensors():
##        print("Sensor {:s} : {:.2f}".format(sensor.id,sensor.get_temperature()))
##    print("-"*40)
##    time.sleep(1)

# Thermal sensors details at thingspeak
therm_channel_id = 1083150
therm_API_write = '23NNOFM7VANJ3KJA'
therm_API_read = '00IX5YL06NSI6W33'

# Smartbolt channel details at thingspeak
bolt_channel_id = 1102730
bolt_API_write = 'XVK2UWY0T72HDJQI'
bolt_API_read = 'ISUW80PVH5LB1TJM'

def get_sensor_data():
    sensor_data = {}
    for sensor in W1ThermSensor.get_available_sensors():
        sensor_data[sensor.id] = sensor.get_temperature()
    return sensor_data

def print_temp(sensor_data):
    for key,val in sensor_data.items():
        print("{:s} : {:.2f}".format(key,val))
    print("-"*50)



def thingspeak_thermal_post(sensor_data):
    params = ""    
    for idx, val in enumerate(sensor_data.values()):
        params += '&' + urllib.parse.urlencode({'field{}'.format(idx+1): val})
##        print(params)
    params += '&' + urllib.parse.urlencode({'key':therm_API_write})
##    print("Final: ")
##    print(params)
    headers = {"Content-typZZe" : "application/x-www-form-urlencoded","Accept":"text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST","/update",params,headers)
        response = conn.getresponse()
        print(response.status)
        print(response.reason)
        data = response.read()
        conn.close()
    except:
        print("connection failed")
    



while True:
    sensor_data = get_sensor_data()
##    print_temp(sensor_data)
    thingspeak_thermal_post(sensor_data)
    time.sleep(15) # maximum rate for free trial with thingspeak
