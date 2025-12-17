# Simulação de otimização energética em Smart Grid com MQTT

### 1.  Objetivo
Projeto desenvolvido para praticar, de maneira introdutória, o protocolo MQTT e seu modelo de comunicação Pub/Sub.

### 2.  Arquitetura
- Protocolo: MQTT  
- Componentes:  
&rarr; Broker: serviço MQTT público  
&rarr; Edge (dispositivo virtual): simula o sensor de potência e atua como Publisher (publica leituras) e Subscriber (recebe comandos)  
&rarr; Central de controle (backend): atua como Subscriber (assina leituras), implementa a lógica de negócios e age como Publisher (publica comandos de corte)  

### 3.  Lógica de controle
- Estratégia: sistema implementa um laço de controle de segurança
- Regra de negócio: se o valor reportado ultrapassar o limite, a central de controle publica a mensagem "DESLIGAR", cortando a carga remotamente

### 4.  Tecnologias
- Linguagem: Python 3.x
- Biblioteca: paho-mqtt  
- Configuração do ambiente:
~~~python
# Criação do ambiente virtual
python3 -m venv venv

# Ativação do ambiente
source venv/bin/activate

# Instalação das dependências
pip install -r src/central_controle/requisitos.txt
~~~

### 5.  Rodando o projeto 
1. Abrir o terminal 1 e simular o Edge: ```python src/dispositivos/sensor_virtual_01.py```  
2. Abrir o terminal 2 e iniciar o sistema de supervisão: ```python src/dispositivos/central_controle.py```  
