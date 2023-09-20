import json
import random
import time
import schedule
import paho.mqtt.client as mqtt

# 1. Definición de constantes:
#    MQTT:
#    - IP MQTT
#    - Puerto MQTT
#    - Usuario MQTT
#    - Contraseña MQTT
#    - Topic suscriptor
#    - Topic publicador
#    Configuraciones:
#    - Intervalo de medición

# 2. Definición de funciones:
#    - Función de conexión MQTT
#    - Función de publicación a tópico
#    - Función de recepción de mensajes
#    - Función de procesar mensaje
#    - Función de medición de datos
#    - Función de desconexión MQTT
#    - Función principal

'''
Dirección IP y puerto del servidor MQTT
'''
MQTT_HOST = "3.83.206.45"  # "ip.maquina.mqtt"
MQTT_PORT = 8082

'''
Usuario y contraseña para la conexión MQTT
'''
MQTT_USER = "admin2"  # "UsuarioMQTT"
MQTT_PASSWORD = "admin2"  # "ContraseñaMQTT"


'''
Topicos de suscripción y publicación
'''
BASE_TOPIC = "colombia/cundinamarca/bogota/" + \
    MQTT_USER  # "<país>/<estado>/<ciudad>/" + MQTT_USER
MQTT_PUB_TOPIC = BASE_TOPIC + "/out"
MQTT_SUB_TOPIC = BASE_TOPIC + "/in"

'''
Intervalo de medición en segundos
'''
MEASURE_INTERVAL = 1

'''
Valor medio de la temperatura en grados Celsius
que el emulador genera y la variación de la temperatura
'''
TEMPERATURE_VALUE = 0.0
TEMPERATURE_VARIATION = 10.0

'''
Valor medio de la humedad en porcentaje
que el emulador genera y la variación de la humedad
'''
MOISTURE_VALUE = 60.0
MOISTURE_VARIATION = 5.0


def process_message(msg: str):
    '''
    Procesar mensaje recibido
    '''
    print("Procesando mensaje: " + msg)

    if ("ALERT" in msg and "record" in msg):
        print("############################################################")
        print("############################################################")
        print("############################################################")
        print("              NUEVO RECORD 🏆: {}            ".format(msg))
        print("############################################################")
        print("############################################################")
        print("############################################################")

    if ("ALERT" in msg):
        print("############################################################")
        print("############################################################")
        print("############################################################")
        print("              ALERTA: {}                     ".format(msg))
        print("############################################################")
        print("############################################################")
        print("############################################################")


def mqtt_publish(topic, msg):
    '''
    Publicar mensaje a tópico
    '''
    client.publish(topic, msg)


def measure_temperature():
    '''
    Función de medición de temperatura
    En emulación, estos datos son aleatorios con distribución uniforme
    desde el valor medio -variación hasta el valor medio +variación.
    Si se utilizara un sensor, acá se debería leer la temperatura real.
    '''
    min_value = TEMPERATURE_VALUE - TEMPERATURE_VARIATION
    max_value = TEMPERATURE_VALUE + TEMPERATURE_VARIATION
    return random.uniform(min_value, max_value)


def measure_moisture():
    '''
    Función de medición de humedad
    En emulación, estos datos son aleatorios con distribución uniforme
    desde el valor medio -variación hasta el valor medio +variación.
    Si se utilizara un sensor, acá se debería leer la humedad real.
    '''
    min_value = MOISTURE_VALUE - MOISTURE_VARIATION
    max_value = MOISTURE_VALUE + MOISTURE_VARIATION
    return random.uniform(min_value, max_value)


def on_connect(client, userdata, flags, rc):
    '''
    Función de conexión MQTT
    '''
    print("Connected with result: " + mqtt.connack_string(rc))
    client.subscribe(MQTT_SUB_TOPIC)


def on_message(client, userdata, msg):
    '''
    Función de recepción de mensajes
    '''
    data = msg.payload.decode("utf-8")
    print(msg.topic + ": " + str(data))
    process_message(data)


def on_disconnect(client, userdata, rc):
    '''
    Función de desconexión MQTT
    '''
    print("Disconnected with result: " + mqtt.connack_string(rc))


def mqtt_setup():
    '''
    Función de conexión MQTT
    '''
    global client
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()


def measure_data():
    '''
    Función de medición y envío de datos
    '''
    print("Midiendo...")
    temperature = measure_temperature()
    moisture = measure_moisture()
    print("\tTemperatura: {}°C".format(temperature))
    print("\tHumedad: {}%".format(moisture))
    mqtt_publish(MQTT_PUB_TOPIC, json.dumps({
        "temperatura": temperature,
        "humedad": moisture
    }))
    print("Datos enviados")


def start_measurement():
    '''
    Función que ejecuta cada intervalo de tiempo la medición de datos
    '''
    schedule.every(MEASURE_INTERVAL).seconds.do(measure_data)
    while True:
        schedule.run_pending()
        time.sleep(1)


client = None

mqtt_setup()
start_measurement()
