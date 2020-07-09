$(function() {

    function filter(element) {
        var value = $(element).val().toUpperCase();
        $("#manga-list > li").each(function () {
            if ($(this).text().toUpperCase().indexOf(value) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $("#search_filter").on('keyup', function() {
        filter(this);
    });


});

