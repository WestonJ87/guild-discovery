<template>
    <AgGridVue style="height: 750px;"
        :class="isDetailsPanelVisible ? 'minimized' : 'full-display'" class="ag-theme-alpine"
        :columnDefs="columnDefs"
        :rowData="rowData"
        :modules="modules"
        :gridOptions="gridOptions"
        @grid-ready="onReady"
        @click="monitorClicks">
    </AgGridVue>
</template>

<script>

import { AgGridVue } from '@ag-grid-community/vue3'

import { AllCommunityModules } from '@ag-grid-community/all-modules';

export default {
  name: 'GuildsTable',
  data () {
    return {
      name: 'GuildsTable',
      columnDefs: null,
      rowData: null,
      modules: AllCommunityModules
    }
  },
  props: [ 'isDetailsPanelVisible', 'allGuildsData', 'raceFilterObject', 'membersFilterObject', 'pointsFilterObject', 'descriptionFilterObject' ],
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
  watch: { 
    allGuildsData: function(newVal) {
      this.rowData = newVal;
    },
    raceFilterObject: function(newVal) {
      this.updateFilter('race', newVal);
    },
    membersFilterObject: function(newVal) {
      this.updateFilter('members', newVal);
    },
    pointsFilterObject: function(newVal) {
      this.updateFilter(newVal.type == 'total' ? 'totalPoints' : 'avgPoints', newVal.filterObject);
    },
    descriptionFilterObject: function(newVal) {
      this.updateFilter('description', newVal);
    }
  },
  methods: {
    onReady() {
        this.gridOptions.api.sizeColumnsToFit();
    },
    monitorClicks(e) {
        if (e.target.matches('.guild-info, i')) {
            this.$emit('launch-guild-details', e.target.parentElement.innerText);
            this.sizeToFit();
        }
    },
    sizeToFit() {
      setTimeout(() => { 
        this.gridOptions.api.sizeColumnsToFit(); 
      }, 50);
      
    },
    updateFilter(field, newVal) {
      var filterInstance = this.gridOptions.api.getFilterInstance(field);
      filterInstance.setModel(newVal);
      this.gridOptions.api.onFilterChanged();
      console.log(this.gridOptions.api.getFilterModel());
    },
    clearFilters() {
      this.gridOptions.api.setFilterModel(null);
    },
    memberCellRenderer(params) {
      return `<a href="https://fracturedmmo.com/hero-profile/user/${params.value}/" target="_blank"> ${params.value} </a>`
    },
    guildCellRenderer(params) {
      return `<p style="width:100%;"><i style="float:left; margin-top:15px;" class="fas fa-info-circle guild-info"></i>${params.value}</p>`
    },
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
      // emit instead
      this.$emit('hit-server', 'guilds');
    },
    createColumnDefs() {
      this.columnDefs = [
        { 
          headerName: 'ID', 
          field: 'guildID',
          sortable: true,
          width: 100,
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          cellRenderer: this.guildCellRenderer,
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
          cellRenderer: this.memberCellRenderer, 
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
          width: 90,  
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort
        },
        { 
          headerName: 'Total Points',
          width: 100, 
          field: 'totalPoints', 
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort 
        },
        { 
          headerName: 'Average Points',
          width: 120, 
          field: 'avgPoints', 
          sortable: true, 
          type: 'numericColumn',
          filter: 'agNumberColumnFilter',
          valueFormatter: this.numberFormatter,
          comparator: this.numberSort
        },
        { 
          headerName: 'Description',
          width: 450,
          field: 'description', 
          sortable: true
        }
      ];
    }
  }
}
</script>

<style scoped lang="scss">
  .minimized {
    width: 70%;
  }

  .full-display {
    width: 100%
  }
</style>
