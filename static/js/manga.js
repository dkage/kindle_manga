$(function() {
    const csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    const manga_id = $("input[name='manga_id']").val();

    $("#subscribe").on('click',function (){
        $.ajax({
            url: '/subscribe',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'manga_id': manga_id
            },
            success: function (result) {
                console.log('Subscription')
            }
        });
    })
});


$(function() {
    $("#subscribe").click(function () {

        let subscribe_div = $("#subscribe")

        if (subscribe_div.hasClass('subbed')){

            subscribe_div.removeClass("subbed");
            subscribe_div.addClass("unsubbed");

        }else{

            subscribe_div.removeClass("unsubbed");
            subscribe_div.addClass("subbed");

        }
    })
});