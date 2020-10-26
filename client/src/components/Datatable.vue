<script>
export default {
  name: 'DataTable',
  props: [
    'data', 'columns', 'query', 'controls_column'
  ],
  data () {
    return {
      view_columns: [],
      view_data: [],
      data_map: {},
      slot_map: {},
      sort: {
        index: 0,
        desc: true
      }
    }
  },
  created() {
      this.parse_columns();
      this.parse_data();
      this.sort_data();
  },
  methods: {
      parse_columns() {
      this.columns.forEach((column, index) => {
        if (typeof(column) == 'string') {
          return this.view_columns.push(column);
        }

        this.view_columns.push(column[0]);

        if (column[1].startsWith('!')) {
          // This is a slot.

        } else if (column.length > 1) {
          // So this would make a map like { column_index: field }
          this.data_map[index] = column[1];
        }
      });
    },
    column_toggle_sort(column_index) {
      if (column_index == this.sort.index) {
        this.sort.desc = !this.sort.desc;
      } else {
        this.sort.index = column_index;
        this.sort.desc = true;
      }

      this.sort_data();
    },
    parse_data() {
      if (this.data == undefined) {
        return;
      }

      this.view_data = [];

      this.data.forEach((row_object) => {
        let row = [];

        // Assume an object if the data_map is set. Otherwise parse as a straight array.
        if (Object.keys(this.data_map).length > 0) {
          Object.keys(this.data_map).forEach((key) => {
            let value = this.data_map[key];

            if (value in row_object) {
              row.push(row_object[value]); 
            }
          });
        } else {
          row = row_object;
        }

        // Filter if a query is provided.
        if (typeof(this.query) !== "undefined" && this.query !== "") {
          let matched = false;

          row.forEach((cell) => {
            let query = String(this.query).toLowerCase().trim();

            if (String(cell).toLowerCase().indexOf(query) !== -1) {
              matched = true;
            }
          });

          if (matched) {
            this.view_data.push(row);
          }
        } else {
          this.view_data.push(row);
        }
      });

    },
    sort_data() {
      this.view_data = _.sortBy(this.view_data, [(row) => {
        if (row[this.sort.index] == "None") {
          return 0;
        }

        let sizes = ['KB','MB','GB','TB'];
        let regex = RegExp('^([0-9\\.]+)\\s?(' + sizes.join('|') + ')', 'ig')
        let matches = regex.exec(row[this.sort.index]);

        if (matches) {
          return Math.pow(1024, _.indexOf(sizes, matches[2])) * parseFloat(matches[1]);
        }

        return row[this.sort.index];
      }]);

      if (!this.sort.desc) {
        this.view_data.reverse();
      }
    }
  },
  watch: {
    query() {
      this.parse_data();
      this.sort_data();
    }
  }
}
</script>