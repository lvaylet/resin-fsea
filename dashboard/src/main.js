import Vue from 'vue'
import App from './App.vue'
import VueMqtt from 'vue-mqtt'

// Connect to MQTT broker
// ---
// DEVELOPMENT
// Publish messages from MacOS with:
// $ brew install mosquitto
// $ mosquitto_pub -h iot.eclipse.org -t "/drone/position" -m "{"ts": [1531604906], "uuid": "7ebf7ece-1332-44ad-8f3a-db72245eded5", "name": "drone1", "latitude": 48.85150569993735, "longitude": 2.2119310978842477}"
Vue.use(VueMqtt, 'ws://iot.eclipse.org:80/ws')

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
