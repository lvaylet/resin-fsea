<template>
  <div id="app">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Fleet Management
          </h1>
          <h2 class="subtitle">
            Real-time geo-location and speed of your drones
          </h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <subscriber></subscriber>
      </div>
    </section>
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

<style lang="scss">
  @import '~bulma/bulma.sass';
</style>
