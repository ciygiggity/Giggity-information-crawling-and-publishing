from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import discord.discordConfig as discordConfig  # 导入配置文件

# 从配置文件获取Chrome选项和服务
chrome_options = discordConfig.get_chrome_options()
chrome_service = discordConfig.get_chrome_service()

message = "------模拟点击信息发送------"

# 获取服务器和频道名称
server_name = discordConfig.server_name
channel_name = discordConfig.channel_name

# 启动浏览器
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # 打开Discord登录页面
    driver.get("https://discord.com/login")

    # 等待用户手动登录，设置超时时间，例如300秒
    time.sleep(5)

    # 定义超时时间和间隔时间
    timeout = 300  # 总共等待的时间，单位为秒
    interval = 5   # 每次检测的间隔时间，单位为秒

    start_time = time.time()  # 记录开始时间

    while time.time() - start_time < timeout:
        current_url = driver.current_url
        if "channels" in current_url:
            print("用户已成功登录")
            login = 1
            break
        else:
            print("正在等待用户登录...")
            time.sleep(interval)
    else:
        print("超时：用户登录失败")
        driver.quit()  # 登录失败，关闭浏览器
        exit()

    # 如果用户登录成功，则开始对页面进行信息监控与发送消息
    if login == 1:
        # 等待并点击服务器图标，进入指定服务器
        try:
            server_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='服务器']//div[@data-dnd-name='{server_name}']"))
            )
            server_element.click()
        except Exception as e:
            print(f"未找到设置中的服务器: {e}")
            driver.quit()
            exit()

        # 等待并点击频道名称，进入指定频道
        try:
            channel_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='linkTop_c8969d']//div[@class='name__4eb92 overflow__993fa' and text()='{channel_name}']"))
            )
            channel_element.click()
        except Exception as e:
            print(f"未找到设置中的频道: {e}")
            driver.quit()
            exit()

        # 等待3秒/防止加载过慢
        time.sleep(3)

        # 定位消息输入框的激活元素
        activate_element = driver.find_element(By.XPATH, "//div[@data-slate-node='element']")
        activate_element.click()

        # 输入消息并发送
        message_to_send = message
        activate_element.send_keys(message_to_send)
        activate_element.send_keys(Keys.ENTER)

        # 等待3秒/防止发送过慢
        time.sleep(3)
finally:
    # 关闭浏览器
    driver.quit()
