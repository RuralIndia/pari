var ListFilter = {
    init: function() {
        $('.type-filter').on('click', $.proxy(function(event){
            var filterElement = $(event.target).parent('.type-filter');
            var listContainer = $('.filter-list-container');
            if(filterElement.hasClass('active')){
                listContainer.data('filter-args-filter', null);
            } else {
                listContainer.data('filter-args-filter', filterElement.data('filter'));
            }
            listContainer.data('filter-args-page', 1);
            this.collectArgsAndSumbit();
        }, this));

        $('[data-page]').on('click', $.proxy(function(event){
            event.preventDefault();
            var paginationElement = $(event.target).closest('li');

            $('.filter-list-container').data('filter-args-page', paginationElement.data('page'));

            this.collectArgsAndSumbit();
        }, this));

        $('.type-filter').tooltip();
    },

    updateHistory: function(args){
        this.historyFlag = false;
        History.pushState(args, null, "?" + $.param(args));
    },

    collectArgsAndSumbit: function(){
        var nonRequiredArgs = this.collectNonRequiredArgs();
        this.submit(nonRequiredArgs);
    },

    collectNonRequiredArgs: function(){
        var filterArgsPrefix = "filterArgs";
        return this.collectArgs(filterArgsPrefix);
    },

    collectRequiredArgs: function(){
        var filterArgsPrefix = "filterRequiredArgs";
        return this.collectArgs(filterArgsPrefix);
    },

    collectArgs: function(argsPrefix){
        var args = {};

        $.each($('.filter-list-container').data(), function(key,value){
            if(value != null && key.substring(0, argsPrefix.length) === argsPrefix){
                var arg = key.replace(argsPrefix,'').toLowerCase();
                args[arg] = value;
            }
        });

        return args;
    },

    historyBind: function(){
        History.Adapter.bind(window,'statechange',$.proxy(function(){
            if(this.historyFlag){
                var State = History.getState();
                var filterEndpoint = $('.filter-list-container').data('filter-endpoint');
                this.submit(State.data)
            }
            this.historyFlag = true;
        }, this));
    },

    submit: function(nonRequiredArgs){
        this.updateHistory(nonRequiredArgs);
        var requiredArgs = this.collectRequiredArgs();
        var args = $.extend({}, nonRequiredArgs, requiredArgs);
        var filterEndpoint = $('.filter-list-container').data('filter-endpoint');
        Dajaxice.pari.article[filterEndpoint]($.proxy(this.submitCallback, this), args);
    },

    submitCallback: function(data) {
        Dajax.process(data);
        this.init();
    },

    historyFlag: true
}

$(function(){
    ListFilter.init();
    ListFilter.historyBind();
});