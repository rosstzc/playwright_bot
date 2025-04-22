import os
from playwright.async_api import async_playwright

XHS_URL = "https://www.xiaohongshu.com/"
USER_DATA_DIR = "user_data"

def is_logged_in():
    return os.path.exists(USER_DATA_DIR) and len(os.listdir(USER_DATA_DIR)) > 0

async def login_and_save_cookie():
    async with async_playwright() as p:
        print("🚀 启动浏览器，准备登录小红书...")
        browser = await p.chromium.launch_persistent_context(USER_DATA_DIR, headless=False)
        page = await browser.new_page()
        await page.goto(XHS_URL)

        input("👉 请扫码或使用密码登录小红书，完成后按回车继续")
        await browser.close()
        print("✅ 登录信息已保存")

async def get_logged_in_context(playwright):
    print("🔁 使用持久登录信息启动浏览器")
    browser = await playwright.chromium.launch_persistent_context(USER_DATA_DIR, headless=False)
    return browser, browser  # browser 即是 context
