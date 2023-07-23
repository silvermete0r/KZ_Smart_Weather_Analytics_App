import requests
from bs4 import BeautifulSoup

url = 'https://all-populations.com/en/kz/list-of-cities-in-kazakhstan-by-population.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'table table-bordered'})
rows = table.find_all('tr')

cities_by_population = {}

for row in rows:
    cells = row.find_all('td')
    city_name = None
    for id, cell in enumerate(cells):
        if id == 0:
            city_name = cell.text
        else:
            cities_by_population[city_name] = ''.join(list(filter(lambda x: x.isdigit(), cell.text)))

print(cities_by_population)