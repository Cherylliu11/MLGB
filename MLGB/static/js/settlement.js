function href (orderid){
　　var orderid=orderid;
　　setTimeout(function(){
　　  window.location.href = '/order/order_info/?orderid=' + orderid
    },600);
}
$(document).ready(function() {
    $('.footer-btn').click(function () {
        addr_id = $(".address-left").attr("addr_id")
        csrf = $('input[name="csrfmiddlewaretoken"]').val()
        params = {"addr_id": addr_id,"csrfmiddlewaretoken":csrf}
        $.post('/order/commit/', params, function(data)  {
            if (data.res == 5) {
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(600).fadeOut();
                href(data.orderid)
            }
            else {
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(600).fadeOut();
            }
        },"json")
    })
});

$(".address").click(function () {
    window.location.href = "/address/addr_list?range_check=1"
    addr_path = window.location.pathname;
    $.cookie('addr_path',addr_path,{ path: "/"});
})
