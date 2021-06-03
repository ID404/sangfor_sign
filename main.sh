#!/bin/bash
#author:ID404
#系统需安装nodejs
#todo:
#1、cookies过期判断
#2、cookies变量参数填写到指定文件
#3、自动获取cookies等变量参数
#4、判断系统是否安装nodejs\npm\request-compse并进行自动安装

#文件路径
filepath=$(pwd)
logfile="${filepath}/sangfor.log"   #日志记录文件
timesfile="${filepath}/CJtimes.txt"  #记录抽奖次数
ckfile="${filepath}/ck.txt"          #用于判断cookies是否失效
cjfile="${filepath}/sangfor_cj.js"   #抽奖程序
signfile="${filepath}/sangfor_sign.js"  #登陆程序
flfile="${filepath}/sangfor_fuli.js"     #每日登陆福利程序
bean_sumfile="${filepath}/bean_sum.txt"   #抽奖S豆合计
bean_addfile="${filepath}/bean_add.txt"   #单次抽奖所得S豆

#pushplus token变量填写
pushplus_token=''   #填写pushplus通知token
add_bean=0

echo "                          " | tee -a $logfile
echo "                          " | tee -a $logfile
date | tee -a $logfile
echo "开始运行程序"
echo "--------------------------------开始清理文件--------------------------------" | tee -a $logfile
rm -rf $bean_sumfile
rm -rf $bean_addfile
rm -rf $timesfile
rm -rf $ckfile
echo "--------------------------------文件清理完毕--------------------------------" | tee -a $logfile

echo "--------------------------------开始执行签到任务--------------------------------" | tee -a $logfile
node $signfile | tee -a $logfile
echo "--------------------------------每日签到任务执行完毕--------------------------------" | tee -a $logfile

#判断ck文件是否存在,存在则认为cookies过期
echo "开始判断cookies是否有效" | tee -a $logfile;
if [ ! -f $ckfile ];then
    echo "ck文件不存在,cookies有效" | tee -a $logfile;
    else
    echo "ck文件存在,cookies已过期.退出程序" | tee -a $logfile;
    curl -d "token=$pushplus_token&title=深信服社区签到&content=Cookies已失效,请及时更新&template=html" http://www.pushplus.plus/send
    echo "微信通知发送成功" | tee -a $logfile;
    rm -rf $ckfile;
    echo "删除CK文件" | tee -a $logfile;
    exit
fi

echo "--------------------------------开始执行每日登陆福利任务--------------------------------" | tee -a $logfile
node $flfile | tee -a $logfile
echo "--------------------------------每日登陆福利任务执行完毕--------------------------------" | tee -a $logfile

echo "--------------------------------开始执行每日首次抽奖任务--------------------------------" | tee -a $logfile
node $cjfile | tee -a $logfile
echo "--------------------------------每日首次抽奖任务执行完毕--------------------------------" | tee -a $logfile

#首次累计增加的S豆
tmp=$(cat $bean_addfile)
echo '本日首次抽奖获得S豆：'$tmp | tee -a $logfile
add_bean=$(($add_bean+$tmp))


#判断文件是否存在
if [ ! -f $timesfile ];then
    echo "抽奖次数文件不存在,退出程序" | tee -a $logfile;exit
    else
    echo "抽奖次数文件存在" | tee -a $logfile
fi


times=$(cat $timesfile)


#免费抽奖次数为0则退出程序
if [ $times -eq 0 ] ; then 
    echo "免费抽奖次数为0,将退出程序" | tee -a $logfile;
    #发送通知
    sum_bean=$(cat $bean_sumfile)
    echo "准备发送微信通知" | tee -a $logfile;
    curl -d "token=$pushplus_token&title=深信服社区签到&content=本次共获得S豆数量：$add_bean<br></br>目前账号S豆数量：$sum_bean<br></br>免费抽奖次数为0,程序退出&template=html" http://www.pushplus.plus/send
    echo "微信通知发送成功" | tee -a $logfile;
    exit
fi

#根据免费抽奖次数进行多次抽奖
echo "--------------------------------开始进行免费抽奖--------------------------------" | tee -a $logfile
echo '共可进行'$times'次免费抽奖'| tee -a $logfile;
for((i=1;i<=$times;i++));  
do   
echo '正在执行第'$i'次抽奖'| tee -a $logfile
node $cjfile | tee -a $logfile
tmp=$(cat $bean_addfile)
echo '本次抽奖获得S豆数量：'$tmp | tee -a $logfile
add_bean=$(($add_bean+$tmp))
done 


sum_bean=$(cat $bean_sumfile)
echo '本次运行共获得S豆数量：' $add_bean'  目前账号S豆数量：'$sum_bean | tee -a $logfile;

#发送签到成功通知
echo "准备发送微信通知" | tee -a $logfile;
curl -d "token=$pushplus_token&title=深信服社区签到&content=签到成功，本日抽奖、签到共获得S豆数量：$add_bean<br></br>目前账号S豆数量：$sum_bean&template=html" http://www.pushplus.plus/send
echo "微信通知发送成功，程序运行完毕!" | tee -a $logfile;