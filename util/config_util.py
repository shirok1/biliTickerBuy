import json
import time
import requests

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CookieManager:
    def __init__(self, config_file_path):
        self.config = {}
        self.config_file_path = config_file_path

        self.cookie_jar = requests.utils.cookiejar_from_dict(self.config)

    @logger.catch
    def _login_and_save_cookies(
        self, login_url="https://show.bilibili.com/platform/home.html"
    ):
        logger.info("启动浏览器中.....")
        try:
            self.driver = webdriver.Chrome()
        except Exception:
            try:
                self.driver = webdriver.Chrome()
            except Exception:
                raise Exception(
                    "没有找到浏览器驱动，请根据自己的浏览器下载相应的驱动：\n"
                    "相关教程：https://blog.csdn.net/zz00008888/article/details/127903475\n"
                    "Edge： https://liushilive.github.io/github_selenium_drivers/md/IE.html\n"
                    "Chrome：https://liushilive.github.io/github_selenium_drivers/md/Chrome.html\n"
                )
        self.wait = WebDriverWait(self.driver, 0.5)
        self.driver.get(login_url)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, "nav-header-register").click()
        logger.info("浏览器启动, 进行登录.")
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "nav-header-register")
            except Exception as _:
                break
        time.sleep(1)
        self.config["bilibili_cookies"] = self.driver.get_cookies()
        self.dump_config()
        self.driver.quit()
        logger.info("登录成功, 浏览器退出.")
        return self.config["bilibili_cookies"]

    def dump_config(self):
        with open(self.config_file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_cookies(self):
        try:
            with open(self.config_file_path, "r") as f:
                self.config = json.load(f)
        except Exception:
            return self._login_and_save_cookies()

        if self.config == {}:
            return self._login_and_save_cookies()
        else:
            cookies = self.config["bilibili_cookies"]
            return cookies

    def get_cookies_str(self):
        cookies = self.get_cookies()
        cookies_str = ""
        for cookie in cookies:
            cookies_str += cookie["name"] + "=" + cookie["value"] + "; "
        return cookies_str

    def get_cookies_value(self, name):
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie["name"] == name:
                return cookie["value"]
        return None

    def get_cookies_str_force(self):
        cookies = self._login_and_save_cookies()
        cookies_str = ""
        for cookie in cookies:
            cookies_str += cookie["name"] + "=" + cookie["value"] + "; "
        return cookies_str


if __name__ == "__main__":
    cookie_manager = CookieManager("../config/cookies.json")
    logger.info(str(cookie_manager.get_cookies_str()))
