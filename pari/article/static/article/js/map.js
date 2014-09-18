$(function () {
    try {
        var map = L.map('map');
    }
     catch(e){
        return true;
    }
    var lat = $('.map-view').data("lat").toString().split(","),
        long = $('.map-view').data("long").toString().split(",");

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 7,
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    for (var i = 0; i < lat.length; i++) {
        map.setView([lat[i], long[i]], 6);
        L.marker([lat[i], long[i]]).addTo(map);
    }

});
