import sys
import urllib.request
import os
from html.parser import HTMLParser
from pathlib import Path
import time
import multiprocessing
from multiprocessing import freeze_support

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
					print("Lecture Link : ",value)
					lec_name = findName(value)
					print("Lecture Name :",lec_name)
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
							print("Video Link : ",value)
							video_url_list.append(value)
						return
					except IndexError:
						video_url_list.append(value) # expected on first round
				break

if( len(sys.argv) < 2 ):
	print ("Must pass a URL")
	print ("i.e. python download.py http://ocw.mit.edu/cources/college/course-title/video-lectures/")
	exit()

lecLinkParser = lecHTMLParser()
f = urllib.request.urlopen(str(sys.argv[1]))
lec_html = f.read()
lecLinkParser.feed(str(lec_html))
lecLinkParser.close()

for lec_url in lec_url_list:
	response = urllib.request.urlopen(base_url + lec_url)
	html = response.read()
	videoParser = vidHTMLParser()
	videoParser.feed(str(html))
	videoParser.close()

def download_video(vid_args):
	vid_url = vid_args[0]
	vid_name = vid_args[1]
	seq = vid_args[2]
	filename = Path(vid_name.format(seq) + ".mp4" )
	print("Downloading",filename.name,".....")
	if filename.exists():
		print ("Already Downloaded: " + filename.name)
	else :
		urllib.request.urlretrieve(vid_url, filename.name)

def main():		
	freeze_support()
	pool = multiprocessing.Pool(processes=10) #use 10 processes for fast downloading, IO takes time 
	output = pool.map(download_video,zip(video_url_list,vid_name_list,list(range(1,len(video_url_list)+1)))) 
	print ("Done.") 

if __name__ == "__main__":
    main()
	