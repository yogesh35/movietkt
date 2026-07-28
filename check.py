from playwright.sync_api import sync_playwright
import requests
import os

# ==========================
# CHANGE THESE 2 LINES ONLY
# ==========================

URL = "https://in.bookmyshow.com/movies/chennai/spider-man-brand-new-day/buytickets/ET00502600/20260730?etCodes=ET00502600&language=english&refEventCode=ET00502600"
#THEATRE="MAYAJAAL Multiplex: ECR, Chennai"
THEATRE = "INOX The Marina Mall, OMR, Chennai"

# ==========================

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_message(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=20
    )


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0 Safari/537.36"
    )

    try:
        page.goto(URL, wait_until="networkidle", timeout=60000)

        # Wait for BookMyShow to load theatres
        page.wait_for_timeout(5000)

        page_text = page.locator("body").inner_text()

        if THEATRE.lower() in page_text.lower():
            send_message(
                f"🎉 Theatre Released!\n\n"
                f"{THEATRE}\n\n"
                f"{URL}"
            )
            print("Notification sent.")
        else:
            print("Theatre not released yet.")

    except Exception as e:
        print(e)

    browser.close()
