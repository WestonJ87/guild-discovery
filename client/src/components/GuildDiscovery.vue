<template>
  <div>
    <GuildFilterPanel
      @filter-by-race="filterByRace"
      @filter-by-participants="filterByMembers"
      @filter-by-points="filterByPoints"
      @reset-filters="resetFilters"
      :isDetailsPanelVisible="isDetailsPanelVisible">
    </GuildFilterPanel>
    <div id="grid-workspace">
      <GuildsTable
        ref="GuildsTable"
        @hit-server="hitServer"
        @launch-guild-details="showDetailsForGuild"
        :allGuildsData="allGuildsData"
        :raceFilterObject="raceFilterObject"
        :membersFilterObject="membersFilterObject"
        :pointsFilterObject="pointsFilterObject"
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
      selectedGuild: null,
      membersMinimum: null,
      membersMaximum: null
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
  methods: {
    hitServer: function (path) {
      axios.get(`http://127.0.0.1:5000/` + path)
        .then((response) => {
          this.allGuildsData = response.data;
        })
        .catch((error) => {
          this.$log.error("CONTEXT : " + this.name + " : ERROR :: " + error);
          return error;
        })
    },
    showDetailsForGuild: function (id) {
      console.log("SHOW DETAILS FOR GUILD :: ", id)
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
    closeDetailPanel: function () {
      this.isDetailsPanelVisible = false;
      this.$refs.GuildsTable.sizeToFit();
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
</style>
