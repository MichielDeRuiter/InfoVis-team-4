import data from './data_bar.json'
import Configuration from './Configuration'
import ServerAPI from './ServerAPI'
import BasicD3Visualization from './BasicD3Visualization'

export default class Timeline extends BasicD3Visualization
{
  constructor()
  {

    super('timeline');
    
    
   // let ctx = this;
    // we get the data from the Flask server
    // the data is return as a JSON and can be used inmediately
    // the server has to be running

    //(ServerAPI.get()).getData(function(data) {
    // append the svg object to the body of the page
    //d3.json("http://localhost:5000/main", function( data) {

    

//#####################################################################33
     var margin = {top: 20, right: 20, bottom: 70, left: 40},
     width = 600 - margin.left - margin.right,
     height = 300 - margin.top - margin.bottom;

// Parse the date / time
    var x = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
    var y = d3.scaleLinear()
          .range([height, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
    var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
     .append("g")
      .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

// get the data from csv
    // d3.csv("barchart.csv", function(error, data) {
    //   if (error) throw error;

     console.log(data)
    //  console.log(data.volume[0])

  // format the data
     data.forEach(function(d) {
        d.volume = +d.volume;
     });

  // Scale the range of the data in the domains
      x.domain(data.map(function(d) { return d.threemonths; }));
      y.domain([0, d3.max(data, function(d) { return d.volume; })]);

  // append the rectangles for the bar chart
      svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.threemonths); })
          .attr("width", x.bandwidth())
          .attr("y", function(d) { return y(d.volume); })
          .attr("height", function(d) { return height - y(d.volume); });

  // add the x Axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

  // add the y Axis
      svg.append("g")
          .call(d3.axisLeft(y));

    });
 //######################################    

  }
}

