from bs4 import BeautifulSoup
import requests
import lxml
import time
from datetime import date

# tarihi çekip dosyanın devamına ekliyoruz.
tarih = date.today()
print(tarih)

with open("news.txt", mode="a") as file:
    file.write(f"\n{tarih}")

headers = {'Accept-Language': "en-US,en;q=0.5", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0"}
response = requests.get("https://eksisozluk.com/debe", headers=headers)
eksi_debe = response.text
soup = BeautifulSoup(eksi_debe, "html.parser")
debes = soup.select(".topic-list a")

for item in range(len(debes)):
    #başlığı çekiyoruz
    baslik = debes[item].getText().replace("\n", "")

    #girdi için ekşi formatına uygun link oluşturuyoruz.
    eksi_girdi_linki = "\n[" + "https://eksisozluk.com" + f"{debes[item].get('href')}" + " " + f"{baslik}" + "]"


    # her başlığı tek tek çekip çorba yapıyoruz.
    tek_baslik_link = "https://eksisozluk.com" + debes[item].get("href")
    tek_baslik = requests.get(tek_baslik_link, headers=headers)
    tek_baslik_text = tek_baslik.text
    tek_baslik_soup = BeautifulSoup(tek_baslik_text, "html.parser")

    # başlığın kanallarını liste yapıyoruz.
    kanallar = tek_baslik_soup.select_one("#hidden-channels").getText()
    bosluksuz_kanallar = kanallar.replace(" ", "")
    kanallar_liste = bosluksuz_kanallar.replace("\r\n", "").split(",")

    # kanal listesinde siyaset ve haber etiketlerinin olup olmadığını kontrol ediyoruz ve istenmeyen etiketleri hariç tutuyoruz.

    if "siyaset" in kanallar_liste and "haber" in kanallar_liste and "ilişkiler" not in kanallar_liste and "seyahat" not in kanallar_liste and "moda" not in kanallar_liste and "magazin" not in kanallar_liste and "müzik" not in kanallar_liste:
        with open("news.txt", mode="a") as file:
            file.write(f"{eksi_909535girdi_linki}")
        print(f"Link eklendi: {eksi_girdi_linki}")
    else:
        continue
    # hata almamak için 2 saniye bekleme süresi veriyoruz.
    time.sleep(2)
