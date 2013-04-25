$(function () {
    map = L.map('map');
    var lat = $('.map-view').data("lat")
    var long = $('.map-view').data("long")
    L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
    }).addTo(map);
    map.setView([lat,long], 8);
    var marker = L.marker([lat,long]).addTo(map);
});
