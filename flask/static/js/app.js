(function() {
  angular.module("RadarChart", [])
    .directive("radar", radar)
    .directive("onReadFile", onReadFile)
    .controller("MainCtrl", MainCtrl);

  // controller function MainCtrl
  function MainCtrl($http) {
    var ctrl = this;
    init();


    // function init
    function init() {
      // initialize controller variables
      ctrl.examples = [
        "data_the_avengers",
        "data_plant_seasons",
        "data_car_ratings"
      ];
      ctrl.exampleSelected = ctrl.examples[0];
      ctrl.getData = getData;
      ctrl.selectExample = selectExample;

      // initialize controller functions
      ctrl.selectExample(ctrl.exampleSelected);
      ctrl.config = {
        w: 250,
        h: 250,
        facet: false,
        levels: 5,
        levelScale: 0.85,
        labelScale: 0.9,
        facetPaddingScale: 2.1,
        showLevels: true,
        showLevelsLabels: false,
        showAxesLabels: true,
        showAxes: true,
        showLegend: true,
        showVertices: true,
        showPolygons: true
      };
    }

    // function getData
    function getData($fileContent) {
      ctrl.csv = $fileContent;
      // console.log(ctrl.csv)
      // ctrl.csv = [{"group":"a","axis":"mileage","value":70,"description":""},{"group":"a","axis":"price","value":100,"description":""},{"group":"a","axis":"safety","value":80,"description":""},{"group":"a","axis":"performance","value":90,"description":""},{"group":"a","axis":"interior","value":74,"description":""},{"group":"a","axis":"warranty","value":70,"description":""},{"group":"b","axis":"mileage","value":86,"description":""},{"group":"b","axis":"price","value":60,"description":""},{"group":"b","axis":"safety","value":94,"description":""},{"group":"b","axis":"performance","value":66,"description":""},{"group":"b","axis":"interior","value":34,"description":""},{"group":"b","axis":"warranty","value":97,"description":""},{"group":"c","axis":"mileage","value":46,"description":""},{"group":"c","axis":"price","value":76,"description":""},{"group":"c","axis":"safety","value":64,"description":""},{"group":"c","axis":"performance","value":36,"description":""},{"group":"c","axis":"interior","value":56,"description":""},{"group":"c","axis":"warranty","value":65,"description":""}]
    }

    // function selectExample
    function selectExample(item) {
      var file = item + ".csv";
      $http.get(file).success(function(data) {
        ctrl.csv = data;
      });
    }
  }

  // directive function sunburst
  function radar() {
    return {
      restrict: "E",
      scope: {
        csv: "=",
        config: "="
      },
      link: radarDraw
    };
  }


  // directive function onReadFile
  function onReadFile($parse) {
    return {
      restrict: "A",
      scope: false,
      link: function(scope, element, attrs) {
        var fn = $parse(attrs.onReadFile);
        element.on("change", function(onChangeEvent) {
          var reader = new FileReader();
          reader.onload = function(onLoadEvent) {
            scope.$apply(function() {
              fn(scope, {
                $fileContent: onLoadEvent.target.result
              });
            });
          };
          reader.readAsText((onChangeEvent.srcElement || onChangeEvent.target).files[0]);
        });
      }
    };
  }
})();