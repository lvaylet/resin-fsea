import Vue from 'vue'
import App from './App.vue'
import VueMqtt from 'vue-mqtt'

// DEVELOPMENT
// Publish messages from MacOS with:
// $ brew install mosquitto
// $ mosquitto_pub -h iot.eclipse.org -t "/drone/position" -m "Hello from MacBook pro"
Vue.use(VueMqtt, 'ws://iot.eclipse.org:80/ws')

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
