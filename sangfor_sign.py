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

def print_with_timestamp(text):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{formatted_time}] {text}")

def login_and_claim_rewards():
    options = Options()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0")
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    main_window = driver.current_window_handle
    try:
        # 打开需要登录的网页
        print_with_timestamp("正在打开网页!")
        driver.get("https://bbs.sangfor.com.cn/plugin.php?id=info:index#?orderby=dateline&type=index&page=1&init")
        print_with_timestamp("等待5秒")
        time.sleep(5)

        # 点击登录的按钮
        print_with_timestamp("点登录的按钮")
        login_button1 = driver.find_element(By.CSS_SELECTOR, '#header > div.container > div > div.col-xs-4.fix-topbar-options > ul > li.header-login-btn > a')
        login_button1.click()

        # 点验证码登录
        print_with_timestamp("点验证码登录")
        VC_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/root/div[1]/div/div[1]/ul/li[2]/a")))
        VC_button.click()

        # 点验账号登录
        print_with_timestamp("点验账号登录")
        sigin_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/root/div[1]/div/form/div[6]/a[1]")))
        sigin_button.click()

        # 输入用户名和密码
        print_with_timestamp(" ")
        username_input = driver.find_element(By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[1]/input[2]")
        password_input = driver.find_element(By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[2]/input")
        username_input.send_keys("admin")
        password_input.send_keys("123456")

        # 点击登录按钮
        print_with_timestamp("点击登录")
        login_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[11]/div/div/root/div[1]/div/form/div[4]/button")))
        login_button.click()
        time.sleep(5)

        try:
            print_with_timestamp("尝试领取每日福利")
            FL_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div[2]/div/div")))
            FL_button.click()
            time.sleep(10)
        except TimeoutException:
            print_with_timestamp("已领取每日福利或领取超时")

        try:            
            QD_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/div/div[2]/div[2]/a/span[1]")))
            QD_button.click()
            print_with_timestamp("点击每日签到")
            time.sleep(5)
        except TimeoutException:
            print_with_timestamp("每日签到超时")

        try: 
            print_with_timestamp("点击去抽奖")
            QCJ_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[10]/div/div/div[2]/div[2]/div[1]/div[1]/p[1]/a")))#
            QCJ_button.click()
            time.sleep(5)
        except TimeoutException:
            print_with_timestamp("点击去抽奖超时")

        #获取所有窗口的句柄，并切换到新窗口
        windows = driver.window_handles
        for window in windows:
            if window != main_window:
                driver.switch_to.window(window)
                break
        
        time.sleep(5)
        
        try: 
            print_with_timestamp("点击抽奖")
            CJ_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div[2]/div[1]/div/div/div[1]")))#
            CJ_button.click()
            time.sleep(5)
        except TimeoutException:
            print_with_timestamp("点击抽奖超时")


        rewawrd_s_dou = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[10]/div/div/div/h3/span")))
        text1 = rewawrd_s_dou.text
        text = "本次抽中" + text1 + "S豆"
        print_with_timestamp(text)
        time.sleep(5)

        S_dou = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/div[2]/div[1]/div/div/div[3]/h4[1]/span[4]")))
        text2 = S_dou.text
        text = "当前S豆总数：" + text2
        print_with_timestamp(text)

        time.sleep(10)

    except TimeoutException:
        print_with_timestamp("程序运行超时")  
    except KeyboardInterrupt:  
        print_with_timestamp(" ")
        print_with_timestamp("手动中断程序运行")
    finally:
        # 关闭浏览器
        print_with_timestamp("关闭浏览器")
        driver.quit()
        print_with_timestamp("签到结束")

if __name__ == "__main__":
    login_and_claim_rewards()
