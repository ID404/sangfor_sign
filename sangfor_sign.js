// author: LJC
/*
深信服社区论坛签到脚本，抓包后替换body,ck
*/


var rp = require('request-promise');
var ck = ''

var options = {
    method: 'POST',
    url: 'https://bbs.sangfor.com.cn/plugin.php?id=sign:index&op=sign',
    body: '',  //抓包后填写
    headers: {
        'Host': "bbs.sangfor.com.cn",
        'Connection': "close",
        'Content-Length': "73",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': "application/json, text/plain, */*",
        'X-Requested-With': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?0",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        'X-Tingyun-Id': "",  //抓包后填写
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Origin': "https://bbs.sangfor.com.cn",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://bbs.sangfor.com.cn/plugin.php?id=info:index",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': ck
    },
    json: true 
};

rp(options)
    .then(function (parsedBody) {
        if (parsedBody.success) {
            console.log('签到时间：',Date()),
            console.log('签到原始日志：')
            console.log(parsedBody)
            if (parsedBody.success == true){
                console.log('签到成功，签到时间',parsedBody.sign_info.dateline)
                console.log('本月连续签到次数',parsedBody.sign_info.continue_sign)
            }
            
        } else {
            console.log('签到时间：',Date())
            console.log('签到执行失败!!!,以下为失败日志：')
            console.log(parsedBody)
        }
    })
    .catch(function (err) {
        console.log('每日签到程序运行错误',parsedBody)// cookies失效或登陆错误.
    });


     

/*
签到成功日志
{
  success: true,
  sign_info: {
    uid: '30',
    count: '4',
    continue_sign: '2',
    dateline: '2021-6-2 08:48',
    raffle: '1',
    sign_count: '629',
    rank: 629,
    medal_level: 1,
    medal_credit: 3,
    medal_nextlevel: 10,
    medal_scale: '30%',
    medal_class: 'medal-sign1',
    has_sign: 1,
    dbdateline: '16229',
    isActivitySign: true,
    this_month_sign_count: '2',
    nextNote: 5
  },
  sbean: 2
}
*/


    