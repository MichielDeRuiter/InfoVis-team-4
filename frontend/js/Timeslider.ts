
export default class Timeslider
{
    constructor()
    {

        var dataSource = [
            { x: new Date(2013, 2, 10), amount: 2000, y2: 10 },
            { x: new Date(2013, 2, 15), amount: 3000, y2: 12 },
            { x: new Date(2014, 2, 20), amount: 5000, y2: 15 },
            { x: new Date(2015, 2, 30), amount: 4000, y2: 10 },
            { x: new Date(2016, 3, 20), amount: 4500, y2: 5 },
            { x: new Date(2017, 4, 25), amount: 6000, y2: 6 },
            { x: new Date(2017, 5, 5), amount: 2000, y2: 10 }
        ];

        $(function(){
            $("#range-selector").dxRangeSelector({
                dataSource: dataSource,

                chart: {
                    commonSeriesSettings: {
                        type: 'line',
                        argumentField: 'x'
                    },
                    series: [
                        { valueField: 'amount' },
                        { valueField: 'y2' }
                    ]
                },

                selectedRangeChanged: function (e) {
                    console.log(e)
                    var chart = $("#chartContainer").dxChart("instance");
                    chart.zoomArgument(e.startValue, e.endValue);
                },
                behavior: {
                    callSelectedRangeChanged: 'onMoving'
                }

                margin: {
                    top: 10
                },
                scale: {
                    minorTick: {
                        visible: true,
                    },
                },
                sliderMarker: {
                    //format: "currency"
                },
                title: "Select Time Period"
            });
    
        });
    }
}