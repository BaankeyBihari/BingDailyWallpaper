#! /usr/local/bin/python3

from urllib.request import urlopen, urlretrieve
from xml.dom import minidom
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
save_dir = os.path.join(dir_path, 'Album')
if not os.path.exists(save_dir):
	os.makedirs(save_dir)

def download_wallpaper(from_archive=False, max_penalty=10):
	do_task = True
	penalty = 0
	idx = 0
	while do_task:
		if penalty >= max_penalty:
			print("Used all penalties, ", penalty)
			return
		try:
			xrep = urlopen(''.join(['http://www.bing.com/HPImageArchive.aspx?format=xml&idx=',
						str(idx), '&n=1&mkt=ru-RU']))
		except Exception as e:
			print("Error downloading xml for #", idx, e)
			return
		try:
			xmldoc = minidom.parse(xrep)
		except Exception as e:
			print("Error parsing xml for #", idx, e)
			return
		urlx = xmldoc.getElementsByTagName('url')[0]
		picurl = 'http://www.bing.com' + urlx.firstChild.nodeValue
		picurl = picurl.replace('_1366x768', '_1920x1200')
		picname = picurl[picurl.rfind('/')+1:]
		picpath = os.path.join(save_dir, picname)
		if os.path.isfile(picpath):
			print(picname, " is already downloaded for #", idx)
			penalty += 1
		else:
			print("Downloading ", picname, " for #", idx)
			try:
				urlretrieve(picurl, picpath)
			except Exception as e:
				print("Error downloading ", filename, " for #", idx)
				return
		idx += 1
		if not from_archive:
			return

if __name__ == "__main__":
	download_wallpaper(True, 10)
