#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import numpy as np
import cv2
import easyocr
from typing import Dict, List, Tuple


def get_verifications(page: int) -> Dict[str, str]:
    """Gets news verifications from fakehunter.pap.pl.

    Args:
        page (int): Page number of fakehunter.pap.pl to process.

    Returns:
        verifications (Dict[str, str]): Dictionary of web page content.
    """
    url = 'https://panel-api.fakehunter.pap.pl/news/published/news?category=koronawirus&domains%5B%5D=koronawirus&page=' + str(page)
    # print(f'Processing page {page}: {url}')
    res = requests.get(url)  
    res.encoding = 'utf-8'                            
    data = res.json()
    verifications = data['results']
    return verifications


reader = easyocr.Reader(['pl'])  # Load the OCR Reader object


def extract_text_from_image(url: str) -> str:
    """Performs OCR on the screenshot of an article.

    Args:
        url (str): URL of the screenshot.

    Returns:
        text (str): Extracted text.
    """
    res = requests.get(url)
    arr = np.asarray(bytearray(res.content), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    result = reader.readtext(img, decoder='beamsearch', detail=0, 
                            paragraph=True, y_ths=4, min_size=200, width_ths=1, 
                            allowlist='#0123456789ABCDEFGHIJKLŁMNOPRSŚTUVWXYZŻŹaąbcćdeęfghijklłmnńoóprstuwyzżź .,-?:-!"()')
    text = ' '.join(result)
    return text


def get_articles_links(page: int) -> List[str]:
    """Gets links to articles from termedia.pl.

    Args:
        page (int): Page number of termedia.pl to process.

    Returns:
        links (List[str]): List of links to articles.
    """
    url = 'https://www.termedia.pl/koronawirus/?&p=' + str(page)
    # print(f'Processing page {page}: {url}')
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    links = ['https://www.termedia.pl' + art.find('a')['href'].strip()
             for art in soup.find_all('div', attrs={'class': 'pl2Pos'})]
    return links


def extract_text_from_article(url: str) -> Tuple[str, str]:
    """Gets the article's title and content.

    Args:
        url (str): URL of the article.

    Returns:
        (Tuple [str, str]): Tuple containing:
            title (str): Article's title.
            text (str): Article's content.
    """
    res = requests.get(url)
    res.encoding = 'utf-8'                             
    soup_art = BeautifulSoup(res.text, 'html.parser')
    title = soup_art.find('div', attrs={'class': 'pageTitle'}).text
    try:
        text = ' '.join([t.text for t in soup_art.find_all('div', attrs={'class': 'articleContent'})])
    except AttributeError:
        text = ''
    return title, text
