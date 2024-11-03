import warnings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Định nghĩa tiêu đề cho file CSV
header = ["Player", "Attribute 1", "Attribute 2", "Attribute 3", "Attribute 4"]

def get_data_from_web(driver, url, data_name):
    driver.get(url)
    player_data = []

    try:
        # Đợi cho phần tử tải lên
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content-part"]/section/div/div/div[1]/div/div[1]')))
        
        # Tải thêm dữ liệu nếu có
        while True:
            try:
                load_more_button = driver.find_element(By.XPATH, '//*[@id="onesignal-slidedown-allow-button"]')
                load_more_button.click()
            except Exception:
                print("All data loaded.")
                break

        # Tìm bảng dữ liệu
        div = driver.find_element(By.XPATH, '//*[@id="content-part"]/section/div/div/div[1]/div/div[1]')
        rows = div.find_elements(By.TAG_NAME, 'tr')

        # Lấy dữ liệu từ từng hàng
        for row in rows[1:]:
            data = []
            cols = row.find_elements(By.TAG_NAME, 'td')
            for index, play in enumerate(cols):
                if index == 0:
                    hong_linh = play.find_element(By.CLASS_NAME, "text").text.strip().split()
                    data.append(f"{hong_linh[0]} {hong_linh[1]}")
                elif index == 1:
                    a = play.text.strip().split('\n')
                    data.extend(a[:2])  # Lấy hai dòng đầu
                elif index == 2:
                    continue
                else:
                    data.append(play.text.strip())
            player_data.append(data)

    except Exception as e:
        print(f"Error occurred: {e}")
    
    print(f"Finish Page {data_name}")
    return player_data


def main():
    url = 'https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league/transfers/2023-2024'
    
    # Sử dụng WebDriver
    with webdriver.Chrome() as driver:
        get_player_data = get_data_from_web(driver, url, '')

        # Lặp qua các trang khác
        for index in range(2, 19):
            page_data = get_data_from_web(driver, f"{url}/{index}", str(index))
            get_player_data += page_data

    # Ghi dữ liệu vào file CSV
    with open('E:/World/Code/Python/BTL/bai4/file/honglinh/result.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(get_player_data)  # Sử dụng writerows để ghi tất cả dữ liệu

    print("Exam 1 Success")


if __name__ == "__main__":
    main()