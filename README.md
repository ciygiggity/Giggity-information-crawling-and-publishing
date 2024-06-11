# Suimit-information-crawling-and-publishing
## 项目介绍
    本项目是针对聊天平台进行非官方机器人注入式的信息抓取与发布
    由于加入官方机器人需要服务器管理者或是频道管理者的许可，
    使用webdriver和selenium为核心，以模拟点击的形式去对指定的服务器内指定的频道信息进行抓取与发布

## 环境依赖
    本项目使用python311版,请运行前保证有python环境
    运行pip install selenium 配置核心库
    安装了 Chrome 浏览器
    请根据自己的Chrome版本前往https://developer.chrome.com/docs/chromedriver/downloads 下载对应的Driver并解压安装好

## 目录结构描述
    ├──feishu
        ├── feishu信息抓取.py           // feishu信息抓取
        ├── feishu信息发布.py          //  feishu信息发布
        ├── feishuConfig.py           //  feishu配置
    ├──discord        
        ├── discord信息抓取.py           // discord信息抓取
        ├── discord信息发布.py          //  discord信息发布
        ├── discordConfig.py           //  discord配置
    ├── README.md                   //  help

## 使用说明
### 无论是信息发布还是信息抓取你都需要进行的配置
    更新你使用的模块config以匹配你的 Chrome 用户配置文件目录和 Chromedriver 可执行文件路径
    使用discord模块功能更新discordConfig.py
    使用feishu模块功能更新feishuConfig.py
    和你要进行信息抓取或信息发布的服务器内的对应频道
    也可以在代码首部进行配置
**位于discord代码页内配置修改示例：**
```python
    #将
    server_name = discordConfig.server_name
    channel_name = discordConfig.channel_name
    #改为
    server_name = "giggity的服务器"
    channel_name = "test3"
 ```
**监测爬取giggity的服务器中的test3频道**
**位于飞书代码页内修改示例：**
```python
    #将
    group_name = feishuConfig.group_name
    #改为
    group_name = "信息爬取测试群2"
```
**监测爬取飞书中群名为信息爬取测试群2的群**
    
### 配置完成后
#### 信息抓取

- 运行脚本：python discord信息抓取.py
 - 一旦脚本运行，它将在 Chrome 浏览器窗口中打开 Discord, 注意运行前请先关闭你配置的浏览器
    -    你可以在你配置的google浏览器中提前登录，这样运行脚本就无需再此登录
    -    如果需要，手动登录 Discord。
 -   机器人将等待你登录并导航到指定的服务器和频道。
    -   一旦机器人检测到你已成功登录并导航到指定的服务器和频道，它将开始监控消息。
    -   消息将记录到名为 "messages.txt" 的文本文件中，该文件位于与脚本相同的目录中。
        -   你可以通过修改脚本中的 open() 函数来自定义消息记录的文件名和路径。
    -   要停止机器人，只需关闭 Chrome 浏览器窗口。

- 新增feishu消息抓取功能，基本原理和运行情况与discord相同
    - 运行脚本：python feishu信息抓取.py

#### 信息发布
- 配置你要指定发布的信息
    ```python
        message = "------模拟点击信息发送------"
    ```
- 运行脚本：python discord信息发布.py
 - 一旦脚本运行，它将在 Chrome 浏览器窗口中打开 Discord, 注意运行前请先关闭你配置的浏览器
    -    你可以在你配置的google浏览器中提前登录，这样运行脚本就无需再此登录
    -    如果需要，手动登录 Discord。
 - 机器人将等待你登录并导航到指定的服务器和频道。
    -   一旦机器人检测到你已成功登录并导航到指定的服务器和频道，它会等待3秒后发送消息
    -   发送消息后3秒会关闭网页

- 新增feishu消息发布功能，基本原理和运行情况与discord相同
    - 运行脚本：python feishu信息发布.py



### 脚本除了登录外全自动无需操作,如果提前登录过也不需要登录操作



## 项目版本
- 1.0.0 discord爬取与发布功能 
 -  项目及文档制作人：陈俊艺 工作日期：2024/6/3 - 2024/6/6
- 2.0.0 添加了feishu爬取与发布功能
 -  项目及文档制作人：陈俊艺 工作日期：2024/6/6 - 2024/6/11









