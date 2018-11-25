import paho.mqtt.publish as publish
 
MQTT_SERVER = "192.168.88.24"
MQTT_PATH = "test_channel"
 
publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)
 
