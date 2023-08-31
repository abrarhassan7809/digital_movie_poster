# scrape data without opening browser
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os.path
import time

url_link = "https://www.themoviedb.org/"
poster_folder = 'static'
poster_data = 'poster_data'


class HeadLess:
    def __init__(self):
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"

        headers = {
            "User-Agent": f"{user_agent}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f"user-agent={user_agent}")
        self.options.add_argument("--window-size=1920, 1080")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")

        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get(url_link)
        print(self.driver.title)

        cards = self.driver.find_elements(By.XPATH, "//div[@class='card style_1']")

        movies_list = []

        for card in cards:
            if len(movies_list) >= 3:
                break
            # for images
            print("Processing...")
            images = card.find_element(By.XPATH, ".//img[@class='poster']")
            image_url = images.get_attribute('src')
            print(image_url)

            if not os.path.exists(poster_folder):
                os.makedirs(poster_folder)

            # for download images
            response = requests.get(image_url, headers=headers)
            print(response)
            if response.status_code == 200:
                image_name = os.path.basename(image_url)
                save_image_path = os.path.join(poster_folder, image_name)

                with open(save_image_path, 'wb') as f:
                    f.write(response.content)

            elif not (response.status_code == 200):
                print('failed to download image')

            # for headings
            headings = card.find_element(By.XPATH, ".//h2")
            headings_text = headings.find_element(By.CSS_SELECTOR, "a")
            print(headings_text.text)

            # for dates
            find_dates = card.find_element(By.XPATH, ".//div[@class='content']")
            movie_dates = find_dates.find_element(By.TAG_NAME, "p")
            print(movie_dates.text)

            # appending all files
            movies_list.append(f"{headings_text.text}, {save_image_path}, {movie_dates.text}")

        if len(movies_list) > 0:
            if not os.path.isdir('movies data'):
                os.makedirs(poster_data)
                with open(f"{poster_data}/data.text", 'w') as f:
                    for data in movies_list:
                        f.write(f"{data}\n")

            else:
                with open(f"{poster_data}/data.text", 'w') as f:
                    for data in movies_list:
                        f.write(f"{data}\n")

            time.sleep(1)

        self.driver.quit()


HeadLess()
