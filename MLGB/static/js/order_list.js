$(".current_order,.history_order").click(function(){
    order_id = $(this).attr('order_id')
    window.location.href = "/order/order_info/?orderid=" + order_id
});