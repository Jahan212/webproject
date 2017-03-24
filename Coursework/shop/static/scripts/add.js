$(document).ajaxSend(function (event, jqxhr, settings) {
     jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
});
$(document).ready(function () {
    $(document).on("click",'.add_item', function() {
        item_id = $(this).attr('id');
        console.log( $('input[name=csrfmiddlewaretoken]').val());
        $.ajax({
            type:'GET',
            url:'/basket/add',
            data: {
                id: item_id,
            },
            success: function(){
                $(location).attr('href', '/basket')
            },
        });
    });
});
