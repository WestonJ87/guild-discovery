<template>
    <div id="filter-bar" class="has-text-white">
      <div id="genius-tab">
        <div id="user-survey-form-btn" class="field">
            <a @click="launchUserSurvey" 
              :class="{'is-danger' : !userCorrelationFormCompleted}"
              class="button"> {{ !userCorrelationFormCompleted ? 'Find my Guild Match' : 'Redo guild dating profile' }}
              <img v-if="userCorrelationFormCompleted" id="cupid" src="@/images/cupid-black.png"/>
              <img v-if="!userCorrelationFormCompleted" id="cupid" src="@/images/cupid-white.png"/>
            </a>
        </div>
        <div id="generate-user-correlation-btn" class="field">
          <a @click="getCorrelationsForUser" v-if="userCorrelationFormCompleted"
            class="button"> Request Match(s)
            <img v-if="userCorrelationFormCompleted" id="wifi" src="@/images/search-love.png"/>
          </a>
        </div>
      </div>
      <QuestionaireModal
          @user-correlation-survey-complete="userCorrelationSurveyComplete"
          @close-correlation-form="closeUserCorrelationForm"
          :userCorrelationFormCompleted="userCorrelationFormCompleted"
          :showUserCorrelationForm="showUserCorrelationForm">
      </QuestionaireModal>
      <div class="level-right" style="margin-top: -60px;">
        <div class="field" style="margin-bottom: -100px; margin-right: 250px;">
          <label disabled style="margin-top:-5px;" class="checkbox is-size-7 is-pulled-left">
            <b style="font-size: 1.2em; color: #ccc!important;">hide compatibility : </b>  
            <input disabled v-model="hideCompatibility" type="checkbox">
          </label>
        </div>
        <div class="field" style="margin-bottom: -100px;">
          <label style="margin-top:-5px;" class="checkbox is-size-7 is-pulled-left">
            hide single member guilds :   
            <input v-model="hideSingleMemberGuilds" type="checkbox" data-testid="hide-single-member-guilds-checkbox">
          </label>
        </div>
        <div class="field" style="margin-bottom: -100px;">
          <label disabled style="margin-top:-5px; color: #ccc!important;" class="checkbox is-size-7 is-pulled-left">
            hide no description guilds :   
            <input disabled v-model="hideGuildsWithoutDescription" type="checkbox">
          </label>
        </div>
      </div>
      <div class="level">
        <div class="level-left">
          <figure class="image is-text-centered">
            <img id="app-logo" src="@/images/fractured-logo.png"/>
          </figure>
        </div>
      </div>
      <div class="level">
        <div class="level-left">
        </div>
        <div class="level-right">
          <div class="field" style="margin-top:5px;">
            <a class="control">
              <p class="label is-small">RESET </p><button @click="resetFilters" style="margin-left: 8px !important;" class="delete"></button>
            </a>
          </div>
          <div class="field" style="margin-top:10px;">
            <label class="label is-small">By Race :</label>
            <div class="control">
                <div class="select is-small">
                <select v-model="race">
                    <option value=""> Race/Planet </option>
                    <option value="Human"> Human/Syndesia </option>
                    <option value="Beastman"> Beastmen/Arboreus </option>
                    <option value="Demon"> Demon/Tartaros </option>
                </select>
                </div>
            </div>
          </div>  
          <div class="field" style="margin-top:10px;">
          <label class="label is-small">By Participants :</label>
          <p class="control">
              <span> from </span> 
              <input v-model="minimumMembers" id="member-min" class="input small-input" type="text" placeholder="MIN">
              <span> to </span> 
              <input v-model="maximumMembers" id="member-max" class="input medium-input" type="text" placeholder="MAX">
              <span> members. </span>
          </p>
          </div>
          <div class="field is-grouped is-grouped-centered">
          <p class="control">
              <label class="label is-small">Total Points:</label>
              <input v-model="minimumTotalPoints" id="total-points" class="input medium-input" type="text" placeholder="MIN">
          </p>
          <p class="control">
              <label class="label is-small">Average Points:</label>
              <input v-model="minimumAveragePoints" id="average-points" class="input medium-input" type="text" placeholder="MIN">
          </p>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import _ from 'lodash'

import QuestionaireModal from './QuestionaireModal'

export default {
  name: 'GuildFilterPanel',
  data () {
    return {
      name: 'GuildFilterPanel',
      race: "",
      minimumMembers: "",
      maximumMembers: "",
      minimumTotalPoints: "",
      minimumAveragePoints: "",
      hideCompatibility: "",
      hideSingleMemberGuilds: "",
      hideGuildsWithoutDescription: "",
      userCorrelationFormCompleted: false
    }
  },
  props: [ 'isDetailsPanelVisible', 'showUserCorrelationForm'],
  components: {
    QuestionaireModal
  },
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
    if (localStorage.surveyResults) {
      this.userCorrelationFormCompleted = true;
    }
  },
  watch: {
    race: function() {
      this.onSelectRaceFilter();
    },
    minimumMembers: _.debounce(function(newVal){
      this.onMemberRangeFilter('min', newVal);
    }, 500),
    maximumMembers: _.debounce(function(newVal){
      this.onMemberRangeFilter('max', newVal);
    }, 500),
    minimumTotalPoints: _.debounce(function(newVal){
      this.onPointsFilter('total', newVal);
    }, 500),
    minimumAveragePoints: _.debounce(function(newVal){
      this.onPointsFilter('average', newVal);
    }, 500),
    hideSingleMemberGuilds: function () {
      this.minimumMembers = "";
      this.maximumMembers = "";
      this.$emit('show-hide-single-member', this.hideSingleMemberGuilds);
    },
    hideGuildsWithoutDescription: function () {
      this.$emit('show-hide-guilds-wo-desc', this.hideGuildsWithoutDescription);
    },
    hideCompatibility: function () {
      this.$emit('hide-compatibility-scores', this.hideCompatibility);
    }
  },
  methods: {
      resetFilters: function () {
        this.$emit('reset-filters');
        this.race = "";
        this.minimumMembers = "";
        this.maximumMembers = "";
        this.minimumTotalPoints = "";
        this.minimumAveragePoints = "";
        this.hideSingleMemberGuilds = false;
        this.hideGuildsWithoutDescription = false;
      },
      closeUserCorrelationForm: function() {
        this.$emit('close-correlation-form');
      },
      launchUserSurvey: function () {
        if (this.userCorrelationFormCompleted) {
          this.userCorrelationFormCompleted = false;
        }
        this.$emit('launch-user-survey');
      },
      getCorrelationsForUser: function () {
        this.$emit('get-user-correlations', 'user-correlations');
      },
      onSelectRaceFilter: function () { 
        this.$emit('filter-by-race', this.race); 
      },
      onMemberRangeFilter: function (MinOrMax, value) { 
        this.$emit('filter-by-participants', { type: MinOrMax, value: value }); 
      },
      onPointsFilter: function (type, value) { 
        this.$emit('filter-by-points', { type: type, value: value }); 
      },
      userCorrelationSurveyComplete: function (results) {
        this.$emit('user-correlation-survey-complete', results);
        this.userCorrelationFormCompleted = true;
      }
  }
}
</script>

<style scoped lang="scss">
#filter-bar {
  margin-bottom: 20px;
}

#app-logo {
  margin-left: 20px;
  width: 550px;
  margin-bottom: -200px;
}

#wifi, #cupid {
  padding: 5px;
  margin-top: 5px;
  margin-left: 10px;
  margin-right: -15px;
  max-height: 45px;
}

#genius-tab {
  position: absolute;
  top: 0;
  left: 40%;
  width: 285px;
  height: 285px;
  background-repeat: no-repeat;
  background-size: 300px 300px;
  background-image: url("../images/match-genius-tab-disabled.png");
  text-align: center;
  transform: translateY(-200px);
  z-index: 100;
}

// #genius-tab:hover {
//   animation-name: show-genius-tab;
//   animation-duration: 0.1s;
//   animation-timing-function: linear;
//   animation-fill-mode: forwards;
// }

@keyframes show-genius-tab {
  from {
    transform: translateY(-200px);
  }
  to {
    transform: translateY(0px);
  }
}

#genius-tab a {
  margin: 0 auto;
}

#cupid {
  transform: rotate(15deg);
  padding: 5px;
  margin-left: -3px;
}

#wifi {
  padding: 6px;
  margin-bottom: 2px;
  filter: brightness(25%);
}

#user-survey-form-btn, #generate-user-correlation-btn  {
  max-width: 260px;
  margin-left: 22px;
}

#user-survey-form-btn {
  margin-top: 5px;
}

#generate-user-correlation-btn {
  margin-top: -25px;
}

.small-input {
  width: 60px;
  height: 25px;
}

.medium-input {
  width: 100px;
  height: 25px;
}

.thin-select {
  height: 35px;
}
.field {
  padding: 10px;
}

.label {
  color: #fff!important;
}
</style>
