d3.json('data/so_history.json', function(data) {
  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart()
    .x(function(d) { return d[0] })
    .y(function(d) { return d[1] }) //adjusting, 100% is 1.00, not 100 as it is in the data
    .color(d3.scale.category10().range());

  chart.xAxis
    .tickFormat(function(d) {
      return d3.time.format('%x')(new Date(d*1000))
    });
  chart.x2Axis
    .tickFormat(function(d) {
      return d3.time.format('%x')(new Date(d*1000))
    });
 
  chart.yAxis
    .tickFormat(d3.format('%5f'));
  chart.y2Axis
    .tickFormat(d3.format('%5f'));

  d3.select('#chart svg')
    .datum(data)
    .transition().duration(500)
    .call(chart);


  //TODO: Figure out a good way to do this automatically
  nv.utils.windowResize(chart.update);
  return chart;
  });

}); 

$('#cumulative').bind('click', function() {
  console.log(chart);
});
