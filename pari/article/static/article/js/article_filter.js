var ArticleFilter = {
    init: function() {
        $('.type-filter').click(function(){
        var filterEndpoint = $('#article-list').data('filter-endpoint');
        var args = { 'filter': $(this).data('filter')};
        var filterArgsPrefix = "filterArgs";
        $.each($('#article-list').data(), function(key,value){
            if(key.substring(0, filterArgsPrefix.length) === filterArgsPrefix){
                var arg = key.replace(filterArgsPrefix,'').toLowerCase();
                args[arg] = value;
            }

        });

        Dajaxice.pari.article[filterEndpoint](Dajax.process, args);
    });
    }
}

$(function(){
    ArticleFilter.init();
});