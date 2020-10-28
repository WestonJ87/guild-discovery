<template>
  <div id="guild-details">
    <article class="message">
      <div class="guild-details-header message-header">
        Guild Details - {{ selectedGuild.name }}
        <button @click="closeDetails" class="delete"></button>
      </div>
      <div class="message-body">
        <div id="guild_details">
          <section class="section">
            <div class="container">
              <span>
                <label class="label is-small">name :</label>
                <h5 class="title">{{ selectedGuild.name }}</h5>
              </span>
              <label class="label is-small">description :</label>
              <h6 class="subtitle description">{{ selectedGuild.description }}</h6>
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
            </div>
          </section>
        </div>
        <div id="banner_displayer" v-html="selectedGuild.bannerDisplayTemplate" style="text-align: center;">
        </div>
      </div>
    </article>
    <article class="message lieutenants">
      <div class="message-body">
        <div v-for="(member, index) in selectedGuild.lieutenants" v-bind:key="index">
          <p>{{ member }}</p>
        </div>
      </div>
    </article>
    <article class="message guild-members">
      <div class="message-body">
        <div v-for="(member, index) in selectedGuild.guildMembers" v-bind:key="index">
          <p>{{ member }}</p>
        </div>
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

.message {
  background-color: #F5F5F5;
}

.message-body {
  display: flex;
  width: 100%;
}

#guild_details {
  width: 90%;
  margin-top: -40px;
  margin-left: -30px;
  margin-bottom: -40px;
  margin-right: -60px;
  padding: -50px;
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
  width: 30%;
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
