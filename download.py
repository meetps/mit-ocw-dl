import sys
import urllib
import os
from HTMLParser import HTMLParser

base_url = 'http://ocw.mit.edu'
lec_url_list = []
video_url_list = []
vid_name_list = []
video_url_list_final = []


def findName(url):
    cut_position = url.rfind("/")
    name = url[cut_position + 1:]
    return name


class lecHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            flag = 0
            for (key, value) in attrs:
                if value == 'bullet medialink' and key == 'class':
                    flag = 1
                if key == 'href' and flag == 1:
                    print "link : ", value
                    lec_name = findName(value)
                    print "Lecture Name :", lec_name
                    lec_url_list.append(value)
                    vid_name_list.append(lec_name)
                    flag = 0


class vidHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if value[:22] == 'http://www.archive.org' and key == 'href':
                    print "link : ", value
                    video_url_list.append(value)
                break


# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

lecLinkParser = lecHTMLParser()
f = urllib.urlopen(str(sys.argv[1]))
lec_html = f.read()
lecLinkParser.feed(lec_html)
lecLinkParser.close()

for lec_url in lec_url_list:
    response = urllib.urlopen(base_url + lec_url)
    html = response.read()
    videoParser = vidHTMLParser()
    videoParser.feed(html)
    videoParser.close()

i = 0
for duplicate in video_url_list:
    i = i + 1
    if i % 2 == 1:
        video_url_list_final.append(duplicate)

j = 0
for vid_url in video_url_list_final:
    print "Downloading Lecture ", j + 1, vid_name_list[j]
    urllib.urlretrieve(vid_url, vid_name_list[j] + ".mp4")
    j = j + 1
