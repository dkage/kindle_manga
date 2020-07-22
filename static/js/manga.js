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
    // Changes color and message of Subscription button when clicked.
    $("#subscribe").click(function () {

        let subscribe_div = $("#subscribe");
        let subscribe_text = $("#subscribe_text");
        let unsubscribe_text = $("#unsubscribe_text");

        // If already subbed, button is red and becomes green when clicked.
        if (subscribe_div.hasClass('subbed')){

            subscribe_div.removeClass("subbed"); // Removes class for RED
            unsubscribe_text.hide();
            subscribe_text.show();
            subscribe_div.addClass("unsubbed"); // Adds class for GREEN

        }else{

            subscribe_div.removeClass("unsubbed"); // Removes class for GREEN
            subscribe_text.hide();
            unsubscribe_text.show();
            subscribe_div.addClass("subbed"); // Adds class for RED

        }
    })
});