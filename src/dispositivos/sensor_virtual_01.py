# código que substitui o microcontrolador
import json
import random
import time

import paho.mqtt.client as mqtt

# config
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_PUB = "lab/energia/blocoA/sensor01"
TOPIC_SUB = "lab/energia/blocoA/comando"

# estado inicial
estado_carga = True


# quando o script conecta ao broker
def on_connect(client, userdata, flags, reason_code, properties):
  print(f"[Sensor Virtual] Conectado ao Broker! (Cod: {reason_code})")
  client.subscribe(TOPIC_SUB)  # escuta comandos


# quando recebe mensagem de comando
def on_message(client, userdata, msg):
  global estado_carga
  comando = msg.payload.decode().upper()

  print(f"[Comando Recebido] {comando}")

  if comando == "DESLIGAR":
    estado_carga = False
    print("Carga foi desligada remotamente")
  elif comando == "LIGAR":
    estado_carga = True
    print("Carga foi ligada remotamente")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Sensor_Virtual_ID_Unico_123")
client.on_connect = on_connect
client.on_message = on_message

print("Iniciando simulação de hardware...")
client.connect(BROKER, PORT, 60)
client.loop_start()  # escuta em segundo plano

# loop principal de envio de dados
try:
  while True:
    if estado_carga:
      corrente = round(random.uniform(4.8, 5.5), 2)
      potencia = round(corrente * 220, 2)
    else:
      corrente = 0.0
      potencia = 0.0

    payload_dict = {
      "id": "sensor_01",
      "corrente_A": corrente,
      "potencia_W": potencia,
      "status": "LIGADO" if estado_carga else "DESLIGADO"
    }
    payload_json = json.dumps(payload_dict)

    # publica no tópico
    client.publish(TOPIC_PUB, payload_json)
    print(f"[Dados enviados] {payload_json}")

    time.sleep(2)  # envia a cada 2s

except KeyboardInterrupt:
  print("\nSimulação encerrada")
  client.loop_stop()
  client.disconnect()
