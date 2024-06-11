from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import feishuConfig as feishuConfig  # 导入配置文件

# 从配置文件获取Chrome选项和服务
chrome_options = feishuConfig.get_chrome_options()
chrome_service = feishuConfig.get_chrome_service()
# 获取群组名称
group_name = feishuConfig.group_name

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

        # 打开文件用于写入消息
        with open("feishu_messages.txt", "a", encoding="utf-8") as file:
           # 等待页面加载
            print("开始监测群组")
            time.sleep(3)
            print("开始爬取历史信息")

            # 初始抓取所有消息，包括 message-last
            messages = driver.find_elements(By.XPATH, "//div[@class='list_items']/div[contains(@class, 'messageItem-wrapper')]")
            # 打印找到的消息元素数量
            print(f"Found {len(messages)} messages.")
            for message in messages:
                try:
                    # 提取aria-label属性（假设其包含时间和作者信息）
                    aria_label = message.get_attribute("aria-label")
                    
                    # 检查是否包含符合条件的span元素
                    content_elements = message.find_elements(By.XPATH, ".//span[contains(@class, 'text-only')]")
                    if not content_elements:
                        # 标记为已处理
                        driver.execute_script("arguments[0].setAttribute('data-scraped', 'true')", message)
                        continue  # 如果没有符合条件的span元素，则跳过该message

                    # 提取消息内容
                    content = content_elements[0].text
                except Exception as e:
                    # 处理可能的异常
                    aria_label = "Unknown time Unknown author"
                    content = "No content"
                    print(f"Error extracting message details: {e}")

                # 格式化消息文本
                message_text = f"[{aria_label}] {content}"
                print(message_text)

                # 将消息写入文件
                file.write(message_text + "\n")

                # 给爬取的消息添加标记
                driver.execute_script("arguments[0].setAttribute('data-scraped', 'true')", message)

            print("历史信息已爬取完成")
            print("开启监控新信息")

            # 开始监控新消息
            while True:
                time.sleep(5)  # 每5秒检查一次新消息

                # 获取所有未标记的消息，包括 message-last
                new_messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'messageItem-wrapper') and not(@data-scraped)]")
                print(f"Checking for new messages... Found {len(new_messages)} new messages.")  # 输出新消息数量

                for message in new_messages:
                    try:
                        aria_label = message.get_attribute("aria-label")
                        
                        # 检查是否包含符合条件的span元素
                        content_elements = message.find_elements(By.XPATH, ".//span[contains(@class, 'text-only')]")
                        if not content_elements:
                            # 标记为已处理
                            driver.execute_script("arguments[0].setAttribute('data-scraped', 'true')", message)
                            continue  # 如果没有符合条件的span元素，则跳过该message

                        # 提取消息内容
                        content = content_elements[0].text
                    except Exception as e:
                        aria_label = "Unknown time Unknown author"
                        content = "No content"
                        print(f"Error extracting message details: {e}")

                    message_text = f"[{aria_label}] {content}"
                    print(message_text)

                    # 将消息写入文件
                    file.write(message_text + "\n")

                    # 给爬取的消息添加标记
                    driver.execute_script("arguments[0].setAttribute('data-scraped', 'true')", message)
finally:
    # 关闭浏览器
    driver.quit()
