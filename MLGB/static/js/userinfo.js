$(document).ready(function() {

    // 显示隐藏修改密码框
    $("#password").click(function () {
        $("#setpwd1,#setpwd2").toggle()
    })
    // 鼠标离开确认密码框时判断密码是否一致
    $("#setpwd2 .right").blur(function () {
        pwd1 = $("#setpwd1 .right").val()
        pwd2 = $("#setpwd2 .right").val()
        if(pwd1!=pwd2){
            $('<div>').appendTo('body').addClass('alert alert-success').html("输入密码不一致,请重新输入").show().delay(600).fadeOut();
        }
    })
    $("#footer").click(function () {
        pwd1 = $("#setpwd1 .right").val()
        pwd2 = $("#setpwd2 .right").val()
        name = $("input[name='name']").val()
        console.log(name)
        if(pwd1!=pwd2){
            $('<div>').appendTo('body').addClass('alert alert-success').html("输入密码不一致,请重新输入").show().delay(800).fadeOut();
        }
        else{
            csrf = $('input[name="csrfmiddlewaretoken"]').val()
            params = {"username":name,"password": pwd1,"csrfmiddlewaretoken":csrf}
            $.post('/users/userinfo/', params, function(data)  {
                if (data.res == 5) {
                    $('<div>').appendTo('body').addClass('alert alert-success').html(data.message).show().delay(800).fadeOut();
                    setTimeout('window.location.href = "/"',800)
                }
                else {
                    err = JSON.parse(data.message)
                    errmsg = ""
                    $.each(err,function () {
                        errmsg += "<p>"+$(this)['0']['message'] +"</p>"
                        $('<div>').appendTo('body').addClass('alert alert-success').html(errmsg).show().delay(800).fadeOut();
                    })
                }
            })
        }
    })
    $('#exit').click(function () {
        $.get("/users/logout",function () {
            window.location.href = "/"
        });
    });
})

