import requests
from bs4 import BeautifulSoup

url = 'https://en.tutiempo.net/climate/01-1973/ws-604020.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

select_elements = soup.select('[style*="user-select"]')

data = []
for element in select_elements:
    data.append(element.text)

print(data)
