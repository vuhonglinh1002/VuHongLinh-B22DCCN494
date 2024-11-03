from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from player import Player
from player import Player_Manager
from player import Squad
from player import Squad_Manager

player_manager = Player_Manager()
squad_manager = Squad_Manager()

def validdata(n):
    if n == '': return "N/a"
    return float(n)

def GetDataFromWeb(url, Xpath_player, Xpath_squad, Data_Name):
    driver = webdriver.Chrome()
    driver.get(url)

    resultPlayerData = []
    resultSquadData = []
    try:
        time.sleep(10)
        table2 = driver.find_element(By.XPATH, Xpath_player)
        rows2 = table2.find_elements(By.TAG_NAME, 'tr')

        for row in rows2:  # Bỏ qua hàng tiêu đề
            cols = row.find_elements(By.TAG_NAME, 'td')
            data = []
            for id, play in enumerate(cols[:-1]):
                if id == 1:
                    a = play.text.strip().split()
                    if len(a) == 2:
                        data.append(a[1])
                    else:
                        data.append(play.text.strip())
                else:
                    s = play.text.strip()
                    if id >= 4:
                        s = s.replace(",", "")
                        s = validdata(s)
                    data.append(s)
            if len(data) != 0: resultPlayerData.append(data)

        table1 = driver.find_element(By.XPATH, Xpath_squad)
        rows1 = table1.find_elements(By.TAG_NAME, 'tr')

        for row in rows1[2:]:  # Bỏ qua hàng tiêu đề
            data = []
            name = row.find_element(By.TAG_NAME, 'th')
            data.append(name.text.strip())

            cols = row.find_elements(By.TAG_NAME, 'td')
            for id, value in enumerate(cols):
                s = value.text.strip()
                if id >= 4:
                    s = s.replace(",", "")
                    s = validdata(s)
                data.append(s)
            if len(data) != 0: resultSquadData.append(data)

    finally:
        driver.quit()
        print("Finish Page " + Data_Name)
    return resultPlayerData, resultSquadData

url = "https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats"
xpath_player = '//*[@id="stats_standard"]'
xpath_Squad = '//*[@id="stats_squads_standard_for"]'
DataName = "Standard"
list_player_result, list_Squad_result = GetDataFromWeb(url, xpath_player, xpath_Squad, DataName)

for i in list_player_result:
    p = player_manager.findPlayerByNameandTeam(i[0], i[3])
    if p == None:
        new_p = Player(i[0], i[1], i[2], i[3], i[4])
        new_p.setPlaying_time(i[6:9])
        new_p.setPerformance([i[13], i[14], i[11], i[16], i[17]])
        new_p.setExpected(i[18:21])
        new_p.setProgression(i[22:25])
        new_p.setPer90(i[25:])
        player_manager.add_Player(new_p)
player_manager.filtering()

# squad data
for i in list_Squad_result:
    s = squad_manager.findSquadByName(i[0])
    if s == None:
        new_s = Squad(*i[0:4])
        new_s.setPlaying_time(i[4:7])
        new_s.setPerformance([i[11], i[12], i[9], i[14], i[15]])
        new_s.setExpected(i[16:19])
        new_s.setProgression(i[20:22])
        new_s.setPer90(i[22:])
        squad_manager.add_Squad(new_s)

# Tiếp tục thu thập dữ liệu cho các loại thống kê khác
# (đoạn mã tiếp theo không thay đổi)

# Lưu kết quả vào file CSV
import csv
from bai1.tieu_de import header, row
from bai1.tieu_de import header2, row2

with open('E:/World/Code/Python/BTL/bai1/file/honglinh_result.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for player in player_manager.list_player:
        r = row(player)
        writer.writerow(r)
print("Exam 1 Success")

with open('E:/World/Code/Python/BTL/bai1/file/honglinh_result2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header2)

    for squad in squad_manager.list_squad:
        r = row2(squad)
        writer.writerow(r)
print("Exam 1 Success")