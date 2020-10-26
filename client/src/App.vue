<template>
  <GuildDiscovery/>
</template>

<script>
import GuildDiscovery from './components/GuildDiscovery.vue'

export default {
  name: 'App',
  components: {
    GuildDiscovery
  }
}
</script>

<style lang="scss">
@import '~@/styles/global.scss';

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
