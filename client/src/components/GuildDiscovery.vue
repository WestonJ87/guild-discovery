<template>
  <div>
    <div id="filter-bar" class="level-right">
      <div class="field" style="margin-top:10px;">
        <label class="label is-small">By Race :</label>
        <div class="control">
          <div class="select is-small">
            <select @change="onSelectRaceFilter($event)">
                <option selected>Race/Planet</option>
                <option>Human/Syndesia</option>
                <option>Beastmen/Arboreus</option>
                <option>Demon/Tartaros</option>
            </select>
          </div>
        </div>
      </div>  
      <div class="field" style="margin-top:10px;">
        <label class="label is-small">By Participants :</label>
        <p class="control">
          <span> from </span> 
            <input @input="onMemberRangeFilter($event)" id="member-min" class="input small-input" type="text" placeholder="MIN">
          <span> to </span> 
            <input @input="onMemberRangeFilter($event)" id="member-max" class="input medium-input" type="text" placeholder="MAX">
          <span> members. </span>
        </p>
      </div>
      <div class="field is-grouped is-grouped-centered">
        <p class="control">
            <label class="label is-small">Total Points:</label>
            <input @input="onTotalPointsFilter($event)" id="total-points" class="input medium-input" type="text" placeholder="MIN">
        </p>
        <p class="control">
          <label class="label is-small">Average Points:</label>
          <input @input="onAveragePointsFilter($event)" id="average-points" class="input medium-input" type="text" placeholder="MIN">
        </p>
      </div>
    </div>
    <AgGridVue style="width:100%; height: 750px;" class="ag-theme-alpine"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :modules="modules"
        :gridOptions="gridOptions"
        @grid-ready="onReady">
    </AgGridVue>
  </div>
</template>

<script>

import axios from 'axios';

import { AgGridVue } from '@ag-grid-community/vue3'

import { AllCommunityModules } from '@ag-grid-community/all-modules';

import _ from 'lodash'

export default {
  name: 'GuildDiscovery',
  props: {},
  data () {
    return {
      name: 'GuildDiscovery',
      columnDefs: null,
      rowData: null,
      modules: AllCommunityModules
    }
  },
  components: {
    AgGridVue
  },
  beforeMount() {
    this.gridOptions = {};
    this.createColumnDefs();
    this.createRowData();
  },
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
  },
  methods: {
    hitServer: function (path) {
      axios.get(`http://127.0.0.1:5000` + path)
        .then((response) => {
          this.rowData = response.data;
        })
        .catch((error) => {
          this.$log.error("CONTEXT : " + this.name + " : ERROR :: " + error);
          return error;
        })
    },
    onReady() {
      this.gridOptions.api.sizeColumnsToFit();
    },
    clearFilters() {
      this.gridOptions.api.setFilterModel(null);
    },
    onSelectRaceFilter: _.debounce((event) => {
      console.log(event.target.value)
    }, 
    100),
    onMemberRangeFilter: _.debounce((event) => {
      console.log(event.target.value)
      var hardcodedFilter = {
        guildID: {
          type: 'greaterThan',
          filter: event.target.value
        }
      }
      this.gridOptions.api.setFilterModel(hardcodedFilter)
    }, 
    1000),
    onTotalPointsFilter: _.debounce((event) => {
      console.log(event.target.value)
    }, 
    1000),
    onAveragePointsFilter: _.debounce((event) => {
      console.log(event.target.value)
    }, 
    1000),
    numberFormatter(params) {
      if (params.value == 0) {
        return "--"
      } else if (typeof params.value !== "number") {
        return parseInt(params.value.replace(/,/g, ''));
      } else {
        return params.value
      }   
    },
    numberSort(num1, num2) {
      return num1 - num2;
    },
    createRowData() {
      // call flaskapp/guilds to get guilds stored in mongo
      this.hitServer('/guilds');
    },
    createColumnDefs() {
      this.columnDefs = [
        { 
          headerName: 'ID', 
          field: 'guildID',
          width: 110, 
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort
        },
        { 
          headerName: 'Guild Name', 
          field: 'name', 
          sortable: true
        },
        { 
          headerName: 'Master', 
          field: 'master', 
          sortable: true
        },
        { 
          headerName: 'Tag', 
          field: 'tag',
          width: 90,  
          sortable: true
        },
        { 
          headerName: 'Race', 
          field: 'race',
          filter: 'agTextColumnFilter',
          width: 120, 
          sortable: true
        },
        { 
          headerName: 'Members', 
          field: 'members',
          width: 150,  
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort
        },
        { 
          headerName: 'Total Points', 
          field: 'totalPoints', 
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort 
        },
        { 
          headerName: 'Average Points', 
          field: 'avgPoints', 
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort
        },
        { 
          headerName: 'Description', 
          field: 'description', 
          sortable: true
        },
        { 
          headerName: 'Lieutenants', 
          field: 'lieutenants', 
          sortable: true
        },
        { 
          headerName: 'Guild Members', 
          field: 'guildMembers', 
          sortable: true
        }
      ];
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
