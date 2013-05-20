$(function () {
    var map = L.map('map');
    var lat = $('.map-view').data("lat").toString().split(",");
    var long = $('.map-view').data("long").toString().split(",");
    L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {}).addTo(map);
    for(var i=0; i<lat.length; i++) {
        map.setView([lat[i], long[i]], 6);
        var marker = L.marker([lat[i], long[i]]).addTo(map);
    }
});
