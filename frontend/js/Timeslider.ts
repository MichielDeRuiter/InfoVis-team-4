
export default class Timeslider
{
    constructor(eventHandler)
    {

        this.eventHandler = eventHandler;
        this.eventHandler.subscribe_timeslider(this)

        var dataSource = [
            { x: new Date(2013, 12, 31), amount: 2000, y2: 10 },
            { x: new Date(2014, 2, 20), amount: 5000, y2: 15 },
            { x: new Date(2015, 2, 30), amount: 4000, y2: 10 },
            { x: new Date(2016, 3, 20), amount: 4500, y2: 5 },
            { x: new Date(2017, 4, 25), amount: 6000, y2: 6 },
            { x: new Date(2017, 4, 30), amount: 2000, y2: 10 }
        ];

        let initial_date = dataSource[0].x.getTime() / (1000*60*60*24);
        
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
                //
                //fromDate
                //endDate
                selectedRangeChanged: function (e) {
                    console.log(e)
                    var chart = $("#chartContainer").dxChart("instance");
                    chart.zoomArgument(e.startValue, e.endValue);
                },
                onValueChanged : (event)=>{
                    let date0 = Math.round((event.value[0].getTime() / (1000*60*60*24)) - initial_date)
                    let date1 = Math.round((event.value[1].getTime() / (1000*60*60*24)) - initial_date)
                    eventHandler.change_dates(date0, date1);
                }
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