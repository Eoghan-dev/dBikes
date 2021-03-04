let map;

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
			marker = new google.maps.Marker({
				position: {lat: station.pos_lat, lng: station.pos_long},
				map: map,
			});
			//const infowindow; could define here and close before creating
			marker.addListener("click", () => {
				//Close info window in this line to fix bug a?
				const infowindow = new google.maps.InfoWindow({
					content: station.name,
				});
				infowindow.open(map, marker);
			});
		});

	}).catch(err => {
		console.log("OOPS!", err);
	})	
}
