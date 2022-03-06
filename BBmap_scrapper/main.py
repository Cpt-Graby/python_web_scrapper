import requests
from bs4 import BeautifulSoup
import random
import time

random.seed(60)


def get_page(url):
    """
      Simple funtion that get the url with requests and return a bs4 object.
      :param  (str): The string of the url
      :return: bs4 object
      """
    try:
        req = requests.get(url)
        return BeautifulSoup(req.text, 'html.parser')
    except requests.exceptions.RequestException:
        print("Could load the page: {}".format(url))


def get_link_dicegrimorium():
    """
    Funtion that returns all the links where to download the sample
    :return: list of links
    """
    bs = get_page('https://dicegrimorium.com/free-rpg-map-library/')
    try:
        content_images = bs.find_all('figure', {'class': 'wp-block-image size-large'})
        links_page = []
        for content in content_images:
            links_page.append(content.find('a').get('href'))
        return links_page
    except:
        print("""Some thing went wrong at the import of 'figure',
         {'class': 'wp-block-image size-large'}""")


def dl_zip_dicegrimorium(url, title):
    """

    :param url:
    :param title:
    :return:
    """
    try:
        r = requests.get(url, allow_redirects=True)
        with open(title + ".zip", 'wb') as dl_file:
            dl_file.write(r.content)
    except:
        print(f'Fail download: {title}')


def import_link_zip_dicegrimorium(links_pages):
    """
     Given a list, this function will get all the href off the zip file in the url that are in the list.
     """
    list_dl = []
    list_wait_time = []
    total_dl = len(links_pages)
    iteration = 1
    for i in links_pages:
        index_fail = 0
        if index_fail > 4:
            break
        try:
            """Making some verbose"""
            print(f'{iteration}/{total_dl}')
            index_fail = 0
            wait_time = random.randint(10, 90)
            list_wait_time.append(wait_time)
            """Main scraper"""
            bs = get_page(i)
            title_zip = bs.h2.text.replace(" ", "-").replace(".", "-").replace('\t', '').replace('\n', '').replace('--',
                                                                                                                   '')
            print(title_zip)
            dl_link = bs.find('figcaption').a.get('href')
            dl_zip_dicegrimorium(dl_link, title_zip)
            list_dl.append((title_zip, dl_link))
            time.sleep(wait_time)
            """verbose _done"""
            print(f'DL{iteration}/{total_dl}: done in {wait_time}')
            iteration += 1
        except:
            print(f"Somethig went wrong with the {iteration}:{i}.\n")
            index_fail += 1
    return list_dl


def main_dicegrimorium():
    all_links = get_link_dicegrimorium()
    list_zip = import_link_zip_dicegrimorium(all_links)
    return None


links = get_link_dicegrimorium()
print(import_link_zip_dicegrimorium(links))
