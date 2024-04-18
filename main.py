import csv
import sys
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from multiprocessing import *
from time import sleep, time
from types import NoneType
from bs4 import BeautifulSoup
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from microfunctions import *


def info(url):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    print('\nGet catalogs...')

    try:
        driver.get(url)
        check_path('catalog')
        os.chdir('catalog')
        sleep(3)
        if driver.title in site_error:
            for x in range(2):
                driver.refresh
                if driver.title in site_error:
                    sleep(3)
                else:
                    start_collect_catalog(driver, url)
                    print('Success!\n')
                    break
            else:
                print(f'\nThe page could not load or the link does not exist')
                sys.exit()
        else:
            start_collect_catalog(driver, url)
            print('Success!\n')

    except Exception as _ex:
        print(_ex)
        print('No link entered')
        sys.exit()

    finally:
        driver.close()
        driver.quit()
        os.chdir(path)


def start_collect_catalog(driver, url):
    write_html(driver, url)
    number_of_pages = check_numbers_of_pages()
    print(f'Total catalogs: {number_of_pages - 1}')
    pages = get_pages(number_of_pages, url)
    with ThreadPoolExecutor(4) as executor:
        executor.map(getting_catalog_thr, pages)


def check_numbers_of_pages():
    html_files = get_html_files()[0]
    with open(html_files, 'r') as file:
        src = file.read()
    number_page = []
    soup = BeautifulSoup(src, 'lxml')
    items_divs = soup.find('ul', class_='pagination-widget__pages')

    if type(items_divs) is NoneType:
        number_of_pages = 0
    else:
        for items in items_divs:
            number_page.append(items.get('data-page-number'))
        number_of_pages = number_page[-1]

    return int(number_of_pages) + 1


def getting_catalog_thr(url):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    try:
        driver.get(url)
        sleep(3)
        if driver.title in site_error:
            print(f'info: {url} (lost)')
            sleep(3)
            driver.refresh
        write_html(driver, url)

    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()


def get_items():
    print('Get urls...')
    os.chdir('catalog')
    html_files = get_html_files()
    urls = []
    for filename in html_files:
        with open(filename, 'r') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_divs = soup.find_all(
            'a', class_='catalog-product__name ui-link ui-link_black')
        for item in items_divs:
            item = item.get('href')
            urls.append('https://www.dns-shop.ru' + item)

    os.chdir(path)
    check_path('urls')
    os.chdir('urls')

    with open('urls.txt', 'w') as file:
        file.write("\n".join(urls))

    os.chdir(path)
    print('Success!\n')


def get_products():
    os.chdir('urls')
    with open('urls.txt', 'r') as file:
        urls = file.read().split('\n')

    os.chdir(path)
    check_path('products')
    os.chdir('products')

    print(f'Get products...')
    print(f'Total products: {len(urls)}')

    with ThreadPoolExecutor(4) as executor:
        executor.map(get_products_thr, urls)

    print('Success!')
    os.chdir(path)


def get_products_thr(url, *, div=None):
    options = Options()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    try:
        driver.get(url)
        sleep(3)

        if driver.title == site_error:
            sleep(3)
            driver.refresh
            print(f'get_product: {url} (lost)')

        if isinstance(div, int):

            element = driver.find_element(
                By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[3]/button')
            # /html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[16]/button
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            sleep(1)
            element.click()
            sleep(2)

        write_html(driver, url)

    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()


def thr_csv(filename):
    try:
        with open(filename, 'r') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        if soup.find('div', class_='product-buy__price') is None:
            options = Options()
            # options.add_argument('--headless')
            options.add_experimental_option("excludeSwitches",
                                            ["enable-automation"])

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options)
            driver.maximize_window()
            break_item = filename.split('.html')[0]
            driver.get(break_item)
            sleep(3)
            while driver.title == '404 Not Found':
                sleep(3)
                driver.refresh
                print(f'get_info_products: {break_item} (lost)')
            write_html(driver, break_item)
            driver.close()
            driver.quit()

            with open(filename, 'r') as file:
                src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        if soup.find('div', class_='product-buy__price-wrap product-buy__price-wrap_not-avail'):
            item_price = (soup.find(
                'div', class_='product-buy__price-wrap product-buy__price-wrap_not-avail')).get_text()
        else:
            item_price = (
                (soup.find('div', class_='product-buy__price')).get_text()).rpartition('₽')

        items_cl_fac = soup.find_all(
            'div', class_='product-characteristics__group')

        price = item_price[0] + item_price[1]
        price = {'Цена': price}
        data = {}
        spec = {}

        for item_group in items_cl_fac:
            title = item_group.find(
                'div', class_='product-characteristics__group-title').get_text()
            spec_title = item_group.find_all(
                'div', class_='product-characteristics__spec-title')
            spec_value = item_group.find_all(
                'div', class_='product-characteristics__spec-value')

            n = 0
            for tit in spec_title:
                spec.update({
                            (tit.get_text()).strip():
                            (spec_value[n].get_text()).strip()
                            })
                n += 1

            data.update({
                        title: spec
                        })
            spec = {}

        n = warranty_check(data)

        name, code = data[list(data.keys())[n]]['Модель'],
        filename.split('\\')[4]

        with open(f"{name.replace('/', '_')} {code}.csv", mode='w',
                  encoding='utf-8') as file:
            file_w = csv.writer(file, delimiter=',', lineterminator='\r')
            price = list(price.items())[0]

            file_w.writerow(price)
            file_w.writerow([])

            for data_items in data:
                elements = data[data_items].items()
                data_items = [data_items]
                file_w.writerow(data_items)
                for element in elements:
                    file_w.writerow(element)
                file_w.writerow([])

    except Exception as _ex:
        print(filename)
        print(_ex)
        print(data)
        with open('lost_urls.txt', 'a') as file:
            file.write(f'{filename}\n')
    finally:
        pass


def main():
    global path
    global site_error
    url = f'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?order=6&q=%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA%20%D0%B8%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9&stock=now&price=100001-543999'
    check_link_catalog(url)
    site_error = ['502 Bad Gateway', '404 Not Found', '403 Forbidden']
    path = os.getcwd()
    info(url)

    if 'product' in url:
        for work_path in ['products', 'results', 'urls']:
            if os.path.exists(work_path):
                shutil.rmtree(work_path)
        print('Get product info...')
        os.chdir('catalog')
        html_file = get_html_files()[0]
        thr_csv(html_file)
        print('Success!')

    else:
        get_items()
        get_products()
        check_path('results')
        os.chdir('products')
        html_files = get_html_files()
        with Pool(4) as executor:
            executor.map(thr_csv, html_files)
        replace_csv(path)

    check_path('results')
    os.chdir('products')
    html_files = get_html_files()
    if os.path.exists('lost_urls.txt'):
        os.remove('lost_urls.txt')
    with Pool(4) as executor:
        executor.map(thr_csv, html_files)
    replace_csv(path)

    if os.path.isfile('lost_urls.txt'):
        with open('lost_urls.txt', 'r') as file:
            urls = (file.read().split('\n'))[:-1]

        html_files = [url.replace('/', '\\') for url in urls]

        for element in range(len(urls)):
            urls[element] = urls[element].split('.html')[0]

        with ThreadPoolExecutor(4) as executor:
            futures = []
            for url in urls:
                futures.append(
                    executor.submit(
                        get_products_thr, url, div=0
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                future.result()

        if os.path.exists('lost_urls.txt'):
            os.remove('lost_urls.txt')

        with Pool(4) as executor:
            executor.map(thr_csv, html_files)
        replace_csv(path)


if __name__ == '__main__':
    start_time = time()
    main()
    print("--- %s seconds ---" % (time() - start_time))
