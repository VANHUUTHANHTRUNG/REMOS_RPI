#!/usr/bin/env python3
import serial
import time
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from w1thermsensor import W1ThermSensor
import http.client
import urllib
import thingspeak
from multiprocessing import Process

port_str = '/dev/ttyACM1'

# Thermal sensors details at thingspeak
therm_channel_id = 1083150
therm_API_write = '23NNOFM7VANJ3KJA'
therm_API_read = '00IX5YL06NSI6W33'

# Smartbolt channel details at thingspeak
strain_channel_id = 1102730
strain_API_write = 'XVK2UWY0T72HDJQI'
strain_API_read = 'ISUW80PVH5LB1TJM'

def get_therm_data():
    sensor_data = {}
    for sensor in W1ThermSensor.get_available_sensors():
        sensor_data[sensor.id] = sensor.get_temperature()
    return sensor_data

def get_strain_therm_data(line):
##    d = {}
##    sub_str = line.split(':')
##    print(sub_str)
##    key,value = zip(*(s.split('=') for s in sub_str))
##    for k in key:
##        d[k] = value
    d = dict(item.split("=") for item in line.split(":"))
    for item in d.items():
        print(item)
    return d
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

def thingspeak_strain_post(sensor_data):
    params = ""    
    for idx, val in enumerate(sensor_data.values()):
        params += '&' + urllib.parse.urlencode({'field{}'.format(idx+1): val})
##        print(params)
    params += '&' + urllib.parse.urlencode({'key':strain_API_write})
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

if __name__ == '__main__':
    ser = serial.Serial(port_str,9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=5)
    ser.flush()
    t1 = time.time()
    time.sleep(15)
    t2 = 0
    while (t2-t1) < 30:
        print("Warming up")
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        time.sleep(1)
        t2 = time.time()
        ser.flush()
    while(True):
        #Thermal sensors:
        therm_sensor_data = get_therm_data()
        thingspeak_thermal_post(therm_sensor_data)

        #Strain gauge:
        strain_val = []
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            strain_therm_sensor_data = get_strain_therm_data(line)
            thingspeak_strain_post(strain_therm_sensor_data)



        time.sleep(15)
