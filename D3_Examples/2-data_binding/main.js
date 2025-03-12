let numbers = [4, 10, 18, 23, 42];
colors = d3.schemeCategory10; // https://github.com/d3/d3-scale-chromatic

svg = d3.select('body')
  .append('svg')
    .attr('width', 500)
    .attr('height', 500);