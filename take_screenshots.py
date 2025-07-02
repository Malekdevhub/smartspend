import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

APP_URL = "http://localhost:8501"
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1600,1200")

driver = webdriver.Chrome(options=chrome_options)
driver.get(APP_URL)
time.sleep(5)  # Wait for Streamlit to fully load

# Screenshot 1: Main dashboard
dashboard_path = os.path.join(SCREENSHOTS_DIR, "dashboard_summary.png")
driver.save_screenshot(dashboard_path)
print(f"Saved dashboard screenshot: {dashboard_path}")

driver.quit()
print("All screenshots completed.")
