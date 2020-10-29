<template>
  <div id="guild-details">
    <article class="message">
      <div class="guild-details-header message-header">
        Guild Details - {{ selectedGuild.name }}
        <button @click="closeDetails" class="delete"></button>
      </div>
      <div class="message-body">
        <div id="banner_displayer" v-html="selectedGuild.bannerDisplayTemplate" style="text-align: center;"></div>
        <div class="container details-columns">
          <div class="container column">
            <span>
              <label class="label is-small">Tag :</label>
              <p class="value">{{ selectedGuild.tag }}</p>
            </span>
            <span>
              <label class="label is-small">Race :</label>
              <p class="value">{{ selectedGuild.race }}</p>
            </span>
            <span>
              <label class="label is-small">Master :</label>
              <p class="value">{{ selectedGuild.master }}</p>
            </span>
            <span>
              <label class="label is-small">Members :</label>
              <p class="value">{{ selectedGuild.members }}</p>
            </span>
          </div>
          <div class="container column">
            <h5 class="foundation-scores-header">FOUNDATION SCORES</h5>
            <span>
              <label class="label is-small">Total Points :</label>
              <p class="value">{{ selectedGuild.totalPoints }}</p>
            </span>
            <span>
              <label class="label is-small">Average Points :</label>
              <p class="value">{{ selectedGuild.avgPoints }}</p>
            </span>
          </div>
        </div>
        <div v-if="selectedGuild.description" class="container">
          <section class="section">
            <div class="container">
              <label class="label is-small">description :</label>
              <h6 class="subtitle description">{{ selectedGuild.description }}</h6>
            </div>
          </section>
        </div>
      </div>
    </article>
    <article class="message is-small lieutenants">
      <div class="message-header">
        <h3> Lieutenants </h3>
      </div>
      <div class="message-body memberslist tags is-centered">
        <span class="tag" v-for="(member, index) in selectedGuild.lieutenants" v-bind:key="index">
          {{ member }}
        </span>
      </div>
    </article>
    <article class="message is-small guild-members">
      <div class="message-header">
        <h3> Guild Members </h3>
      </div>
      <div class="message-body memberslist tags is-centered">
        <span class="tag" v-for="(member, index) in selectedGuild.guildMembers" v-bind:key="index">
          {{ member }}
        </span>
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: 'GuildDetailsPanel',
  props: [ 'selectedGuild' ],
  data () {
    return {
      name: 'GuildDetailsPanel'
    }
  },
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
  },
  methods: {
    closeDetails() {
      this.$emit('close-details-panel');
    }
  }
}
</script>

<style scoped lang="scss">
#guild-details {
  width: 30%;
  padding: 10px;
}

.section {
  margin: -50px;
  margin-left: -25px;
  margin-right: -100px;
}

.description {
  margin-right: -70px;
}

.message {
  background-color: #F5F5F5;
}

.message-body {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.memberslist {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.memberslist > span {
  margin: -1px;
}

.foundation-scores-header {
  margin-top: -10px;
  font-size: 0.7em;
  margin-bottom: 10px;
}

.description {
  font-size: 0.9em;
}

.details-columns {
  display: flex;
  width: 100%;
  margin-left: -5px;
  margin-right: -55px;
}

.column {
  width: 50%;
}

span {
  display: flex;
}

span > h5,h6,p {
  font-size: 0.8em;
  margin-left: 10px;
}

#guild_details > section > .container > span > .title {
  font-size: 1.2em;
}

.section {
  width: 100%;
}

#banner_displayer {
  width: 60%;
  margin-left: 60px;
  transform: scale(0.9);
}

/deep/ #banner_displayer::after {
  background: radial-gradient(ellipse at center, rgba(245,245,245, 0) 0%,rgba(245,245,245, 0.5) 70%,rgba(245,245,245, 1) 100%) !important;
}

/deep/ .guild-banner-color {
    position: absolute;
    width: 100%;
    padding-top: 150%;
    background-image: url(https://assets.fracturedmmo.com/images/guild_banner_colors.jpg);
    background-size: cover;
}

/deep/ .guild-banner-shape {
    position: absolute;
    width: 100%;
    padding-top: 150%;
    background-image: url(https://assets.fracturedmmo.com/images/guild_banner_shapes01.png);
    background-size: cover;
}

/deep/ .guild-banner-symbol {
    position: absolute;
    width: 100%;
    padding-top: 150%;
    background-size: cover;
}

/deep/ .guild-banner-spacer {
    width: 100%;
    padding-top: 150%;
}
</style>
