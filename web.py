# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import requests
import sys
URL ="https://timesofindia.indiatimes.com/city/kanpur/iit-kanpur-hosts-meet-on-urban-healthcare-challenges/articleshow/132318837.cms"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
sys.stdout.reconfigure(encoding='utf-8')
# print(soup.prettify())
# table = soup.find_all("table")[1]
# th = table.find_all("th")
# print(th[0].text.strip() )
# print(table.find_all("tr")[0].text.strip() )  
# print(table.th.text.strip()) 
print(soup.get_text(separator='\n', strip=True))
