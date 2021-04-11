let map;
var infowindow = null;

function initCharts(){
	google.charts.load('current',{'packages':['corechart']});
	google.charts.setOnLoadCallback(initMap);
}

function initMap(){
	fetch("/stations").then(response => {
		return response.json()
	}).then(data => {
		//console.log("data: ", data);

		map = new google.maps.Map(document.getElementById("map"),{
				center: {lat: 53.34632331338235, lng: -6.26150959615664},
				zoom: 13,
		});

        var stationStr = "";

		data.forEach(station => {
		    stationStr = stationStr + "<li><a href='javascript:showInfowindow(" + station.number + ")'>" + formatStationName(str=station.name) + "</a></li>";
            // get circle colour
            if (station.available_bikes/station.bike_stands < 0.25){
                colour = 'red';
            } else if (station.available_bikes/station.bike_stands > 0.75){
                colour = 'green';
            } else {
                colour = 'orange';
            }
            //circles for density
            const circle = new google.maps.Circle({
                strokeColor: colour,
                strokeOpacity: '0.9',
                strokeWeight: 0,
                fillColor: colour,
                fillOpacity: 0.55,
                map: map,
                radius: 50,
                clickable:false,
                center: {lat: station.pos_lat, lng: station.pos_long},
            });

		    //make markers
			const marker = new google.maps.Marker({
				position: {lat: station.pos_lat, lng: station.pos_long},
				map: map,
			});

            var infoStr = "<div><h4>" + formatStationName(station.name) + "</h4><p>Available Bikes: "
                + station.available_bikes + "<br>Available Bike Stands: " + station.available_bike_stands + "</p></div>";

			//add listeners to markers
			marker.addListener("click", () => {
				//Close info window in this line to fix bug a
				if (infowindow) {
				    infowindow.close();
				}
				infowindow = new google.maps.InfoWindow({
					content: infoStr + get_weather(),
				});
				infowindow.open(map, marker);
				//console.log("calling drawOccupancyWeekly " + station.number);
				drawOccupancyDaily(station.number);
				drawOccupancyWeekly(station.number);
			});
		});
        document.getElementById("stationList").innerHTML = stationStr;

		const bikeLayer = new google.maps.BicyclingLayer();
  		bikeLayer.setMap(map);


	}).catch(err => {
		console.log("OOPS!", err);
	})
}

function drawOccupancyDaily(station_number) {
	// called when user clicks marker
	// use google charts to draw chart

	fetch( "/occupancyD/" + station_number).then(response => {
	    //console.log("get_occupancy response:",response);
		return response.json()
	}).then( data => {
		//console.log("occupancy data:",data);

		var options = {
            title: "Average Bike Availability per day",
            legend: "none",
            hAxis: {
                title: "Date"
            },
            vAxis: {
                title: "Avg Number of Bikes"
            }
		}

		var chart = new google.visualization.LineChart(document.getElementById('chartL'));
		var chart_data = new google.visualization.DataTable();
		chart_data.addColumn('datetime', "Date");
		chart_data.addColumn('number', "Avg Bike Availability");

		data.forEach(v => {
			chart_data.addRow([new Date(v.last_update), v.available_bikes]);
		})
		chart.draw(chart_data, options);
	})
}

function drawOccupancyWeekly(station_number) {
	// called when user clicks marker
	// use google charts to draw chart

	fetch( "/occupancyW/" + station_number).then(response => {
	    //console.log("get_occupancy response:",response);
		return response.json()
	}).then( data => {
		//console.log("occupancy data:",data);

		var options = {
			title: "Average Bike Availability per week",
			legend: "none",
            vAxis: {
                title: "Avg Number of Bikes"
            }
		}

		var chart = new google.visualization.ColumnChart(document.getElementById('chartR'));
		var chart_data = new google.visualization.DataTable();
		chart_data.addColumn('string', "Day");
		chart_data.addColumn('number', "Avg Bike Availability");

		data.forEach(v => {
			chart_data.addRow([v.last_update_day, v.available_bikes]);
		})
		chart.draw(chart_data, options);
	})
}

function formatStationName(str){
    var words = str.toLowerCase().split(",");
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i][0].toUpperCase() + words[i].substr(1);
    }
    return words.join(" ");
}

function showInfowindow(station_number) {
	fetch( "/sideBar/" + station_number).then(response => {
	    //console.log("get_occupancy response:",response);
		return response.json()
	}).then( data => {
		//console.log("occupancy data:",data);
		data.forEach(v => {
		    console.log(v.name);
            var infoStr = "<div><h4>" + formatStationName(v.name) + "</h4><p>Available Bikes: "
                    + v.available_bikes + "<br>Available Bike Stands: " + v.available_bike_stands + "</p></div>";
			if (infowindow) {
				    infowindow.close();
				}
            infowindow = new google.maps.InfoWindow({
                content: infoStr + get_weather(),
                position: {lat: v.pos_lat, lng: v.pos_long}
            });
            infowindow.open(map);
		})
	})
}

var weather = {}
fetch("/weather").then(response => {
	return response.json()
}).then(data => {
	weather = data[0]
})

function get_weather() {
	return "<div class='weather'><img src='/static/images/"+weather['weather_icon']+".png'>" +
		"<p><strong>Current weather: " + weather['weather_description'] + "</strong></p>" +
		"<p>Temperature " + parseInt(weather['temp'] - 273.15) + "&#8451;</p>" +
		"<p>Feels like " + parseInt(weather['feels_like'] - 273.15) + "&#8451;</p>" +
		"<p>Humidity " + weather['humidity'] + "%</p>" +
		"<p>Clouds " + weather['clouds'] + "%</p>" +
		"<p>Wind speed " + weather['wind_speed'] + " m/s</p>" +
		"</div>"
}