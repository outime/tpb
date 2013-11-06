#!/usr/bin/python
#coding=UTF-8

##################################
# tuentiphotobackup (tpb)        #
# https://github.com/outime/tpb/ #
# Ruben Diaz <outime@gmail.com>  #
##################################

import re, getpass, requests, os
from time import sleep

path = os.path.dirname(os.path.abspath(__file__))
dirs = ['tagged', 'uploaded']

def init():
  for dir in dirs:
    if not os.path.exists(path + '/' + dir):
      os.makedirs(path + '/' + dir)
      print "Created %s directory" % dir
  
  email = raw_input('E-mail: ')

  while( not re.match(r"[^@]+@[^@]+\.[^@]+", email) ):
    email = raw_input("Wrong e-mail, please try again: ")

  password = getpass.getpass()

  startDownload(email, password)


def startDownload(email, password):
  print "Logging in as %s..." % email
  
  s = requests.Session()
  r = s.get("https://m.tuenti.com/?m=Login")
  csrf = re.findall('name="csrf" value="(.*?)"', r.text)[0]

  data = { "csrf": csrf, "tuentiemailaddress": email, "password": password, "remember": 1 }
  s.post("https://m.tuenti.com/?m=Login&f=process_login", data)
  
  for i in range(1,3):
    r = s.get("https://m.tuenti.com/?m=Profile&func=my_profile")
    print "Downloading " + dirs[i-1] + " photos"
    album = "https://m.tuenti.com/?m=Albums&func=index&collection_key=%i-" % i + re.findall('key=%i-(.*?)&' % i, r.text)[0]

    r = s.get(album)
    firstPic = "https://m.tuenti.com/?m=Photos&func=view_album_photo&collection_key=%i-" % i + re.findall('key=%i-(.*?)&' % i, r.text)[0]

    r = s.get(firstPic)
    picQuantity = int(re.findall('[of|de|\/|sur|di|van|z]\s(\d+)\)', r.text)[0])
    photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
    if picQuantity > 1:
      nextPhotoUrl = re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace("&amp;", "&") # not loading a whole lib for one single entity
    else:
      nextPhotoUrl = None

    for x in range(1, picQuantity + 1):
      if x != 1:
        r = s.get(nextPhotoUrl, cookies={"screen": "1920-1080-1920-1040-1-20.74"})
        photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
        if x != picQuantity:
          nextPhotoUrl = re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace("&amp;", "&")

      with open(path + "/"+ dirs[i-1]+ "/" + str(x) + ".jpg", "wb") as handle:
        r = s.get(photoDownloadUrl)

        for block in r.iter_content(1024):
          if not block:
            break

          handle.write(block)

      percent = (x*100) / picQuantity
      print "%s.jpg downloaded (%i%%)... (%i/2)" % (x, percent, i)
      sleep(0.5) # avoid flooding

    print "Done."


if __name__ == "__main__":
  version = 1.1
  print "~ tpb %s ~" % version
  init()
