$(document).ajaxSend(function (event, jqxhr, settings) {
     jqxhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
});
$(document).ready(function () {
    $(document).on("click",'.delete_item', function() {
        item_id = $(this).attr('id').substring(1);
        $.ajax({
            type:'GET',
            url:'remove',
            dataType: 'text',
            data: {
                id: item_id,
            },
            success: function(data){
                console.log("hello");
                location.reload();
            },
            error: function(data){
                console.log("error fool" + data);
            }
        });
    });
});
