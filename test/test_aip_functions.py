#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import aip_functions as aip
import requests
from bs4 import BeautifulSoup
from airports import airports
import os
import shutil

base_url = 'https://aip.enaire.es/AIP/'
pdf = 'LE_AD_2_LEAM_SID_3_en.pdf'
url_long = 'https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/LEAM/LE_AD_2_LEAM_SID_3_en.pdf'


class TestAipFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = requests.get(url=base_url)
        cls.soup = BeautifulSoup(r.content, "html.parser")

    def test_file_name(self):
        """Test if the function returns a pdf file name"""
        self.assertEqual(aip.file_name(
            'https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/LEAM/LE_AD_2_LEAM_SID_3_en.pdf'
        ), 'LE_AD_2_LEAM_SID_3_en.pdf')
        self.assertTrue(type(aip.file_name(
            'https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/LEAM/LE_AD_2_LEAM_SID_3_en.pdf'
        )), 'The file_name is not a str')
        self.assertIn('.pdf', aip.file_name(
            'https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/LEAM/LE_AD_2_LEAM_SID_3_en.pdf'
        ), 'File is not a pdf')

    def test_create_url(self):
        """Test if a URL is created"""
        self.assertRegex(
            aip.create_url(base_url, pdf),
            r'https.*\.pdf',
            'Invalid URL format'
        )
        self.assertEqual(
            len(aip.create_url(base_url, pdf)),
            len(base_url + pdf),
            'Join failure'
        )

    def test_parse_pdf(self):
        """Test if airport charts are parsed from soup"""
        self.assertIn('.pdf',
                      aip.parse_pdf(self.soup)[0],
                      'No pdf file_name in soup')
        self.assertTrue(aip.parse_pdf(self.soup),
                        'List of pdf files is empty')

    def test_create_path(self):
        """Test parent folder name format"""
        self.assertEqual(len(aip.create_path(self.soup)),
                         21,
                         'Invalid folder name')

    def test_create_airport_folders(self):
        """Test if folder structure is created"""
        aip.create_airport_folders(airports,
                                   0o755,
                                   self.soup)
        self.assertTrue(os.path.exists(
            aip.create_path(self.soup)))

    @classmethod  # new
    def tearDownClass(cls):
        shutil.rmtree(aip.create_path(cls.soup))


if __name__ == '__main__':
    unittest.main()
