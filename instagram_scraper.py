import json
import time
import gzip
import pickle
import os

import pandas as pd

from playsound import playsound

from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

profile_urls = list(pd.read_csv("/home/sus/PycharmProjects/pythonProject/instaaaa/neww_insta script_using_selenium_wir/unique_users_indonesia_csv")["0"])[550:651]
print(len(profile_urls))
if os.path.exists('user_metadata.pkl'):
    user_data = pickle.load(open('user_metadata.pkl', 'rb'))
else:
    user_data = []

print(len(user_data))

profile_urls = profile_urls[len(user_data):]

for user in profile_urls:
    #executable_path = ChromeDriverManager().install()
    # Create a new instance of the Chrome driver
    service = Service(executable_path='C:\Program Files\Chrome Driver\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    #driver = webdriver.Chrome()


    def interceptor(chrome_request):
        del chrome_request.headers['Referer']  # Delete the header first
        chrome_request.headers['Referer'] = f'https://www.google.com/'


    # Set the interceptor on the driver
    driver.request_interceptor = interceptor

    driver.get(url=f"https://www.instagram.com/{user}/")

    time.sleep(5)
    try:
        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response and "https://www.instagram.com/api/v1/users/web_profile_info" in request.url:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type'],
                    json.loads(gzip.decompress(request.response.body))
                )
                user_data.append([
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type'],
                    json.loads(gzip.decompress(request.response.body))]
                )
                with open('user_metadata.pkl', 'wb') as f:
                    pickle.dump(user_data, f)
    except Exception as e:
        print(e)
        import traceback as tb

        tb.print_exc()
        playsound('/home/sus/PycharmProjects/pythonProject/instaaaa/neww_insta script_using_selenium_wir/typical-trap-loop-140bpm-129880.mp3')
        break
    driver.close()
    print("profile done")

# https://pypi.org/project/selenium-wire/
