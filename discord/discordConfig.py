# discordConfig.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    #在浏览器的地址栏中输入chrome://version命令获取个人资料路径
    chrome_options.add_argument("user-data-dir=C:\\Users\\liyufeng\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument("--profile-directory=Profile 2")
    return chrome_options

def get_chrome_service():
    # 替换为你的chromedriver.exe的绝对路径
    return Service('C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe') 
# 配置服务器和频道名称
server_name = "giggity的服务器"  # 替换为你的服务器名称
channel_name = "test3"  # 替换为你的频道名称