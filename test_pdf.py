from selenium import webdriver
from PIL import Image
import pytesseract

url = "https://es.climate-data.org/region/667/"

driver = webdriver.Firefox(executable_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe")
driver.get(url)

table = driver.find_element_by_class_name("medias mensuales numspan")
location = table.location
size = table.size

driver.save_screenshot("screenshot.png")

im = Image.open("screenshot.png")

left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']

im = im.crop((left, top, right, bottom))
im.save("cropped_screenshot.png")

text = pytesseract.image_to_string(Image.open("cropped_screenshot.png"))

print(text)

driver.quit()