<template>
  <ag-grid-vue class="ag-theme-alpine"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :modules="modules">
  </ag-grid-vue>
</template>

<script>

import axios from 'axios';

import AgGridVue from '@ag-grid-community/vue3'

import {AllCommunityModules} from '@ag-grid-community/all-modules';

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
    this.columnDefs = [
      { headerName: 'Guild ID', field: 'guildID' },
      { headerName: 'Guild Name', field: 'name' },
      { headerName: 'Master', field: 'master' },
      { headerName: 'Tag', field: 'tag' },
      { headerName: 'Race', field: 'Race' },
      { headerName: 'Members', field: 'members' },
      { headerName: 'Total Points', field: 'totalPoints' },
      { headerName: 'Average Points', field: 'avgPoints' },
      { headerName: 'Description', field: 'description' },
      { headerName: 'Lieutenants', field: 'lieutenants' },
      { headerName: 'Guild Members', field: 'guildMembers' }
    ];

    this.hitServer('/guilds');
  },
  mounted: function () {
    this.$log.info("CONTEXT : ", this.name + " : MOUNTED");
  },
  methods: {
    hitServer: function (path) {
      axios.get(`http://127.0.0.1:5000` + path)
        .then((response) => {
          console.log(response.data);
          this.rowData = response.data;
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

</style>
