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
import strain_calculation as cal


# Thermal sensors details at thingspeak
therm_channel_id = 1083150
therm_API_write = '23NNOFM7VANJ3KJA'
therm_API_read = '00IX5YL06NSI6W33'

# Smartbolt channel details at thingspeak
strain_channel_id = 1104638
strain_API_write = 'RGNVI3JND687TN33'
strain_API_read = 'Y4YL8OS6I3L1BXOA'

# USB port for arduino connecting to Raspberry, Arduino with thermal sensor is the last in list
arduino_port1 = '/dev/ttyUSB0'
arduino_port2 = '/dev/ttyUSB2'
arduino_port3 = '/dev/ttyUSB1'
port_list = [arduino_port1,arduino_port2,arduino_port3]

# Thermal code
def get_therm_data():
    sensor_data = {}
    for sensor in W1ThermSensor.get_available_sensors():
        sensor_data[sensor.id] = sensor.get_temperature()
    return sensor_data

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

def get_strain_therm_data(line):
    print(line)
##    sub_str = line.split(':')
##    print(sub_str)
    
    d = dict(item.split("=") for item in line.split(":"))
    return d

def get_arduino_data(port_list):
    arduino_data = {}
    for port in port_list:
        print(port)
        ser = serial.Serial(port,9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=5)
        ser.flush()
        if ser.readline():
            try:
                line = ser.readline().decode('utf-8').rstrip()
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
                pass
            else:
                try:
                    data_per_ard = get_strain_therm_data(line)
                except ValueError:
                    print("ValueError")
                    pass
                else:
                    for key in data_per_ard.keys():
                        if key != 'temp':
                            arduino_data[key + port.split('/')[2]] = data_per_ard[key]
                        else:
                            arduino_data[key] = data_per_ard[key]
    if 'temp' in arduino_data.keys():
        return arduino_data
    else:
        return {}
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
    while True:
##        therm_sensor_data = get_therm_data()
##        thingspeak_thermal_post(therm_sensor_data)
        arduino_data = get_arduino_data(port_list)
        print(arduino_data)
        thingspeak_strain_post(arduino_data)
        time.sleep(15)
