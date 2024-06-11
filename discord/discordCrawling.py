from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import discordConfig as discordConfig  # 导入配置文件

# 从配置文件获取Chrome选项和服务
chrome_options = discordConfig.get_chrome_options()
chrome_service = discordConfig.get_chrome_service()
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

    # 如果用户登录成功，则开始对页面进行信息监控与爬取
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

        # 打开文件用于写入消息
        with open("messagesDiscord.txt", "a", encoding="utf-8") as file:
            time.sleep(3)
            print(f"开始监测频道: {channel_name}")

            last_author = "Unknown"  # 存储上一个消息的用户名

            # 初始抓取所有消息
            messages = driver.find_elements(By.XPATH, "//ol[@class='scrollerInner__37fee']//li[@class='messageListItem__050f9']")

            for message in messages:
                try:
                    author = message.find_element(By.XPATH, ".//span[@class='headerText_bd68ec']//span").text
                    last_author = author  # 更新最后的用户名
                except Exception as e:
                    author = last_author
                    print(f"Error extracting author, using last known author: {last_author}")

                try:
                    content = message.find_element(By.XPATH, ".//div[@class='markup_a7e664 messageContent_abea64']//span").text
                except Exception as e:
                    content = "No content"
                    print(f"Error extracting content: {e}")

                try:
                    # 获取时间
                    time_element = message.find_element(By.XPATH, ".//span[contains(@class, 'timestamp_c79dd2')]//time")
                    timestamp = time_element.get_attribute("aria-label")
                except Exception as e:
                    timestamp = "Unknown time"
                    print(f"Error extracting timestamp: {e}")

                message_text = f"[{timestamp}] {author}: {content}"
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

                # 获取所有未标记的消息
                new_messages = driver.find_elements(By.XPATH, "//ol[@class='scrollerInner__37fee']//li[@class='messageListItem__050f9' and not(@data-scraped)]")

                for message in new_messages:
                    try:
                        author = message.find_element(By.XPATH, ".//span[@class='headerText_bd68ec']//span").text
                        last_author = author  # 更新最后的用户名
                    except Exception as e:
                        author = last_author
                        print(f"Error extracting author, using last known author: {last_author}")

                    try:
                        content = message.find_element(By.XPATH, ".//div[@class='markup_a7e664 messageContent_abea64']//span").text
                    except Exception as e:
                        content = "No content"
                        print(f"Error extracting content: {e}")

                    try:
                        # 获取时间
                        time_element = message.find_element(By.XPATH, ".//span[contains(@class, 'timestamp_c79dd2')]//time")
                        timestamp = time_element.get_attribute("aria-label")
                    except Exception as e:
                        timestamp = "Unknown time"
                        print(f"Error extracting timestamp: {e}")

                    message_text = f"[{timestamp}] {author}: {content}"
                    print(message_text)

                    # 将消息写入文件
                    file.write(message_text + "\n")

                    # 给爬取的消息添加标记
                    driver.execute_script("arguments[0].setAttribute('data-scraped', 'true')", message)

finally:
    # 关闭浏览器
    driver.quit()
