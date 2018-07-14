var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://mqtt-broker')  // use service name from docker-compose.yml, automatically resolved by Docker

const MQTT_TOPIC = '/drone/position'

client.on('connect', function () {
  console.log('Connected to MQTT broker.')
  console.log('Subscribing to topic [' + MQTT_TOPIC + ']...')
  client.subscribe(MQTT_TOPIC)
  console.log('Successfully subscribed to topic [' + MQTT_TOPIC + '].')
})

client.on('message', function (topic, message) {
  console.log(topic, message.toString())
})
