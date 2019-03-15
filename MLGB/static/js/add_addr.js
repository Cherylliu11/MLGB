$("#addr").click(function(){
    addr_path = window.location.pathname + window.location.search;
    $.cookie('addr_path',addr_path);
    $.cookie('user_a',$('#user .right').val());
    $.cookie('tel_a',$('#tel .right').val());
    $.cookie('district_a',$('#district .right').val());
});

$("header .left-item").click(function(){
    $.cookie('addr_path','',{expires: -1})
    $.cookie('user_a','',{expires: -1})
    $.cookie('tel_a','',{expires: -1})
    $.cookie('district_a','',{expires: -1})
    $.cookie('business_a','',{expires: -1})
});

$("#addr").click(function(){
    addrid = window.location.pathname;
    $.cookie('addrid',addrid);
});

var prev_path = $.cookie('prev_path')

if (prev_path == 'location'){
    $('#user .right').val($.cookie('user_a'));
    $('#tel .right').val($.cookie('tel_a'));
    $('#district .right').val($.cookie('district_a'));
    business_cookie = $.cookie('business')
    console.log(business_cookie)
    if (business_cookie){
        $('#addr .right').val(business_cookie)
    }
}
$.cookie('prev_path','',{expires: -1})


$('#comfirm').click(function () {
    name = $('#user .right').val();
    mobilephone = $('#tel .right').val();
    business = $('#addr .right').val();
    address = $('#district .right').val();
    addr_id = $('.wrapper').attr('addr_id');
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.cookie('addr_path','',{expires: -1})
    $.cookie('user_a','',{expires: -1})
    $.cookie('tel_a','',{expires: -1})
    $.cookie('district_a','',{expires: -1})
    $.cookie('business_a','',{expires: -1})
    console.log(business)
    params = {'name': name,'mobilephone': mobilephone,'business':business,'address':address,'csrfmiddlewaretoken':csrf};
    $.post("/address/add_addr",params,function(data){
        if (data.res == 5){
            $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(600).fadeOut();
            window.location.href = "addr_list"
        }
        else{
            $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(600).fadeOut();
        }
    });
})



