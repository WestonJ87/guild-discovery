<template>
    <div id="filter-bar">
      <div class="level-right">
        <div class="field" style="margin-bottom: -25px;">
          <label style="margin-top:-5px;" class="checkbox is-size-7 is-pulled-left">
            hide single member guilds :   
            <input type="checkbox">
          </label>
        </div>
        <div class="field" style="margin-bottom: -25px;">
          <label style="margin-top:-5px;" class="checkbox is-size-7 is-pulled-left">
            hide no description guilds :   
            <input type="checkbox">
          </label>
        </div>
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
</template>

<script>
import _ from 'lodash'

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
    }
  },
  props: [ 'isDetailsPanelVisible' ],
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
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
    }, 500)
  },
  methods: {
      resetFilters: function () {
        this.$emit('reset-filters');
        this.race = "";
        this.minimumMembers = "";
        this.maximumMembers = "";
        this.minimumTotalPoints = "";
        this.minimumAveragePoints = "";
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
  }
}
</script>

<style scoped lang="scss">
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
</style>
