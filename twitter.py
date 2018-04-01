#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

def getCounts(handle):
	r = requests.get('https://twitter.com/'+handle)
	soup = BeautifulSoup(r.text,'html.parser')
	s = soup.find("span", class_="ProfileNav-value")
	return s['data-count']

if __name__ == '__main__':
	import time
	start_time = time.perf_counter()

	handles = ['potus','vp', 'whitehouse', 'realdonaldtrump']
	for handle in handles:
		s = getCounts(handle)
		print('{0}: {1}'.format(handle,s))
	
	end_time = time.perf_counter()
	print('Runtime was: {0}'.format(end_time - start_time))