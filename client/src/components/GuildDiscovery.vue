<template>
  <div>
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
import _ from 'lodash'

export default {
  name: 'GuildDiscovery',
  data () {
    return {
      name: 'GuildDiscovery',
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
      showUserCorrelation: true
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
    filterByRace: function (race) {
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
          type: 'blanks'
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
      axios.get(`http://127.0.0.1:5000/` + path)
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
#grid-workspace {
  display: flex;
  width: 100%;
}

.is-text-centered {
  margin-left: auto;
  margin-right: auto;
}
</style>
