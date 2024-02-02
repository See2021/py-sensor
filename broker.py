import paho.mqtt.client as mqtt
import time
import random
import mysql.connector

# MySQL connection
mydb = mysql.connector.connect(
  host="sensor.c3ukce48cxxt.us-east-1.rds.amazonaws.com",
  user="root",
  password="mn403193",
  database="sensors"
)

mycursor = mydb.cursor()

# MQTT settings
host = "mqtt.eclipseprojects.io"
port = 8000
topic = "Temperature"
# pump_topic = "Pump"
# fertilizer_topic = "Fertilizer"
# tank_topic = "Tank"

# Initiate the MQTT client
client = mqtt.Client()
client.connect(host)

sensor_id = 1
# sensor_id = 2
# sensor_id = 3
# sensor_id = 4

# Your random_delta function
def random_delta(start_value, min_delta, max_delta, precision=2):
    value_range = max_delta - min_delta
    half_range = value_range / 2
    while True:
        delta = random.random() * value_range - half_range
        yield round(start_value, precision)
        start_value += delta

# Use your random_delta function to generate temperature values
temperature_generator = random_delta(start_value=25, min_delta=-2, max_delta=2)
# pump_generator = random_delta(size=10, start_value=24, min_delta=-1, max_delta=1)
# ferti_generator = random_delta(size=10, start_value=80, min_delta=-1, max_delta=1)
# tank_generator = random_delta(size=10, start_value=258, min_delta=-1, max_delta=1)

while True:
    temperature = next(temperature_generator)
    # pump = next(pump_generator)
    # ferti = next(ferti_generator)
    # tank = next(tank_generator)

    message = f"{temperature:.2f}°C"
    # pump_message = f"{int(round(pump))}°C"
    # fertilizer_message = f"{int(round(ferti))}%"
    # tank_message = int(round(tank))


    # Insert temperature into MySQL
    sql = "INSERT INTO Temperature (Sensor_ID, Temperature) VALUES (%s, %s)"
    val = (sensor_id, temperature)
    mycursor.execute(sql, val)
    mydb.commit()

    # Publish temperature
    client.publish(topic, message)
    # client.publish(pump_topic, pump_message)
    # client.publish(fertilizer_topic, fertilizer_message)
    # client.publish(tank_topic, tank_message)

    print(f"Published: {message} to topic: {topic}")
    # print(f"Published: {pump_message} to topic: {pump_topic}")
    # print(f"Published: {fertilizer_message} to topic: {fertilizer_topic}")
    # print(f"Published: {tank_message} to topic: {tank_topic}")
    time.sleep(5)

client.loop_forever()