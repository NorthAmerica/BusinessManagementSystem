// 是否为手机号码
function isPhoneNo(phone)
{
    var pattern = /^1[345678]\d{9}$/;
    return pattern.test(phone);
}

// 获取URL参数
function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  decodeURI(r[2]); return null;
}

// 生成随机数
function getRandom(min, max)
{
    var r = Math.random() * (max - min);
    var re = Math.round(r + min);
    re = Math.max(Math.min(re, max), min);
    return re;
}