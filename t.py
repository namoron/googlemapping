import folium
from selenium import webdriver
import os
import time


mapFname = 'map.html'

mapUrl = 'file://{0}/{1}'.format(os.getcwd(), mapFname)

# download gecko driver for firefox from here - https://github.com/mozilla/geckodriver/releases

# use selenium to save the html as png image
driver = webdriver.Firefox()
driver.set_window_size(1920*100, 1080*100) 
driver.get(mapUrl)
# wait for 5 seconds for the maps and other assets to be loaded in the browser
time.sleep(70)
driver.save_screenshot('output.png')
driver.quit()