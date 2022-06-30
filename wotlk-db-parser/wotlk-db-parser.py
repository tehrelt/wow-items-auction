import lxml
import requests
from bs4 import BeautifulSoup

def main():
    url = 'https://wotlkdb.com/?skill=197'
    response = requests.get(url)
    with open('wotlk-db-parser/index.html', 'w') as f:
        f.write(response.text)
    with open('wotlk-db-parser/index.html', 'r') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    table = soup.find('table', class_='listview-mode-default')
    print(table)
    

if __name__ == '__main__':
    main()
    print('Done.')
    exit(0)