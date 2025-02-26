import Configuration from './Configuration'
import ServerAPI from './ServerAPI'
import BasicD3Visualization from './BasicD3Visualization'

export default class Network extends BasicD3Visualization
{
  constructor()
  {

    super('network');

    let ctx = this;
    // we get the data from the Flask server
    // the data is return as a JSON and can be used inmediately
    // the server has to be running
    (ServerAPI.get()).getData(function(data) {
    // append the svg object to the body of the page
    console.log(JSON.stringify(data))
    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_network.json", function( data) {
      // Initialize the links
      var link = ctx.svg
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")

        .style("stroke", "#aaa")

      // Initialize the nodes
      var node = ctx.svg
        .selectAll("circle")
        .data(data.nodes)
        .enter()
        .append("circle")
          .attr("r", 20)
          .style("fill", "#69b3a2")

      // Let's list the force we wanna apply on the network
      var simulation = d3.forceSimulation(data.nodes)                 // Force algorithm is applied to data.nodes
          .force("link", d3.forceLink()                               // This force provides links between nodes
                .id(function(d) { return d.id; })                     // This provide  the id of a node
                .links(data.links)                                    // and this the list of links
          )
          .force("charge", d3.forceManyBody().strength(-400))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
          .force("center", d3.forceCenter(ctx.width / 2, ctx.height / 2))     // This force attracts nodes to the center of the svg area
          .on("end", ticked);

      // This function is run at each iteration of the force algorithm, updating the nodes position.
      function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
             .attr("cx", function (d) { return d.x+6; })
             .attr("cy", function(d) { return d.y-6; });
      }

    });

});

  }
}

