import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Initialize and configure the Selenium driver
def init_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Download image from URL and save it to a file
def download_image(url, filename):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")


output_dir = "berserk_images"
os.makedirs(output_dir, exist_ok=True)

# Save image to the dir
def save_image(image_url: str, page_num: int):
    filename = os.path.join(output_dir, f"page_{page_num:03}.jpg")
    try:
        r = requests.get(image_url, timeout=10)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"⬇️ Downloaded: {filename}")
        else:
            print(f"❌ Failed to download page {page_num}: status code {r.status_code}")
    except Exception as e:
        print(f"❌ Error downloading page {page_num}: {e}")


# Main scraping function
def scrape_chapter(chapter_url: str, total_pages: int, driver):
    print(f"🔢 Starting scrape: {chapter_url}")
    for page_num in range(1, total_pages + 1):
        url = f"{chapter_url}#page-{page_num}"
        print(f"🔗 Loading page {page_num}: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.reader__item-wrap.active img.reader__item[src]"))
            )
            img = driver.find_element(By.CSS_SELECTOR, "div.reader__item-wrap.active img.reader__item")
            src = img.get_attribute("src")
            print(f" - Page: {page_num} {src}")
            if src:
                save_image(src, page_num)
            else:
                print(f"⚠️ No image found on page {page_num}")
        except Exception as e:
            print(f"❌ Error on page {page_num}: {e}")

        time.sleep(random.uniform(1.0, 3.0))
        # Longer pause every 10 pages
        if page_num % 10 == 0:
            pause_sec = random.uniform(5, 10)
            print(f"⏸️ Taking a longer break for {pause_sec:.1f} seconds")
            time.sleep(pause_sec)

    print("✅ Done!")


if __name__ == "__main__":
    chapter_url = "https://manga-bay.org/reader/47/7041"
    total_pages = 91
    driver = init_driver()
    try:
        scrape_chapter(chapter_url, total_pages, driver)
    finally:
        driver.quit()