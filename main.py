import os
from login_helper2 import is_logged_in, login_and_save_cookie, get_logged_in_context
from playwright.sync_api import sync_playwright

def scrape_note_detail(page, note_url):
    page.goto(note_url)
    page.wait_for_timeout(2000)  # 等页面加载（或更换为 page.wait_for_selector）

    # 抓标题
    try:
        title = page.locator("h1").first.inner_text()
    except:
        title = "❌ 无法获取标题"

    # 抓作者昵称
    try:
        author = page.locator("a.username").first.inner_text()
    except:
        author = "❌ 无法获取作者"

    # 滚动加载更多评论cd
    for _ in range(5):
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1000)

    # 抓评论内容
    comments = []
    try:
        comment_items = page.locator("div.comment-item")
        count = comment_items.count()
        for i in range(count):
            comment = comment_items.nth(i).inner_text()
            comments.append(comment)
    except:
        comments = ["❌ 无法获取评论"]

    print("\n📌 标题：", title)
    print("👤 作者：", author)
    print("💬 评论：")
    for idx, c in enumerate(comments[:10], 1):
        # 替换所有平台上的换行符（\r\n 和 \n）为单一空格
        c = c.strip().replace('\r\n', '\n').replace('\n', ' ')  # 统一替换换行符为单一空格
        print(f"  {idx}. {c}")

def main():
    NOTE_URL = "https://www.xiaohongshu.com/explore/67237f07000000003c01ded9?xsec_token=ABqVcNlNnS8s75V1iKcFpjmq4bflwuwmhN1L0gfInQFWY=&xsec_source=pc_search&source=web_explore_feed"

    with sync_playwright() as p:
        if not is_logged_in():
            login_and_save_cookie()

        browser, context = get_logged_in_context(p)
        page = context.new_page()

        scrape_note_detail(page, NOTE_URL)

        browser.close()

if __name__ == "__main__":
    main()
