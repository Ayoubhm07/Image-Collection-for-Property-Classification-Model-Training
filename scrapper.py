from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import time
import os

# Initialize the web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.sothebysrealty.com/eng/sales/du-uae")
WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

try:
    while True:  # Loop through pagination
        initial_properties_list = WebDriverWait(driver, 45).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.Search-results__grid > li.Search-results__item"))
        )
        print("Properties found:", len(initial_properties_list))

        for property_index in range(len(initial_properties_list)):
            # Re-query the properties list and click on the current property
            properties_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.Search-results__grid > li.Search-results__item"))
            )
            property_elem = properties_list[property_index]
            ActionChains(driver).move_to_element(property_elem).click().perform()

            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "m-listing-title__carousel-button"))).click()

            photo_count_span = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span.count"))
            )
            photo_count = int(photo_count_span.text)
            print(f"Number of photos for property {property_index+1}:", photo_count)

            for i in range(photo_count):
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.responsive-image-container img"))
                )
                time.sleep(6)  # Ensures image is fully loaded

                screenshot = driver.get_screenshot_as_png()
                screenshot_image = Image.open(BytesIO(screenshot))

                img_width, img_height = screenshot_image.size
                left = img_width // 4
                top = img_height // 7
                right = img_width - left
                bottom = img_height - (img_height // 5)

                cropped_image = screenshot_image.crop((left, top, right, bottom))
                property_folder = f'C:/Users/HP/Desktop/RealEstateImages/data/property_{property_index+1}'
                os.makedirs(property_folder, exist_ok=True)
                save_path = f'{property_folder}/property_{property_index+1}cropped{i+1}.png'
                cropped_image.save(save_path)
                print(f"Image {i+1} of property {property_index+1} saved successfully at {save_path}.")

                if i < photo_count - 1:
                    next_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon-arrow-long-right.js-custom-arrow-swiper-right"))
                    )
                    next_button.click()

            driver.execute_script("window.history.go(-1)")
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.Search-results__grid > li.Search-results__item"))
            )

        next_page_arrow = driver.find_element(By.CSS_SELECTOR, "a.Pagination__item--arrow[rel='next']")
        if "disabled" in next_page_arrow.get_attribute("class"):
            print("Reached the last page. No more pages to navigate.")
            break
        else:
            next_page_arrow.click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.Search-results__grid > li.Search-results__item"))
            )

except Exception as e:
    print("An error occurred:", str(e))

finally:
    driver.quit()
