#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import web_scraping_functions


class TestWebScraping(unittest.TestCase):
    def test_get_verifications(self):
        result = web_scraping_functions.get_verifications(page=1)
        self.assertEqual(len(result), 20)
        a = result[0].keys()
        b = ['screenshot_url', 'expert_opinion', 'title', 'url']
        self.assertTrue(set(a).issuperset(set(b)))

    def test_extract_text_from_image(self):
        result = web_scraping_functions.extract_text_from_image('https://sfnf-collector-prod.s3.amazonaws.com/image_20210519_100444_116126')
        expected = 'Krasnostawski lek na KORONAWIRUSA SKUTECZNE SPRAWDŹ TERAZ!'
        self.assertEqual(result, expected)

    def test_get_articles_links(self):
        result = web_scraping_functions.get_articles_links(page=1)
        self.assertEqual(len(result), 10)
        self.assertIn('https://www.termedia.pl/koronawirus', result[0])

    def test_extract_text_from_article(self):
        result = web_scraping_functions.extract_text_from_article('https://www.termedia.pl/koronawirus/Do-Polski-trafil-doustny-molnupirawir,45095.html')
        self.assertEqual(tuple, type(result))
        self.assertEqual(str, type(result[0]))
        self.assertEqual(str, type(result[1]))

if __name__ == '__main__':
    unittest.main()
    