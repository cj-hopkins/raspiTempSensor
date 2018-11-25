import bluetooth
import time
import subprocess

subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

bd_addr = "B8:27:EB:52:84:13"
port = 3

while True:
    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect((bd_addr, port))
    except:
        continue
    sock.send("Hello!!")
    time.sleep(5)
    
sock.close()

