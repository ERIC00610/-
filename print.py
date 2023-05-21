import requests
from bs4 import BeautifulSoup

re = requests.get('https://www.google.com/')
soup = BeautifulSoup(re.text, "html.parser")
print(soup.title)