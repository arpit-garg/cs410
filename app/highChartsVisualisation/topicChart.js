var completeData = {};
var completeRelevantData = {};
var timeSeries = [];
var seriesData = [];
$( document ).ready(function() {
	$("#detailsDiv").hide();
   	$.get( "http://127.0.0.1:5000/temporalStrength", function( data ) {
   		completeData = data;
	});

	$.get( "http://127.0.0.1:5000/relevantData", function( data ) {
   		completeRelevantData = data;
	});
});

function submit(topic=0) {
    // $("input[type=checkbox]:checked").each(function(){
        getCompleteTimePeriod(completeData[topic]);
        seriesData=[]
        // seriesData.push({'name': $(this)[0].value, marker: {symbol: 'square'}, data: completeData[$(this)[0].value].prediction})
        seriesData.push({'name': topic, marker: {symbol: 'square'}, data: completeData[topic].temporalStrength})
        var relevantData = completeRelevantData[topic];
        var finalRelevantData = [];
        var html = '<table id="relevantData" class="display" cellspacing="0" width="100%"><thead><tr><th class="serialNo">Sr.No.</th><th class="title">Title</th><th class="venue">Venue</th><th class="year">Year</th></tr></thead>';
        html += '<tfoot><tr><th>Sr.No.</th><th>Title</th><th>Venue</th><th>Year</th></tr></tfoot><tbody>';
        if(relevantData != undefined && relevantData != null && relevantData.length > 0){
        	for(var i = 0; i < relevantData.length; i++){
        		html += '<tr><td>' + parseInt(i+1) + '</td><td><a href="https://www.ncbi.nlm.nih.gov/pubmed/' + relevantData[i].pmid + '">' + relevantData[i].title + '</a></td><td>' + relevantData[i].venue + '</td><td>' + relevantData[i].year + '</td></tr>';
        	}
        	html += '</tbody></table>';
        	$("#topicRelevant").html(html);

        	$(document).ready(function(){
        		console.log("data table")
    			$('#relevantData').DataTable({
    				"ordering":false
    				//"paging":false
    			});
			});

        	$("#detailsDiv").show();
        }
        // seriesData.push(checkDataIntegrity(topic));
    // });
    
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
	        text: ''
	    },
	    xAxis: {
	        categories: topicData
	    },
	    yAxis: {
	        title: {
	            text: 'Probability of Strength'
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