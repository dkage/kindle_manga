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