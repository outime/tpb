#!/usr/bin/python
#coding=UTF-8

################################################
# tuentiphotobackup (tpb)                      #
# https://github.com/outime/tpb/               #
# Ruben Diaz <outime@gmail.com>                #
################################################

import re, getpass, requests, os

path = os.path.dirname(os.path.abspath(__file__))

def init():
  if not os.path.exists(path + '/photos'):
    os.makedirs(path + '/photos')
    print "Created 'photos' directory"
  
  email = raw_input('E-mail: ')

  while( not re.match(r"[^@]+@[^@]+\.[^@]+", email) ):
    email = raw_input("Wrong e-mail, please try again: ")

  password = getpass.getpass()

  startDownload(email, password)


def startDownload(email, password):
  print "Logging in as " + email + "..."

  s = requests.Session()
  r = s.get("https://m.tuenti.com/?m=Login")
  csrf = re.findall('name="csrf" value="(.*?)"', r.text)[0]
  
  data = { "csrf": csrf, "tuentiemailaddress": email, "password": password, "remember": 1 }
  s.post("https://m.tuenti.com/?m=Login&f=process_login", data)
  
  r = s.get("https://m.tuenti.com/?m=Profile&func=my_profile")
  taggedAlbum = "https://m.tuenti.com/?m=Albums&func=index&collection_key=1-" + re.findall('key=1-(.*?)&', r.text)[0]

  r = s.get(taggedAlbum)
  firstPic = "https://m.tuenti.com/?m=Photos&func=view_album_photo&collection_key=1-" + re.findall('key=1-(.*?)&', r.text)[0]

  r = s.get(firstPic)
  picQuantity = int(re.findall('[of|de|\/|sur|di|van|z]\s(\d+)\)', r.text)[0])
  photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
  nextPhotoUrl = re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace("&amp;", "&") # not loading a whole lib for one single entity

  for x in range(1, picQuantity):
    if x != 1:
      r = s.get(nextPhotoUrl, cookies={"screen": "1920-1080-1920-1040-1-20.74"})
      photoDownloadUrl = re.findall('img\ssrc="(.*?)"', r.text)[0]
      nextPhotoUrl = re.findall('\)\s\<a href="(.*?)"', r.text)[0].replace("&amp;", "&")

    with open(path + "/photos/" + str(x) + ".jpg", "wb") as handle:
      r = s.get(photoDownloadUrl)

      for block in r.iter_content(1024):
        if not block:
          break

        handle.write(block)

    percent = (x*100) / picQuantity
    print str(x) + ".jpg downloaded (" + str(percent) + "%) ..."

  print "Done."


if __name__ == "__main__":
  version = "1.0.2"
  print "-" * 11
  print "| tpb " + version + " |"
  print "-" * 11
  init()
