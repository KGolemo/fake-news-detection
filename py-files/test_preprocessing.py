#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import preprocessing_functions

class TestPreprocessing(unittest.TestCase):
    def test_drop_title_and_url(self):
        df_input = pd.DataFrame(columns=['Verdict', 'Title', 'Text', 'Url'])
        df_expected = pd.DataFrame(columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_title_and_url(df_input).columns[1], df_expected.columns[1])

    def test_drop_empty(self):
        df_input = pd.DataFrame(data=[['false', 'tekst1'],
                                      ['true', None]],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[['false', 'tekst1']],
                                   columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_empty(df_input)['Text'].iloc[-1], df_expected['Text'].iloc[-1])

    def test_drop_non_polish(self):
        df_input = pd.DataFrame(data=[['false', 'english test article'],
                                      ['true', 'polski testowy artykuł']],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[['true', 'polski testowy artykuł']],
                                   columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_non_polish(df_input)['Text'].iloc[0], df_expected['Text'].iloc[0])

    def test_drop_unidentified(self):
        df_input = pd.DataFrame(data=[['unidentified', 'tekst1'],
                                      ['true', 'tekst2']],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[['true', 'tekst2']],
                                   columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_unidentified(df_input)['Text'].iloc[0], df_expected['Text'].iloc[0])

    def test_drop_twitter(self):
        df_input = pd.DataFrame(data=[['false', 'Nowy na Twitterze'],
                                      ['true', 'tekst2']],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[['true', 'tekst2']],
                                   columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_twitter(df_input)['Text'].iloc[0], df_expected['Text'].iloc[0])

    def test_change_verdict_dtype(self):
        df_input = pd.DataFrame(data=[['false', 'tekst1'],
                                      ['true', 'tekst2']],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[[False, 'tekst1'],
                                         [True, 'tekst2']],
                                   columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.change_verdict_dtype(df_input)['Verdict'].iloc[0], df_expected['Verdict'].iloc[0])

    def test_drop_short(self):
        df_input = pd.DataFrame(data=[[False, 4 * 'tekst1'],
                                      [True, 5 * 'tekst2']],
                                columns=['Verdict', 'Text'])
        df_expected = pd.DataFrame(data=[[True, 5 * 'tekst2']], columns=['Verdict', 'Text'])
        self.assertEqual(preprocessing_functions.drop_short(df_input)['Text'].iloc[0], df_expected['Text'].iloc[0])

    def test_delete_escape_chars(self):
        input = 'klasyfikacja\\ntekstu\nz\twykorzystaniem\ruczenia maszynowego'
        expected = 'klasyfikacja tekstu z wykorzystaniem uczenia maszynowego'
        self.assertEqual(preprocessing_functions.delete_escape_chars(input), expected)

    def test_strip_non_polish(self):
        input = 'klasyfikacjaĕ!"(),012ätekstu'
        expected = 'klasyfikacja          tekstu'
        self.assertEqual(preprocessing_functions.strip_non_polish(input), expected)

    def test_replace_whitespace(self):
        input = 'klasyfikacja' + 5 * ' ' + 'tekstu'
        expected = 'klasyfikacja tekstu'
        self.assertEqual(preprocessing_functions.replace_whitespace(input), expected)

    def test_lowercase_all(self):
        input = 'KlaSYfikAcJA teKSTu'
        expected = 'klasyfikacja tekstu'
        self.assertEqual(preprocessing_functions.lowercase_all(input), expected)

    def test_tokenize(self):
        input = 'klasyfikacja tekstu z wykorzystaniem uczenia maszynowego'
        expected = ['klasyfikacja', 'tekstu', 'z', 'wykorzystaniem', 'uczenia', 'maszynowego']
        self.assertListEqual(preprocessing_functions.tokenize(input), expected)

    def test_delete_stop_words(self):
        input = ['przy', 'klasyfikacji', 'tekstu', 'z', 'wykorzystaniem', 'przede', 'wszystkim', 'uczenia', 'maszynowego']
        expected = ['klasyfikacji', 'tekstu', 'wykorzystaniem', 'uczenia', 'maszynowego']
        self.assertListEqual(preprocessing_functions.delete_stop_words(input), expected)

    def test_lemmatize(self):
        input = ['klasyfikacji', 'tekstu', 'wykorzystaniem', 'uczenia', 'maszynowego']
        df_input = pd.DataFrame([[input]], columns=['Text'])
        expected = 'klasyfikacja tekst wykorzystać uczyć maszynowy'
        df_expected = pd.DataFrame([[expected]], columns=['Text'])
        self.assertEqual(preprocessing_functions.lemmatize(df_input)['Text'].iloc[0], df_expected['Text'].iloc[0])
