$(function(){
    $('.type-filter').click(function(){
        $filterEndpoint = $('#article-list').data('filter-endpoint');
        Dajaxice.pari.article[$filterEndpoint](Dajax.process, {'id':1});
    });
})