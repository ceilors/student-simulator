var margin = {top: 30, right: 20, bottom: 70, left: 50},
width = 600 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom;
var tick_fn = function ( d ) { return d.tick; }
//Create the Scale we will use for the Axis
var axisScale = d3.scale.linear()
    .domain([d3.min(data, tick_fn), d3.max(data, tick_fn)])
    .range([0, width]);
var yaxisScale = d3.scale.linear()
    .domain([-100, 100])
    // .domain([d3.min(data, max_fn), d3.max(data, min_fn)])
    .range([ height, 0]);
var xAxis = d3.svg.axis()
    .scale(axisScale)
    .orient("bottom");
var yAxis = d3.svg.axis()
    .scale(yaxisScale)
    .orient("left");
var svgContainer = d3.select("body").
    append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
svgContainer.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
svgContainer.append("g")
    .attr("class", "y axis")
    .call(yAxis);
// create a line
var line_mood = d3.svg.line()
.x( function( d, i ) { return axisScale( d.tick ); })
.y( function( d, i ) { return yaxisScale( d.mood ); })
var line_progress = d3.svg.line()
.x( function( d, i ) { return axisScale( d.tick ); })
.y( function( d, i ) { return yaxisScale( d.progress ); })
var line_satiety = d3.svg.line()
.x( function( d, i ) { return axisScale( d.tick ); })
.y( function( d, i ) { return yaxisScale( d.satiety ); })
var line_finances = d3.svg.line()
.x( function( d, i ) { return axisScale( d.tick ); })
.y( function( d, i ) { return yaxisScale( d.finances ); })
svgContainer.append("svg:path").attr("class", "line")
    .attr("stroke", "green").attr("d", line_mood(data));
svgContainer.append("svg:path").attr("class", "line")
    .attr("stroke", "blue").attr("d", line_progress(data));
svgContainer.append("svg:path").attr("class", "line")
    .attr("stroke", "red").attr("d", line_satiety(data));
svgContainer.append("svg:path").attr("class", "line")
    .attr("stroke", "black").attr("d", line_finances(data));