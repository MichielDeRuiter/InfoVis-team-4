import ServerAPI from './ServerAPI';

export default class Timeslider
{
    constructor(eventHandler)
    {

        this.eventHandler = eventHandler;
        this.eventHandler.subscribe_timeslider(this)

        let start_date = new Date(2013, 12, 31);
        //enddate = new Date(2017, 4, 30)
        let initial_date = start_date.getTime() / (1000*60*60*24);

        (ServerAPI.get()).getMainTotal( function(data2) {


            let array_data = Object.values(data2);

            const BLOCK = 15;
            let arr = [];

            for ( var i = 0; i < array_data.length; i+= BLOCK) {
                let sum = 0;
                for (var j = 0; j < BLOCK; j++) {
                    sum += array_data[i + j];
                }

                arr.push({
                    x : new Date((initial_date + i) * (1000*60*60*24)),
                    amount : sum * sum
                })

            }
            console.log(arr)

            //let data = Object.values(data2).map((date, i )=>{
            //    return {x : new Date((initial_date + i) * (1000*60*60*24)), amount : date * date}
            //})
        
        
        $(function(){
            $("#range-selector").dxRangeSelector({
                dataSource: arr,

                chart: {
                    commonSeriesSettings: {
                        type: 'bar',
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


        });
    }
}