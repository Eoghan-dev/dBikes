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
				zoom: 14,
				//read documentation and find features
		});

		data.forEach(station => {
			const marker = new google.maps.Marker({
				position: {lat: station.pos_lat, lng: station.pos_long},
				map: map,
			});
			marker.addListener("click", () => {
				//Close info window in this line to fix bug a
				var infowindow = new google.maps.InfoWindow({
					content: station.name,
				});
				infowindow.open(map, marker);
				console.log("calling drawOccupancyWeekly " + station.number);
				drawOccupancyWeekly(station.number);
			});
		});

		const bikeLayer = new google.maps.BicyclingLayer();
  		bikeLayer.setMap(map);


	}).catch(err => {
		console.log("OOPS!", err);
	})	
}

function drawOccupancyWeekly(station_number) {
	// called when user clicks marker
	// use google charts to draw chart

	fetch( input: "/occupancy/" + station_number).then(response => {
		return response.json;
	}).then( data => {
		console.log(data);

		var options = {
			title: "Bike Availability per day"
		}

		var chart = new google.visualisation.ColumnChart(document.getElementById( elementid: 'charts'));
		var chart_data = new google.visualisation.Data_able();
		chart_data.addColumn('datetime', 'Date');
		chart_data.addColumn('number', 'Bike Availability');

		data.forEach(v => {
			chart_data.addRow([new Date(v.last_update, v.available_bikes)]);
		})
		chart.draw(chart_data, options);
	})
}