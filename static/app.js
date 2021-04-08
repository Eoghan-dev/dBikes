let map;

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
					content: station.name + get_weather(),
				});
				infowindow.open(map, marker);
			});
		});

		const bikeLayer = new google.maps.BicyclingLayer();
  		bikeLayer.setMap(map);


	}).catch(err => {
		console.log("OOPS!", err);
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
