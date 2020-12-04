<template>
  <div id="discovery-workspace" 
    v-bind:style="{ 
      backgroundImage: 'url(https://assets.fracturedmmo.com/images/universe_feature_' + raceImageIndex + '.jpg)' 
      }">
    <GuildFilterPanel
      @filter-by-race="filterByRace"
      @filter-by-participants="filterByMembers"
      @filter-by-points="filterByPoints"
      @user-correlation-survey-complete="storeAndSubmitUserCorrelation"
      @close-correlation-form="turnOffCorrelationForm"
      @get-user-correlations="getCorrelationForUser"
      @launch-user-survey="launchUserSurvey"
      @show-hide-single-member="showHideSingleMemberGuilds"
      @show-hide-guilds-wo-desc="showHideGuildsWithoutDescription"
      @hide-compatibility-scores="showHideCompatibilityScores"
      @reset-filters="resetFilters"
      :showUserCorrelationForm="showUserCorrelationForm"
      :isDetailsPanelVisible="isDetailsPanelVisible">
    </GuildFilterPanel>
    <div id="grid-workspace">
      <GuildsTable
        id="grid-table"
        ref="GuildsTable"
        @hit-server="hitServer"
        @launch-guild-details="showDetailsForGuild"
        @show-user-correlation="showHideCompatibilityScores"
        :allGuildsData="allGuildsData"
        :userCorrelationMap="userCorrelationMap"
        :showUserCorrelation="showUserCorrelation"
        :raceFilterObject="raceFilterObject"
        :membersFilterObject="membersFilterObject"
        :pointsFilterObject="pointsFilterObject"
        :descriptionFilterObject="descriptionFilterObject"
        :isDetailsPanelVisible="isDetailsPanelVisible">
      </GuildsTable>
      <GuildDetailsPanel v-if="isDetailsPanelVisible"
        id="guild-detail-panel"
        @close-details-panel="closeDetailPanel"
        :selectedGuild="selectedGuild">
      </GuildDetailsPanel>
    </div>
  </div>
</template>

<script>
import GuildFilterPanel from './GuildFilterPanel'
import GuildDetailsPanel from './GuildDetailsPanel'
import GuildsTable from './GuildsTable'

import axios from 'axios';
import _ from 'lodash';

export default {
  name: 'GuildDiscovery',
  data () {
    return {
      name: 'GuildDiscovery',
      baseURL: 'http://ec2-54-160-106-66.compute-1.amazonaws.com:5000',
      isDetailsPanelVisible: false,
      allGuildsData: null,
      raceFilterObject: null,
      membersFilterObject: null,
      pointsFilterObject: null,
      descriptionFilterObject: null,
      selectedGuild: null,
      membersMinimum: null,
      membersMaximum: null,
      userCorrelationMap: null,
      showUserCorrelationForm: false,
      showUserCorrelation: true,
      raceImageIndex: '01'
    }
  },
  components: {
    GuildFilterPanel,
    GuildDetailsPanel,
    GuildsTable
  },
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
  },
  watch: {
    userCorrelationMap: function (newVal) {
      if (newVal) {
        this.allGuildsData = [...this.allGuildsData.concat(this.userCorrelationMap).reduce((m, o) => 
          m.set(o.guildID, Object.assign(m.get(o.guildID) || {}, o))
        , new Map()).values()];
      }
    }
  },
  methods: {
    showDetailsForGuild: function (id) {
      this.$log.info("SHOW DETAILS FOR GUILD :: ", id)
      this.isDetailsPanelVisible = true;
      this.selectedGuild = this.allGuildsData.find(guild => guild.guildID == id) // Get Guild by ID and show details panel constructed from info.
    },
    resetFilters: function () {
      this.$refs.GuildsTable.clearFilters();
    },
    updateRaceBackgroundImageIndex: function (race) {
      switch(race) {
        case "":
          this.raceImageIndex = '01';
          break;
        case "Human":
          this.raceImageIndex = '02';
          break;
        case "Beastman":
          this.raceImageIndex = '03';
          break;
        case "Demon":
          this.raceImageIndex = '04';
          break;
      }
    },
    filterByRace: function (race) {
      this.updateRaceBackgroundImageIndex(race);
      this.raceFilterObject = {
        filterType: 'text',
        type: 'Equals',
        filter: race
      }
    },
    filterByMembers: function (typeAndAmount) {
      // First set current values for min and max # of members for guild.
      if (typeAndAmount.type == 'min') {
        this.membersMinimum = typeAndAmount.value
      } else if (typeAndAmount.type == 'max') {
        this.membersMaximum = typeAndAmount.value
      }

      if (this.membersMinimum && this.membersMaximum) {
        this.membersFilterObject = {
          filterType: 'number',
          type: 'inRange',
          filter: this.membersMinimum,
          filterTo: this.membersMaximum
        }
      } else {
        this.membersFilterObject = {
          filterType: 'number',
          type: typeAndAmount.type == 'max' ? 'lessThan' : 'greaterThan',
          filter: typeAndAmount.type == 'max' ? this.membersMaximum : this.membersMinimum
        }
      }
    },
    filterByPoints: function (typeAndAmount) {
      this.pointsFilterObject = {
        type: typeAndAmount.type,
        filterObject: {
          filterType: 'number',
          type: 'greaterThan',
          filter: typeAndAmount.value
        }
      }
    },
    showHideSingleMemberGuilds: function (showHide) {
      if (showHide) {
        this.filterByMembers({ type: 'min', value: 1 });
      } else {
        // reset
      }
    },
    showHideGuildsWithoutDescription: function (showHide) {
       if (showHide) {
        this.descriptionFilterObject = {
          filterType: 'text',
          type: 'empty',
          includeBlanksInEquals: false
        }
      } else {
        // unhide
      }
    },
    showHideCompatibilityScores: function (showHide) {
      this.showUserCorrelation = showHide;
    },
    turnOffCorrelationForm: function () {
      this.showUserCorrelationForm = false;
    },
    launchUserSurvey: function () {
      this.showUserCorrelationForm = true;
    },
    getCorrelationForUser: function () {
      this.hitServer('user-correlations')
    },
    closeDetailPanel: function () {
      this.isDetailsPanelVisible = false;
      this.$refs.GuildsTable.sizeToFit();
    },
    storeAndSubmitUserCorrelation: function (results) {
      localStorage.surveyResults = results;
    },
    hitServer: function (path) {
      axios.get(this.baseURL + `/api/` + path)
        .then((response) => {
          if (response.data.AllGuilds) {
            this.allGuildsData = response.data.AllGuilds;
          } else if (response.data.UserCorrelation) {
            this.userCorrelationMap = response.data.UserCorrelation;
          }else {
            this.$log.info(response.data);
          }
        })
        .catch((error) => {
          this.$log.error("CONTEXT : " + this.name + " : ERROR :: " + error);
          return error;
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
#discovery-workspace {
  background-position: 0% -30%;
  background-repeat: repeat-y;
  webkit-transition: background-image 0.5s ease-in-out;
  transition: background-image 0.5s ease-in-out;
}

#grid-workspace {
  display: flex;
  width: 100%;
  max-height: 105vh;
}

#grid-table {
  height: 83vh;
}

#guild-detail-panel {
  margin-left: 1vw;
  width: 27vw;
  max-height: 84vh;
  overflow: scroll;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
  margin-bottom: 50px;
}

#guild-detail-panel::-webkit-scrollbar {
  display: none;
}

.is-text-centered {
  margin-left: auto;
  margin-right: auto;
}
</style>
