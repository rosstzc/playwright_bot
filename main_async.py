import asyncio
from login_helper_async import is_logged_in, login_and_save_cookie, get_logged_in_context
from playwright.async_api import async_playwright

async def scrape_note_detail(page, note_url):
    await page.goto(note_url)
    await page.wait_for_timeout(2000)

    try:
        title = await page.locator("h1").first.inner_text()
    except:
        title = "❌ 无法获取标题"

    try:
        author = await page.locator("a.username").first.inner_text()
    except:
        author = "❌ 无法获取作者"

    for _ in range(5):
        await page.mouse.wheel(0, 2000)
        await page.wait_for_timeout(1000)

    comments = []
    try:
        comment_items = page.locator("div.comment-item")
        count = await comment_items.count()
        for i in range(count):
            comment = await comment_items.nth(i).inner_text()
            comments.append(comment)
    except:
        comments = ["❌ 无法获取评论"]

    print("\n📌 标题：", title)
    print("👤 作者：", author)
    print("💬 评论：")
    for idx, c in enumerate(comments[:10], 1):
        print(f"  {idx}. {c.strip().replace('\\n', ' ')}")

async def main():
    NOTE_URL = "https://www.xiaohongshu.com/explore/67237f07000000003c01ded9?xsec_token=ABqVcNlNnS8s75V1iKcFpjmq4bflwuwmhN1L0gfInQFWY=&xsec_source=pc_search&source=web_explore_feed"

    if not is_logged_in():
        await login_and_save_cookie()

    async with async_playwright() as p:
        browser, context = await get_logged_in_context(p)
        page = await context.new_page()

        await scrape_note_detail(page, NOTE_URL)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
