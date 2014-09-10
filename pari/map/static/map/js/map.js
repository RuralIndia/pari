var mapInterface = {
    init: function() {
        this.template = Handlebars.compile(this.source);
        this.populateLocations();
    },

    populateLocations: function() {
        $.get('/article/api/locations/?format=json', $.proxy(function(data) {
            this.data = data;
            $('#map').vectorMap({
                map: 'in_mill_en',
                regionStyle: {
                    initial: {
                        fill: 'grey'
                    }
             },
                backgroundColor: '#ffffff',
                hoverColor:'#000000',
                markers: data,
                markerStyle: {
                    initial: {
                        fill: '#F8E23B',
                        stroke: '#383f47'
                    }
                },
                onMarkerClick: $.proxy(function(e, index){
                    this.onMarkerClick(e, index);
                }, this)
            });
        }, this));
    },

    onMarkerClick: function (e, index) {
        var id = this.data[index].id;
        this._populateSideBar(id);
        this.updateHistory({'location': id});
    },

    _getState: function() {
        var State = History.getState();
        if(State.data['location']) {
            this._populateSideBar(State.data['location']);
        } else {
            this._clearSidebar();
        }
    },

    _populateSideBar: function(id) {
        $.get('/article/api/locations/' + id + '/article/?format=json', $.proxy(function(locationData) {
            var templateHtml= this.template(locationData);
            $("#side").html(templateHtml);
        }, this));
    },

    _clearSidebar: function() {
        $("#side").empty();
    },

    updateHistory: function(args){
        this.historyFlag = false;
        var paramArgs = $.param(args);
        History.pushState(args, 
            "", 
            paramArgs === "" ? null : "?" + paramArgs);
    },

    historyBind: function(){
        History.Adapter.bind(window,'statechange',$.proxy(function(){
            if(this.historyFlag){
                this._getState();
            }
            this.historyFlag = true;
        }, this));
        this._getState();
    },

    historyFlag: true,

    source: $("#article-template").html(),

    data: null
};


$(function(){
    mapInterface.init();
    mapInterface.historyBind();
});