$(document).ready(function() {
    $('.footer-btn').click(function () {
        addr_id = $(".address-left").attr("addr_id")
        csrf = $('input[name="csrfmiddlewaretoken"]').val()
        params = {'addr_id': addr_id,'csrfmiddlewaretoken':csrf}
        $.post('/order/commit/', params, function (data) {
            if (data.res == 5) {
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(800).fadeOut();
            }
            else {
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(800).fadeOut();
            }
        })
    })
});

$('#cancel').click(function () {
    order_id = $('#order_info').attr('order_id')
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    params = {'order_id':order_id,'csrfmiddlewaretoken':csrf}
    $.post('/order/cancel/',params,function (data) {
        if (data.res == 5) {
            $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(800).fadeOut();
            setTimeout("window.location.href = '/order/order_list';",800)
        }
        else{
            $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(800).fadeOut();
            setTimeout("window.location.href = '/order/order_list';",800)
        }
    })
})



