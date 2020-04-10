import requests
import numpy
from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_totalPages(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    try:
        return int(soup.find_all('a', class_='Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page')[-1].text)
    except:
        return 1


def getAllLinks(year):
    with open('./links.csv', 'a') as f:
        for km in np.arange(0, 305000, 5000):
            if km == 300000:
                url = 'https://auto.ru/cars/' + str(year) + '-year/used/?sort=fresh_relevance_1-desc&km_age_from=' + str(km)
            else:
                url = 'https://auto.ru/cars/' + str(year) + '-year/used/?sort=fresh_relevance_1-desc&km_age_to=' + str(km + 4999) +'&km_age_from=' + str(km)
            total_pages = get_totalPages(url)
            print('Current miles: {}\nTotal Pages: {}'.format(km, total_pages))
            if total_pages == 99:
                print(year, km)
                raise
            for i in range(1,total_pages + 1):
                if '?' in url:
                    pageUrl = url + '&output_type=list&page=' + str(i)
                else:
                    pageUrl = url + '?output_type=list&page=' + str(i)
                data = requests.get(pageUrl).text
                soup = BeautifulSoup(data, 'html.parser')
                links = soup.find_all('a', class_='Link ListingItemThumb')
                for link in links:
                    f.write(link.attrs['href'] + '\n')


