var addr_path = $.cookie('addr_path');

if(addr_path == '/order/settlement/'){
    $("header .left-item").attr("href",addr_path);
    $(".url").click(function(){
        addrid = $(this).attr('addrid')
        window.location.href = "/order/settlement/?addrid=" + addrid
    });
}

