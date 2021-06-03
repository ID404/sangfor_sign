// author: ID404
/*
深信服社区论坛签到领福利，抓包后替换ck
*/

var rp = require('request-promise');
var ck = ''

var options = {
    method: 'POST',
    url: 'https://bbs.sangfor.com.cn/home.php?mod=spacecp&ac=ordinary&op=reward&submit=1',
    body: 'ajaxdata=json',
    headers: {
        'Host': 'bbs.sangfor.com.cn',
        'Connection': 'close',
        'Content-Length': '13',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Tingyun-Id': 'xxx',  //抓包
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://bbs.sangfor.com.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://bbs.sangfor.com.cn/plugin.php?id=info:index',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': ck
        
    },
    json: true 
};

rp(options)
    .then(function (parsedBody) {
        if (parsedBody.ret.success) {
            console.log('领登陆福利运行时间：',Date()),
            console.log(parsedBody)
            console.log('领登陆福利执行成功 ',parsedBody.message)
            //console.log('本次获得S豆：',parsedBody.data.prize.name),
            //console.log('账号S豆数量：',parsedBody.data.ownSbean),
            //console.log('本日可免费抽奖次数：',parsedBody.data.freetimes),
            //console.log('本日剩余抽奖次数：',parsedBody.data.lesstimes)
            
        } else {
            console.log('领登陆福利运行时间：',Date()),
            console.log('领登陆福利执行失败',parsedBody.message)
        }
    })
    .catch(function (err) {
        console.log('领登陆福利程序运行错误')// cookies失效或登陆错误.
    });

