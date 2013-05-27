$(function(){
    var datePicker = $('.datepicker');
    var startDate = datePicker.data('start');
    var endDate = datePicker.data('end');
    datePicker.datepicker({minViewMode: 1, startDate: startDate, endDate: endDate}).on('changeMonth',function (e){
        var month = e.date.getMonth() + 1;
        var year = e.date.getFullYear();
        window.location = datePicker.data('url') + year + "/" + month;
    });
});