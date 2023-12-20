
#此程序主要为登陆深信服官网签到并领取S豆
#定位网页元素可以通过chrome 右键检查，复制完整xpath
#linux下需要先安装好firefox
#yum install firefox
#同时需要下载geckodriver   下载地址 https://github.com/mozilla/geckodriver/releases
#geckodriver需要放在/usr/bin/ 下

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import datetime
import requests
import re

alarm_url = "https://api.day.app/R/sangfor_sign_"
alarm_day = 1

user_credentials = {
    'user1': '123456',
    'user2': '123456',    
    'user3': '123456',
    # 添加更多用户和密码
}

def print_with_timestamp(username,text,text1=None):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    if text1 is not None: # 检查传入的参数是否为 None
        if text1: # 如果传入了网址参数并且不为零
            print(f"[{formatted_time}] { username } {text} {text1}")
        else: # 如果传入了网址参数但为零
            print(f"[{formatted_time}] { username } {text} 0")
    else: # 如果没有传入网址参数
        print(f"[{formatted_time}] { username } {text}")

def click_element_with_selector(selector,selector_content,descritpion,backup_selector=None,backup_content=None):
    try:
        print_with_timestamp(sangfor_username,descritpion)
        CJ_button = wait.until(EC.presence_of_element_located((selector, selector_content)))
        CJ_button.click()
        #time.sleep(5)
    except TimeoutException:
        if backup_selector is not None and backup_content is not None:
            print_with_timestamp(sangfor_username,descritpion)
            CJ_button = wait.until(EC.presence_of_element_located((backup_selector, backup_content)))
            CJ_button.click()
            #time.sleep(5)    
        else:
            print_with_timestamp(sangfor_username, descritpion,"超时")

for sangfor_username,sangfor_password in user_credentials.items():
    try:
        options = Options()
        options.headless = True
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0")
        options.add_argument("--width=0")
        #options.add_argument("--headless")
        options.add_argument("--height=0")
        driver = webdriver.Firefox(options=options)
        wait = WebDriverWait(driver, 10)

        # 打开需要登录的网页
        print_with_timestamp(sangfor_username,"正在打开网页!")
        driver.get("https://bbs.sangfor.com.cn/plugin.php?id=info:index#?orderby=dateline&type=index&page=1&init")
        print_with_timestamp(sangfor_username,"等待5秒")
        #time.sleep(5)
        main_window = driver.current_window_handle
        print_with_timestamp(sangfor_username,"点登录的按钮")
        login_button1 = driver.find_element(By.CSS_SELECTOR, '#header > div.container > div > div.col-xs-4.fix-topbar-options > ul > li.header-login-btn > a')
        login_button1.click()

        print_with_timestamp(sangfor_username,"点验证码登录")
        VC_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/root/div[1]/div/div[1]/ul/li[2]/a")))
        VC_button.click()

        print_with_timestamp(sangfor_username,"点验账号登录")
        sigin_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/root/div[1]/div/form/div[6]/a[1]")))
        sigin_button.click()

        # 输入用户名和密码
        print_with_timestamp(sangfor_username,"输入用户名密码")
        username_input = driver.find_element(By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[1]/input[2]")
        password_input = driver.find_element(By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[2]/input")
        username_input.send_keys(sangfor_username)
        password_input.send_keys(sangfor_password)
        
        click_element_with_selector(By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[4]/button","点击登录")

        click_element_with_selector(By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div[2]/div/div","尝试领取每日福利")

        click_element_with_selector(By.CSS_SELECTOR,"body > div.container.ng-scope > div > div.col-xs-3.components-info > div.sign-btn-wrap > a > span.sign-info","点击每日签到",By.CSS_SELECTOR,"body > div.container.ng-scope > div > div.col-xs-3.components-info > div.sign-btn-wrap > a > span.sign-info.has_sign")

        click_element_with_selector(By.CSS_SELECTOR,"body > div.modal.fade.ng-isolate-scope.in > div > div > div.sign_share.text-333.ng-scope > div:nth-child(2) > div.sign-info-content > div.sign_share-inner > p.mt10 > a","点击去抽奖")


        #获取所有窗口的句柄，并切换到新窗口
        windows = driver.window_handles
        for window in windows:
            if window != main_window:
                driver.switch_to.window(window)
                break

        #time.sleep(8)

        #获取可抽奖次数
        choujiang_time_text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div.container.ng-scope > div.row.mt10 > div.col-md-9 > div > div > div.text-center.text-white > h4:nth-child(2) > span:nth-child(3)")))#
        choujiang_time_text1 = choujiang_time_text.text
        match = re.search(r'(\d+)', choujiang_time_text1)
        print_with_timestamp(sangfor_username,match)
        choujiang_time = int(match.group())
        print_with_timestamp(sangfor_username,"当前可抽奖次数:",choujiang_time)


        while choujiang_time > 0:
            print_with_timestamp(sangfor_username,"剩余可抽奖次数:",choujiang_time)

            click_element_with_selector(By.CSS_SELECTOR,"body > div.container.ng-scope > div.row.mt10 > div.col-md-9 > div > div > div.raffle-con-btn","点击抽奖")#

            try:
                rewawrd_s_dou = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div.modal.fade.ng-isolate-scope.in > div > div > div > h3 > span")))#
                text = rewawrd_s_dou.text
                print_with_timestamp(sangfor_username,"本次抽中S豆数量：",text)
                time.sleep(5)
            except TimeoutException:
                print_with_timestamp(sangfor_username,"获取抽中S豆总数超时")
            #time.sleep(10)

            click_element_with_selector(By.CSS_SELECTOR,By.CSS_SELECTOR,"body > div.container.ng-scope > div.row.mt10 > div.col-md-9 > div > div > div.raffle-con-btn","点击继续抽奖")#

            try:
                S_dou = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div.container.ng-scope > div.row.mt10 > div.col-md-9 > div > div > div.text-center.text-white > h4:nth-child(2) > span:nth-child(4)")))
                text = "当前S豆总数：" + S_dou.text
                print_with_timestamp(sangfor_username,text)
            except TimeoutException:
                print_with_timestamp(sangfor_username,"获取当前S豆总数超时")

            #time.sleep(10)
            choujiang_time -= 1

        try:
            S_dou = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > div.container.ng-scope > div.row.mt10 > div.col-md-9 > div > div > div.text-center.text-white > h4:nth-child(2) > span:nth-child(4)")))
            text = "当前S豆总数：" + S_dou.text
            print_with_timestamp(sangfor_username,text)
        except TimeoutException:
            text = "无法获取当前S豆数量"
            print_with_timestamp(sangfor_username,"获取当前S豆总数超时")


        #发送通知
        current_date = datetime.date.today()
        if current_date.day == alarm_day:
            # 指定的URL
            url = alarm_url + sangfor_username + "/" + text
            # 发送HTTP GET请求访问URL
            response = requests.get(url)
            
            # 输出访问结果
            if response.status_code == 200:
                print_with_timestamp(sangfor_username,"通知发送成功")
                print_with_timestamp(sangfor_username,text)
            else:
                print_with_timestamp(sangfor_username,"通知发送失败")
                print_with_timestamp(sangfor_username,text)
        else:
            print_with_timestamp(sangfor_username,"当前日期不是每月1号,不发送通知")


        # 关闭浏览器
        print_with_timestamp(sangfor_username,"关闭浏览器")
        driver.quit()
        print_with_timestamp(sangfor_username,"退出程序")
    except:
        print_with_timestamp(sangfor_username,"脚本执行错误，继续执行下一个用户")
        continue
