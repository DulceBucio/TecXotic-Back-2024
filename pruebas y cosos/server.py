from flask import Flask
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT Settings
MQTT_BROKER_URL = "localhost"
MQTT_BROKER_PORT = 1883  # Default MQTT port is 1883. Use 8883 for SSL
MQTT_USERNAME = ""  # Add if your broker requires username/password
MQTT_PASSWORD = ""  # Add if your broker requires username/password
MQTT_KEEPALIVE = 60  # Second

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("your/topic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload} on topic {msg.topic}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

if MQTT_USERNAME and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

mqtt_client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_KEEPALIVE)

# Start the loop in the background (non-blocking)
mqtt_client.loop_start()

@app.route('/')
def index():
    return "Hello, MQTT!"

@app.route('/publish')
def publish_message():
    # Example route to publish messages
    mqtt_client.publish("your/topic", "Hello from Flask!")
    return "Message published"

if __name__ == '__main__':
    app.run(debug=True)

