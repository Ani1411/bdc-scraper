import os
import random
import time
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BDCScraper:
    def __init__(self, params, chromePath):
        # self.postalCodesDictList = params['postalCodesList']
        print(params)
        self.destinations = params['destinations']
        self.chromePath = chromePath
        # self.postCodePropertyListMappingObject = []
        # self.display = Display(visible=False, size=(1024, 768)) if platform.system() != 'Darwin' else ''
        self.browser, self.wait = self.initiateBrowserObject()
        # self.postCodePropertyListMappingObjectConsidered = []

    def initiateBrowserObject(self):
        print('ini')
        if platform.system() == 'Darwin':
            options = Options()
            # options.add_argument('--headless')
            options.add_argument('--start-maximized')
            browser = webdriver.Chrome(options=options, executable_path=self.chromePath)
            wait = WebDriverWait(browser, 10)
        else:
            options = Options()
            options.add_argument("--no-sandbox")
            if os.path.exists('/usr/bin/chromedriver'):
                print('exists')
            else:
                print('not exists')
            browser = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
            wait = WebDriverWait(browser, 10)
        print('connected chrome urlFetch')

        return browser, wait

    def cleanLink(self, links):

        index = links.find("html?") + 5
        new_link = links[0:index]
        return new_link

    def get_hotel_search_list(self, checkin, checkout):
        destPropertyListMapping = []

        destList = []
        for item in self.destinations:
            dest = item['city'] + ' ' + item['state']
            if dest not in destList:
                time.sleep(1)
                print("________________________Looping for Destination Started_________________", dest)
                search_page_link = "https://www.booking.com/searchresults.en-gb.html?ss=" + dest + "&checkin=" + checkin + "&checkout=" + checkout
                self.browser.get(search_page_link)
                time.sleep(1 + random.uniform(0, 1))

                for i in range(30):
                    time.sleep(1)
                    full_container = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._814193827')))
                    container_elements = full_container.find_elements(By.CSS_SELECTOR,
                                                                      "div._fe1927d9e._0811a1b54._a8a1be610._022ee35ec.b9c27d6646.fb3c4512b4.fc21746a73")
                    print(len(container_elements))
                    j = 0
                    for box in container_elements:
                        randomTime = random.uniform(0, 1) + 0.3
                        print("Going to Sleep for " + str(randomTime) + " seconds!!!")
                        time.sleep(randomTime)
                        propertyDict = {'destination': dest}
                        try:
                            propertyDict['Name'] = box.find_element(By.CSS_SELECTOR, "div.fde444d7ef._c445487e2").text
                        except:
                            propertyDict['Name'] = 'NA'
                        # try:
                        #     propertyDict['Hotel Id'] =
                        try:
                            distance_text = box.find_element(By.XPATH, ".//span[@data-testid='distance']").text
                            propertyDict['distance'] = distance_text
                        except:
                            propertyDict['distance'] = 0

                        try:
                            propertyDict['property_url'] = self.cleanLink(
                                box.find_element(By.CSS_SELECTOR, "a.fb01724e5b").get_attribute("href"))
                        except:
                            propertyDict['property_url'] = ''
                        try:
                            propertyDict['rating'] = box.find_element(By.CSS_SELECTOR, "div._9c5f726ff.bd528f9ea6").text
                        except:
                            propertyDict['rating'] = 'NA'
                        try:
                            propertyDict['remark'] = box.find_element(By.CSS_SELECTOR,
                                                                      "div._9c5f726ff._192b3a196.f1cbb919ef").text
                        except:
                            propertyDict['remark'] = 'NA'
                        try:
                            propertyDict['locationScore'] = box.find_element(By.CSS_SELECTOR,
                                                                             "span._8ae9a3c91").text.split(' ')[1]
                        except:
                            propertyDict['locationScore'] = 0
                        try:
                            propertyDict['stars'] = len(box.find_elements(By.CSS_SELECTOR,
                                                                          "span._3ae5d40db._617879812._6ab38b430"))
                        except:
                            propertyDict['stars'] = 0
                        try:
                            propertyDict['price'] = box.find_element(By.CSS_SELECTOR, "span.fde444d7ef._e885fdc12").text
                        except:
                            propertyDict['price'] = 'NA'
                        try:
                            propertyDict['payment'] = box.find_element(By.CSS_SELECTOR,"div._3abe99b47").text
                        except:
                            propertyDict['payment'] = ''
                        try:
                            text_reviews = box.find_element(By.CSS_SELECTOR,
                                                            "div._4abc4c3d5._1e6021d2f._6e869d6e0").text.split()
                            if 'external' not in text_reviews:
                                propertyDict['total_reviews'] = int(text_reviews[0])
                            else:
                                propertyDict['total_reviews'] = 0
                        except:
                            propertyDict['total_reviews'] = 0
                        destPropertyListMapping += [propertyDict]
                        print(j)
                        # if j == 10:
                        #     break
                        j += 1
                    try:
                        if self.browser.find_element(By.CSS_SELECTOR, "div.ce83a38554._ea2496c5b.bc9f15a430"):
                            break
                    except:
                        self.browser.find_element(By.CSS_SELECTOR, "div.ce83a38554._ea2496c5b").find_element(
                            By.CSS_SELECTOR, "button._4310f7077._fd15ae127").click()

            destList.append(dest)
        postCodePropertyList = []
        for propertyDict in destPropertyListMapping:
            if propertyDict['total_reviews'] > 0:  # & (propertyDict['distance'] <= 500):
                postCodePropertyList += [propertyDict]
        self.browser.quit()
        return postCodePropertyList

        # self.postCodePropertyListMappingObject = postCodePropertyList
        #
        # self.postCodePropertyListMappingObjectConsidered = self.postCodePropertyListMappingObject
