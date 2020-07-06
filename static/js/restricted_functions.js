// AJAX for running full scan function


$(function () {
    const csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

$(function() {
    const csrftoken = $("input[name='csrfmiddlewaretoken']").val();

    $( "#scan-full-btn" ).on('click',function (){
        $.ajax({
            url: '/full_scan',
            type: 'POST',
            data: {'csrfmiddlewaretoken': csrftoken},
            success: function (result) {
                console.log('Function is running')
            }
        });
    })
});


// $.ajax({
//             url: 'controller/addBookmark',
//             type: 'POST',
//             data: {'submit':true}, // An object with the key 'submit' and value 'true;
//             success: function (result) {
//               alert("Your bookmark has been saved");
//             }