const mqtt = require('mqtt')

// Connect to the broker over WebSocket
const client = mqtt.connect('ws://192.168.5.1:1883')

client.on('connect', function () {
  console.log('Connected to MQTT broker')
  client.subscribe('your/topic', function (err) {
    if (!err) {
      console.log('Subscribed to topic')
    }
  })
})

client.on('message', function (topic, message) {
  // message is a Buffer
  console.log(topic, message.toString())
})

// Example of publishing a message
function publishMessage(topic, message) {
  client.publish(topic, message)
}
