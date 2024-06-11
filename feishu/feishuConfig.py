# feishuConfig.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    #在浏览器的地址栏中输入chrome://version命令获取个人资料路径
    chrome_options.add_argument("user-data-dir=C:\\Users\\liyufeng\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument("--profile-directory=Default")
    return chrome_options

def get_chrome_service():
    # 替换为你的chromedriver.exe的绝对路径
    return Service('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe') 

# 配置飞书的群名
group_name = "信息爬取测试群2"

