#!/usr/bin/python
# -*- coding: utf-8 -*-

# Rubén Díaz <outime@gmail.com>
# https://github.com/outime/tpb

import re
import os
import sys
import logging
from time import sleep

import requests

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
logger = logging.getLogger(__name__)

CWD = os.getcwdu()
MOBILE_TUENTI_URL = 'https://m.tuenti.com/'
CATEGORIES = ['tagged', 'uploaded']

class Tpb():

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.is_authenticated = False
        self.r_s = None

        self._check_directories()
        self._do_login()

    def _update_progress(self, current, total):
        progress = (current * 100) / total
        sys.stdout.write('\r%d%% (%s / %s)' % (progress, current, total))
        sys.stdout.flush()

    def _check_directories(self):
        """
        Checks if directories in CATEGORIES exist in
        CWD, otherwise creates them.
        """
        for category in CATEGORIES:
            directory = CWD + '/photos/' + category
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info('Created {0} directory'.format(directory))

    def _do_login(self):
        """
        Verifies credentials against the site.
        """
        self.r_s = requests.Session()

        logger.info('Authenticating as {0}...'.format(self.user))
        r = self.r_s.get('{0}?m=Login'.format(MOBILE_TUENTI_URL))
        csrf = re.findall('name="csrf" value="(.*?)"', r.text)[0]

        login_url = '{0}?m=Login&f=process_login'.format(MOBILE_TUENTI_URL)
        form_data = {
                "csrf": csrf,
                "tuentiemailaddress": self.user,
                "password": self.password,
                "remember": 1
                }
        r = self.r_s.post(login_url, form_data)

        if 'tuentiemail' in r.cookies:
            raise ValueError('User or password is not valid.')

        self.is_authenticated = True

    def download_photos(self):
        """
        Downloads the photos to the local storage.
        """
        for i in range(1,3):
            current_category = CATEGORIES[i - 1]
            logger.info('Downloading "{0}" photos'.format(current_category))

            r = self.r_s.get('{0}?m=Profile&func=my_profile'.format(MOBILE_TUENTI_URL))
            collection_key = re.findall('key=%i-(.*?)&' % i, r.text)[0]
            collection_url = '{0}?m=Albums&func=index&collection_key={1}-{2}'.format(MOBILE_TUENTI_URL, i, collection_key)

            r = self.r_s.get(collection_url)
            collection_key = re.findall('key=%i-(.*?)&' % i, r.text)[0]
            first_photo_url = '{0}?m=Photos&func=view_album_photo&collection_key={1}-{2}'.format(MOBILE_TUENTI_URL, i, collection_key)

            r = self.r_s.get(first_photo_url)
            number_of_photos = int(re.findall('[of|de|\/|sur|di|van|z]\s(\d+)\)', r.text)[0])
            next_photo_url = None
            if number_of_photos > 1:
                next_photo_url =  re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace('&amp;', '&')

            for n in range(1, number_of_photos+1):
                if n > 1:
                    r = self.r_s.get(next_photo_url, cookies={"screen": "1920-1080-1920-1040-1-20.74"})
                    photo_url = re.findall('img\ssrc="(.*?)"', r.text)[0]
                    if n != number_of_photos:
                        next_photo_url = re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace('&amp;', '&')

                with open('{0}/photos/{1}/{2}.jpg'.format(CWD, current_category, n), 'wb') as handle:
                    r = self.r_s.get(next_photo_url)
                    for block in r.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)

                self._update_progress(n, number_of_photos)
                sleep(0.4)

            logger.info('All pictures were downloaded successfully.')
