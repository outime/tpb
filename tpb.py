#!/usr/bin/python
# coding=UTF-8

##################################
# tuentiphotobackup (tpb)        #
# https://github.com/outime/tpb/ #
# Ruben Diaz <outime@gmail.com>  #
##################################

import re
import getpass
import requests
import os
from time import sleep

PATH = os.path.dirname(os.path.abspath(__file__))
BASEURI = "https://m.tuenti.com/"
dirs = ['tagged', 'uploaded']


def init():
    for dir in dirs:
        if not os.path.exists(PATH + '/' + dir):
            os.makedirs(PATH + '/' + dir)
            print "Created %s directory" % dir

    email = raw_input('E-mail: ')

    while(not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
        email = raw_input("Wrong e-mail, please try again: ")

    password = getpass.getpass()

    while not password:
        password = getpass.getpass()

    startDownload(email, password)


def startDownload(email, password):
    s = requests.Session()

    print "Logging in as %s..." % email
    r = s.get(BASEURI + "?m=Login")
    csrf = re.findall('name="csrf" value="(.*?)"', r.text)[0]
    data = {
        "csrf": csrf,
        "tuentiemailaddress": email,
        "password": password,
        "remember": 1}
    r = s.post(BASEURI + "?m=Login&f=process_login", data)

    if 'tuentiemail' in r.cookies:
        print "Wrong login :("
        init()

    for i in range(1, 3):
        r = s.get(BASEURI + "?m=Profile&func=my_profile")
        print "Downloading " + dirs[i - 1] + " photos..."
        album = BASEURI + "?m=Albums&func=index&collection_key=%i-" % i + \
            re.findall('key=%i-(.*?)&' % i, r.text)[0]

        r = s.get(album)
        firstPic = BASEURI + "?m=Photos&func=view_album_photo&collection_key=%i-" % i + \
            re.findall('key=%i-(.*?)&' % i, r.text)[0]

        r = s.get(firstPic)
        picQuantity = int(
            re.findall('[of|de|\/|sur|di|van|z]\s(\d+)\)',
                       r.text)[0])
        photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
        if picQuantity > 1:
            nextPhotoUrl = re.findall(
                '\)\s\<a href="(.*?)"',
                r.text)[0].replace("&amp;",
                                   "&")  # not loading a whole lib for one single entity
        else:
            nextPhotoUrl = None

        for x in range(1, picQuantity + 1):
            if x != 1:
                r = s.get(
                    nextPhotoUrl,
                    cookies={"screen": "1920-1080-1920-1040-1-20.74"})
                photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
                if x != picQuantity:
                    nextPhotoUrl = re.findall(
                        '\)\s\<a href="(.*?)"',
                        r.text)[0].replace("&amp;",
                                           "&")

            with open(PATH + "/" + dirs[i - 1] + "/" + str(x) + ".jpg", "wb") as handle:
                r = s.get(photoDownloadUrl)

                for block in r.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)

            percent = (x * 100) / picQuantity
            print "%s.jpg downloaded (%i%%)... (album %i/2)" % (x, percent, i)
            sleep(0.5)  # avoid flooding

        print "Done!"


if __name__ == "__main__":
    print "~ tpb ~"
    try:
        init()
    except KeyboardInterrupt:
        pass
