from bs4 import BeautifulSoup
import requests

url = 'https://www.pagina12.com.ar/'

response = requests.get(url)
if response.status_code ==200:
    parsed = BeautifulSoup(response.text, 'lxml')
    titulo = parsed.find_all('a')
    print(titulo.text)
    
