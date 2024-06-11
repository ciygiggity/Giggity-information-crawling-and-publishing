from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import feishu.feishuConfig as feishuConfig  # 导入配置文件

# 从配置文件获取Chrome选项和服务
chrome_options = feishuConfig.get_chrome_options()
chrome_service = feishuConfig.get_chrome_service()
# 获取群组名称
group_name = feishuConfig.group_name
message = "------模拟点击信息发送------"
# 启动浏览器
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # 打开飞书登录页面
    driver.get("https://accounts.feishu.cn/accounts/page/login?app_id=1&no_trap=1&redirect_uri=https%3A%2F%2Fwww.feishu.cn%2Fmessenger%2F")

    # 等待用户手动登录，设置超时时间，例如300秒
    time.sleep(5)

    # 定义超时时间和间隔时间
    timeout = 300  # 总共等待的时间，单位为秒
    interval = 5   # 每次检测的间隔时间，单位为秒

    start_time = time.time()  # 记录开始时间

    while time.time() - start_time < timeout:
        current_url = driver.current_url
        if "messenger" in current_url:
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

    # 如果用户登录成功，则开始对页面进行信息监控与爬取
    if login == 1:
        # 等待并点击群组名称，进入指定群组
        try:
            group_element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{group_name}']"))
            )
            group_element.click()
        except Exception as e:
            print(f"未找到设置中的群组: {e}")
            driver.quit()
            exit()

        # 等待页面加载
        time.sleep(2)

        # 检查并定位消息输入框的激活元素
        try:
            activate_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='lark-editor-container']//pre[@contenteditable='true']"))
            )
            activate_element.click()

            # 输入消息并发送
            message_to_send = message
            activate_element.send_keys(message_to_send)
            activate_element.send_keys(Keys.ENTER)

            # 等待3秒，防止发送过慢
            time.sleep(3)
        except Exception as e:
            print(f"未找到消息输入框: {e}")
            driver.quit()
            exit()
finally:
    # 关闭浏览器
    driver.quit()
