#config
import json

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_SENSOR = "lab/energia/blocoA/sensor01"
TOPIC_COMANDO = "lab/energia/blocoA/comando"

LIMITE_POTENCIA = 1000.0 #W

def on_connect(client, userdata, flags, reason_code, properties):
  print("[Central]Conectada ao Broker! Monitorando...")
  client.subscribe(TOPIC_SENSOR)

def on_message(client, userdata, msg):
  try:
    payload = json.loads(msg.payload.decode())
    potencia = payload["potencia_W"]
    status = payload["status"]

    print(f"Monitor: {potencia}W | Status atual: {status}")

    #se ligado e > que limite, corta
    if status == "LIGADO" and potencia > LIMITE_POTENCIA:
      print(f"Alerta: consumo de {potencia}W excedeu o limite! Cortando carga...")
      client.publish(TOPIC_COMANDO, "DESLIGAR")

  except Exception as e:
    print("Erro ao ler dados:", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Central_Supervisoria_ID_999")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()















