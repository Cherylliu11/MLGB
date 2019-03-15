var addrid = $.cookie('addrid');


if(addrid){
    $("header .left-item").attr("href",addrid);
    $("header .right-item").attr("href",addrid);
}

$("header .right-item").click(function(){
    $.cookie('prev_path','location');
    $.cookie('business',myValue)
});

$("header .left-item").click(function(){
    $.cookie('prev_path','location');
});

function G(id) {
    return document.getElementById(id);
}

var map = new BMap.Map("container");
var point = new BMap.Point(121.480237, 31.236305);
map.centerAndZoom(point,12);
map.enableScrollWheelZoom(true);


var ac = new BMap.Autocomplete(    //建立一个自动完成的对象
    {"input" : "suggestId"
    ,"location" : map
    ,"onSearchComplete":function(result){
        // console.log(result['Ar'])
        search_res=result
        var res=''
        $.each(result['Ar'],function () {
            res += "<li class='suggestId'><p class='business'>" + this['business'] + "</p><p class='city'>" + this['city'] + this['district'] + "</p></li>"
        $("#searchResultPanel>ul").html(res)
        })
    ac.hide();
    }
});

$("#searchResultPanel").on('click','.business',function () {
    myValue=$(this).text();
    console.log(myValue);
    $('.business').css('color','black')
    $(this).css('color','red')
    $(this).val(myValue)
    setPlace()
})

function setPlace(){// 创建地址解析器实例
    var myGeo = new BMap.Geocoder();// 将地址解析结果显示在地图上,并调整地图视野
    myGeo.getPoint(myValue, function(point){
      if (point) {
        map.centerAndZoom(point, 16);
        map.addOverlay(new BMap.Marker(point));
      }
    }, "上海");
}