from playwright.sync_api import sync_playwright
import os

XHS_URL = "https://www.xiaohongshu.com/"
USER_DATA_DIR = "user_data"  # 用于持久保存登录信息的文件夹

def is_logged_in():
    return os.path.exists(USER_DATA_DIR) and len(os.listdir(USER_DATA_DIR)) > 0

def login_and_save_cookie():
    with sync_playwright() as p:
        print("🚀 启动浏览器，准备登录小红书...")
        browser = p.chromium.launch_persistent_context(USER_DATA_DIR, headless=False)
        page = browser.new_page()
        page.goto(XHS_URL)

        print("👉 请扫码或使用密码登录小红书，登录完成后按回车继续")
        input("✅ 登录后按下回车...")

        print("💾 登录信息已保存，下次将自动复用")
        browser.close()

def get_logged_in_context(playwright):
    print("🔁 使用持久登录信息启动浏览器")
    browser = playwright.chromium.launch_persistent_context(USER_DATA_DIR, headless=False)
    return browser, browser  # browser 作为 context 使用
