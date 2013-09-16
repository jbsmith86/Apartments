function initialize() {
  var mapOptions = {
  zoom: 11,
  mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  
  //html 5 geolocation code
  /*if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                 position.coords.longitude);
      var infowindow = new google.maps.InfoWindow({
        map: map,
        position: pos,
      });
      map.setCenter(pos);
    }, function() {
      handleNoGeolocation(true);
    });
  } else {
  // Browser doesn't support Geolocation
    handleNoGeolocation(false);
  }*/

  //static Seattle code
  var options = {
    map: map,
    position: new google.maps.LatLng(47.609722, -122.333056)
  };
  map.setCenter(options.position);


  //loads json
  $.ajax({
    url: 'aptmatches.json',
    async: false,
    dataType: 'json',
    success: function (response) {
      for (var i=0; i<response.length; i++) {
        createMarker(response[i].ApartmentName, response[i].Linkurl, response[i].Bedrooms, response[i].Price, response[i].Latitude, response[i].Longitude, response[i].Address, response[i].City, response[i].State, response[i].Zipcode)
      }
    }
  });

  var infowindow = null;
}

function createMarker(name, link, bed, price, lat, lon, add, city, state, zip) {

  /*var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);*/
  // console.log(name)
  var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 id="firstHeading" class="firstHeading">' + name + '</h1>'+
      '<div id="bodyContent">'+
      '<p>' + bed + ' ' + price + '</p>'+
      '<p>' + name + '<br/>' +
      add + '<br/>' +
      city + ', ' + state + ' ' + zip + '</p>'+
      '<p><a href="' + link + '" target="_blank">'+ link + '</a> ' + '</p>'+
      '</div>'+
      '</div>';

  var newLatlng = new google.maps.LatLng(lat,lon);

  var marker = new google.maps.Marker({
      position: newLatlng,
      map: map,
      title: name
  });

  google.maps.event.addListener(marker, 'click', function() {
    if (typeof infowindow === 'undefined') {
      infowindow = null
    }
    if (infowindow) {
        infowindow.close();
    }
    infowindow = new google.maps.InfoWindow({content: contentString});
    infowindow.open(map, marker);
  });

}

function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = "Error: The Geolocation service failed.";
  } else {
    var content = "Error: Your browser doesn't support geolocation.";
  }
  var options = {
    map: map,
    position: new google.maps.LatLng(60, 105),
    content: content
  };
  var infowindow = new google.maps.InfoWindow(options);
  map.setCenter(options.position);
}


google.maps.event.addDomListener(window, 'load', initialize);