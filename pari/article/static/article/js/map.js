$(function () {
    var map = L.map('map');
    var CLOUD_MAP_API_KEY = '8ee2a50541944fb9bcedded5165f09d9';
    var lat = $('.map-view').data("lat").toString().split(",");
    var long = $('.map-view').data("long").toString().split(",");
    L.tileLayer('http://{s}.tile.cloudmade.com/' + CLOUD_MAP_API_KEY + '/997/256/{z}/{x}/{y}.png', {
        maxZoom: 7,
        attribution: '&copy; 2013 <a href="http://cloudmade.com/">CloudMade</a> – Map data ODbL 2013 <a href="http://www.openstreetmap.org/">OpenStreetMap.org</a> contributors – <a href="http://cloudmade.com/website-terms-conditions">Terms of Use</a>'
    }).addTo(map);
    for (var i = 0; i < lat.length; i++) {
        map.setView([lat[i], long[i]], 6);
        var marker = L.marker([lat[i], long[i]]).addTo(map);
    }
});
