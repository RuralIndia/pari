$(function(){
    var source = $("#article-template").html();
    var template = Handlebars.compile(source);
    $.get('/article/api/locations/?format=json', function(data) {
        $('#map').vectorMap({
          map: 'in_mill_en',
          regionStyle: {
            initial: {
              fill: 'grey'
            }
          },
          backgroundColor: '#ffffff',
          markers: data,
          markerStyle: {
            initial: {
                fill: '#F8E23B',
                stroke: '#383f47'
            }
          },
          onMarkerClick: function(e, index){
            var id = data[index].id;
            $.get('/article/api/locations/' + id + '/article/?format=json', function(locationData) {
              var templateHtml= template(locationData);
              $("#side").html(templateHtml);
            });

          }
        });
    });
});