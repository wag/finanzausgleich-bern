(function(d3){

var units = "CHF",
    valueRange = [1, 100000000];


var chart = document.getElementById('chart'),
    margin = {top: 30, right: 40, bottom: 120, left: 20},
    width = chart.offsetWidth - margin.left - margin.right,
    height = 650 - margin.top - margin.bottom;


var formatNumber = d3.format(",.0f"),    // zero decimal places
    format = function(d) { return formatNumber(d) + " " + units; },
    color = d3.scale.category20(),
    nodeClass = function(d){
      return "node " + d.side;
    };

var colorScaleRed = d3.scale.quantize()
        .domain(valueRange)
        .range(colorbrewer.Reds[6]),
    colorScaleGrey = d3.scale.quantize()
        .domain(valueRange)
        .range(colorbrewer.Greys[4]),
    colorScaleGreen = d3.scale.quantize()
        .domain(valueRange)
        .range(colorbrewer.Greens[6]);

var colors =  {left: colorScaleRed, container: colorScaleGrey, right: colorScaleGreen};

var nodeColor = function(d){
    return colors[d.side](d.value);
};

// append the svg canvas to the page
var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Set the sankey diagram properties
var sankey = d3.sankey()
    .nodeWidth(36)
    .nodePadding(10)
    .size([width, height]);

var path = sankey.link();

// load the data
d3.json("data/2012.json", function(error, graph) {
  sankey
      .nodes(graph.nodes)
      .links(graph.links)
      .layout(32);

// add in the links
  var link = svg.append("g").selectAll(".link")
      .data(graph.links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

// add the link titles
  link.append("title")
        .text(function(d) {
        return d.source.name + " -> " +
                d.target.name + "\n" + format(d.value); });

// add in the nodes
  var node = svg.append("g").selectAll(".node")
      .data(graph.nodes)
    .enter().append("g")
      .attr("class", nodeClass)
      .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")"; })
    .call(d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", function() {
          this.parentNode.appendChild(this); })
      .on("drag", dragmove));

// add the rectangles for the nodes
  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d) {
          d.color = nodeColor(d);
          return d.color;
      })
      .style("stroke", function(d) {
          return d3.rgb(d.color).darker(0.3); })
    .append("title")
      .text(function(d) {
          return d.name + "\n" + format(d.value); });

// add in the title for the nodes
  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

// the function for moving the nodes
  function dragmove(d) {
    d3.select(this).attr("transform",
        "translate(" + (
               d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
            ) + "," + (
                   d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
            ) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
});

}(d3));
