// author: ID404
/*
深信服社区论坛抽奖，抓包后替换url1和ck
*/

var rp = require('request-promise');
const fs = require('fs');
const cj_time = fs.createWriteStream('./CJtimes.txt');
const bean_sum = fs.createWriteStream('./bean_sum.txt');
const bean_add = fs.createWriteStream('./bean_add.txt');

let cj_time_log = new console.Console(cj_time, cj_time);
let bean_sum_log = new console.Console(bean_sum, bean_sum);
let bean_add_log = new console.Console(bean_add, bean_add);


var url1 = ''
var ck = ''

var options = {
    method: 'POST',
    url: url1,
    body: 'ajaxdata=json',
    headers: {
        'Host': 'bbs.sangfor.com.cn',
        'Connection': 'close',
        'Content-Length': '13',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'X-Requested-With',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'X-Tingyun-Id': '',//每次不同
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://bbs.sangfor.com.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://bbs.sangfor.com.cn/plugin.php?id=common_plug:raffle',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': ck
    },
    json: true 
};

rp(options)
    .then(function (parsedBody) {
        if (parsedBody.data.success) {
            //console.log(parsedBody),
            console.log('抽奖时间：',Date())
            if (parsedBody.data.freetimes-1<0){
                console.log('本次抽奖花费10S豆')
            } else {
                console.log('本次抽奖没花费S豆')
            }
            cj_time_log.log(parsedBody.data.freetimes)
            bean_sum_log.log(parsedBody.data.ownSbean)
            bean_add_log.log(parsedBody.data.prize.name)
            console.log('本次获得S豆：',parsedBody.data.prize.name)
            console.log('账号S豆数量：',parsedBody.data.ownSbean)
            console.log('本日剩余免费抽奖次数：',parsedBody.data.freetimes)
            console.log('本日剩余可抽奖次数：',parsedBody.data.lesstimes)           
        } else {
            console.log('抽奖时间：',Date()),
            console.log('执行失败',parsedBody.message)
        }
    })
    .catch(function (err) {
        console.log('程序运行错误')// POST failed...
    });

