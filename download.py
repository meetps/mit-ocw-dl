import sys
import urllib
import os
from HTMLParser import HTMLParser
from pathlib import Path
import time

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
					print "Lecture Link : ",value
					lec_name = findName(value)
					print "Lecture Name :",lec_name
					lec_url_list.append(value)
					lec_name = "{:02.0f}_" + lec_name
					vid_name_list.append(lec_name)
					flag = 0

class vidHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			for (key,value) in attrs:
				if( key == 'href' and ( value[:22] == 'http://www.archive.org' or value[:19] == 'https://archive.org') and value.endswith( "mp4" ) ):
					try:
						if value != video_url_list[-1] :
							print "Video Link : ",value
							video_url_list.append(value)
						return
					except IndexError:
						video_url_list.append(value) # expected on first round
				break


def progress(count, block_size, total_size):
	global start_time
	global time_array
	global skip
	if count == 0:
		skip = 100
		time_array = [0]*skip
		start_time = time.time()
		return
	duration = time.time()-start_time
	progress_size = int( count * block_size)
	speed = int(progress_size/(1024*duration))
	time_left = int(( total_size - (count * block_size ))/(speed*1024))
	time_array[count % skip ] = time_left
	time_left = 0
	if count % skip:
		return
	for t in time_array:
		time_left = time_left + t
	time_left = int(time_left / skip)
	percent = int(count * block_size * 100/total_size)

	sys.stdout.write ("\r ...%d%%, %d MB, %d KB/s, %d seconds   " %
	(percent, progress_size / (1024*1024), speed, time_left))
	sys.stdout.flush()

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if( len(sys.argv) < 2 ):
	print "Must pass a URL"
	print "i.e. python download.py http://ocw.mit.edu/cources/college/course-title/video-lectures/"
	exit()
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

j=0
for vid_url in video_url_list:
	filename = Path( vid_name_list[j].format(j+1) + ".mp4" )
	print "Downloading {:02d} of {:02d}: ".format(j+1,len(video_url_list)) + filename.name
	if filename.exists():
		print "Already Downloaded: " + filename.name
	else :
		urllib.urlretrieve(vid_url, filename.name, progress)
	j = j + 1
print "Done."
