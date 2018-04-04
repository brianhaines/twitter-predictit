#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import json
import re


class TwitterMarkets(object):
	"""docstring for TwitterMarkets"""
	def __init__(self):
		super(TwitterMarkets, self).__init__()

	def getTwitters(self):
		#url = 'https://www.predictit.org/home/browse?Search=twitter&isSearch=true'
		url = 'https://www.predictit.org/api/marketdata/all/'
		r = requests.get(url)
		soup = BeautifulSoup(r.text,'lxml')
		d = json.loads(soup.p.contents[0])

		n = 0
		handleIDs = {}
		for i in d['Markets']:
			if 'tweets' in i['ShortName']:
				handle = i['ShortName'].split(' ')[0][1:]
				handleIDs[handle]=i['ID']
		return handleIDs

	async def getStartingTweets(self, session, url,mid,handle):
		async with session.get(url+mid) as response:
			res = await response.read()
		return {handle: res}
	

	async def run(self, markets):
		url = 'https://www.predictit.org/Market/' 

		async with aiohttp.ClientSession() as session:
			#[print(str(v)) for k, v in markets.items()]
			tasks = [self.getStartingTweets(session, url, str(mid), handle) for handle, mid in markets.items()]
			results = await asyncio.gather(*tasks)

		output = {}
		
		#for ids, r in zip(market, results):
		
		for result in results:
			for k, v in result.items():
				soup = BeautifulSoup(v,'html.parser')
				#print(soup)
				s = soup.find("div", class_="tab-c").p.contents[0]
				tweets = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)",s)
				#print('{0}: {1}'.format(k,tweets[0]))
				output[k] = tweets[0]
		return output

if __name__ == '__main__':
	import time

	twm = TwitterMarkets()

	# Get all twitter markets from the API
	markets = twm.getTwitters()

	# Scrape market listing to get the market's starting tweet count
	loop = asyncio.get_event_loop()
	startingTweets = loop.run_until_complete(twm.run(markets))
	loop.close()


	for k, v in startingTweets.items():
		print('{0}: {1}'.format(k, v))


	




	#start_time = time.perf_counter()
	#loop = asyncio.get_event_loop()
	#r = loop.run_until_complete(run(handles))
	#loop.close()
	#end_time = time.perf_counter()
	#for key, value in r.items():
	#	print('{0}: {1}'.format(key,value))
	#print('Runtime was: {0}'.format(end_time - start_time))