module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  transformIgnorePatterns: [
    "/node_modules/(?!(@ag-grid-community|@ag-grid-enterprise|axios)/)"
  ],
}
