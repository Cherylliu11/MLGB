window.onload = function() {
    var arrheight = [];

    function arrHeight() {
        var items = document.getElementsByClassName('right-list');
        for (let i = 0; i < items.length; i += 4) {
            var scrolltop = items[i].offsetTop;
            arrheight.push(scrolltop);
        }
    }

    function noactive() {
        let item = document.getElementsByClassName('list');
        for (let i = 0; i < item.length; i++) {
            item[i].setAttribute('class', 'list')
        }
    }

    function scrollactive() {
        var scrolltop = document.getElementById('right-hook').scrollTop;
        for (let i = 0; i < arrheight.length; i++) {
            if (scrolltop > arrheight[i] && scrolltop < arrheight[i + 1]) {
                noactive();
                document.getElementsByClassName('list')[i].setAttribute('class', 'list list-active')
            }
        }
    }

    function clickactive() {
        let list = document.getElementsByClassName('list');
        for (let i = 0; i < list.length; i++) {
            list[i].onclick = function() {
                noactive()
                list[i].setAttribute('class', 'list list-active')
            }
        }
    }
    document.getElementById('right-hook').onscroll = function() {
        scrollactive()
    };
    arrHeight();
    scrollactive();
    clickactive()
};

error_update = false;
//footer数据同步
function update_remote_cart_info(product_id, count) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    // 组织参数
    params = {'product_id':product_id, 'count':count, 'csrfmiddlewaretoken':csrf};
    // 设置ajax请求为同步
    $.ajaxSettings.async = false
    // 发起ajax post请求，访问/cart/update, 传递参数:product_id count
    // 默认发起的ajax请求都是异步的，不会等回调函数执行
    $.post('/order/add/', params, function (data) {
        if (data.res == 4){
            // 更新成功
            error_update = false;
            total = data.total_count;
            if (total == 0){
                $(".submit-btn").attr("href","javajavascript:;");
                $(".submit-btn").css("background","grey")
            }else if (total == 1){
                $(".submit-btn").attr("href","order/settlement");
                $(".submit-btn").css("background","orange")
            }
        }
        else{
            // 更新失败
            error_update = true;
            $('.add_cart').click(function () {
                 $('<div>').appendTo('body').addClass('alert alert-success').html(data.errmsg).show().delay(800).fadeOut();
            });
        }
    });
    // 设置ajax请求为异步
    $.ajaxSettings.async = true
}

// 获取购物车弹出层数据同步
function cart_list(){
    // 设置ajax请求为同步
    $.ajaxSettings.async = false;
    html_resultinfo="<div><p class='selected'>已选商品</p><p class='clear'>清空购物车</p></div>"
    $.get('/order/cart_list/',function (data) {
        // 遍历服务器返回数据
        $.each(data,function (index,item) {
            // 拼接购物车弹出层页面
            html_resultinfo += "<ul class='cart_product_info'><li class='cart_product_name'>"+item['name']+"</li>" +
                "<li class='cart_product_amount'>￥"+item['amount']+"</li>" +
                "<button class='add minus_cart cart_product_minus' price='" + item['price'] + "'product_id="+item['id']+" num='0' id='add_cart'>-</button>" +
                "<li class='cart_product_count'>"+item['count']+"</li>" +
                "<button class='add cart_product_add' price='" + item['price'] + "'product_id="+item['id']+" num='0' id='add_cart'>+</button></ul>"
            $(".cart-list-detail").empty();
            $('.cart-list-detail').html(html_resultinfo)
        })
    });
    $.ajaxSettings.async = true
}

//购物车遮罩层效果
function addShade() {
    $("body").append('<div class="loading-shade"></div>');
    $(".loading-shade").css("100%");
}
//点击footer层弹出购物车遮罩层
$('.footer').unbind("click").bind("click.show", function () {
    c = $(".submit-count span").text()
    if ( c>0 ) {
        cart_list();
        addShade();
        $('#footer-div').show();
        del_footer();
    }
});
// 删除遮罩层效果
function del_footer() {
    $('.loading-shade,.footer').bind('click.hide', function () {
        $('.loading-shade').remove();
        $('#footer-div').hide();
        $('.footer').unbind("click.hide");
    })
}

//左侧弹出导航栏
function addShade_nav() {
    $("body").append('<div class="loading-shade-nav"></div>');
    $(".loading-shade-nav").css("100%");
}
// 点击导航栏按钮弹出导航栏遮罩层
    $('.menu').unbind("click").bind("click.show", function () {
        addShade_nav();
        $('.cd-nav').show();
        del_nav();
    });

// 删除遮罩层效果
function del_nav() {
    $('.loading-shade-nav,.cd-nav').bind('click.hide', function () {
        $('.loading-shade-nav').remove();
        $('.cd-nav').hide();
        $('.cd-nav').unbind("click.hide");
    })
}

$('#order').click(function () {
    addr_path = window.location.pathname;
    window.location.href = "/order/order_list"
});

$('#user').click(function () {
    addr_path = window.location.pathname;
    window.location.href = "/users/userinfo"
});

$('#addr').click(function () {
    addr_path = window.location.pathname;
    $.cookie('addr_path',addr_path,{ path: "/"});
    window.location.href = "/address/addr_list"
});

$('#logout').click(function () {
    $.get("/users/logout",function () {
        location.reload([bForceGet])
    });
    event.stopPropagation();
});

$('.cart-list-detail').on('click','.clear',function () {
    $.get("/order/clearcart/",function () {
        html_resultinfo="<div><p class='selected'>已选商品</p><p class='clear'>清空购物车</p></div>"
        $(".cart-list-detail").empty();
        $('.cart-list-detail').html(html_resultinfo)
        $(".submit-btn").attr("href","javajavascript:;");
        $(".submit-btn").css("background","grey")
        $('.submit-price span').html("&yen;"+0);
        $('.submit-count span').html(0);
    })
})

