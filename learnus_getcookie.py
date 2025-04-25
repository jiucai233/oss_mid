from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
# 设置浏览器驱动（确保已安装对应的浏览器驱动程序，如 chromedriver）

def get_cookies(username, password):
    driver = webdriver.Chrome()

    try:
        # 打开登录页面
        driver.get("https://ys.learnus.org/login/method/sso.php")

        # 输入用户名
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)  # 替换为你的用户名

        # 输入密码
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)  # 替换为你的密码

        # 提交表单
        password_field.send_keys(Keys.RETURN)

        # 等待页面加载完成
        time.sleep(3)

        # 检查是否跳转到首页
        if driver.current_url == "https://ys.learnus.org/":
            print("登录成功！")

            # 获取登录后的 Cookie
            cookies = driver.get_cookies()
            print("Cookies:", cookies)
            # 将 Cookie 保存到 JSON 文件中
            with open("cookies.json", "w") as cookie_file:
                json.dump(cookies, cookie_file)
            print("Cookies 已保存到 cookies.json 文件中。")
            return cookies
        else:
            print("登录失败！请检查用户名和密码。")
            return None

    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    # 替换为你的用户名和密码
    username = "your_username"
    password = "your_password"

    get_cookies(username, password)