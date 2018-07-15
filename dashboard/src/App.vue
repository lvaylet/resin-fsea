<template>
  <div id="app">
    <h1>Fleet Management Dashboard</h1>
    <subscriber></subscriber>
  </div>
</template>

<script>
import Subscriber from './components/Subscriber.vue'

export default {
  name: 'app',
  components: {
    Subscriber
  },
  mounted () {
    this.$mqtt.subscribe('drone/position')
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
