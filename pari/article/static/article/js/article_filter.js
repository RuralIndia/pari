var ArticleFilter = {
    init: function() {
        $('.type-filter').on('click', $.proxy(function(event){
            var filterElement = $(event.target).parent('.type-filter');
            if(filterElement.hasClass('active')){
                $('#article-list').removeData('filter-args-filter');
            } else {
                $('#article-list').data('filter-args-filter', filterElement.data('filter'));
            }
            this.collectArgsAndSumbit();
        }, this));

        $('[data-page]').on('click', $.proxy(function(event){
            event.preventDefault();
            var paginationElement = $(event.target).closest('li');

            $('#article-list').data('filter-args-page', paginationElement.data('page'));

            this.collectArgsAndSumbit();
        }, this));
    },

    updateHistory: function(args){
        this.historyFlag = false;
        History.pushState(args, null, "?" + $.param(args));
    },

    collectArgsAndSumbit: function(){
        var filterArgsPrefix = "filterArgs";
        args = {};

        $.each($('#article-list').data(), function(key,value){
            if(key.substring(0, filterArgsPrefix.length) === filterArgsPrefix){
                var arg = key.replace(filterArgsPrefix,'').toLowerCase();
                args[arg] = value;
            }
        });

        var filterEndpoint = $('#article-list').data('filter-endpoint');
        this.submit(filterEndpoint, args);
    },

    historyBind: function(){
        History.Adapter.bind(window,'statechange',$.proxy(function(){
            if(this.historyFlag){
                var State = History.getState();
                var filterEndpoint = $('#article-list').data('filter-endpoint');
                this.submit(filterEndpoint, State.data)
            }
            this.historyFlag = true;
        }, this));
    },

    submit: function(filterEndpoint, args){
        this.updateHistory(args);
        Dajaxice.pari.article[filterEndpoint](Dajax.process, args);
    },

    historyFlag: true
}

$(function(){
    ArticleFilter.init();
    ArticleFilter.historyBind();
});