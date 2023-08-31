# scrape data with opening browser
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os.path

options = Options()
options.add_experimental_option('detach', True)

url_link = "https://www.themoviedb.org/"
poster_folder = 'static'
poster_data = 'poster_data'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url_link)
driver.maximize_window()
print(f"Page Title: {driver.title}")

cards = driver.find_elements(By.XPATH, "//div[@class='card style_1']")

movies_list = []

for card in cards:
    # for images
    print("Processing...")
    images = card.find_element(By.XPATH, ".//img[@class='poster']")
    image_url = images.get_attribute('src')

    if not os.path.exists(poster_folder):
        os.makedirs(poster_folder)

    # for download images
    response = requests.get(image_url)
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

    # for dates
    find_dates = card.find_element(By.XPATH, ".//div[@class='content']")
    movie_dates = find_dates.find_element(By.TAG_NAME, "p")

    # appending all files
    movies_list.append(f"{headings_text.text}, {image_url}, {movie_dates.text}")

if len(movies_list) > 0:
    if not os.path.isdir(poster_data):
        os.makedirs(poster_data)
        with open(f"{poster_data}/data.text", 'w') as f:
            for data in movies_list:
                f.write(f"{data}\n")

    else:
        with open(f"{poster_data}/data.text", 'w') as f:
            for data in movies_list:
                f.write(f"{data}\n")

driver.quit()
