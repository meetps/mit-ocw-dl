from HTMLParser import HTMLParser
import urllib
import os

base_url = 'http://ocw.mit.edu'
lec_url_list = []
video_url_list = []
vid_name_list = []

def findName(url):
	cut_position = url.rfind("/")
	name = url[cut_position + 1:]
	return name


class lecHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			flag = 0
			for (key,value) in attrs:
				if(value == 'bullet medialink' and key == 'class'):
					flag =1
				if(key == 'href' and flag == 1):
					print "link : ",value
					lec_name = findName(value)
					print "Lecture Name :",lec_name
					lec_url_list.append(value)
					vid_name_list.append(lec_name)
					flag = 0

class vidHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for (key,value) in attrs:
				if(value[:22] == 'http://www.archive.org' and key == 'href'):
					print "link : ",value
					video_url_list.append(value)
				break

lecLinkParser = lecHTMLParser()
f = urllib.urlopen("sample.html")
lec_html = f.read()
lecLinkParser.feed(lec_html)
lecLinkParser.close()

'''videoLinkParser = vidHTMLParser()
g = urllib.urlopen("video.html")
vid_html = g.read()
videoLinkParser.feed(vid_html)
videoLinkParser.close()'''

for lec_url in lec_url_list:
	response = urllib.urlopen(base_url + lec_url)
	html = response.read()
	videoParser = vidHTMLParser()
	videoParser.feed(html)
	videoParser.close()

i=0
for duplicate in video_url_list:
	if(i%2 == 1):
		video_url_list.remove(duplicate)
	i = i + 1

j=0
for vid_url in video_url_list:
	print "Downloading Lecture " , j , vid_name_list[j]
	urllib.urlretrieve(vid_url,vid_name_list[j]+".mp4")
	j = j + 1


