import ctypes
import os
from random import choice

import requests
from settings import *
from bs4 import BeautifulSoup
from lxml import etree


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r


def download_picture(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('picture.jpeg', 'wb') as f:
            f.write(r.content)


def randomize_picture(urls):
    return "https:" + choice(urls)


def get_urls_pictures(dom):
    return dom.xpath('//*[@class="image-gallery-image__inner"]/@href')


def get_picture(html):
    soup = BeautifulSoup(html, "html.parser")
    dom = etree.HTML(str(soup))

    urls = get_urls_pictures(dom)

    url = randomize_picture(urls)

    html_picture = get_html(url)

    dom = etree.HTML(html_picture.text)

    picture_url = dom.xpath('//*[@id="main-image"]/@src')[0]

    download_picture(picture_url)


def main(tags):

    url = f'https://ru.wallpaper.mob.org/pc/gallery/tag={tags}/'

    html = get_html(url)

    get_picture(html.text)

    set_picture_desktop()


def set_picture_desktop():
    path = os.getcwd() + "\\picture.jpeg"
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


if __name__ == "__main__":
    main('3d')
