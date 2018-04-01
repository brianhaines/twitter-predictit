#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio



async def getCounts(session, url):
	async with session.get(url) as response:
		return await response.read()

async def run():
	handles = [
	'potus',
	'vp', 
	'whitehouse', 
	'realdonaldtrump'
	]

	t = 'https://twitter.com/'
	
	async with aiohttp.ClientSession() as session:
		tasks = [getCounts(session, t + handle) for handle in handles]
		results = await asyncio.gather(*tasks)
	
	for h, r in zip(handles, results):
		soup = BeautifulSoup(r,'html.parser')
		s = soup.find("span", class_="ProfileNav-value")
		print('{0}: {1}'.format(h, s['data-count']))


if __name__ == '__main__':
	import time
	start_time = time.perf_counter()
	loop = asyncio.get_event_loop()
	r = loop.run_until_complete(run())
	loop.close()
	end_time = time.perf_counter()
	print('Runtime was: {0}'.format(end_time - start_time))