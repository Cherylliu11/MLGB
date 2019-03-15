name = $('#user .right').val();
mobilephone = $('#tel .right').val();
business = $('#addr .right').text();
address = $('#district .right').val();

$("#addr").click(function(){
    addrid = window.location.search;
    addrpath = window.location.pathname;
    $.cookie('addrid',addrpath+addrid);
    $.cookie('user',$('#user .right').val());
    $.cookie('tel',$('#tel .right').val());
    $.cookie('district',$('#district .right').val());
});

$("header .left-item").click(function(){
    $.cookie('addrid','',{expires: -1})
    $.cookie('user','',{expires: -1})
    $.cookie('tel','',{expires: -1})
    $.cookie('district','',{expires: -1})
    $.cookie('business','',{expires: -1})
});

// var source = $.cookie('source')
var prev_path = $.cookie('prev_path')

if (prev_path == 'location'){
    $('#user .right').val($.cookie('user'));
    $('#tel .right').val($.cookie('tel'));
    $('#district .right').val($.cookie('district'));
    business_cookie = $.cookie('business')
    if (business_cookie){
        $('#addr .right').val(business_cookie)
    }
}
$.cookie('prev_path','',{expires: -1})


$('#comfirm').click(function () {
    name_n = $('#user .right').val();
    mobilephone_n = $('#tel .right').val();
    business_n = $('#addr .right').val();
    address_n = $('#district .right').val();
    addr_id = $('.wrapper').attr('addr_id');
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.cookie('addrid','',{expires: -1})
    $.cookie('user','',{expires: -1})
    $.cookie('tel','',{expires: -1})
    $.cookie('district','',{expires: -1})
    $.cookie('business','',{expires: -1})
    if ( name == name_n && mobilephone == mobilephone_n && business == business_n && address == address_n ){
        $('<div>').appendTo('body').addClass('alert alert-success').html("保存成功").show().delay(600).fadeOut();
        setTimeout("window.location.href = 'addr_list';",800)
    }
    else {
        params = {'addr_id':addr_id,'name': name_n,'mobilephone': mobilephone_n,'business':business_n,'address':address_n,'csrfmiddlewaretoken':csrf};
        $.post("/address/modifity_addr",params,function(data){
            if (data.res == 5){
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(600).fadeOut();
                setTimeout("window.location.href = 'addr_list';",800)
            }
            else{
                console.log(data.errmsg)
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(600).fadeOut();
            }
        });
    }
})

$('#del').click(function () {
    addr_id = $('.wrapper').attr('addr_id');
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    params = {'addr_id':addr_id,'csrfmiddlewaretoken':csrf}
    $.post("/address/del_addr",params,function(data){
            if (data.res == 5){
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(600).fadeOut();
                setTimeout("window.location.href = 'addr_list';",800)
            }
            else{
                $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(600).fadeOut();
            }
    })
})
