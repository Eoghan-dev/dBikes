let map;

function initCharts(){
	google.charts.load('current',{'packages':['corechart']});
	google.charts.setOnLoadCallback(initMap);
}

function initMap(){
	fetch("/stations").then(response => {
		return response.json()
	}).then(data => {
		console.log("data: ", data);

		map = new google.maps.Map(document.getElementById("map"),{
				center: {lat: 53.34632331338235, lng: -6.26150959615664},
				zoom: 13,
				//read documentation and find features
		});

		data.forEach(station => {
		    // get circle colour
		    if (station.available_bikes/station.available_bike_stands < 0.25){
		        colour = 'red';
		    } else if (station.available_bikes/station.available_bike_stands > 0.75){
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

			//add listeners to markers
			marker.addListener("click", () => {
				//Close info window in this line to fix bug a
				var infowindow = new google.maps.InfoWindow({
					content: station.name,
				});
				infowindow.open(map, marker);
				console.log("calling drawOccupancyWeekly " + station.number);
				drawOccupancyDaily(station.number);
				drawOccupancyWeekly(station.number);
			});
		});

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
		console.log("occupancy data:",data);

		var options = {
            title: "Average Bike Availability per day",
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
		console.log("occupancy data:",data);

		var options = {
			title: "Average Bike Availability per week",
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

function stationDensity(station_number){
    // This function should colour the circles under markers to represent
    // how many bikes are available (red - none, green - loads)

    // currently density is done with stations table which was scraped once (way back when)
    // think about implementing availability using this function
    // or updating stations before submission and exclude this function
}