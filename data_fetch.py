from bs4 import BeautifulSoup
import requests
import time
import json
import os.path


BASE_URL = 'https://www.lakepedia.com/'
PATH = r"C:/Users/chaof/Desktop/507/Final_project/data_storage"
FILE_NAME="final_project_source.json"
CACHE_FILE_NAME = os.path.join(PATH, FILE_NAME)         
FILE_NAME = "data_structure.json"
DATA_FILE_NAME = os.path.join(PATH, FILE_NAME) 

CACHE_DICT = {}
DATA_DICT={}


#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'}


def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)#
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

def initialize():
    search_url = BASE_URL
    url_text = make_url_request_using_cache(search_url, CACHE_DICT)
    #response = requests.get(courses_page_url)

    soup = BeautifulSoup(url_text, 'html.parser')

    #print(soup)
    all_continent = soup.find('div', class_='container container-custom margin_80_0')

    all_continent = all_continent.findAll('div', class_='wrapper')
    #print(all_continent)

    continent_dict = {}
    for i in range(len(all_continent)):
        link=all_continent[i].find('a')
        continent_name = link.text
        continent_link = link['href']
       # continent_dict[continent_name] = lake_country

        url_text = make_url_request_using_cache(continent_link, CACHE_DICT)
        soup = BeautifulSoup(url_text, 'html.parser')

        all_lakes = soup.findAll('div', class_='col-lg-8 col-sm-12')
        all_lakes_pictures = soup.findAll('div', class_='col-lg-4 col-sm-12')

        #print(all_lakes[0])
        lake_country = {}
        for i in range(len(all_lakes)):
            link=all_lakes[i].find('a')
            lake_name = link.text
            lake_link = link['href']
            
            picture = all_lakes_pictures[i].find('img')['src'].replace('\'', '')
            #lake_dict[lake_name] = lake_link

            url_text = make_url_request_using_cache(lake_link, CACHE_DICT)
            soup = BeautifulSoup(url_text, 'html.parser')
            all_lakes_data = soup.findAll('table', id='lake-stats')
            lake_data_table = all_lakes_data[0].findAll('tr')
            lake_data_dict = {}
            for data_entry in lake_data_table:
                name = data_entry.findAll('td')[0].text
                data = data_entry.findAll('td')[1].text
                lake_data_dict[name] = data

            try:
                lake_max_depth = lake_data_dict["Maximum depth"]
            except:
                lake_max_depth = "null"
            try:
                lake_altitude = lake_data_dict["Altitude"]
            except:
                lake_max_depth = "null"
            try:
                lake_volume = lake_data_dict["Volume"]
            except:
                lake_max_depth = "null"

            lake_name = lake_data_dict["Lake Name"]
            country_name = lake_data_dict["Country"]
            #lake_depth = 
            lake_data_dict = {}
            lake_data_dict[lake_name] = [lake_max_depth, lake_altitude, lake_volume, picture]
            if (country_name not in lake_country.keys()):
                lake_country[country_name] = {}
            lake_country[country_name][lake_name] = [picture, lake_max_depth, lake_altitude, lake_volume]
        continent_dict[continent_name] = lake_country
        
    # #course = all_courses[3].find('a')
    return continent_dict

def save_data_dict():
    cache_file = open(DATA_FILE_NAME, 'w')
    contents_to_write = json.dumps(DATA_DICT)
    cache_file.write(contents_to_write)
    cache_file.close()

if __name__ == "__main__":    
    CACHE_DICT = load_cache()
    DATA_DICT = initialize()
    save_data_dict()