$("#id_captcha_1").attr('placeholder','请输入验证码');


$("img.captcha").click(function(){
    $.getJSON('/captcha/refresh/', function(json){
        console.log(json);
        $("img.captcha").attr("src", json.image_url);
        $("#id_captcha_0").val(json.key);
    });
    return false;
});
