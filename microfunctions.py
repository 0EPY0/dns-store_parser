import os
import shutil
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# def check_catalog_or_product(url):
#     return 'product' in url


def get_pages(number_of_pages, url):
    pages = []
    # url_check = url.split('?order=')
    # print(url_check)
    if '?' in url:
        for page in range(2, number_of_pages):
            url_next = url + '&p=' + str(page)
            pages.append(url_next)
    else:
        for page in range(2, number_of_pages):
            url_next = url + '?p=' + str(page)
            pages.append(url_next)

    return pages


# def next_url(url, n):
#     return url + '&p=' + str(n)


# def get_pages(number_of_pages, url):
#     pages = []

#     for page in range(2, number_of_pages):
#         url_next = url + '&p=' + str(page)
#         pages.append(url_next)

#     return pages


def replace_csv(path):
    csv_files = []
    for csv in os.listdir(os.getcwd()):
        if 'csv' in csv:
            csv_files.append(csv)

    for g in csv_files:
        os.replace(path + '/products/' + g, path + '/results/' + g)


def check_files():
    os.chdir('products')
    html_files = []
    for filename in os.listdir(os.getcwd()):
        if 'html' in filename:
            html_files.append(filename)

    csv_files = []
    for filename in os.listdir(os.getcwd()):
        if 'csv' in filename:
            csv_files.append(filename)


def get_html_files():
    html_files = []
    for filename in os.listdir(os.getcwd()):
        if 'html' in filename:
            html_files.append(filename)
    return html_files


def write_html(driver, url):
    url = url.replace('/', '\\')
    with open(f'{url}.html', 'w') as file:
        file.write(driver.page_source)


def check_element(driver, type_element, element):
    try:
        driver.find_element(type_element, f'{element}')
    except Exception as _ex:
        return False
    return True


def check_link_catalog(url):
    if 'dns-shop' in url:
        pass
    else:
        print('A link from another site has been entered')
        sys.exit()


def check_path(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        os.mkdir(dir)
    else:
        os.mkdir(dir)


# def check_button(driver, n):
#     try:
#         driver.find_element(By.XPATH, f'/html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[{n}]/button')
#         '''
#         /html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[3]/button
#         /html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[3]/button
#         /html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[2]/div[3]/button

#         /html/body/div[2]/div[4]/div[2]/div[1]/div/div[1]/div[3]/div[16]/button
#         '''

#     except:
#         check_button(driver, )


def warranty_check(data):
    if 'Модель' not in data[list(data.keys())[1]]:
        n = 0
    else:
        n = 1
    return n
