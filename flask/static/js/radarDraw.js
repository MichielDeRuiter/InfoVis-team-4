function radarDraw(scope, element) {
  /**
   * Angular variables
   *
   */
   
  // watch for changes on scope.data
  var config;
  var csv;

  function get_data_and_draw(names) {
    d3.json("http://127.0.0.1:5000/radar?name=" + names, function(json_data){
          RadarChart.draw(element[0], json_data, config);
    })
  }

  ///scope.$watch("[csv, config]", function() {
    csv = scope.csv;
    config = scope.config;
    // var data = csv2json(csv);
  ///  get_data_and_draw("badpolitics,politics,shitredditsays,shitpoliticssays")

    // var data = [{"group":"a","axis":"mileage","value":70,"description":""},{"group":"a","axis":"price","value":100,"description":""},{"group":"a","axis":"safety","value":80,"description":""},{"group":"a","axis":"performance","value":90,"description":""},{"group":"a","axis":"interior","value":74,"description":""},{"group":"a","axis":"warranty","value":70,"description":""},{"group":"b","axis":"mileage","value":86,"description":""},{"group":"b","axis":"price","value":60,"description":""},{"group":"b","axis":"safety","value":94,"description":""},{"group":"b","axis":"performance","value":66,"description":""},{"group":"b","axis":"interior","value":34,"description":""},{"group":"b","axis":"warranty","value":97,"description":""},{"group":"c","axis":"mileage","value":46,"description":""},{"group":"c","axis":"price","value":76,"description":""},{"group":"c","axis":"safety","value":64,"description":""},{"group":"c","axis":"performance","value":36,"description":""},{"group":"c","axis":"interior","value":56,"description":""},{"group":"c","axis":"warranty","value":65,"description":""}]
    // call the D3 RadarChart.draw function to draw the vis on changes to data or config
    // RadarChart.draw(element[0], data, config);  // call the D3 RadarChart.draw function to draw the vis on changes to data or config

  ///});


  // helper function csv2json to return json data from csv
  function csv2json(csv) {
    csv = csv.replace(/, /g, ","); // trim leading whitespace in csv file
    var json = d3.csv.parse(csv); // parse csv string into json
    // reshape json data
    var data = [];
    var groups = []; // track unique groups
    json.forEach(function(record) {
      var group = record.group;
      if (groups.indexOf(group) < 0) {
        groups.push(group); // push to unique groups tracking
        data.push({ // push group node in data
          group: group,
          axes: []
        });
      };
      data.forEach(function(d) {
        if (d.group === record.group) { // push record data into right group in data
          d.axes.push({
            axis: record.axis,
            value: parseInt(record.value),
            description: record.description
          });
        }
      });
    });

    return data;
  }



  function receiveMessage(event) {
    console.log(event.data)
    get_data_and_draw(event.data)

    //if (event.origin !== "http://example.org:8080")
    //  return;
  }

  window.addEventListener("message", receiveMessage, false);
}
