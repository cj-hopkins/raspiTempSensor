from Adafruit_DHT import read_retry, DHT11
from logging import basicConfig, info, INFO, Formatter, warning
from time import sleep, time
from argparse import ArgumentParser
from bluetooth import  BluetoothSocket, RFCOMM
from subprocess import call
from datetime import datetime
import paho.mqtt.publish as publish
from threading import Timer, Semaphore

# bluetooth setup
call(['sudo', 'hciconfig', 'hci0', 'piscan'])
bd_addr = 'B8:27:EB:52:84:13'
port = 3
sock=BluetoothSocket(RFCOMM)
sock.connect((bd_addr, port))

# Temp sensor setup
SENSOR = DHT11
PIN = 3

# MQTT setup
MQTT_SERVER = '192.168.88.31'
MQTT_PATH = 'test_channel'

# logging setup
basicConfig(
            filename='dht11.log', 
            filemode='w',
            format='%(asctime)s.%(msecs)06d %(message)s',
            datefmt='%Y-%m-%d,%H:%M:%S',
            level=INFO,
        )

CURRENT_PROTOCOL = 'RFCOMM'
SWAP_MUTEX = Semaphore(1)

def swapProtocols():
    with SWAP_MUTEX:
        if CURRENT_PROTOCOL == 'RFCOMM':
            CURRENT_PROTOCOL = 'MQTT'
            sock.msg('mqtt')
            sock.close()
        else:
            CURRENT_PROTOCOL = 'RFCOMM'
            publish.single(MQTT_PATH, 'bluetooth', hostname=MQTT_SERVER)
            sock.connect((bd_addr, port))
    Timer(10.0, swapProtocols).start()

def sendMsg(msg):
    if CURRENT_PROTOCOL == 'RFCOMM':
        sock.send(msg)
    else:
        publish.single(MQTT_PATH, msg, hostname=MQTT_SERVER)


def main():
    Timer(10.0, swapProtocols).start()
    while True:
        humidity, temperature = read_retry(SENSOR, PIN)
        if humidity is not None and temperature is not None:
            result = '{}\tSensorID=17205700, Temperature={}, Humidity={}'.format(datetime.now(), temperature, round(humidity))
            print(result)
            info(result)
            print('sending')
            try:
                #sock.send(result)
                #publish.single(MQTT_PATH, result, hostname=MQTT_SERVER)
                with SWAP_MUTEX:
                    sendMsg(result)
            except Exception as e:
                print('failed connection')
                print(e)
                info(e)
                sleep(5)
                continue
            print('sent')
            sleep(5)

        else:
            result = 'Failed to get reading. Try again!'
            info(result)

if __name__ == '__main__':
    main()
