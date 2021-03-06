var completeData = {};
var timeSeries = [];
var seriesData = [];
$( document ).ready(function() {
   	$.getJSON( "topicTemporalStrength.json", function( data ) {
   		completeData = data;
	});
});

function submit(topic=0) {
    $("input[type=checkbox]:checked").each(function(){
        getCompleteTimePeriod(completeData[topic]);
        seriesData=[]
        // seriesData.push({'name': $(this)[0].value, marker: {symbol: 'square'}, data: completeData[$(this)[0].value].prediction})
        seriesData.push({'name': topic, marker: {symbol: 'square'}, data: completeData[topic].temporalStrength})
        // seriesData.push(checkDataIntegrity(topic));
    });
    
    //render(completeData[$("input[type=checkbox]:checked")[0].value], seriesData);
    render(completeData[topic].timeline, seriesData);
};

function getCompleteTimePeriod(timePeriod){
	var newTimeSeries = [];
	// if(timeSeries.length == 0){
	// 	timeSeries = timePeriod;
	// }
	// else{
		
	// }
};

function checkDataIntegrity(topicName){

	
};

function render(topicData, seriesData){
	Highcharts.chart('topicChart', {
	    chart: {
	        type: 'spline'
	    },
	    title: {
	        text: 'Topic Prediction Over Time'
	    },
	    xAxis: {
	        categories: topicData
	    },
	    yAxis: {
	        title: {
	            text: 'Prediction'
	        }	        
	    },
	    tooltip: {
	        crosshairs: true,
	        shared: true
	    },
	    plotOptions: {
	        spline: {
	            marker: {
	                radius: 4,
	                lineColor: '#666666',
	                lineWidth: 1
	            }
	        },
	        series: {
	            connectNulls: true
	        }
	    },
	    series: seriesData
	});
}