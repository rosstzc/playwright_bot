import os
from login_helper2 import is_logged_in, login_and_save_cookie, get_logged_in_context
from playwright.sync_api import sync_playwright

def scrape_note_detail(page, note_url):
    page.goto(note_url)
    page.wait_for_timeout(2000)  # 等页面加载（或更换为 page.wait_for_selector）

    

def main():
    NOTE_URL = "https://sycm.taobao.com/portal/home.htm"
    with sync_playwright() as p:
        if not is_logged_in():
            login_and_save_cookie()

        browser, context = get_logged_in_context(p)
        page = context.new_page()

        scrape_note_detail(page, NOTE_URL)

        browser.close()

if __name__ == "__main__":
    main()
