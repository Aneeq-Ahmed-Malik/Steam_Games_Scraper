from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL = "https://steamdb.info/charts/"


a = np.array([["Rank", "Name", "Current", "24h Peak", "All-time Peak"]])


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("--headless")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ['enable-logging'])


class DataBot(webdriver.Chrome):
    def __init__(self, path="C:\Development\chromedriver.exe"):
        super().__init__(service=Service(path), options=options)
        self.data = []
        self.get(URL)
        self.maximize_window()
        self.implicitly_wait(10)

    def get_data(self):

        select_all = self.find_elements(by=By.TAG_NAME, value="select")[-1]
        select_all.click()
        option_all = select_all.find_elements(by=By.TAG_NAME, value="option")[-1]
        option_all.click()

        content = self.page_source
        self.quit()
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find(name="table")
        all_rows = table.find_all_next(name="tr")[1:]

        for row in all_rows:
            columns = row.text.strip().split("\n")
            columns.pop(6)
            columns.pop(1)
            self.data.append(columns)


bot = DataBot()
bot.get_data()

a = np.append(a, bot.data, axis=0)

df = pd.DataFrame(a)
df.to_csv("GameData.csv", index=False, header=False)
