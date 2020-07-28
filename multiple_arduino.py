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





def get_strain_therm_data(line):
    print(line)
##    sub_str = line.split(':')
##    print(sub_str)
    
    d = dict(item.split("=") for item in line.split(":"))
    return d

def thingspeak_strain_post(sensor_data):
    params = ""    
    for idx, val in enumerate(sensor_data.values()):
        params += '&' + urllib.parse.urlencode({'field{}'.format(idx+1): val})
    params += '&' + urllib.parse.urlencode({'key':strain_API_write})
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


# USB port for arduino connecting to Raspberry, Arduino with thermal sensor is the last in list
arduino_port1 = '/dev/ttyUSB1'
port_list = [arduino_port1]


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
                        arduino_data[key] = data_per_ard[key]
    therm_strain = cal.strain_therm(float(arduino_data["temp1"]))
    for key in arduino_data.keys():
        if key != "temp1":
            total_strain = cal.strain_total(float(arduino_data[key]))
            result_strain = total_strain - therm_strain
            arduino_data[key] = result_strain
    return arduino_data

if __name__ == '__main__':
    while True:
        arduino_data = get_arduino_data(port_list)
        print(arduino_data)
        time.sleep(1)
        
        
        




                    
