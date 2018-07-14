<template>
  <div class="sub">
    <ul>
      <li v-for="message in messages" :key="message">
        {{ message }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data () {
    return {
      messages: []
    }
  },
  mqtt: {
    'drone/position' (data) {
      let message = String.fromCharCode.apply(null, data)
      this.messages.push(message)
    }
  }
}
</script>

<style>
.sub {
  width: 100%;
  border: 1px solid #ccc;
  margin: 20px 1%;
  padding: 20px 0;
}
.sub ul {
  list-style-type: none;
}
</style>
